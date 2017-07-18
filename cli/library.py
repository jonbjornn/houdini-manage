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
import json
import os
import re
import sys
import {main} from './index'

# http://www.sidefx.com/docs/houdini/ref/env
LIBRARY_ENVIRONMENT_EXTENSIONS = [
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
@click.option('--remove', help='Remove a Houdini library.')
@click.option('--version-of', help='Print the version of a Houdini library.')
@click.option('--list', is_flag=True, help='List all installed Houdini libraries.')
@click.option('--dry', is_flag=True, help='Do not save changes to the '
  'environment file, but print the new content instead. Only with --install '
  'and --remove.')
@click.pass_context
def library(ctx, hou, install, remove, version_of, list, dry):
  """
  Install, manage and remove external Houdini libraries.

  HOU

      The name of a installed Houdini version or a path to a Houdini
      environment file. The default value can be changed in the user's
      `~/.houdini-manage.ini` configuration file. The default value is
      "houdini16.0".

  --install LIBRARY_PATH

      The path to the Houdini library to install. This directory must contain
      a valid `houdini-library.json` file.

  --remove LIBRARY_NAME

      The name of the Houdini library to uninstall.

  --version-of LIBRARY_NAME

      Print the library name of the specified Houdini library.

  --list

      List all installed Houdini libraries.
  """

  # Only one operation valid per invokation.
  count = sum(map(bool, [install, remove, version_of, list]))
  if count == 0:
    print(ctx.get_usage())
    return
  if count != 1:
    ctx.fail('no or multiple operations specified')

  # Determine the Houdini environment file to work on.
  # TODO: Parse user configuration file.
  hou = hou or 'houdini16.0'
  if not '/' in hou and not os.sep in hou:
    hou = os.path.expanduser('~/Documents/' + hou + '/houdini.env')
  hou = os.path.normpath(hou)
  if not os.path.isfile(hou):
    ctx.fail('file does not exist: {}'.format(hou))

  if install:
    # Open the librarie's configuration file.
    config_file = os.path.join(install, 'houdini-library.json')
    if not os.path.isfile(config_file):
      ctx.fail('missing library configuration file: {}'.format(config_file))
    with open(config_file) as fp:
      config = json.load(fp)

    # TODO: Proper parsing of the environment file.
    # Find the section of the configuration matching this library.
    with open(hou) as fp:
      env_content = fp.read()
    exbegin = re.compile(
        r'^##\s*BEGIN\s+LIBRARY\s*\(' + re.escape(config['libraryName'])
        + r'\)\s*', re.M)
    exend = re.compile(r'^##\s*END\s+LIBRARY\s*', re.M)
    mbegin = exbegin.search(env_content, 0)
    mend = exend.search(env_content, mbegin.end()) if mbegin else None
    if mbegin and not mend:
      ctx.fail('missing "end library" for opening definition of "{}"'
        .format(config['libraryName']))

    if mbegin:
      print('removing old library section "{}"'.format(config['libraryName']), file=sys.stderr)
      env_content = env_content[:mbegin.start()] + env_content[mend.end():]
    print('installing library section "{}"'.format(config['libraryName']), file=sys.stderr)

    # TODO: Add DEFAULTS section to the environment file that maintains
    # the default values of Houdini's search paths.
    # - $HFS/houdini/{dir}
    # - $HOUDINI_USER_PREF_DIR/{dir}

    directory = os.path.normpath(os.path.abspath(install))
    lines = []
    lines.append('HLIBPATH_{}="{}"'.format(config['libraryName'], directory))
    lines.append('HLIBVERSION_{}="{}"'.format(config['libraryName'], config['libraryVersion']))
    lines.append('HLIB_INSTALLED="$HLIB_INSTALLED{}{}"'.format(os.path.pathsep, config['libraryName']))
    for data in LIBRARY_ENVIRONMENT_EXTENSIONS:
      if not data['dir']: continue
      libdir = os.path.join(directory, data['dir'])
      if not os.path.isdir(libdir): continue
      lines.append('{0}="${0}{1}{2}"'.format(data['var'], os.path.pathsep, libdir))
    lines.extend(config.get('environment', []))

    env_content += '## BEGIN LIBRARY ({})\n'.format(config['libraryName'])
    env_content += '\n'.join(lines)
    env_content += '\n## END LIBRARY\n'

    if dry:
      print(env_content)
    else:
      with open(hou, 'w') as fp:
        fp.write(env_content)
      print('saved "{}"'.format(hou), file=sys.stderr)

  if remove:
    pass # TODO

  if version_of:
    pass # TODO

  if list:
    pass # TODO
