'Netdata configurations.'

import giga
import io
from configparser import ConfigParser
from giga import configs
from lura.attrs import ottr
from lura.hash import hashs
from shlex import quote

log = giga.logs.get_logger(__name__)

class Debian(configs.os.Apt):
  'Apply Debian packages needed by netdata.'

  packages = [
    'zlib1g-dev',
    'uuid-dev',
    'libuv1-dev',
    'liblz4-dev',
    'libjudy-dev',
    'libssl-dev',
    'libmnl-dev',
    'gcc',
    'make',
    'git',
    'autoconf',
    'autoconf-archive',
    'autogen',
    'automake',
    'pkg-config',
    'curl',
    'python',
    'python-pip',
    'python-ipaddress',
    'lm-sensors',
    'libmnl0',
    'netcat',
  ]

class RedHat(configs.os.Yum):
  '''
  Apply RedHat packages needed by netdata and enable rc-local. epel and ius
  must already be installed.
  '''

  packages = [
    'automake',
    'curl',
    'gcc',
    'git2u-core',
    'libmnl-devel',
    'libuuid-devel',
    'openssl-devel',
    'libuv-devel',
    'lz4-devel',
    'Judy-devel',
    'make',
    'pkgconfig',
    'python',
    'python-pip',
    'python-ipaddress',
    'zlib-devel',
    'lm_sensors',
    'libmnl',
    'nc',
  ]

class Python(configs.python.Packages):

  py = 2
  packages = ['dnspython']

class Packages(giga.Config):

  def config_include(self):
    include = []
    family = self.system.os.family
    if family == 'debian':
      include.append(Debian)
    elif family == 'redhat':
      include.append(RedHat)
    else:
      raise ValueError(f'Unsupported os family: {family}')
    include.append(Python)
    return include

class Ksm(giga.Config):
  '''
  Arrange for ksm to be enabled at boot and enable ksm immediately when
  settings.ksm is True.

  ksm[1] is 'kernel samepage merging', a feature of the Linux kernel which can
  merge identical memory pages into a single copy-on-write page, thus
  introducing significant memory savings for certain workloads. The netdata
  authors claim that ksm can reduce netdata's memory usage by up to 60%.
  There's really no reason to disable it, but this is a base class, so we leave
  it to you.

  [1] https://en.wikipedia.org/wiki/Kernel_same-page_merging
  '''

  settings = None

  _ksm = (
    'echo 1 >/sys/kernel/mm/ksm/run',
    'echo 1000 >/sys/kernel/mm/ksm/sleep_millisecs',
  )
  _ksm = '\n' + '\n'.join(_ksm) + '\n'

  def config_include(self):
    return [configs.os.RcLocal755] if self.settings.ksm else []

  def on_apply(self):
    super().on_apply()
    with self.task('Apply kernel samepage merging') as task:
      if self.settings.ksm:
        task.ensure.fs.in_file('/etc/rc.local', self._ksm)
        task.ensure.fs.pseudofs('/sys/kernel/mm/ksm/run', 1)
        task.ensure.fs.pseudofs('/sys/kernel/mm/ksm/sleep_millisecs', 1000)

  def on_delete(self):
    super().on_delete()
    settings = self.settings
    with self.task('Delete kernel samepage merging') as task:
      if settings.ksm:
        if not settings.ksm_keep:
          task.ensure.fs.not_in_file('/etc/rc.local', self._ksm)
          task.ensure.fs.pseudofs('/sys/kernel/mm/ksm/run', 0)

  def on_is_applied(self):
    sys = self.system
    return (
      super().on_is_applied() and
      sys.exists('/etc/rc.local') and
      sys.contains('/etc/rc.local', self._ksm)
    )

class Installer(giga.Config):
  'Apply netdata package installation.'

  settings = None

  def on_apply(self):
    super().on_apply()
    sys = self.system
    settings = self.settings
    with self.task('Apply netdata package') as task:
      root = quote(settings.root)
      uninstaller = f'{root}/netdata/usr/libexec/netdata/netdata-uninstaller.sh'
      if not sys.isfile(uninstaller):
        with sys.tempdir(prefix='netdata.') as temp_dir:
          repo_url = 'https://github.com/netdata/netdata'
          repo_dir = f'{temp_dir}/netdata'
          args = f'--dont-wait --dont-start-it --install {root}'
          if not settings.telemetry:
            args += ' --disable-telemetry'
          task.ensure.git.cloned(repo_dir, repo_url, f'v{settings.version}')
          with task.item('netdata-installer.sh'):
            sys(f'$SHELL netdata-installer.sh {args}', cwd=repo_dir)
            +task

  def on_delete(self):
    super().on_delete()
    sys = self.system
    root = quote(self.settings.root)
    uninstaller = f'{root}/netdata/usr/libexec/netdata/netdata-uninstaller.sh'
    with self.task('Delete netdata package') as task:
      with task.item('netdata-uninstaller.sh'):
        if sys.isfile(uninstaller):
          sys(f'{uninstaller} -y -f')
          +task

  def on_is_applied(self):
    root = quote(self.settings.root)
    uninstaller = f'{root}/netdata/usr/libexec/netdata/netdata-uninstaller.sh'
    return (
      super().on_is_applied() and
      self.system.isfile(uninstaller)
    )

class Conf(giga.Config):
  '''
  Apply custom values to netdata.conf.

  `settings.conf` must be a list of tuples:

    ('config section', 'variable name', 'new value')

  For example, to set the history limit to 24 hours:

    ('global', 'history', 86400)
  '''

  settings = None

  def on_apply(self):
    super().on_apply()
    settings = self.settings
    if not settings.conf:
      return
    sys = self.system
    path = f'{settings.root}/netdata/etc/netdata/netdata.conf'
    config = ConfigParser()
    with io.StringIO(sys.loads(path)) as buf:
      config.read_file(buf)
    with self.task(f'Apply {len(settings.conf)} netdata.conf values') as task:
      for section, key, value in (self.settings.conf or ()):
        if value is None:
          raise ValueError(f'netdata.conf: {section}.{key}: value is None')
        value = str(value)
        with task.item(f'conf {section} {key}'):
          if (
            section in config and
            key in config[section] and
            config[section][key] == value
          ):
            continue
          config.setdefault(section, {})
          config[section][key] = value
          +task
    with io.StringIO() as buf:
      config.write(buf)
      task.ensure.fs.contents(path, buf.getvalue())

  def on_is_applied(self):
    return (
      super().on_is_applied() # FIXME
    )

class Healthd(giga.Config):
  '''
  Apply custom values to health.d conf files.

  `settings.healthd` must be a list of tuples:

    ('conf filename', {selector fields}, {update fields})

  For example, to silence the `ram_in_use` alarm on Linux:

   ('ram.conf', {'alarm': 'ram_in_use', 'os': 'linux'}, {'to': 'silent'})
  '''

  # FIXME allow the selector to be a callable to which we will pass a check;
  #       the callable would return True if the check matches, else False.
  #       the issue is that we need to provide a way to select on field
  #       presence, rather than field value. a user may know the field name
  #       but they may not reliably know its value to use in a selector

  settings = None

  def load_checks(self, path):
    sys = self.system
    checks = []
    check = None
    with io.StringIO(sys.loads(path)) as buf:
      for line in buf:
        line = line.strip()
        if not line or line[0] == '#':
          continue
        k, v = line.split(': ', 1)
        if k in ('alarm', 'template'):
          check = ottr()
          checks.append(check)
        check[k] = v
    return checks

  def format_checks(self, checks):
    with io.StringIO() as buf:
      for check in checks:
        field_len = max(len(k) for k in check)
        for (k, v) in check.items():
          if v is None:
            # FIXME setting a field's value to None will remove the field
            #       entirely from the check. this is undesriable because then
            #       the field can no longer be matched by a selector. we should
            #       see if netdata can gracefully handle empty fields so that
            #       they don't need to be removed to be disabled
            continue
          k = '%s%s' % (' ' * (field_len - len(k)), k)
          buf.write(f'{k}: {v}\n')
        buf.write('\n')
      return buf.getvalue()

  def apply_healthd_change(self, task, file, selector, update):
    settings = self.settings
    path = f'{settings.root}/netdata/usr/lib/netdata/conf.d/health.d/{file}'
    checks = self.load_checks(path)
    sum_old = hashs(self.format_checks(checks))
    selected = tuple(
      check for check in checks
      if all(k in check and check[k] == v for (k, v) in selector.items())
    )
    if len(selected) == 0:
      return # FIXME what to do here
    for check in selected:
      for k in update:
        check[k] = update[k]
    contents = self.format_checks(checks)
    sum_new = hashs(contents)
    msg = f'healthd {path.split("conf.d/")[1]} {", ".join(update.keys())}'
    with task.item(msg):
      if sum_old != sum_new:
        task.ensure.fs.backuponce(path)
        task.ensure.fs.contents(path, contents)

  def on_apply(self):
    super().on_apply()
    settings = self.settings
    with self.task(f'Apply {len(settings.healthd)} health.d updates') as task:
      for file, selector, update in (settings.healthd or ()):
        self.apply_healthd_change(task, file, selector, update)

  def on_is_applied(self):
    return (
      super().on_is_applied() # FIXME
    )

class CustomSender(giga.Config):
  '''
  Apply a custom_sender() bash function to health_alarm_notify.conf when
  settings.custom_sender is set.
  '''

  settings = None

  def on_apply(self):
    super().on_apply()
    sys = self.system
    settings = self.settings
    with self.task('Apply custom sender') as task:
      if not settings.custom_sender:
        return
      custom_sender = settings.custom_sender
      root = quote(settings.root)
      path = f'{root}/netdata/usr/lib/netdata/conf.d/health_alarm_notify.conf'
      with io.StringIO(sys.loads(path)) as cf, io.StringIO() as buf:
        while True:
          line = cf.readline()
          if line == '':
            break
          if line.startswith('DEFAULT_RECIPIENT_CUSTOM='):
            buf.write('DEFAULT_RECIPIENT_CUSTOM="custom"\n')
            continue
          elif line.rstrip() == 'custom_sender() {':
            buf.write(custom_sender)
            while True:
              line = cf.readline()
              if line == '':
                raise RuntimeError('Received EOF before end of custom_sender()')
              elif line.rstrip() == '}':
                break
            continue
          buf.write(line)
        task.ensure.fs.backuponce(path)
        task.ensure.fs.contents(path, buf.getvalue())

  def on_is_applied(self):
    sys = self.system
    settings = self.settings
    root = quote(settings.root)
    path = f'{root}/netdata/usr/lib/netdata/conf.d/health_alarm_notify.conf'
    return (
      super().on_is_applied() and
      sys.exists(path) and
      sys.contains(path, settings.custom_sender)
    )

class Start(configs.systemd.Starts):

  services = ['netdata']

class Netdata(giga.Config):

  version       = '1.18.1'
  root          = '/opt'
  start         = True
  telemetry     = True
  ksm           = True
  ksm_keep      = False
  conf          = None
  healthd       = None
  custom_sender = None

  def config_include(self):
    include = [
      Packages,
      Ksm(settings=self),
      Installer(settings=self),
      Conf(settings=self),
      Healthd(settings=self),
      CustomSender(settings=self),
    ]
    if self.start:
      include.append(Start)
    return include
