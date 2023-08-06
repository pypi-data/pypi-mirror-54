'Parallel executor.'

import sys
import threading
import traceback
from collections import Sequence
from copy import deepcopy
from giga import sync
from lura import threads
from lura import logs
from lura import utils
from lura.iter import always
from lura.time import poll
from multiprocessing import pool
from time import sleep

log = logs.get_logger(__name__)

class ThreadPool(threads.Thread):
  "Encapsulate python's thread pool."

  def __init__(self, fn, args, workers):
    super().__init__()
    self.fn = fn
    self.args = args
    self.workers = workers

  def run(self):
    with pool.ThreadPool(self.workers) as p:
      res = p.map(self.fn, self.args)
      return res

class Executor(utils.Kwargs):
  'Apply methods on Configurations in parallel.'

  threads_start_timeout  = 2.0
  threads_start_interval = 0.02
  coordinator_type       = sync.Coordinator
  pool_type              = ThreadPool

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def log_pool_errors(self, pool):
    if isinstance(pool.result, Sequence):
      for res in pool.result:
        if utils.isexc(res):
          log.error('-' * 40)
          log.error(''.join(traceback.format_exception(*res)))

  def wait_for_start(self, configs):
    test = lambda: all(bool(_.system) for _ in configs)
    timeout = self.threads_start_timeout
    pause = self.threads_start_interval
    if not poll(test, timeout=timeout, pause=pause):
      raise TimeoutError(f'Threads did not start within {timeout} seconds')

  def run(self, fn, group):
    configs = [deepcopy(group.config) for _ in range(0, len(group.systems))]
    coord = self.coordinator_type(
      configs, group.synchronize, group.fail_early, group.verbose)
    items = zip(
      configs,
      group.systems,
      always(coord),
      always(group.args),
      always(group.kwargs),
    )
    pool = self.pool_type.spawn(fn, items, group.workers)
    try:
      try:
        self.wait_for_start(configs)
        coord.coordinate()
      except (TimeoutError, RuntimeError):
        self.log_pool_errors(pool)
        raise
      pool.join()
      return pool.result
    except BaseException:
      if pool.is_alive():
        coord.cancel()
        pool.join()
      raise

  def apply_in_thread(self, item):
    try:
      config, system, coord, args, kwargs = item
      return config.apply(system, *args, coordinator=coord, **kwargs)
    except Exception:
      return sys.exc_info()

  def apply(self, group):
    return self.run(self.apply_in_thread, group)

  def delete_in_thread(self, item):
    try:
      config, system, coord, args, kwargs = item
      return config.delete(system, *args, coordinator=coord, **kwargs)
    except Exception:
      return sys.exc_info()

  def delete(self, group):
    return self.run(self.delete_in_thread, group)

  def is_applied_in_thread(self, item):
    try:
      config, system, coord, args, kwargs = item
      return config.is_applied(system, *args, coordinator=coord, **kwargs)
    except Exception:
      return sys.exc_info()

  def is_applied(self, group):
    return self.run(self.is_applied_in_thread, group)
