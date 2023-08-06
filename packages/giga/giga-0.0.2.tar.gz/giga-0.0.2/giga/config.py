'System configuration root class.'

import giga
import io
import os
import sys
import traceback
from giga import method
from giga import task
from lura import strutils
from lura import utils

log = giga.logs.get_logger(__name__)

class Config(utils.Kwargs):

  config_logger    = log
  config_log_level = log.INFO
  config_include   = None
  config_after     = None

  # fallbacks for when running without a coordinator
  config_verbose = True
  config_sync    = False

  # coordinator timeouts
  config_ready_timeout = 2.0
  config_sync_timeout  = None
  config_done_timeout  = None

  # types
  config_apply_type      = method.Apply
  config_delete_type     = method.Delete
  config_is_applied_type = method.IsApplied
  config_task_type       = task.Task

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    cls = type(self)
    self.name = '%s.%s' % (cls.__module__, cls.__name__)
    self.parent = None
    self.system = None
    self.coordinator = None
    self.args = None
    self.kwargs = None
    self.changes = 0
    self.applied = True

  @property
  def first(self):
    coord = self.coordinator
    return True if not coord else self.system is coord.configs[0].system

  @property
  def depth(self):
    i = 0
    parent = self.parent
    while parent is not None:
      i += 1
      parent = parent.parent
    return i

  @property
  def changed(self):
    return self.changes > 0

  def log_format(self, msg, exc_info=False):
    msg = msg.rstrip()
    prefix = f'[{self.system.name}] '
    with io.StringIO() as buf:
      if os.linesep in msg:
        buf.write(strutils.prefix(msg, prefix))
      else:
        buf.write(f'{prefix}{msg}')
      if exc_info:
        buf.write(os.linesep)
        tb = ''.join(traceback.format_exception(*sys.exc_info()).rstrip())
        buf.write(tb)
      return buf.getvalue()

  def log(self, msg, exc_info=False):
    msg = self.log_format(msg, exc_info)
    log = self.config_logger[self.config_log_level]
    log(msg)

  def sync(self):
    coord = self.coordinator
    if not coord:
      return
    if coord.cancelled:
      raise Cancel(self)
    coord.wait('sync', timeout=self.config_sync_timeout)
    if coord.cancelled:
      raise Cancel(self)

  def task(self, *args, **kwargs):
    return self.config_task_type(self, *args, **kwargs)

  def on_init(self):
    pass

  def on_reset(self):
    pass

  def on_apply_start(self):
    self.log(f'= apply= {self.name}')

  def on_apply(self):
    pass

  def on_apply_finish(self):
    pass

  def on_apply_error(self):
    if self.parent:
      self.log(f'- {self.name}, included by')
    else:
      self.log(f'- {self.name}')

  def on_apply_cancel(self):
    if not self.parent:
      self.log('Apply cancelled')

  def apply(self, system, *args, coordinator=None, **kwargs):
    apply = self.config_apply_type(
      'apply',
      self,
      system,
      coordinator,
      args,
      kwargs,
      self.on_init,
      self.on_apply_start,
      self.on_apply,
      self.on_apply_finish,
      self.on_apply_error,
      self.on_apply_cancel,
      self.on_reset,
    )
    return apply.run()

  def on_delete_start(self):
    self.log(f'=delete= {self.name}')

  def on_delete(self):
    pass

  def on_delete_finish(self):
    pass

  def on_delete_error(self):
    self.log('- ' + self.name)

  def on_delete_cancel(self):
    if not self.parent:
      self.log('Delete cancelled')

  def delete(self, system, *args, coordinator=None, **kwargs):
    delete = self.config_delete_type(
      'delete',
      self,
      system,
      coordinator,
      args,
      kwargs,
      self.on_init,
      self.on_delete_start,
      self.on_delete,
      self.on_delete_finish,
      self.on_delete_error,
      self.on_delete_cancel,
      self.on_reset,
    )
    return delete.run()

  def on_is_applied_start(self):
    pass

  def on_is_applied(self):
    return self.applied

  def on_is_applied_finish(self):
    c = ('- ' if self.applied else '* ') + ('..' * (self.depth + 1))
    self.log(f'{c} {self.name}')

  def on_is_applied_error(self):
    self.log('- ' + self.name)

  def on_is_applied_cancel(self):
    if not self.parent:
      self.log('Apply query cancelled')

  def is_applied(self, system, *args, coordinator=None, **kwargs):
    is_applied = self.config_is_applied_type(
      'is_applied',
      self,
      system,
      coordinator,
      args,
      kwargs,
      self.on_init,
      self.on_is_applied_start,
      self.on_is_applied,
      self.on_is_applied_finish,
      self.on_is_applied_error,
      self.on_is_applied_cancel,
      self.on_reset,
    )
    return is_applied.run()
