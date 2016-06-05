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
    CommandError

from doit.text.pgen.readers.glap.cmd.runtime import \
    isderived, \
    Pair, \
    List, \
    HashMap, \
    ExceptionClass

from doit.text.pgen.readers.glap.cmd.eval import \
    Environment, \
    CommandProcessor

from doit.text.pgen.readers.glap.cmd.commands import \
    Finalizer, \
    Command

class LoggingEnv(Environment):
    __slots__ = []

    def __init__(self, processor = None, outer = None):
        Environment.__init__(self, processor, outer)
    #-def

    def wlog(self, processor, msg):
        processor.log.append(msg)
    #-def
#-class

class LoggingProcessor(CommandProcessor):
    __slots__ = [ 'log' ]

    def __init__(self, env = None):
        CommandProcessor.__init__(self, env)
        self.log = []
    #-def
#-class

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

class TStore(Command):
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
        processor.insertcode(self.enter, self.do_store, Finalizer(self))
    #-def

    def do_store(self, processor):
        self.env.setvar(self.varname, processor.acc())
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
        self.env = processor.envclass()(processor, processor.getenv())
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

class TLogBlock(TBlock):
    __slots__ = [ 'i' ]

    def __init__(self, i, cmds):
        TBlock.__init__(self, cmds)
        self.i = i
    #-def

    def enter(self, processor):
        self.env = processor.envclass()(processor, processor.getenv())
        processor.pushcmd(self)
        self.env.wlog(processor, "<%d>" % self.i)
    #-def

    def leave(self, processor):
        processor.popcmd(self)
        self.env.wlog(processor, "</%d>" % self.i)
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

class TThrow(Command):
    __slots__ = [ 'ename', 'emsg' ]

    def __init__(self, ename, emsg):
        Command.__init__(self)
        self.ename = ename
        self.emsg = emsg
    #-def

    def expand(self, processor):
        processor.insertcode(self.do_throw)
    #-def

    def do_throw(self, processor):
        ecls = processor.getenv().getvar(self.ename)
        if not isinstance(ecls, ExceptionClass):
            raise CommandError(processor.TypeError,
                "Only exception objects can be throwed"
            )
        processor.insertcode(CommandError(ecls, self.emsg))
    #-def
#-class

class TTryCatch(Command):
    __slots__ = [ 'cmds', 'handlers' ]

    def __init__(self, cmds, handlers):
        Command.__init__(self)
        self.cmds = tuple(cmds)
        self.handlers = handlers
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

    def find_exception_handler(self, e):
        try:
            if not (
                isinstance(e, CommandError)
                and isinstance(e.ecls, ExceptionClass)
            ):
                return None
            for name, handler in self.handlers:
                ec = self.env.getvar(name)
                if isderived(e.ecls, ec):
                    return handler
            return None
        except CommandError as ce:
            return [ce]
    #-def
#-class

class TDefError(Command):
    __slots__ = [ 'ename', 'ebasename' ]

    def __init__(self, name, basename):
        Command.__init__(self)
        self.ename = name
        self.ebasename = basename
    #-def

    def expand(self, processor):
        processor.insertcode(self.do_deferror)
    #-def

    def do_deferror(self, processor):
        processor.define_exception(self.ename, self.ebasename)
    #-def
#-class

class TestEnvironmentCase(unittest.TestCase):

    def test_vars(self):
        p = CommandProcessor()
        e1 = Environment(p)
        e1.setvar('x', 42)
        e2 = Environment(outer = e1)
        e2.setprocessor(p)
        e2.setvar('x', 43)
        e2['y'] = 44

        self.assertEqual(e1.getvar('x'), 42)
        self.assertEqual(e2.getvar('x'), 43)
        with self.assertRaises(CommandError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e2.unsetvar('x')
        self.assertEqual(e1.getvar('x'), 42)
        self.assertEqual(e2.getvar('x'), 42)
        with self.assertRaises(CommandError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e2.unsetvar('x')
        self.assertEqual(e1.getvar('x'), 42)
        self.assertEqual(e2.getvar('x'), 42)
        with self.assertRaises(CommandError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e1.unsetvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('x')
        with self.assertRaises(CommandError):
            e2.getvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e1.unsetvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('x')
        with self.assertRaises(CommandError):
            e2.getvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e1.unsetvar('y')
        with self.assertRaises(CommandError):
            e1.getvar('x')
        with self.assertRaises(CommandError):
            e2.getvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('y')
        self.assertEqual(e2.getvar('y'), 44)
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e2.unsetvar('y')
        with self.assertRaises(CommandError):
            e1.getvar('x')
        with self.assertRaises(CommandError):
            e2.getvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('y')
        with self.assertRaises(CommandError):
            e2.getvar('y')
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e2.unsetvar('y')
        with self.assertRaises(CommandError):
            e1.getvar('x')
        with self.assertRaises(CommandError):
            e2.getvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('y')
        with self.assertRaises(CommandError):
            e2.getvar('y')
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e2.unsetvar('z')
        with self.assertRaises(CommandError):
            e1.getvar('x')
        with self.assertRaises(CommandError):
            e2.getvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('y')
        with self.assertRaises(CommandError):
            e2.getvar('y')
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e1.unsetvar('z')
        with self.assertRaises(CommandError):
            e1.getvar('x')
        with self.assertRaises(CommandError):
            e2.getvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('y')
        with self.assertRaises(CommandError):
            e2.getvar('y')
        with self.assertRaises(CommandError):
            e1.getvar('z')
        with self.assertRaises(CommandError):
            e2.getvar('z')

        e2.setvar('z', 7)
        with self.assertRaises(CommandError):
            e1.getvar('x')
        with self.assertRaises(CommandError):
            e2.getvar('x')
        with self.assertRaises(CommandError):
            e1.getvar('y')
        with self.assertRaises(CommandError):
            e2.getvar('y')
        with self.assertRaises(CommandError):
            e1.getvar('z')
        self.assertEqual(e2.getvar('z'), 7)
    #-def
#-class

class TestCommandProcessorCase(unittest.TestCase):

    def test_constants(self):
        p = CommandProcessor()

        self.assertIs(p.Null, p)
        self.assertIsNone(p.BaseException.base())
        self.assertEqual(str(p.BaseException), 'BaseException')
        self.assertIs(p.Exception.base(), p.BaseException)
        self.assertEqual(str(p.Exception), 'Exception')
        self.assertIs(p.NameError.base(), p.Exception)
        self.assertEqual(str(p.NameError), 'NameError')
        self.assertIs(p.TypeError.base(), p.Exception)
        self.assertEqual(str(p.TypeError), 'TypeError')
        self.assertIs(p.ValueError.base(), p.Exception)
        self.assertEqual(str(p.ValueError), 'ValueError')
        self.assertIs(p.IndexError.base(), p.Exception)
        self.assertEqual(str(p.IndexError), 'IndexError')
        self.assertIs(p.KeyError.base(), p.Exception)
        self.assertEqual(str(p.KeyError), 'KeyError')
        with self.assertRaises(CommandProcessorError):
            p.Uvw
    #-def

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
        with self.assertRaises(CommandError):
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

    def test_run(self):
        p = CommandProcessor()

        p.run([True])
        self.assertIs(p.acc(), True)
        p.run([False])
        self.assertIs(p.acc(), False)
        p.run([1])
        self.assertEqual(p.acc(), 1)
        p.run([1.25])
        self.assertEqual(p.acc(), 1.25)
        p.run(["abc"])
        self.assertEqual(p.acc(), "abc")
        p.run([Pair(3, 7)])
        self.assertIsInstance(p.acc(), Pair)
        self.assertEqual(p.acc(), (3, 7))
        p.run([List("xyz")])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [ 'x', 'y', 'z' ])
        p.run([HashMap({'a': 0.5, 1: 'x'})])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {'a': 0.5, 1: 'x'})
        p.run([(2, 5)])
        self.assertIsInstance(p.acc(), Pair)
        self.assertEqual(p.acc(), (2, 5))
        with self.assertRaises(CommandProcessorError):
            p.run([()])
        with self.assertRaises(CommandProcessorError):
            p.run([(1,)])
        with self.assertRaises(CommandProcessorError):
            p.run([(1, 3, -1)])
        with self.assertRaises(CommandProcessorError):
            p.run([(1, 3, -1, 0.25)])
        p.run([[1, 2, 3]])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [1, 2, 3])
        p.run([{0.5: "cc", -4: (1,), ('a', 3): 0.25}])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {0.5: "cc", -4: (1,), ('a', 3): 0.25})
        p.run([None])
        self.assertIs(p.acc(), p.Null)
        p.run([p.Null])
        self.assertIs(p.acc(), p.Null)
        with self.assertRaises(CommandProcessorError):
            p.run([CommandProcessor()])
    #-def

    def test_exception_handling(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([TLoad('?'), TSet('x', -1)])

        with self.assertRaises(CommandProcessorError):
            p.run([TLoad('?'), Command(), Command(), Command()])

        p.run([
            TTryCatch([
                TLoad('?')
            ], [
                ('TypeError', [TSet('et', 1)]),
                ('NameError', [TSet('et', 2)])
            ])
        ])
        self.assertEqual(p.getenv().getvar('et'), 2)

        p.run([
            TTryCatch([
                TLoad('?')
            ], [
                ('BaseException', [TSet('et', 0)]),
                ('TypeError', [TSet('et', 1)]),
                ('NameError', [TSet('et', 2)])
            ])
        ])
        self.assertEqual(p.getenv().getvar('et'), 0)

        with self.assertRaises(CommandProcessorError):
            p.run([
                TTryCatch([
                    TLoad('?')
                ], [
                    ('_TypeError', [TSet('et', 1)]),
                    ('NameError', [TSet('et', 2)])
                ])
            ])

        p.run([
            TTryCatch([
                TLoad('?')
            ], [
                ('NameError', [TSet('et', 3)]),
                ('_NameError', [TSet('et', 4)])
            ])
        ])
        self.assertEqual(p.getenv().getvar('et'), 3)

        p.run([
            TTryCatch([
                TTryCatch([
                    TLoad('?')
                ], [
                    ('TypeError', [TSet('et', 5)]),
                    ('_Error', [TSet('et', 6)])
                ])
            ], [
                ('NameError', [TSet('et', 7)])
            ])
        ])
        self.assertEqual(p.getenv().getvar('et'), 7)

        with self.assertRaises(CommandProcessorError):
            p.run([
                TTryCatch([
                    TTryCatch([
                        TLoad('?')
                    ], [
                        ('TypeError', [TSet('et', 5)]),
                        ('_Error', [TSet('et', 6)])
                    ])
                ], [
                    ('TypeError', [TSet('et', 7)])
                ])
            ])

        with self.assertRaises(CommandProcessorError):
            p.run([
                TTryCatch([
                    TLoad('?'), Finalizer(Command())
                ], [
                    ('NameError', [])
                ])
            ])
    #-def

    def test_cleanup(self):
        le = LoggingEnv()
        p = LoggingProcessor(le)

        try:
            p.pushval(0)
            p.pushval(7)
            p.setacc('z')
            p.run([
                TLogBlock(1, [
                    TLogBlock(2, [
                        CommandProcessor(),
                        TSet('x', 'y'),
                        CommandProcessor(),
                        TSet('x', 'y')
                    ]),
                    TSet('x', 'y')
                ]),
                TSet('x', 'y')
            ])
        except CommandProcessorError:
            pass
        self.assertEqual(p.log, [ "<1>", "<2>" ])
        self.assertEqual(p.popval(), 7)
        self.assertEqual(p.popval(), 0)
        with self.assertRaises(CommandProcessorError):
            p.popval()
        self.assertEqual(p.acc(), 'z')

        le = LoggingEnv()
        p = LoggingProcessor(le)

        try:
            p.pushval(0)
            p.pushval(7)
            p.setacc('z')
            p.run([
                TLogBlock(1, [
                    TLogBlock(2, [
                        CommandProcessor(),
                        TSet('x', 'y'),
                        CommandProcessor(),
                        TSet('x', 'y')
                    ]),
                    TSet('x', 'y')
                ]),
                TSet('x', 'y')
            ])
        except CommandProcessorError:
            p.cleanup()
        self.assertEqual(p.log, [ "<1>", "<2>", "</2>", "</1>" ])
        with self.assertRaises(CommandProcessorError):
            p.popval()
        self.assertIsNone(p.acc())
    #-def

    def test_define_exception(self):
        m = "Oook!"
        p = CommandProcessor()
        env = p.getenv()

        p.run([
            TDefError('MyError', 'Exception'),
            TTryCatch([
                TThrow('MyError', m)
            ], [
                ('MyError', [TStore('x')])
            ])
        ])
        self.assertIs(env.getvar('x').ecls, env.getvar('MyError'))
        self.assertEqual(env.getvar('x').emsg, m)

        p.run([
            TTryCatch([
                TDefError('MySecondError', 'u')
            ], [
                ('NameError', [TSet('x', 42)])
            ])
        ])
        self.assertEqual(env.getvar('x'), 42)

        p.run([
            TTryCatch([
                TDefError('MySecondError', 'x')
            ], [
                ('TypeError', [TSet('x', 43)])
            ])
        ])
        self.assertEqual(env.getvar('x'), 43)

        p.run([
            TDefError('E', 'Exception'),
            TBlock([
                TDefError('E', 'Exception'),
                TLoad('E')
            ]),
            TStore('X'),
            TTryCatch([
                TThrow('E', "1")
            ], [
                ('X', [TSet('a', 11)]),
                ('E', [TSet('a', 12)])
            ]),
            TTryCatch([
                TThrow('X', "2")
            ], [
                ('E', [TSet('b', 13)]),
                ('X', [TSet('b', 14)])
            ])
        ])
        self.assertEqual(env.getvar('a'), 12)
        self.assertEqual(env.getvar('b'), 14)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestEnvironmentCase))
    suite.addTest(unittest.makeSuite(TestCommandProcessorCase))
    return suite
#-def
