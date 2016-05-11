#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/ \
#!              test_readers/test_glap/test_cmd/test_eval.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-04-18 18:07:39 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Glap reader command processor eval module tests.\
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

from ......common import StdoutMock

from doit.text.pgen.readers.glap.cmd.eval import \
    Environment, \
    CommandProcessor

class TestEnvironmentCase(unittest.TestCase):

    def test_vars(self):
        e = Environment()
        e.setvar('x', 42)

        self.assertEqual(e.getvar('x'), 42)
        self.assertIsNone(e.getvar('y'))
        e.unsetvar('y')
        self.assertEqual(e.getvar('x'), 42)
        e.unsetvar('x')
        self.assertIsNone(e.getvar('x'))
        self.assertIsNone(e.getvar('y'))
    #-def

    def test_wterm(self):
        m = "Hello!\n"
        e = Environment()

        with StdoutMock() as stdout:
            e.wterm(m)
            self.assertEqual(stdout.data, m)
    #-def
#-class

class TestCommandProcessorCase(unittest.TestCase):

    def test_x(self):
        pass
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEnvironmentCase))
    suite.addTest(unittest.makeSuite(TestCommandProcessorCase))
    return suite
#-def
