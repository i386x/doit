#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-03-09 17:10:29 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! errors and exceptions.\
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

import sys
import inspect

ERROR_OK = 0
ERROR_ASSERT = 1
ERROR_NOT_IMPLEMENTED = 2
ERROR_OVERFLOW = 3
ERROR_UNDERFLOW = 4
ERROR_MEMORY_ACCESS = 5
ERROR_RUNTIME = 6
ERROR_TYPE = 7
ERROR_ASSEMBLER = 8
ERROR_LINKER = 9
ERROR_UNKNOWN = 255

class DoItError(Exception):
    """General |doit| exception.

    :cvar str ERRMSGFMT: Error message format string.
    :ivar int errcode: Error code.
    :ivar str detail: Why the exception was raised.
    """
    ERRMSGFMT = "%s [errcode = %d]: %s."
    __slots__ = [ 'errcode', 'detail' ]

    def __init__(self, ecode, emsg):
        """Initializes the exception.

        :param int ecode: An error code.
        :param str emsg: An error message.
        """

        Exception.__init__(self, ecode, emsg)
        self.errcode = ecode
        self.detail = emsg
    #-def

    def __repr__(self):
        """Implements the :func:`repr` operator.

        :returns: The text representation of exception (:class:`str`).
        """

        return self.__class__.__name__ + repr(self.args)
    #-def

    def __str__(self):
        """Implements the :class:`str` operator.

        :returns: The formatted error message (:class:`str`).
        """

        return DoItError.ERRMSGFMT % (
            self.__class__.__name__, self.errcode, self.detail
        )
    #-def
#-class

class DoItAssertionError(DoItError):
    """Raised when assertion fails.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_ASSERT, emsg)
    #-def
#-class

class DoItNotImplementedError(DoItError):
    """Raised when invoked method or function is not implemented.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_NOT_IMPLEMENTED, emsg)
    #-def
#-class

class DoItOverflowError(DoItError):
    """Raised when arithmetic operation overflows.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_OVERFLOW, emsg)
    #-def
#-class

class DoItUnderflowError(DoItError):
    """Raised when arithmetic operation underflows.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_UNDERFLOW, emsg)
    #-def
#-class

class DoItMemoryAccessError(DoItError):
    """Raised when the attempt to access to the given memory location fails.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_MEMORY_ACCESS, emsg)
    #-def
#-class

class DoItRuntimeError(DoItError):
    """Raised when the execution of |doit| code fails.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_RUNTIME, emsg)
    #-def
#-class

class DoItTypeError(DoItError):
    """Raised when operand has a bad type.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_TYPE, emsg)
    #-def
#-class

class DoItAssemblerError(DoItError):
    """Raised when assembling the code fails.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_ASSEMBLER, emsg)
    #-def
#-class

class DoItLinkerError(DoItError):
    """Raised when linking the linkable objects fails.
    """
    __slots__ = []

    def __init__(self, emsg):
        """Initializes the exception.

        :param str emsg: An error message.
        """

        DoItError.__init__(self, ERROR_LINKER, emsg)
    #-def
#-class

def __get_caller_name(caller_frame):
    """Gets the name of the caller (fully qualified, if possible).

    :param caller_frame: A caller's frame.
    :type caller_frame: :class:`frame`

    :returns: The name of the caller (:class:`str`).
    """

    caller_name = caller_frame.f_code.co_name
    if 'self' in caller_frame.f_locals:
        caller_name = "%s.%s" % (
            caller_frame.f_locals['self'].__class__.__name__, caller_name
        )
    module = inspect.getmodule(caller_frame)
    if module:
        caller_name = "%s.%s" % (module.__name__, caller_name)
    return caller_name
#-def

def doit_assert(
    cond, emsg = "Assertion failed", exc = DoItAssertionError, nframe = 1
):
    """Raise `exc(emsg)` if `cond` is false.

    :param bool cond: A condition.
    :param str emsg: An error message.
    :param type exc: A :exc:`DoItError <doit.support.errors.DoItError>` \
        based exception class.
    :param int nframe: A caller's frame position.

    :raises ~doit.support.errors.DoItError: When `cond` is false.
    """

    if not cond:
        raise exc("%s: %s" % (__get_caller_name(sys._getframe(nframe)), emsg))
#-def

def not_implemented():
    """Raise an exception if the called method or function is not implemented.

    :raises ~doit.support.errors.DoItNotImplementedError: When the invoked \
        method or function is not implemented.

    Call this function from another function or method. If you call this
    function from method, it must not to be a static method or class method
    (additionally, tagging a static/class method as not implemented has no
    sense). Example::

        def some_function():
            not_implemented()

        class SomeClass:
            def some_method(self):
                not_implemented()
    """

    raise DoItNotImplementedError(
        "%s is not implemented" % __get_caller_name(sys._getframe(1))
    )
#-def
