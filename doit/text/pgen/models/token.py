#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/models/token.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-10 19:58:42 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Token definition.\
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

from doit.support.cmd.runtime import UserType

class Token(UserType):
    """
    """
    __slots__ = [ 'ttype', 'data' ]

    def __init__(self, ttype, *data):
        """
        """

        UserType.__init__(self)
        self.ttype = ttype
        self.data = data
    #-def

    def __repr__(self):
        """
        """

        return "Token(ttype = %r, data = %r)" % (self.ttype, self.data)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, type(self)) \
        and self.ttype == other.ttype \
        and self.data == other.data
    #-def
#-class
