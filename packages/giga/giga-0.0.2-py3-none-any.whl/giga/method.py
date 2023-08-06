'Implements apply(), delete(), and is_applied() methods of giga.Config.'

import giga
import sys
from abc import abstractmethod

log = giga.logs.get_logger(__name__)

class Abort(RuntimeError):

  def __init__(self, method, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.changes = 0
    self.applied = True
    self.update(method)

  def update(self, method):
    if isinstance(method, Change):
      self.changes = method.result()
    elif isinstance(method, IsApplied):
      self.applied = method.result()

class Cancel(Abort):

  def __init__(self, method):
    super().__init__(method, 'Config cancelled')

class Fail(Abort):

  def __init__(self, method, exc_info):
    super().__init__(method, 'Config failed')
    self.exc_info = exc_info

class Method:
  '''
  Abstract base method type. The methods of this class represent the execution
  steps of the apply(), delete(), and is_applied() methods of giga.Conifg. The
  run() method of this class glues these steps together, effectively
  executing the method of giga.Config represented by a concrete instance
  of this abstract base class.

  From an execution perspective, there is very little difference between
  apply(), delete(), and is_applied(). We're only running handlers, and they're
  all executed in the same general way, with minor differences between them;
  convention (how users choose to implement their Config handlers) is largely
  what differentiates the methods, semantically.

  This base class encapsulates those aspects of execution common to all
  three methods. Sub-classes will implement the small bits of behavior
  unique to each method by implementing the following methods of this class:

  - include_early()          - abstract method
  - work_result(on_work_res) - optional method needed for is_applied()
  - include_late()           - abstract method
  - result()                 - abstract method
  '''

  cancel_type = Cancel
  fail_type = Fail

  def __init__(
    self, method, config, system, coordinator, args, kwargs, on_init,
    on_start, on_work, on_finish, on_error, on_cancel, on_reset
  ):
    super().__init__()
    self.method = method
    self.config = config
    self.system = system
    self.coordinator = coordinator
    self.args = args
    self.kwargs = kwargs
    self.on_init = on_init
    self.on_start = on_start
    self.on_work = on_work
    self.on_finish = on_finish
    self.on_error = on_error
    self.on_cancel = on_cancel
    self.on_reset = on_reset

  def init(self):
    'Set the standard attributes on the config.'

    config = self.config
    if isinstance(self.system, giga.Config):
      parent = self.system
      config.parent = parent
      config.system = parent.system
      config.coordinator = parent.coordinator
      config.args = parent.args
      config.kwargs = parent.kwargs
    else:
      config.parent = None
      config.system = self.system
      config.coordinator = self.coordinator
      config.args = self.args
      config.kwargs = self.kwargs

  def reset(self):
    'Reset the standard attributes on the config to their pristine state.'

    config = self.config
    vars(config).clear()
    config.parent = None
    config.system = None
    config.coordinator = None
    config.args = None
    config.kwargs = None

  def wait(self, cond, timeout):
    'Wait for the given condition when using a coordinator.'

    coord = self.config.coordinator
    if coord:
      if coord.cancelled:
        raise Cancel(self)
      coord.wait(cond, timeout=timeout)
      if coord.cancelled:
        raise Cancel(self)

  def ready(self):
    '''
    If the Config is a root config (has no parent), then wait for the
    ready condition; else wait for the sync condition.
    '''

    config = self.config
    if config.parent:
      config.sync()
    else:
      self.wait('ready', timeout=config.config_ready_timeout)

  def done(self):
    '''
    If the Config is a root config (has no parent), then wait for the
    done condition; else wait for the sync condition.
    '''

    config = self.config
    if config.parent:
      config.sync()
    else:
      self.wait('done', timeout=config.config_done_timeout)

  def cancel(self):
    'Cancel when configured to fail early, or if not using a coordinator.'

    coord = self.config.coordinator
    if coord:
      if coord.fail_early:
        coord.cancel()
    else:
      raise Cancel(self) # FIXME hmm

  def include(self, include):
    '''
    Apply the method represented by this class to all configs in include.
    '''

    if include is None:
      return ()
    if callable(include):
      include = include()
    res = []
    for config in include:
      if isinstance(config, type):
        config = config()
      method = getattr(config, self.method)
      result = method(self.config)
      res.append(result)
    return res

  @abstractmethod
  def include_early(self):
    'Run the early included configs.'

    pass

  def work_result(self, on_work_res):
    '''
    Update instance state using the result of on_work().

    Users' on_finish() handlers need a way to access the result of on_work()
    in the case where on_work() returns a meaningful value - for example,
    on_is_applied(). on_apply() and on_delete() don't need to bother with this
    becuase their return values are currently ignored, therefore this
    method is not abstract.
    '''

    pass

  @abstractmethod
  def include_late(self):
    'Run the late included configs.'

    pass

  @abstractmethod
  def result(self):
    'Return the result of the method.'

    pass

  def error(self, exc):
    'Handle exceptions.'

    config = self.config
    if isinstance(exc, self.cancel_type):
      config.on_cancel()
      exc.update(self)
      raise
    elif isinstance(exc, self.fail_type):
      self.on_error()
      exc.update(self)
      raise
    else:
      self.cancel()
      self.on_error()
      raise self.fail_type(self, sys.exc_info())

  def run(self):
    'Apply the method to the config.'

    try:
      self.init()
      self.on_init()
      self.ready()
      self.include_early()
      self.on_start()
      res = self.on_work()
      self.work_result(res)
      self.on_finish()
      self.include_late()
      self.done()
      return self.result()
    except Exception as exc:
      self.error(exc)
    finally:
      self.reset()
      self.on_reset()

class Change(Method):
  'Base class for apply() and delete() methods.'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.include_early_changes = 0
    self.include_late_changes = 0

  def init(self):
    super().init()
    self.config.changes = 0

  def reset(self):
    super().reset()
    self.config.changes = None

  def result(self):
    return (
      self.include_early_changes +
      self.config.changes +
      self.include_late_changes
    )

class Apply(Change):
  'Implements giga.Config.apply().'

  def include_early(self):
    config = self.config
    include = config.config_include
    if include:
      res = self.include(include)
      self.include_early_changes = sum(res)

  def include_late(self):
    config = self.config
    include = config.config_after
    if include:
      res = self.include(include)
      self.include_late_changes = sum(res)

class Delete(Change):
  'Implements giga.Config.delete().'

  def include(self, include):
    if callable(include):
      include = include()
    include = reversed(include)
    return super().include(include)

  def include_early(self):
    config = self.config
    include = config.config_after
    if include:
      res = self.include(include)
      self.include_early_changes = sum(res)

  def include_late(self):
    config = self.config
    include = config.config_include
    if include:
      res = self.include(include)
      self.include_late_changes = sum(res)

class IsApplied(Method):
  'Implements giga.Config.is_applied().'

  def init(self):
    super().init()
    self.config.applied = True

  def reset(self):
    super().reset()
    self.config.applied = None

  def include_early(self):
    config = self.config
    include = config.config_include
    res = self.include(include)
    config.applied = config.applied and all(res)

  def work_result(self, on_work_res):
    if isinstance(on_work_res, bool):
      self.config.applied = self.config.applied and on_work_res

  def include_late(self):
    config = self.config
    include = self.include(config.config_after)
    res = self.include(include)
    config.applied = config.applied and all(res)

  def result(self):
    return self.config.applied
