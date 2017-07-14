#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/cmd/eval.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-14 14:41:36 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor implementation.\
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

import collections

from doit.config.version import DOIT_VERSION

from doit.support.cmd.errors import \
    CommandProcessorError, \
    CommandError

from doit.support.cmd.runtime import \
    Location, \
    Iterable, \
    Pair, \
    List, \
    HashMap, \
    UserType, \
    ExceptionClass, \
    Traceback, \
    Procedure

from doit.support.cmd.commands import \
    NONE, \
    EXCEPTION, \
    RETURN, \
    BREAK, \
    CONTINUE, \
    CLEANUP, \
    Finalizer, \
    Command, \
    Macro, \
    Module, \
    MainModule

class MetaInfo(object):
    """
    """
    __slots__ = [ 'qname', 'location' ]

    def __init__(self):
        """
        """

        self.qname = ""
        self.location = Location()
    #-def
#-class

class Environment(dict):
    """
    """
    __slots__ = [ 'processor', '__outer', 'meta' ]

    def __init__(self, processor = None, outer = None):
        """
        """

        dict.__init__(self)
        self.processor = \
            processor if processor is not None else \
            outer.processor if outer is not None else \
            None
        self.__outer = outer
        self.meta = {}
    #-def

    def setvar(self, name, value):
        """
        """

        self[name] = value
        if name not in self.meta:
            self.meta[name] = MetaInfo()
    #-def

    def getvar(self, name):
        """
        """

        if name in self:
            return self[name]
        if self.__outer:
            return self.__outer.getvar(name)
        raise CommandError(self.processor.NameError,
            "Undefined variable '%s'" % name,
            self.processor.traceback()
        )
    #-def

    def unsetvar(self, name):
        """
        """

        if name in self:
            del self[name]
        if name in self.meta:
            del self.meta[name]
    #-def

    def outer(self):
        """
        """

        return self.__outer
    #-def
#-class

class CommandProcessor(object):
    """
    """
    __slots__ = [
        '__env', '__ctxstack', '__valstack', '__codebuff', '__acc', '__consts',
        '__types'
    ]

    def __init__(self, env = None):
        """
        """

        self.__env = env if env is not None else Environment()
        self.__env.processor = self
        self.__ctxstack = []
        self.__valstack = []
        self.__codebuff = []
        self.__acc = None
        self.__initialize_types_and_constants()
        self.__copy_exceptions_to_env()
        self.__initialize_main_module()
        self.cleanup()
    #-def

    def version(self):
        """
        """

        return Pair(
            DOIT_VERSION.major * 10000 \
            + DOIT_VERSION.minor * 100 \
            + DOIT_VERSION.patchlevel,
            DOIT_VERSION.date
        )
    #-def

    def envclass(self):
        """
        """

        return self.__env.__class__
    #-def

    def newenv(self, outer = None):
        """
        """

        return self.__env.__class__(
            self, self.getenv() if outer is None else outer
        )
    #-def

    def getenv(self):
        """
        """

        if self.__ctxstack and self.__ctxstack[-1].env is not None:
            return self.__ctxstack[-1].env
        return self.__env
    #-def

    def pushctx(self, ctx):
        """
        """

        self.__ctxstack.append(ctx)
    #-def

    def cmdctx(self, cmd):
        """
        """

        if not self.__ctxstack:
            raise CommandProcessorError(Traceback([]),
                "cmdctx: Command context stack is empty"
            )
        ctx = self.__ctxstack[-1]
        fnlz, i = None, 0
        while i < len(self.__codebuff):
            if isinstance(self.__codebuff[i], Finalizer):
                fnlz = self.__codebuff[i]
                break
            i += 1
        if not fnlz or fnlz.ctx is not ctx or ctx.cmd is not cmd:
            raise CommandProcessorError(Traceback(self.__ctxstack),
                "cmdctx: Inconsistent state"
            )
        return ctx
    #-def

    def popctx(self, ctx):
        """
        """

        if not self.__ctxstack:
            raise CommandProcessorError(Traceback([]),
                "popctx: Command context stack is empty"
            )
        if self.__ctxstack[-1] is not ctx:
            raise CommandProcessorError(Traceback(self.__ctxstack),
                "popctx: Command context stack is corrupted"
            )
        self.__ctxstack.pop()
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
            raise CommandProcessorError(Traceback(self.__ctxstack),
                "topval: Value stack is empty"
            )
        return self.__valstack[-1]
    #-def

    def popval(self):
        """
        """

        if not self.__valstack:
            raise CommandProcessorError(Traceback(self.__ctxstack),
                "popval: Value stack is empty"
            )
        return self.__valstack.pop()
    #-def

    def nvals(self):
        """
        """

        return len(self.__valstack)
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

    def traceback(self):
        """
        """

        return Traceback(self.__ctxstack)
    #-def

    def mkqname(self, name):
        """
        """

        return "%s::%s" % ("::".join([x.name for x in self.traceback()]), name)
    #-def

    def types(self):
        """
        """

        return list(self.__types.values())
    #-def

    def run(self, commands):
        """
        """

        cb = self.__codebuff
        cb[:0] = commands
        types = self.types()
        while cb:
            x = cb.pop(0)
            if isinstance(x, Command):
                x.expand(self)
            elif hasattr(x, '__call__'):
                try:
                    x(self)
                except CommandError as e:
                    cb[:0] = [e]
            elif isinstance(x, (
                bool, int, float, str, Iterable, UserType, Procedure
            )) or x in types:
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
                self.handle_event(EXCEPTION, x)
            else:
                raise CommandProcessorError(Traceback(self.__ctxstack),
                    "run: Unexpected object in code buffer appeared"
                )
    #-def

    def handle_event(self, event, *args):
        """
        """

        if event == NONE:
            return
        args = list(args)
        cb, stack = self.__codebuff, self.__ctxstack
        tb = self.extract_tb(event, args)
        handled = False
        while cb:
            x = cb.pop(0)
            if isinstance(x, Finalizer):
                if not stack or x.ctx is not stack[-1]:
                    raise CommandProcessorError(tb,
                        "Command context stack is corrupted"
                    )
                self.update_fnlz_state(x, event, args)
                cb.insert(0, x)
                handled = True
                break
        if event == CLEANUP:
            return
        if (event == EXCEPTION and not handled) or not cb:
            raise CommandProcessorError(tb,
                "Uncaught exception %r" % args[0] if event == EXCEPTION else \
                "return used outside function" if event == RETURN else \
                "break used outside loop" if event == BREAK else \
                "continue used outside loop" if event == CONTINUE else \
                "Unhandled event #%d" % event
            )
    #-def

    def extract_tb(self, event, args):
        """
        """

        if event == EXCEPTION:
            return args[0].tb
        elif event in (RETURN, BREAK, CONTINUE, CLEANUP):
            if args[0] is None:
                args[0] = self.traceback()
            return args[0]
        else:
            raise CommandProcessorError(self.traceback(),
                "Unhandled event #%d" % event
            )
    #-def

    def update_fnlz_state(self, fnlz, event, args):
        """
        """

        if event == EXCEPTION:
            e = args[0]
            eh = fnlz.ctx.cmd.find_exception_handler(fnlz.ctx, e)
            fnlz.state = (event, e, eh)
        elif event == RETURN:
            tb = args[0]
            rc = args[1]
            fnlz.state = (event, tb, rc)
        elif event in (BREAK, CONTINUE, CLEANUP):
            tb = args[0]
            fnlz.state = (event, tb)
        else:
            raise CommandProcessorError(self.traceback(),
                "Unhandled event #%d" % event
            )
    #-def

    def cleanup(self):
        """
        """

        self.handle_event(CLEANUP, None)
        self.run([])
        while self.__ctxstack:
            self.__ctxstack.pop()
        while self.__valstack:
            self.__valstack.pop()
        self.__acc = None
    #-def

    def __getattr__(self, attr):
        """
        """

        if attr[0].isupper():
            if attr not in self.__types and attr not in self.__consts:
                raise CommandProcessorError(Traceback(self.__ctxstack),
                    "There is no '%s' type or constant defined" % attr
                )
            return self.__types.get(attr, self.__consts.get(attr))
        return object.__getattribute__(self, attr)
    #-def

    def __initialize_types_and_constants(self):
        """
        """

        _ = lambda s, b: ExceptionClass(s, self.mkqname(s), b)
        self.__types = collections.OrderedDict([
            ('NullType', self.__class__),
            ('Boolean', bool),
            ('Integer', int),
            ('Float', float),
            ('String', str),
            ('Pair', Pair),
            ('List', list),
            ('HashMap', dict),
            ('UserType', UserType),
            ('ErrorClass', ExceptionClass),
            ('Error', CommandError),
            ('Macro', Macro),
            ('Proc', Procedure),
            ('Module', Module)
        ])
        self.__consts = { 'Null': self }
        self.__consts['BaseException'] = _('BaseException', None)
        self.__consts['Exception'] = _('Exception', self.BaseException)
        self.__consts['SyntaxError'] = _('SyntaxError', self.Exception)
        self.__consts['NameError'] = _('NameError', self.Exception)
        self.__consts['TypeError'] = _('TypeError', self.Exception)
        self.__consts['ValueError'] = _('ValueError', self.Exception)
        self.__consts['IndexError'] = _('IndexError', self.Exception)
        self.__consts['KeyError'] = _('KeyError', self.Exception)
    #-def

    def __copy_exceptions_to_env(self):
        """
        """

        for x in (
            self.BaseException, self.Exception,
            self.SyntaxError, self.NameError,
            self.TypeError, self.ValueError,
            self.IndexError, self.KeyError
        ):
            if str(x) not in self.__env:
                self.__env[str(x)] = x
    #-def

    def __initialize_main_module(self):
        """
        """

        mm = MainModule()
        self.__env.setvar(mm.name, mm)
        self.run([mm])
    #-def

    def print_impl(self, s):
        """
        """

        pass
    #-def
#-class
