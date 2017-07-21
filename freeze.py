frieza = require('@nodepy/frieza')
frieza.executable(
  entry_point = 'cli/index',
  targetName = 'houdini-manage.exe',
  base = 'Win32GUI'
)
frieza.include('click', 'configparser', 'PyQt5', 'sip')
frieza.exclude('notebook', 'jupyter')
