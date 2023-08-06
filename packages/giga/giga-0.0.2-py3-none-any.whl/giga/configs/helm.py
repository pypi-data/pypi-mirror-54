import giga
from giga.configs import kube
from lura import net
from lura.time import poll
from shlex import quote

log = giga.logs.get_logger(__name__)

class Helm(giga.Config):
  'Apply Helm binaries to a system.'

  version = '2.14.3'
  bin_dir = '/usr/local/bin'
  keep = False

  _bins = ['linux-amd64/helm', 'linux-amd64/tiller']

  def on_init(self):
    super().on_init()
    self.url = 'https://get.helm.sh/helm-v%s-linux-amd64.tar.gz' % self.version

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self._bins)} helm bins') as task:
      with self.system.tempdir() as temp_dir:
        tar = f'{temp_dir}/helm.tgz'
        for bin in self._bins:
          path = f'{self.bin_dir}/{bin.split("/")[-1]}'
          with task.item(f'curl {path}'):
            if not sys.isfile(path):
              if not sys.exists(tar):
                alg = 'sha256'
                sum = net.wgets(f'{self.url}.{alg}').rstrip().split()[0]
                sys.wget(self.url, tar, alg, sum)
              sys(f'tar xf {tar} -C {self.bin_dir} --strip=1 {bin}')
              +task
          task.ensure.fs.mode(path, 0o755)
          task.ensure.fs.owner(path, 'root')
          task.ensure.fs.group(path, 'root')

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task(f'Delete {len(self._bins)} helm bins') as task:
      for bin in self._bins:
        path = f'{self.bin_dir}/{bin.split("/")[-1]}'
        if not self.keep:
          task.ensure.fs.absent(path)

  def on_is_applied(self):
    sys = self.system
    bins = tuple(f'{self.bin_dir}/{bin.split("/")[-1]}' for bin in self._bins)
    return (
      super().on_is_applied() and
      all(sys.isfile(bin) for bin in bins) and
      all(sys.ismode(bin, 0o755) for bin in bins)
    )

class Tiller(kube.Resource):
  'Apply Tiller to a cluster.'

  history_max = 200
  create_timeout = 10
  ready_timeout  = 10
  force_delete = False
  keep = False

  _poll_interval = 0.2

  def get_pods(self):
    return tuple(
      pod for pod in self.get('pod', namespace='kube-system').get('items', [])
      if pod.metadata.name.startswith('tiller-deploy-')
    )

  def on_apply(self):
    super().on_apply()
    with self.task('Apply tiller') as task:
      sys = self.system
      with task.item('helm init'):
        if not self.get_pods():
          sys(f'helm init --history-max {self.history_max}')
          +task
    self.wait_for_deploy_create('tiller-deploy', 'kube-system')
    self.wait_for_pods_ready(self.get_pods)

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task('Apply helm reset') as task:
      with task.item('helm reset'):
        if not self.keep:
          if self.get_pods():
            if self.force_delete:
              sys('helm reset --force')
            else:
              sys('helm reset')
            +task

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      bool(self.get_pods()) # FIXME
    )

class Charts(kube.Resource):

  charts = None
  purge = True
  keep = False

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with self.task(f'Apply {len(self.charts)} helm charts') as task:
      for chart, name, values in self.charts:
        with task.item(f'{chart} {name}'):
          if sys.nonzero(f'helm status {name}'):
            argv = [f'helm install {chart} --name {name}']
            if values:
              for opt, val in values.items():
                argv.append(f'--set {quote(opt)}={quote(str(val))}')
            argv = ' '.join(argv)
            sys(argv)
            +task

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with self.task(f'Delete {len(self.charts)} helm charts') as task:
      if not self.keep:
        for chart, name, _ in self.charts:
          with task.item(f'{chart} {name}'):
            if sys.zero(f'helm status {name}'):
              if self.purge:
                sys(f'helm delete --purge {name}')
              else:
                sys(f'helm delete {name}')
              +task

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      all(
        self.system.zero(f'helm status {name}')
        for (_, name, _) in self.charts
      )
    )

class DockerRegistry(Charts):

  charts = [
    (
      'stable/docker-registry',
      'docker-registry',
      {
        'persistence.enabled': 'true',
        'service.type': 'NodePort',
        'service.nodePort': 32000,
      })]

  def get_pods(self):
    return tuple(
      pod for pod in self.get('pod', namespace='default').get('items', [])
      if pod.metadata.name.startswith('docker-registry-')
    )

  def on_apply(self):
    super().on_apply()
    self.wait_for_deploy_create('docker-registry', namespace='default')
    self.wait_for_pods_ready(self.get_pods)

giga.set_config_logger(__name__, log)
