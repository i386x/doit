#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/ \
#!              test_readers/test_glap/test_cmd/test_commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-05-10 13:16:59 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Glap reader command processor commands module tests.\
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

from doit.text.pgen.readers.glap.cmd.commands import \
    Location, \
    Command

from doit.text.pgen.readers.glap.cmd.eval import \
    Environment, \
    CommandProcessor

class TEnv(Environment):
    __slots__ = [ 'data' ]

    def __init__(self):
        Environment.__init__(self)
        self.data = []
    #-def

    def wterm(self, s):
        self.data.append(s)
    #-def
#-class

class Relax(Command):
    __slots__ = []

    def __init__(self):
        Command.__init__(self)
    #-def
#-class

class Compute(Command):
    __slots__ = []

    def __init__(self, code, *args):
        Command.__init__(self)
        self.set_name('exec')
        self.set_location("num.l", 33, 4)
        self.set_argspec('code')
        self.add_argspec(Arguments.ELLIPSIS)
        self.set_args(code)
        self.add_args(*args)
        self.atstart(self.__logon)
        self.atexit(self.__logoff)
    #-def

    def help(self, processor):
        processor.getenv().wterm("Usage: exec <code> [data]\n")
    #-def

    def run(self, processor):
        code = processor.valueof('code')
    #-def

    def __logon(self, processor):
        processor.getenv().wterm("exec: logged on\n")
    #-def

    def __logoff(self, processor):
        processor.getenv().wterm("exec: logged off\n")
    #-def
#-class

class TestLocationCase(unittest.TestCase):

    def test_methods(self):
        loc0 = Location()
        loc1 = Location("A", 1, 2)

        self.assertIsNone(loc0.file())
        self.assertEqual(loc0.line(), -1)
        self.assertEqual(loc0.column(), -1)
        self.assertEqual(loc0, (None, -1, -1))
        x, y, z = loc0
        self.assertEqual((x, y, z), (None, -1, -1))
        self.assertEqual(str(loc0), "(internal)")

        self.assertEqual(loc1.file(), "A")
        self.assertEqual(loc1.line(), 1)
        self.assertEqual(loc1.column(), 2)
        self.assertEqual(loc1, ("A", 1, 2))
        x, y, z = loc1
        self.assertEqual((x, y, z), ("A", 1, 2))
        self.assertEqual(str(loc1), 'at ["A":1:2]')
    #-def
#-class

class TestCommandCase(unittest.TestCase):

    def test_simple_command(self):
        e = TEnv()
        p = CommandProcessor(e)
        relax = Relax()

        self.assertEqual(relax.get_name(), 'relax')
        self.assertEqual(relax.get_location(), (None, -1, -1))
        self.assertEqual("%s" % relax, '"relax" (internal)')
        self.assertEqual(relax.get_args(), [])
        relax.help(p)
        self.assertIs(relax.run(p), relax)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLocationCase))
    suite.addTest(unittest.makeSuite(TestCommandCase))
    return suite
#-def
