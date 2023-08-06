import giga
import invoke
import os
from contextlib import contextmanager
from lura import run
from lura import ssh
from lura.attrs import attr
from lura.attrs import ottr
from lura.hash import hashs
from shlex import quote

log = giga.logs.get_logger(__name__)

super_ = super

class Gnu:

  def __init__(self, system):
    super().__init__()
    self.system = system

  def stat(self, argv):
    return self.system.stdout(f'stat {argv}').rstrip()

  def isfifo(self, path):
    if self.system.exists(path):
      return self.stat(f'-c %F {quote(path)}') == 'fifo'
    return False

  def ismode(self, path, mode):
    sys = self.system
    if sys.exists(path):
      if isinstance(mode, int):
        mode = oct(mode)[2:]
      file_mode = self.stat(f'-c %a {quote(path)}')
      return mode == file_mode
    return False

  def isowner(self, path, owner):
    sys = self.system
    if sys.exists(path):
      return self.stat(f'-c %U {quote(path)}') == owner
    return False

  def isgroup(self, path, group):
    sys = self.system
    if sys.exists(path):
      return self.stat(f'-c %G {quote(path)}') == group
    return False

  def ls(self, path, long=False):
    argv = f'/bin/ls -a --indicator-style=none {quote(path)}|cat'
    files = self.system.stdout(argv).rstrip('\n').split('\n')
    files = (_ for _ in files if _ not in ('.', '..'))
    if long:
      return [os.path.join(path, _) for _ in files]
    else:
      return list(files)

  def readlink(self, path, canonical=True):
    sys = self.system
    path = quote(path)
    if canonical:
      return sys.stdout(f'readlink -f {path}').rstrip()
    else:
      return sys.stdout(f'readlink {path}').rstrip()

class Bsd:

  def __init__(self, system):
    super().__init__()
    self.system = system

  def isfifo(self, path):
    raise NotImplementedError() # FIXXME

  def ismode(self, path, mode):
    raise NotImplementedError() # FIXXME

  def isowner(self, path, owner):
    raise NotImplementedError() # FIXXME

  def isgroup(self, path, group):
    raise NotImplementedError() # FIXXME

  def ls(self, path, long=False):
    raise NotImplementedError() # FIXXME

  def readlink(self, canonical=True):
    raise NotImplementedError() # FIXXME

class BusyBox(Gnu):

  def ls(self, path, long=False):
    raise NotImplementedError() # FIXXME

def impl(system):
  userland = system.os.userland
  if userland == 'gnu':
    return Gnu(system)
  elif userland == 'bsd':
    return Bsd(system)
  elif userland == 'busybox':
    return BusyBox(system)
  else:
    raise RuntimeError(f'Unknown userland "{userland}"')

def impl(sys):
  if not hasattr(sys, '_impl'):
    userland = sys.os.userland
    if userland == 'gnu':
       sys._impl = Gnu(sys)
    elif userland == 'bsd':
      sys._impl = Bsd(sys)
    elif userland == 'busybox':
      sys._impl = BusyBox(sys)
    else:
      raise RuntimeError(f'Unknown userland "{userland}"')
  return sys._impl

class System(giga.System):
  'Unix system interface.'

  def __init__(
    self, name=None, super=False, super_user=None, super_password=None
  ):
    super_().__init__(
      name=name, super=super, super_user=super_user,
      super_password=super_password)

  #####
  ## properties

  @property
  def os(self):
    # FIXME lol. this should return a data structure that is uniform across
    #       platforms and describes the remote's operating system as
    #       precisely as possible.
    os = attr(kind='unix', flavor='linux', userland='gnu')
    if self.which('apt-get', 'apt'):
      os.family = 'debian'
    elif self.which('yum', 'dnf'):
      os.family = 'redhat'
    elif self.which('apk'):
      os.family = 'alpine'
    else:
      raise RuntimeError('Unable to determine operating system')
    return os

  @property
  def hostname(self):
    if self.which('hostname'):
      return self.stdout('hostname')
    hostname = self.stdout('echo $HOSTNAME').rstrip()
    if hostname:
      return hostname
    if self.isfile('/etc/hostname'):
      return self.loads('/etc/hostname').rstrip()
    raise RuntimeError('Unable to determine system hostname')

  @property
  def linesep(self):
    return '\n'

  @property
  def linesep(self):
    return '/'

  @property
  def shell(self):
    return self.stdout('echo $SHELL').rstrip()

  #####
  ## temp files

  def mktempdir(self, prefix=None):
    if prefix is None:
      prefix = 'lura.system.'
    argv = f'mktemp -p /tmp -d {quote(prefix)}' + 'X' * 12
    return self.run(argv).stdout.rstrip()

  @contextmanager
  def tempdir(self, prefix=None):
    try:
      path = self.mktempdir(prefix=prefix)
      yield path
    finally:
      self.rmrf(path)

  #####
  ## predicates

  def test(self, argv, *args, **kwargs):
    kwargs.setdefault('enforce', False)
    return self.zero(f'test {argv}', *args, **kwargs)

  def exists(self, path):
    return self.test(f'-e {quote(path)}')

  def isfile(self, path):
    return self.test(f'-f {quote(path)}')

  def isdir(self, path):
    return self.test(f'-d {quote(path)}')

  def islink(self, path):
    return self.test(f'-L {quote(path)}')

  def ismode(self, path, mode):
    return impl(self).ismode(path, mode)

  def isfifo(self, path):
    return impl(self).isfifo(path)

  def isowner(self, path, owner):
    return impl(self).isowner(path, owner)

  def isgroup(self, path, group):
    return impl(self).isgroup(path, group)

  def ishash(self, path, alg, sum):
    return sum == self.hash(path, alg)

  def iscontents(self, path, data):
    if self.exists(path):
      alg = 'sha512'
      sum = hashs(data, alg)
      return self.ishash(path, alg, sum)
    return False

  def contains(self, path, substring, encoding=None):
    if isinstance(substring, bytes):
      return substring in self.load(path)
    elif isinstance(substring, str):
      return substring in self.loads(path, encoding=encoding)
    else:
      assert(False)

  #####
  ## identity

  def whoami(self):
    return self.stdout('whoami').rstrip()

  #####
  ## files

  def ls(self, path, long=False):
    return impl(self).ls(path, long)

  def readlink(self, path, canonical=True):
    return impl(self).readlink(path, canonical)

  def cpf(self, src, dst, preserve=False):
    cp = ['cp', '-f']
    if preserve:
      cp.append('--preserve=all')
    cp.extend((quote(src), quote(dst)))
    cp = ' '.join(cp)
    self.run(cp)

  def cprf(self, src, dst, preserve=False):
    argv = ['cp', '-rf']
    if preserve:
      argv.append('--preserve=all')
    argv.extend((quote(src), quote(dst)))
    argv = ' '.join(argv)
    self.run(argv)

  def mvf(self, src, dst):
    self.run(f'mv -f {quote(src)} {quote(dst)}')

  def rmf(self, path):
    self.run(f'rm -f {quote(path)}')

  def rmrf(self, path):
    self.run(f'rm -rf {quote(path)}')

  def ln(self, src, dst):
    self.run(f'ln {quote(src)} {quote(dst)}')

  def lns(self, src, dst):
    self.run(f'ln -s {quote(src)} {quote(dst)}')

  def chmod(self, path, mode, recurse=False):
    if isinstance(mode, int):
      mode = oct(mode)[2:]
    argv = ['chmod']
    if recurse:
      argv.append('-R')
    argv.extend((mode, quote(path)))
    argv = ' '.join(argv)
    self.run(argv)

  def chown(self, path, spec, recurse=False):
    argv = ['chown']
    if recurse:
      argv.append('-R')
    argv.extend((spec, quote(path)))
    argv = ' '.join(argv)
    self.run(argv)

  def chgrp(self, path, group, recurse=False):
    argv = ['chgrp']
    if recurse:
      argv.append('-R')
    argv.extend((group, quote(path)))
    argv = ' '.join(argv)
    self.run(argv)

  def touch(self, path):
    self.run(f'touch {quote(path)}')

  def mkdir(self, dir):
    if self.isdir(dir):
      return
    self.run(f'mkdir {quote(dir)}')

  def mkdirp(self, dir):
    if self.isdir(dir):
      return
    self.run(f'mkdir -p {quote(dir)}')

  def rmdir(self, dir):
    if not self.isdir(dir):
      return
    self.run(f'rmdir {qoute(dir)}')

  def which(self, *names, error=False):
    if len(names) == 1 and not isinstance(names[0], str):
      names = names[0]
    for name in names:
      res = self.run(f'which {quote(name)}', enforce=False)
      if res.return_code == 0:
        return res.stdout.rstrip()
    else:
      if error:
        raise FileNotFoundError(f'Binaries not found: {",".join(names)}')
    return None

  def hash_openssl(self, path, alg):
    raise NotImplementedError() # FIXME

  def hash_md5sum(self, path, alg):
    raise NotImplementedError() # FIXME

  def hash_shasum(self, path, alg):
    raise NotImplementedError() # FIXME

  def hash_algsum(self, path, alg):
    return self.stdout(f'{alg}sum {quote(path)}').rstrip().split()[0]

  def hash(self, path, alg='sha512'):
    alg = alg.lower()
    if self.which(f'{alg}sum'):
      return self.hash_algsum(path, alg)
    elif alg.startswith('sha') and self.which('shasum'):
      return self.hash_shasum(path, alg)
    elif alg == 'md5' and self.which('md5sum'):
      return self.hash_md5sum(path, alg)
    elif self.which('openssl'):
      return self.hash_openssl(path, alg)
    else:
      raise RuntimeError('No supported hashing methods found on remote system')

  #####
  ## misc helpers

  def wget(self, url, path, alg='sha512', sum=None):
    url, path = quote(url), quote(path)
    if self.which('curl'):
      self.run(f'curl -L {url} -o {path}')
    elif self.which('wget'):
      self.run(f'wget {url} -O {path}')
    else:
      raise FileNotFoundError('Neither curl nor wget were found on the system')
    if sum and not self.ishash(path, alg, sum):
      self.rmf(path)
      msg = '%s sum mismatch for %s\nExpected: %s\nReceived: %s'
      raise ValueError(msg % (alg, path, sum, path_sum))

class Local(System):

  def __init__(
    self, name=None, super=False, super_user=None, super_password=None
  ):
    super_().__init__(
      name=name, super=super, super_user=super_user,
      super_password=super_password)

  @property
  def host(self):
    return 'localhost'

  def put(self, src, dst):
    self.cpf(src, dst)

  def get(self, src, dst):
    with self.nosuper():
      user = self.whoami()
      group = self.run('id -gn').stdout.strip()
    self.cpf(src, dst)
    self.chown(dst, user)
    self.chgrp(dst, group)

  def run(self, argv, *args, **kwargs):
    if self.super_use:
      kwargs['sudo'] = True
      if self.super_user:
        kwargs['sudo_user'] = self.super_user
      if self.super_password is not None:
        kwargs['sudo_password'] = self.super_password
      kwargs['sudo_login'] = True
    shell = run('echo $SHELL', *args, shell=True, **kwargs).stdout.rstrip()
    user_argv = argv
    argv = [shell, '-c', user_argv]
    try:
      res = run(argv, *args, **kwargs)
      return giga.system.RunResult(
        user_argv, res.code, self.super_use, res.stdout, res.stderr)
    except run.error as exc:
      res = exc.result
    res = giga.system.RunResult(
      user_argv, res.code, self.super_use, res.stdout, res.stderr)
    raise giga.system.RunError(res)

class Ssh(System):

  def __init__(
    self, host, port=22, user=None, password=None, key_file=None,
    private_key=None, passphrase=None, connect_timeout=60.0, auth_timeout=60.0,
    compress=True, name=None, super=False, super_user=None, super_password=None
  ):
    self._super_password = None
    self._client = None
    self._client_args = (host,)
    self._client_kwargs = dict(
      port = port,
      user = user,
      password = password,
      key_file = key_file,
      private_key = private_key,
      passphrase = passphrase,
      connect_timeout = connect_timeout,
      auth_timeout = auth_timeout,
      compress = compress,
    )
    super_().__init__(
      name=name, super=super, super_user=super_user,
      super_password=super_password)
    if self._client is None:
      self._reconnect()

  def _reconnect(self):
    args = self._client_args
    kwargs = self._client_kwargs.copy()
    kwargs['sudo_password'] = self._super_password
    if self._client:
      self._client.close()
    self._client = ssh.Client(*args, **kwargs)

  @property
  def super_password(self):
    return self._super_password

  @super_password.setter
  def super_password(self, password):
    if password != self._super_password:
      self._super_password = password
      self._reconnect()

  @property
  def host(self):
    return self._client._host

  def put(self, src, dst):
    with self.nosuper():
      whoami = self.whoami()
    with self.tempdir(prefix='put.') as temp_dir:
      tmp = f'{temp_dir}/{os.path.basename(dst)}'
      self.chown(temp_dir, whoami)
      self._client.put(src, temp_dir)
      self.cpf(tmp, dst)

  def get(self, src, dst):
    with self.nosuper():
      whoami = self.whoami()
    with self.tempdir(prefix='get.') as temp_dir:
      tmpsrc = f'{temp_dir}/{os.path.basename(src)}'
      self.cpf(src, tmpsrc)
      self.chown(temp_dir, whoami, recurse=True)
      self._client.get(tmpsrc, dst)

  def run(self, argv, *args, **kwargs):
    try:
      if self.super_use:
        res = self._client.sudo(
          argv, *args, user=self.super_user, login=True, **kwargs)
      else:
        res = self._client.run(argv, *args, **kwargs)
      return giga.system.RunResult(
        argv, res.return_code, self.super_use, res.stdout, res.stderr)
    except invoke.exceptions.UnexpectedExit as exc:
      res = exc.result
    res = giga.system.RunResult(
      argv, res.return_code, self.super_use, res.stdout, res.stderr)
    raise giga.system.RunError(res)

__all__ = ('System', 'Local', 'Ssh')
