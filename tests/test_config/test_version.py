#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_config/test_version.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-09-10 10:24:39 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! version module tests.\
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

from doit.support.errors import DoItAssertionError
from doit.config.version import Version

class TestVersionCase(unittest.TestCase):

    def test_version_initialization(self):
        major, minor, patchlevel, date, info = 1, 2, 3, 20150910, "Final"
        v = Version(major, minor, patchlevel, date, info)

        self.assertEqual(v.major, major)
        self.assertEqual(v.minor, minor)
        self.assertEqual(v.patchlevel, patchlevel)
        self.assertEqual(v.date, date)
        self.assertEqual(v.info, info)
    #-def

    def test_version_initialization_default(self):
        v = Version()

        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patchlevel, 0)
        self.assertEqual(v.date, 0)
        self.assertEqual(v.info, "")
    #-def

    def test_version_consistency_check(self):
        # 1) v1 <  v2 && !(d1 <  d2):
        v1 = Version(1, 2, 1, 20140101, "v1")
        v2 = Version(1, 2, 2, 20140101, "v2")

        with self.assertRaises(DoItAssertionError):
            v1 == v2 # Triggers ``Version.__compare(self, rhs)``

        v1 = Version(1, 1, 1, 20140102, "v1")
        v2 = Version(1, 2, 0, 20140101, "v2")

        with self.assertRaises(DoItAssertionError):
            v1 == v2

        # 2) v1 >  v2 && !(d1 >  d2):
        v1 = Version(2, 0, 2, 20140102, "v1")
        v2 = Version(1, 0, 2, 20140102, "v2")

        with self.assertRaises(DoItAssertionError):
            v1 == v2

        v1 = Version(2, 0, 2, 20140101, "v1")
        v2 = Version(1, 0, 2, 20140102, "v2")

        with self.assertRaises(DoItAssertionError):
            v1 == v2

        # 3) v1 == v2 && !(d1 == d2):
        v1 = Version(1, 1, 0, 20150502, "v1")
        v2 = Version(1, 1, 0, 20150101, "v2")

        with self.assertRaises(DoItAssertionError):
            v1 == v2
    #-def

    def test_version_ignore_date(self):
        v1 = Version(1, 2, 3, -1, "v1")
        v2 = Version(1, 2, 3, 20140208, "v2")

        self.assertTrue(v1 == v2)
        self.assertTrue(v2 == v1)
    #-def

    def test_version_equal(self):
        v1 = Version(1, 2, 3, 20140102, "v1")
        v2 = Version(1, 2, 3, 20140102, "v2")
        v3 = Version(1, 2, 2, 20140101, "v3")

        self.assertTrue(v1 == v1)
        self.assertTrue(v1 == v2)
        self.assertTrue(v2 == v1)
        self.assertFalse(v1 == v3)
        self.assertFalse(v3 == v1)
    #-def

    def test_version_not_equal(self):
        v1 = Version(1, 0, 0, 20140301, "v1")
        v2 = Version(1, 0, 1, 20140401, "v2")
        v3 = Version(1, 0, 0, 20140301, "v3")

        self.assertFalse(v1 != v1)
        self.assertTrue(v1 != v2)
        self.assertTrue(v2 != v1)
        self.assertFalse(v1 != v3)
        self.assertFalse(v3 != v1)
    #-def

    def test_version_less_than(self):
        v1 = Version(1, 0, 0, 20141231, "v1")
        v2 = Version(1, 1, 1, 20150101, "v2")
        v3 = Version(1, 0, 0, 20141231, "v3")

        self.assertFalse(v1 < v1)
        self.assertTrue(v1 < v2)
        self.assertFalse(v2 < v1)
        self.assertFalse(v1 < v3)
        self.assertFalse(v3 < v1)
    #-def

    def test_version_greater_than(self):
        v1 = Version(3, 2, 1, 20150725, "v1")
        v2 = Version(2, 2, 0, 20150429, "v2")
        v3 = Version(3, 2, 1, 20150725, "v3")

        self.assertFalse(v1 > v1)
        self.assertTrue(v1 > v2)
        self.assertFalse(v2 > v1)
        self.assertFalse(v1 > v3)
        self.assertFalse(v3 > v1)
    #-def

    def test_version_less_or_equal(self):
        v1 = Version(1, 1, 0, 20150601, "v1")
        v2 = Version(1, 2, 1, 20150608, "v2")
        v3 = Version(1, 1, 0, 20150601, "v3")

        self.assertTrue(v1 <= v1)
        self.assertTrue(v1 <= v2)
        self.assertFalse(v2 <= v1)
        self.assertTrue(v1 <= v3)
        self.assertTrue(v3 <= v1)
    #-def

    def test_version_greater_or_equal(self):
        v1 = Version(3, 3, 3, 20150910, "v1")
        v2 = Version(2, 6, 4, 20140820, "v2")
        v3 = Version(3, 3, 3, 20150910, "v3")

        self.assertTrue(v1 >= v1)
        self.assertTrue(v1 >= v2)
        self.assertFalse(v2 >= v1)
        self.assertTrue(v1 >= v3)
        self.assertTrue(v3 >= v1)
    #-def

    def test_version_str_and_repr(self):
        v = Version(2, 1, 5, 20140301, "v")

        self.assertEqual(str(v), "2.1.5")
        self.assertEqual(
            repr(v),
            "Version(" \
                "major = 2, " \
                "minor = 1, " \
                "patchlevel = 5, " \
                "date = 20140301, " \
                "info = 'v'" \
            ")"
        )
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestVersionCase))
    return suite
#-def
