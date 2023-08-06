import giga
from giga import configs

log = giga.logs.get_logger(__name__)

class Debian(configs.os.Apt):

  packages = ['docker.io']
  config_logger = log

class RedHat(configs.os.Yum):
  'Install Docker on a RedHat system.'

  pass # FIXME

class Docker(giga.Config):

  config_logger = log

  def config_include(self):
    family = self.system.os.family
    if family == 'debian':
      return [Debian]
    elif family == 'redhat':
      return [RedHat]
    else:
      raise giga.NotImplementedFor(family)

class DockerCompose(configs.utils.CurlBins):
  'Install docker-compose on a system.'

  version = '1.24.1'
  bin_dir = '/usr/local/bin'
  config_logger = log

  def on_init(self):
    super().on_init()
    url = 'https://github.com/docker/compose/releases/download/%s/docker-compose-Linux-x86_64' % self.version
    self.bins = [(f'{self.bin_dir}/docker-compose', url, 'sha256', f'{url}.sha256')]
