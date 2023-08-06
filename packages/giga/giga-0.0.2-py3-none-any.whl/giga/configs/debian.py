import giga

log = giga.logs.get_logger(__name__)

class RcLocal755(giga.Config):
  '''
  Create /etc/rc.local if it doesn't exist and make it executable.
  '''

  keep = True
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task('Apply rc.local executable bit') as task:
      path = '/etc/rc.local'
      task.ensure.fs.contains(path, '#!/bin/bash\n')
      task.ensure.fs.mode(path, 0o755)

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task('Delete rc.local executable bit') as task:
      if not self.keep:
        task.ensure.fs.mode('/etc/rc.local', 0o644)

  def on_is_applied(self):
    sys = self.system
    path = '/etc/rc.local'
    return (
      super().on_is_applied() and
      sys.isfile(path) and
      sys.ismode(path, 0o755)
    )
