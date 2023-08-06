'Task helper.'

import giga
import io
import os
from contextlib import contextmanager
from giga import ensure

log = giga.logs.get_logger(__name__)

class Task:
  '''
  A context manager representing some activity which may or may not generate
  changes on a Configuration.

  This class provides a logical place to...

  - handle some automatic logging/console output
  - handle change tracking
  - provide access to an Ensure object
  - provide the thread synchronization hook
  '''

  def __init__(self, config, msg):
    super().__init__()
    self.config = config
    self.msg = msg
    self.verbose = config.config_verbose
    self.sync = config.config_sync
    coord = config.coordinator
    if coord:
      self.verbose = coord.verbose
      self.sync = coord.synchronize
    self.ensure = ensure.Ensure(self)
    self.changes = 0
    self.items = []

  def __enter__(self):
    self.on_enter()
    return self

  def __exit__(self, *exc_info):
    assert(self.changes >= 0)
    self.config.changes += self.changes
    self.on_exit(exc_info)

  def on_enter(self):
    if self.sync:
      self.config.sync()

  def on_exit(self, exc_info):
    self.config.log(self.format_result(exc_info))

  def format_result(self, exc_info):
    config = self.config
    verbose = config.config_verbose
    if config.coordinator:
      verbose = config.coordinator.verbose
    with io.StringIO() as buf:
      if verbose:
        buf.writeline = lambda line: buf.write(line + os.linesep)
        buf.writeline(f'(  task) {self.msg}')
        for item, changed in self.items:
          c = '+' if changed else '.'
          buf.writeline(f'      {c}  {item}')
      if exc_info != (None, None, None):
        buf.write('[ error] ')
      elif self.changes == 0:
        buf.write('(    ok) ')
      else:
        buf.write('[change] ')
      buf.write(self.msg)
      return buf.getvalue()

  @property
  def changed(self):
    return self.changes > 0

  def change(self, count=1, item=None):
    assert(count >= 0)
    self.changes += count
    if item is not None:
      self.items.append((item, count > 0))
    return self.changes

  __pos__ = change
  __add__ = change

  @contextmanager
  def item(self, item):
    changes = self.changes
    try:
      yield
    finally:
      self.items.append((item, changes != self.changes))

  @contextmanager
  def synchronized(self):
    coord = self.config.coordinator
    if coord:
      with coord.rlock:
        yield
    else:
      yield
