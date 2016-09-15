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

import time
import unittest

from ..common import RAISE_FROM_ENTER, SUPRESS, ContextManagerMock, \
                     ModuleContext

from doit.support.errors import DoItAssertionError

from doit.support.utils import \
    ordinal_suffix, timestamp, WithStatementExceptionHandler, Collection

class Struct(object):
    __slots__ = [ '__kwargs' ]

    def __init__(self, **kwargs):
        cls = object.__getattribute__(self, '__class__')
        clsname = cls.__name__
        _ = lambda x: x.startswith('__') and '_%s%s' % (clsname, x) or x
        setattr(self, _('__kwargs'), kwargs)
    #-def

    def __getattr__(self, value):
        cls = object.__getattribute__(self, '__class__')
        clsname = cls.__name__
        _ = lambda x: x.startswith('__') and '_%s%s' % (clsname, x) or x
        kwargs = object.__getattribute__(self, _('__kwargs'))
        if value in kwargs:
            return kwargs[value]
        object.__getattribute__(self, value)
    #-def
#-class

class TimeModuleMock(ModuleContext):
    __slots__ = [
        '__old_localtime',
        '__old_timezone'
    ]

    def __init__(self, env):
        ModuleContext.__init__(self, env)
        self.__old_localtime = time.localtime
        self.__old_timezone = time.timezone
    #-def

    def replace(self, env):
        def _localtime():
            return Struct(
                tm_year = env['year'],
                tm_mon = env['month'],
                tm_mday = env['day'],
                tm_hour = env['hour'],
                tm_min = env['min'],
                tm_sec = env['sec'],
                tm_isdst = env['isdst']
            )
        self.__old_localtime = time.localtime
        self.__old_timezone = time.timezone
        time.localtime = _localtime
        time.timezone = env['tz']
    #-def

    def restore(self):
        time.localtime = self.__old_localtime
        time.timezone = self.__old_timezone
    #-def
#-class

class TestOrdinalSuffixCase(unittest.TestCase):

    def test_ordinal_suffix(self):
        cases = [
            (0, 'th'),
            (1, 'st'),
            (2, 'nd'),
            (3, 'rd'),
            (4, 'th'),
            (5, 'th'),
            (10, 'th'),
            (11, 'th'),
            (12, 'th'),
            (13, 'th'),
            (14, 'th'),
            (15, 'th'),
            (20, 'th'),
            (21, 'st'),
            (22, 'nd'),
            (23, 'rd'),
            (24, 'th'),
            (25, 'th'),
            (30, 'th'),
            (31, 'st'),
            (32, 'nd'),
            (33, 'rd'),
            (34, 'th'),
            (35, 'th'),
            (50, 'th'),
            (51, 'st'),
            (52, 'nd'),
            (53, 'rd'),
            (54, 'th'),
            (55, 'th'),
            (90, 'th'),
            (91, 'st'),
            (92, 'nd'),
            (93, 'rd'),
            (94, 'th'),
            (95, 'th')
        ]
        bases = [0, 100, 1000, 10000, 1000000]

        for b in bases:
            for c in cases:
                self.assertEqual(ordinal_suffix(b + c[0]), c[1])
                self.assertEqual(ordinal_suffix(-(b + c[0])), c[1])
    #-def
#-class

class TestTimeStampCase(unittest.TestCase):

    def test_dst(self):
        env = dict(
            year = 2008, month = 7, day = 11,
            hour = 13, min = 15, sec = 34,
            isdst = 1, tz = -5378
        )
        with TimeModuleMock(env):
            t = timestamp()
        self.assertEqual(t['year'], 2008)
        self.assertEqual(t['month'], 7)
        self.assertEqual(t['day'], 11)
        self.assertEqual(t['hour'], 13)
        self.assertEqual(t['min'], 15)
        self.assertEqual(t['sec'], 34)
        self.assertEqual(t['utcsign'], '+')
        self.assertEqual(t['utchour'], 1)
        self.assertEqual(t['utcmin'], 29)
        self.assertEqual(t['utcsec'], 38)
        self.assertEqual(t['dsthour'], 1)
        self.assertEqual(t['dstmin'], 0)
        self.assertEqual(t['dstsec'], 0)
    #-def

    def test_nodst(self):
        env = dict(
            year = 2008, month = 11, day = 11,
            hour = 13, min = 15, sec = 34,
            isdst = 0, tz = 5378
        )
        with TimeModuleMock(env):
            t = timestamp()
        self.assertEqual(t['year'], 2008)
        self.assertEqual(t['month'], 11)
        self.assertEqual(t['day'], 11)
        self.assertEqual(t['hour'], 13)
        self.assertEqual(t['min'], 15)
        self.assertEqual(t['sec'], 34)
        self.assertEqual(t['utcsign'], '-')
        self.assertEqual(t['utchour'], 1)
        self.assertEqual(t['utcmin'], 29)
        self.assertEqual(t['utcsec'], 38)
        self.assertEqual(t['dsthour'], 0)
        self.assertEqual(t['dstmin'], 0)
        self.assertEqual(t['dstsec'], 0)
    #-def

    def test_dst_not_avail(self):
        env = dict(
            year = 2008, month = 7, day = 11,
            hour = 13, min = 15, sec = 34,
            isdst = -1, tz = 14400
        )
        with TimeModuleMock(env):
            t = timestamp()
        self.assertEqual(t['year'], 2008)
        self.assertEqual(t['month'], 7)
        self.assertEqual(t['day'], 11)
        self.assertEqual(t['hour'], 13)
        self.assertEqual(t['min'], 15)
        self.assertEqual(t['sec'], 34)
        self.assertEqual(t['utcsign'], '-')
        self.assertEqual(t['utchour'], 4)
        self.assertEqual(t['utcmin'], 0)
        self.assertEqual(t['utcsec'], 0)
        self.assertEqual(t['dsthour'], 0)
        self.assertEqual(t['dstmin'], 0)
        self.assertEqual(t['dstsec'], 0)
    #-def
#-class

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
    suite.addTest(unittest.makeSuite(TestOrdinalSuffixCase))
    suite.addTest(unittest.makeSuite(TestTimeStampCase))
    suite.addTest(unittest.makeSuite(TestWithStatementExceptionHandlerCase))
    suite.addTest(unittest.makeSuite(TestCollectionCase))
    return suite
#-def
