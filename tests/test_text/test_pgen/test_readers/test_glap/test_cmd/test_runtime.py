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

from doit.support.errors import DoItNotImplementedError

from doit.text.pgen.readers.glap.cmd.errors import \
    CmdProcNameError, \
    CmdProcContainerError

from doit.text.pgen.readers.glap.cmd.commands import \
    Location

from doit.text.pgen.readers.glap.cmd.runtime import \
    ExceptionObject, \
    ExceptionClass, \
    BaseExceptionClass, \
    Exceptions, \
    ValueProvider, \
    Traceback, \
    TracebackProvider, \
    StackItem, \
    Scope, \
    Frame

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

class PseudoCommand(object):
    __slots__ = [ '__name', '__location' ]

    def __init__(self, name, location):
        self.__name = name
        self.__location = location
    #-def

    def __str__(self):
        return self.__name
    #-def

    def get_location(self):
        return self.__location
    #-def
#-class

class PseudoFinalizer(object):
    __slots__ = [ '__l', '__v' ]

    def __init__(self, l, v):
        self.__l = l
        self.__v = v
    #-def

    def __call__(self):
        self.__l.append(self.__v)
    #-def
#-class

class PseudoArgumentProxy(ValueProvider):
    __slots__ = [ '__v' ]

    def __init__(self, v):
        ValueProvider.__init__(self)
        self.__v = v
    #-def

    def value(self, traceback_provider):
        return self.__v
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
        with self.assertRaises(CmdProcContainerError):
            self.exceptions.register_exception('Exception', 'BaseException')
        with self.assertRaises(CmdProcContainerError):
            self.exceptions.register_exception('MyError', '_UserException')
    #-def
#-class

class TestValueProviderCase(unittest.TestCase):

    def test_base(self):
        with self.assertRaises(DoItNotImplementedError):
            ValueProvider().value(PseudoProcessor(1001))
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
            tb = Traceback(PseudoCommand("<cmd>", l))
            for c in i:
                tb.append(PseudoCommand(c, Location()))
            self.assertEqual(str(tb), r)
    #-def
#-class

class TestTracebackProviderCase(unittest.TestCase):

    def test_base(self):
        with self.assertRaises(DoItNotImplementedError):
            TracebackProvider().traceback()
    #-def
#-class

class TestStackItemsCase(unittest.TestCase):

    def setUp(self):
        self.globals = Scope(None, None)
        self.locals = self.globals

        self.locals0 = self.locals
        self.push(PseudoCommand("print", Location("c.g", 10, 4)), Frame)
        self.locals1 = self.locals
        self.push(PseudoCommand("if", Location("c.g", 16, 8)), Scope)
        self.locals2 = self.locals
        self.push(PseudoCommand("assign", Location("c.g", 20, 12)), StackItem)
        self.locals3 = self.locals
    #-def

    def push(self, cmd, sticls):
        self.locals = sticls(cmd, self.locals)
    #-def

    def test_get_command(self):
        self.assertIsNone(self.globals.get_command())
        self.assertEqual(str(self.locals.get_command()), "assign")
        self.assertIsNone(self.locals0.get_command())
        self.assertEqual(str(self.locals1.get_command()), "print")
        self.assertEqual(str(self.locals2.get_command()), "if")
        self.assertEqual(str(self.locals3.get_command()), "assign")
    #-def

    def test_get_prev(self):
        self.assertIsNone(self.globals.get_prev())
        self.assertIs(self.locals.get_prev(), self.locals2)
        self.assertIsNone(self.locals0.get_prev())
        self.assertIs(self.locals1.get_prev(), self.locals0)
        self.assertIs(self.locals2.get_prev(), self.locals1)
        self.assertIs(self.locals3.get_prev(), self.locals2)
    #-def

    def test_setvar_getvar(self):
        # Global scope:
        self.globals.setvar("gvar_A01", 1001)
        # "if" scope:
        self.locals.setvar("lvar_B01", 1002)
        # Global scope:
        self.locals0.setvar("l0var_C01", 1003)
        # "print" scope:
        self.locals1.setvar("l1var_D01", PseudoArgumentProxy(1004))
        # "if" scope:
        self.locals2.setvar("l2var_E01", 1005)
        # "if" scope:
        self.locals3.setvar("l3var_F01", 1006)

        # "if" scope:
        self.assertEqual(self.locals.getvar("gvar_A01"), 1001)
        self.assertEqual(self.locals.getvar("lvar_B01"), 1002)
        self.assertEqual(self.locals.getvar("l0var_C01"), 1003)
        self.assertEqual(self.locals.getvar("l1var_D01"), 1004)
        self.assertEqual(self.locals.getvar("l2var_E01"), 1005)
        self.assertEqual(self.locals.getvar("l3var_F01"), 1006)

        # "if" scope:
        self.assertEqual(self.locals3.getvar("gvar_A01"), 1001)
        self.assertEqual(self.locals3.getvar("lvar_B01"), 1002)
        self.assertEqual(self.locals3.getvar("l0var_C01"), 1003)
        self.assertEqual(self.locals3.getvar("l1var_D01"), 1004)
        self.assertEqual(self.locals3.getvar("l2var_E01"), 1005)
        self.assertEqual(self.locals3.getvar("l3var_F01"), 1006)

        # "if" scope:
        self.assertEqual(self.locals2.getvar("gvar_A01"), 1001)
        self.assertEqual(self.locals2.getvar("lvar_B01"), 1002)
        self.assertEqual(self.locals2.getvar("l0var_C01"), 1003)
        self.assertEqual(self.locals2.getvar("l1var_D01"), 1004)
        self.assertEqual(self.locals2.getvar("l2var_E01"), 1005)
        self.assertEqual(self.locals2.getvar("l3var_F01"), 1006)

        # "print" scope:
        self.assertEqual(self.locals1.getvar("gvar_A01"), 1001)
        with self.assertRaises(CmdProcNameError):
            self.locals1.getvar("lvar_B01")
        self.assertEqual(self.locals1.getvar("l0var_C01"), 1003)
        self.assertEqual(self.locals1.getvar("l1var_D01"), 1004)
        with self.assertRaises(CmdProcNameError):
            self.locals1.getvar("l2var_E01")
        with self.assertRaises(CmdProcNameError):
            self.locals1.getvar("l3var_F01")

        # Global scope:
        self.assertEqual(self.locals0.getvar("gvar_A01"), 1001)
        with self.assertRaises(CmdProcNameError):
            self.locals0.getvar("lvar_B01")
        self.assertEqual(self.locals0.getvar("l0var_C01"), 1003)
        with self.assertRaises(CmdProcNameError):
            self.locals0.getvar("l1var_D01")
        with self.assertRaises(CmdProcNameError):
            self.locals0.getvar("l2var_E01")
        with self.assertRaises(CmdProcNameError):
            self.locals0.getvar("l3var_F01")
    #-def

    def test_finalizers_container(self):
        l = []
        self.locals.add_finalizer(PseudoFinalizer(l, "f1"))
        self.locals.add_finalizer(PseudoFinalizer(l, "f2"))
        self.locals.add_finalizer(PseudoFinalizer(l, "f3"))
        self.locals.run_finalizers()

        self.assertEqual(l, ["f1", "f2", "f3"])
    #-def

    def test_exception_handlers_container(self):
        self.locals.add_exception_handler(1, 2)
        self.locals.add_exception_handler(3, 4)
        self.locals.add_exception_handler(5, 6)

        self.assertEqual(
            self.locals.get_exception_handlers(), [(1, 2), (3, 4), (5, 6)]
        )
    #-def

    def test_traceback(self):
        locals = Scope(None, None)
        locals = Scope(PseudoCommand("Block", Location("f.g", 1, 1)), locals)
        locals = Scope(PseudoCommand("if", Location("f.g", 2, 1)), locals)
        locals = Frame(PseudoCommand("print", Location("f.g", 10, 11)), locals)
        locals = Scope(PseudoCommand("if", Location("tty.l", 2, 4)), locals)
        locals = Frame(PseudoCommand("write", Location("io.l", 6, 8)), locals)
        locals = Frame(PseudoCommand("_write", Location()), locals)
        locals = StackItem(PseudoCommand("add", Location("z.l", 9, 8)), locals)

        with self.assertRaises(CmdProcNameError) as eh:
            locals.getvar('a')

        self.assertEqual(str(eh.exception),
            "In _write\n" \
            "| from write\n" \
            "| from print:\n" \
            "> At [\"z.l\":9:8]: " \
            "CmdProcNameError [errcode = 258]: Undefined symbol 'a'."
        )
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestExceptionObjectCase))
    suite.addTest(unittest.makeSuite(TestExceptionsCase))
    suite.addTest(unittest.makeSuite(TestValueProviderCase))
    suite.addTest(unittest.makeSuite(TestTracebackCase))
    suite.addTest(unittest.makeSuite(TestTracebackProviderCase))
    suite.addTest(unittest.makeSuite(TestStackItemsCase))
    return suite
#-def
