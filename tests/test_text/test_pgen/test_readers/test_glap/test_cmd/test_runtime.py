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

from doit.text.pgen.readers.glap.cmd.errors import \
    CmdExceptionError, \
    CmdTypeError

from doit.text.pgen.readers.glap.cmd.runtime import \
    BaseIterator, \
    FiniteIterator, \
    ExceptionClass, \
    BaseExceptionClass, \
    Exceptions, \
    Traceback, \
    ProcedureTemplate

from doit.text.pgen.readers.glap.cmd.commands import \
    Location

class PseudoCommand(object):
    __slots__ = [ 'name', 'location', '__isfunc' ]

    def __init__(self, name, location, isfunc = True):
        self.name = name
        self.location = location
        self.__isfunc = isfunc
    #-def

    def __str__(self):
        return self.name
    #-def

    def isfunc(self):
        return self.__isfunc
    #-def
#-class

class TestIteratorCase(unittest.TestCase):

    def test_BaseIterator(self):
        i = BaseIterator()

        i.reset()
        self.assertIs(i.next(), i)
    #-def

    def test_FiniteIterator(self):
        fi0 = FiniteIterator(())
        fi1 = FiniteIterator("abc")

        with self.assertRaises(CmdTypeError):
            FiniteIterator(None)

        fi0.reset()
        self.assertEqual(fi0.next(), fi0)
        self.assertEqual(fi0.next(), fi0)
        fi0.reset()
        self.assertEqual(fi0.next(), fi0)
        self.assertEqual(fi0.next(), fi0)

        fi1.reset()
        self.assertEqual(fi1.next(), "a")
        self.assertEqual(fi1.next(), "b")
        fi1.reset()
        self.assertEqual(fi1.next(), "a")
        self.assertEqual(fi1.next(), "b")
        self.assertEqual(fi1.next(), "c")
        self.assertEqual(fi1.next(), fi1)
        self.assertEqual(fi1.next(), fi1)
        fi1.reset()
        self.assertEqual(fi1.next(), "a")
    #-def
#-class

class TestExceptionsCase(unittest.TestCase):

    def setUp(self):
        self.exceptions = Exceptions()
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
        exceptions = Exceptions()
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
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['Exception']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['TypeError']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['ValueError']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['RuntimeError']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['IOError']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['UserException']
            )
        )
        self.assertTrue(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['Exception']
            )
        )
        self.assertTrue(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['TypeError']
            )
        )
        self.assertTrue(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['ValueError']
            )
        )
        self.assertTrue(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['RuntimeError']
            )
        )
        self.assertTrue(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['IOError']
            )
        )
        self.assertTrue(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['UserException']
            )
        )
        self.assertTrue(
            self.exceptions['UserException'].is_superclass_of(
                self.exceptions['UserException']
            )
        )
        self.assertTrue(
            self.exceptions['UserException'].is_superclass_of(
                self.exceptions['ArgumentsError']
            )
        )
        self.assertTrue(
            self.exceptions['UserException'].is_superclass_of(
                self.exceptions['AccessError']
            )
        )
        self.assertTrue(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['ArgumentsError']
            )
        )
        self.assertTrue(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['AccessError']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['ArgumentsError']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['AccessError']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['SystemExit']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['SystemPause']
            )
        )
        self.assertTrue(
            self.exceptions['BaseException'].is_superclass_of(
                self.exceptions['SystemResume']
            )
        )
        self.assertTrue(
            self.exceptions['SystemPause'].is_superclass_of(
                self.exceptions['SystemPause']
            )
        )
        self.assertTrue(
            self.exceptions['AccessError'].is_superclass_of(
                self.exceptions['AccessError']
            )
        )
        self.assertFalse(
            self.exceptions['Exception'].is_superclass_of(
                self.exceptions['SystemPause']
            )
        )
        self.assertFalse(
            self.exceptions['SystemPause'].is_superclass_of(
                self.exceptions['Exception']
            )
        )
        self.assertFalse(
            self.exceptions['AccessError'].is_superclass_of(
                self.exceptions['RuntimeError']
            )
        )
        self.assertFalse(
            self.exceptions['RuntimeError'].is_superclass_of(
                self.exceptions['AccessError']
            )
        )
        self.assertFalse(
            self.exceptions['ArgumentsError'].is_superclass_of(
                self.exceptions['SystemExit']
            )
        )
        self.assertFalse(
            self.exceptions['SystemExit'].is_superclass_of(
                self.exceptions['ArgumentsError']
            )
        )
        self.assertFalse(
            self.exceptions['UserException'].is_superclass_of(
                self.exceptions['SystemPause']
            )
        )
        self.assertFalse(
            self.exceptions['SystemPause'].is_superclass_of(
                self.exceptions['UserException']
            )
        )
        self.assertFalse(
            self.exceptions['IOError'].is_superclass_of(
                self.exceptions['SystemPause']
            )
        )
        self.assertFalse(
            self.exceptions['SystemPause'].is_superclass_of(
                self.exceptions['IOError']
            )
        )
    #-def

    def test_register_exception(self):
        with self.assertRaises(CmdExceptionError):
            self.exceptions.register_exception('Exception', 'BaseException')
        with self.assertRaises(CmdExceptionError):
            self.exceptions.register_exception('MyError', '_UserException')
    #-def
#-class

class TestTracebackCase(unittest.TestCase):

    def test_traceback_methods(self):
        testdata = [(
            [],
            Location(),
            "In <main>:\n"
        ), (
            [],
            Location("foo.g", 1, 1),
            "In <main>:\n"
        ), (
            [ "cmd0" ],
            Location(),
            "In cmd0:\n" \
            ">"
        ), (
            [ "cmd1" ],
            Location("foo.g", 2, 3),
            "In cmd1:\n" \
            "> At [\"foo.g\":2:3]:"
        ), (
            [ "A", "B", "C" ],
            Location(),
            "In A\n" \
            "| from B\n" \
            "| from C:\n" \
            ">"
        ), (
            [ "f", "g", "h" ],
            Location("foo.g", 4, 7),
            "In f\n" \
            "| from g\n" \
            "| from h:\n" \
            "> At [\"foo.g\":4:7]:"
        )]

        for i, l, r in testdata:
            stack = []
            for cn in i:
                stack.append(PseudoCommand(cn, Location()))
            stack.append(PseudoCommand("<cmd>", l, False))
            tb = Traceback(stack)
            self.assertEqual(str(tb), r)
    #-def
#-class

class TestProcedureTemplateCase(unittest.TestCase):

    def test_ProcedureTemplate(self):
        bvars, params, body, outer = ['x'], ['y', 'z'], [], [[]]
        proct = ProcedureTemplate(bvars, params, body, outer)

        _bvars, _params, _body, _outer = proct
        self.assertEqual(_bvars, bvars)
        self.assertEqual(_params, params)
        self.assertEqual(_body, body)
        self.assertEqual(_outer, outer)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIteratorCase))
    suite.addTest(unittest.makeSuite(TestExceptionsCase))
    suite.addTest(unittest.makeSuite(TestTracebackCase))
    suite.addTest(unittest.makeSuite(TestProcedureTemplateCase))
    return suite
#-def
