#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-02-20 20:31:35 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! errors module tests.\
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
import unittest

from ..common import PYTHON_OBJECT_REPR_STR_ds

from doit.support.errors import ERROR_ASSERT, \
                                ERROR_NOT_IMPLEMENTED, \
                                ERROR_MEMORY_ACCESS, \
                                ERROR_RUNTIME, \
                                ERROR_ASSEMBLER, \
                                ERROR_LINKER, \
                                ERROR_UNKNOWN, \
                                DoItError, \
                                DoItAssertionError, \
                                DoItNotImplementedError, \
                                DoItMemoryAccessError, \
                                DoItRuntimeError, \
                                DoItAssemblerError, \
                                DoItLinkerError, \
                                doit_assert, \
                                not_implemented

class AuxError(DoItError):
    __slots__ = []

    def __init__(self, emsg):
        DoItError.__init__(self, ERROR_UNKNOWN, emsg)
    #-def
#-class

def some_function():
    not_implemented()
#-def

class SomeClass(object):
    __slots__ = []

    def some_method(self):
        not_implemented()
    #-def
#-class

class TestDoItErrorCase(unittest.TestCase):

    def test_DoItError(self):
        error_code = ERROR_UNKNOWN
        error_message = "Test DoIt error"

        with self.assertRaises(DoItError) as eh:
            raise DoItError(error_code, error_message)

        self.assertEqual(eh.exception.errcode, error_code)
        self.assertEqual(eh.exception.detail, error_message)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_ds % (
                DoItError.__name__,
                error_code,
                error_message
            )
        )
        self.assertEqual(
            str(eh.exception),
            DoItError.ERRMSGFMT % (
                DoItError.__name__,
                error_code,
                error_message
            )
        )
    #-def

    def test_DoItAssertionError(self):
        error_code = ERROR_ASSERT
        error_message = "Test DoIt assertion error"

        with self.assertRaises(DoItAssertionError) as eh:
            raise DoItAssertionError(error_message)

        self.assertEqual(eh.exception.errcode, error_code)
        self.assertEqual(eh.exception.detail, error_message)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_ds % (
                DoItAssertionError.__name__,
                error_code,
                error_message
            )
        )
        self.assertEqual(
            str(eh.exception),
            DoItAssertionError.ERRMSGFMT % (
                DoItAssertionError.__name__,
                error_code,
                error_message
            )
        )
    #-def

    def test_DoItNotImplementedError(self):
        error_code = ERROR_NOT_IMPLEMENTED
        error_message = "Test DoIt not implemented error"

        with self.assertRaises(DoItNotImplementedError) as eh:
            raise DoItNotImplementedError(error_message)

        self.assertEqual(eh.exception.errcode, error_code)
        self.assertEqual(eh.exception.detail, error_message)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_ds % (
                DoItNotImplementedError.__name__,
                error_code,
                error_message
            )
        )
        self.assertEqual(
            str(eh.exception),
            DoItNotImplementedError.ERRMSGFMT % (
                DoItNotImplementedError.__name__,
                error_code,
                error_message
            )
        )
    #-def

    def test_DoItMemoryAccessError(self):
        error_code = ERROR_MEMORY_ACCESS
        error_message = "Test DoIt memory access error"

        with self.assertRaises(DoItMemoryAccessError) as eh:
            raise DoItMemoryAccessError(error_message)

        self.assertEqual(eh.exception.errcode, error_code)
        self.assertEqual(eh.exception.detail, error_message)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_ds % (
                DoItMemoryAccessError.__name__,
                error_code,
                error_message
            )
        )
        self.assertEqual(
            str(eh.exception),
            DoItMemoryAccessError.ERRMSGFMT % (
                DoItMemoryAccessError.__name__,
                error_code,
                error_message
            )
        )
    #-def

    def test_DoItRuntimeError(self):
        error_code = ERROR_RUNTIME
        error_message = "Test DoIt runtime error"

        with self.assertRaises(DoItRuntimeError) as eh:
            raise DoItRuntimeError(error_message)

        self.assertEqual(eh.exception.errcode, error_code)
        self.assertEqual(eh.exception.detail, error_message)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_ds % (
                DoItRuntimeError.__name__,
                error_code,
                error_message
            )
        )
        self.assertEqual(
            str(eh.exception),
            DoItRuntimeError.ERRMSGFMT % (
                DoItRuntimeError.__name__,
                error_code,
                error_message
            )
        )
    #-def

    def test_DoItAssemblerError(self):
        error_code = ERROR_ASSEMBLER
        error_message = "Test DoIt assembler error"

        with self.assertRaises(DoItAssemblerError) as eh:
            raise DoItAssemblerError(error_message)

        self.assertEqual(eh.exception.errcode, error_code)
        self.assertEqual(eh.exception.detail, error_message)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_ds % (
                DoItAssemblerError.__name__,
                error_code,
                error_message
            )
        )
        self.assertEqual(
            str(eh.exception),
            DoItAssemblerError.ERRMSGFMT % (
                DoItAssemblerError.__name__,
                error_code,
                error_message
            )
        )
    #-def

    def test_DoItLinkerError(self):
        error_code = ERROR_LINKER
        error_message = "Test DoIt linker error"

        with self.assertRaises(DoItLinkerError) as eh:
            raise DoItLinkerError(error_message)

        self.assertEqual(eh.exception.errcode, error_code)
        self.assertEqual(eh.exception.detail, error_message)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_ds % (
                DoItLinkerError.__name__,
                error_code,
                error_message
            )
        )
        self.assertEqual(
            str(eh.exception),
            DoItLinkerError.ERRMSGFMT % (
                DoItLinkerError.__name__,
                error_code,
                error_message
            )
        )
    #-def
#-class

class TestDoItAssertCase(unittest.TestCase):

    def test_doit_assert(self):
        this_module_name = inspect.getmodule(sys._getframe(0)).__name__
        this_method_qname = "%s.TestDoItAssertCase.test_doit_assert" \
                            % this_module_name
        error_message_template = "%s: %s"
        error_message = "Something is wrong"
        remsg1 = error_message_template % (
            this_method_qname, "Assertion failed"
        )
        remsg2 = error_message_template % (this_method_qname, error_message)

        fail = lambda emsg: doit_assert(False, emsg, AuxError, 2)

        doit_assert(True)
        doit_assert(True, error_message)
        doit_assert(True, error_message, AuxError)
        doit_assert(True, error_message, AuxError, 2)

        with self.assertRaises(DoItAssertionError) as eh1:
            doit_assert(False)

        self.assertEqual(eh1.exception.errcode, ERROR_ASSERT)
        self.assertEqual(eh1.exception.detail, remsg1)

        with self.assertRaises(DoItAssertionError) as eh2:
            doit_assert(False, error_message)

        self.assertEqual(eh2.exception.errcode, ERROR_ASSERT)
        self.assertEqual(eh2.exception.detail, remsg2)

        with self.assertRaises(AuxError) as eh3:
            doit_assert(False, error_message, AuxError)

        self.assertEqual(eh3.exception.errcode, ERROR_UNKNOWN)
        self.assertEqual(eh3.exception.detail, remsg2)

        with self.assertRaises(AuxError) as eh4:
            fail(error_message)

        self.assertEqual(eh4.exception.errcode, ERROR_UNKNOWN)
        self.assertEqual(eh4.exception.detail, remsg2)
    #-def
#-class

class TestDoItNotImplementedCase(unittest.TestCase):

    def test_not_implemented(self):
        this_module_name = inspect.getmodule(sys._getframe(0)).__name__
        error_message_template = "%s.%s is not implemented"
        emsg1 = error_message_template % (this_module_name, "some_function")
        emsg2 = error_message_template % (
            this_module_name, "SomeClass.some_method"
        )

        with self.assertRaises(DoItNotImplementedError) as eh1:
            some_function()

        self.assertEqual(eh1.exception.errcode, ERROR_NOT_IMPLEMENTED)
        self.assertEqual(eh1.exception.detail, emsg1)

        with self.assertRaises(DoItNotImplementedError) as eh2:
            SomeClass().some_method()

        self.assertEqual(eh2.exception.errcode, ERROR_NOT_IMPLEMENTED)
        self.assertEqual(eh2.exception.detail, emsg2)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDoItErrorCase))
    suite.addTest(unittest.makeSuite(TestDoItAssertCase))
    suite.addTest(unittest.makeSuite(TestDoItNotImplementedCase))
    return suite
#-def
