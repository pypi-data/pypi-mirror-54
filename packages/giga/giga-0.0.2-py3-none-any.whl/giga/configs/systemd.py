import giga
from giga import configs

log = giga.logs.get_logger(__name__)

class BaseServiceFiles(giga.Config):

  config_logger = log

  def apply_systemd_reload(self):
    with self.task('Apply systemd reload') as task:
      if self.changed:
        task.ensure.systemd.reloaded()

  def on_apply(self):
    super().on_apply()
    self.apply_systemd_reload()

  def on_delete(self):
    super().on_delete()
    self.apply_systemd_reload()

class Files(BaseServiceFiles, configs.fs.Files):
  'Apply systemd service files and reload systemd.'

  pass

class TemplateFiles(BaseServiceFiles, configs.fs.TemplateFiles):
  'Apply systemd service templates and reload systemd.'

  pass

class Assets(BaseServiceFiles, configs.assets.Assets):
  'Apply systemd service asset files and reload systemd.'

  pass

class TemplateAssets(BaseServiceFiles, configs.assets.TemplateAssets):
  'Apply systemd service asset templates and reload systemd.'

  pass

class Starts(giga.Config):
  'Enable and start services.'

  services = None
  enable = True
  disable = True
  config_logger = log

  def on_apply(self):
    super().on_apply()
    with self.task(f'Apply {len(self.services)} systemd services') as task:
      for service in self.services:
        if self.enable:
          task.ensure.systemd.enabled_and_started(service)
        else:
          task.ensure.systemd.started(service)

  def on_delete(self):
    super().on_delete()
    with self.task(f'Delete {len(self.services)} systemd services') as task:
      for service in self.services:
        if self.disable:
          task.ensure.systemd.disabled_and_stopped(service)
        else:
          task.ensure.systemd.stopped(service)

  def on_is_applied(self):
    sys = self.system
    return (
      super().on_is_applied() and
      all(sys.zero(f'systemctl status {_}') for _ in self.services) and
      all(
        (
          sys.zero(f'systemctl is-enabled {_}') for _ in self.services
        ) if self.enable else ()
      )
    )
