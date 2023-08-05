'Thread synchronization.'

import giga
import threading
from lura import utils
from lura.attrs import ottr
from lura.time import poll

log = giga.logs.get_logger(__name__)

class Coordinator(utils.Kwargs):

  default_poll_interval = 0.05

  def __init__(self, configs, synchronize, fail_early, **kwargs):
    self._conds = ottr(
      ready = threading.Condition(),
      sync = threading.Condition(),
      done = threading.Condition(),
    )
    self.configs = configs
    self.synchronize = synchronize
    self.fail_early = fail_early
    self.cancelled = None
    self.rlock = threading.RLock()
    super().__init__(**kwargs)

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
    if pause is None:
      pause = self.default_poll_interval
    test = lambda: self.awaiting(cond)
    return poll(test, timeout=timeout, retries=retries, pause=pause)

  def notify(self, cond):
    with self._conds[cond]:
      self._conds[cond].notify_all()

  def cancel(self):
    conds = self._conds
    with conds.ready, conds.sync, conds.done:
      self.cancelled = True
      # FIXME
      for cond in conds.values():
        cond.notify_all()

  def wait(self, cond, timeout=None):
    if cond == 'sync' and not self.synchronize:
      return
    with self._conds[cond]:
      if not self._conds[cond].wait(timeout):
        raise TimeoutError(
          f'Coordinator did not send "{cond}" within {timeout} seconds')
