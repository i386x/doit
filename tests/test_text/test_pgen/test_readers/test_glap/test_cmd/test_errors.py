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
    ERROR_COMMAND_PROCESSOR, \
    ERROR_COMMAND, \
    CommandProcessorError, \
    CommandError, \
    CmdExceptionError, \
    CmdNameError, \
    CmdTypeError

class AuxTraceback(list):
    __slots__ = []

    def __init__(self, content):
        list.__init__(self, content)
    #-def

    def __str__(self):
        return ".".join(self)
    #-def
#-class

class TestCommandProcessorErrorCase(unittest.TestCase):

    def test_CommandProcessorError(self):
        error_code = ERROR_COMMAND_PROCESSOR
        error_message = "Dummy error message"
        traceback = AuxTraceback(["f1", "f2", "g3"])
        empty_traceback = AuxTraceback([])

        with self.assertRaises(CommandProcessorError) as eh:
            raise CommandProcessorError(traceback, error_message)

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
            raise CommandProcessorError(empty_traceback, error_message)

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                CommandProcessorError.__name__,
                error_code,
                error_message
            )
        )
    #-def
#-class

class TestCommandErrorCase(unittest.TestCase):

    def test_CommandError(self):
        detail = "Some error detail"

        self.assertEqual(CommandError.SID, 'CommandError')

        with self.assertRaises(CommandError) as eh:
            raise CommandError(detail)

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                "CommandError <CommandError>", ERROR_COMMAND, detail
            )
        )
        self.assertEqual(
            repr(eh.exception), "CommandError(\"%s\")" % detail
        )
    #-def

    def test_CmdExceptionError(self):
        detail = "Some error detail"

        self.assertEqual(CmdExceptionError.SID, 'ExceptionError')

        with self.assertRaises(CmdExceptionError) as eh:
            raise CmdExceptionError(detail)

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                "CommandError <ExceptionError>", ERROR_COMMAND, detail
            )
        )
        self.assertEqual(
            repr(eh.exception), "ExceptionError(\"%s\")" % detail
        )
    #-def

    def test_CmdNameError(self):
        detail = "Some error detail"

        self.assertEqual(CmdNameError.SID, 'NameError')

        with self.assertRaises(CmdNameError) as eh:
            raise CmdNameError(detail)

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                "CommandError <NameError>", ERROR_COMMAND, detail
            )
        )
        self.assertEqual(
            repr(eh.exception), "NameError(\"%s\")" % detail
        )
    #-def

    def test_CmdTypeError(self):
        detail = "Some error detail"

        self.assertEqual(CmdTypeError.SID, 'TypeError')

        with self.assertRaises(CmdTypeError) as eh:
            raise CmdTypeError(detail)

        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                "CommandError <TypeError>", ERROR_COMMAND, detail
            )
        )
        self.assertEqual(
            repr(eh.exception), "TypeError(\"%s\")" % detail
        )
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommandProcessorErrorCase))
    suite.addTest(unittest.makeSuite(TestCommandErrorCase))
    return suite
#-def
