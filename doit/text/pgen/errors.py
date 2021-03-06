#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2017-02-28 18:13:50 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Parser generator errors.\
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

from doit.support.errors import DoItError
from doit.support.app.errors import ApplicationError

ERROR_PARSING = DoItError.alloc_codes(2)
ERROR_PARSER  = ERROR_PARSING + 1

class ParsingError(DoItError):
    """
    """
    __slots__ = []

    def __init__(self, emsg):
        """
        """

        DoItError.__init__(self, ERROR_PARSING, emsg)
    #-def
#-class

class ParserError(DoItError):
    """
    """
    __slots__ = []

    def __init__(self, emsg):
        """
        """

        DoItError.__init__(self, ERROR_PARSER, emsg)
    #-def
#-class

class ParserGeneratorError(ApplicationError):
    """
    """
    __slots__ = []

    def __init__(self, emsg):
        """
        """

        ApplicationError.__init__(self, emsg)
    #-def
#-class
