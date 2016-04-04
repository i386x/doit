#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/cmd/runtime.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-04-01 13:05:11 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor runtime.\
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

class ExceptionObject(object):
    """
    """
    __slots__ = []

    def __init__(self, cls, *args):
        """
        """

        self.__cls = cls
        self.__args = args
    #-def

    def cls(self):
        """
        """

        return self.__cls
    #-def

    def args(self):
        """
        """

        return self.__args
    #-def
#-class

class ExceptionClass(object):
    """
    """
    __slots__ = []

    def __init__(self, container, name, base):
        """
        """

        self.__container = container
        self.__name = name
        self.__base = base
    #-def

    def name(self):
        """
        """

        return self.__name
    #-def

    def base(self):
        """
        """

        return self.__base
    #-def

    def is_superclass_of(self, cls):
        """
        """

        if self is cls:
            return True
        if self.__base is self:
            return False
        return self.is_superclass_of(cls.base())
    #-def
#-class

class BaseExceptionClass(ExceptionClass):
    """
    """
    __slots__ = []

    def __init__(self, container):
        """
        """

        ExceptionClass.__init__(self, container, 'BaseException', self)
    #-def
#-class

class Exceptions(object):
    """
    """
    __slots__ = []

    def __init__(self, processor):
        """
        """

        self.__processor = processor
        base = BaseExceptionClass(self)
        self.__data = { base.name(): base }
    #-def

    def register_exception(self, name, basename):
        """
        """

        if name in self.__data:
            raise CmdProcRegisterExceptionError(self.__processor,
                "Exception %s is already registered" % name
            )
        if basename not in self.__data:
            raise CmdProcRegisterExceptionError(self.__processor,
                "Unknown exception base %s" % basename
            )
        self.__data[name] = ExceptionClass(self, name, self.__data[basename])
    #-def
#-class

class Traceback(list):
    """
    """
    __slots__ = []

    def __init__(self, last_command):
        """
        """

        list.__init__(self)
        _, l, c = last_command.get_location()
        if l < 0 or c < 0:
            self.__punctator = ">"
        else:
            self.__punctator = "Line %d, column %d:" % (l, c)
    #-def

    def __str__(self):
        """
        """

        if len(self) == 0:
            return "In <main>:\n"
        s = "In %s" % str(self[0])
        i = 1
        while i < len(self):
            s += "\n| from %s" % str(self[i])
            i += 1
        return "%s:\n%s" % (s, self.__punctator)
    #-def
#-class

class TracebackProvider(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def

    def traceback(self):
        """
        """

        not_implemented()
    #-def
#-class

class StackItem(TracebackProvider):
    """
    """
    __slots__ = []

    def __init__(self, cmd, prev):
        """
        """

        TracebackProvider.__init__(self)
        self.__cmd = cmd
        self.__prev = prev
        self.__finalizers = []
        self.__ehs = []
    #-def

    def get_command(self):
        """
        """

        return self.__cmd
    #-def

    def get_prev(self):
        """
        """

        return self.__prev
    #-def

    def setvar(self, name, value):
        """
        """

        self.__prev.setvar(name, value)
    #-def

    def getvar(self, name):
        """
        """

        return self.__prev.getvar(name)
    #-def

    def add_finalizer(self, finalizer):
        """
        """

        self.__finalizers.append(finalizer)
    #-def

    def run_finalizers(self):
        """
        """

        for f in self.__finalizers:
            f()
    #-def

    def add_exception_handler(self, exception, handler):
        """
        """

        self.__ehs.append((exception, handler))
    #-def

    def get_exception_handlers(self):
        """
        """

        return self.__ehs
    #-def

    def traceback(self):
        """
        """

        tb = Traceback(self.get_command())
        frame = self
        while frame:
            if isinstance(frame, Frame):
                tb.append(frame.get_command())
            frame = frame.get_prev()
        return tb
    #-def
#-class

class Scope(StackItem):
    """
    """
    __slots__ = []

    def __init__(self, cmd, prev):
        """
        """

        StackItem.__init__(self, cmd, prev)
        self.__vars = {}
    #-def

    def setvar(self, name, value):
        """
        """

        self.__vars[name] = value
    #-def

    def getvar(self, name):
        """
        """

        if name not in self.__vars:
            prev = self.get_prev()
            if prev:
                return prev.getvar(name)
            raise CmdProcUndefinedVariable(self, name)
        v = self.__vars[name]
        if isinstance(v, ArgumentProxy):
            v = v.value(self)
        return v
    #-def
#-class

class Frame(Scope):
    """
    """
    __slots__ = []

    def __init__(self, cmd, prev):
        """
        """

        Scope.__init__(self, cmd, prev)
    #-def
#-class
