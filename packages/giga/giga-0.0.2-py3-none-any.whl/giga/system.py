import giga
import os
from abc import abstractmethod
from contextlib import contextmanager
from lura import fs
from lura.attrs import ottr
from lura.formats import yaml

log = giga.logs.get_logger(__name__)

super_ = super

class RunResult:

  def __init__(self, argv, code, super, stdout, stderr):

    super_().__init__()
    self.argv = argv
    self.code = code
    self.super = super
    self.stdout = stdout
    self.stderr = stderr

  def format(self):
    vars = ottr(
      argv=self.argv, code=self.code, super=self.super, stdout=self.stdout,
      stderr=self.stderr)
    return yaml.dumps({'result': vars})

  def print(self, *args, **kwargs):
    print(self.format, *args, **kwargs)

class RunError(RuntimeError):

  def __init__(self, result):
    super().__init__(f'Command exited with unexpected code\n{result.format()}')
    self.result = result

class System:
  '''
  Abstract base class representing the minimum requirements for a useful
  system interface. This interface should be general enough to encapsulate
  every modern operating system any sane person would want to use.

  This class defines a protocol for acting as the superuser. Most users won't
  care about this because they'll be using giga.Group with super=True, so I'm
  not going to go over it much, but here are the basics.

  For users, if you pass super=True to the constructor, or enter the
  System.super() context manager, then all of your run(), get(), and put()
  calls will happen according to your super arguments:

    with sys.super(super_password='disco'):
      sys('cat /root/.ssh/id_rsa')

    with sys.super(super_user='jenkins', super_password='disco'):
      sys('git pull', cwd='/home/jenkins/repos/dingus.git')

  For implementors, we expect you to pay attention to the super_use attribute.
  When it is True, you must not only run() all commands as root using super and
  according to the super_* attributes, but you must also get() and put() as
  the superuser.
  '''

  def __init__(
    self, name=None, super=False, super_user=None, super_password=None
  ):
    super_().__init__()
    self._name = name
    self.super_use = super
    self.super_user = super_user
    self.super_password = super_password

  #####
  ## super things

  @contextmanager
  def super(self, user=None, password=None):
    o_use = self.super_use
    o_user = self.super_user
    if user is not None:
      self.super_user = user
    o_password = self.super_password
    if password is not None:
      self.super_password = password
    try:
      yield self
    finally:
      self.super_use = o_use
      self.super_user = o_user
      self.super_password = o_password

  @contextmanager
  def nosuper(self):
    o_use = self.super_use
    self.super_use = False
    try:
      yield self
    finally:
      self.super_use = o_use

  #####
  ## properties

  @property
  def name(self):
    return self._name or self.host

  @property
  @abstractmethod
  def host(self):
    pass

  @property
  @abstractmethod
  def hostname(self):
    pass

  @property
  @abstractmethod
  def os(self):
    pass

  @property
  @abstractmethod
  def linesep(self):
    pass

  @property
  @abstractmethod
  def pathsep(self):
    pass

  #####
  ## file exchange

  @abstractmethod
  def put(self, src, dst):
    pass

  @abstractmethod
  def get(self, src, dst):
    pass

  #####
  ## command execution

  @abstractmethod
  def run(
    self, argv, cwd=None, env=None, replace_env=False, encoding=None,
    stdin=None, stdout=None, stderr=None, enforce=True
  ):
    pass

  @property
  def __call__(self):
    return self.run

  def code(self, *args, **kwargs):
    kwargs.setdefault('enforce', False)
    return self.run(*args, **kwargs).return_code

  def zero(self, *args, **kwargs):
    return self.code(*args, **kwargs) == 0

  def nonzero(self, *args, **kwargs):
    return self.code(*args, **kwargs) != 0

  def stdout(self, *args, **kwargs):
    return self.run(*args, **kwargs).stdout

  def stderr(self, *args, **kwargs):
    return self.run(*args, **kwargs).stderr

  def lines(self, *args, **kwargs):
    return self.stdout(*args, **kwargs).split(self.linesep)

  #####
  ## path operations

  def join(self, *paths):
    raise NotImplementedError() # FIXME

  def split(self, path):
    return path.rsplit(path, self.pathsep, 1)

  def dirname(self, path):
    return self.split(path)[0]

  def basename(self, path):
    return self.split(path)[1]

  #####
  ## file operations

  def _tempdir_local(self, *args, prefix=None, **kwargs):
    user_prefix = prefix
    prefix = f'{self.__module__}.{type(self).__name__}.'
    if user_prefix:
      prefix = f'{prefix}{user_prefix}'
    return fs.TempDir(*args, prefix=prefix, **kwargs)

  def load(self, path):
    with self._tempdir_local(prefix='load.') as temp_dir:
      dst = os.path.join(temp_dir, self.split(path)[1])
      self.get(path, dst)
      return fs.load(dst)

  def loads(self, path, encoding=None):
    with self._tempdir_local(prefix='loads.') as temp_dir:
      dst = f'{temp_dir}/{os.path.basename(path)}'
      self.get(path, dst)
      return fs.loads(dst, encoding=encoding)

  def dump(self, path, data):
    with self._tempdir_local(prefix='dump.') as temp_dir:
      src = f'{temp_dir}/{os.path.basename(path)}'
      fs.dump(src, data)
      self.put(src, path)

  def dumps(self, path, data, encoding=None):
    with self._tempdir_local(prefix='dumps.') as temp_dir:
      src = f'{temp_dir}/{os.path.basename(path)}'
      fs.dumps(src, data, encoding=encoding)
      self.put(src, path)

  def append(self, path, data):
    if not self.exists(path):
      self.dump(path)
    else:
      self.dump(path, sys.load(path) + data)

  def appends(self, path, data, encoding=None):
    if not self.exists(path):
      self.dumps(path, data, encoding=encoding)
    else:
      self.dumps(
        path, self.loads(path, encoding=encoding) + data, encoding=encoding)

  #####
  ## giga.Config support

  def apply(self, config, *args, **kwargs):
    config = config() if isinstance(config, type) else config
    return config.apply(self, *args, **kwargs)

  def delete(self, config, *args, **kwargs):
    config = config() if isinstance(config, type) else config
    return config.delete(self, *args, **kwargs)

  def is_applied(self, config, *args, **kwargs):
    config = config() if isinstance(config, type) else config
    return config.is_applied(self, *args, **kwargs)
