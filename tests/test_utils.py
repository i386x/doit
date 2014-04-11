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

from doit.utils import sys2path, path2sys

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPathConversionsCase))
    return suite
#-def
