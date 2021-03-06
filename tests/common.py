#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/common.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-02-20 13:52:05 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! tests common stuff.\
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

import sys

PYTHON_OBJECT_REPR_STR = "%s()"
PYTHON_OBJECT_REPR_STR_d = "%s(%d)"
PYTHON_OBJECT_REPR_STR_s = "%s('%s')"
PYTHON_OBJECT_REPR_STR_dd = "%s(%d, %d)"
PYTHON_OBJECT_REPR_STR_ds = "%s(%d, '%s')"
PYTHON_OBJECT_REPR_STR_sd = "%s('%s', %d)"
PYTHON_OBJECT_REPR_STR_ss = "%s('%s', '%s')"

RAISE_FROM_ENTER = 1
SUPRESS = 2

OPEN_FAIL = 1

class DataBuffer(object):
    __slots__ = [ 'data' ]

    def __init__(self):
        self.data = ""
    #-def

    def __iadd__(self, rhs):
        self.data = "%s%s" % (self.data, rhs)
        return self
    #-def
#-class

class ContextManagerMock(object):
    __slots__ = [ '__raising_strategy' ]

    def __init__(self, raising_strategy):
        self.__raising_strategy = raising_strategy
    #-def

    def __enter__(self):
        if (self.__raising_strategy & RAISE_FROM_ENTER) == RAISE_FROM_ENTER:
            raise Exception()
        return self
    #-def

    def __exit__(self, type, value, traceback):
        if (self.__raising_strategy & SUPRESS) == SUPRESS:
            return True
        return False
    #-def
#-class

class FileMock(object):
    __slots__ = [
        '__old_way', '__behaviour',
        'closed', 'name', 'mode', 'encoding', 'newline', 'data'
    ]

    def __init__(self, behaviour, name, mode, encoding, newline, data):
        self.__old_way = False
        self.__behaviour = behaviour
        self.closed = True
        self.name = name
        self.mode = mode
        self.encoding = encoding
        self.newline = newline
        self.data = data
    #-def

    def __enter__(self):
        if (self.__behaviour & OPEN_FAIL) == OPEN_FAIL:
            raise FileNotFoundError(\
                "[Errno 2] No such file or directory: '%s'" % self.name \
            )
        self.__old_way = False
        self.closed = False
        return self
    #-def

    def __exit__(self, et, ev, tb):
        assert not self.__old_way
        self.closed = True
        return False
    #-def

    def __call__(self, name, mode, encoding, newline):
        assert name == self.name
        assert mode == self.mode
        assert encoding == self.encoding
        assert newline == self.newline
        if (self.__behaviour & OPEN_FAIL) == OPEN_FAIL:
            raise FileNotFoundError(\
                "[Errno 2] No such file or directory: '%s'" % self.name\
            )
        self.__old_way = True
        self.closed = False
        return self
    #-def

    def close(self):
        assert self.__old_way
        self.closed = True
    #-def

    def read(self):
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return self.data
    #-def

    def write(self, data):
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        self.data += data
    #-def
#-class

class StderrMock(FileMock):
    __slots__ = [ '__old_stderr' ]

    def __init__(self):
        FileMock.__init__(self, 0, '<stderr>', "w", 'utf8', "")
        self.__old_stderr = sys.stderr
    #-def

    def __enter__(self):
        sys.stderr = FileMock.__enter__(self)
        return sys.stderr
    #-def

    def __exit__(self, et, ev, tb):
        sys.stderr = self.__old_stderr
        return FileMock.__exit__(self, et, ev, tb)
    #-def
#-class

class StdoutMock(FileMock):
    __slots__ = [ '__old_stdout' ]

    def __init__(self):
        FileMock.__init__(self, 0, '<stdout>', "w", 'utf8', "")
        self.__old_stdout = sys.stdout
    #-def

    def __enter__(self):
        sys.stdout = FileMock.__enter__(self)
        return sys.stdout
    #-def

    def __exit__(self, et, ev, tb):
        sys.stdout = self.__old_stdout
        return FileMock.__exit__(self, et, ev, tb)
    #-def
#-class

def make_open(behaviour, data, old_way = False):
    def open_mock(name, mode, encoding, newline):
        f = FileMock(behaviour, name, mode, encoding, newline, data)
        if old_way:
            f(name, mode, encoding, newline)
        return f
    return open_mock
#-def

def make_rwopen(behaviour, data, old_way = False):
    def rwopen_mock(name, mode, encoding, newline):
        f = FileMock(
            behaviour[mode], name, mode, encoding, newline, data[mode]
        )
        if old_way:
            f(name, mode, encoding, newline)
        return f
    return rwopen_mock
#-def

class OpenContext(object):
    __slots__ = [
        '__old_open', '__behaviour', '__data', '__old_way', '__open_factory'
    ]

    def __init__(
        self, behaviour, data, old_way = False, open_factory = make_open
    ):
        self.__old_open = __builtins__['open']
        self.__behaviour = behaviour
        self.__data = data
        self.__old_way = old_way
        self.__open_factory = open_factory
    #-def

    def __enter__(self):
        __builtins__['open'] = self.__open_factory(
            self.__behaviour, self.__data, self.__old_way
        )
        return self
    #-def

    def __exit__(self, et, ev, tb):
        __builtins__['open'] = self.__old_open
        return False
    #-def
#-class

class ModuleContext(object):
    __slots__ = [ '__env' ]

    def __init__(self, env):
        self.__env = env
    #-def

    def __enter__(self):
        self.replace(self.__env)
        return self
    #-def

    def __exit__(self, et, ev, tb):
        self.restore()
        return False
    #-def

    def replace(self, env):
        raise NotImplementedError()
    #-def

    def restore(self):
        raise NotImplementedError()
    #-def
#-class
