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

from doit.text.pgen.readers.glap.cmd.errors import \
    CommandProcessorError, \
    CmdNameError

from doit.text.pgen.readers.glap.cmd.commands import \
    Finalizer, \
    Command

from doit.text.pgen.readers.glap.cmd.eval import \
    Environment, \
    CommandProcessor

class TLoad(Command):
    __slots__ = [ 'varname' ]

    def __init__(self, varname):
        Command.__init__(self)
        self.varname = varname
    #-def

    def enter(self, processor):
        self.env = processor.getenv()
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        processor.insertcode(self.enter, self.do_load, Finalizer(self))
    #-def

    def do_load(self, processor):
        processor.setacc(self.env.getvar(self.varname))
    #-def

    def leave(self, processor):
        processor.popcmd(self)
        self.env = None
    #-def
#-class

class TBlock(Command):
    __slots__ = [ 'cmds' ]

    def __init__(self, cmds):
        Command.__init__(self)
        self.cmds = tuple(cmds)
    #-def

    def enter(self, processor):
        self.env = Environment(processor.getenv())
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        processor.insertcode(
            *((self.enter,) + self.cmds + (Finalizer(self),))
        )
    #-def

    def leave(self, processor):
        processor.popcmd(self)
        self.env = None
    #-def
#-class

class TSet(Command):
    __slots__ = [ 'varname', 'value' ]

    def __init__(self, varname, value):
        Command.__init__(self)
        self.varname = varname
        self.value = value
    #-def

    def enter(self, processor):
        self.env = processor.getenv()
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        processor.insertcode(self.enter, self.do_set, Finalizer(self))
    #-def

    def do_set(self, processor):
        self.env.setvar(self.varname, self.value)
    #-def

    def leave(self, processor):
        processor.popcmd(self)
        self.env = None
    #-def
#-class

class TLoadEnv(Command):
    __slots__ = [ 'load_global' ]

    def __init__(self, load_global = False):
        Command.__init__(self)
        self.load_global = load_global
    #-def

    def enter(self, processor):
        if not self.load_global: 
            self.env = processor.getenv()
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        processor.insertcode(self.enter, self.do_loadenv, Finalizer(self))
    #-def

    def do_loadenv(self, processor):
        processor.setacc(processor.getenv())
    #-def

    def leave(self, processor):
        processor.popcmd(self)
        self.env = None
    #-def
#-class

class TTryCatch(Command):
    __slots__ = [ 'cmds', 'handlers' ]

    def __init__(self, cmds, handlers):
        Command.__init__(self)
        self.cmds = tuple(cmds)
        self.handlers = tuple(handlers)
    #-def

    def enter(self, processor):
        self.env = processor.getenv()
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        processor.insertcode(
            *((self.enter,) + self.cmds + (Finalizer(self),))
        )
    #-def

    def leave(self, processor):
        processor.popcmd(self)
        self.env = None
    #-def

    def find_exception_handler(self, processor, e):
        ecls = processor.find_exception(e.SID)
        if not ecls:
            
    #-def
#-class

class TestEnvironmentCase(unittest.TestCase):

    def test_vars(self):
        e1 = Environment()
        e1.setvar('x', 42)
        e2 = Environment(e1)
        e2.setvar('x', 43)
        e2.setvar('y', 44)

        self.assertEqual(e1.getvar('x'), 42)
        self.assertEqual(e2.getvar('x'), 43)
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e2.unsetvar('x')
        self.assertEqual(e1.getvar('x'), 42)
        self.assertEqual(e2.getvar('x'), 42)
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e2.unsetvar('x')
        self.assertEqual(e1.getvar('x'), 42)
        self.assertEqual(e2.getvar('x'), 42)
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e1.unsetvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('x')
        with self.assertRaises(CmdNameError):
            e2.getvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e1.unsetvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('x')
        with self.assertRaises(CmdNameError):
            e2.getvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e1.unsetvar('y')
        with self.assertRaises(CmdNameError):
            e1.getvar('x')
        with self.assertRaises(CmdNameError):
            e2.getvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e2.unsetvar('y')
        with self.assertRaises(CmdNameError):
            e1.getvar('x')
        with self.assertRaises(CmdNameError):
            e2.getvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        with self.assertRaises(CmdNameError):
            e2.getvar('y')
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e2.unsetvar('y')
        with self.assertRaises(CmdNameError):
            e1.getvar('x')
        with self.assertRaises(CmdNameError):
            e2.getvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        with self.assertRaises(CmdNameError):
            e2.getvar('y')
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e2.unsetvar('z')
        with self.assertRaises(CmdNameError):
            e1.getvar('x')
        with self.assertRaises(CmdNameError):
            e2.getvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        with self.assertRaises(CmdNameError):
            e2.getvar('y')
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e1.unsetvar('z')
        with self.assertRaises(CmdNameError):
            e1.getvar('x')
        with self.assertRaises(CmdNameError):
            e2.getvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        with self.assertRaises(CmdNameError):
            e2.getvar('y')
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        with self.assertRaises(CmdNameError):
            e2.getvar('z')

        e2.setvar('z', 7)
        with self.assertRaises(CmdNameError):
            e1.getvar('x')
        with self.assertRaises(CmdNameError):
            e2.getvar('x')
        with self.assertRaises(CmdNameError):
            e1.getvar('y')
        with self.assertRaises(CmdNameError):
            e2.getvar('y')
        with self.assertRaises(CmdNameError):
            e1.getvar('z')
        self.assertEqual(e2.getvar('z'), 7)
    #-def
#-class

class TestCommandProcessorCase(unittest.TestCase):

    def test_given_env(self):
        e = Environment()
        p = CommandProcessor(e)

        e.setvar('$$', 8)
        self.assertIsNone(p.acc())
        p.run([TLoad('$$')])
        self.assertEqual(p.acc(), 8)
    #-def

    def test_getenv(self):
        e = Environment()
        e.setvar('x', "<1>")
        p = CommandProcessor(e)

        self.assertIs(p.getenv(), e)
        p.run([TLoadEnv(True)])
        self.assertIs(p.acc(), e)
        p.run([
            TBlock([
                TSet('y', "<2>"), TLoadEnv(False)
            ])
        ])
        self.assertIsNot(p.acc(), e)
        self.assertEqual(p.acc().getvar('x'), "<1>")
        self.assertEqual(p.acc().getvar('y'), "<2>")
        with self.assertRaises(CmdNameError):
            e.getvar('y')
    #-def

    def test_cmdstack(self):
        p = CommandProcessor()
        c1 = Command()
        c2 = Command()

        with self.assertRaises(CommandProcessorError):
            p.popcmd(c1)
        p.pushcmd(c1)
        with self.assertRaises(CommandProcessorError):
            p.popcmd(c2)
        p.popcmd(c1)
        with self.assertRaises(CommandProcessorError):
            p.popcmd(c1)
    #-def

    def test_valstack(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.topval()
        with self.assertRaises(CommandProcessorError):
            p.popval()
        p.pushval(1)
        p.pushval(2)
        p.setacc(3)
        p.pushacc()
        self.assertEqual(p.topval(), 3)
        self.assertEqual(p.popval(), 3)
        self.assertEqual(p.topval(), 2)
        self.assertEqual(p.popval(), 2)
        self.assertEqual(p.topval(), 1)
        self.assertEqual(p.popval(), 1)
        with self.assertRaises(CommandProcessorError):
            p.topval()
        with self.assertRaises(CommandProcessorError):
            p.popval()
    #-def

    def test_acc(self):
        p = CommandProcessor()

        self.assertIsNone(p.acc())
        p.setacc("ax")
        self.assertEqual(p.acc(), "ax")
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEnvironmentCase))
    suite.addTest(unittest.makeSuite(TestCommandProcessorCase))
    return suite
#-def
