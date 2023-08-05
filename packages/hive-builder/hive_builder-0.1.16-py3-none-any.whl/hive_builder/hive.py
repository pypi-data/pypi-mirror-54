#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 Procube Co., Ltd.

"""
hive: support tool to build docker site
"""
import argparse
import configparser
import subprocess
import os
import yaml
from logging import getLogger, StreamHandler, DEBUG, INFO
import backtrace
import sys
import re
import select
import termios
import tty
import pty
import signal
import time
import pathlib


def get_python_path():
  for path in os.getenv("PATH").split(os.path.pathsep):
    full_path = os.path.join(path, 'python')
    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
      return full_path


class Error(Exception):
  pass


def directory_cast(directory):
  if directory.endswith('/'):
    directory = directory[:-1]
  if not os.path.isdir(directory):
    raise Error(f'{directory} is not a directory')
  return os.path.abspath(directory)


def int_cast(int_string):
  try:
    return int(int_string)
  except ValueError:
    raise Error(f'cannot parse as integer {int_string}')


def enum_cast(value, options):
  if value not in options:
    raise Error(f'value {value} not in {options}')
  return value


def bool_cast(s):
  if s.lower() in ["true", "yes", "1"]:
    return True
  if s.lower() in ["false", "no", "0"]:
    return False
  raise Error(f'boolean value {s} not in ["true", "yes", "1", "false", "no", "0"]')


class commandHandlerBase:
  def __init__(self, name, description):
    self.name = name
    self.description = description
    self.logger = getLogger('hive')

  def setup_parser(self, subparsers, variables_metainf):
    self.subparser = subparsers.add_parser(
        self.name, description=self.description, help='see `{0} -h`'.format(self.name))
    self.subparser.set_defaults(handler=self)


class initializeEnvironment(commandHandlerBase):
  def __init__(self):
    super().__init__('init', 'initialize hive environment')

  def do(self, context):
    if context.initialize():
      self.logger.info('Success to initialize hive context on {0}'.format(
          f'{context.vars["root_dir"]}/.hive'))
    else:
      self.logger.info('hive context on {0} is already initialized'.format(
          f'{context.vars["root_dir"]}/.hive'))


class setPersistent(commandHandlerBase):
  def __init__(self):
    super().__init__('set', 'set hive variable persistently')

  def do(self, context):
    name = context.args.variable_name
    casted_value = context.get_cast(name)(context.args.value)
    scope = context.set_persistent(name, casted_value)
    context.save_persistent()
    context.logger.info(f'set persistently {casted_value} to {name} on {scope}')

  def setup_parser(self, subparsers, variables_metainf):
    super().setup_parser(subparsers, variables_metainf)
    self.subparser.add_argument('variable_name', help='variable name')
    self.subparser.add_argument('value', help='variable value')


class hiveContext:
  def __init__(self):
    self.init_logger()

  def setup(self, subcommand_handlers):
    self.load_variables_metainf()
    self.args = self.get_parser(subcommand_handlers).parse_args()
    # raise SystemExit when invalid argument or -h option is specified
    self.reset_logger()
    self.vars = {'root_dir': self.args.root_dir,
                 'install_dir': os.path.abspath(os.path.dirname(__file__)),
                 'local_python_path': get_python_path()}
    self.load_persistents()
    self.load_command_line_options()
    self.overwritables = []
    self.load_defaults()
    self.overwritables = []
    self.logger.debug(f'varaiables initialized as {self.vars}')

  def load_variables_metainf(self):
    variables_metainf_path = os.path.dirname(
        __file__) + '/variables_metainf.yml'
    if os.path.exists(variables_metainf_path):
      with open(variables_metainf_path, 'r+') as envf:
        self.variables_metainf = yaml.load(envf, Loader=yaml.SafeLoader)
      self.logger.debug('variables meta information {0} is loaded from {1}'.format(
          self.variables_metainf, variables_metainf_path))

  def load_persistents(self):
    # persistent format
    # varname:
    #   global: global value
    #   private: value for private stage
    #   staging: value for staging stage
    #   production: value for production stage
    persistent_values_path = f'{self.vars["root_dir"]}/.hive/persistents.yml'
    if os.path.exists(persistent_values_path):
      with open(persistent_values_path, 'r+') as envf:
        self.persistent_values = yaml.load(envf, Loader=yaml.SafeLoader)
      self.logger.debug('persistent values {0} is loaded from {1}'.format(
          self.persistent_values, persistent_values_path))
    else:
      self.persistent_values = {}
    # update from persistent values
    self.vars.update(dict(
        (k, v['global']) for k, v in self.persistent_values.items() if 'global' in v))
    if 'stage' not in self.vars:
      self.vars['stage'] = self.variables_metainf['stage']['default']
    # update from stage specific value
    self.vars.update(dict((k, v[self.vars['stage']])
                          for k, v in self.persistent_values.items() if self.vars['stage'] in v))

  def save_persistent(self):
    persistent_values_path = f'{self.vars["root_dir"]}/.hive/persistents.yml'
    with open(persistent_values_path, 'w') as envf:
      yaml.dump(self.persistent_values, envf, default_flow_style=False)

  def set_persistent(self, name, value):
    self.initialize()
    if name not in self.variables_metainf:
      raise Error(f'unknown variable {name}')
    metainf = self.variables_metainf[name]
    if ('persistent_scope' in metainf) and metainf['persistent_scope'] == 'none':
      raise Error(f'variable {name} can not be saved persistently')
    persistent_scope = metainf['persistent_scope'] if 'persistent_scope' in metainf else 'global'
    key = self.vars['stage'] if persistent_scope == 'stage' else 'global'
    if name not in self.persistent_values:
      self.persistent_values[name] = {}
    self.persistent_values[name][key] = value
    return key

  def load_defaults(self):
    vars_defaults = [(k, v['default'])
                     for k, v in self.variables_metainf.items() if 'default' in v]
    dirty = True
    while (dirty):
      dirty = False
      for k, v in vars_defaults:
        new_value = v
        try:
          if type(v) == str:
            new_value = v.format(**self.vars)
        except Exception:
          pass
        else:
          if k not in self.vars or (k in self.overwritables and self.vars[k] != new_value):
            self.vars[k] = new_value
            if k not in self.overwritables:
              self.overwritables.append(k)
            dirty = True

  def initialize(self):
    path = f'{self.vars["root_dir"]}/.hive'
    if not os.path.exists(path):
      os.mkdir(path)
      return True
    return False

  def get_cast(self, name):
    if name not in self.variables_metainf:
      raise Error(f'unknown variable {name}')
    metainf = self.variables_metainf[name]
    if 'type' in metainf and metainf['type'] == 'boolean':
      return bool_cast
    if 'type' in metainf and metainf['type'] == 'enum':
      return lambda x: enum_cast(x, metainf['options'])
    if 'type' in metainf and metainf['type'] == 'integer':
      return int_cast
    if 'type' in metainf and metainf['type'] == 'directory':
      return directory_cast
    return str

  @staticmethod
  def add_argument(parser, name, metainf, mutually_exclusive_group_map, help_format_dict):
    long_option = f'--{name.replace("-","_")}'
    kwargs = {'help': metainf['description'].format(**help_format_dict)}
    if 'type' in metainf and metainf['type'] == 'boolean':
      kwargs['action'] = 'store_true'
    if 'type' in metainf and metainf['type'] == 'enum':
      kwargs['choices'] = metainf['options']
    if 'type' in metainf and metainf['type'] == 'integer':
      kwargs['type'] = int_cast
    if 'type' in metainf and metainf['type'] == 'directory':
      kwargs['type'] = directory_cast
    target = parser
    if 'command_line_mutually_exclusive_group' in metainf:
      group_name = metainf['command_line_mutually_exclusive_group']
      if group_name not in mutually_exclusive_group_map:
        mutually_exclusive_group_map[group_name] = parser.add_mutually_exclusive_group()
      target = mutually_exclusive_group_map[group_name]
    target.add_argument(metainf['command_line_option'], long_option, **kwargs)

  def get_parser(self, subcommand_handlers):
    parser = argparse.ArgumentParser(
        description='support tool to build docker site')
    mutually_exclusive_group_map = {}
    for metainf in [(k, v) for k, v in self.variables_metainf.items()
                    if 'command_line_option' in v and (('command_line_option_level' not in v) or v['command_line_option_level'] == 'global')]:
      hiveContext.add_argument(
          parser, metainf[0], metainf[1], mutually_exclusive_group_map, {})
    parser.set_defaults(root_dir=os.getcwd())
    subparsers = parser.add_subparsers(title='subcommands')
    for handler in subcommand_handlers:
      handler.setup_parser(subparsers, self.variables_metainf)
    return parser

  def load_command_line_options(self):
    self.vars.update(dict((k, getattr(self.args, k)) for k, v in self.variables_metainf.items()
                          if k != 'root_dir' and 'command_line_option' in v and hasattr(self.args, k) and getattr(self.args, k)))

  def do_subcommand(self):
    self.args.handler.do(self)

  def init_logger(self):
    self.logger = getLogger('hive')
    self.standard_handler = StreamHandler()
    self.logger.addHandler(self.standard_handler)
    self.logger.propagate = False
    self.standard_handler.setLevel(INFO)
    self.logger.setLevel(INFO)

  def reset_logger(self):
    if self.args.verbose:
      self.standard_handler.setLevel(DEBUG)
      self.logger.setLevel(DEBUG)


def sigchld_handler(sig, frame):
  raise InterruptedError()


def get_popen_lines(proc, master_fd, slave_fd):
  o = b''
  while proc.poll() is None:
    r = []
    w = []
    e = []
    try:
      signal.signal(signal.SIGCHLD, sigchld_handler)
      r, w, e = select.select([sys.stdin, master_fd], [], [])
    except InterruptedError:
      pass
    finally:
      signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    if sys.stdin in r:
      d = os.read(sys.stdin.fileno(), 40960)
      if d.find(b'\x03') >= 0:
        # ^C is pressed, so send_signal
        proc.send_signal(signal.SIGINT)
        raise Error('Keyboard Interrupt')
      os.write(master_fd, d)
    elif master_fd in r:
      o += os.read(master_fd, 40960)
      while o.find(b'\n') > 0:
        bline = o[:o.find(b'\n') + 1]
        o = o[o.find(b'\n') + 1:]
        os.write(sys.stdout.fileno(), bline)
        yield bline.decode('utf-8')
  if len(o) > 0:
    yield o.decode('utf-8')


RECAP_PATTERN = re.compile(
    r'[^ :]*[ :]*ok=(\d*)\s*changed=(\d*)\s*unreachable=(\d*)\s*failed=(\d*)\s*skipped=(\d*)\s*rescued=(\d*)\s*ignored=(\d*)\s*')
ANSI_ESCAPE = re.compile(r'\x1b[^m]*m')


def run_and_check_ansible_playbook(args):
  # save original tty setting then set it to raw mode
  old_tty = termios.tcgetattr(sys.stdin)
  tty.setraw(sys.stdin.fileno())

  # open pseudo-terminal to interact with subprocess
  master_fd, slave_fd = pty.openpty()
  try:
    proc = subprocess.Popen(args, stdin=slave_fd,
                            stdout=slave_fd,
                            stderr=slave_fd,
                            start_new_session=True,
                            universal_newlines=True)
    wait_recap = True
    error_count = 0
    for line in get_popen_lines(proc, master_fd, slave_fd):
      line = ANSI_ESCAPE.sub('', line)
      if wait_recap:
        if line.startswith('PLAY RECAP'):
          wait_recap = False
      else:
        m = RECAP_PATTERN.match(line)
        if m:
          error_count += int(m.group(3)) + int(m.group(4))
    if proc.returncode != 0:
      raise Error(f'ansible-playbook command failed: exit code = {proc.returncode}')
    if error_count > 0:
      raise Error(f'{error_count} tasks failed or unreachable')
  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


HOST_DEF_PATTERN = re.compile('^Host *(.*)$')


class ansbileCommandBase(commandHandlerBase):
  def get_playbook_path(self, vars):
    return f'{vars["playbooks_dir"]}/{self.name}.yml'

  def collect_ansible_vars(self, vars, variables_metainf):
    # override when phase sapecific ansible variale
    ansible_vars = dict((v['name_in_ansible'], vars[k])
                        for k, v in variables_metainf.items() if k in vars and 'name_in_ansible' in v)
    # ansible_vars['hive_temp_dir'] = f'{vars["root_dir"]}/{vars["stage"]}/.wk_{self.name}'
    return ansible_vars

  def collect_ansible_cfg_vars(self, vars, variables_metainf):
    # override when phase sapecific ansible variale
    ansible_cfg_vars = [dict(name=v['name_in_ansible_cfg'], value=vars[k], section=v['section_in_ansible_cfg'] if 'section_in_ansible_cfg' in v else 'defaults')
                        for k, v in variables_metainf.items() if k in vars and 'name_in_ansible_cfg' in v]
    return ansible_cfg_vars

  def collect_environment_vars(self, vars, variables_metainf, ansible_cfg_file_path):
    # override when phase sapecific ansible variale
    environment_vars = dict((v['name_in_environment'], vars[k])
                            for k, v in variables_metainf.items() if k in vars and 'name_in_environment' in v)
    environment_vars['ANSIBLE_CONFIG'] = ansible_cfg_file_path
    return environment_vars

  def build_context(self, context):
    context.load_defaults()
    context_dir = context.vars["context_dir"]
    temp_dir = context.vars["temp_dir"]
    os.makedirs(context_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    ansible_vars = self.collect_ansible_vars(
        context.vars, context.variables_metainf)
    self.vars_file_path = f'{temp_dir}/vars.yml'
    context.logger.debug(f'ansible extra variables: {ansible_vars}')
    with open(self.vars_file_path, 'w') as varsf:
      yaml.dump(ansible_vars, varsf, default_flow_style=False)
      ansible_cfg_vars = self.collect_ansible_cfg_vars(
          context.vars, context.variables_metainf)
      context.logger.debug(f'ansible cfg setting {ansible_cfg_vars}')
      # default interpolation cause error by % char, which is used by ssh_args
      config = configparser.ConfigParser(
          interpolation=configparser.ExtendedInterpolation())
      for var in ansible_cfg_vars:
        if not config.has_section(var['section']):
          config.add_section(var['section'])
        config.set(var['section'], var['name'], str(var['value']))
      ansible_cfg_file_path = f'{temp_dir}/ansible.cfg'
      with open(ansible_cfg_file_path, 'w') as cfg_varsf:
        config.write(cfg_varsf)
      environment_vars = self.collect_environment_vars(
          context.vars, context.variables_metainf, ansible_cfg_file_path)
      for k, v in environment_vars.items():
        os.environ[k] = v
      context.logger.debug(f'environment variables: {os.environ}')

  def setup_parser(self, subparsers, variables_metainf):
    super().setup_parser(subparsers, variables_metainf)
    mutually_exclusive_group_map = {}
    for variable in [(k, v) for k, v in variables_metainf.items() if 'command_line_option' in v and
                     ('command_line_option_level' in v and v['command_line_option_level'] == 'phase') and
                     self.name in v['command_line_option_available']]:
      hiveContext.add_argument(self.subparser, variable[0], variable[1], mutually_exclusive_group_map, {
                               'subject_name': self.subject_name})


class phaseBase(ansbileCommandBase):
  def do(self, context):
    context.vars['phase'] = self.name
    self.build_context(context)
    self.do_one(context)

  def get_limit_targets(self, context):
    return context.vars["stage"]

  def do_one(self, context):
    context.logger.info(f'=== PHASE {self.name} START at {time.strftime("%Y-%m-%d %H:%M:%S %z")} ===')
    args = ['ansible-playbook', '--limit', self.get_limit_targets(context)]
    if 'verbose' in context.vars and context.vars['verbose']:
      args.append('-vvv')
    if 'check_mode' in context.vars and context.vars['check_mode']:
      args.append('-C')
    args += ['--extra-vars', f'@{self.vars_file_path}']
    args.append(self.get_playbook_path(context.vars))
    context.logger.debug(f'commnad={args}')
    run_and_check_ansible_playbook(args)
    context.set_persistent('start_phase', self.name)
    if not context.vars.get('destroy'):
      next_idx = PHASE_LIST.index(self) + 1
      if next_idx < len(PHASE_LIST):
        context.set_persistent('start_phase', PHASE_NAME_LIST[next_idx])
    context.save_persistent()
    context.logger.info(f'=== PHASE {self.name} END at {time.strftime("%Y-%m-%d %H:%M:%S %z")} ===')


class buildInfra(phaseBase):
  def __init__(self):
    super().__init__('build-infra', 'build infrastructure, setup networks, global ip, firewall')
    self.subject_name = 'vpc/subnet/host'


class setupHosts(phaseBase):
  def __init__(self):
    super().__init__('setup-hosts',
                     'setup hosts, install software, configure services, configure cluster')
    self.subject_name = 'host'

  def get_limit_targets(self, context):
    if 'limit_target' in context.vars:
      return ':'.join(context.vars['limit_target'].split(',')) + ':&' + context.vars["stage"]
    return context.vars["stage"]


class phaseWithDockerSocket(phaseBase):

  def do_one(self, context):
    ssh_config_path = context.vars['context_dir'] + '/ssh_config'
    grep_proc = subprocess.run(['grep', '^Host ', ssh_config_path], stdout=subprocess.PIPE)
    if grep_proc.returncode == 1:
      raise Error(f'no Host entry in {ssh_config_path}')
    if grep_proc.returncode != 0:
      raise Error(f'fail to read ssh_config {ssh_config_path} error, you may never done build-infra: {grep_proc.stderr}')
    ssh_tunnel_procs = []
    for host_name in map(lambda x: x.decode(encoding='utf-8').split(' ')[1], grep_proc.stdout.splitlines()):
      socket_path = f'{context.vars["temp_dir"]}/docker.sock@{host_name}'
      if pathlib.Path(socket_path).is_socket():
        raise Error(f'fail to create socket {socket_path}, another hive process may doing build-image' +
                    ' or the file has been left because previus hive process aborted suddenly')
      args = ['ssh', '-N', '-F', ssh_config_path, '-L', socket_path + ':/var/run/docker.sock', host_name]
      ssh_tunnel_procs.append((socket_path, subprocess.Popen(args)))
    try:
      super().do_one(context)
    finally:
      for socket_path, ssh_tunnel_proc in ssh_tunnel_procs:
        ssh_tunnel_proc.send_signal(signal.SIGTERM)
        while ssh_tunnel_proc.poll() is None:
          try:
            ssh_tunnel_proc.wait(timeout=1)
          except subprocess.TimeoutExpired:
            pass
        os.remove(socket_path)


class buildImages(phaseWithDockerSocket):
  def __init__(self):
    super().__init__('build-images', 'build container images')
    self.subject_name = 'container'

  def get_limit_targets(self, context):
    if 'limit_target' in context.vars:
      return ':'.join(map(lambda x: 'image_' + x, context.vars['limit_target'].split(','))) + ':repository:&' + context.vars["stage"]
    return context.vars["stage"]


class buildVolumes(phaseBase):
  def __init__(self):
    super().__init__('build-volumes', 'build volumes on hives')
    self.subject_name = 'volume'


class buildNetworks(phaseBase):
  def __init__(self):
    super().__init__('build-networks', 'build networks for swarm')
    self.subject_name = 'ingress network'


class deployServices(phaseBase):
  def __init__(self):
    super().__init__('deploy-services', 'deploy services')
    self.subject_name = 'service'


class initializeServices(phaseWithDockerSocket):
  def __init__(self):
    super().__init__('initialize-services', 'initialize services')
    self.subject_name = 'service'

  def get_playbook_path(self, vars):
    return f'{vars["root_dir"]}/{self.name}.yml'


PHASE_LIST = [buildInfra(), setupHosts(), buildImages(),
              buildVolumes(), buildNetworks(), deployServices(), initializeServices()]
PHASE_NAME_LIST = list(map(lambda x: x.name, PHASE_LIST))


class allPhase(phaseBase):
  def __init__(self):
    super().__init__('all', 'do all phase')
    self.subject_name = 'all'

  def do(self, context):
    start_phase_idx = PHASE_NAME_LIST.index(context.vars['start_phase'])
    last_idx = len(PHASE_LIST)
    for idx in range(start_phase_idx, last_idx):
      PHASE_LIST[idx].build_context(context)
      PHASE_LIST[idx].do_one(context)


class inventoryList(ansbileCommandBase):
  def __init__(self):
    super().__init__('inventory', 'list ansible inventory')

  def do(self, context):
    self.build_context(context)
    args = ['ansible-inventory', '--playbook-dir=' +
            context.vars['playbooks_dir'], '--list']
    subprocess.run(args)


class execSsh(ansbileCommandBase):
  def __init__(self):
    super().__init__('ssh', 'ssh to hive server')
    self.subject_name = 'host'

  def do(self, context):
    self.build_context(context)
    ssh_config_path = context.vars['context_dir'] + '/ssh_config'
    grep_proc = subprocess.run(['grep', '^Host ', ssh_config_path], stdout=subprocess.PIPE)
    if grep_proc.returncode == 1:
      raise Error(f'no Host entry in {ssh_config_path}')
    if grep_proc.returncode != 0:
      raise Error(f'fail to read ssh_config {ssh_config_path} error, you may never done build-infra: {grep_proc.stderr}')
    hosts = list(map(lambda x: x.decode(encoding='utf-8').split(' ')[1], grep_proc.stdout.splitlines()))
    ssh_host = context.vars.get('ssh_host')
    if ssh_host is None:
      ssh_host = hosts[len(hosts) - 1]
    elif ssh_host not in hosts:
      raise Error(f'host {ssh_host} is not found in {ssh_config_path}')
    args = ['/usr/bin/ssh', '-F', ssh_config_path]
    if context.vars['foward_zabbix']:
      args += ['-L', f'localhost:{context.vars["foward_zabbix_port"]}:{ssh_host}:10052']
    if context.vars.get('port_forwarding'):
      args += ['-L', context.vars['port_forwarding']]
    args += [ssh_host]
    context.logger.debug(f'commnad={args}')
    try:
      ssh_proc = subprocess.Popen(args)
      ssh_proc.wait()
    except KeyboardInterrupt:
      ssh_proc.send_signal(signal.SIGTERM)
      ssh_proc.wait()


SUBCOMMANDS = PHASE_LIST + [allPhase(), inventoryList(), initializeEnvironment(), setPersistent(), execSsh()]


def get_parser():
  context = hiveContext()
  context.load_variables_metainf()
  return context.get_parser(SUBCOMMANDS)


def main():
  context = hiveContext()
  try:
    context.setup(SUBCOMMANDS)
    context.do_subcommand()
  except Error as e:
    context.logger.error(f'HIVE ERROR: {str(e)}')
    sys.exit(1)
  except Exception:
    tpe, v, tb = sys.exc_info()
    backtrace.hook(reverse=True, strip_path=True, tb=tb, tpe=tpe, value=v)
    sys.exit(1)


if __name__ == '__main__':
  main()
