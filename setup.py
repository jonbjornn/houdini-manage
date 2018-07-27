
from setuptools import setup, find_packages

setup(
  name = 'houdini-manage',
  version = '1.0.0',
  author = 'Niklas Rosenstein',
  author_email = 'rosensteinniklas@gmail.com',
  license = 'MIT',
  packages = find_packages(),
  entry_points = dict(
    console_scripts = [
      'houdini-manage = houdini_manage.main:main'
    ]
  )
)
