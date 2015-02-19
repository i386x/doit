#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-03-09 17:10:29 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! errors and exceptions.\
"""

__license__ = """\
Copyright (c) 2014 - 2015 Jiří Kučera.

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

PythonRuntimeError = RuntimeError
PythonIOError = IOError

def perror(msg):
    """perror(msg)

    Prints an error message to standard error output.
    """

    sys.stderr.write("%s\n" % msg)
#-def

class DoItError(Exception):
    """Basic DoIt! exception.
    """

    def __init__(self, emsg, ecode = 255):
        """DoItError(emsg[, ecode]) -> instance of DoItError

        Constructor. Create an exception object initialized with error message
        emsg and error code ecode (255 as default).
        """

        Exception.__init__(self, emsg, ecode)
        self.detail = emsg
        self.errcode = ecode
    #-def

    def __repr__(self):
        """__repr__() -> str

        Return the text representation of exception.
        """

        return self.__class__.__name__ + repr(self.args)
    #-def

    def __str__(self):
        """__str__() -> str

        Return message associated with exception to be printed.
        """

        return "%s [errcode = %d]: %s." % (
            self.__class__.__name__, self.errcode, self.detail
        )
    #-def
#-class

class RuntimeError(DoItError):
    """Raised when virtual machine is aborted abnormally.
    """

    def __init__(self, name, ip, emsg):
        """RuntimeError(name, ip, emsg) -> instance of RuntimeError

        Constructor.
        """

        DoItError.__init__(self,
            "VM aborted. Detail: %s [ip = %d]: %s." % (name, ip, emsg)
        )
    #-def
#-class

class IOError(DoItError):
    """Raised when DoIt! I/O operation fails.
    """

    def __init__(self, emsg):
        """IOError(emsg) -> instance of IOError

        Constructor.
        """

        DoItError.__init__(self, emsg)
    #-def
#-class
