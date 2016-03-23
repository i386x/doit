#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/cmd/eval.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-14 14:41:36 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor.\
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

class CommandProcessor(object):
    """
    """
    __slots__ = [
        '__env', '__globals', '__locals', '__result', '__last_error'
    ]

    def __init__(self, env):
        """
        """

        self.__env = env
        self.reinitialize()
    #-def

    def reinitialize(self):
        """
        """

        self.__globals = Scope(None, None)
        self.__locals = self.__globals
        self.clear_state()
    #-def

    def begin_command(self, cmd):
        """
        """

        self.__locals = cmd.stackitem(self.__locals)
    #-def

    def end_command(self, cmd):
        """
        """

        last = self.__locals
        if cmd is not last.get_command():
            CmdProcRuntimeError(self, "Execution stack is corrupted")
        last.run_finalizers()
        self.__locals = last.get_prev()
        return last
    #-def

    def setlocal(self, name, value):
        """
        """

        self.__locals.setvar(name, value)
    #-def

    def getlocal(self, name):
        """
        """

        return self.__locals.getvar(name)
    #-def

    def setglobal(self, name, value):
        """
        """

        self.__globals.setvar(name, value)
    #-def

    def getglobal(self, name):
        """
        """

        return self.__globals.getvar(name)
    #-def

    def do_commands(self, commands):
        """
        """

        if self.__last_error:
            return False
        for cmd in commands:
            try:
                self.__result = self.eval_command(cmd)
            except CommandError as e:
                self.__last_error = e
                return False
        return True
    #-def

    def eval_commands(self, cmdlist):
        """
        """

        r = self.__result
        for cmd in cmdlist:
            if self.__exception:
                break
            r = self.eval_command(cmd)
        self.handle_exception()
        return r
    #-def

    def eval_command(self, cmd):
        """
        """

        self.begin_command(cmd)
        cmd.run_initializers(self)
        r = cmd.run(self)
        cmd.run_finalizers(self)
        self.end_command(cmd)
        return r
    #-def

    def result(self):
        """
        """

        return self.__result
    #-def

    def last_error(self):
        """
        """

        return self.__last_error
    #-def

    def clear_result(self):
        """
        """

        self.__result = None
    #-def

    def clear_error(self):
        """
        """

        self.__last_error = None
    #-def

    def clear_state(self):
        """
        """

        self.clear_result()
        self.clear_error()
    #-def

    def getenv(self):
        """
        """

        return self.__env
    #-def

    def commandize(self, x):
        """
        """

        # First, evaluate x:
        if isinstance(x, Command):
            x = self.eval_command(x)
        # Second, convert x to Command instance:
        if x is None:
            x = Null()
        elif isinstance(x, str):
            x = String(x)
        elif isinstance(x, int):
            x = Integer(x)
        elif not isinstance(x, Command):
            raise CmdErrBadType(self)
        # x is Command:
        return x
    #-def

    def cast(self, x, t):
        """
        """

        if isinstance(x, t):
            return x

        castrules = {
            (Null, Integer):   self.__null2int,
            (Null, String):    self.__null2str,
            (Symbol, String):  self.__sym2str,
            (Integer, Null):   self.__int2null,
            (Integer, String): self.__int2str,
            (String, Null):    self.__str2int,
            (String, Symbol):  self.__str2sym,
            (String, Integer): self.__str2int
        }
        castfunc = castrules.get(
            (self.__unify(x, (Null, Symbol, Integer, String)), t), None
        )
        x2s = lambda x: (
            x.get_name() if isinstance(x, Command) else type(x).__name__
        )
        t2s = lambda t: (
            t.__name__.lower() if issubclass(t, Command) else t.__name__
        )

        if not castfunc:
            raise CmdErrNotCastableTo(self,
                "%s is not castable to %s" % (x2s(x), t2s(t))
            )
        return castfunc(x)
    #-def

    def valueof(x, t = None):
        """
        """

        return self.cast(self.commandize(x), t) if t else self.commandize(t)
    #-def

    def evlocal(name, t = None):
        """
        """

        return self.valueof(self.getlocal(name), t)
    #-def

    def evglobal(name, t = None):
        """
        """

        return self.valueof(self.getglobal(name), t)
    #-def

    def __unify(self, x, ts):
        """
        """

        for t in ts:
            if isinstance(x, t):
                return t
        return None
    #-def

    def __null2int(self, x):
        """
        """

        return Integer(0)
    #-def

    def __null2str(self, x):
        """
        """

        return String("")
    #-def

    def __sym2str(self, x):
        """
        """

        return String(x.value())
    #-def

    def __int2null(self, x):
        """
        """

        if x.value() != 0:
            raise CmdErrNotCastableTo(self,
                "%d (integer) cannot be casted to null" % x.value()
            )
        return Null()
    #-def

    def __int2str(self, x):
        """
        """

        return String("%d" % x.value())
    #-def

    def __str2null(self, x):
        """
        """

        if x.value() != "":
            raise CmdErrNotCastableTo(self,
                "%s (string) cannot be casted to null" % repr(x.value())
            )
        return Null()
    #-def

    def __str2sym(self, x):
        """
        """

        if x.value() == "":
            raise CmdErrNotCastableTo(self,
                "Empty string cannot be converted to symbol"
            )
        return Symbol(x.value())
    #-def

    def __str2int(self, x):
        """
        """

        try:
            return int(x.value())
        except ValueError:
            raise CmdErrNotCastableTo(self,
                "%s (string) cannot be converted to integer" % repr(x.value())
            )
    #-def
#-class