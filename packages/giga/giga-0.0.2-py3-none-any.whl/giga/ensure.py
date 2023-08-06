import giga
from lura.hash import hashs
from shlex import quote

log = giga.logs.get_logger(__name__)

class BaseEnsurer:

  def __init__(self, task):
    super().__init__()
    self.task = task
    self.system = task.config.system

  def item(self, *args, **kwargs):
    return self.task.item(*args, **kwargs)

class Fs(BaseEnsurer):

  def directory(self, path):
    'Ensure a directory exists.'

    sys = self.system
    with self.item(f'directory {path}'):
      if not sys.isdir(path):
        sys.mkdirp(path)
        +self.task

  def file(self, path):
    'Ensure a file exists.'

    sys = self.system
    with self.item(f'file {path}'):
      if not sys.isfile(path):
        sys.touch(path)
        +self.task

  def symlink(self, src, dst):
    'Ensure a symlink exists.'

    sys = self.system
    with self.item(f'symlink {dst}'):
      if not sys.islink(dst):
        sys.lns(src, dst)
        +self.task

  def mode(self, path, mode):
    'Ensure a file mode on a path.'

    sys = self.system
    with self.item(f'mode {oct(mode)[2:]} {path}'):
      if not sys.ismode(path, mode):
        sys.chmod(path, mode)
        +self.task

  def owner(self, path, owner):
    'Ensure an owner on a path.'

    sys = self.system
    with self.item(f'owner {owner} {path}'):
      if not sys.isowner(path, owner):
        sys.chown(path, owner)
        +self.task

  def group(self, path, group):
    'Ensure a group on a path.'

    sys = self.system
    with self.item(f'group {group} {path}'):
      if not sys.isgroup(path, group):
        sys.chgrp(path, group)
        +self.task

  def contents(self, path, contents):
    'Ensure the contents of a file.'

    sys = self.system
    alg = 'sha512'
    with self.item(f'contents {path}'):
      if sys.isfile(path):
        if sys.hash(path, alg) == hashs(contents, alg):
          return
      sys.dumps(path, contents)
      +self.task

  def contains(self, path, contents):
    'Ensure contents are present in a file.'

    sys = self.system
    with self.item(f'contains {path}'):
      if sys.isfile(path):
        if contents not in sys.loads(path):
          sys.appends(path, contents)
          +self.task
      else:
        sys.dumps(path, contents)
        +self.task

  def absent(self, path):
    'Ensure the absence of a file or directory.'

    sys = self.system
    with self.item(f'absent {path}'):
      if sys.exists(path):
        sys.rmrf(path)
        +self.task

  def append(self, path, data):
    'Ensure data is appended to file at path if not already present.'

    sys = self.system
    with self.item(f'contains {path}'):
      if not sys.contains(path, data):
        sys.append(path, data)
        +self.task

  def backuponce(self, path):
    'Create a backup of path ending with .dist if one does not already exist.'

    sys = self.system
    end = '.dist'
    backup = f'{path}{end}'
    with self.item(f'backuponce {backup}'):
      if not sys.exists(backup):
        sys.cpf(path, backup)
        +self.task

  def in_file(self, path, data, encoding=None):
    'Ensure data is present in file at path by appending it when absent.'

    sys = self.system
    with self.item(f'in_file {path}'):
      if not (sys.exists(path) and sys.contains(path, data, encoding=encoding)):
        sys.appends(path, data, encoding=encoding)
        +self.task

  def not_in_file(self, path, data, count=-1, encoding=None):
    'Ensure data is absent from file at path.'

    sys = self.system
    with self.item(f'not_in_file {path}'):
      if sys.exists(path):
        buf = sys.loads(path, encoding=encoding).replace(data, '', count)
        self.contents(path, buf)

  def pseudofs(self, path, value):
    'Ensure the value of a pseudo-fs (proc, sys) file.'

    sys = self.system
    path, value = quote(path), quote(str(value))
    with self.item(f'psuedofs {path}'):
      if sys.nonzero(f'test $(cat {path}) = {value}'):
        sys(f'tee {path} <<< {value}') # FIXME
        +self.task

class Systemd(BaseEnsurer):

  def started(self, service):
    sys = self.system
    with self.item(f'started {service}'):
      if sys.nonzero(f'systemctl status {service}'):
        sys(f'systemctl start {service}')
        +self.task

  def stopped(self, service):
    sys = self.system
    with self.item(f'stopped {service}'):
      if sys.zero(f'systemctl status {service}'):
        sys(f'systemctl stop {service}')
        +self.task

  def enabled(self, service):
    sys = self.system
    with self.item(f'enabled {service}'):
      if sys.nonzero(f'systemctl is-enabled {service}'):
        sys(f'systemctl enable {service}')
        +self.task

  def disabled(self, service):
    sys = self.system
    with self.item(f'disabled {service}'):
      if sys.zero(f'systemctl is-enabled {service}'):
        sys(f'systemctl disable {service}')
        +self.task

  def enabled_and_started(self, service):
    self.enabled(service)
    self.started(service)

  def disabled_and_stopped(self, service):
    self.disabled(service)
    self.stopped(service)

  def reloaded(self):
    with self.item('daemon-reload'):
      self.system('systemctl daemon-reload')
      +self.task

class Git(BaseEnsurer):

  def cloned(self, dir, repo, branch=None):
    sys = self.system
    with self.item(f'cloned {dir}'):
      if not sys.isdir(dir):
        if branch:
          sys(f'git clone -b {branch} {repo} {dir}')
        else:
          sys(f'git clone {repo} {dir}')
        +self.task

  def pulled(self, dir):
    sys = self.system
    with self.item(f'pulled {dir}'):
      sys('git remote update', cwd=dir)
      ref = sys.stdout("git branch --format '%(refname)'", cwd=dir)
      behind = sys.stdout(f'git revlist --count HEAD..{ref}', cwd=dir)
      if int(behind) > 0:
        sys('git pull --all', cwd=dir)
        +self.task

class Ensure:

  def __init__(self, task):
    super().__init__()
    self.fs = Fs(task)
    self.systemd = Systemd(task)
    self.git = Git(task)
