#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_utils.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-04-10 20:58:24 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! utilities tests.\
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

import os
import unittest

from doit.utils import sys2path, path2sys,\
                       WithStatementExceptionHandler,\
                       doit_read,\
                       Collection

RAISE_FROM_ENTER = 1
SUPRESS = 2

class ContextManagerMock(object):
    __slots__ = [ '__raising_strategy' ]

    def __init__(self, raising_strategy):
        self.__raising_strategy = raising_strategy
    #-def

    def __enter__(self):
        if (self.__raising_strategy & RAISE_FROM_ENTER) == RAISE_FROM_ENTER:
            raise Exception()
        return self
    #-def

    def __exit__(self, type, value, traceback):
        if (self.__raising_strategy & SUPRESS) == SUPRESS:
            return True
        return False
    #-def
#-class

OPEN_FAIL = 1

class FileMock(object):
    __slots__ = [\
        '__behaviour', 'closed', 'name', 'mode', 'encoding', '__data'\
    ]

    def __init__(self, behaviour, name, mode, encoding, data):
        self.__behaviour = behaviour
        self.closed = True
        self.name = name
        self.mode = mode
        self.encoding = encoding
        self.__data = data
    #-def

    def __enter__(self):
        if (self.__behaviour & OPEN_FAIL) == OPEN_FAIL:
            raise FileNotFoundError(\
                "[Errno 2] No such file or directory: '%s'" % self.name\
            )
        self.closed = False
        return self
    #-def

    def __exit__(self, et, ev, tb):
        self.closed = True
        return False
    #-def

    def read(self):
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return self.__data
    #-def
#-class

def make_open(behaviour, data):
    def open_mock(name, mode, encoding):
        return FileMock(behaviour, name, mode, encoding, data)
    return open_mock
#-def

class TestPathConversionsCase(unittest.TestCase):

    def test_sys2path(self):
        ts = [
          ('', ""),
          ("a", "a"),
          ("a.b", "a.b"),
          (".a", ".a"),
          ("b.", "b."),
          (os.path.join('', ''), ""),
          (os.path.join('a', ''), "a/"),
          (os.path.join('', 'a'), "a"),
          (os.path.join('a', 'b'), "a/b"),
          (os.path.join(os.curdir, 'a', 'b', 'd.e'), "./a/b/d.e"),
          (os.path.join('a', 'b', os.pardir, 'c', 'd.e'), "a/b/../c/d.e")
        ]
        for i, o in ts:
            self.assertTrue(sys2path(i) == o)
    #-def

    def test_path2sys(self):
        ts = [
          ('', ""),
          ("a", "a"),
          ("a.b", "a.b"),
          (".a", ".a"),
          ("b.", "b."),
          ("/", ""),
          ("a/", os.path.join('a', '')),
          ("/a", "a"),
          ("a/b", os.path.join('a', 'b')),
          ("./", ""),
          ("./a", "a"),
          ("./.a", ".a"),
          ("./a.", "a."),
          ("./a.b", "a.b"),
          ("./a/b", os.path.join('a', 'b')),
          ("./a/b/", os.path.join('a', 'b', '')),
          ("a/b/./../c.d", os.path.join(
            'a', 'b', os.curdir, os.pardir, 'c.d'
          )),
          ("./a/b/../../d/./e.c", os.path.join(
            'a', 'b', os.pardir, os.pardir, 'd', os.curdir, 'e.c'
          ))
        ]
        for i, o in ts:
            self.assertTrue(path2sys(i) == o)
    #-def
#-class

class TestWithStatementExceptionHandlerCase(unittest.TestCase):

    def test_what_happen_when_exception_is_not_raised(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(0)
        with wseh, ctxmock:
            pass
        self.assertTrue(wseh.etype is None)
        self.assertTrue(wseh.evalue is None)
        self.assertTrue(wseh.etraceback is None)
    #-def

    def test_what_happen_when_exception_is_raised_from_enter(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(RAISE_FROM_ENTER)
        with wseh, ctxmock:
            pass
        self.assertFalse(wseh.etype is None)
        self.assertFalse(wseh.evalue is None)
        self.assertFalse(wseh.etraceback is None)
    #-def

    def test_what_happen_when_exception_is_raised_within_block(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(0)
        with wseh, ctxmock:
            raise Exception()
        self.assertFalse(wseh.etype is None)
        self.assertFalse(wseh.evalue is None)
        self.assertFalse(wseh.etraceback is None)
    #-def

    def test_what_happen_when_exception_is_not_raised_and_supressed(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(SUPRESS)
        with wseh, ctxmock:
            pass
        self.assertTrue(wseh.etype is None)
        self.assertTrue(wseh.evalue is None)
        self.assertTrue(wseh.etraceback is None)
    #-def

    def test_what_happen_when_exception_is_raised_and_supressed(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(SUPRESS)
        with wseh, ctxmock:
            raise Exception()
        self.assertTrue(wseh.etype is None)
        self.assertTrue(wseh.evalue is None)
        self.assertTrue(wseh.etraceback is None)
    #-def
#-class

class TestDoItReadCase(unittest.TestCase):

    def test_reading_from_existing_file(self):
        old_open = __builtins__['open']
        data = "some data"
        __builtins__['open'] = make_open(0, data)
        s = doit_read("<foo>")
        __builtins__['open'] = old_open
        self.assertEqual(s, data)
    #-def

    def test_reading_from_nonexisting_file(self):
        old_open = __builtins__['open']
        data = "some data"
        __builtins__['open'] = make_open(OPEN_FAIL, data)
        s = doit_read("<foo>")
        __builtins__['open'] = old_open
        self.assertTrue(s is None)
    #-def
#-class

class TestCollectionCase(unittest.TestCase):

    def test_create_unique_objects(self):
        a = Collection('MyColl1')
        self.assertEqual(a.name, 'MyColl1')
        self.assertEqual(a.qname, 'MyColl1')
        b = Collection('MyColl1')
        self.assertEqual(b.name, 'MyColl1')
        self.assertEqual(b.qname, 'MyColl1')
        c = Collection('MyColl2')
        self.assertEqual(c.name, 'MyColl2')
        self.assertEqual(c.qname, 'MyColl2')
        d = Collection()
        e = Collection()
        self.assertTrue(a is b)
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.qname, b.qname)
        self.assertFalse(a is c)
        self.assertNotEqual(a.name, c.name)
        self.assertNotEqual(a.qname, c.qname)
        self.assertFalse(d is e)
        self.assertNotEqual(d.name, e.name)
        self.assertNotEqual(d.qname, e.qname)
    #-def

    def test_create_subobjects(self):
        Fruit = Collection('Fruit')
        self.assertEqual(Fruit.name, 'Fruit')
        self.assertEqual(Fruit.qname, 'Fruit')
        Apple = Fruit.Apple
        self.assertEqual(Apple.name, 'Apple')
        self.assertEqual(Apple.qname, 'Fruit.Apple')
        Orange = Fruit.Orange
        self.assertEqual(Orange.name, 'Orange')
        self.assertEqual(Orange.qname, 'Fruit.Orange')
        Banana = Fruit.Banana
        self.assertEqual(Banana.name, 'Banana')
        self.assertEqual(Banana.qname, 'Fruit.Banana')
        Vegetable = Collection('Vegetable')
        self.assertEqual(Vegetable.name, 'Vegetable')
        self.assertEqual(Vegetable.qname, 'Vegetable')
        Carrot = Vegetable.Carrot
        self.assertEqual(Carrot.name, 'Carrot')
        self.assertEqual(Carrot.qname, 'Vegetable.Carrot')
        Potato = Vegetable.Potato
        self.assertEqual(Potato.name, 'Potato')
        self.assertEqual(Potato.qname, 'Vegetable.Potato')
        Tomato = Vegetable.Tomato
        self.assertEqual(Tomato.name, 'Tomato')
        self.assertEqual(Tomato.qname, 'Vegetable.Tomato')
        Dairy = Collection('Dairy')
        self.assertEqual(Dairy.name, 'Dairy')
        self.assertEqual(Dairy.qname, 'Dairy')
        Cheese = Dairy.Cheese
        self.assertEqual(Cheese.name, 'Cheese')
        self.assertEqual(Cheese.qname, 'Dairy.Cheese')
        Chedar = Cheese.Chedar
        self.assertEqual(Chedar.name, 'Chedar')
        self.assertEqual(Chedar.qname, 'Dairy.Cheese.Chedar')
        ProceededChedar = Chedar.Proceeded
        self.assertEqual(ProceededChedar.name, 'Proceeded')
        self.assertEqual(
          ProceededChedar.qname, 'Dairy.Cheese.Chedar.Proceeded'
        )
        Ementaler = Cheese.Ementaler
        self.assertEqual(Ementaler.name, 'Ementaler')
        self.assertEqual(Ementaler.qname, 'Dairy.Cheese.Ementaler')
        Food = Collection(
          'Food', 'Fruit', 'Vegetable', 'Dairy.Cheese.Chedar', 'Dairy.Cheese'
        )
        self.assertEqual(Food.name, 'Food')
        self.assertEqual(Food.qname, 'Food')
        self.assertTrue(Apple is Food.Apple)
        self.assertTrue(Orange is Food.Orange)
        self.assertTrue(Banana is Food.Banana)
        self.assertTrue(Carrot is Food.Carrot)
        self.assertTrue(Potato is Food.Potato)
        self.assertTrue(Tomato is Food.Tomato)
        self.assertTrue(Chedar is Food.Chedar)
        self.assertTrue(ProceededChedar is Food.Proceeded)
        self.assertTrue(Ementaler is Food.Ementaler)
    #-def

    def test_contains_operator(self):
        A = Collection("A")
        B = Collection("@")
        self.assertFalse(A in B)
        self.assertFalse(B in A)
        self.assertTrue(A in A)
        self.assertTrue(B in B)
        self.assertTrue(A.B in A)
        self.assertFalse(A.B in A.C)
        self.assertTrue(A.B not in A.C)
        self.assertTrue(B.C.D.S in B.C)
        self.assertFalse(B in B.A)
        self.assertFalse(A.BCEF.G in A.BCE)
        self.assertTrue(A.BCE.G in A.BCE)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPathConversionsCase))
    suite.addTest(unittest.makeSuite(TestCollectionCase))
    suite.addTest(unittest.makeSuite(TestWithStatementExceptionHandlerCase))
    suite.addTest(unittest.makeSuite(TestDoItReadCase))
    return suite
#-def
