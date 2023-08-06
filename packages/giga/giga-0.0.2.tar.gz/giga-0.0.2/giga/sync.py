'Thread synchronization.'

import giga
import threading
from lura import utils
from lura.attrs import ottr
from lura.time import poll
from time import sleep

log = giga.logs.get_logger(__name__)

class Coordinator(utils.Kwargs):

  ready_timeout         = 2.0
  default_poll_interval = 0.05

  def __init__(self, configs, synchronize, fail_early, verbose, **kwargs):
    super().__init__(**kwargs)
    self._conds = ottr(
      ready = threading.Condition(),
      sync = threading.Condition(),
      done = threading.Condition(),
    )
    self.configs = configs
    self.synchronize = synchronize
    self.fail_early = fail_early
    self.verbose = verbose
    self.cancelled = None
    self.rlock = threading.RLock()

  @property
  def active(self):
    return tuple(_ for _ in self.configs if _.system)

  def waiters(self, cond):
    return len(self._conds[cond]._waiters)

  def awaiting(self, cond):
    if not self.synchronize and cond == 'sync':
      return False
    with self._conds[cond]:
      return len(self._conds[cond]._waiters) >= len(self.active)

  def poll(self, cond, timeout=-1, retries=-1, pause=None):
    if retries == 0:
      return self.awaiting(cond)
    if pause is None:
      pause = self.default_poll_interval
    test = lambda: self.awaiting(cond)
    return poll(test, timeout=timeout, retries=retries, pause=pause)

  def notify(self, cond):
    with self._conds[cond]:
      self._conds[cond].notify_all()

  def cancel(self):
    self.cancelled = True
    conds = self._conds
    for _ in range(0, 2):
      with conds.ready, conds.sync, conds.done:
        for cond in conds.values():
          cond.notify_all()

  def wait(self, cond, timeout=None):
    if cond == 'sync' and not self.synchronize:
      return
    with self._conds[cond]:
      if not self._conds[cond].wait(timeout):
        raise TimeoutError(
          f'Coordinator did not send "{cond}" within {timeout} seconds')

  def coordinate(self):
    timeout = self.ready_timeout
    if not self.poll('ready', timeout=timeout):
      raise RuntimeError(f'Configs did not ready within {timeout} seconds')
    self.notify('ready')
    while not self.awaiting('done'):
      if self.cancelled:
        break
      if self.awaiting('sync'):
        self.notify('sync')
        sleep(0)
      else:
        sleep(self.default_poll_interval)
    else:
      self.notify('done')
