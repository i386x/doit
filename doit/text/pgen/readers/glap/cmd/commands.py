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

class ArgumentProxy(object):
    """
    """
    __slots__ = []

    def __init__(self, cmd, i, isvararg = False):
        """
        """

        self.__cmd = cmd
        self.__i = i
        self.__isvararg = isvararg
    #-def

    def value(self, processor):
        """
        """

        try:
            args = self.__cmd.get_args()
            if self.__isvararg:
                return args[self.__i:]
            return args[self.__i]
        except IndexError:
            raise CmdErrNArgs(processor, self.__i)
    #-def
#-class

class Command(object):
    """
    """
    __slots__ = [ '__name', '__argspec', '__args' ]

    def __init__(self):
        """
        """

        self.__name = self.__class__.__name__.lower()
        self.__file = None
        self.__line = -1
        self.__column = -1
        self.__args = []
        self.__argproxies = {}
        self.__initializers = [self.init_vars]
        self.__finalizers = []
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

    def set_location(self, file, line, column):
        """
        """

        self.__file = file
        self.__line = line
        self.__column = column
    #-def

    def get_location(self):
        """
        """

        return self.__file, self.__line, self.__column
    #-def

    def __str__(self):
        """
        """

        scmd = "\"%s\"" % self.__name
        if self.__file and self.__line >= 0 and self.__column >= 0:
            return "%s at [\"%s\":%d:%d]" % (
                scmd, self.__file, self.__line, self.__column
            )
        return "%s (internal)" % scmd
    #-def

    def set_argspec(self, *argspec):
        """
        """

        self.__argproxies.clear()
        self.add_argspec(*argspec)
    #-def

    def add_argspec(self, *argspec):
        """
        """

        self.__install_argproxies(argspec)
    #-def

    def set_args(self, *args):
        """
        """

        self.__args = list(args)
    #-def

    def add_args(self, *args):
        """
        """

        self.__args.extend(args)
    #-def

    def get_args(self):
        """
        """

        return self.__args
    #-def

    def __install_argproxies(self, argspec):
        """
        """

        i = 0
        while i < len(argspec):
            k = argspec[i]
            self.__argproxies['args' if k == '...' else k] = ArgumentProxy(
                self, i, k == '...'
            )
            i += 1
        #-while
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

    def help(self, processor):
        """
        """

        pass
    #-def

    def run(self, processor):
        """
        """

        return self
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

    def init_vars(self, processor):
        """
        """

        for k in self.__argproxies:
            processor.setlocal(k, self.__argproxies[k])
    #-def

    def stackitem(self, prev):
        """
        """

        return StackItem(self, prev)
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
        self.set_argspec(())
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

class Print(BuiltinCommand):
    """
    """
    __slots__ = []

    def __init__(self, *args):
        """
        """

        BuiltinCommand.__init__(self, ("...",), *args)
    #-def

    def run(self, processor):
        """
        """

        env = processor.getenv()
        for arg in processor.getlocal("args"):
            env.defout.write(processor.valueof(arg, String).value())
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
