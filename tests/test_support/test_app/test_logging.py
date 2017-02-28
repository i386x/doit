#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_app/test_logging.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-09-12 12:54:27 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Logging tests.\
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

import os
import time
import unittest

from ...common import OPEN_FAIL, OpenContext, ModuleContext

from doit.support.utils import WithStatementExceptionHandler
from doit.support.app.errors import ApplicationError
from doit.support.app.io import CharBuffer
from doit.support.app.application import Application

from doit.support.app.logging import \
    StreamWrapper, Log

class Struct(object):
    __slots__ = [ '__kwargs' ]

    def __init__(self, **kwargs):
        cls = object.__getattribute__(self, '__class__')
        clsname = cls.__name__
        _ = lambda x: x.startswith('__') and '_%s%s' % (clsname, x) or x
        setattr(self, _('__kwargs'), kwargs)
    #-def

    def __getattr__(self, value):
        cls = object.__getattribute__(self, '__class__')
        clsname = cls.__name__
        _ = lambda x: x.startswith('__') and '_%s%s' % (clsname, x) or x
        kwargs = object.__getattribute__(self, _('__kwargs'))
        if value in kwargs:
            return kwargs[value]
        object.__getattribute__(self, value)
    #-def
#-class

class OsTimeModuleEnv(object):
    __slots__ = [
        'basename', 'dirname', 'realpath', 'relpath',
        'splitext', 'join', 'exists', 'isfile',
        'mkdir_raise',
        'lt_year', 'lt_month', 'lt_day',
        'lt_hour', 'lt_min', 'lt_sec',
        'lt_isdst', '_timezone',
        'dirs'
    ]

    def __init__(self):
        self.basename = (lambda x: "basename(%s)" % x)
        self.dirname = (lambda x: "dirname(%s)" % x)
        self.realpath = (lambda x: "realpath(%s)" % x)
        self.relpath = (lambda x: "relpath(%s)" % x)
        self.splitext = (lambda x: x.split('.'))
        self.join = (lambda *x: '/'.join(x))
        self.exists = []
        self.isfile = []
        self.mkdir_raise = False
        self.lt_year = 2008
        self.lt_month = 7
        self.lt_day = 11
        self.lt_hour = 21
        self.lt_min = 42
        self.lt_sec = 39
        self.lt_isdst = 1
        self._timezone = -3600
        self.dirs = []
    #-def

    def _basename(self, x):
        return self.basename(x)
    #-def

    def _dirname(self, x):
        return self.dirname(x)
    #-def

    def _realpath(self, x):
        return self.realpath(x)
    #-def

    def _relpath(self, x):
        return self.relpath(x)
    #-def

    def _splitext(self, x):
        return self.splitext(x)
    #-def

    def _join(self, *x):
        return self.join(*x)
    #-def

    def _exists(self, x):
        return x in self.exists
    #-def

    def _isfile(self, x):
        return x in self.isfile
    #-def

    def _mkdir(self, x):
        if self.mkdir_raise:
            raise OSError("mkdir(%s)" % x)
        self.dirs.append("mkdir(%s)" % x)
    #-def

    def _localtime(self):
        return Struct(
            tm_year = self.lt_year,
            tm_mon = self.lt_month,
            tm_mday = self.lt_day,
            tm_hour = self.lt_hour,
            tm_min = self.lt_min,
            tm_sec = self.lt_sec,
            tm_isdst = self.lt_isdst
        )
    #-def
#-class

class OsTimeModuleMock(ModuleContext):
    __slots__ = [
        '__old_os_path_basename',
        '__old_os_path_dirname',
        '__old_os_path_realpath',
        '__old_os_path_relpath',
        '__old_os_path_splitext',
        '__old_os_path_join',
        '__old_os_path_exists',
        '__old_os_path_isfile',
        '__old_os_mkdir',
        '__old_time_localtime',
        '__old_time_timezone'
    ]

    def __init__(self, env):
        ModuleContext.__init__(self, env)
        self.save()
    #-def

    def save(self):
        self.__old_os_path_basename = os.path.basename
        self.__old_os_path_dirname = os.path.dirname
        self.__old_os_path_realpath = os.path.realpath
        self.__old_os_path_relpath = os.path.relpath
        self.__old_os_path_splitext = os.path.splitext
        self.__old_os_path_join = os.path.join
        self.__old_os_path_exists = os.path.exists
        self.__old_os_path_isfile = os.path.isfile
        self.__old_os_mkdir = os.mkdir
        self.__old_time_localtime = time.localtime
        self.__old_time_timezone = time.timezone
    #-def

    def replace(self, env):
        self.save()
        os.path.basename = env._basename
        os.path.dirname = env._dirname
        os.path.realpath = env._realpath
        os.path.relpath = env._relpath
        os.path.splitext = env._splitext
        os.path.join = env._join
        os.path.exists = env._exists
        os.path.isfile = env._isfile
        os.mkdir = env._mkdir
        time.localtime = env._localtime
        time.timezone = env._timezone
    #-def

    def restore(self):
        os.path.basename = self.__old_os_path_basename
        os.path.dirname = self.__old_os_path_dirname
        os.path.realpath = self.__old_os_path_realpath
        os.path.relpath = self.__old_os_path_relpath
        os.path.splitext = self.__old_os_path_splitext
        os.path.join = self.__old_os_path_join
        os.path.exists = self.__old_os_path_exists
        os.path.isfile = self.__old_os_path_isfile
        os.mkdir = self.__old_os_mkdir
        time.localtime = self.__old_time_localtime
        time.timezone = self.__old_time_timezone
    #-def
#-class

class TestStreamWrapperCase(unittest.TestCase):

    def test_StreamWrapper(self):
        app = Application()
        log = CharBuffer(app)
        stream = CharBuffer(app)
        wrapper = StreamWrapper(log, stream)

        wrapper.write("A")
        wrapper.logging_on(False)
        wrapper.write("B")
        wrapper.logging_on()
        wrapper.write("C")
        with wrapper.nolog():
            wrapper.write("D")
        wrapper.write("E")
        with wrapper.log():
            wrapper.write("F")
        wrapper.write("G")

        self.assertEqual(str(stream), "ABCDEFG")
        self.assertEqual(str(log), "ACEFG")
    #-def
#-class

class TestLogCase(unittest.TestCase):

    def test_log_init1(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
        self.assertEqual(log.log_dir(), "dirname(realpath(/x/y/z.py))/log")
        self.assertEqual(log.fmode(), 'a')
        self.assertEqual(log.fencoding(), 'utf-8')
        self.assertEqual(log.fnewline(), '\n')
        self.assertIsNone(log.logfile())
    #-def

    def test_log_init2(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app, logfile_mode = 'w')
        self.assertEqual(log.fmode(), 'w')
    #-def

    def test_log_init3(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app, logfile_mode = '1')
        self.assertEqual(log.fmode(), 'a')
    #-def

    def test_wrap(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env):
            app = Application()
            app.set_path('/x/y/z.py')
            s1 = CharBuffer(app)
            s2 = CharBuffer(app)
            log = Log(app).wrap(ostream = s1, errstream = s2)
            log.ostream.write('foo')
            log.errstream.write('bar')
        self.assertIsInstance(log.ostream, StreamWrapper)
        self.assertIsInstance(log.errstream, StreamWrapper)
        self.assertEqual(str(s1), 'foo')
        self.assertEqual(str(s2), 'bar')
    #-def

    def test_log_name(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            r = log.log_name()
        self.assertEqual(r, "basename(realpath(/x/y/z-20080711.log")
    #-def

    def test_fopen_succeed(self):
        data = "Some text."
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env), OpenContext(0, data, True):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            log.fopen('x')
        fd = log.logfile()
        self.assertIsNotNone(fd)
        self.assertFalse(fd.closed)
        self.assertEqual(fd.name, "realpath(x)")
        self.assertEqual(fd.mode, "a")
        self.assertEqual(fd.encoding, "utf-8")
        self.assertEqual(fd.newline, "\n")
        self.assertEqual(fd.data, data)
    #-def

    def test_fopen_close(self):
        data = "Some text."
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env), OpenContext(0, data, True):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            log.fopen('x')
            f1 = log.logfile()
            log.fopen('y')
            f2 = log.logfile()
        self.assertIsNotNone(f1)
        self.assertIsNotNone(f2)
        self.assertTrue(f1.closed)
        self.assertFalse(f2.closed)
        self.assertEqual(f1.name, "realpath(x)")
        self.assertEqual(f2.name, "realpath(y)")
    #-def

    def test_fopen_fail(self):
        data = "Some text."
        env = OsTimeModuleEnv()
        eh = WithStatementExceptionHandler()
        with eh, OsTimeModuleMock(env), OpenContext(OPEN_FAIL, data, True):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            log.fopen('x')
        self.assertIs(eh.etype, ApplicationError)
        self.assertEqual(
            eh.evalue.detail,
            "[Errno 2] No such file or directory: 'realpath(x)'"
        )
    #-def

    def test_mkdir_not_exists(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            log.mkdir('A')
        self.assertEqual(env.dirs, ["mkdir(realpath(A))"])
    #-def

    def test_mkdir_isfile(self):
        env = OsTimeModuleEnv()
        env.exists.append("realpath(A)")
        env.isfile.append("realpath(A)")
        eh = WithStatementExceptionHandler()
        with eh, OsTimeModuleMock(env):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            log.mkdir('A')
        self.assertIs(eh.etype, ApplicationError)
        self.assertEqual(
            eh.evalue.detail, "Can't create directory 'realpath(A)'"
        )
    #-def

    def test_mkdir_isdir(self):
        env = OsTimeModuleEnv()
        env.exists.append("realpath(A)")
        with OsTimeModuleMock(env):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            log.mkdir('A')
        self.assertEqual(env.dirs, [])
    #-def

    def test_flush_on_uninitialized_file(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env), OpenContext(0, "", True):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            f1 = log.logfile()
            log.write('abc')
            log.flush()
        self.assertEqual(str(log), 'abc')
        self.assertIsNone(f1)
    #-def

    def test_flush_on_closed_file(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env), OpenContext(0, "", True):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            log.fopen('x')
            f1 = log.logfile()
            f1.close()
            log.write('abc')
            log.flush()
        self.assertEqual(str(log), 'abc')
        self.assertIsNotNone(f1)
        self.assertTrue(f1.closed)
        self.assertEqual(f1.data, "")
    #-def

    def test_logging(self):
        env = OsTimeModuleEnv()
        with OsTimeModuleMock(env), OpenContext(0, "", True):
            app = Application()
            app.set_path('/x/y/z.py')
            log = Log(app)
            log.write("Message.")
            with log as l:
                f1 = l.logfile()
                l.flush()
            f2 = log.logfile()
        self.assertEqual(env.dirs, [
            "mkdir(realpath(dirname(realpath(/x/y/z.py))/log))",
            "mkdir(realpath(%s/%s))" % (
                "dirname(realpath(/x/y/z.py))/log",
                "basename(realpath(/x/y/z"
            )
        ])
        self.assertIsNotNone(f1)
        self.assertTrue(f1.closed)
        # app_path: "realpath(/x/y/z.py)"
        # app_dir: "dirname(realpath(/x/y/z.py))"
        # log_dir: "dirname(realpath(/x/y/z.py))/log"
        # app_name: "basename(realpath(/x/y/z"
        # log_name: "basename(realpath(/x/y/z-20080711.log"
        # "realpath($log_dir/$app_name/$log_name)"
        self.assertEqual(f1.name, "realpath(%s/%s/%s)" % (
            "dirname(realpath(/x/y/z.py))/log",
            "basename(realpath(/x/y/z",
            "basename(realpath(/x/y/z-20080711.log"
        ))
        self.assertEqual(f1.data,
            "[Logged at 2008-07-11 21:42:39 (UTC+01:00, DST+01:00)]\n" \
            "Message.\n" \
            "[End of log record]\n\n"
        )
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStreamWrapperCase))
    suite.addTest(unittest.makeSuite(TestLogCase))
    return suite
#-def
