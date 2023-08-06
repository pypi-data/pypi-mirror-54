import giga
from giga import configs

log = giga.logs.get_logger(__name__)

class Epel(configs.os.Yum):
  'Apply epel.'

  version = None
  config_logger = log

  def on_init(self):
    super().on_init()
    self.packages = [
      ('epel-release', f'https://dl.fedoraproject.org/pub/epel/epel-release-latest-{self.version}.noarch.rpm'),
    ]

class Ius(configs.os.Yum):
  'Apply ius.'

  version = None
  config_logger = log

  def on_init(self):
    super().on_init()
    self.packages = [
      ('ius-release', f'https://repo.ius.io/ius-release-el{self.version}.rpm'),
    ]

class RcLocal755(giga.Config):
  'Make /etc/rc.d/rc.local executable.'

  keep = True
  config_logger = log

  def on_apply(self):
    super().on_apply()
    with self.task('Apply rc.local executable bit') as task:
      task.ensure.fs.mode('/etc/rc.d/rc.local', 0o755)

  def on_delete(self):
    super().on_delete()
    with self.task('Delete rc.local executable bit') as task:
      if not self.keep:
        task.ensure.fs.mode('/etc/rc.d/rc.local', 0o644)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      self.system.ismode('/etc/rc.d/rc.local', 0o755)
    )
