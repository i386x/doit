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

import types

from doit.text.pgen.readers.glap.cmd.errors import \
    CommandProcessorError, \
    CommandError

from doit.text.pgen.readers.glap.cmd.commands import \
    Command

class Environment(object):
    """
    """
    __slots__ = [ '__vars' ]

    def __init__(self, outer = None):
        """
        """

        self.__outer = outer
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

        if name in self.__vars:
            return self.__vars[name]
        if self.__outer:
            return self.__outer.getvar(name)
        raise CmdNameError("Undefined variable '%s'" % name)
    #-def

    def unsetvar(self, name):
        """
        """

        if name in self.__vars:
            del self.__vars[name]
    #-def
#-class

class CommandProcessor(object):
    """
    """
    __slots__ = []

    def __init__(self, env = None):
        """
        """

        self.__env = env or Environment()
        self.__cmdstack = []
        self.__valstack = []
        self.__codebuff = []
        self.__acc = None
    #-def

    def getenv(self):
        """
        """

        return (self.__cmdstack and self.__cmdstack[-1].env) or self.__env
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
            elif isinstance(x, (types.MethodType, Finalizer)):
                try:
                    x(self)
                except CommandError as e:
                    cb[:0] = [e]
            elif isinstance(x, CommandError):
                self.handle_exception(x)
    #-def

    def handle_exception(self, e):
        """
        """

        cb, stack = self.__codebuff, self.__stack
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
                    handled = True
                x(self)
        if not handled:
            raise CommandProcessorError(tb, "Uncaught exception %r" % e)
    #-def
#-class
