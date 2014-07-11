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
Copyright (c) 2014 Jiří Kučera.

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

__errors = {}

def register_error(errid):
    """register_error(errid) -> function

    Return a function which registers an error as pair (errid, errcls). Used
    as class decorator. Example:

    >>> @register_error(Exceptions.ParseError)
    ... class ParseError(DoItError):
    ...    ...
    """

    def __f(errcls):
        __errors[errid] = errcls
        return errcls
    return __f
#-def

def perror(msg):
    """perror(msg)

    Prints an error message to standard error output.
    """

    sys.stderr.write("%s\n" % msg)
#-def

def error(ctx, errid, what):
    """error(ctx, errid, what)

    Stops DoIt! execution with error class ERR_EXCEPTION and error subclass
    errid. Error can be handled and processed.
    """

    ctx.set_error(ErrorType.ERR_EXCEPTION, errid, what)
    raise __errors[errid](what)
#-def

def internal_error(ctx, msg):
    """internal_error(ctx, msg)

    Raise InternalError exception with msg.
    """

    error(ctx, Exceptions.InternalError, msg)
#-def

def check(ctx, cond, msg):
    """check(ctx, cond, msg)

    If cond is False, raise CheckError exception with msg.
    """

    if not cond:
        error(ctx, Exceptions.CheckError, msg)
#-def

def parse_error(ctx, pos, what):
    """parse_error(ctx, pos, what)

    Specialization of error for parsers.
    """

    error(ctx, Exceptions.ParseError, "In %s at line %d, column %d: %s" % (
        pos[0], pos[1], pos[2], what
    ))
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

@register_error(Exceptions.InternalError)
class InternalError(DoItError):
    """Raising this exception means that there is a bug inside DoIt!
       interpreter.
    """

    def __init__(self, msg):
        """InternalError(msg) -> instance of DoItError

        Constructor.
        """

        DoItError.__init__(self, msg)
    #-def
#-class

@register_error(Exceptions.CheckError)
class CheckError(DoItError):
    """Denotes inconsistencies or bad values of command arguments.
    """

    def __init__(self, msg):
        """CheckError(msg) -> instance of DoItError

        Constructor.
        """

        DoItError.__init__(self, msg)
    #-def
#-class

@register_error(Exceptions.ParseError)
class ParseError(DoItError):
    """Raised during parsing process when parser realizes that word does not
       belong to given language.
    """

    def __init__(self, msg):
        """ParseError(msg) -> instance of DoItError

        Constructor.
        """

        DoItError.__init__(self, msg)
    #-def
#-class
