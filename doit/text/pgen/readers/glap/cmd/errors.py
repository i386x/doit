#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/cmd/errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-15 13:19:12 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor errors.\
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

ERROR_COMMAND_PROCESSOR = DoItError.alloc_codes(1)
ERROR_COMMAND = DoItError.alloc_codes(1)

class CommandProcessorError(DoItError):
    """
    """
    __slots__ = [ 'traceback' ]

    def __init__(self, tb, emsg):
        """
        """

        DoItError.__init__(self, ERROR_COMMAND_PROCESSOR, emsg)
        self.traceback = tb
    #-def

    def __str__(self):
        """
        """

        if self.traceback:
            return "%s %s" % (self.traceback, DoItError.__str__(self))
        return DoItError.__str__(self)
    #-def
#-class

class CommandError(DoItError):
    """
    """
    __slots__ = [ 'ecls', 'emsg' ]

    def __init__(self, ecls, emsg):
        """
        """

        DoItError.__init__(self, ERROR_COMMAND, "%s: %s" % (ecls, emsg))
        self.ecls = ecls
        self.emsg = emsg
    #-def

    def __repr__(self):
        """
        """

        return "%s(\"%s\")" % (self.ecls, self.emsg)
    #-def
#-class
