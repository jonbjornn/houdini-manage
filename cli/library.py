# Copyright (C) 2017  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import click
import datetime
import json
import os
import re
import sys
import {main} from './index'
import {SectionEnvfile} from '../lib/envfile'
import hmConfig from '../lib/config'

# http://www.sidefx.com/docs/houdini/ref/env
# Currently not used, setting HOUDINI_PATH seems to be sufficient.
HOUDINI_PATH_ENVVARS = [
  {
    'var': 'HOUDINI_VOP_DEFINITIONS_PATH',
    'dir': 'vop'
  },
  {
    'var': 'HOUDINI_OTLSCAN_PATH',
    'dir': 'otls'
  },
  {
    'var': 'HOUDINI_SCRIPT_PATH',
    'dir': 'scripts'
  },
  {
    'var': 'HOUDINI_DESK_PATH',
    'dir': 'desktop'
  },
  {
    'var': 'HOUDINI_DSO_PATH',
    'dir': 'dso'
  },
  {
    'var': 'HOUDINI_GEOMETRY_PATH',
    'dir': 'geo'
  },
  {
    'var': 'HOUDINI_MACRO_PATH',
    'dir': None,  # TODO
  },
  {
    'var': 'HOUDINI_MENU_PATH',
    'dir': None  # TODO
  },
  {
    'var': 'HOUDINI_PYTHON_PANEL_PATH',
    'dir': 'python_panels'
  },
  {
    'var': 'HOUDINI_TEXTURE_PATH',
    'dir': 'pic'
  },
  {
    'var': 'HOUDINI_TOOLBAR_PATH',
    'dir': 'toolbar'
  },
  {
    'var': 'HOUDINI_RADIALMENU_PATH',
    'dir': 'radialmenu'
  },
  {
    'var': 'HOUDINI_VEX_PATH',
    'dir': 'vex'
  },
  {
    'var': 'HOUDINI_GLSL_PATH',
    'dir': 'glsl'
  },
  {
    'var': 'HOUDINI_OCL_PATH',
    'dir': 'ocl'
  },
]


@main.command()
@click.argument('hou', required=False)
@click.option('--install', help='Install the specified Houdini library.')
@click.option('--overwrite', is_flag=True, help='Overwrite a previous installation of the same library.')
@click.option('--remove', help='Remove a Houdini library.')
@click.option('--version-of', help='Print the version of a Houdini library.')
@click.option('--path-of', help='Print the path of a Houdini library.')
@click.option('--list', is_flag=True, help='List all installed Houdini libraries.')
@click.option('--dry', is_flag=True, help='Do not save changes to the '
  'environment file, but print the new content instead. Only with --install '
  'and --remove.')
@click.pass_context
def library(ctx, hou, install, overwrite, remove, version_of, path_of, list, dry):
  """
  Install or remove external Houdini libraries.
  """

  # Only one operation valid per invokation.
  count = sum(map(bool, [install, remove, version_of, path_of, list]))
  if count == 0:
    print(ctx.get_usage())
    return
  if count != 1:
    ctx.fail('no or multiple operations specified')

  # Determine the Houdini environment file to work on.
  # TODO: Parse user configuration file.
  hou = hou or hmConfig.get('houdinienv', 'houdini16.0')
  if not '/' in hou and not os.sep in hou:
    hou = os.path.expanduser('~/Documents/' + hou + '/houdini.env')
  hou = os.path.normpath(hou)
  if not os.path.isfile(hou):
    ctx.fail('file does not exist: {}'.format(hou))

  # Parse the environment file into its sections.
  with open(hou) as fp:
    env = SectionEnvfile.parse(fp)

  def save_env():
    with open(hou, 'w') as fp:
      env.render(fp)

  if list:
    for section in env.iter_named_sections():
      if section.name.startswith('library:'):
        libname = section.name[8:]
        dirname = section.extract_var('HLIBPATH_' + libname) or '???'
        version = section.extract_var('HLIBVERSION_' + libname) or '???'
        print('* {} v{} ({})'.format(libname, version, dirname))
    return

  if version_of or path_of:
    section = env.get_named_section('library:' + (version_of or path_of))
    if not section:
      print('library "{}" not installed'.format(version_of), file=sys.stderr)
      ctx.exit(1)
    var = 'HLIBVERSION_' if version_of else 'HLIBPATH_'
    print(section.extract_var(var + section.name[8:]) or '???')
    return

  if remove:
    try:
      env.remove_section('library:' + remove)
    except ValueError:
      print('library "{}" not installed'.format(remove))
      ctx.exit(1)
    else:
      print('library "{}" removed'.format(remove))
    if not dry:
      save_env()
    return

  if install:
    # Open the librarie's configuration file.
    config_file = os.path.join(install, 'houdini-library.json')
    if not os.path.isfile(config_file):
      ctx.fail('missing library configuration file: {}'.format(config_file))
    with open(config_file) as fp:
      config = json.load(fp)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    version = module.package.json['version']

    # Initialize the default section. It's purpose is to make sure that
    # Houdini's default paths do not get messed up.
    section = env.get_named_section('DEFAULT')
    if not section:
      section = env.add_named_section('DEFAULT', '', before=env.get_first_named_section())
    else:
      section.clear()
    section.add_comment('  Automatically generated by houdini-manage v{}'.format(version))
    section.add_comment('  Last update: {}'.format(now))
    #for info in HOUDINI_PATH_ENVVARS:
    #  # Houdini will use the default value of the variable when it sees
    #  # the ampersand.
    #  section.add_variable(info['var'], '&')
    section.add_variable('HOUDINI_PATH', '&')
    section.add_variable('PYTHONPATH', '&')

    # Create or update the section for this library.
    directory = os.path.normpath(os.path.abspath(install))
    section = env.get_named_section('library:' + config['libraryName'])
    if not section:
      previous = False
      section = env.add_named_section('library:' + config['libraryName'], '')
    else:
      previous = True
      if not overwrite:
        print('error: previous installation found. pass --overwrite to proceed')
        ctx.exit(1)

    if previous:
      print('note: overwriting previous installation')

    section.clear()
    section.add_comment('  Automatically generated by houdini-manage v{}'.format(version))
    section.add_comment('  Last update: {}'.format(now))
    #for info in HOUDINI_PATH_ENVVARS:
    #  if not info['dir']: continue
    #  vardir = os.path.join(directory, info['dir'])
    #  if not os.path.isdir(vardir): continue
    #  section.add_variable(info['var'], '$' + info['var'], vardir)
    section.add_variable('HOUDINI_PATH', '$HOUDINI_PATH', directory)
    if os.path.isdir(os.path.join(directory, 'python')):
      section.add_variable('PYTHONPATH', '$PYTHONPATH', os.path.join(directory, 'python'))
    section.add_variable('HLIBPATH_' + config['libraryName'], directory)
    section.add_variable('HLIBVERSION_' + config['libraryName'], config['libraryVersion'])
    if config.get('environment'):
      section.add_comment('Environment variables specified by the library:')
      for line in config['environment']:
        section.add_line(line)

    print('library "{}" installed'.format(config['libraryName']))

    if not dry:
      save_env()
