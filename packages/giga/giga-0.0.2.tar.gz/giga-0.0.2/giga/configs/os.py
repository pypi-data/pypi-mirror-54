import giga
from shlex import quote

log = giga.logs.get_logger(__name__)

class Apt(giga.Config):

  packages = None
  keep = True
  config_logger = log

  def get_installed_packages(self):
    argv = "dpkg-query -W -f='${binary:Package}|${Version}&'"
    packages = self.system.stdout(argv)[:-1]
    return {
      name.split(':')[0]: version
      for (name, version) in (pkg.split('|') for pkg in packages.split('&'))
    }

  def on_apply(self):
    super().on_apply()
    sys = self.system
    env = {'DEBIAN_FRONTEND': 'noninteractive'}
    installed = self.get_installed_packages()
    missing = [pkg for pkg in self.packages if pkg not in installed]
    with self.task('Apply apt update') as task:
      if missing:
        sys('apt-get update', env=env)
    with self.task(f'Apply {len(self.packages)} apt package(s)') as task:
      if missing:
        packages = ' '.join(missing)
        sys(f'apt-get -y install {packages}', env=env)
      for pkg in self.packages:
        with task.item(pkg):
          if pkg in missing:
            +task

  def on_delete(self):
    super().on_delete()
    sys = self.system
    env = {'DEBIAN_FRONTEND': 'noninteractive'}
    with self.task(f'Delete {len(self.packages)} apt package(s)') as task:
      if not self.keep:
        installed = self.get_installed_packages()
        present = [pkg for pkg in self.packges if pkg in installed]
        if present:
          packages = ' '.join(reversed(present))
          sys(f'apt-get -y remove --purge {packages}')
        for pkg in reversed(self.packages):
          with task.item(pkg):
            if pkg in present:
              +task

  def on_is_applied(self):
    installed = self.get_installed_packages()
    return (
      super().on_is_applied() and
      all(pkg in installed for pkg in self.packages)
    )

class Yum(giga.Config):

  packages = None
  keep = True
  config_logger = log

  def on_init(self):
    super().on_init(self)
    self._yum = 'yum'
    if self.which('dnf'):
      self._yum = 'dnf'

  def get_installed_packages(self):
    argv = "rpm -qa --queryformat '%{NAME}|%{VERSION}&'"
    packages = self.system.stdout(argv)[:-1]
    return dict(pkg.split('|') for pkg in packages.split('&'))

  def on_apply(self):
    super().on_apply()
    sys = self.system
    installed = self.get_installed_packages()
    missing = []
    for pkg in self.packages:
      if isinstance(pkg, str):
        if pkg not in installed:
          missing.append(pkg)
      else:
        if pkg[0] not in installed:
          missing.append(pkg[1])
    with self.task(f'Apply {len(self.packages)} {self._yum} package(s)') as task:
      if missing:
        packages = ' '.join(quote(pkg) for pkg in self.packages)
        sys(f'{self._yum} -y install {packages}')
      for pkg in self.packages:
        with task.item(pkg):
          if pkg in missing:
            +task

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task(f'Delete {len(self.packages)} yum package(s)') as task:
      if not self.keep:
        installed = self.get_installed_packages()
        present = []
        for pkg in self.packages:
          if isinstance(pkg, str):
            if pkg in installed:
              present.append(pkg)
          else:
            if pkg[0] in installed:
              present.append(pkg[0])
        if present:
          packages = ' '.join(reversed(present))
          sys(f'{self._yum} -y remove {packages}')
        for pkg in reversed(self.packages):
          with task.item(pkg):
            if pkg in present:
              +task

  def on_is_applied(self):
    installed = self.get_installed_packages()
    return (
      super.on_is_applied() and
      all(
        (pkg if isinstance(pkg, str) else pkg[0]) in installed
        for pkg in self.packages
      )
    )

Dnf = Yum

class RcLocal755(giga.Config):

  config_logger = log

  def config_include(self):
    family = self.system.os.family
    if family == 'debian':
      from giga.configs.debian import RcLocal755
    elif family == 'redhat':
      from giga.configs.redhat import RcLocal755
    else:
      raise NotImplementedError(f'Unsupported os family: {family}')
    return [RcLocal755]
