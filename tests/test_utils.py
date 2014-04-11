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
                       Input, StrInput, FileInput

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPathConversionsCase))
    suite.addTest(unittest.makeSuite(TestInputCase))
    suite.addTest(unittest.makeSuite(TestStrInputCase))
    suite.addTest(unittest.makeSuite(TestFileInputCase))
    return suite
#-def
