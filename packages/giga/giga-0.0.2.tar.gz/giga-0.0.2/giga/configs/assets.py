import giga
from lura.plates import jinja2

log = giga.logs.get_logger(__name__)

class Assets(giga.Config):

  assets = None
  paths  = None
  keep   = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self.paths)} assets') as task:
      for src, dst in self.paths:
        task.ensure.fs.contents(dst, self.assets.loads(src))

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task(f'Delete {len(self.paths)} assets') as task:
      if not self.keep:
        for _, dst in reversed(self.paths):
          task.ensure.fs.absent(dst)

  def on_is_applied(self):
    return (
      super.on_is_applied() and
      all(
        self.system.iscontents(dst, self.assets.loads(src))
        for (src, dst) in self.paths
      )
    )

class TemplateAssets(giga.Config):

  assets    = None
  paths     = None
  env       = None
  keep      = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    env = self.env or vars(self)
    with self.task(f'Apply {len(self.paths)} template assets') as task:
      for src, dst in self.paths:
        contents = jinja2.expandss(env, self.assets.loads(src))
        task.ensure.fs.contents(dst, contents)

  def on_delete(self):
    super().on_delete()
    with self.task(f'Delete {len(self.paths)} template assets') as task:
      if not self.keep:
        for _, dst in reversed(self.paths):
          task.ensure.fs.absent(dst)

  def on_is_applied(self):
    sys = self.system
    return (
      super().on_is_applied() and
      all(
        (
          sys.exists(dst) and
          sys.iscontents(dst, jinja2.expandss(self.env, self.assets.loads(src)))
        ) for (src, dst) in self.paths
      )
    )
