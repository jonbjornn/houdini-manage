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

from six.moves import configparser
import os

filename = os.path.expanduser('~/.houdini-manage.ini')
if os.path.isfile(filename):
  parser = configparser.SafeConfigParser()
  parser.read([filename])


class ConfigWrapper(object):

  def __init__(self, parser, section, filename):
    self.parser = parser
    if not parser.has_section(section):
      parser.add_section(section)
    self.section = section
    self.filename = filename

  def __getitem__(self, key):
    try:
      return self.parser.get(self.section, key)
    except configparser.NoOptionError:
      raise KeyError(key) from None

  def __setitem__(self, key, value):
    self.parser.set(self.section, key, str(value))

  def get(self, key, default=None):
    try:
      return self[key]
    except KeyError:
      return default

  def save(self):
    with open(self.filename, 'w') as fp:
      self.parser.write(fp)


exports = ConfigWrapper(parser, 'houdini-manage', filename)
