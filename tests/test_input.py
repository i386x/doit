#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_input.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-06-28 18:44:47 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! input module tests.\
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

import unittest

from doit.input import Input

class TestInputCase(unittest.TestCase):

    def test_Input_initialization(self):
        n = "My Input"
        s = "Hello, World!"
        l = len(s)
        input = Input(n, s)
        self.assertEqual(input.name, n)
        self.assertEqual(input.offset, 0)
        self.assertEqual(input.size, l)
        self.assertEqual(input.data, s)
    #-def

    def test_Input_keeps_changes(self):
        n = "My Input"
        s = "Hello, World!"
        l = len(s)
        input = Input(n, s)
        offset = input.offset
        input.offset += l
        self.assertEqual(input.name, n)
        self.assertEqual(input.offset, offset + l)
        self.assertEqual(input.size, l)
        self.assertEqual(input.data, s)
    #-def

    def test_position(self):
        input0 = Input("", "")
        self.assertTrue(input0.offset <= input0.size)
        self.assertEqual(input0.position(), (0, 0))
        input1 = Input("", "abcdef")
        input1.offset = 3
        self.assertTrue(input1.offset <= input1.size)
        self.assertEqual(input1.position(), (0, 3))
        input1.offset = 5
        self.assertTrue(input1.offset <= input1.size)
        self.assertEqual(input1.position(), (0, 5))
        input1.offset = input1.size
        self.assertTrue(input1.offset <= input1.size)
        self.assertEqual(input1.position(), (0, input1.size))
        input2 = Input("", "\na\nb\ncd\n")
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (0, 0))
        input2.offset = 1
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (1, 0))
        input2.offset = 2
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (1, 1))
        input2.offset = 3
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (2, 0))
        input2.offset = 4
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (2, 1))
        input2.offset = 5
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (3, 0))
        input2.offset = 6
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (3, 1))
        input2.offset = 7
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (3, 2))
        input2.offset = 8
        self.assertTrue(input2.offset <= input2.size)
        self.assertEqual(input2.position(), (4, 0))
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInputCase))
    return suite
#-def
