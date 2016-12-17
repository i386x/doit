#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_app/test_config.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-12-13 15:57:50 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Configuration files maintaining tests.\
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

import os
import unittest

from ...common import OPEN_FAIL, DataBuffer, make_rwopen, OpenContext, \
                      ModuleContext

from doit.support.app.application import EXIT_SUCCESS, EXIT_FAILURE

from doit.support.app.config import \
    NL, COMM, ITEM, \
    load_config, \
    set_item, get_item, del_item, \
    merge_items, config_to_kvmap, \
    save_config, \
    set_config_option, unset_config_option

cfgA = """\
pgen.quite = 1

# Default format directory:
pgen.fmtdir = ../../fmt

ignored line
 = another ignored line
  test  =  0
path =

"""
cfgA_d = [
  (ITEM, 'pgen.quite', "1"),
  (NL, ""),
  (COMM, "# Default format directory:"),
  (ITEM, 'pgen.fmtdir', "../../fmt"),
  (NL, ""),
  (COMM, "ignored line"),
  (COMM, "= another ignored line"),
  (ITEM, 'test', "0"),
  (ITEM, 'path', "")
]
cfgA_m = {
  'pgen.quite': 0,
  'pgen.fmtdir': 3,
  'test': 7,
  'path': 8
}

class OsModuleMock(ModuleContext):
    __slots__ = [
        '__old_exists', '__old_isfile'
    ]

    def __init__(self, env):
        ModuleContext.__init__(self, env)
        self.save()
    #-def

    def save(self):
        self.__old_exists = os.path.exists
        self.__old_isfile = os.path.isfile
    #-def

    def replace(self, env):
        os.path.exists = (lambda p: env[0])
        os.path.isfile = (lambda p: env[1])
    #-def

    def restore(self):
        os.path.exists = self.__old_exists
        os.path.isfile = self.__old_isfile
    #-def
#-class

class ConfigCommandMock(object):
    __slots__ = [ 'stream', 'name' ]

    def __init__(self, name):
        self.stream = ""
        self.name = name
    #-def

    def wout(self, s):
        self.stream += s
    #-def

    werr = wout

    def get_name(self):
        return self.name
    #-def
#-class

class TestLoadConfigCase(unittest.TestCase):

    def test_load_config(self):
        with OpenContext(0, cfgA, False):
            d, m = load_config("f")
        self.assertEqual(d, cfgA_d)
        self.assertEqual(m, cfgA_m)
    #-def

    def test_load_config_empty(self):
        with OpenContext(0, "", False):
            d, m = load_config("f")
        self.assertEqual(d, [])
        self.assertEqual(m, {})
    #-def

    def test_load_config_error(self):
        with OpenContext(OPEN_FAIL, cfgA_d, False):
            d, m = load_config("f")
        self.assertIsNone(d)
        self.assertIsNone(m)
    #-def
#-class

class TestSetItemCase(unittest.TestCase):

    def setUp(self):
        self.dA = [
          (COMM, "# Comment."),
          (ITEM, 'a.b', "cd")
        ]
        self.mA = {
          'a.b': 1
        }
    #-def

    def test_set_item(self):
        set_item(self.dA, self.mA, 'a.b', "ef")
        self.assertEqual(self.dA, [
            (COMM, "# Comment."),
            (ITEM, 'a.b', "ef")
        ])
        self.assertEqual(self.mA, {'a.b': 1})
        set_item(self.dA, self.mA, 'x.y', "zzz")
        self.assertEqual(self.dA, [
            (COMM, "# Comment."),
            (ITEM, 'a.b', "ef"),
            (ITEM, 'x.y', "zzz")
        ])
        self.assertEqual(self.mA, {'a.b': 1, 'x.y': 2})
        set_item(self.dA, self.mA, 'x.y', "acc")
        self.assertEqual(self.dA, [
            (COMM, "# Comment."),
            (ITEM, 'a.b', "ef"),
            (ITEM, 'x.y', "acc")
        ])
        self.assertEqual(self.mA, {'a.b': 1, 'x.y': 2})
    #-def
#-class

class TestGetItemCase(unittest.TestCase):

    def setUp(self):
        self.dA = [
          (ITEM, 'a', "asdf"),
          (ITEM, 'gh', "1258"),
          (NL, ""),
          (COMM, "#"),
          (ITEM, '56', "#4$")
        ]
        self.mA = {'a': 0, 'gh': 1, '56': 4}
    #-def

    def test_get_item(self):
        self.assertEqual(get_item(self.dA, self.mA, 'gh'), "1258")
        self.assertEqual(get_item(self.dA, self.mA, 'a'), "asdf")
        self.assertIsNone(get_item(self.dA, self.mA, 'b.c'))
        self.assertEqual(get_item(self.dA, self.mA, '56'), "#4$")
    #-def
#-class

class TestDelItemCase(unittest.TestCase):

    def setUp(self):
        self.dA = [
          (NL, ""),
          (COMM, "#"),
          (ITEM, 'a.b', "1"),
          (NL, ""),
          (ITEM, 'c.d', "23"),
          (ITEM, 'e2', "uth"),
          (ITEM, 'e2', "hut"),
          (COMM, "# $")
        ]
        self.mA = {'a.b': 2, 'c.d': 4, 'e2': 6}
    #-def

    def test_del_item(self):
        self.assertEqual(get_item(self.dA, self.mA, 'c.d'), "23")
        del_item(self.dA, self.mA, 'c.d')
        self.assertEqual(self.dA, [
            (NL, ""),
            (COMM, "#"),
            (ITEM, 'a.b', "1"),
            (NL, ""),
            (COMM, "#c.d = 23"),
            (ITEM, 'e2', "uth"),
            (ITEM, 'e2', "hut"),
            (COMM, "# $")
        ])
        self.assertEqual(self.mA, {'a.b': 2, 'e2': 6})
        self.assertIsNone(get_item(self.dA, self.mA, 'c.d'))
        del_item(self.dA, self.mA, 'R')
        self.assertEqual(self.dA, [
            (NL, ""),
            (COMM, "#"),
            (ITEM, 'a.b', "1"),
            (NL, ""),
            (COMM, "#c.d = 23"),
            (ITEM, 'e2', "uth"),
            (ITEM, 'e2', "hut"),
            (COMM, "# $")
        ])
        self.assertEqual(self.mA, {'a.b': 2, 'e2': 6})
        del_item(self.dA, self.mA, 'a.b')
        self.assertEqual(self.dA, [
            (NL, ""),
            (COMM, "#"),
            (COMM, "#a.b = 1"),
            (NL, ""),
            (COMM, "#c.d = 23"),
            (ITEM, 'e2', "uth"),
            (ITEM, 'e2', "hut"),
            (COMM, "# $")
        ])
        self.assertEqual(self.mA, {'e2': 6})
        del_item(self.dA, self.mA, 'e2')
        self.assertEqual(self.dA, [
            (NL, ""),
            (COMM, "#"),
            (COMM, "#a.b = 1"),
            (NL, ""),
            (COMM, "#c.d = 23"),
            (COMM, "#e2 = uth"),
            (COMM, "#e2 = hut"),
            (COMM, "# $")
        ])
        self.assertEqual(self.mA, {})
    #-def
#-class

class TestMergeItemsCase(unittest.TestCase):

    def setUp(self):
        self.data_1 = [
            (COMM, "# 1."),
            (ITEM, 'x', "yy"),
            (NL, ""),
            (ITEM, 'y', "123"),
            (NL, "")
        ]
        self.data_2 = [
            (NL, ""),
            (ITEM, 'x', "25l"),
            (COMM, "= []"),
            (ITEM, 'a', "iuo"),
            (NL, ""),
            (COMM, "# $.")
        ]
        self.data_12 = [
            (COMM, "# 1."),
            (ITEM, 'x', "yy"),
            (NL, ""),
            (ITEM, 'y', "123"),
            (NL, ""),
            (NL, ""),
            (ITEM, 'x', "25l"),
            (COMM, "= []"),
            (ITEM, 'a', "iuo"),
            (NL, ""),
            (COMM, "# $.")
        ]
        self.data_map_12 = {
            'x': 6, 'y': 3, 'a': 8
        }
    #-def

    def test_merge_items(self):
        r = merge_items(self.data_1, self.data_2)
        self.assertEqual(r[0], self.data_12)
        self.assertEqual(r[1], self.data_map_12)
    #-def
#-class

class TestConfigToKvMapCase(unittest.TestCase):

    def setUp(self):
        self.data = [
            (COMM, "# 1."),
            (ITEM, 'x', "yy"),
            (NL, ""),
            (ITEM, 'y', "123"),
            (NL, ""),
            (NL, ""),
            (ITEM, 'x', "25l"),
            (COMM, "= []"),
            (ITEM, 'a', "iuo"),
            (NL, ""),
            (COMM, "# $.")
        ]
        self.data_map = {
            'x': 6, 'y': 3, 'a': 8
        }
        self.kvmap = {
            'x': "25l", 'y': "123", 'a': "iuo"
        }
    #-def

    def test_config_to_kvmap(self):
        r = config_to_kvmap(self.data, self.data_map)
        self.assertEqual(r, self.kvmap)
    #-def
#-class

class TestSaveConfigCase(unittest.TestCase):

    def test_save_config(self):
        b = DataBuffer()
        with OpenContext(0, cfgA, False):
            d, m = load_config("fgh")
        del_item(d, m, 'pgen.fmtdir')
        set_item(d, m, 'pgen.quite', "0")
        set_item(d, m, 'pgen.fmtdir', "doit/meta/fmt ")
        with OpenContext(0, b, False):
            r, m = save_config("cfg", d)
        self.assertTrue(r)
        self.assertEqual(m, "")
        self.assertEqual(b.data,
            "pgen.quite = 0\n" \
            "\n" \
            "# Default format directory:\n" \
            "#pgen.fmtdir = ../../fmt\n" \
            "\n" \
            "ignored line\n" \
            "= another ignored line\n" \
            "test = 0\n" \
            "path =\n" \
            "pgen.fmtdir = doit/meta/fmt\n"
        )
    #-def

    def test_save_config_empty(self):
        b = DataBuffer()
        with OpenContext(0, b, False):
            r, m = save_config("cfg", [])
        self.assertTrue(r)
        self.assertEqual(m, "")
        self.assertEqual(b.data, "")
    #-def

    def test_save_config_fail(self):
        b = DataBuffer()
        with OpenContext(0, cfgA, False):
            d, m = load_config("fgh")
        del_item(d, m, 'pgen.fmtdir')
        set_item(d, m, 'pgen.quite', "0")
        set_item(d, m, 'pgen.fmtdir', "doit/meta/fmt ")
        with OpenContext(OPEN_FAIL, b, False):
            r, m = save_config("cfg", d)
        self.assertFalse(r)
        self.assertEqual(m, "Can't write to <cfg>")
    #-def
#-class

class TestSetConfigOptionCase(unittest.TestCase):

    def test_set_config_option_fails1(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': OPEN_FAIL
        }
        d = {
            'r': "x = y",
            'w': DataBuffer()
        }
        e = (True, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_FAILURE)
        self.assertEqual(c.stream, "config: File <conf> cannot be opened.\n")
    #-def

    def test_set_config_option_fails2(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': OPEN_FAIL
        }
        d = {
            'r': "x = y",
            'w': DataBuffer()
        }
        e = (False, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_FAILURE)
        self.assertEqual(c.stream, "config: Can't write to <conf>.\n")
    #-def

    def test_set_config_option_fails3(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': OPEN_FAIL
        }
        d = {
            'r': "x = y",
            'w': DataBuffer()
        }
        e = (True, False)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_FAILURE)
        self.assertEqual(c.stream, "config: Can't write to <conf>.\n")
    #-def

    def test_set_config_option_fails4(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': OPEN_FAIL
        }
        d = {
            'r': "x = y",
            'w': DataBuffer()
        }
        e = (False, False)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_FAILURE)
        self.assertEqual(c.stream, "config: Can't write to <conf>.\n")
    #-def

    def test_set_config_option_noconfig1(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': 0
        }
        d = {
            'r': "x = y\n1 = 2",
            'w': DataBuffer()
        }
        e = (False, False)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream,
            "config: Option 'x' in <conf> has been updated.\n"
        )
        self.assertEqual(d['w'].data, "x = z\n")
    #-def

    def test_set_config_option_noconfig2(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': 0
        }
        d = {
            'r': "x = y\n1 = 2",
            'w': DataBuffer()
        }
        e = (False, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream,
            "config: Option 'x' in <conf> has been updated.\n"
        )
        self.assertEqual(d['w'].data, "x = z\n")
    #-def

    def test_set_config_option_noconfig3(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': 0
        }
        d = {
            'r': "x = y\n1 = 2",
            'w': DataBuffer()
        }
        e = (True, False)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream,
            "config: Option 'x' in <conf> has been updated.\n"
        )
        self.assertEqual(d['w'].data, "x = z\n")
    #-def

    def test_set_config_option_save_fails1(self):
        c = ConfigCommandMock('config')
        b = {
            'r': 0,
            'w': OPEN_FAIL
        }
        d = {
            'r': "x = y\n1 = 2",
            'w': DataBuffer()
        }
        e = (True, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_FAILURE)
        self.assertEqual(c.stream, "config: Can't write to <conf>.\n")
    #-def

    def test_set_config_option_save_succeed1(self):
        c = ConfigCommandMock('config')
        b = {
            'r': 0,
            'w': 0
        }
        d = {
            'r': "x = y\n1 = 2",
            'w': DataBuffer()
        }
        e = (True, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", True)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream,
            "config: Option 'x' in <conf> has been updated.\n"
        )
        self.assertEqual(d['w'].data, "x = z\n1 = 2\n")
    #-def

    def test_set_config_option_save_succeed2(self):
        c = ConfigCommandMock('config')
        b = {
            'r': 0,
            'w': 0
        }
        d = {
            'r': "x = y\n1 = 2",
            'w': DataBuffer()
        }
        e = (True, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = set_config_option(c, "conf", 'x', "z", False)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream, "")
        self.assertEqual(d['w'].data, "x = z\n1 = 2\n")
    #-def
#-class

class TestUnsetConfigOptionCase(unittest.TestCase):

    def test_unset_config_option_fail1(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': 0
        }
        d = {
            'r': "x = y",
            'w': DataBuffer()
        }
        e = (True, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = unset_config_option(c, "conf", 'x', True)
        self.assertEqual(xc, EXIT_FAILURE)
        self.assertEqual(c.stream, "config: File <conf> cannot be opened.\n")
        self.assertEqual(d['w'].data, "")
    #-def

    def test_unset_config_option_noconfig1(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': 0
        }
        d = {
            'r': "x = y",
            'w': DataBuffer()
        }
        e = (False, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = unset_config_option(c, "conf", 'x', True)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream, "")
        self.assertEqual(d['w'].data, "")
    #-def

    def test_unset_config_option_noconfig2(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': 0
        }
        d = {
            'r': "x = y",
            'w': DataBuffer()
        }
        e = (True, False)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = unset_config_option(c, "conf", 'x', True)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream, "")
        self.assertEqual(d['w'].data, "")
    #-def

    def test_unset_config_option_noconfig3(self):
        c = ConfigCommandMock('config')
        b = {
            'r': OPEN_FAIL,
            'w': 0
        }
        d = {
            'r': "x = y",
            'w': DataBuffer()
        }
        e = (False, False)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = unset_config_option(c, "conf", 'x', True)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream, "")
        self.assertEqual(d['w'].data, "")
    #-def

    def test_unset_config_option_savefail1(self):
        c = ConfigCommandMock('config')
        b = {
            'r': 0,
            'w': OPEN_FAIL
        }
        d = {
            'r': "x = y\n1 = 2\nx = 3",
            'w': DataBuffer()
        }
        e = (True, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = unset_config_option(c, "conf", 'x', True)
        self.assertEqual(xc, EXIT_FAILURE)
        self.assertEqual(c.stream, "config: Can't write to <conf>.\n")
        self.assertEqual(d['w'].data, "")
    #-def

    def test_unset_config_option_ok1(self):
        c = ConfigCommandMock('config')
        b = {
            'r': 0,
            'w': 0
        }
        d = {
            'r': "x = y\n1 = 2\nx = 3",
            'w': DataBuffer()
        }
        e = (True, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = unset_config_option(c, "conf", 'x', True)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream,
            "config: Option 'x' in <conf> has been unset.\n"
        )
        self.assertEqual(d['w'].data, "#x = y\n1 = 2\n#x = 3\n")
    #-def

    def test_unset_config_option_ok2(self):
        c = ConfigCommandMock('config')
        b = {
            'r': 0,
            'w': 0
        }
        d = {
            'r': "x = y\n1 = 2\nx = 3",
            'w': DataBuffer()
        }
        e = (True, True)
        with OsModuleMock(e), OpenContext(b, d, False, make_rwopen):
            xc = unset_config_option(c, "conf", 'x', False)
        self.assertEqual(xc, EXIT_SUCCESS)
        self.assertEqual(c.stream, "")
        self.assertEqual(d['w'].data, "#x = y\n1 = 2\n#x = 3\n")
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLoadConfigCase))
    suite.addTest(unittest.makeSuite(TestSetItemCase))
    suite.addTest(unittest.makeSuite(TestGetItemCase))
    suite.addTest(unittest.makeSuite(TestDelItemCase))
    suite.addTest(unittest.makeSuite(TestMergeItemsCase))
    suite.addTest(unittest.makeSuite(TestConfigToKvMapCase))
    suite.addTest(unittest.makeSuite(TestSaveConfigCase))
    suite.addTest(unittest.makeSuite(TestSetConfigOptionCase))
    suite.addTest(unittest.makeSuite(TestUnsetConfigOptionCase))
    return suite
#-def
