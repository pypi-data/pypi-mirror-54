import giga
from giga.configs import utils
from lura.attrs import attr
from lura.formats import json
from lura.time import poll

log = giga.logs.get_logger(__name__)

class Kubectl(utils.CurlBins):

  version = '1.15.4'
  bin_dir = '/usr/local/bin'
  config_logger = log

  def on_init(self):
    super().on_init()
    url = 'https://storage.googleapis.com/kubernetes-release/release/v%s/bin/linux/amd64/kubectl' % self.version
    self.bins = [(f'{self.bin_dir}/kubectl', url, 'sha256', f'{url}.sha256', )]

class Kc(giga.Config):

  bin_dir = '/usr/local/bin'
  keep = False
  config_logger = log

  _kc = '#!/bin/sh\nexec kubectl "$@"\n'

  def on_apply(self):
    super().on_apply()
    kc_path = f'{self.bin_dir}/kc'
    with self.task(f'Apply {kc_path}') as task:
      task.ensure.fs.contents(kc_path, self._kc)
      task.ensure.fs.mode(kc_path, 0o755)

  def on_delete(self):
    super().on_delete()
    kc_path = f'{self.bin_dir}/kc'
    with self.task(f'Delete {kc_path}') as task:
      if not self.keep:
        task.ensure.fs.absent(kc_path)

  def on_is_applied(self):
    sys = self.system
    kc_path = f'{self.bin_dir}/kc'
    return(
      super().on_is_applied() and
      sys.iscontents(kc_path, self._kc) and
      sys.ismode(kc_path, 0o755)
    )

class Resource(giga.Config):

  poll_interval = 0.3
  deploy_create_timeout = 300
  pods_ready_timeout = 300
  config_logger = log

  def get(self, type, name=None, namespace=None):
    'Return a parsed call to kubectl get --output=json.'

    argv = [f'kubectl get {type}']
    if name:
      argv.append(name)
    if namespace == '*':
      argv.append('--all-namespaces')
    elif namespace:
      argv.append(f'--namespace={namespace}')
    argv.append('--output=json')
    argv = ' '.join(argv)
    res = self.system(argv, enforce=False)
    if res.return_code != 0:
      return attr()
    return json.loads(res.stdout)

  def is_deploy_created(self, deploy, namespace):
    deploys = self.get('deploy', namespace=namespace).get('items', [])
    return any(_.metadata.name.startswith(deploy) for _ in deploys)

  def wait_for_deploy_create(self, deploy, namespace):
    with self.task('Wait for deploy create') as task:
      test = lambda: self.is_deploy_created(deploy, namespace)
      timeout = self.deploy_create_timeout
      if not poll(test, timeout=timeout, pause=self.poll_interval):
        raise TimeoutError(f'Timed out waiting for deploy: {deploy}')

  def wait_for_pods_ready(self, getter):
    with self.task(f'Wait for pods ready') as task:
      def test():
        return all(
          all(
            status.ready for status in pod.status.containerStatuses
          ) if 'containerStatuses' in pod.status else False for pod in getter()
        )
      timeout = self.pods_ready_timeout
      if not poll(test, timeout=timeout, pause=self.poll_interval):
        raise TimeoutError(f'Timed out waiting for pods')
