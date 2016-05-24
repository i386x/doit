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

class Finalizer(object):
    """
    """
    __slots__ = [ 'cmd' ]

    def __init__(self, cmd):
        """
        """

        self.cmd = cmd
    #-def

    def __call__(self, processor):
        """
        """

        self.cmd.leave(processor)
    #-def
#-class

class Command(object):
    """
    """
    __slots__ = [ 'name', 'location', 'args', 'env' ]

    def __init__(self):
        """
        """

        self.name = self.__class__.__name__.lower()
        self.location = Location()
        self.env = None
    #-def

    def isfunc(self):
        """
        """

        return False
    #-def

    def set_location(self, file = None, line = -1, column = -1):
        """
        """

        self.location = Location(file, line, column)
    #-def

    def __str__(self):
        """
        """

        return "\"%s\" %s" % (self.name, self.location)
    #-def

    def help(self, processor):
        """
        """

        pass
    #-def

    def enter(self, processor):
        """
        """

        pass
    #-def

    def expand(self, processor):
        """
        """

        pass
    #-def

    def leave(self, processor):
        """
        """

        pass
    #-def

    def pushacc(self, processor):
        """
        """

        processor.pushacc()
    #-def

    def find_exception_handler(self, e):
        """
        """

        return None
    #-def
#-class

class Trackable(Command):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Command.__init__(self)
    #-def

    def enter(self, processor):
        """
        """

        self.env = processor.getenv()
        processor.pushcmd(self)
    #-def

    def leave(self, processor):
        """
        """

        processor.popcmd(self)
        self.env = None
    #-def
#-class

class Value(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        Trackable.__init__(self)
        self.value = v
    #-def

    def expand(self, processor):
        """
        """

        processor.insercode(
            self.enter, self.self2acc, Finalizer(self)
        )
    #-def

    def self2acc(self, processor):
        """
        """

        processor.setacc(self)
    #-def
#-class

class Null(Value):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Value.__init__(self, None)
    #-def
#-class

class Int(Value):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        if isinstance(v, Value):
            v = v.value
        if not hasattr(v, '__int__'):
            raise CmdTypeError("Int must be initialized with integer")
        Value.__init__(self, int(v))
    #-def
#-class

class Str(Value):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        if isinstance(v, Value):
            v = v.value
        if not hasattr(v, '__str__'):
            raise CmdTypeError("Str must be initialized with string")
        Value.__init__(self, v)
    #-def
#-class

class Sym(Value):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        if isinstance(v, Value):
            v = v.value
        if not hasattr(v, '__str__'):
            raise CmdTypeError("Sym must be initialized with string")
        Value.__init__(self, v)
    #-def
#-class

class Iterable(Value):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        if not hasattr(v, '__iter__'):
            raise CmdTypeError(
                "Iterable must be initialized with iterable object"
            )
        Value.__init__(self, v)
    #-def

    def iterator(self):
        """
        """

        return BaseIterator()
    #-def
#-class

class List(Iterable):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        if isinstance(v, Value):
            v = v.value
        Iterable.__init__(self, v)
        self.value = list(self.value)
    #-def

    def iterator(self):
        """
        """

        return FiniteIterator(self.value)
    #-def
#-class

class Block(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, *commands):
        """
        """

        Command.__init__(self)
        self.commands = commands
    #-def

    def enter(self, processor):
        """
        """

        self.env = Environment(processor.getenv())
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            *((self.enter,) + self.commands + (Finalizer(self),))
        )
    #-def
#-class

class If(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, c, t, e):
        """
        """

        Command.__init__(self)
        self.c = c
        self.t = t
        self.e = e
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            self.c, self.pushacc, self.do_if, Finalizer(self)
        )
    #-def

    def do_if(self, processor):
        """
        """

        processor.insertcode(
            *(self.t if processor.popval() else self.e)
        )
    #-def
#-class

class Foreach(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, var, itexp, body):
        """
        """

        Trackable.__init__(self)
        self.var = var
        self.itexp = itexp
        self.body = body
        self.iterator = None
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            self.enter, self.itexp, self.do_for, Finalizer(self)
        )
    #-def

    def do_for(self, processor):
        """
        """

        if not isinstance(processor.acc(), Iterable):
            raise CmdTypeError("Object must be iterable")
        self.iterator = processor.acc().iterator()
        self.iterator.reset()
        processor.insertcode(self.do_loop)
    #-def

    def do_loop(self, processor):
        """
        """

        x = self.iterator.next()
        if x is self.iterator:
            return
        processor.pushval(x)
        processor.insertcode(
            *((self.do_setvar,) + self.body + (self.do_loop,))
        )
    #-def

    def do_setvar(self, processor):
        """
        """

        self.env.setvar(self.var, processor.popval())
    #-def

    def leave(self, processor):
        """
        """

        self.iterator.reset()
        self.iterator = None
        Trackable.leave(self, processor)
    #-def
#-class

class Closure(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, name, bvars, args, body, outer):
        """
        """

        Trackable.__init__(self)
        self.name = name
        self.bvars = bvars
        self.args = args
        self.body = body
        self.outer = outer
    #-def

    def isfunc(self):
        """
        """

        return True
    #-def

    def enter(self, processor):
        """
        """

        self.env = Environment(self.outer)
        for bvar in self.bvars:
            self.env.setvar(bvar, Null())
        for argname in self.args:
            self.env.setvar(argname, self.args[argname])
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            *((self.enter,) + self.body + (Finalizer(self),))
        )
    #-def
#-class

class Call(Command):
    """
    """
    __slots__ = []

    def __init__(self, name, *args):
        """
        """

        Command.__init__(self)
        self.name = value(name)
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        proc = processor.getenv().getvar(self.name)
        if not isinstance(proc, ProcedureTemplate):
            procedure.insertcode(CmdTypeError(
                "%s must be callable" % self.name
            ))
            return
        _, params, _, _ = proc
        nparams = len(params)
        nargs = len(self.args)
        if nargs != nparams:
            processor.insertcode(CmdTypeError(
                "%s takes %d argument%s but %d w%s given" \
                % (
                    self.name,
                    nparams,
                    "" if nparams == 1 else "s",
                    nargs,
                    "as" if nargs == 1 else "ere"
                )
            ))
            return
        processor.pushval(Value({}))
        i = 0
        for arg in self.args:
            processor.insertcode(
                arg, self.pushacc, Value(params[i]), self.pushacc, self.do_arg
            )
            i += 1
        processor.insertcode(
            Value((self.name, proc)), self.pushacc, self.do_call
        )
    #-def

    def do_arg(self, processor):
        """
        """

        name = processor.popval().value
        value = processor.popval()
        processor.topval().value[name] = value
    #-def

    def do_call(self, processor):
        """
        """

        name, proc = processor.popval().value
        args = processor.popval().value
        bvars, _, body, outer = proc
        processor.insertcode(Closure(name, bvars, args, body, outer))
    #-def
#-class

class Print(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, *args):
        """
        """

        Trackable.__init__(self)
        self.args = args
        self.tty = None
    #-def

    def enter(self, processor):
        """
        """

        Trackable.enter(self, processor)
        self.tty = self.env.getvar('$TTY')
        if not isinstance(self.tty, Terminal):
            CmdTypeError("$TTY variable must refer to terminal")
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(self.enter)
        for arg in self.args:
            processor.insertcode(arg, self.do_print_arg)
        processor.insertcode(Finalizer(self))
    #-def

    def do_print_arg(self, processor):
        """
        """

        self.tty.write("%s" % processor.acc())
    #-def

    def leave(self, processor):
        """
        """

        self.tty = None
        Trackable.leave(self, processor)
    #-def
#-class
