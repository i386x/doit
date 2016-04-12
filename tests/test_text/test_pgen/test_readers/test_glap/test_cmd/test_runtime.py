#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/ \
#!              test_readers/test_glap/test_cmd/test_runtime.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-04-07 18:58:51 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Glap reader command processor runtime module tests.\
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

from doit.text.pgen.readers.glap.cmd.runtime import \
    ExceptionObject, \
    ExceptionClass, \
    BaseExceptionClass, \
    Exceptions

class PseudoTraceback(object):
    __slots__ = [ '__content' ]

    def __init__(self, content):
        self.__content = content
    #-def

    def __str__(self):
        return self.__content
    #-def
#-class

class PseudoProcessor(object):
    __slots__ = [ '__uid' ]

    def __init__(self, uid):
        self.__uid = uid
    #-def

    def traceback(self):
        return PseudoTraceback("<tb #%d>" % self.__uid)
    #-def
#-class

class TestExceptionObjectCase(unittest.TestCase):

    def test_getters(self):
        obj = ExceptionObject(self, 1, 2, 'a')

        self.assertIs(obj.cls(), self)
        self.assertEqual(obj.args(), (1, 2, 'a'))
    #-def
#-class

class TestExceptionsCase(unittest.TestCase):

    def setUp(self):
        self.exceptions = Exceptions(PseudoProcessor(123))
        self.exceptions.register_exceptions(
            ('Exception', 'BaseException'),
            ('SystemExit', 'BaseException'),
            ('SystemPause', 'BaseException'),
            ('SystemResume', 'BaseException'),
            ('TypeError', 'Exception'),
            ('ValueError', 'Exception'),
            ('RuntimeError', 'Exception'),
            ('IOError', 'Exception'),
            ('UserException', 'Exception'),
            ('ArgumentsError', 'UserException'),
            ('AccessError', 'UserException')
        )
    #-def

    def test_getters(self):
        cls = self.exceptions['Exception']

        self.assertTrue(isinstance(cls, ExceptionClass))
        self.assertEqual(cls.name(), 'Exception')
        self.assertTrue(isinstance(cls.base(), BaseExceptionClass))
        self.assertIs(cls.base(), self.exceptions['BaseException'])
        self.assertEqual(cls.base().name(), 'BaseException')
    #-def

    def test_is_superclass_of(self):
        exceptions = Exceptions(PseudoProcessor(456))
        exceptions.register_exception('Exception', 'BaseException')

        self.assertFalse(self.exceptions['Exception'].is_superclass_of(0))
        self.assertFalse(
            exceptions['Exception'].is_superclass_of(
                self.exceptions['AccessError']
            )
        )
        self.assertFalse(
            exceptions['BaseException'].is_superclass_of(
                self.exceptions['Exception']
            )
        )
        self.assertFalse(
            exceptions['Exception'].is_superclass_of(
                self.exceptions['BaseException']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['BaseException']
            )
        )
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestExceptionObjectCase))
    suite.addTest(unittest.makeSuite(TestExceptionsCase))
    return suite
#-def
