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

from doit.support.errors import not_implemented

from doit.text.pgen.readers.glap.cmd.errors import \
    CmdProcNameError, \
    CmdProcContainerError

class ExceptionObject(object):
    """
    """
    __slots__ = [ '__cls', '__args' ]

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
    __slots__ = [ '__container', '__name', '__base' ]

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

        if not isinstance(cls, ExceptionClass):
            return False
        if cls.name() not in self.__container:
            return False
        if self.__container[cls.name()] is not cls:
            return False
        if self is cls:
            return True
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

        ExceptionClass.__init__(self, container, 'BaseException', None)
    #-def
#-class

class Exceptions(dict):
    """
    """
    __slots__ = [ '__processor' ]

    def __init__(self, processor):
        """
        """

        dict.__init__(self)
        self.__processor = processor
        base = BaseExceptionClass(self)
        self[base.name()] = base
    #-def

    def register_exception(self, name, basename):
        """
        """

        if name in self:
            raise CmdProcContainerError(self.__processor,
                "Exception %s is already registered" % name
            )
        if basename not in self:
            raise CmdProcContainerError(self.__processor,
                "Unknown exception base %s" % basename
            )
        self[name] = ExceptionClass(self, name, self[basename])
    #-def

    def register_exceptions(self, *specs):
        """
        """

        for name, basename in specs:
            self.register_exception(name, basename)
    #-def
#-class

class ValueProvider(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def

    def value(self, processor):
        """
        """

        not_implemented()
    #-def
#-class

class Traceback(list):
    """
    """
    __slots__ = [ '__punctator' ]

    def __init__(self, last_command):
        """
        """

        list.__init__(self)
        self.__punctator = ">"
        if last_command:
            f, l, c = last_command.get_location()
            if f is not None and l >= 0 and c >= 0:
                self.__punctator += " At [\"%s\":%d:%d]:" % (f, l, c)
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
    __slots__ = [ '__cmd', '__prev', '__finalizers', '__ehs' ]

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

    def unsetvar(self, name):
        """
        """

        self.__prev.unsetvar(name)
    #-def

    def getvar(self, name, first = None):
        """
        """

        if first is None:
            first = self
        return self.__prev.getvar(name, first)
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
    __slots__ = [ '__vars' ]

    def __init__(self, cmd, prev):
        """
        """

        StackItem.__init__(self, cmd, prev)
        self.bind(cmd.bounded_scope(), cmd.bounded_vars())
        self.__vars = {}
    #-def

    def bind(self, scope, bounded_vars = None):
        """
        """

        self.__outer_scope = scope
        if bounded_vars is None:
            bounded_vars = scope.getvars()
        self.__bounded_vars = bounded_vars
    #-def

    def outer_scope(self):
        """
        """

        return self.__outer_scope
    #-def

    def bounded_vars(self):
        """
        """

        return self.__bounded_vars
    #-def

    def setvar(self, name, value):
        """
        """

        self.__vars[name] = value
    #-def

    def unsetvar(self, name):
        """
        """

        if name in self.__vars:
            del self.__vars[name]
    #-def

    def getvar(self, name, first = None):
        """
        """

        # The stack item with the command that requested the variable (this is
        # in fact the topmost stack item).
        if first is None:
            first = self
        # Try to find the requested variable in this scope first.
        v = self.getval(name)
        if v is None:
            scope = self
            # The variable is not in this scope. Try to find it in bounded
            # scopes.
            while scope is not None:
                if name in scope.bounded_vars():
                    break
                scope = scope.outer_scope()
            if scope is None:
                # The requested variable has been never defined.
                raise CmdProcNameError(first, "Undefined symbol '%s'" % name)
            v = scope.outer_scope().getval(name)
            if v is None:
                # The requested variable has been defined but now it is
                # deleted.
                raise CmdProcNameError(first, "Undefined symbol '%s'" % name)
        return v
    #-def

    def getvars(self):
        """
        """

        return list(self.__vars.keys())
    #-def

    def getval(self, name):
        """
        """

        v = self.__vars.get(name, None)
        if isinstance(v, ValueProvider):
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
