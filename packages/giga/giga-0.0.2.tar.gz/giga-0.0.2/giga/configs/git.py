import giga

log = giga.logs.get_logger(__name__)

class Clones(giga.Config):
  'Apply git clones if needed.'

  repos = None
  keep  = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    with self.task(f'Apply {len(self.repos)} git repo clones') as task:
      for path, remote, branch in self.repos:
        task.ensure.git.cloned(path, remote, branch)

  def on_delete(self):
    super().on_delete()
    with self.task(f'Delete {len(self.repos)} git repo clones') as task:
      if not self.keep:
        for path, _, _ in self.repos:
          task.ensure.fs.absent(path)

  def on_is_applied(self):
    return (
      super.on_is_applied()
    )

class Pulls(giga.Config):
  'Apply git pulls if needed.'

  repos = None
  config_logger = log

  def on_apply(self):
    super().on_apply()

  def on_delete(self):
    super().on_delete()

  def on_is_applied(self):
    return (
      super.on_is_applied()
    )
