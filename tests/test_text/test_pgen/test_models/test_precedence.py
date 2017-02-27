#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/test_models/test_precedence.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2017-02-24 15:51:05 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Precedence graph tests.\
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

from doit.support.errors import DoItAssertionError

from doit.text.pgen.models.precedence import PrecedenceGraph

class TestPrecedenceGraphCase(unittest.TestCase):

    def test_initialization(self):
        pg = PrecedenceGraph()

        self.assertEqual(pg.name_prefix(), "expr")
        self.assertEqual(pg.data(), {})
        self.assertEqual(pg.cache, {})

        pg = PrecedenceGraph("E")
        self.assertEqual(pg.name_prefix(), "E")
        self.assertEqual(pg.data(), {})
        self.assertEqual(pg.cache, {})

        with self.assertRaises(DoItAssertionError):
            PrecedenceGraph((1,))

        with self.assertRaises(DoItAssertionError):
            PrecedenceGraph("EE", (1,))

        pg = PrecedenceGraph(
            (0, (0, '+', 1)),
            (0, (0, '-', 1), "sub"),
            (1, (1, '*', 2), "mul")
        )
        self.assertEqual(pg.name_prefix(), "expr")
        self.assertEqual(pg.data(), {
            0: [
                ((0, '+', 1), None),
                ((0, '-', 1), "sub")
            ],
            1: [
                ((1, '*', 2), "mul")
            ]
        })
        self.assertEqual(pg.cache, {})

        pg = PrecedenceGraph(
            "ExprX",
            (0, (0, '+', 1)),
            (0, (0, '-', 1), "sub"),
            (1, (1, '/', 2))
        )
        self.assertEqual(pg.name_prefix(), "ExprX")
        self.assertEqual(pg.data(), {
            0: [
                ((0, '+', 1), None),
                ((0, '-', 1), "sub")
            ],
            1: [
                ((1, '/', 2), None)
            ]
        })
        self.assertEqual(pg.cache, {})
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPrecedenceGraphCase))
    return suite
#-def
