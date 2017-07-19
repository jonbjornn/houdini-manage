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
"""
Section parser for the Houdini environment file.
"""

import os
import re
import shlex

class Section(object):

  def render(self, fp):
    raise NotImplementedError


class PlainContentSection(Section):

  def __init__(self, content):
    self.content = content

  def __bool__(self):
    return bool(self.content)

  __nonzero__ = __bool__

  def render(self, fp):
    fp.write(self.content)

  def add_line(self, line):
    self.content += line


class NamedSection(Section):

  @staticmethod
  def parse(line, fp):
    match = re.match('^#+\s*BEGIN_SECTION\(([^\)]+)\)\s*$', line)
    if not match:
      return line, None
    name = match.group(1)
    lines = []
    for line in fp:
      match = re.match('^#+\s*END_SECTION\s*', line)
      if match:
        break
      lines.append(line)
    else:
      raise ValueError('missing END_SECTION for section "{}"'.format(name))
    return fp.readline(), NamedSection(name, ''.join(lines))

  def __init__(self, name, content=''):
    self.name = name
    self.content = content.rstrip()
    if content and not self.content.endswith('\n'):
      self.content += '\n'

  def clear(self):
    self.content = ''

  def is_library(self):
    return self.name.startswith('library:')

  def get_library_name(self):
    if self.is_library():
      return self.name[8:]
    return None

  def get_library_path(self):
    name = self.get_library_name()
    if name:
      return self.extract_var('HLIBPATH_' + name)
    return None

  def get_library_version(self):
    name = self.get_library_name()
    if name:
      return self.extract_var('HLIBVERSION_' + name)
    return None

  def add_comment(self, comment):
    lines = comment.split('\n')
    self.content += '\n'.join('# ' + line for line in lines) + '\n'

  def add_variable(self, variable, *values):
    value = os.path.pathsep.join(values)
    self.content += '{}="{}"\n'.format(variable, value.replace('"', '\\"'))

  def add_line(self, line):
    line = line.rstrip()
    if not line.endswith('\n'):
      line += '\n'
    self.content += line

  def extract_var(self, varname):
    for line in self.content.split('\n'):
      if line.startswith(varname + '='):
        return shlex.split(line[len(varname) + 1:])[0]
    return None

  def render(self, fp):
    fp.write('# BEGIN_SECTION({})\n'.format(self.name))
    fp.write(self.content)
    fp.write('# END_SECTION\n')


class SectionEnvfile(object):
  """
  Represents a Houini envfile in its sections separated by
  `# BEGIN_SECTION(NAME)` and `# END_SECTION` comments and allows modification
  of the sections.
  """

  @classmethod
  def parse(cls, fp):
    sections = []
    plain = PlainContentSection('')
    for line in fp:
      # Parse named sections until we can get no more.
      while True:
        line, section = NamedSection.parse(line, fp)
        if not section:
          break
        if plain: sections.append(plain)
        plain = PlainContentSection('')
        sections.append(section)
      plain.add_line(line)
    if plain: sections.append(plain)
    return cls(sections)

  def __init__(self, sections):
    self.sections = sections
    self.changed = False

  def render(self, fp):
    for section in self.sections:
      section.render(fp)
    self.changed = False

  def add_section(self, section, before=None, after=None):
    if before is not None:
      index = self.sections.index(before)
    elif after is not None:
      index = self.sections.index(after) + 1
    else:
      index = None
    if index is None:
      self.sections.append(section)
    else:
      self.sections.insert(index, section)
    self.changed = True

  def add_plain_content(self, content, before=None, after=None):
    section = PlainContentSection(content)
    self.add_section(section, before=before, after=after)
    return section

  def add_named_section(self, name, content, before=None, after=None):
    section = NamedSection(name, content)
    self.add_section(section, before=before, after=after)
    return section

  def get_named_section(self, name):
    for section in self.sections:
      if isinstance(section, NamedSection) and section.name == name:
        return section
    return None

  def get_library(self, name):
    return self.get_named_section('library:' + name)

  def get_first_named_section(self):
    return next(self.iter_named_sections(), None)

  def iter_named_sections(self):
    return (sec for sec in self.sections if isinstance(sec, NamedSection))

  def remove_section(self, name):
    section = self.get_named_section(name)
    if section is None:
      raise ValueError('no such section: "{}"'.format(name))
    self.sections.remove(section)
    self.changed = True
