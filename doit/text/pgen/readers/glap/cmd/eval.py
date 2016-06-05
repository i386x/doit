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

from doit.text.pgen.readers.glap.cmd.errors import \
    CommandProcessorError, \
    CommandError

from doit.text.pgen.readers.glap.cmd.runtime import \
    Iterable, \
    Pair, \
    List, \
    HashMap, \
    ExceptionClass, \
    Traceback

from doit.text.pgen.readers.glap.cmd.commands import \
    Finalizer, \
    Command

class Environment(dict):
    """
    """
    __slots__ = [ '__processor', '__outer' ]

    def __init__(self, processor = None, outer = None):
        """
        """

        dict.__init__(self)
        self.__processor = processor
        self.__outer = outer
    #-def

    def setprocessor(self, processor):
        """
        """

        self.__processor = processor
    #-def

    def setvar(self, name, value):
        """
        """

        self[name] = value
    #-def

    def getvar(self, name):
        """
        """

        if name in self:
            return self[name]
        if self.__outer:
            return self.__outer.getvar(name)
        raise CommandError(self.__processor.NameError,
            "Undefined variable '%s'" % name
        )
    #-def

    def unsetvar(self, name):
        """
        """

        if name in self:
            del self[name]
    #-def
#-class

class CommandProcessor(object):
    """
    """
    __slots__ = [
        '__env', '__cmdstack', '__valstack', '__codebuff', '__acc', '__consts'
    ]

    def __init__(self, env = None):
        """
        """

        self.__env = env if env is not None else Environment()
        self.__env.setprocessor(self)
        self.__cmdstack = []
        self.__valstack = []
        self.__codebuff = []
        self.__acc = None
        self.__initialize_constants()
        self.__copy_exceptions_to_env()
    #-def

    def envclass(self):
        """
        """

        return self.__env.__class__
    #-def

    def newenv(self):
        """
        """

        return self.__env.__class__(self, self.getenv())
    #-def

    def getenv(self):
        """
        """

        if self.__cmdstack and self.__cmdstack[-1].env is not None:
            return self.__cmdstack[-1].env
        return self.__env
    #-def

    def pushcmd(self, cmd):
        """
        """

        self.__cmdstack.append(cmd)
    #-def

    def popcmd(self, cmd):
        """
        """

        if not self.__cmdstack:
            raise CommandProcessorError(Traceback([]),
                "popcmd: Command stack is empty"
            )
        if self.__cmdstack[-1] is not cmd:
            raise CommandProcessorError(Traceback(self.__cmdstack),
                "popcmd: Command stack is corrupted"
            )
        self.__cmdstack.pop()
    #-def

    def pushval(self, val):
        """
        """

        self.__valstack.append(val)
    #-def

    def pushacc(self):
        """
        """

        self.__valstack.append(self.__acc)
    #-def

    def topval(self):
        """
        """

        if not self.__valstack:
            raise CommandProcessorError(Traceback(self.__cmdstack),
                "topval: Value stack is empty"
            )
        return self.__valstack[-1]
    #-def

    def popval(self):
        """
        """

        if not self.__valstack:
            raise CommandProcessorError(Traceback(self.__cmdstack),
                "popval: Value stack is empty"
            )
        return self.__valstack.pop()
    #-def

    def insertcode(self, *ops):
        """
        """

        self.__codebuff[:0] = ops
    #-def

    def setacc(self, v):
        """
        """

        self.__acc = v
    #-def

    def acc(self):
        """
        """

        return self.__acc
    #-def

    def run(self, commands):
        """
        """

        cb = self.__codebuff
        cb[:0] = commands
        while cb:
            x = cb.pop(0)
            if isinstance(x, Command):
                x.expand(self)
            elif hasattr(x, '__call__'):
                try:
                    x(self)
                except CommandError as e:
                    cb[:0] = [e]
            elif isinstance(x, (bool, int, float, str, Iterable)):
                self.__acc = x
            elif isinstance(x, tuple) and len(x) == 2:
                self.__acc = Pair(*x)
            elif isinstance(x, list):
                self.__acc = List(x)
            elif isinstance(x, dict):
                self.__acc = HashMap(x)
            elif x is None or x is self.Null:
                self.__acc = self.Null
            elif isinstance(x, CommandError):
                self.handle_exception(x)
            else:
                raise CommandProcessorError(Traceback(self.__cmdstack),
                    "run: Unexpected object in code buffer appeared"
                )
    #-def

    def handle_exception(self, e):
        """
        """

        cb, stack = self.__codebuff, self.__cmdstack
        tb = Traceback(stack)
        handled = False
        while not handled and cb and stack:
            x = cb.pop(0)
            if isinstance(x, Finalizer):
                if x.cmd is not stack[-1]:
                    raise CommandProcessorError(tb,
                        "handle_exception: Command stack is corrupted"
                    )
                eh = stack[-1].find_exception_handler(e)
                if eh is not None:
                    cb[:0] = eh
                    self.__acc = e
                    handled = True
                x(self)
        if not handled:
            raise CommandProcessorError(tb, "Uncaught exception %r" % e)
    #-def

    def cleanup(self):
        """
        """

        while self.__codebuff:
            f = self.__codebuff.pop(0)
            if isinstance(f, Finalizer):
                f(self)
        while self.__cmdstack:
            self.__cmdstack.pop()
        while self.__valstack:
            self.__valstack.pop()
        self.__acc = None
    #-def

    def define_exception(self, name, basename):
        """
        """

        env = self.getenv()
        base = env.getvar(basename)
        if not isinstance(base, ExceptionClass):
            raise CommandError(self.TypeError, "Base class must be exception")
        env[name] = ExceptionClass(name, base)
    #-def

    def __getattr__(self, attr):
        """
        """

        if attr[0].isupper():
            if attr not in self.__consts:
                raise CommandProcessorError(Traceback(self.__cmdstack),
                    "There is no '%s' constant defined" % attr
                )
            return self.__consts[attr]
        return object.__getattribute__(self, attr)
    #-def

    def __initialize_constants(self):
        """
        """

        self.__consts = { 'Null': self }
        self.__consts['BaseException'] = ExceptionClass('BaseException', None)
        self.__consts['Exception'] = ExceptionClass(
            'Exception', self.BaseException
        )
        self.__consts['NameError'] = ExceptionClass(
            'NameError', self.Exception
        )
        self.__consts['TypeError'] = ExceptionClass(
            'TypeError', self.Exception
        )
        self.__consts['ValueError'] = ExceptionClass(
            'ValueError', self.Exception
        )
        self.__consts['IndexError'] = ExceptionClass(
            'IndexError', self.Exception
        )
        self.__consts['KeyError'] = ExceptionClass(
            'KeyError', self.Exception
        )
    #-def

    def __copy_exceptions_to_env(self):
        """
        """

        for x in (
            self.BaseException, self.Exception, \
            self.NameError, self.TypeError, self.ValueError, \
            self.IndexError, self.KeyError
        ):
            if str(x) not in self.__env:
                self.__env[str(x)] = x
    #-def
#-class
