#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/ \
#!              test_readers/test_glap/test_cmd/test_errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-04-06 20:37:59 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Glap reader command processor error module tests.\
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

import unittest

from doit.support.errors import DoItError

from doit.text.pgen.readers.glap.cmd.errors import \
    COMMAND_PROCESSOR_ERROR_BASE, \
    ERROR_CMDPROC_RUNTIME, \
    ERROR_CMDPROC_ARGUMENTS, \
    ERROR_CMDPROC_NAME, \
    ERROR_CMDPROC_TYPE, \
    ERROR_CMDPROC_CAST, \
    ERROR_CMDPROC_CONTAINER, \
    CommandProcessorError, \
    CmdProcRuntimeError, \
    CmdProcArgumentsError, \
    CmdProcNameError, \
    CmdProcTypeError, \
    CmdProcCastError, \
    CmdProcContainerError

class AuxTraceback(object):
    __slots__ = [ '__content' ]

    def __init__(self, content):
        self.__content = content
    #-def

    def __str__(self):
        return ".".join(self.__content)
    #-def
#-class

class AuxTracebackProvider(object):
    __slots__ = [ '__content' ]

    def __init__(self, *content):
        self.__content = list(content)
    #-def

    def traceback(self):
        return AuxTraceback(self.__content)
    #-def
#-class

class NoTracebackProvider(object):
    __slots__ = []

    def __init__(self):
        pass
    #-def

    def traceback(self):
        return None
    #-def
#-class

class TestCommandProcessorErrorCase(unittest.TestCase):

    def test_CommandProcessorError(self):
        error_code = COMMAND_PROCESSOR_ERROR_BASE
        error_message = "Dummy error message"
        traceback_provider = AuxTracebackProvider("f1", "f2", "g3")
        no_traceback_provider = NoTracebackProvider()

        with self.assertRaises(CommandProcessorError) as eh:
            raise CommandProcessorError(
                traceback_provider, error_code, error_message
            )

        self.assertEqual(eh.exception.internal_name(), 'SystemError')
        self.assertEqual(
            str(eh.exception),
            "f1.f2.g3 %s" % (
                DoItError.ERRMSGFMT % (
                    CommandProcessorError.__name__,
                    error_code,
                    error_message
                )
            )
        )

        with self.assertRaises(CommandProcessorError) as eh:
            raise CommandProcessorError(
                no_traceback_provider, error_code, error_message
            )

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                CommandProcessorError.__name__,
                error_code,
                error_message
            )
        )
    #-def

    def test_CmdProcRuntimeError(self):
        error_message = "Dummy runtime error"
        traceback_provider = AuxTracebackProvider("f1", "g2", "h3")
        no_traceback_provider = NoTracebackProvider()

        with self.assertRaises(CmdProcRuntimeError) as eh:
            raise CmdProcRuntimeError(
                traceback_provider, error_message
            )

        self.assertEqual(eh.exception.internal_name(), 'RuntimeError')
        self.assertEqual(
            str(eh.exception),
            "f1.g2.h3 %s" % (
                DoItError.ERRMSGFMT % (
                    CmdProcRuntimeError.__name__,
                    ERROR_CMDPROC_RUNTIME,
                    error_message
                )
            )
        )

        with self.assertRaises(CmdProcRuntimeError) as eh:
            raise CmdProcRuntimeError(
                no_traceback_provider, error_message
            )

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                CmdProcRuntimeError.__name__,
                ERROR_CMDPROC_RUNTIME,
                error_message
            )
        )
    #-def

    def test_CmdProcArgumentsError(self):
        error_message = "Dummy arguments error"
        traceback_provider = AuxTracebackProvider("f4", "g5", "h6")
        no_traceback_provider = NoTracebackProvider()

        with self.assertRaises(CmdProcArgumentsError) as eh:
            raise CmdProcArgumentsError(
                traceback_provider, error_message
            )

        self.assertEqual(eh.exception.internal_name(), 'ArgumentsError')
        self.assertEqual(
            str(eh.exception),
            "f4.g5.h6 %s" % (
                DoItError.ERRMSGFMT % (
                    CmdProcArgumentsError.__name__,
                    ERROR_CMDPROC_ARGUMENTS,
                    error_message
                )
            )
        )

        with self.assertRaises(CmdProcArgumentsError) as eh:
            raise CmdProcArgumentsError(
                no_traceback_provider, error_message
            )

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                CmdProcArgumentsError.__name__,
                ERROR_CMDPROC_ARGUMENTS,
                error_message
            )
        )
    #-def

    def test_CmdProcNameError(self):
        error_message = "Name 'name' is not defined"
        traceback_provider = AuxTracebackProvider("f_1", "g_2", "h_3")
        no_traceback_provider = NoTracebackProvider()

        with self.assertRaises(CmdProcNameError) as eh:
            raise CmdProcNameError(
                traceback_provider, error_message
            )

        self.assertEqual(eh.exception.internal_name(), 'NameError')
        self.assertEqual(
            str(eh.exception),
            "f_1.g_2.h_3 %s" % (
                DoItError.ERRMSGFMT % (
                    CmdProcNameError.__name__,
                    ERROR_CMDPROC_NAME,
                    error_message
                )
            )
        )

        with self.assertRaises(CmdProcNameError) as eh:
            raise CmdProcNameError(
                no_traceback_provider, error_message
            )

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                CmdProcNameError.__name__,
                ERROR_CMDPROC_NAME,
                error_message
            )
        )
    #-def

    def test_CmdProcTypeError(self):
        error_message = "Dummy type error"
        traceback_provider = AuxTracebackProvider("f_", "g_", "h_")
        no_traceback_provider = NoTracebackProvider()

        with self.assertRaises(CmdProcTypeError) as eh:
            raise CmdProcTypeError(
                traceback_provider, error_message
            )

        self.assertEqual(eh.exception.internal_name(), 'TypeError')
        self.assertEqual(
            str(eh.exception),
            "f_.g_.h_ %s" % (
                DoItError.ERRMSGFMT % (
                    CmdProcTypeError.__name__,
                    ERROR_CMDPROC_TYPE,
                    error_message
                )
            )
        )

        with self.assertRaises(CmdProcTypeError) as eh:
            raise CmdProcTypeError(
                no_traceback_provider, error_message
            )

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                CmdProcTypeError.__name__,
                ERROR_CMDPROC_TYPE,
                error_message
            )
        )
    #-def

    def test_CmdProcCastError(self):
        error_message = "Dummy cast error"
        traceback_provider = AuxTracebackProvider("fx", "gx", "hx")
        no_traceback_provider = NoTracebackProvider()

        with self.assertRaises(CmdProcCastError) as eh:
            raise CmdProcCastError(
                traceback_provider, error_message
            )

        self.assertEqual(eh.exception.internal_name(), 'CastError')
        self.assertEqual(
            str(eh.exception),
            "fx.gx.hx %s" % (
                DoItError.ERRMSGFMT % (
                    CmdProcCastError.__name__,
                    ERROR_CMDPROC_CAST,
                    error_message
                )
            )
        )

        with self.assertRaises(CmdProcCastError) as eh:
            raise CmdProcCastError(
                no_traceback_provider, error_message
            )

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                CmdProcCastError.__name__,
                ERROR_CMDPROC_CAST,
                error_message
            )
        )
    #-def

    def test_CmdProcContainerError(self):
        error_message = "Dummy container error"
        traceback_provider = AuxTracebackProvider("a1", "a2", "a3")
        no_traceback_provider = NoTracebackProvider()

        with self.assertRaises(CmdProcContainerError) as eh:
            raise CmdProcContainerError(
                traceback_provider, error_message
            )

        self.assertEqual(eh.exception.internal_name(), 'ContainerError')
        self.assertEqual(
            str(eh.exception),
            "a1.a2.a3 %s" % (
                DoItError.ERRMSGFMT % (
                    CmdProcContainerError.__name__,
                    ERROR_CMDPROC_CONTAINER,
                    error_message
                )
            )
        )

        with self.assertRaises(CmdProcContainerError) as eh:
            raise CmdProcContainerError(
                no_traceback_provider, error_message
            )

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                CmdProcContainerError.__name__,
                ERROR_CMDPROC_CONTAINER,
                error_message
            )
        )
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommandProcessorErrorCase))
    return suite
#-def
