'Command-line interface.'

import click
import giga
import os
import traceback
from getpass import getpass
from getpass import getuser
from importlib import import_module
from lura.attrs import attr
from lura.click import StartsWithGroup
from sys import exit
from tabulate import tabulate

log = logger = giga.logs.get_logger(__name__)

def parse_hosts(hosts):
  '''
  Parse the -h/--host argument.

  All things that accept -h handle it in the same way. The rules:

  * --host is repeatable:

      -h host1 -h host2 -h host3

  * --host can be a list of comma-delimited hosts:

      -h host1,host2,host3 -h host4,host5

  * --hosts can be given a name, which will be printed in the logs in lieu
    of long hostnames, which helps reduce the column count

      -h host1=zaybxcwd-01.mycompany.com,host2=zaybxcwd-02.mycompany.com

  * --hosts can be a filename containing a list of hosts with each line
    formatted as described above.

    The '#' character may be used in the file for comments, and blank lines
    are ignored.

      -h @myhosts.txt
  '''
  res = []
  for host in hosts:
    if host[0] == '@':
      path = host[1:]
      with open(path) as pathf:
        for line in pathf:
          line = line.strip()
          if not line or line[0] == '#':
            continue
          res.append(line)
    elif ',' in host:
      res.extend(host.rstrip(',').split(','))
    else:
      res.append(host)
  hosts = res
  res = []
  for host in hosts:
    if '=' in host:
      name, host = host.split('=', 1)
      res.append(name.strip(), host.strip())
    else:
      res.append((host, host))
  return res

def get_hosts(args, config, config_args, config_kwargs):
  '''
  Determine and return the list of hosts, a sequence of (name, host) pairs.
  The name field is intended as a short, friendly name for use in log
  messages. The host field is the address of the remote host. When no name
  is available, it should default to the host.

  If hosts are provided on the command line, then they are always used.

  If hosts are not provided on the command line, then the target Configuration
  may provide a hosts list by providing a `giga_hosts` attribute.

  The `Configuration.giga_hosts` attribute may be a sequence of pairs, or
  a callable which returns a sequence of pairs, as described above. The
  callable will be passed the exploded Configuration args and kwargs provided
  on the command line via -a and -A.

  Note that if multiple Configurations are specified for an operation, the
  `giga_hosts` from the first one will be used for all of them.
  ''' # FIXME

  name = (config if isinstance(type, config) else type(config)).__name__
  if args.host:
    return parse_hosts(args.host)
  elif hasattr(config, 'giga_hosts'):
    if callable(config.giga_hosts):
      hosts = config.giga_hosts(*config_args, **config_kwargs)
    else:
      hosts = config.giga_hosts
    if not hosts:
      log.error(f'fError: No hosts (-h) given, and {name}.giga_hosts is empty')
      exit(2)
  else:
    msg = 'Error: No hosts (-h) given, and %s has no giga_hosts attribute'
    log.error(msg % name)
    exit(2)

def get_passwords(args):
  'Sort out the password arguments.'

  password, super_password = args.login_password, args.super_password
  if not password and args.prompt_login:
    password = getpass('Login password: ')
  if not super_password and args.prompt_super:
    if password:
      super_password = getpass('Sudo password [enter to use login]: ')
      if super_password == '':
        super_password = password
    else:
      super_password = getpass('Super password: ')
  return password, super_password

def group(args):
  "Create a `giga.Group` for the systems we'll be working with."

  password, super_password = get_passwords(args)
  return giga.Group(
    args.hosts,
    user = args.user,
    password = password,
    super_password = super_password,
    connect_timeout = args.connect_timeout,
    auth_timeout = args.auth_timeout,
    super = args.super,
    compress = True,
    verbose = args.verbose,
  )

# here is probably a good time to talk about what these ok and err things
# are, and a bit about what giga.Group does
#
# when you create a giga.Group for a set of hosts (cf. _group() above),
# you can perform operations on that Group of hosts in parallel. those
# operations are:
#
# - apply      - applies a configuration to a host group
# - delete     - deletes a configuration from a host group
# - is-applied - show whether or not a configuration is applied to a host group
#
# so you have a bunch of threads running, usually applying or deleting a
# configuration over ssh. so all the threads finish, and apply or delete
# returns a pair of values: ok, err
#
# ok will be a list of pairs:  (giga.System, int(change_count))
# err will be a list of pairs: (giga.System, sys.exc_info())
#
# in the ok case, we gather up the change counts and summarize them.
#
# in the err case, a giga.Fail exception will have recorded the change
# count for the system at the time of its raise, so we gather up the change
# counts from the exceptions and summarize them.
#
# is-applied is not handled by the function below, but for completeness, here's
# how it works. for is-applied:
#
# ok will be a list of pairs:  (giga.System, bool(applied))
# err will be a list of pairs: (giga.System, sys.exc_info())
#
# in the err case for is-applied, the giga.Fail exception will not
# record additional state information at the time of its raise.

def log_change_summary(ok, err):
  'Log the change count for each host for apply/delete.'

  log = logger[logger.INFO]
  results = sorted(ok + err, key=lambda _: _[0].name)
  for res in results:
    sys, res = res
    if isinstance(res, int):
      if res == 0:
        log(f'[{sys.name}] (  done) %5d changes' % res)
      else:
        log(f'[{sys.name}] [  done] %5d changes' % res)
    else: # a giga.Fail/giga.Cancel exc_info
      log(f'[{sys.name}] [ error] %5d changes' % res[1].changes)

def log_err_tracebacks(err):
  'Attempt to log exceptions from hosts in a readable way.'

  def mark():
    log('')
    log('-' * 50)
  log = logger[logger.ERROR]
  for sys, exc in err:
    if isinstance(exc[1], giga.Cancel):
      continue
    elif isinstance(exc[1], giga.Fail):
      exc = exc[1].exc_info
    msg = f'[{sys.name}] Failed with unhandled exception' + os.linesep
    tb = ''.join(traceback.format_exception(*exc)).rstrip()
    mark()
    log(msg + tb)
  mark()

def lookup_config(config):
  'Lookup a Configuration object using its module and object name.'

  if '.' not in config:
    log.error(f'Error: invalid config "{config}", expected python object path')
    exit(2)
  mod, obj = config.rsplit('.', 1)
  try:
    mod = import_module(mod)
  except ModuleNotFoundError:
    log.error(f'Error: module not found: {mod}')
    exit(2)
  if not hasattr(mod, obj):
    log.error(f'Error: module "{mod.__name__}" has no objet "{obj}"')
    exit(2)
  obj = getattr(mod, obj)
  return obj

#####
## giga
@click.group('giga', cls=StartsWithGroup)
@click.option(
  '-v', '--verbose', is_flag=True, help='Enable verbose output.')
@click.option(
  '-d', '--debug', is_flag=True, help='Enable debug output.')
@click.pass_context
def cli_giga(ctx, verbose, debug):
  'Apply or delete configurations.'

  import lura
  level = log.DEBUG if debug else log.INFO
  format = giga.logs.formats.hax if verbose or debug else giga.logs.formats.user
  giga.logs.set_level(level)
  lura.logs.set_level(level)
  giga.logs.set_format(format)
  lura.logs.set_format(format)
  ctx.obj = attr(verbose=verbose, debug=debug)

#####
## giga apply
@cli_giga.command('apply')
@click.option(
  '-u', '--user', default=getuser(),
  help='Login username, default current user.')
@click.option(
  '-s', '--super', is_flag=True, help='Run as the superuser.')
@click.option(
  '-p', '--prompt-login', is_flag=True, help='Prompt for login password.')
@click.option(
  '-P', '--prompt-super', is_flag=True, help='Prompt for superuser password.')
@click.option(
  '--login-password', help='Specify login password.')
@click.option(
  '--super-password', help='Specify superuser password.')
@click.option(
  '-h', '--host', multiple=True, help='Host(s) to apply.')
@click.option(
  '-f', '--force', is_flag=True, help='Suppress is-applied check.')
@click.option(
  '-a', '--set-arg', multiple=True, help='Set a config arg.')
@click.option(
  '-A', '--set-kwarg', multiple=True, help='Set a config kwarg.')
@click.option(
  '--connect-timeout', default=120, envvar='GIGA_CONNECT_TIMEOUT',
  help='Connect timeout, default 120.')
@click.option(
  '--auth-timeout', default=120, envvar='GIGA_AUTH_TIMEOUT',
  help='Auth timeout, default 120.')
@click.argument(
  'config', nargs=-1, required=True)
@click.pass_obj
def cli_giga_apply(ctx, **args):
  'Apply a configuration.'

  args = attr(args)
  args.verbose = ctx.verbose
  configs = args.pop('config')
  try:
    for config in configs:
      apply(config, args)
  except Exception:
    log.exception(f'Unhandled exception while applying {config}')
    exit(2)

def apply(config, args):
  config = lookup_config(config)
  config_args = args.set_arg
  config_kwargs = attr()
  for kwarg in args.set_kwarg:
    k, v = kwarg.split('=', 1)
    config_kwargs[k] = v
  args.hosts = get_hosts(args, config, config_args, config_kwargs)
  grp = group(args)
  if not args.force:
    ok, err = grp.is_applied(config, *config_args, **config_kwargs)
    if err:
      log_err_tracebacks(err)
      exit(2)
    if all(res for (_, res) in ok):
      return
  ok, err = grp.apply(config, *config_args, **config_kwargs)
  if err:
    log_err_tracebacks(err)
    log_change_summary(ok, err)
    exit(2)
  log_change_summary(ok, err)

#####
## giga delete
@cli_giga.command('delete')
@click.option(
  '-u', '--user', default=getuser(), show_default='current user',
  help='Login username.')
@click.option(
  '-s', '--super', is_flag=True, help='Run as the superuser.')
@click.option(
  '-p', '--prompt-login', is_flag=True, help='Prompt for login password.')
@click.option(
  '-P', '--prompt-super', is_flag=True, help='Prompt for superuser password.')
@click.option(
  '--login-password', help='Specify login password.')
@click.option(
  '--super-password', help='Specify superuser password.')
@click.option(
  '-h', '--host', multiple=True, help='Host(s) to delete.')
@click.option(
  '-f', '--force', is_flag=True, help='Delete if alread deleted.')
@click.option(
  '-a', '--set-arg', multiple=True, help='Set a config arg.')
@click.option(
  '-A', '--set-kwarg', multiple=True, help='Set a config kwarg.')
@click.option(
  '--connect-timeout', default=120, envvar='GIGA_CONNECT_TIMEOUT',
  help='Connect timeout, default 120.')
@click.option(
  '--auth-timeout', default=120, envvar='GIGA_AUTH_TIMEOUT',
  help='Auth timeout, default 120.')
@click.argument(
  'config', nargs=-1, required=True)
@click.pass_obj
def cli_giga_delete(ctx, **args):
  'Delete a configuration.'

  args = attr(args)
  args.verbose = ctx.verbose
  configs = args.pop('config')
  try:
    for config in configs:
      delete(config, args)
  except Exception:
    log.exception('Unhandled exception while deleting')
    exit(2)

def delete(config, args):
  config = lookup_config(config)
  config_args = args.set_arg
  config_kwargs = attr()
  for kwarg in args.set_kwarg:
    k, v = kwarg.split('=', 1)
    config_kwargs[k] = v
  args.hosts = get_hosts(args, config, config_args, config_kwargs)
  grp = group(args)
  if not args.force:
    ok, err = grp.is_applied(config, *config_args, **config_kwargs)
    if err:
      log_err_tracebacks(err)
      exit(2)
    if all(not res for (_, res) in ok):
      return
  ok, err = grp.delete(config, *config_args, **config_kwargs)
  if err:
    log_err_tracebacks(err)
    log_change_summary(ok, err)
    exit(2)
  log_change_summary(ok, err)

#####
## giga is-applied
@cli_giga.command('is-applied')
@click.option(
  '-u', '--user', default=getuser(), show_default='current user',
  help='Login username.')
@click.option(
  '-s', '--super', is_flag=True, help='Run as the superuser.')
@click.option(
  '-p', '--prompt-login', is_flag=True, help='Prompt for login password.')
@click.option(
  '-P', '--prompt-super', is_flag=True, help='Prompt for superuser password.')
@click.option(
  '--login-password', help='Specify login password.')
@click.option(
  '--super-password', help='Specify super password.')
@click.option(
  '-h', '--host', multiple=True, help='Host(s) to query.')
@click.option(
  '-a', '--set-arg', multiple=True, help='Set a config arg.')
@click.option(
  '-A', '--set-kwarg', multiple=True, help='Set a config kwarg.')
@click.option(
  '--connect-timeout', default=120, envvar='GIGA_CONNECT_TIMEOUT',
  help='Connect timeout, default 120.')
@click.option(
  '--auth-timeout', default=120, envvar='GIGA_AUTH_TIMEOUT',
  help='Auth timeout, default 120.')
@click.argument(
  'config', nargs=-1, required=True)
@click.pass_obj
def cli_giga_is_applied(ctx, **args):
  'Check if a configuration is applied.'

  args = attr(args)
  args.verbose = ctx.verbose
  configs = args.pop('config')
  res = 0
  try:
    for config in configs:
      if not is_applied(config, args):
        res = 1
  except Exception:
    log.exception('Unhandled exception while checking apply state')
    exit(2)
  exit(res)

def is_applied(config, args):
  config = lookup_config(config)
  config_args = args.set_arg
  config_kwargs = attr()
  for kwarg in args.set_kwarg:
    k, v = kwarg.split('=', 1)
    config_kwargs[k] = v
  args.hosts = get_hosts(args, config, config_args, config_kwargs)
  grp = group(args)
  ok, err = grp.is_applied(config, *config_args, **config_kwargs)
  if err:
    log_err_tracebacks(err)
    exit(2)
  return all(res for (_, res) in ok)

#####
### giga list
@cli_giga.command('list')
@click.argument(
  'module', nargs=-1)
def cli_giga_list(module):
  'List configurations in a module.'

  pass

if __name__ == '__main__':
  cli_giga()
