#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/models/precedence.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-09-18 11:55:03 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Precedence graph and associated structures.\
"""

__license__ = """\
Copyright (c) 2014 - 2016 Jiří Kučera.

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

from doit.support.errors import doit_assert as _assert

from doit.support.cmd.runtime import UserType

class PrecedenceGraph(UserType):
    """
    """
    __slots__ = [ '__np', '__data', 'cache' ]

    def __init__(self, *spec):
        """
        """

        UserType.__init__(self)
        self.__np = spec[0] if spec and isinstance(spec[0], str) else "expr"
        # level -> [(opspec, action)]
        self.__data = {}
        self.cache = {}
        self.madd(*spec)
    #-def

    def add(self, level, opspec, action = None):
        """
        """

        if level not in self.__data:
            self.__data[level] = []
        self.__data[level].append((opspec, action))
    #-def

    def madd(self, *spec):
        """
        """

        for x in spec:
            if isinstance(x, tuple):
                if len(x) == 2:
                    self.add(x[0], x[1], None)
                elif len(x) == 3:
                    self.add(x[0], x[1], x[2])
                else:
                    _assert(False, "Invalid argument")
    #-def

    def name_prefix(self):
        """
        """

        return self.__np
    #-def

    def data(self):
        """
        """

        return self.__data
    #-def
#-class
