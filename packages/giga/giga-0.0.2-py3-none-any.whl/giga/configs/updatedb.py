import giga
import io
from giga import configs

log = giga.logs.get_logger(__name__)

class Prunes(giga.Config):
  'Apply PRUNEPATHS to /etc/updatedb.conf.'

  paths = None
  conf = '/etc/updatedb.conf'
  keep = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self.paths)} updatedb prunes') as task:
      if sys.isfile(self.conf):
        with io.StringIO(sys.loads(self.conf)) as conf, io.StringIO() as buf:
          for line in conf:
            if line.startswith('PRUNEPATHS='):
              paths = line.strip().split('=', 1)[1][1:-1].split(' ')
              paths += [path for path in self.paths if path not in paths]
              paths = ' '.join(paths)
              line = f'PRUNEPATHS="{paths}"\n'
            buf.write(line)
          task.ensure.fs.contents(self.conf, buf.getvalue())

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task('Delete updatedb prune') as task:
      if not self.keep:
        if sys.isfile(self.conf):
          with io.StringIO(sys.loads(self.conf)) as conf, io.StringIO() as buf:
            for line in conf:
              if line.startswith('PRUNEPATHS='):
                paths = line.strip().split('=', 1)[1][1:-1].split(' ')
                paths = [path for path in paths if path not in self.paths]
                paths = ' '.join(paths)
                line = f'PRUNEPATHS="{paths}"\n'
              buf.write(line)
            task.ensure.fs.contents('/etc/updatedb.conf', buf.getvalue())

  def on_is_applied(self):
    sys = self.system
    if super().on_is_applied():
      if sys.isfile(self.conf):
        with io.StringIO(sys.loads(self.conf)) as conf:
          for line in conf:
            if line.startswith('PRUNEPATHS='):
              paths = line.strip().split('=', 1)[1][1:-1].split(' ')
              return all(path in paths for path in self.paths)
          else:
            # PRUNEPATHS not in updatedb.conf. something is broken and we
            # shouldn't mess with it
            return True
    return False
