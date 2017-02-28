#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/cache/__init__.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-05 13:27:09 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Parser generators maintainer cache.\
"""

__license__ = """\
Copyright (c) 2014 - 2017 Jiří Kučera.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.\
"""

import sys
import os
import importlib

from doit.support.app.io import read_all, write_items
from doit.text.pgen.builders.builder import Builder

CACHE_DIR = os.path.dirname(os.path.realpath(__file__))
COMMANDS_CACHE = os.path.join(CACHE_DIR, 'commands')
COMMANDS_DIR = os.path.dirname(os.path.realpath(
    sys.modules[Builder.__module__].__file__
))
COMMANDS_BASE = '.'.join(Builder.__module__.split('.')[:-1])

del Builder
del sys

def get_commands(dont_import = False):
    """
    """

    cache_raw_data = read_all(COMMANDS_CACHE)
    if cache_raw_data is None:
        return None
    cache_data = cache_raw_data.split('\n')
    cache_data = [x.strip() for x in cache_data]
    cache_data = [x for x in cache_data if x]
    cache_data = [x.split(' ') for x in cache_data]
    cache_data = [[x for x in y if x] for y in cache_data]
    if not cache_data:
        return []
    length_set = dict([(len(x), 1) for x in cache_data])
    if len(length_set) != 1 or 2 not in length_set:
        return None
    cache_data = [(x[0].strip(), x[1].strip()) for x in cache_data]
    if dont_import:
        return cache_data
    importlib.invalidate_caches()
    commands = []
    try:
        for x in cache_data:
            m = importlib.import_module("%s.%s" % x)
            if not m or not hasattr(m, 'get_command_class'):
                return None
            commands.append(m.get_command_class())
    except ImportError:
        return None
    return commands
#-def

def add_command(name):
    """
    """

    command_file = os.path.join(COMMANDS_DIR, "%s.py" % name)
    if not os.path.exists(command_file) or not os.path.isfile(command_file):
        return False, "File <%s> not found" % command_file
    cache_data = get_commands(dont_import = True)
    if cache_data is None:
        return False, "Can't read from cache <%s>" % COMMANDS_CACHE
    if name in [x[1] for x in cache_data]:
        return False, "Command/Builder `%s` has been already added" % name
    cache_data.append((COMMANDS_BASE, name))
    if not write_items(COMMANDS_CACHE, cache_data, (lambda x: "%s %s\n" % x)):
        return False, "Can't write to cache <%s>" % COMMANDS_CACHE
    return True, ""
#-def
