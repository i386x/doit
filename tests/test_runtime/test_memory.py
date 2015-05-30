#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_runtime/test_memory.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-05-28 22:57:52 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! virtual machine memory tests.\
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

import unittest

from doit.runtime.memory import Pointer, Memory

class TestPointerCase(unittest.TestCase):

    def test_pointer_initialization_offset_default(self):
        m = Memory()
        p = Pointer(m)
        self.assertIs(p.segment(), m)
        self.assertEqual(p.offset(), 0)
    #-def

    def test_pointer_initialization_offset_given(self):
        offset = 1
        m = Memory()
        p = Pointer(m, offset)
        self.assertIs(p.segment(), m)
        self.assertEqual(p.offset(), offset)
    #-def

    def test_pointer_initialization_from_pointer_offset_default(self):
        m = Memory()
        p = Pointer(Pointer(m))
        self.assertIs(p.segment(), m)
        self.assertEqual(p.offset(), 0)
    #-def

    def test_pointer_initialization_from_pointer_offset_given(self):
        offset = -1
        m = Memory()
        p = Pointer(Pointer(m, offset), offset)
        self.assertIs(p.segment(), m)
        self.assertEqual(p.offset(), offset + offset)
    #-def

    def test_read(self):
        m = Memory()
        m.sbrk(1)
        m[0] = (1, 2, 3)
        p = Pointer(m)
        self.assertIs(p.read(), m[0])
    #-def

    def test_read_fail(self):
        p = Pointer(Memory())
        with self.assertRaises(AssertionError):
            p.read()
    #-def

    def test_write(self):
        d = (1, 2, True)
        m = Memory()
        m.sbrk(1)
        p = Pointer(m)
        p.write(d)
        self.assertIs(p[0], m[0])
    #-def

    def test_write_fail(self):
        p = Pointer(Memory())
        with self.assertRaises(AssertionError):
            p.write(1)
    #-def

    def test_pointer_arithmetic_add(self):
        x, y = 2, 3
        p = Pointer(Memory(), x)
        self.assertEqual((p + y).offset(), x + y)
    #-def

    def test_pointer_arithmetic_increment(self):
        i, j = -2, 5
        p = Pointer(Memory(), i)
        p += j
        self.assertEqual(p.offset(), i + j)
    #-def

    def test_pointer_arithmetic_sub(self):
        x, y = 1, 2
        p = Pointer(Memory(), x)
        self.assertEqual((p - y).offset(), x - y)
    #-def

    def test_pointer_arithmetic_pointer_sub(self):
        x, y = 3, 7
        m = Memory()
        p, q = Pointer(m, x), Pointer(m, y)
        self.assertEqual(p - q, x - y)
        self.assertEqual(q - p, y - x)
    #-def

    def test_pointer_arithmetic_pointer_sub_fail(self):
        x, y = 3, 8
        p, q = Pointer(Memory(), x), Pointer(Memory(), y)
        with self.assertRaises(AssertionError):
            p - q
        with self.assertRaises(AssertionError):
            q - p
    #-def

    def test_pointer_arithmetic_decrement(self):
        i, j = 6, 4
        p = Pointer(Memory(), i)
        p -= j
        self.assertEqual(p.offset(), i - j)
    #-def

    def test_indexed_access_to_memory(self):
        d = dict(a = 1)
        i, j = 1, 2
        m = Memory()
        m.sbrk(4)
        p = Pointer(m, i)
        p[j] = d
        self.assertIs(m[i + j], p[j])
    #-def

    def test_indexed_access_to_memory_fail(self):
        p = Pointer(Memory())
        with self.assertRaises(AssertionError):
            p[0] = 1
        with self.assertRaises(AssertionError):
            p[1]
    #-def
#-class

class TestMemoryCase(unittest.TestCase):

    def test_memory_initialization(self):
        m = Memory()
        self.assertEqual(m.stats(), (0, 0))
    #-def

    def test_sbrk(self):
        m = Memory()
        m.sbrk(1)
        self.assertEqual(m.stats(), (1, 1))
        self.assertIsNone(m[0])
        m.sbrk(0)
        self.assertEqual(m.stats(), (0, 1))
    #-def

    def test_sbrk_fail(self):
        m = Memory()
        with self.assertRaises(AssertionError):
            m.sbrk(-1)
    #-def

    def test_conversion_to_pointer(self):
        d = dict(x = 0.5)
        m = Memory()
        m.sbrk(2)
        m[1] = d
        self.assertIs((m + 1)[0], d)
    #-def

    def test_access_to_memory(self):
        x, y = dict(x = 1), dict(y = 'a')
        m = Memory()
        m.sbrk(2)
        m[0], m[1] = x, y
        self.assertIs(m[0], x)
        self.assertIs(m[1], y)
        m.sbrk(1)
        self.assertIs(m[0], x)
        with self.assertRaises(AssertionError):
            m[1] = y
        with self.assertRaises(AssertionError):
            m[1]
    #-def

    def test_access_to_memory_bad_indicies(self):
        m = Memory()
        with self.assertRaises(AssertionError):
            m[-1] = 0
        with self.assertRaises(AssertionError):
            m[-1]
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPointerCase))
    suite.addTest(unittest.makeSuite(TestMemoryCase))
    return suite
#-def
