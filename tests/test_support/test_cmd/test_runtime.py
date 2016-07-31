#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_cmd/test_runtime.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-04-07 18:58:51 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor's runtime module tests.\
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

from doit.support.cmd.errors import \
    CommandError

from doit.support.cmd.runtime import \
    isderived, \
    BaseIterator, \
    FiniteIterator, \
    Iterable, \
    Pair, \
    List, \
    HashMap, \
    UserType, \
    ExceptionClass, \
    Traceback, \
    Procedure

from doit.support.cmd.eval import \
    CommandProcessor

from doit.support.cmd.commands import \
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

class PseudoContext(object):
    __slots__ = [ 'cmd' ]

    def __init__(self, name, location, isfunc = True):
        self.cmd = PseudoCommand(name, location, isfunc)
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

class TestIterableCase(unittest.TestCase):

    def test_Iterable(self):
        self.assertIsInstance(Iterable().iterator(), BaseIterator)
    #-def

    def test_Pair(self):
        p = Pair(1, 2)
        q = Pair(*p)
        i = q.iterator()

        self.assertEqual(p, (1, 2))
        self.assertEqual(q, (1, 2))
        self.assertEqual(i.next(), 1)
        self.assertEqual(i.next(), 2)
        self.assertIs(i.next(), i)
    #-def

    def test_List(self):
        l = List((1, 2, 3))
        m = List(l)
        i = m.iterator()

        self.assertEqual(l, [1, 2, 3])
        self.assertEqual(m, [1, 2, 3])
        self.assertEqual(i.next(), 1)
        self.assertEqual(i.next(), 2)
        self.assertEqual(i.next(), 3)
        self.assertIs(i.next(), i)
    #-def

    def test_HashMap(self):
        d = {'a': '1', 1: 'b', "xy": 0.25}
        c = (lambda x: {1: 0, 'a': 1, "xy": 2}.get(x, -1))
        h = HashMap(d)
        hh = HashMap(h)
        i = hh.iterator()
        k = list(hh.keys())
        k.sort(key=c)
        l = []

        self.assertEqual(h, d)
        self.assertEqual(hh, d)
        x = i.next()
        self.assertTrue(x in k and x not in l)
        l.append(x)
        x = i.next()
        self.assertTrue(x in k and x not in l)
        l.append(x)
        x = i.next()
        self.assertTrue(x in k and x not in l)
        l.append(x)
        self.assertIs(i.next(), i)
        l.sort(key=c)
        self.assertEqual(l, k)
        self.assertEqual(l, [1, 'a', "xy"])
    #-def
#-class

class TestUserTypeCase(unittest.TestCase):

    def test_UserType(self):
        p = CommandProcessor()

        self.assertTrue(UserType().to_bool(p))
        with self.assertRaises(CommandError):
            UserType().to_int(p)
        with self.assertRaises(CommandError):
            UserType().to_float(p)
        with self.assertRaises(CommandError):
            UserType().to_str(p)
        with self.assertRaises(CommandError):
            UserType().to_pair(p)
        with self.assertRaises(CommandError):
            UserType().to_list(p)
        with self.assertRaises(CommandError):
            UserType().to_hash(p)
        with self.assertRaises(CommandError):
            UserType().do_visit(p, (lambda x: x), 0, 1)
    #-def
#-class

class TestExceptionClassCase(unittest.TestCase):

    def setUp(self):
        self.e0 = ExceptionClass('BaseException', '::BaseException', None)
        self.e01 = ExceptionClass('Exception', '::Exception', self.e0)
        self.e02 = ExceptionClass('SystemError', '::SystemError', self.e0)
        self.e011 = ExceptionClass('NameError', '::NameError', self.e01)
        self.e012 = ExceptionClass('TypeError', '::TypeError', self.e01)
    #-def

    def test_members(self):
        self.assertEqual(self.e0.qname, '::BaseException')
    #-def

    def test_getters(self):
        self.assertIsNone(self.e0.base())
        self.assertIsInstance(self.e01.base(), ExceptionClass)
        self.assertEqual(str(self.e01), 'Exception')
        self.assertIs(self.e011.base(), self.e01)
    #-def

    def test_isderived(self):
        self.assertTrue(isderived(self.e0, self.e0))
        self.assertTrue(isderived(self.e01, self.e0))
        self.assertTrue(isderived(self.e02, self.e0))
        self.assertTrue(isderived(self.e011, self.e0))
        self.assertTrue(isderived(self.e012, self.e0))

        self.assertTrue(isderived(self.e01, self.e01))
        self.assertTrue(isderived(self.e011, self.e01))
        self.assertTrue(isderived(self.e012, self.e01))

        self.assertTrue(isderived(self.e011, self.e011))
        self.assertTrue(isderived(self.e012, self.e012))

        self.assertTrue(isderived(self.e02, self.e02))

        self.assertFalse(isderived(self.e0, self.e01))
        self.assertFalse(isderived(self.e0, self.e02))
        self.assertFalse(isderived(self.e0, self.e011))
        self.assertFalse(isderived(self.e0, self.e012))

        self.assertFalse(isderived(self.e01, self.e011))
        self.assertFalse(isderived(self.e01, self.e012))

        self.assertFalse(isderived(self.e01, self.e02))
        self.assertFalse(isderived(self.e02, self.e01))

        self.assertFalse(isderived(self.e02, self.e011))
        self.assertFalse(isderived(self.e02, self.e012))
        self.assertFalse(isderived(self.e011, self.e02))
        self.assertFalse(isderived(self.e012, self.e02))

        self.assertFalse(isderived(self.e011, self.e012))
        self.assertFalse(isderived(self.e012, self.e011))

        self.assertFalse(isderived(self.e011, 2))
        self.assertFalse(isderived((), self.e012))
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
                stack.append(PseudoContext(cn, Location()))
            stack.append(PseudoContext("<cmd>", l, False))
            tb = Traceback(stack)
            self.assertEqual(str(tb), r)
    #-def
#-class

class TestProcedureTemplateCase(unittest.TestCase):

    def test_Procedure(self):
        name, qname, bvars, params, vararg, body, outer = \
            "proc", "::proc", ['x'], ['y', 'z'], True, [], [[]]
        proc = Procedure(name, qname, bvars, params, vararg, body, outer)

        _name, _qname, _bvars, _params, _vararg, _body, _outer = proc
        self.assertEqual(_name, name)
        self.assertEqual(_qname, qname)
        self.assertEqual(_bvars, bvars)
        self.assertEqual(_params, params)
        self.assertEqual(_vararg, vararg)
        self.assertEqual(_body, body)
        self.assertEqual(_outer, outer)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIteratorCase))
    suite.addTest(unittest.makeSuite(TestIterableCase))
    suite.addTest(unittest.makeSuite(TestUserTypeCase))
    suite.addTest(unittest.makeSuite(TestExceptionClassCase))
    suite.addTest(unittest.makeSuite(TestTracebackCase))
    suite.addTest(unittest.makeSuite(TestProcedureTemplateCase))
    return suite
#-def
