#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_app/test_options.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-30 18:18:42 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Application options tests.\
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

from doit.support.app.errors import \
    ApplicationError

from doit.support.app.options import \
    Option, OptionDispatcher, Options, OptionProcessor

from doit.support.app.application import \
    Application

class MyOption(Option):
    LONG_PREFIX = '/'
    KW_DELIM = ':'
    __slots__ = []

    def __init__(self, name, **kwargs):
        Option.__init__(self, name, **kwargs)
    #-def
#-class

class Log(object):
    __slots__ = [ 'content' ]

    def __init__(self):
        self.content = ""
    #-def

    def write(self, s):
        self.content += s
    #-def
#-class

class TestAppA(Application):
    __slots__ = []

    def __init__(self, **kwargs):
        Application.__init__(self, None, **kwargs)
        self.set_name('app')
        l = Log()
        self.set_output(l)
        self.set_log(l)
        self.set_error_log(l)
    #-def

    def at_start(self):
        self.define_option('halt',
            shorts = ['s'],
            cb = self.op_halt
        )
        self.define_kwoption('put',
            shorts = ['p'],
            cb = self.on_put,
            default = ""
        )
    #-def

    def main(self):
        op = self.get_option_processor()
        opts = op.get_options()
        if opts['halt'].when_given >= 0:
            self.wlog("Option processing halted.\n")
    #-def

    def op_halt(self, opt):
        self.get_option_processor().get_dispatcher().halt()
    #-def

    def on_put(self, opt):
        self.wlog("%s\n" % opt.value)
    #-def

    def handle_error(self, e):
        self.werr(e.detail)
    #-def
#-class

class TestAppB(TestAppA):
    __slots__ = []

    def __init__(self):
        TestAppA.__init__(self)
    #-def

    def at_start(self):
        self.define_option('halt',
            shorts = ['s'],
            cb = self.op_halt
        )
        self.define_kwoption('put',
            shorts = ['p'],
            cb = self.on_put,
            default = ""
        )
        self.define_option('halt',
            shorts = ['s'],
            cb = self.op_halt
        )
    #-def
#-class

class TestAppC(TestAppA):
    __slots__ = []

    def __init__(self):
        TestAppA.__init__(self)
    #-def

    def at_start(self):
        self.define_option('halt',
            shorts = ['s'],
            cb = self.op_halt
        )
        self.define_kwoption('put',
            shorts = ['p'],
            cb = self.on_put,
            default = ""
        )
        self.define_option('chalt',
            shorts = ['c', 's'],
            cb = self.op_halt
        )
    #-def
#-class

class TestAppD(TestAppA):
    __slots__ = []

    def __init__(self):
        TestAppA.__init__(self)
    #-def

    def at_start(self):
        opts = self.get_option_processor().get_options()
        self.define_option('halt',
            shorts = ['s'],
            cb = self.op_halt
        )
        self.define_kwoption('put',
            shorts = ['p'],
            cb = self.on_put,
            default = ""
        )
        del opts['tut']
        del opts['halt']
    #-def
#-class

class TestAppE(TestAppA):
    __slots__ = []

    def __init__(self):
        TestAppA.__init__(self)
    #-def

    def at_start(self):
        self.define_option('halt',
            shorts = ['s']
        )
        self.define_option('put',
            shorts = ['p']
        )
        self.define_option('lock',
            shorts = ['l']
        )
    #-def
#-class

class TestAppF(TestAppA):
    __slots__ = []

    def __init__(self):
        TestAppA.__init__(self)
    #-def

    def at_start(self):
        self.define_option('halt',
            shorts = ['s'],
            cb = self.op_halt
        )
        self.define_option('put',
            shorts = ['p'],
            flags = Option.REQUIRED
        )
        self.define_option('lock',
            shorts = ['l'],
            cb = self.op_halt_nocheck
        )
    #-def

    def op_halt_nocheck(self, opt):
        self.get_option_processor().get_dispatcher().halt()
        self.get_option_processor().get_options().disable_check()
    #-def
#-class

class TestOptionCase(unittest.TestCase):

    def test_default_values(self):
        o = Option('myopt')

        self.assertEqual(o.SHRT_PREFIX, "-")
        self.assertEqual(o.LONG_PREFIX, "--")
        self.assertEqual(o.KW_DELIM, "=")
        self.assertEqual(o.NAME_METAVAR, 'name')
        self.assertEqual(o.VALUE_METAVAR, 'value')
        self.assertEqual(o.OPTREQ_BIT_MASK, 1)
        self.assertEqual(o.OPTIONAL, 0)
        self.assertEqual(o.REQUIRED, 1)

        self.assertEqual(o.name, 'myopt')
        self.assertEqual(o.short_aliases, [])
        self.assertEqual(o.when_defined, -1)
        self.assertEqual(o.when_given, -1)
        self.assertEqual(o.about, "")
        self.assertEqual(o.about_value, "value")
        self.assertIsNone(o.action_callback(o))
        self.assertEqual(o.flags, 0)
        self.assertIsNone(o.default)
        self.assertFalse(o.has_value)
        self.assertIsNone(o.value)
    #-def

    def test_helprow(self):
        c0, c1 = Option('print', short_aliases = ['p', 't'],
            about = "prints the data to the output"
        ).helprow()
        self.assertEqual([repr(x) for x in c0], [
            "WORD('--print,')", "WORD('-p,')", "WORD('-t')"
        ])
        self.assertEqual([repr(x) for x in c1], [
            "WORD('prints')", "WORD('the')", "WORD('data')", "WORD('to')",
            "WORD('the')", "WORD('output')"
        ])

        c0, c1 = Option('jobmode', short_aliases = ['j', 'm'],
            about = "sets the `%(value)s' to the job",
            about_value = "mode", has_value = True
        ).helprow()
        self.assertEqual([repr(x) for x in c0], [
            "WORD('--jobmode=<mode>,')", "WORD('-j<mode>,')",
            "WORD('-m<mode>')"
        ])
        self.assertEqual([repr(x) for x in c1], [
            "WORD('sets')", "WORD('the')", "WORD(\"`mode'\")", "WORD('to')",
            "WORD('the')", "WORD('job')"
        ])
    #-def

    def test_is_required(self):
        self.assertFalse(Option('file').is_required())
        self.assertFalse(Option('file', flags = Option.OPTIONAL).is_required())
        self.assertTrue(Option('file', flags = Option.REQUIRED).is_required())
    #-def

    def test_reprs(self):
        self.assertEqual(Option.repr_short('f'), "-f")
        self.assertEqual(Option.repr_long('file'), "--file")
    #-def
#-class

class TestOptionProcessingCase(unittest.TestCase):

    def test_option_dispatcher_halt1(self):
        app = TestAppA()

        app.run(['--put=X', '--put=Y', '-pABC'])
        self.assertEqual(app.get_log().content, "X\nY\nABC\n")
    #-def

    def test_option_dispatcher_halt2(self):
        app = TestAppA()
        op = app.get_option_processor()
        od = op.get_dispatcher()

        app.run(['--put=X', '--put=Y', '-s', '-pUVW', '-pABC'])
        self.assertEqual(
            app.get_log().content, "X\nY\nOption processing halted.\n"
        )
        self.assertEqual(app.get_pending_args(), ['-pUVW', '-pABC'])
        self.assertFalse(od.halted())
        op.process(app.get_pending_args())
        self.assertEqual(
            app.get_log().content,
            "X\nY\nOption processing halted.\nUVW\nABC\n"
        )
        self.assertEqual(app.get_pending_args(), ['-pUVW', '-pABC'])
        self.assertFalse(od.halted())
    #-def

    def test_option_dispatcher_get_processor(self):
        app = TestAppA()

        od = app.get_option_processor().get_dispatcher()
        op = od.get_processor()

        self.assertIsInstance(op, OptionProcessor)
        self.assertIs(op, app.get_option_processor())
    #-def

    def test_option_dispatcher_dispatch_long_noopt(self):
        app = TestAppA()

        app.run(['--'])
    #-def

    def test_option_dispatcher_dispatch_long_nokey(self):
        app = TestAppA()

        app.run(['--=x'])
        self.assertEqual(
            app.get_error_log().content, "app: `--=x' - missing key"
        )
    #-def

    def test_option_dispatcher_dispatch_long_novalue(self):
        app = TestAppA()
        opts = app.get_option_processor().get_options()

        app.run(['--put='])
        self.assertIsInstance(opts['put'].value, str)
        self.assertEqual(opts['put'].value, "")
    #-def

    def test_option_dispatcher_dispatch_short_noopt(self):
        app = TestAppA()

        app.run(['-'])
    #-def

    def test_option_dispatcher_dispatch_short_unknown(self):
        app = TestAppA()

        app.run(['-x'])
        self.assertEqual(
            app.get_error_log().content, "app: Invalid option `-x'"
        )
    #-def

    def test_option_dispatcher_dispatch_short_novalue(self):
        app = TestAppA()
        opts = app.get_option_processor().get_options()

        app.run(['-p'])
        self.assertIsInstance(opts['put'].value, str)
        self.assertEqual(opts['put'].value, "")
    #-def

    def test_options_get_processor(self):
        app = TestAppA()
        op1 = app.get_option_processor()
        op2 = op1.get_options().get_processor()

        self.assertIsInstance(op1, OptionProcessor)
        self.assertIs(op1, op2)
    #-def

    def test_options_set_option_invalid_option(self):
        app = TestAppA()

        app.run(['--foo'])
        self.assertEqual(
            app.get_error_log().content, "app: Invalid option `foo'"
        )
    #-def

    def test_options_set_option_expected_option(self):
        app = TestAppA()

        app.run(['--put'])
        self.assertEqual(
            app.get_error_log().content,
            "app: `put' must be simple (not key-value) option"
        )
    #-def

    def test_options_set_kwoption_invalid_option(self):
        app = TestAppA()

        app.run(['--foo=bar'])
        self.assertEqual(
            app.get_error_log().content, "app: Invalid option `foo'"
        )
    #-def

    def test_options_set_kwoption_expected_kwoption(self):
        app = TestAppA()

        app.run(['--halt=yes'])
        self.assertEqual(
            app.get_error_log().content,
            "app: `halt' must be key-value option"
        )
    #-def

    def test_options_option_conflict(self):
        app = TestAppB()

        app.run(['--put=x'])
        self.assertEqual(
            app.get_error_log().content,
            "app: Long option `halt' is already specified"
        )
    #-def

    def test_options_alias_conflict(self):
        app = TestAppC()

        app.run(['--put=x'])
        self.assertEqual(
            app.get_error_log().content,
            "app: Short option `s' is already specified"
        )
    #-def

    def test_options_remove_defined(self):
        app1 = TestAppD()
        app2 = TestAppD()

        app1.run(['--halt'])
        app2.run(['-s'])
        self.assertEqual(
            app1.get_error_log().content,
            "app: Invalid option `halt'"
        )
        self.assertEqual(
            app2.get_error_log().content,
            "app: Invalid option `-s'"
        )
    #-def

    def test_options_remove_given(self):
        app1 = TestAppA()
        app2 = TestAppA()
        opts1 = app1.get_option_processor().get_options()
        opts2 = app2.get_option_processor().get_options()

        app1.run(['--halt'])
        app2.run(['-s'])
        halt1 = opts1['halt']
        halt2 = opts2['halt']
        self.assertTrue('halt' in opts1)
        self.assertTrue('halt' in opts2)
        self.assertEqual(halt1.when_given, 0)
        self.assertEqual(halt2.when_given, 0)
        del opts1['halt']
        del opts2['halt']
        self.assertFalse('halt' in opts1)
        self.assertFalse('halt' in opts2)
        self.assertEqual(halt1.when_given, -1)
        self.assertEqual(halt2.when_given, -1)
    #-def

    def test_options_adjust(self):
        app = TestAppE()
        opts = app.get_option_processor().get_options()

        app.run(['-lsp'])
        put = opts['put']
        self.assertEqual(put.when_defined, 1)
        self.assertEqual(put.when_given, 2)
        del opts['halt']
        self.assertEqual(put.when_defined, 0)
        self.assertEqual(put.when_given, 1)
    #-def

    def test_options_check(self):
        app1 = TestAppF()
        app2 = TestAppF()

        app1.run(['--halt'])
        app2.run(['--lock'])
        self.assertEqual(
            app1.get_error_log().content,
            "app: Required option `put' is missing"
        )
        self.assertEqual(app2.get_error_log().content, "")
    #-def

    def test_options_getters(self):
        app = TestAppF()

        app.run(['-ppp', '-l'])
        opts = app.get_option_processor().get_options()
        defined = opts.get_defined_options()
        given = opts.get_given_options()
        self.assertEqual([o.name for o in defined], ['halt', 'put', 'lock'])
        self.assertEqual([o.name for o in given], ['put', 'lock'])
    #-def

    def test_option_processor_getters(self):
        app = TestAppA()
        op = app.get_option_processor()

        self.assertIs(op.get_app(), app)
        self.assertIs(op.get_option_class(), Option)
        self.assertIs(op.get_options_class(), Options)
        self.assertIs(op.get_dispatcher_class(), OptionDispatcher)
        self.assertIs(op.get_error_class(), ApplicationError)
        self.assertIsInstance(op.get_options(), Options)
        self.assertIsInstance(op.get_dispatcher(), OptionDispatcher)
    #-def
#-class

class TestCustomOptionClassCase(unittest.TestCase):

    def test_custom_option_class(self):
        app = TestAppA(option_class = MyOption)

        app.run(['/put:ItWorks!'])
        self.assertEqual(app.get_log().content, "ItWorks!\n")
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestOptionCase))
    suite.addTest(unittest.makeSuite(TestOptionProcessingCase))
    suite.addTest(unittest.makeSuite(TestCustomOptionClassCase))
    return suite
#-def
