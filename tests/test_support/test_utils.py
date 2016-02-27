#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_utils.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-04-10 20:58:24 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! utilities tests.\
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

from ..common import RAISE_FROM_ENTER, SUPRESS, ContextManagerMock

from doit.support.errors import DoItAssertionError
from doit.support.utils import WithStatementExceptionHandler, Collection

class TestWithStatementExceptionHandlerCase(unittest.TestCase):

    def test_what_happen_when_exception_is_not_raised(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(0)

        with wseh, ctxmock:
            pass

        self.assertIsNone(wseh.etype)
        self.assertIsNone(wseh.evalue)
        self.assertIsNone(wseh.etraceback)
    #-def

    def test_what_happen_when_exception_is_raised_from_enter(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(RAISE_FROM_ENTER)

        with wseh, ctxmock:
            pass

        self.assertIsNotNone(wseh.etype)
        self.assertIsNotNone(wseh.evalue)
        self.assertIsNotNone(wseh.etraceback)
    #-def

    def test_what_happen_when_exception_is_raised_within_block(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(0)

        with wseh, ctxmock:
            raise Exception()

        self.assertIsNotNone(wseh.etype)
        self.assertIsNotNone(wseh.evalue)
        self.assertIsNotNone(wseh.etraceback)
    #-def

    def test_what_happen_when_exception_is_not_raised_and_supressed(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(SUPRESS)

        with wseh, ctxmock:
            pass

        self.assertIsNone(wseh.etype)
        self.assertIsNone(wseh.evalue)
        self.assertIsNone(wseh.etraceback)
    #-def

    def test_what_happen_when_exception_is_raised_and_supressed(self):
        wseh = WithStatementExceptionHandler()
        ctxmock = ContextManagerMock(SUPRESS)

        with wseh, ctxmock:
            raise Exception()

        self.assertIsNone(wseh.etype)
        self.assertIsNone(wseh.evalue)
        self.assertIsNone(wseh.etraceback)
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

        self.assertIs(a, b)
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.qname, b.qname)
        self.assertIsNot(a, c)
        self.assertNotEqual(a.name, c.name)
        self.assertNotEqual(a.qname, c.qname)
        self.assertIsNot(d, e)
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
        self.assertIs(Apple, Food.Apple)
        self.assertIs(Orange, Food.Orange)
        self.assertIs(Banana, Food.Banana)
        self.assertIs(Carrot, Food.Carrot)
        self.assertIs(Potato, Food.Potato)
        self.assertIs(Tomato, Food.Tomato)
        self.assertIs(Chedar, Food.Chedar)
        self.assertIs(ProceededChedar, Food.Proceeded)
        self.assertIs(Food.Chedar.Proceeded, Food.Proceeded)
        self.assertIs(Ementaler, Food.Ementaler)
    #-def

    def test_contains_operator(self):
        A = Collection("A")
        B = Collection("@")

        self.assertNotIn(A, B)
        self.assertNotIn(B, A)
        self.assertIn(A, A)
        self.assertIn(B, B)
        self.assertIn(A.B, A)
        self.assertNotIn(A.B, A.C)
        self.assertIn(B.C.D.S, B.C)
        self.assertNotIn(B, B.A)
        self.assertNotIn(A.BCEF.G, A.BCE)
        self.assertIn(A.BCE.G, A.BCE)
    #-def

    def test_lock(self):
        with self.assertRaises(DoItAssertionError):
            Collection.lock()
            T = Collection("T")
        with self.assertRaises(DoItAssertionError):
            Collection.unlock()
            T = Collection("T")
            Collection.lock()
            t = T.Test
    #-def

    def test_unlock(self):
        Collection.lock()
        Collection.unlock()
        Test = Collection("Test")
        t = Test.Test1
    #-def

    def tearDown(self):
        Collection.unlock()
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWithStatementExceptionHandlerCase))
    suite.addTest(unittest.makeSuite(TestCollectionCase))
    return suite
#-def
