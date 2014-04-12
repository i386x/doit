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
Copyright (c) 2014 Jiří Kučera.

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
                       Collection,\
                       Input, StrInput, FileInput,\
                       Token

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
#-class

class TestInputCase(unittest.TestCase):

    def test_members(self):
        iname = '<abc>'
        input = Input(iname)
        self.assertEqual(input.name, iname)
        self.assertEqual(input.line, 0)
    #-def

    def test_methods(self):
        input = Input('<ab>')
        self.assertRaises(NotImplementedError, input.getchar)
        self.assertRaises(NotImplementedError, input.getc)
        input.ungets('xyz')
        self.assertEqual(input.getc(), 'x')
        self.assertEqual(input.getc(), 'y')
        self.assertEqual(input.getc(), 'z')
        self.assertRaises(NotImplementedError, input.getc)
    #-def
#-class

class TestStrInputCase(unittest.TestCase):

    def test_empty_string(self):
        nm = '<>'
        sinput = StrInput("", nm)
        self.assertEqual(sinput.getc(), "")
        self.assertEqual(sinput.getc(), "")
        sinput.ungets("gh")
        self.assertEqual(sinput.getc(), 'g')
        self.assertEqual(sinput.getc(), 'h')
        self.assertEqual(sinput.getc(), "")
        self.assertEqual(sinput.getc(), "")
        self.assertEqual(sinput.name, nm)
        self.assertEqual(sinput.line, 0)
    #-def

    def test_nonempty_string(self):
        name = '<mystr>'
        s = 'ab\nc\n'
        sinput = StrInput(s, name)
        self.assertEqual(sinput.getc(), 'a')
        self.assertEqual(sinput.getc(), 'b')
        self.assertEqual(sinput.getc(), '\n')
        self.assertEqual(sinput.getc(), 'c')
        sinput.ungets('xy')
        self.assertEqual(sinput.getc(), 'x')
        self.assertEqual(sinput.getc(), 'y')
        self.assertEqual(sinput.getc(), '\n')
        self.assertEqual(sinput.getc(), "")
        self.assertEqual(sinput.getc(), "")
        self.assertEqual(sinput.name, name)
        self.assertEqual(sinput.line, 0)
    #-def
#-class

class PseudoFile(object):
    __slots__ = [ 'name', 'mode', 'closed', '__fpos', '__fsize', '__content' ]

    def __init__(self, content):
        self.name = None
        self.mode = None
        self.closed = True
        self.__fpos = 0
        self.__fsize = len(content)
        self.__content = content
    #-def

    def open(self, name, mode = 'r'):
        assert mode in [ 'r', 'w' ], "PseudoFile: Bad mode."
        assert self.closed, "PseudoFile: Not closed."
        self.name = name
        self.mode = mode
        self.closed = False
        self.__fpos = 0
        if mode == 'w':
            self.__fsize = 0
            self.__content = type(self.__content)()
    #-def

    def close(self):
        assert not self.closed, "PseudoFile: Closed."
        self.closed = True
    #-def

    def read(self, size):
        assert size >= 0, "PseudoFile: Size is negative."
        assert self.mode == 'r', "PseudoFile: Mode is not for reading."
        assert not self.closed, "PseudoFile: Closed."
        assert self.__fpos <= self.__fsize,\
               "PseudoFile: File pointer value is out of range."
        s = self.__content[self.__fpos : self.__fpos + size]
        self.__fpos += len(s)
        assert self.__fpos <= self.__fsize,\
               "PseudoFile: File pointer value is out of range."
        return s
    #-def
#-class

class TestFileInputCase(unittest.TestCase):

    def setUp(self):
        self.__fobjA = PseudoFile("")
        self.__fobjB = PseudoFile("ab\nc\n")
        self.__fobjA.open('<empty>')
        self.__fobjB.open('<test>')
    #-def

    def test_empty_file(self):
        finput = FileInput(self.__fobjA)
        self.assertEqual(finput.getc(), "")
        self.assertEqual(finput.getc(), "")
        finput.ungets("gh")
        self.assertEqual(finput.getc(), 'g')
        self.assertEqual(finput.getc(), 'h')
        self.assertEqual(finput.getc(), "")
        self.assertEqual(finput.getc(), "")
        self.assertEqual(finput.name, self.__fobjA.name)
        self.assertEqual(finput.line, 0)
    #-def

    def test_nonempty_file(self):
        finput = FileInput(self.__fobjB)
        self.assertEqual(finput.getc(), 'a')
        self.assertEqual(finput.getc(), 'b')
        self.assertEqual(finput.getc(), '\n')
        self.assertEqual(finput.getc(), 'c')
        finput.ungets('xy')
        self.assertEqual(finput.getc(), 'x')
        self.assertEqual(finput.getc(), 'y')
        self.assertEqual(finput.getc(), '\n')
        self.assertEqual(finput.getc(), "")
        self.assertEqual(finput.getc(), "")
        self.assertEqual(finput.name, self.__fobjB.name)
        self.assertEqual(finput.line, 0)
    #-def

    def tearDown(self):
        self.__fobjB.close()
        self.__fobjA.close()
    #-def
#-class

class TestTokenCase(unittest.TestCase):

    def test_functionality(self):
        tt = Collection('TestTokenType')
        W, L = tt.W, tt.L
        v1, v2, v3 = 'abc', 123, (1, 2)
        l1, l2, l3 = 42, 53, 112
        t1, t2, t3 = Token(W, v1, l1), Token(L, v2, l2), Token(W, v3, l3)
        self.assertTrue(t1.type is W)
        self.assertEqual(t1.value, v1)
        self.assertEqual(t1.line, l1)
        self.assertTrue(t1 == t3)
        self.assertTrue(t1 != t2)
        self.assertEqual(repr(t1), "Token(TestTokenType.W, 'abc')")
        self.assertEqual(str(t2), "Token(TestTokenType.L, 123)")
        self.assertEqual(str(t3), "Token(TestTokenType.W, (1, 2))")
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPathConversionsCase))
    suite.addTest(unittest.makeSuite(TestCollectionCase))
    suite.addTest(unittest.makeSuite(TestInputCase))
    suite.addTest(unittest.makeSuite(TestStrInputCase))
    suite.addTest(unittest.makeSuite(TestFileInputCase))
    suite.addTest(unittest.makeSuite(TestTokenCase))
    return suite
#-def
