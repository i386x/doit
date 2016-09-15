#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_app/test_application.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-30 17:37:03 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Application tests.\
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

from ...common import ModuleContext

from doit.support.app.errors import \
    ApplicationError

from doit.support.app.io import \
    CharBuffer

from doit.support.app.printer import \
    PageFormatter, PageBuilder

from doit.support.app.options import \
    Option, \
    OptionProcessor

from doit.support.app.application import \
    Application

custom_app_no_args_log = """\
<start>
Application ends up with error.
<end>
"""

custom_app_help = """\
<start>
Usage: testapp <options>

where options are:

  --help, -h, -?            print this screen and exit
  --log=<message>,
  -l<message>               writes `message' into the log
  --greet=<greeting>,
  -g<greeting>              writes `greeting' to the output
  --action=<action>,
  -a<action>                performs `action'

<end>
"""

custom_app_args1 = """\
<start>
some message
Hi!
<end>
"""

custom_app_args3 = """\
<start>
abc
Hello!
<end>
"""

custom_app_args5 = """\
<start>
efgh
Hi!
Application ends up with error.
<end>
"""

custom_app_args6 = """\
<start>
efgh
Hi!
Action invoked.
<end>
"""

class OsPathMock(ModuleContext):
    __slots__ = [
        '__old_realpath',
        '__old_dirname',
        '__old_relpath'
    ]

    def __init__(self, env):
        ModuleContext.__init__(self, env)
        self.__old_realpath = os.path.realpath
        self.__old_dirname = os.path.dirname
        self.__old_relpath = os.path.relpath
    #-def

    def replace(self, env):
        def _realpath(x):
            return env[0]
        def _dirname(x):
            return env[1]
        def _relpath(x):
            return env[2]
        self.__old_realpath = os.path.realpath
        self.__old_dirname = os.path.dirname
        self.__old_relpath = os.path.relpath
        os.path.realpath = _realpath
        os.path.dirname = _dirname
        os.path.relpath = _relpath
    #-def

    def restore(self):
        os.path.realpath = self.__old_realpath
        os.path.dirname = self.__old_dirname
        os.path.relpath = self.__old_relpath
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

class CustomApp(Application):
    __slots__ = [ '__helppage' ]

    def __init__(self):
        Application.__init__(self)
        self.set_name('testapp')
        log = Log()
        self.set_output(log)
        self.set_log(log)
        self.set_error_log(log)
        self.__helppage = CharBuffer(self)
    #-def

    def at_start(self):
        self.define_option('help',
            shorts = ['h', '?'],
            cb = self.print_help,
            about = "print this screen and exit"
        )
        self.define_kwoption('log',
            shorts = ['l'],
            about = "writes `%(value)s' into the log",
            value_meta = "message",
            flags = Option.REQUIRED
        )
        self.define_kwoption('greet',
            shorts = ['g'],
            about = "writes `%(value)s' to the output",
            value_meta = "greeting",
            default = "Hi!"
        )
        self.define_kwoption('action',
            shorts = ['a'],
            about = "performs `%(value)s'",
            value_meta = "action",
            cb = self.handle_action_option,
            default = 0
        )

        helppage = PageBuilder()
        helppage.paragraph("""
        Usage:\\ %s\\ <options>
        """ % self.get_name())
        helppage.paragraph("""
        where options are:
        """)
        helppage.table(self.list_options())
        PageFormatter().format(helppage.page, self.__helppage)
        self.wlog("<start>\n")
    #-def

    def main(self):
        opts = self.get_option_processor().get_options()
        self.wlog(opts['log'].value)
        self.wlog('\n')
        self.wlog(opts['greet'].value)
        self.wlog('\n')

        a = opts['action'].value
        if a == 0:
            pass
        elif a == 1:
            self.wlog("Action invoked.\n")
        else:
            raise ApplicationError("Invalid action")
        return 0
    #-def

    def print_help(self, opt):
        self.werr(self.__helppage)
        self.exit(1)
    #-def

    def handle_action_option(self, opt):
        try:
            opt.value = int(opt.value.strip())
        except:
            opt.value = opt.default
    #-def

    def handle_error(self, e):
        self.werr("Application ends up with error.\n")
        self.set_exitcode(2)
    #-def

    def at_end(self):
        self.wlog("<end>\n")
    #-def
#-class

class TestApplicationCase(unittest.TestCase):

    def test_initialization_and_setters_getters(self):
        app = Application()
        app_ = Application(app)

        self.assertIsNone(app.get_owner())
        self.assertIs(app_.get_owner(), app)
        self.assertIsNone(app.get_name())
        app_.set_name('xcomm')
        self.assertEqual(app_.get_name(), 'xcomm')
        self.assertIs(app.get_option_processor_class(), OptionProcessor)
        self.assertIsInstance(app.get_option_processor(), OptionProcessor)
        self.assertEqual(app.get_pending_args(), [])
        self.assertEqual(app.get_exitcode(), 0)
        app_.set_exitcode(3)
        self.assertEqual(app_.get_exitcode(), 3)
        self.assertIsNone(app.get_output())
        self.assertIsNone(app.get_log())
        self.assertIsNone(app.get_error_log())
        app_.wout("Aye!")
        app_.wlog("Woof!")
        app_.werr("Meow!")
        app_.set_output(Log())
        app_.set_log(Log())
        app_.set_error_log(Log())
        app_.wout("1")
        app_.werr("2")
        app_.wlog("3")
        app_.werr("-A")
        app_.wout("+B")
        app_.wlog("*C")
        self.assertEqual(app_.get_output().content, "1+B")
        self.assertEqual(app_.get_log().content, "3*C")
        self.assertEqual(app_.get_error_log().content, "2-A")
    #-def

    def test_custom_app_path1(self):
        app = CustomApp()
        app.set_name(None)

        with OsPathMock(('C:\\X\\Y\\t.py', 'C:\\X\\Y', 'Y\\t.py')):
            app.set_path("t.py")
        self.assertEqual(app.get_name(), 'Y\\t.py')
        self.assertEqual(app.get_path(), 'C:\\X\\Y\\t.py')
        self.assertEqual(app.get_dir(), 'C:\\X\\Y')
    #-def

    def test_custom_app_path2(self):
        app = CustomApp()

        with OsPathMock(('C:\\X\\Y\\t.py', 'C:\\X\\Y', 'Y\\t.py')):
            app.set_path("t.py")
        self.assertEqual(app.get_name(), 'testapp')
        self.assertEqual(app.get_path(), 'C:\\X\\Y\\t.py')
        self.assertEqual(app.get_dir(), 'C:\\X\\Y')
    #-def

    def test_custom_app_path3(self):
        app = CustomApp()
        app.set_dir('D:\\data\\temp\\testapp')

        with OsPathMock(('C:\\X\\Y\\t.py', 'C:\\X\\Y', 'Y\\t.py')):
            app.set_path("t.py")
        self.assertEqual(app.get_name(), 'testapp')
        self.assertEqual(app.get_path(), 'C:\\X\\Y\\t.py')
        self.assertEqual(app.get_dir(), 'D:\\data\\temp\\testapp')
    #-def

    def test_custom_app_no_args(self):
        app = CustomApp()

        app.run()
        self.assertEqual(app.get_name(), 'testapp')
        self.assertEqual(app.get_log().content, custom_app_no_args_log)
        self.assertEqual(app.get_exitcode(), 2)
    #-def

    def test_custom_app_no_name1(self):
        import sys
        argv = sys.argv
        del sys
        app = CustomApp()
        app.set_name(None)

        app.run()
        self.assertEqual(app.get_name(), argv[0] if argv else "<app-name>")
    #-def

    def test_custom_app_no_name2(self):
        app = CustomApp()
        app.set_name(None)

        app.run(['script.t'])
        self.assertEqual(app.get_name(), 'script.t')
    #-def

    def test_custom_app_no_args_no_name(self):
        app = CustomApp()
        app.set_name(None)

        app.run([])
        self.assertEqual(app.get_name(), "<app-name>")
    #-def

    def test_custom_app_help1(self):
        app = CustomApp()

        app.run(['--help'])
        self.assertEqual(app.get_exitcode(), 1)
        self.assertEqual(app.get_log().content, custom_app_help)
    #-def

    def test_custom_app_help2(self):
        app = CustomApp()

        app.run(['-gu', '-h'])
        self.assertEqual(app.get_exitcode(), 1)
        self.assertEqual(app.get_log().content, custom_app_help)
    #-def

    def test_custom_app_help3(self):
        app = CustomApp()

        app.run(['-lo', '-?', '--log=ooo'])
        self.assertEqual(app.get_exitcode(), 1)
        self.assertEqual(app.get_log().content, custom_app_help)
    #-def

    def test_custom_app_args1(self):
        app = CustomApp()

        app.run(['--log=some message'])
        self.assertEqual(app.get_exitcode(), 0)
        self.assertEqual(app.get_log().content, custom_app_args1)
    #-def

    def test_custom_app_args2(self):
        app = CustomApp()

        app.run(['-lsome message'])
        self.assertEqual(app.get_exitcode(), 0)
        self.assertEqual(app.get_log().content, custom_app_args1)
    #-def

    def test_custom_app_args3(self):
        app = CustomApp()

        app.run(['--greet=Hello!', '-labc'])
        self.assertEqual(app.get_exitcode(), 0)
        self.assertEqual(app.get_log().content, custom_app_args3)
    #-def

    def test_custom_app_args4(self):
        app = CustomApp()

        app.run(['-gHello!', '-labc'])
        self.assertEqual(app.get_exitcode(), 0)
        self.assertEqual(app.get_log().content, custom_app_args3)
    #-def

    def test_custom_app_args5(self):
        app = CustomApp()

        app.run(['--action=1', '-a2', '-lefgh'])
        self.assertEqual(app.get_exitcode(), 2)
        self.assertEqual(app.get_log().content, custom_app_args5)
    #-def

    def test_custom_app_args6(self):
        app = CustomApp()
        app.set_name(None)

        app.run(['gterm', '--action=1', '-lefgh', 'build', '-zgt'])
        self.assertEqual(app.get_name(), 'gterm')
        self.assertEqual(app.get_pending_args(), ['build', '-zgt'])
        self.assertEqual(app.get_exitcode(), 0)
        self.assertEqual(app.get_log().content, custom_app_args6)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestApplicationCase))
    return suite
#-def
