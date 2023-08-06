'Filesystem provisioners.'

import giga
import os
from lura import fs
from lura.plates import jinja2

log = giga.logs.get_logger(__name__)

class Directories(giga.Config):
  'Create directories.'

  paths         = None
  keep          = False
  keep_nonempty = True
  config_logger = log

  def on_apply(self):
    super().on_apply()
    with self.task(f'Apply {len(self.paths)} directories') as task:
      for dir in self.paths:
        task.ensure.fs.directory(dir)

  def on_delete(self):
    super().on_delete()
    with self.task(f'Delete {len(self.paths)} directories') as task:
      if not self.keep:
        for dir in reversed(self.paths):
          if self.keep_nonempty and len(self.system.ls(dir)) > 0:
            continue
          task.ensure.fs.absent(dir)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      all(self.system.isdir(dir) for dir in self.paths)
    )

class Files(giga.Config):
  'Copy files from the local system.'

  paths = None
  keep  = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    with self.task(f'Apply {len(self.paths)} files') as task:
      for src, dst in paths:
        task.ensure.fs.contents(dst, fs.loads(src))

  def on_delete(self):
    super().on_delete()
    with self.task(f'Delete {len(self.paths)} files') as task:
      if not self.keep:
        for _, dst in reversed(self.paths):
          task.ensure.fs.absent(dst)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      all(
        self.system.iscontents(dst, fs.loads(src))
        for (src, dst) in self.paths
      )
    )

class TemplateFiles(giga.Config):
  'Expand templates from the local system.'

  paths = None
  env   = None
  keep  = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self.path)} templates') as task:
      for src, dst in self.paths:
        contents = jinja2.expandss(self.env, fs.loads(src))
        task.ensure.fs.contents(dst, contents)

  def on_delete(self):
    super().on_delete()
    with self.task(f'Delete {len(self.paths)} assets') as task:
      if not self.keep:
        with _, dst in reversed(self.paths):
          task.ensure.fs.absent(dst)

  def on_is_applied(self):
    sys = self.system
    return (
      super().on_is_applied() and
      all(
        sys.iscontents(dst, jinja2.expandss(self.env, fs.loads(src)))
        for (src, dst) in self.paths
      )
    )

class Symlinks(giga.Config):
  'Create symlinks.'

  paths = None
  keep  = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self.paths)} symlinks') as task:
      for src, dst in self.paths:
        task.ensure.fs.symlink(src, dst)

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task(f'Delete {len(self.paths)} symlinks') as task:
      if not self.keep:
        for _, dst in reversed(self.paths):
          task.ensure.fs.absent(dst)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      all(self.system.islink(dst) for (_, dst) in self.paths)
    )

class Modes(giga.Config):
  'Set file modes.'

  paths = None
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self.paths)} modes') as task:
      for path, mode in self.paths:
        task.ensure.fs.mode(path, mode)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      all(self.system.ismode(path, mode) for (path, mode) in self.paths)
    )

class Contains(giga.Config):

  contents = None
  paths = None
  keep = False
  config_logger = log

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self.paths)} file content(s)') as task:
      for path, contents in self.paths:
        task.ensure.fs.in_file(path, contents)

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task(f'Delete {len(self.paths)} file content(s)') as task:
      if not self.keep:
        for path, contents in self.paths:
          task.ensure.fs.not_in_file(path, contents)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      all(self.system.contains(p, c) for (p, c) in self.paths)
    )

class Chowns(giga.Config):

  paths = None
  config_logger = log

  def on_apply(self):
    super().on_apply()
    with self.task(f'Apply {len(self.paths)} owners') as task:
      for path, owner, group in self.paths:
        if owner:
          task.ensure.fs.owner(path, owner)
        if group:
          task.ensure.fs.group(path, group)

  def on_is_applied(self):
    sys = self.system
    return (
      super().on_is_applied() and
      all(
        sys.exists(path) or sys.islink(path) for (path, _, _) in self.paths
      ) and
      all(
        sys.isowner(path, owner) for (path, owner, _) in self.paths
        if owner
      ) and
      all(
        sys.isgroup(path, group) for (path, _, group) in self.paths
        if group
      )
    )
