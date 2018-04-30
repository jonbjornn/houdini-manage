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

import argparse
import os
import sys
from . import __version__, library as _library
from .envfile import SectionEnvfile


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


parser = argparse.ArgumentParser(prog='houdini-manage')
parser.add_argument('hou', nargs='?', help='The name of the Houdini version.')
parser.add_argument('--version', action='version', version=__version__)
parser.add_argument('--gui', action='store_true', help='Runs the GUI.')
parser.add_argument('-i', '--install', metavar='LIBRARY', help='Install the specified Houdini library.')
parser.add_argument('--remove', metavar='LIBRARY', help='Remove a Houdini library.')
parser.add_argument('--version-of', metavar='LIBRARY', help='Print the version of a Houdini library.')
parser.add_argument('--path-of', metavar='LIBRARY', help='Print the path of a Houdini library.')
parser.add_argument('-l', '--list', action='store_true', help='List all installed Houdini libraries.')
parser.add_argument('--dry', action='store_true', help='Do not save changes to the environment file, but print the new content instead. Only with --install and --remove.')

error = lambda *a: print(*a, file=sys.stderr)


def _main(argv=None):
  args = parser.parse_args(argv)

  # Only one operation valid per invokation.
  count = sum(map(bool, [args.gui, args.install, args.remove, args.version_of, args.path_of, args.list]))
  if count == 0:
    parser.print_usage()
    return
  if count != 1:
    error('fatal: no or multiple operations specified')
    return 1

  if args.gui:
    from .gui import QApplication, Window
    app = QApplication([])
    wnd = Window()
    wnd.show()
    app.exec_()
    return 0

  # Determine the Houdini environment file to work on.
  # TODO: Parse user configuration file.
  hou = _library.get_houdini_environment_path(args.hou)
  if not os.path.isfile(hou):
    error('fatal: file does not exist: {}'.format(hou))
    return 1

  # Parse the environment file into its sections.
  with open(hou) as fp:
    env = SectionEnvfile.parse(fp)

  def save_env():
    with open(hou, 'w') as fp:
      env.render(fp)

  if args.list:
    for section in env.iter_named_sections():
      if section.is_library():
        print('* {} v{} ({})'.format(
          section.get_library_name(),
          section.get_library_version() or '???',
          section.get_library_path() or '???'
        ))
    return

  if args.version_of or args.path_of:
    section = env.get_library(args.version_of or args.path_of)
    if not section:
      error('fatal: library "{}" not installed'.format(args.version_of or args.path_of))
      return 1
    value = section.get_library_version() if args.version_of else section.get_library_path()
    print(value or '???')
    return

  if args.remove:
    try:
      env.remove_section('library:' + args.remove)
    except ValueError:
      print('library "{}" not installed'.format(args.remove))
      return 1
    else:
      print('library "{}" removed'.format(args.remove))
    if not args.dry:
      save_env()
    return

  if args.install:
    _library.install_library()
    print('library "{}" installed'.format(config['libraryName']))
    if not args.dry:
      save_env()
    return
  return library(args)


def main(argv=None):
  sys.exit(_main(argv))


if __name__ == '__main__':
  main()
