import giga
from lura.formats import json
from shlex import quote

log = giga.logs.get_logger(__name__)

class BasePackages(giga.Config):

  packages = None
  py = 3
  pys = {
    2: ('python2', 'python2.7'),
    3: ('python3', 'python3.8', 'python3.7', 'python3.6'),
  }
  python = None # overrides the above py/pys stuff if set
  keep = True
  config_logger = log

  def on_init(self):
    super().on_init()
    sys = self.system
    self.python = self.python or sys.which(self.pys[self.py])

  def get_installed_packages(self):
    sys = self.system
    if not self.python or sys.nonzero(f'{self.python} -m pip --help'):
      return {}
    argv = f'{self.python} -m pip list --format json'
    packages = json.loads(sys.stdout(argv))
    return dict((pkg.name, pkg.get('version')) for pkg in packages)

  def missing(self, packages):
    installed = self.get_installed_packages()
    return [pkg for pkg in packages if pkg.split()[0] not in installed]

  def require_python(self):
    sys = self.system
    if self.python is None:
      raise FileNotFoundError(
        f'Python{self.py} is missing, cannot proceed')
    if sys.nonzero(f'{self.python} -m pip --help'):
      raise FileNotFoundError(
        f'Python{self.py} pip module is missing, cannon proceed')

  def on_apply_start(self):
    super().on_apply_start()
    self.require_python()

  def present(self, packages):
    installed = self.get_installed_packages()
    return [pkg for pkg in packages if pkg.split()[0] in installed]

class Packages(BasePackages):

  def on_apply(self):
    super().on_apply()
    sys = self.system
    missing = self.missing(self.packages)
    with self.task(f'Apply {len(self.packages)} python package(s)') as task:
      if missing:
        packages = ' '.join(quote(pkg) for pkg in missing)
        sys(f'{self.python} -m pip install {packages}')
      for pkg in self.packages:
        with task.item(pkg):
          if pkg in missing:
            +task

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task(f'Delete {len(self.packages)} python package(s)') as task:
      if not self.keep:
        installed = self.get_installed_packages()
        present = self.present(self.packages)
        if present:
          packages = ' '.join(reversed(quote(pkg) for pkg in present))
          sys(f'yes|{self.python} -m pip uninstall {pkg}')
        for pkg in reversed(self.packages):
          with task.item(pkg):
            if pkg in present:
              +task

  def on_is_applied(self):
    installed = self.get_installed_packages()
    return (
      super().on_is_applied() and
      all(pkg.split()[0] in installed for pkg in self.packages)
    )

class EditablePackages(BasePackages):

  synchronize = False

  def on_apply(self):
    super().on_apply()
    sys = self.system
    missing = self.missing(pkg for (pkg, _) in self.packages)
    with self.task(f'Apply {len(self.packages)} editable packages') as task:
      for pkg, path in self.packages:
        with task.item(pkg):
          if pkg in missing:
            if self.synchronize:
              with task.synchronized():
                sys(f'{self.python} -m pip install -e {path}')
            else:
              sys(f'{self.python} -m pip install -e {path}')
            +task

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task(f'Delete {len(self.packages)} editable packages') as task:
      if not self.keep:
        present = self.present(pkg for (pkg, _) in self.packages)
        for pkg, path in reversed(self.packages):
          with task.item(pkg):
            if pkg in present:
              if self.synchronize:
                with task.synchronized():
                  sys(f'{self.python} setup.py develop -u', cwd=path)
              else:
                sys(f'{self.python} setup.py develop -u', cwd=path)
              +task

  def on_is_applied(self):
    installed = self.get_installed_packages()
    return (
      super().on_is_applied() and
      all(pkg in installed for (pkg, _) in self.packages)
    )
