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
import os
import sys
import {main} from './index'
import {SectionEnvfile} from '../lib/envfile'
import _library from '../lib/library'

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
  hou = _library.get_houdini_environment_path(hou)
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
      if section.is_library():
        print('* {} v{} ({})'.format(
          section.get_library_name(),
          section.get_library_version() or '???',
          section.get_library_path() or '???'
        ))
    return

  if version_of or path_of:
    section = env.get_library(version_of or path_of)
    if not section:
      print('library "{}" not installed'.format(version_of or path_of), file=sys.stderr)
      ctx.exit(1)
    value = section.get_library_version() if version_of else section.get_library_path()
    print(value or '???')
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
    _library.install_library()
    print('library "{}" installed'.format(config['libraryName']))
    if not dry:
      save_env()
    return
