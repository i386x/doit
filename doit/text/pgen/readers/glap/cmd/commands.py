#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/cmd/commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-14 15:36:02 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Possible commands to be processed by command processor.\
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

from doit.text.pgen.readers.glap.cmd.errors import \
    CmdProcArgumentsError

from doit.text.pgen.readers.glap.cmd.runtime import \
    ValueProvider, \
    StackItem

class Location(tuple):
    """
    """
    __slots__ = []

    def __new__(cls, file = None, line = -1, column = -1):
        """
        """

        return super(Location, cls).__new__(cls, (file, line, column))
    #-def

    def __init__(self, file = None, line = -1, column = -1):
        """
        """

        tuple.__init__(self)
    #-def

    def file(self):
        """
        """

        return self[0]
    #-def

    def line(self):
        """
        """

        return self[1]
    #-def

    def column(self):
        """
        """

        return self[2]
    #-def

    def __str__(self):
        """
        """

        f, l, c = self
        if f is None or l < 0 or c < 0:
            return "(internal)"
        return "at [\"%s\":%d:%d]" % self
    #-def
#-class

class Command(object):
    """
    """
    __slots__ = [
        '__name', '__location', '__arguments', '__initializers', '__finalizers'
    ]

    def __init__(self):
        """
        """

        self.__name = self.__class__.__name__.lower()
        self.__location = Location()
        self.__initializers = []
        self.__finalizers = []
        self.__outer = None
        self.__vars = {}
    #-def

    def set_name(self, name):
        """
        """

        self.__name = name
    #-def

    def get_name(self):
        """
        """

        return self.__name
    #-def

    def set_location(self, file = None, line = -1, column = -1):
        """
        """

        self.__location = Location(file, line, column)
    #-def

    def get_location(self):
        """
        """

        return self.__location
    #-def

    def __str__(self):
        """
        """

        return "\"%s\" %s" % (self.__name, self.__location)
    #-def

    def setvar(self, name, value):
        """
        """

        self.__vars[name] = value
    #-def

    def getvar(self, name, top = None):
        """
        """

        if top is None:
            top = self
        if name in self.__vars:
            return self.__vars[name]
        if self.__outer:
            return self.__outer.getvar(name, top)
        raise CmdProcNameError(top, "Undefined symbol '%s'" % name)
    #-def

    def setenv(self, env):
        """
        """

        self.__vars = env
    #-def

    def getenv(self):
        """
        """

        return self.__vars
    #-def

    def atstart(self, *inits):
        """
        """

        self.__initializers.extend(inits)
    #-def

    def atexit(self, *finits):
        """
        """

        self.__finalizers.extend(finits)
    #-def

    def bind(self, outer):
        """
        """

        self.__outer = outer
    #-def

    def outer(self):
        """
        """

        return self.__outer
    #-def

    def help(self, processor):
        """
        """

        pass
    #-def

    def run(self, processor):
        """
        """

        return self.result()
    #-def

    def run_initializers(self, processor):
        """
        """

        for i in self.__initializers:
            i(processor)
    #-def

    def run_finalizers(self, processor):
        """
        """

        for f in self.__finalizers:
            f(processor)
    #-def
#-class

class Eval(Command):
    """
    """
    CODE = 0
    __slots__ = []

    def __init__(self, code, env = {}):
        """
        """

        Command.__init__(self)
        self.setenv(env)
        self.bind(None)
        self.setvar(self.__class__.CODE, code)
    #-def

    def run(self, processor):
        """
        """

        processor.push(self.getvar(self.__class__.CODE))
    #-def
#-class

class If(Command):
    """
    """
    __slots__ = []

    def __init__(self, *args):
        """
        """

        Command.__init__(self)
        self.setvar(self.__class__.ARGS, args)
    #-def

    def run(self, processor):
        """
        """

        processor.pushcode(
            self.getvar(self.__class__.IF),
            self.__if
        )
    #-def

    def __if(self, processor):
        """
        """

        c = processor.popval()
        if c:
            processor.pushcode(self.getvar(self.__class__.THEN))
        else:
            processor.pushcode(self.getvar(self.__class__.ELSE))
    #-def
#-class

class Value(Command):
    """
    """
    __slots__ = [ '__value' ]

    def __init__(self):
        """
        """

        Command.__init__(self)
        self.set_argspec()
        self.set_args()
        self.__value = None
    #-def

    def setval(self, v):
        """
        """

        self.__value = v
    #-def

    def value(self):
        """
        """

        return self.__value
    #-def

    def clone(self):
        """
        """

        new = self.__class__()
        new.setval(self.__value)
        return new
    #-def
#-class

class Null(Value):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Value.__init__(self)
    #-def
#-class

class Symbol(Value):
    """
    """
    __slots__ = []

    def __init__(self, v = "symbol"):
        """
        """

        Value.__init__(self)
        self.setval(v)
    #-def
#-class

class Integer(Value):
    """
    """
    __slots__ = []

    def __init__(self, v = 0):
        """
        """

        Value.__init__(self)
        self.setval(v)
    #-def
#-class

class String(Value):
    """
    """
    __slots__ = []

    def __init__(self, v = ""):
        """
        """

        Value.__init__(self)
        self.setval(v)
    #-def
#-class

class Statement(Command):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Command.__init__(self)
        self.set_argspec(())
        self.set_args()
    #-def
#-class

class Callable(Command):
    """
    """
    __slots__ = []

    def __init__(self, argspec, *args):
        """
        """

        Command.__init__(self)
        self.set_argspec(argspec)
        self.set_args(args)
    #-def

    def stackitem(self, prev):
        """
        """

        return Frame(self, prev)
    #-def
#-class

class Block(Statement):
    """
    """
    __slots__ = []

    def __init__(self, commands = []):
        """
        """

        Statement.__init__(self, ())
        self.__commands = commands
    #-def

    def stackitem(self, prev):
        """
        """

        return Scope(self, prev)
    #-def

    def run(self, processor):
        """
        """

        return processor.eval_commands(self.__commands)
    #-def
#-class

class ExceptionHandler(Block):
    """
    """
    __slots__ = []

    def __init__(self, commands = []):
        """
        """

        Block.__init__(self, commands)
    #-def
#-class

class Print(Callable):
    """
    """
    __slots__ = []

    def __init__(self, *args):
        """
        """

        Callable.__init__(self, ("...",), *args)
    #-def

    def run(self, processor):
        """
        """

        env = processor.getenv()
        for arg in processor.getlocal("args"):
            env.wterm(processor.valueof(arg, String).value())
        return Null()
    #-def
#-class

class BreakEH(ExceptionHandler):
    """
    """
    __slots__ = []

    def __init__(self, outer):
        """
        """

        ExceptionHandler.__init__(self)
        self.__outer = outer
    #-def

    def run(self, processor):
        """
        """

        self.__outer.stop_iteration()
        return processor.result()
    #-def
#-class

class Foreach(Statement):
    """
    """
    __slots__ = []

    def __init__(self, var, iterable, commands):
        """
        """

        Statement.__init__(self, commands)
        self.__var = var
        self.__iterable = iterable
        self.atstart(self.__install_eh)
    #-def

    def __install_eh(self, processor):
        """
        """

        top.add_exception_handler(BREAK, BreakExceptionHandler(self))
    #-def
#-class
