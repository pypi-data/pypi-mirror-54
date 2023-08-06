'Run a shell command.'

import giga
from lura import net
from lura.formats import yaml
from lura.strutils import as_bool
from shlex import quote

log = giga.logs.get_logger(__name__)

class Shell(giga.Config):

  shell = None
  quiet = False
  config_logger = log

  def on_init(self):
    super().on_init()
    if 'shell' in self.kwargs:
      self.shell = self.kwargs.shell
    if not self.shell:
      self.shell = self.system.shell
    self.argv = self.kwargs.argv if 'argv' in self.kwargs else self.args[0]

  def on_apply(self):
    super().on_apply()
    argv = self.argv
    with self.task(f'Run {argv}') as task:
      with task.item(argv):
        res = self.system.run(f'{self.shell} -i -c {quote(argv)}')
        +task
    quiet = as_bool(self.kwargs.get('quiet', self.quiet))
    if not quiet:
      self.log('\n' + res.format().rstrip() + '\n')

  def on_is_applied(self):
    return False

class CurlBins(giga.Config):

  bins = None
  keep = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self.bins)} curl bins') as task:
      for bin, url, alg, sum_url in self.bins:
        with task.item(f'curl {bin}'):
          if not sys.isfile(bin):
            sum = None
            if sum_url:
              sum = net.wgets(sum_url).rstrip().rsplit()[0]
            sys.wget(url, bin, alg, sum)
            +task
        task.ensure.fs.mode(bin, 0o755)

  def on_delete(self):
    super().on_delete()
    with self.task(f'Delete {len(self.bins)} curl bins') as task:
      if not self.keep:
        for bin, _, _, _ in self.bins:
          task.ensure.fs.absent(bin)

  def on_is_applied(self):
    sys = self.system
    bins = (bin for (bin, _, _, _) in self.bins)
    return (
      super().on_is_applied() and
      all(sys.isfile(bin) and sys.ismode(bin, 0o755) for bin in bins)
    )
