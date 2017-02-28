#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/builders/builder.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-10 21:13:02 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Parser generator output builder interface.\
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
import re
import importlib

from doit.support.app.application import Application

class Builder(Application):
    """
    """
    PY_DOTTED_NAME = re.compile(r"^[.a-zA-Z0-9_]+$")
    __slots__ = []

    def __init__(self, owner = None, **kwargs):
        """
        """

        Application.__init__(self, owner, **kwargs)
    #-def

    @classmethod
    def name(cls):
        """
        """

        return cls.__name__.lower()
    #-def

    def load_module(self, path, name, attr = None):
        """
        """

        if re.match(self.PY_DOTTED_NAME, path):
            return self.__load_module("%s.%s" % (path, name), attr)
        if not path:
            path = self.get_cwd()
        path = os.path.realpath(path)
        if path not in sys.path:
            sys.path.insert(0, path)
        return self.__load_module(name, attr)
    #-def

    def __load_module(self, name, attr = None):
        """
        """

        importlib.invalidate_caches()
        try:
            m = importlib.import_module(name)
            if not m or (attr and not hasattr(m, attr)):
                return None
            return m
        except ImportError:
            return None
    #-def
#-class
