#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/app/errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-09-03 14:38:52 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Application errors.\
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

from doit.support.errors import DoItError

ERROR_APPLICATION = DoItError.alloc_codes(1)

class ApplicationError(DoItError):
    """
    """
    __slots__ = []

    def __init__(self, emsg):
        """
        """

        DoItError.__init__(self, ERROR_APPLICATION, emsg)
    #-def
#-class

class ApplicationExit(ApplicationError):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        ApplicationError.__init__(self,
            "I am a signal rather then error. Please, handle me properly"
        )
    #-def
#-class
