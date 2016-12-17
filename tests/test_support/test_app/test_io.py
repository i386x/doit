#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_app/test_io.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-09-06 11:58:46 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Application I/O services tests.\
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

from ...common import OPEN_FAIL, DataBuffer, OpenContext
from doit.support.errors import DoItNotImplementedError

from doit.support.app.application import \
    Application

from doit.support.app.io import \
    AbstractStream, CharBuffer, OutputProxy, \
    read_all, write_items

class TestAbstractStreamCase(unittest.TestCase):

    def test_AbstractStream_methods(self):
        app = Application()
        stream = AbstractStream(app)

        self.assertIs(stream.get_app(), app)
        with self.assertRaises(DoItNotImplementedError):
            stream.read()
        with self.assertRaises(DoItNotImplementedError):
            stream.write("")
        with self.assertRaises(DoItNotImplementedError):
            stream.seek(0)
        with self.assertRaises(DoItNotImplementedError):
            stream.tell()
        with self.assertRaises(DoItNotImplementedError):
            stream.size()
    #-def
#-class

class TestCharBufferCase(unittest.TestCase):

    def test_CharBuffer_methods(self):
        app = Application()
        b = CharBuffer(app)

        self.assertEqual(b.size(), 0)
        self.assertEqual(b.tell(), 0)
        self.assertEqual(b.read(), "")
        self.assertEqual(b.tell(), 0)

        b.write("abcdefgh")
        self.assertEqual(b.size(), 8)
        self.assertEqual(b.tell(), 0)

        self.assertEqual(b.read(), "abcdefgh")
        self.assertEqual(b.tell(), 8)

        b.seek(-4, 2)
        self.assertEqual(b.tell(), 4)
        self.assertEqual(b.read(2), "ef")
        self.assertEqual(b.tell(), 6)

        b.seek(0)
        self.assertEqual(b.tell(), 0)
        b.seek(0, 2)
        self.assertEqual(b.tell(), b.size())
        b.seek(3, 0)
        self.assertEqual(b.tell(), 3)
        b.seek(2, 1)
        self.assertEqual(b.tell(), 5)
        b.seek(0, 10)
        self.assertEqual(b.tell(), 5)
        b.seek(1000, 0)
        self.assertEqual(b.tell(), b.size())
        b.seek(0)
        self.assertEqual(b.tell(), 0)
        b.seek(1, 2)
        self.assertEqual(b.tell(), b.size())
        b.seek(-20, 2)
        self.assertEqual(b.tell(), 0)

        self.assertEqual(str(b), "abcdefgh")
    #-def
#-class

class TestOutputProxyCase(unittest.TestCase):

    def test_OutputProxy(self):
        app = Application()
        log1 = CharBuffer(app)
        log2 = CharBuffer(app)
        proxy1 = OutputProxy(app)
        proxy2 = OutputProxy(app, outfunc = (lambda s: log2.write(s)))

        app.set_output(log1)
        proxy1.write("ABC")
        proxy2.write("DEF")
        self.assertEqual(str(log1), "ABC")
        self.assertEqual(str(log2), "DEF")
    #-def
#-class

class TestReadAllCase(unittest.TestCase):

    def test_read_all_empty(self):
        data = ""

        with OpenContext(0, data, False):
            v = read_all("abc")
        self.assertEqual(v, "")
    #-def

    def test_read_all_nonempty(self):
        data = "abc"

        with OpenContext(0, data, False):
            v = read_all("f")
        self.assertEqual(v, data)
    #-def

    def test_read_all_error(self):
        data = "abc"

        with OpenContext(OPEN_FAIL, data, False):
            v = read_all("f")
        self.assertIsNone(v)
    #-def
#-class

class TestWriteItemsCase(unittest.TestCase):

    def test_write_items_empty(self):
        b = DataBuffer()

        with OpenContext(0, b, False):
            r = write_items("f", [], (lambda x: x))
        self.assertTrue(r)
        self.assertEqual(b.data, "")
    #-def

    def test_write_items_nonempty(self):
        b = DataBuffer()

        with OpenContext(0, b, False):
            r = write_items("f", [ 'a', 'b', "cd" ], (lambda x: x))
        self.assertTrue(r)
        self.assertEqual(b.data, "abcd")
    #-def

    def test_write_items_error(self):
        b = DataBuffer()

        with OpenContext(OPEN_FAIL, b, False):
            r = write_items("f", [ 'a', 'b', "cd" ], (lambda x: x))
        self.assertFalse(r)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAbstractStreamCase))
    suite.addTest(unittest.makeSuite(TestCharBufferCase))
    suite.addTest(unittest.makeSuite(TestOutputProxyCase))
    suite.addTest(unittest.makeSuite(TestReadAllCase))
    suite.addTest(unittest.makeSuite(TestWriteItemsCase))
    return suite
#-def
