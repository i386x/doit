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

from doit.support.errors import DoItError, not_implemented

COMMAND_PROCESSOR_ERROR_BASE = DoItError.alloc_codes(16)

ERROR_CMDPROC_RUNTIME   = COMMAND_PROCESSOR_ERROR_BASE
ERROR_CMDPROC_ARGUMENTS = ERROR_CMDPROC_RUNTIME + 1
ERROR_CMDPROC_EVAL      = ERROR_CMDPROC_ARGUMENTS + 1
ERROR_CMDPROC_NAME      = ERROR_CMDPROC_EVAL + 1
ERROR_CMDPROC_TYPE      = ERROR_CMDPROC_NAME + 1
ERROR_CMDPROC_CAST      = ERROR_CMDPROC_TYPE + 1
ERROR_CMDPROC_CONTAINER = ERROR_CMDPROC_CAST + 1

class CommandProcessorError(DoItError):
    """
    """
    __slots__ = [ 'traceback' ]

    def __init__(self, traceback_provider, ecode, emsg):
        """
        """

        DoItError.__init__(self, ecode, emsg)
        self.traceback = traceback_provider.traceback()
    #-def

    def __str__(self):
        """
        """

        if self.traceback:
            return "%s %s" % (str(self.traceback), DoItError.__str__(self))
        return DoItError.__str__(self)
    #-def

    def internal_name(self):
        """
        """

        not_implemented()
    #-def
#-class

class CmdProcRuntimeError(CommandProcessorError):
    """
    """
    __slots__ = []

    def __init__(self, traceback_provider, emsg):
        """
        """

        CommandProcessorError.__init__(self,
            traceback_provider, ERROR_CMDPROC_RUNTIME, emsg
        )
    #-def

    def internal_name(self):
        """
        """

        return 'RuntimeError'
    #-def
#-class

class CmdProcArgumentsError(CommandProcessorError):
    """
    """
    __slots__ = []

    def __init__(self, traceback_provider, emsg):
        """
        """

        CommandProcessorError.__init__(self,
            traceback_provider, ERROR_CMDPROC_ARGUMENTS, emsg
        )
    #-def

    def internal_name(self):
        """
        """

        return 'ArgumentsError'
    #-def
#-class

class CmdProcEvalError(CommandProcessorError):
    """
    """
    __slots__ = []

    def __init__(self, traceback_provider, emsg):
        """
        """

        CommandProcessorError.__init__(self,
            traceback_provider, ERROR_CMDPROC_EVAL, emsg
        )
    #-def

    def internal_name(self):
        """
        """

        return 'EvalError'
    #-def
#-class

class CmdProcNameError(CommandProcessorError):
    """
    """
    __slots__ = []

    def __init__(self, traceback_provider, emsg):
        """
        """

        CommandProcessorError.__init__(self,
            traceback_provider, ERROR_CMDPROC_NAME, emsg
        )
    #-def

    def internal_name(self):
        """
        """

        return 'NameError'
    #-def
#-class

class CmdProcTypeError(CommandProcessorError):
    """
    """
    __slots__ = []

    def __init__(self, traceback_provider, emsg):
        """
        """

        CommandProcessorError.__init__(self,
            traceback_provider, ERROR_CMDPROC_TYPE, emsg
        )
    #-def

    def internal_name(self):
        """
        """

        return 'TypeError'
    #-def
#-class

class CmdProcCastError(CommandProcessorError):
    """
    """
    __slots__ = []

    def __init__(self, traceback_provider, emsg):
        """
        """

        CommandProcessorError.__init__(self,
            traceback_provider, ERROR_CMDPROC_CAST, emsg
        )
    #-def

    def internal_name(self):
        """
        """

        return 'CastError'
    #-def
#-class

class CmdProcContainerError(CommandProcessorError):
    """
    """
    __slots__ = []

    def __init__(self, traceback_provider, emsg):
        """
        """

        CommandProcessorError.__init__(self,
            traceback_provider, ERROR_CMDPROC_CONTAINER, emsg
        )
    #-def

    def internal_name(self):
        """
        """

        return 'ContainerError'
    #-def
#-class
