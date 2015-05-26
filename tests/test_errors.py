#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-02-20 20:31:35 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! errors module tests.\
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
import unittest

from .common import PYTHON_OBJECT_REPR_STR_sd, StderrMock
from doit import errors

class TestPerrorCase(unittest.TestCase):

    def test_perror_send_data_to_stderr(self):
        emsg = "Something is bad."
        with StderrMock() as stderr:
            errors.perror(emsg)
        self.assertEqual("%s\n" % emsg, stderr.data)
    #-def
#-class

class TestDoItErrorCase(unittest.TestCase):

    def test_DoItError(self):
        error_message = "Error message"
        error_code = 214
        with self.assertRaises(errors.DoItError) as eh1:
            raise errors.DoItError(error_message)
        self.assertEqual(eh1.exception.detail, error_message)
        self.assertEqual(eh1.exception.errcode, errors.DEFAULT_ERROR_CODE)
        self.assertEqual(
            repr(eh1.exception),
            PYTHON_OBJECT_REPR_STR_sd % (
                errors.DoItError.__name__,
                error_message,
                errors.DEFAULT_ERROR_CODE
            )
        )
        self.assertEqual(
            str(eh1.exception),
            errors.DoItError.ERRMSGFMT % (
                errors.DoItError.__name__,
                errors.DEFAULT_ERROR_CODE,
                error_message
            )
        )
        with self.assertRaises(errors.DoItError) as eh2:
            raise errors.DoItError(error_message, error_code)
        self.assertEqual(eh2.exception.detail, error_message)
        self.assertEqual(eh2.exception.errcode, error_code)
        self.assertEqual(
            repr(eh2.exception),
            PYTHON_OBJECT_REPR_STR_sd % (
                errors.DoItError.__name__,
                error_message,
                error_code
            )
        )
        self.assertEqual(
            str(eh2.exception),
            errors.DoItError.ERRMSGFMT % (
                errors.DoItError.__name__,
                error_code,
                error_message
            )
        )
    #-def

    def test_RuntimeError(self):
        iname = 'INST'
        ip = 3
        error_message = "Error message"
        with self.assertRaises(errors.RuntimeError) as eh:
            raise errors.RuntimeError(iname, ip, error_message)
        self.assertEqual(
            eh.exception.detail,
            errors.RuntimeError.ERRMSGFMT % (iname, ip, error_message)
        )
        self.assertEqual(eh.exception.errcode, errors.DEFAULT_ERROR_CODE)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_sd % (
                errors.RuntimeError.__name__,
                errors.RuntimeError.ERRMSGFMT % (iname, ip, error_message),
                errors.DEFAULT_ERROR_CODE
            )
        )
        self.assertEqual(
            str(eh.exception),
            errors.DoItError.ERRMSGFMT % (
                errors.RuntimeError.__name__,
                errors.DEFAULT_ERROR_CODE,
                errors.RuntimeError.ERRMSGFMT % (iname, ip, error_message)
            )
        )
    #-def

    def test_IOError(self):
        error_message = "I/O operation failed"
        with self.assertRaises(errors.IOError) as eh:
            raise errors.IOError(error_message)
        self.assertEqual(eh.exception.detail, error_message)
        self.assertEqual(eh.exception.errcode, errors.DEFAULT_ERROR_CODE)
        self.assertEqual(
            repr(eh.exception),
            PYTHON_OBJECT_REPR_STR_sd % (
                errors.IOError.__name__,
                error_message,
                errors.DEFAULT_ERROR_CODE
            )
        )
        self.assertEqual(
            str(eh.exception),
            errors.DoItError.ERRMSGFMT % (
                errors.IOError.__name__,
                errors.DEFAULT_ERROR_CODE,
                error_message
            )
        )
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPerrorCase))
    suite.addTest(unittest.makeSuite(TestDoItErrorCase))
    return suite
#-def
