#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/ \
#!              test_readers/test_glap/test_bootstrap/test_parser.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2017-05-15 15:16:20 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
GLAP bootstrap parser tests.\
"""

__license__ = """\
Copyright (c) 2014 - 2017 Jiří Kučera.

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

from doit.text.pgen.readers.glap.bootstrap import \
    make_location

class FakeContext(object):
    __slots__ = [ 'stream' ]

    def __init__(self):
        self.stream = None
    #-def
#-class

class FakeStream(object):
    __slots__ = [ 'context', 'name', 'data', 'pos', 'size' ]

    def __init__(self, ctx, name, s):
        ctx.stream = self
        self.context = ctx
        self.name = name
        self.data = s
        self.pos = 0
        self.size = len(s)
    #-def
#-class

name_001 = "sample_001.g"
sample_001 = """\
-- Sample grammar

module sample_001
  grammar X
    start -> "a"+;
  end
end
"""

class TestMakeLocationCase(unittest.TestCase):

    def test_make_location(self):
        ctx = FakeContext()
        stream = FakeStream(ctx, name_001, sample_001)

        self.assertEqual(make_location(ctx), (name_001, 1, 1))

        p = 26
        self.assertEqual(stream.data[p : p + 10], "sample_001")
        self.assertEqual(make_location(ctx, p), (name_001, 3, 8))

        p = 18
        stream.pos = p
        self.assertEqual(stream.data[p : p + 2], "\nm")
        self.assertEqual(make_location(ctx), (name_001, 2, 1))

        stream.pos = stream.size
        self.assertEqual(make_location(ctx), (name_001, 8, 1))
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMakeLocationCase))
    return suite
#-def
