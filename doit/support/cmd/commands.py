#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/cmd/commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-14 15:36:02 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor's basic commands.\
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

from doit.support.cmd.errors import \
    CommandError

from doit.support.cmd.runtime import \
    isderived, \
    Pair, \
    List, \
    HashMap, \
    UserType, \
    ExceptionClass, \
    Procedure

NONE = 0
EXCEPTION = 1
RETURN = 2
BREAK = 3
CONTINUE = 4
CLEANUP = 5

NumericTypes = (int, float)
SequenceTypes = (str, Pair, list)
FixedLengthSequenceTypes = (Pair,)
VariableLengthSequenceTypes = (str, list)
CollectionTypes = (str, Pair, list, dict)

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

class CommandContext(object):
    """
    """
    __slots__ = [ 'cmd', 'env', 'nvals' ]

    def __init__(self, cmd):
        """
        """

        self.cmd = cmd
        self.env = None
        self.nvals = 0
    #-def
#-class

class Initializer(object):
    """
    """
    __slots__ = [ 'ctx' ]

    def __init__(self, ctx):
        """
        """

        self.ctx = ctx
    #-def

    def __call__(self, processor):
        """
        """

        self.ctx.cmd.enter(processor, self)
    #-def
#-class

class Finalizer(object):
    """
    """
    __slots__ = [
        'state', 'ctx', 'after', '__acc', '__sandboxed', '__on_throw'
    ]

    def __init__(self, ctx,
        after = [], sb = False, on_throw = (lambda f, p, e: None)
    ):
        """
        """

        self.state = (NONE,)
        self.ctx = ctx
        self.after = after
        self.__acc = None
        self.__sandboxed = sb
        self.__on_throw = on_throw
    #-def

    def acc_backup(self, processor):
        """
        """

        self.__acc = processor.acc()
    #-def

    def acc_restore(self, processor):
        """
        """

        processor.setacc(self.__acc)
    #-def

    def pushacc(self, processor):
        """
        """

        processor.pushacc()
    #-def

    def sandboxed(self):
        """
        """

        return self.__sandboxed
    #-def

    def __call__(self, processor):
        """
        """

        if self.sandboxed():
            self.ctx.cmd.leave(processor, self)
            processor.setacc(self)
            return
        self.acc_backup(processor)
        eh = self.state[2] if self.state[0] == EXCEPTION else []
        if eh is None:
            eh = []
        processor.insertcode(
            SandBox(eh), self.pushacc, SandBox(self.after), self.finalize
        )
    #-def

    def finalize(self, processor):
        """
        """

        after_fnlz = processor.acc()
        eh_fnlz = processor.popval()

        if after_fnlz.state[0] == NONE:
            if self.state[0] == EXCEPTION:
                _, e, eh = self.state
                if eh is None:
                    self.do_throw(processor, e)
                elif eh_fnlz.state[0] == EXCEPTION:
                    self.resolve_exception(processor, eh_fnlz.state)
                elif eh_fnlz.state[0] == RETURN:
                    self.resolve_return(processor, eh_fnlz.state)
                elif eh_fnlz.state[0] == BREAK:
                    self.resolve_break(processor, eh_fnlz.state)
                elif eh_fnlz.state[0] == CONTINUE:
                    self.resolve_continue(processor, eh_fnlz.state)
                else:
                    self.do_leave(processor)
            elif self.state[0] == RETURN:
                self.resolve_return(processor, self.state)
            elif self.state[0] == BREAK:
                self.resolve_break(processor, self.state)
            elif self.state[0] == CONTINUE:
                self.resolve_continue(processor, self.state)
            elif self.state[0] == CLEANUP:
                self.resolve_cleanup(processor, self.state)
            else:
                self.do_leave(processor)
        elif after_fnlz.state[0] == EXCEPTION:
            self.resolve_exception(processor, after_fnlz.state)
        elif after_fnlz.state[0] == RETURN:
            self.resolve_return(processor, after_fnlz.state)
        elif after_fnlz.state[0] == BREAK:
            self.resolve_break(processor, after_fnlz.state)
        elif after_fnlz.state[0] == CONTINUE:
            self.resolve_continue(processor, after_fnlz.state)
        else:
            self.do_leave(processor)
    #-def

    def resolve_exception(self, processor, state):
        """
        """

        _, e, _ = state
        self.do_throw(processor, e)
    #-def

    def resolve_return(self, processor, state):
        """
        """

        _, tb, rc = state
        self.do_leave(processor)
        if self.ctx.cmd.isfunc():
            processor.setacc(rc)
        else:
            processor.handle_event(RETURN, tb, rc)
    #-def

    def resolve_break(self, processor, state):
        """
        """

        _, tb = state
        if self.ctx.cmd.isfunc():
            self.do_throw(processor, CommandError(
                processor.SyntaxError,
                "%s: break used outside loop" % self.ctx.cmd.name,
                tb
            ))
        elif self.ctx.cmd.isloop():
            self.do_leave(processor)
        else:
            self.do_leave(processor)
            processor.handle_event(BREAK, tb)
    #-def

    def resolve_continue(self, processor, state):
        """
        """

        _, tb = state
        if self.ctx.cmd.isfunc():
            self.do_throw(processor, CommandError(
                processor.SyntaxError,
                "%s: continue used outside loop" % self.ctx.cmd.name,
                tb
            ))
        elif self.ctx.cmd.isloop():
            self.state = (NONE,)
            processor.insertcode(self)
            self.ctx.cmd.do_continue(processor)
        else:
            self.do_leave(processor)
            processor.handle_event(CONTINUE, tb)
    #-def

    def resolve_cleanup(self, processor, state):
        """
        """

        _, tb = state
        self.do_leave(processor)
        processor.handle_event(CLEANUP, tb)
    #-def

    def do_throw(self, processor, e):
        """
        """

        self.__on_throw(self, processor, e)
        self.do_leave(processor)
        processor.insertcode(e)
    #-def

    def do_leave(self, processor):
        """
        """

        self.ctx.cmd.leave(processor, self)
        self.acc_restore(processor)
    #-def
#-class

class Command(object):
    """
    """
    __slots__ = [ 'name', 'qname', 'location' ]

    def __init__(self):
        """
        """

        self.name = self.__class__.__name__.lower()
        self.qname = self.name
        self.location = Location()
    #-def

    def isloop(self):
        """
        """

        return False
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

    def enter(self, processor, inlz):
        """
        """

        pass
    #-def

    def expand(self, processor):
        """
        """

        pass
    #-def

    def leave(self, processor, fnlz):
        """
        """

        pass
    #-def

    def pushacc(self, processor):
        """
        """

        processor.pushacc()
    #-def

    def find_exception_handler(self, ctx, e):
        """
        """

        return None
    #-def

    def do_continue(self, processor):
        """
        """

        pass
    #-def
#-class

class Const(Command):
    """
    """
    __slots__ = [ 'constval' ]

    def __init__(self, constval):
        """
        """

        Command.__init__(self)
        self.constval = constval
    #-def

    def expand(self, processor):
        """
        """

        processor.setacc(self.constval)
    #-def
#-class

class Version(Command):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Command.__init__(self)
    #-def

    def expand(self, processor):
        """
        """

        processor.setacc(processor.version())
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

    def enter(self, processor, inlz):
        """
        """

        inlz.ctx.env = processor.getenv()
        inlz.ctx.nvals = processor.nvals()
        processor.pushctx(inlz.ctx)
    #-def

    def leave(self, processor, fnlz):
        """
        """

        while processor.nvals() > fnlz.ctx.nvals:
            processor.popval()
        processor.popctx(fnlz.ctx)
    #-def
#-class

class MacroNode(object):
    """
    """
    __slots__ = [ 'ctor', 'nodes' ]

    def __init__(self, ctor, *nodes):
        """
        """

        self.ctor = ctor
        self.nodes = nodes
    #-def

    def substitute(self, p2v):
        """
        """

        return self.ctor(*[x.substitute(p2v) for x in self.nodes])
    #-def
#-class

class MacroNodeSequence(MacroNode):
    """
    """
    __slots__ = []

    def __init__(self, *nodes):
        """
        """

        MacroNode.__init__(self, (lambda *args: list(args)), *nodes)
    #-def
#-class

class MacroNodeAtom(MacroNode):
    """
    """
    __slots__ = []

    def __init__(self, atom):
        """
        """

        MacroNode.__init__(self, None, atom)
    #-def

    def substitute(self, p2v):
        """
        """

        return self.nodes[0]
    #-def
#-class

class MacroNodeParam(MacroNode):
    """
    """
    __slots__ = []

    def __init__(self, param):
        """
        """

        MacroNode.__init__(self, None, param)
    #-def

    def substitute(self, p2v):
        """
        """

        return p2v.get(self.nodes[0], self)
    #-def
#-class

class Macro(object):
    """
    """
    __slots__ = [ 'name', 'qname', 'params', 'body' ]

    def __init__(self, name, qname, params, body):
        """
        """

        self.name = name
        self.qname = qname
        self.params = params
        self.body = body
    #-def

    def substitute(self, args):
        """
        """

        return [node.substitute(dict(zip(self.params, args)))
            for node in self.body
        ]
    #-def
#-class

class Expand(Command):
    """
    """
    __slots__ = [ 'macro', 'args' ]

    def __init__(self, macro, *args):
        """
        """

        Command.__init__(self)
        self.macro = macro
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(self.macro, self.do_expand)
    #-def

    def do_expand(self, processor):
        """
        """

        macro = processor.acc()

        if not isinstance(macro, Macro):
            raise CommandError(processor.TypeError,
                "%s: Macro expected" % self.name,
                processor.traceback()
            )
        if len(macro.params) != len(self.args):
            raise CommandError(processor.TypeError,
                "%s: Macro %s needs %d argument%s, but %d %s given" % (
                    self.name, macro.name,
                    len(macro.params),
                    "" if len(macro.params) == 1 else "s",
                    len(self.args),
                    "was" if len(self.args) == 1 else "were"
                ),
                processor.traceback()
            )
        processor.insertcode(*(macro.substitute(self.args)))
    #-def
#-class

class SetLocal(Trackable):
    """
    """
    __slots__ = [ 'varname', 'value', 'depth' ]

    def __init__(self, name, value, depth = 0):
        """
        """

        Trackable.__init__(self)
        self.varname = name
        self.value = value
        self.depth = depth
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx), self.value, self.do_setlocal, Finalizer(ctx)
        )
    #-def

    def do_setlocal(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        env, d = ctx.env, self.depth
        while d > 0:
            env = env.outer()
            d -= 1
        env.setvar(self.varname, processor.acc())
        env.meta[self.varname].qname = processor.mkqname(self.varname)
    #-def
#-class

class GetLocal(Trackable):
    """
    """
    __slots__ = [ 'varname' ]

    def __init__(self, name):
        """
        """

        Trackable.__init__(self)
        self.varname = name
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx), self.do_getlocal, Finalizer(ctx)
        )
    #-def

    def do_getlocal(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        processor.setacc(ctx.env.getvar(self.varname))
    #-def
#-class

class DefMacro(Trackable):
    """
    """
    __slots__ = [ 'mname', 'params', 'body' ]

    def __init__(self, mname, params, body):
        """
        """

        Trackable.__init__(self)
        self.mname = mname
        self.params = params
        self.body = body
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx), self.do_defmacro, Finalizer(ctx)
        )
    #-def

    def do_defmacro(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        qname = processor.mkqname(self.mname)
        ctx.env.setvar(self.mname, Macro(
            self.mname, qname, self.params, self.body
        ))
        ctx.env.meta[self.mname].qname = qname
    #-def
#-class

class DefError(Trackable):
    """
    """
    __slots__ = [ 'ename', 'ebase' ]

    def __init__(self, ename, ebase):
        """
        """

        Trackable.__init__(self)
        self.ename = ename
        self.ebase = ebase
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx), self.ebase, self.do_deferror, Finalizer(ctx)
        )
    #-def

    def do_deferror(self, processor):
        """
        """

        ebase = processor.acc()
        ctx = processor.cmdctx(self)

        if not isinstance(ebase, ExceptionClass):
            raise CommandError(processor.TypeError,
                "%s: Error base must be exception class" % self.name,
                processor.traceback()
            )
        qname = processor.mkqname(self.ename)
        ctx.env.setvar(self.ename, ExceptionClass(self.ename, qname, ebase))
        ctx.env.meta[self.ename].qname = qname
    #-def
#-class

class Define(Trackable):
    """
    """
    __slots__ = [ 'pname', 'bvars', 'params', 'vararg', 'body' ]

    def __init__(self, pname, bvars, params, vararg, body):
        """
        """

        Trackable.__init__(self)
        self.pname = pname
        self.bvars = bvars
        self.params = params
        self.vararg = vararg
        self.body = body
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx), self.do_define, Finalizer(ctx)
        )
    #-def

    def do_define(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        qname = processor.mkqname(self.pname)
        ctx.env.setvar(
            self.pname,
            Procedure(self.pname, qname,
                self.bvars, self.params, self.vararg, self.body, ctx.env
            )
        )
        ctx.env.meta[self.pname].qname = qname
    #-def
#-class

class DefModule(Trackable):
    """
    """
    __slots__ = [ 'mname', 'body' ]

    def __init__(self, mname, body):
        """
        """

        Trackable.__init__(self)
        self.mname = mname
        self.body = body
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.create_module,
            self.do_defmodule,
            Finalizer(ctx)
        )
    #-def

    def create_module(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        m = Module(
            self.mname, processor.mkqname(self.mname), self.body, ctx.env
        )
        processor.insertcode(m, self.pushacc, m)
    #-def

    def do_defmodule(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        m = processor.acc()
        ctx.env.setvar(self.mname, m)
        ctx.env.meta[self.mname].qname = m.qname
        processor.setacc(processor.popval())
    #-def
#-class

class Operation(Trackable):
    """
    """
    OP_TAB = {
        # Arithmetic operations:
        'add': dict(
            types = [(NumericTypes, NumericTypes)],
            operation = (lambda a, b: a + b)
        ),
        'sub': dict(
            types = [(NumericTypes, NumericTypes)],
            operation = (lambda a, b: a - b)
        ),
        'mul': dict(
            types = [(NumericTypes, NumericTypes)],
            operation = (lambda a, b: a * b)
        ),
        'div': dict(
            types = [(NumericTypes, NumericTypes)],
            constraints = (lambda p, a, b: \
                (True, None, "") if b != 0 else \
                (False, p.ValueError, "Second operand must be non-zero")
            ),
            operation = (lambda a, b: a / b)
        ),
        'mod': dict(
            types = [(NumericTypes, NumericTypes)],
            constraints = (lambda p, a, b: \
                (True, None, "") if b != 0 else \
                (False, p.ValueError, "Second operand must be non-zero")
            ),
            operation = (lambda a, b: a % b)
        ),
        'neg': dict(
            types = [(NumericTypes,)],
            operation = (lambda a: -a)
        ),
        # Bitwise operations:
        'bitand': dict(
            types = [(int, int)],
            operation = (lambda a, b: a & b)
        ),
        'bitor': dict(
            types = [(int, int)],
            operation = (lambda a, b: a | b)
        ),
        'bitxor': dict(
            types = [(int, int)],
            operation = (lambda a, b: a ^ b)
        ),
        'shiftl': dict(
            types = [(int, int)],
            constraints = (lambda p, a, b: \
                (True, None, "") if b >= 0 else \
                (False, p.ValueError,
                    "Second operand must be a non-negative integer"
                )
            ),
            operation = (lambda a, b: a << b)
        ),
        'shiftr': dict(
            types = [(int, int)],
            constraints = (lambda p, a, b: \
                (True, None, "") if b >= 0 else \
                (False, p.ValueError,
                    "Second operand must be a non-negative integer"
                )
            ),
            operation = (lambda a, b: a >> b)
        ),
        'inv': dict(
            types = [(int,)],
            operation = (lambda a: ~a)
        ),
        # Comparison operations:
        'lt': dict(
            types = [(NumericTypes, NumericTypes), (str, str)],
            operation = (lambda a, b: a < b)
        ),
        'gt': dict(
            types = [(NumericTypes, NumericTypes), (str, str)],
            operation = (lambda a, b: a > b)
        ),
        'le': dict(
            types = [(NumericTypes, NumericTypes), (str, str)],
            operation = (lambda a, b: a <= b)
        ),
        'ge': dict(
            types = [(NumericTypes, NumericTypes), (str, str)],
            operation = (lambda a, b: a >= b)
        ),
        'eq': dict(
            types = [(object, object)],
            operation = (lambda a, b: a == b)
        ),
        'ne': dict(
            types = [(object, object)],
            operation = (lambda a, b: a != b)
        ),
        'is': dict(
            types = [(object, object)],
            operation = (lambda a, b: a is b)
        ),
        # Logic operations:
        # - 'and' and 'or' are defined separately
        'not': dict(
            types = [(bool,)],
            conversions = (lambda p, a: \
                False if a is p.Null else a
            ),
            operation = (lambda a: not a)
        ),
        # Collection operations:
        # - constructive:
        'newpair': dict(
            types = [(object, object)],
            operation = (lambda a, b: Pair(a, b))
        ),
        # 'newlist' and 'newhashmap' are defined separately
        'copy': dict(
            types = [(CollectionTypes,)],
            operation = (lambda a: \
                a.__class__(*(a if isinstance(a, Pair) else [a]))
            )
        ),
        'slice': dict(
            types = [(VariableLengthSequenceTypes, int, int)],
            operation = (lambda a, b, c: a.__class__(a[b:c]))
        ),
        'concat': dict(
            types = [(str, str)],
            operation = (lambda a, b: "%s%s" % (a, b))
        ),
        'join': dict(
            types = [(list, list)],
            operation = (lambda a, b: List(a + b))
        ),
        'merge': dict(
            types = [(dict, dict)],
            operation = (lambda a, b: HashMap.merge(a, b))
        ),
        # - informative:
        # 'type' is defined separately
        'instanceof': dict(
            types = [(object, object)],
            operation = (lambda a, b: isinstance(a, b))
        ),
        'strlen': dict(
            types = [(str,)],
            operation = (lambda a: len(a))
        ),
        'size': dict(
            types = [(CollectionTypes,)],
            operation = (lambda a: len(a))
        ),
        'empty': dict(
            types = [(CollectionTypes,)],
            operation = (lambda a: len(a) == 0)
        ),
        'contains': dict(
            types = [(CollectionTypes, object)],
            constraints = (lambda p, a, b: \
                (True, None, "") \
                if (isinstance(a, str) and isinstance(b, str)) \
                or not isinstance(a, str) \
                else (False, p.TypeError,
                    "Bad type of second operand (string was expected)"
                )
            ),
            operation = (lambda a, b: b in a)
        ),
        'count': dict(
            types = [(SequenceTypes, object)],
            constraints = (lambda p, a, b: \
                (True, None, "") \
                if (isinstance(a, str) and isinstance(b, str)) \
                or not isinstance(a, str) \
                else (False, p.TypeError,
                    "Bad type of second operand (string was expected)"
                )
            ),
            operation = (lambda a, b: a.count(b))
        ),
        'isdigit': dict(
            types = [(str,)],
            operation = (lambda a: a[0].isdigit() if a != "" else False)
        ),
        'isupper': dict(
            types = [(str,)],
            operation = (lambda a: a[0].isupper() if a != "" else False)
        ),
        'islower': dict(
            types = [(str,)],
            operation = (lambda a: a[0].islower() if a != "" else False)
        ),
        'isalpha': dict(
            types = [(str,)],
            operation = (lambda a: a[0].isalpha() if a != "" else False)
        ),
        'isletter': dict(
            types = [(str,)],
            operation = (lambda a: \
                a[0].isalpha() or a[0] == "_" if a != "" else False
            )
        ),
        'isalnum': dict(
            types = [(str,)],
            operation = (lambda a: a[0].isalnum() if a != "" else False)
        ),
        'isword': dict(
            types = [(str,)],
            operation = (lambda a: \
                a[0].isalnum() or a[0] == "_" if a != "" else False
            )
        ),
        'keys': dict(
            types = [(dict,)],
            operation = (lambda a: List(a.keys()))
        ),
        'values': dict(
            types = [(dict,)],
            operation = (lambda a: List(a.values()))
        ),
        # - elementwise:
        'first': dict(
            types = [(Pair,)],
            operation = (lambda a: a[0])
        ),
        'second': dict(
            types = [(Pair,)],
            operation = (lambda a: a[1])
        ),
        'getitem': dict(
            types = [(CollectionTypes, object)],
            constraints = (lambda p, a, b: \
                (True, None, "") if isinstance(a, dict) and b in a else \
                (True, None, "") if isinstance(a, SequenceTypes) \
                                 and isinstance(b, int) \
                                 and 0 <= b and b < len(a) else \
                (False, p.KeyError if isinstance(a, dict) else p.IndexError, \
                    "%r is not a valid key into the hashmap" % b \
                        if isinstance(a, dict) else \
                    "%r is not a valid index into the sequence" % b
                )
            ),
            operation = (lambda a, b: a[b])
        ),
        # - searching:
        'substr': dict(
            types = [(str, str)],
            operation = (lambda a, b: a.find(b))
        ),
        'find': dict(
            types = [(str, str, int, int)],
            operation = (lambda a, b, c, d: a.find(b, c, d))
        ),
        'rfind': dict(
            types = [(str, str, int, int)],
            operation = (lambda a, b, c, d: a.rfind(b, c, d))
        ),
        # - adjustments/miscellaneous:
        'lstrip': dict(
            types = [(str,)],
            operation = (lambda a: a.lstrip())
        ),
        'rstrip': dict(
            types = [(str,)],
            operation = (lambda a: a.rstrip())
        ),
        'strip': dict(
            types = [(str,)],
            operation = (lambda a: a.strip())
        ),
        'toupper': dict(
            types = [(str,)],
            operation = (lambda a: a.upper())
        ),
        'tolower': dict(
            types = [(str,)],
            operation = (lambda a: a.lower())
        ),
        'subst': dict(
            types = [(str, str, str)],
            operation = (lambda a, b, c: a.replace(b, c))
        ),
        'trans': dict(
            types = [(str, dict)],
            operation = (lambda a, b: ''.join([b.get(x, x) for x in a]))
        ),
        'head': dict(
            types = [(SequenceTypes,)],
            constraints = (lambda p, a: \
                (True, None, "") if len(a) >= 1 else \
                (False, p.ValueError, "Non-empty sequence was expected")
            ),
            operation = (lambda a: a[0])
        ),
        'tail': dict(
            types = [(SequenceTypes,)],
            constraints = (lambda p, a: \
                (True, None, "") if len(a) >= 1 else \
                (False, p.ValueError, "Non-empty sequence was expected")
            ),
            operation = (lambda a: \
                list(a[1:]) if isinstance(a, tuple) else a[1:]
            )
        ),
        'sort': dict(
            types = [(list,)],
            operation = (lambda a: (lambda l: l.sort() or l)(List(a)))
        ),
        'reverse': dict(
            types = [(list,)],
            operation = (lambda a: (lambda l: l.reverse() or l)(List(a)))
        ),
        'unique': dict(
            types = [(list,)],
            operation = (lambda a: List.unique(a))
        ),
        'split': dict(
            types = [(str, str)],
            operation = (lambda a, b: List(a.split(b)))
        )
    }
    __slots__ = [ 'operands' ]

    def __init__(self, *operands):
        """
        """

        Trackable.__init__(self)
        self.operands = operands
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        code = [Initializer(ctx)]
        for o in self.operands:
            code.extend([o, self.pushacc])
        code.extend([self.do_op, Finalizer(ctx)])
        processor.insertcode(*code)
    #-def

    def do_op(self, processor):
        """
        """

        # 1) Test whether the operation is defined:
        op_tab = self.__class__.OP_TAB
        if self.name not in op_tab:
            raise CommandError(processor.NameError,
                "Undefined operation '%s'" % self.name,
                processor.traceback()
            )

        # 2) Load operands:
        args, nargs = self.load_operands(processor)

        # 3) Load operation specification:
        op_spec = op_tab[self.name]

        # 4) Check if the number of operands coincides with the arity of the
        #    operator:
        types = op_spec['types']
        arity = len(types[0])
        if arity != nargs:
            raise CommandError(processor.TypeError,
                "%s: Exactly %d operand%s %s needed (%d %s given)" \
                % (
                    self.name,
                    arity,
                    "s" if arity != 1 else "",
                    "are" if arity != 1 else "is",
                    nargs,
                    "were" if nargs != 1 else "was"
                ),
                processor.traceback()
            )

        # 5) Do the occasional conversions:
        if 'conversions' in op_spec:
            conversions = op_spec['conversions']
            for i in range(arity):
                args[i] = conversions(processor, args[i])

        # 6) Check the types of operands:
        type_error, bo = False, None
        i = 0
        for typespec in types:
            type_error, bo = False, None
            for j in range(arity):
                if not isinstance(args[j], typespec[j]):
                    type_error, bo = True, args[j]
                    i = j
                    break
            if not type_error:
                break
        if type_error:
            raise CommandError(processor.TypeError,
                "%s: Bad type of the %d%s operand (%r)" \
                % (
                    self.name,
                    i + 1,
                    "st" if (i % 10) == 0 and (i % 100) != 10 else \
                    "nd" if (i % 10) == 1 and (i % 100) != 11 else \
                    "rd" if (i % 10) == 2 and (i % 100) != 12 else \
                    "th",
                    bo
                ),
                processor.traceback()
            )

        # 7) Test the occasional constraints:
        r, e, m = op_spec.get('constraints', (lambda p, *x: (True, None, "")))(
            processor, *args
        )
        if not r:
            raise CommandError(
                e, "%s: %s" % (self.name, m), processor.traceback()
            )

        # 8) Do the operation:
        processor.setacc(op_spec['operation'](*args))
    #-def

    def load_operands(self, processor):
        """
        """

        args = []
        for _ in self.operands:
            args.append(processor.popval())
        args.reverse()
        return args, len(args)
    #-def
#-class

class Add(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Sub(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Mul(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Div(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Mod(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Neg(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class BitAnd(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class BitOr(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class BitXor(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class ShiftL(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class ShiftR(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Inv(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Lt(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Gt(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Le(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Ge(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Eq(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Ne(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Is(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class AndOr(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.operands[0],
            self.pushacc,
            self.to_bool,
            self.do_andor,
            Finalizer(ctx)
        )
    #-def

    def to_bool(self, processor):
        """
        """

        processor.insertcode(ToBool(processor.acc()))
    #-def

    def do_andor(self, processor):
        """
        """

        bool_a = processor.acc()
        orig_a = processor.popval()

        if self.__class__ is Or:
            if bool_a:
                processor.setacc(orig_a)
            else:
                processor.insertcode(self.operands[1])
        else:
            if bool_a:
                processor.insertcode(self.operands[1])
            else:
                processor.setacc(orig_a)
    #-def
#-class

class And(AndOr):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        AndOr.__init__(self, a, b)
    #-def
#-class

class Or(AndOr):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        AndOr.__init__(self, a, b)
    #-def
#-class

class Not(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class NewPair(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class NewList(Operation):
    """
    """
    __slots__ = []

    def __init__(self, *items):
        """
        """

        Operation.__init__(self, *items)
    #-def

    def do_op(self, processor):
        """
        """

        processor.setacc(List(self.load_operands(processor)[0]))
    #-def
#-class

class NewHashMap(Operation):
    """
    """
    __slots__ = []

    def __init__(self, *items):
        """
        """

        Operation.__init__(self, *items)
    #-def

    def do_op(self, processor):
        """
        """

        items, _ = self.load_operands(processor)

        for n, i in enumerate(items, 1):
            if not isinstance(i, tuple) or len(i) != 2:
                raise CommandError(processor.TypeError,
                    "%s: %d%s argument must be a pair" % (
                        self.name,
                        n,
                        "st" if (n % 10) == 1 and (n % 100) != 11 else \
                        "nd" if (n % 10) == 2 and (n % 100) != 12 else \
                        "rd" if (n % 10) == 3 and (n % 100) != 13 else \
                        "th"
                    ),
                    processor.traceback()
                )
        processor.setacc(HashMap(dict(items)))
    #-def
#-class

class Copy(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Slice(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c):
        """
        """

        Operation.__init__(self, a, b, c)
    #-def
#-class

class Concat(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Join(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Merge(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Type(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def

    def do_op(self, processor):
        """
        """

        a = processor.popval()
        for t in processor.types():
            if isinstance(a, t):
                processor.setacc(t)
                return
        raise CommandError(processor.TypeError,
            "%s: Unknown type" % self.name,
            processor.traceback()
        )
    #-def
#-class

class InstanceOf(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Strlen(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Size(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Empty(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Contains(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Count(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class IsDigit(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsUpper(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsLower(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsAlpha(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsLetter(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsAlnum(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsWord(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Keys(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Values(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class First(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Second(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class GetItem(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Substr(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Find(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c, d):
        """
        """

        Operation.__init__(self, a, b, c, d)
    #-def
#-class

class RFind(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c, d):
        """
        """

        Operation.__init__(self, a, b, c, d)
    #-def
#-class

class LStrip(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class RStrip(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Strip(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class ToUpper(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class ToLower(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Subst(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c):
        """
        """

        Operation.__init__(self, a, b, c)
    #-def
#-class

class Trans(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Head(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Tail(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Sort(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Reverse(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Unique(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Split(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class ToBool(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def

    def do_op(self, processor):
        """
        """

        arg = processor.popval()
        if isinstance(arg, bool):
            processor.setacc(arg)
        elif isinstance(arg, NumericTypes):
            processor.setacc(arg != 0)
        elif isinstance(arg, CollectionTypes):
            processor.setacc(len(arg) > 0)
        elif isinstance(arg, UserType):
            processor.setacc(arg.to_bool(processor))
        elif isinstance(arg, Procedure):
            processor.setacc(True)
        elif arg is processor.Null:
            processor.setacc(False)
        else:
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
    #-def
#-class

class ToInt(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def

    def do_op(self, processor):
        """
        """

        arg = processor.popval()
        if isinstance(arg, bool):
            processor.setacc(1 if arg else 0)
        elif isinstance(arg, NumericTypes):
            processor.setacc(int(arg))
        elif isinstance(arg, str):
            try:
                processor.setacc(int(arg))
            except ValueError:
                try:
                    processor.setacc(int(float(arg)))
                except ValueError:
                    raise CommandError(processor.ValueError,
                        "%s: String to integer conversion failed" % self.name,
                        processor.traceback()
                    )
        elif isinstance(arg, UserType):
            processor.setacc(arg.to_int(processor))
        else:
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
    #-def
#-class

class ToFlt(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def

    def do_op(self, processor):
        """
        """

        arg = processor.popval()
        if isinstance(arg, bool):
            processor.setacc(1.0 if arg else 0.0)
        elif isinstance(arg, NumericTypes):
            processor.setacc(float(arg))
        elif isinstance(arg, str):
            try:
                processor.setacc(float(arg))
            except ValueError:
                raise CommandError(processor.ValueError,
                    "%s: String to float conversion failed" % self.name,
                    processor.traceback()
                )
        elif isinstance(arg, UserType):
            processor.setacc(arg.to_float(processor))
        else:
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
    #-def
#-class

class ToStr(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b = {}):
        """
        """

        Operation.__init__(self, a, b)
    #-def

    def do_op(self, processor):
        """
        """

        convspec = processor.popval()
        if not isinstance(convspec, dict):
            raise CommandError(processor.TypeError,
                "%s: Conversion specifications must be stored in hashmap" \
                % self.name,
                processor.traceback()
            )
        arg = processor.popval()
        if isinstance(arg, bool):
            sTrue = convspec.get('strue', "true")
            sFalse = convspec.get('sfalse', "false")
            if not isinstance(sTrue, str) or not isinstance(sFalse, str):
                raise CommandError(processor.TypeError,
                    "%s: The names of booleans constants must be strings" \
                    % self.name,
                    processor.traceback()
                )
            processor.setacc(sTrue if arg is True else sFalse)
        elif isinstance(arg, int):
            processor.setacc(self.makefmt(
                processor, convspec, ("i", ("d", "o", "x", "X"))
            ) % arg)
        elif isinstance(arg, float):
            processor.setacc(self.makefmt(
                processor, convspec, ("f", ("f", "e", "E"))
            ) % arg)
        elif isinstance(arg, str):
            processor.setacc(arg)
        elif isinstance(arg, UserType):
            processor.setacc(arg.to_str(processor))
        elif isinstance(arg, Procedure):
            processor.setacc(arg[0])
        elif arg is processor.Null:
            sNull = convspec.get('snull', "null")
            if not isinstance(sNull, str):
                raise CommandError(processor.TypeError,
                    "%s: The name of null constant must be string" % self.name,
                    processor.traceback()
                )
            processor.setacc(sNull)
        else:
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
    #-def

    def makefmt(self, processor, spec, tspec):
        """
        """

        p, types = tspec
        flags = spec.get('%sflags' % p, spec.get('flags', ""))
        if not isinstance(flags, str) or len(set(flags) - set("-+ 0")) > 0:
            raise CommandError(processor.TypeError,
                "%s: Bad flag specifier ('-', '+', ' ', '0')" % self.name,
                processor.traceback()
            )
        size = spec.get('%ssize' % p, spec.get('size', 0))
        if not isinstance(size, int):
            raise CommandError(processor.TypeError,
                "%s: Size specifier must be integer" % self.name,
                processor.traceback()
            )
        size = "" if size < 1 else "%d" % size
        prec = spec.get('%sprec' % p, spec.get('prec', -1))
        if not isinstance(prec, int):
            raise CommandError(processor.TypeError,
                "%s: Precision specifier must be integer" % self.name,
                processor.traceback()
            )
        prec = "" if prec < 0 else ".%d" % prec
        type = spec.get('%stype' % p, types[0])
        if type not in types:
            raise CommandError(processor.TypeError,
                "%s: Bad display type %r" % (self.name, types),
                processor.traceback()
            )
        return "%%%s%s%s%s" % (flags, size, prec, type)
    #-def
#-class

class ToPair(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def

    def do_op(self, processor):
        """
        """

        arg = processor.popval()
        if isinstance(arg, SequenceTypes):
            if len(arg) != 2:
                raise CommandError(processor.ValueError,
                    "%s: A pair can be made only from a sequence of length 2" \
                    % self.name,
                    processor.traceback()
                )
            processor.setacc(Pair(arg[0], arg[1]))
        elif isinstance(arg, UserType):
            processor.setacc(arg.to_pair(processor))
        else:
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
    #-def
#-class

class ToList(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def

    def do_op(self, processor):
        """
        """

        arg = processor.popval()
        if isinstance(arg, SequenceTypes):
            processor.setacc(List(arg))
        elif isinstance(arg, dict):
            l = List()
            for k in arg:
                l.append(Pair(k, arg[k]))
            processor.setacc(l)
        elif isinstance(arg, UserType):
            processor.setacc(arg.to_list(processor))
        else:
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
    #-def
#-class

class ToHash(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def

    def do_op(self, processor):
        """
        """

        arg = processor.popval()
        if isinstance(arg, Pair):
            arg = [arg]
        if isinstance(arg, list):
            for x in arg:
                if not isinstance(x, tuple) or len(x) != 2:
                    raise CommandError(processor.ValueError,
                        "%s: A pair was expected inside list" % self.name,
                        processor.traceback()
                    )
        if isinstance(arg, (list, dict)):
            processor.setacc(HashMap(arg))
        elif isinstance(arg, UserType):
            processor.setacc(arg.to_hash(processor))
        else:
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
    #-def
#-class

class Quantifier(Operation):
    """
    """
    __slots__ = [ 'iv', 'cf' ]

    def __init__(self, a, b, iv, cf):
        """
        """

        Operation.__init__(self, a, b)
        self.iv = iv
        self.cf = cf
    #-def

    def do_op(self, processor):
        """
        """

        state = {}
        proc = processor.popval()
        if not isinstance(proc, Procedure):
            raise CommandError(processor.TypeError,
                "%s: Bad type of 2nd operand" % self.name,
                processor.traceback()
            )
        state[0] = proc
        it = processor.popval()
        if isinstance(it, str):
            it = List(it)
        if not isinstance(it, CollectionTypes):
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
        state[1] = it.iterator()
        state[1].reset()
        state[2] = self.iv
        processor.insertcode(state, self.pushacc, self.do_next)
    #-def

    def do_next(self, processor):
        """
        """

        state = processor.topval()
        x = state[1].next()
        if x is state[1]:
            processor.setacc(state[2])
            processor.popval()
            return
        processor.insertcode(
            Call(state[0], x), self.do_contribute, self.do_next
        )
    #-def

    def do_contribute(self, processor):
        """
        """

        state = processor.topval()
        r = processor.acc()
        if not isinstance(r, bool):
            raise CommandError(processor.TypeError,
                "%s: Function %s should return boolean value" \
                % (self.name, state[0][0]),
                processor.traceback()
            )
        state[2] = self.cf(state[2], r)
    #-def
#-class

class All(Quantifier):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Quantifier.__init__(self, a, b, True, (lambda a, b: a and b))
    #-def
#-class

class Any(Quantifier):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Quantifier.__init__(self, a, b, False, (lambda a, b: a or b))
    #-def
#-class

class SeqOp(Operation):
    """
    """
    __slots__ = [ 'opf' ]

    def __init__(self, a, b, opf):
        """
        """

        Operation.__init__(self, a, b)
        self.opf = opf
    #-def

    def do_op(self, processor):
        """
        """

        state = {}
        proc = processor.popval()
        if not isinstance(proc, Procedure):
            raise CommandError(processor.TypeError,
                "%s: Bad type of 2nd operand" % self.name,
                processor.traceback()
            )
        state[0] = proc
        it = processor.popval()
        if not isinstance(it, SequenceTypes):
            raise CommandError(processor.TypeError,
                "%s: Bad type of 1st operand" % self.name,
                processor.traceback()
            )
        if isinstance(it, str):
            it = List(it)
        state[1] = it.iterator()
        state[1].reset()
        state[2] = List()
        processor.insertcode(state, self.pushacc, self.do_next)
    #-def

    def do_next(self, processor):
        """
        """

        state = processor.topval()
        x = state[1].next()
        if x is state[1]:
            processor.setacc(state[2])
            processor.popval()
            return
        processor.insertcode(
            Call(self.opf, state[0], x), self.do_contribute, self.do_next
        )
    #-def

    def do_contribute(self, processor):
        """
        """

        state = processor.topval()
        r = processor.acc()
        if not isinstance(r, Pair):
            raise CommandError(processor.TypeError,
                "%s: Function %s should return a pair" \
                % (self.name, state[0][0]),
                processor.traceback()
            )
        result, keep_result = r
        if not isinstance(keep_result, bool):
            raise CommandError(processor.TypeError,
                "%s: Function %s should return a pair (any, boolean)" \
                % (self.name, state[0][0]),
                processor.traceback()
            )
        if keep_result:
            state[2].append(result)
    #-def
#-class

class Map(SeqOp):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        SeqOp.__init__(self, a, b, Lambda(["f", "x"], False, [
            Return(NewPair(Call(GetLocal("f"), GetLocal("x")), True))
        ], []))
    #-def
#-class

class Filter(SeqOp):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        SeqOp.__init__(self, a, b, Lambda(["p", "x"], False, [
            Return(NewPair(GetLocal("x"), Call(GetLocal("p"), GetLocal("x"))))
        ], []))
    #-def
#-class

class Lambda(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c, d):
        """
        """

        Operation.__init__(self, a, b, c, d)
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(Initializer(ctx), self.do_op, Finalizer(ctx))
    #-def

    def do_op(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        params, vararg, body, bvars = self.operands
        processor.setacc(Procedure("<lambda>", processor.mkqname("<lambda>"),
            bvars, params, vararg, body, ctx.env
        ))
    #-def
#-class

class Block(Trackable):
    """
    """
    __slots__ = [ 'commands' ]

    def __init__(self, *commands):
        """
        """

        Trackable.__init__(self)
        self.commands = commands
    #-def

    def enter(self, processor, inlz):
        """
        """

        inlz.ctx.env = processor.newenv()
        inlz.ctx.nvals = processor.nvals()
        processor.pushctx(inlz.ctx)
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            *((Initializer(ctx),) + self.commands + (Finalizer(ctx),))
        )
    #-def
#-class

class If(Trackable):
    """
    """
    __slots__ = [ 'c', 't', 'e' ]

    def __init__(self, c, t, e):
        """
        """

        Trackable.__init__(self)
        self.c = c
        self.t = t
        self.e = e
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx), ToBool(self.c), self.do_if, Finalizer(ctx)
        )
    #-def

    def do_if(self, processor):
        """
        """

        processor.insertcode(
            *(self.t if processor.acc() else self.e)
        )
    #-def
#-class

class Loop(Trackable):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Trackable.__init__(self)
    #-def

    def isloop(self):
        """
        """

        return True
    #-def
#-class

class Foreach(Loop):
    """
    """
    __slots__ = [ 'var', 'qvar', 'itexp', 'body' ]

    def __init__(self, var, itexp, body):
        """
        """

        Loop.__init__(self)
        self.var = var
        self.qvar = var
        self.itexp = itexp
        self.body = tuple(body)
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        self.qvar = processor.mkqname(self.var)
        processor.insertcode(
            Initializer(ctx), self.itexp, self.do_foreach, Finalizer(ctx)
        )
    #-def

    def do_foreach(self, processor):
        """
        """

        state = {}
        it = processor.acc()
        if not isinstance(it, CollectionTypes):
            raise CommandError(processor.TypeError,
                "%s: Object must be iterable" % self.name,
                processor.traceback()
            )
        if isinstance(it, str):
            it = List(it)
        state[0] = it.iterator()
        state[0].reset()
        processor.insertcode(state, self.pushacc, self.do_loop)
    #-def

    def do_loop(self, processor):
        """
        """

        state = processor.topval()
        x = state[0].next()
        if x is state[0]:
            processor.popval()
            return
        processor.insertcode(
            *((x, self.do_setvar) + self.body + (self.do_loop,))
        )
    #-def

    def do_setvar(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        ctx.env.setvar(self.var, processor.acc())
        ctx.env.meta[self.var].qname = self.qvar
    #-def

    def do_continue(self, processor):
        """
        """

        processor.insertcode(self.do_loop)
    #-def
#-class

class While(Loop):
    """
    """
    __slots__ = [ 'c', 'b' ]

    def __init__(self, c, b):
        """
        """

        Loop.__init__(self)
        self.c = c
        self.b = tuple(b)
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(Initializer(ctx), self.do_while, Finalizer(ctx))
    #-def

    def do_while(self, processor):
        """
        """

        processor.insertcode(ToBool(self.c), self.do_next)
    #-def

    def do_next(self, processor):
        """
        """

        if processor.acc():
            processor.insertcode(*(self.b + (self.do_while,)))
    #-def

    def do_continue(self, processor):
        """
        """

        processor.insertcode(self.do_while)
    #-def
#-class

class DoWhile(Loop):
    """
    """
    __slots__ = [ 'b', 'c' ]

    def __init__(self, b, c):
        """
        """

        Loop.__init__(self)
        self.b = tuple(b)
        self.c = c
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(Initializer(ctx), self.do_dowhile, Finalizer(ctx))
    #-def

    def do_dowhile(self, processor):
        """
        """

        processor.insertcode(*(self.b + (ToBool(self.c), self.do_next)))
    #-def

    def do_next(self, processor):
        """
        """

        if processor.acc():
            processor.insertcode(self.do_dowhile)
    #-def

    def do_continue(self, processor):
        """
        """

        processor.insertcode(ToBool(self.c), self.do_next)
    #-def
#-class

class Break(Command):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Command.__init__(self)
    #-def

    def expand(self, processor):
        """
        """

        processor.handle_event(BREAK, None)
    #-def
#-class

class Continue(Command):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Command.__init__(self)
    #-def

    def expand(self, processor):
        """
        """

        processor.handle_event(CONTINUE, None)
    #-def
#-class

class Closure(Trackable):
    """
    """
    __slots__ = [ 'bvars', 'args', 'body', 'outer' ]

    def __init__(self, name, qname, bvars, args, body, outer):
        """
        """

        Trackable.__init__(self)
        self.name = name
        self.qname = qname
        self.bvars = bvars
        self.args = args
        self.body = tuple(body)
        self.outer = outer
    #-def

    def isfunc(self):
        """
        """

        return True
    #-def

    def enter(self, processor, inlz):
        """
        """

        inlz.ctx.env = processor.newenv(self.outer)
        for bvar in self.bvars:
            inlz.ctx.env.setvar(bvar, processor.Null)
            inlz.ctx.env.meta[bvar].qname = "%s::%s" % (self.qname, bvar)
        for argname in self.args:
            inlz.ctx.env.setvar(argname, self.args[argname])
            inlz.ctx.env.meta[argname].qname = "%s::%s" % (self.qname, argname)
        inlz.ctx.nvals = processor.nvals()
        processor.pushctx(inlz.ctx)
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            *((Initializer(ctx),) + self.body + (Finalizer(ctx),))
        )
    #-def
#-class

class ICall(Command):
    """
    """
    __slots__ = [ 'proc' ]

    def __init__(self, proc):
        """
        """

        Command.__init__(self)
        self.proc = proc
    #-def

    def expand(self, processor):
        """
        """

        args = processor.popval()
        name, qname, bvars, _, _, body, outer = self.proc
        processor.insertcode(Closure(name, qname, bvars, args, body, outer))
    #-def
#-class

class Call(Trackable):
    """
    """
    __slots__ = [ 'proc', 'args', 'evargs', 'valist' ]

    def __init__(self, proc, *args):
        """
        """

        Trackable.__init__(self)
        self.proc = proc
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx), self.proc, self.do_call, Finalizer(ctx)
        )
    #-def

    def do_call(self, processor):
        """
        """

        proc = processor.acc()
        if not isinstance(proc, Procedure):
            raise CommandError(processor.TypeError,
                "%s: Procedure expected" % self.name,
                processor.traceback()
            )
        _, _, _, params, vararg, _, _ = proc
        nargs, nparams = len(self.args), len(params)
        argsokf = (lambda na, np: np > 0 and na >= np - 1) if vararg \
            else (lambda na, np: na == np)
        if not argsokf(nargs, nparams):
            raise CommandError(processor.TypeError,
                "%s %s (%s): Bad count of arguments" % (
                    self.name, proc[0], proc[1]
                ),
                processor.traceback()
            )
        code = [{}, self.pushacc]
        nreqargs = nparams - 1 if vararg else nparams
        i = 0
        while i < nreqargs:
            code.extend([self.args[i], self.pushacc, params[i], self.do_arg])
            i += 1
        if vararg:
            code.extend([[], self.pushacc])
        while i < nargs:
            code.extend([self.args[i], self.do_vararg])
            i += 1
        if vararg:
            code.extend([params[-1], self.finish_varargs])
        code.append(ICall(proc))
        processor.insertcode(*code)
    #-def

    def do_arg(self, processor):
        """
        """

        name = processor.acc()
        value = processor.popval()
        processor.topval()[name] = value
    #-def

    def do_vararg(self, processor):
        """
        """

        processor.topval().append(processor.acc())
    #-def

    def finish_varargs(self, processor):
        """
        """

        name = processor.acc()
        valist = processor.popval()
        processor.topval()[name] = valist
    #-def
#-class

class ECall(Trackable):
    """
    """
    __slots__ = [ 'proc', 'args' ]

    def __init__(self, proc, *args):
        """
        """

        Trackable.__init__(self)
        self.proc = proc
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.do_args,
            self.do_ecall,
            Finalizer(ctx)
        )
    #-def

    def do_args(self, processor):
        """
        """

        if not hasattr(self.proc, '__call__'):
            raise CommandError(processor.TypeError,
                "%s: External procedure must be callable" % self.name,
                processor.traceback()
            )
        code = [[], self.pushacc]
        for x in self.args:
            code.extend([x, self.do_arg])
        processor.insertcode(*code)
    #-def

    def do_arg(self, processor):
        """
        """

        processor.topval().append(processor.acc())
    #-def

    def do_ecall(self, processor):
        """
        """

        try:
            args = processor.popval()
            r = self.proc(*args)
            processor.insertcode(r)
        except CommandError as e:
            processor.insertcode(e)
        except:
            raise CommandError(processor.TypeError,
                "%s: Calling the external procedure has failed" % self.name,
                processor.traceback()
            )
    #-def
#-class

class Return(Command):
    """
    """
    __slots__ = [ 'expr' ]

    def __init__(self, expr = None):
        """
        """

        Command.__init__(self)
        self.expr = expr
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(self.expr, self.do_return)
    #-def

    def do_return(self, processor):
        """
        """

        processor.handle_event(RETURN, None, processor.acc())
    #-def
#-class

class TryCatchFinally(Trackable):
    """
    """
    __slots__ = [ 'b', 'h', 'f' ]

    def __init__(self, b, h, f):
        """
        """

        Trackable.__init__(self)
        self.b = tuple(b)
        self.h = h
        self.f = f
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            *((Initializer(ctx),) + self.b + (Finalizer(ctx, self.f),))
        )
    #-def

    def find_exception_handler(self, ctx, e):
        """
        """

        try:
            if not (
                isinstance(e, CommandError)
                and isinstance(e.ecls, ExceptionClass)
            ):
                return None
            for name, vname, handler in self.h:
                ec = ctx.env.getvar(name)
                if isderived(e.ecls, ec):
                    if vname:
                        ctx.env.setvar(vname, e)
                        p = ctx.env.processor
                        ctx.env.meta[vname].qname = p.mkqname(vname)
                    return handler
            return None
        except CommandError as ce:
            return [ce]
    #-def
#-class

class Throw(Trackable):
    """
    """
    __slots__ = [ 'ecls', 'msg' ]

    def __init__(self, ecls, msg):
        """
        """

        Trackable.__init__(self)
        self.ecls = ecls
        self.msg = msg
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.ecls, self.pushacc,
            self.msg,
            self.do_throw,
            Finalizer(ctx)
        )
    #-def

    def do_throw(self, processor):
        """
        """

        msg = processor.acc()
        ecls = processor.popval()

        if not isinstance(ecls, ExceptionClass):
            raise CommandError(processor.TypeError,
                "%s: Error class expected" % self.name,
                processor.traceback()
            )
        if not isinstance(msg, str):
            raise CommandError(processor.TypeError,
                "%s: Error message must be string" % self.name,
                processor.traceback()
            )
        raise CommandError(ecls, msg, processor.traceback())
    #-def
#-class

class Rethrow(Trackable):
    """
    """
    __slots__ = [ 'e' ]

    def __init__(self, e):
        """
        """

        Trackable.__init__(self)
        self.e = e
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx), self.e, self.do_rethrow, Finalizer(ctx)
        )
    #-def

    def do_rethrow(self, processor):
        """
        """

        e = processor.acc()
        if not isinstance(e, CommandError):
            raise CommandError(processor.TypeError,
                "%s: Only command error can be thrown" % self.name,
                processor.traceback()
            )
        processor.insertcode(e)
    #-def
#-class

class SandBox(Trackable):
    """
    """
    __slots__ = [ 'cmds' ]

    def __init__(self, cmds):
        """
        """

        Trackable.__init__(self)
        self.cmds = tuple(cmds)
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(*(
            (Initializer(ctx),) + self.cmds + (Finalizer(ctx, sb = True),)
        ))
    #-def
#-class

class SetItem(Trackable):
    """
    """
    __slots__ = [ 'container', 'index', 'value' ]

    def __init__(self, container, index, value):
        """
        """

        Trackable.__init__(self)
        self.container = container
        self.index = index
        self.value = value
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.container, self.pushacc,
            self.index, self.pushacc,
            self.value,
            self.do_setitem,
            Finalizer(ctx)
        )
    #-def

    def do_setitem(self, processor):
        """
        """

        value = processor.acc()
        index = processor.popval()
        container = processor.popval()

        if not isinstance(container, (list, dict)):
            raise CommandError(processor.TypeError,
                "%s: Container must be list or hashmap" % self.name,
                processor.traceback()
            )
        if isinstance(container, list) and not (
            isinstance(index, int) and 0 <= index and index < len(container)
        ):
            raise CommandError(processor.IndexError,
                "%s: Invalid index" % self.name,
                processor.traceback()
            )
        container[index] = value
    #-def
#-class

class DelItem(Trackable):
    """
    """
    __slots__ = [ 'container', 'index' ]

    def __init__(self, container, index):
        """
        """

        Trackable.__init__(self)
        self.container = container
        self.index = index
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.container, self.pushacc,
            self.index,
            self.do_delitem,
            Finalizer(ctx)
        )
    #-def

    def do_delitem(self, processor):
        """
        """

        index = processor.acc()
        container = processor.popval()

        if not isinstance(container, (list, dict)):
            raise CommandError(processor.TypeError,
                "%s: Container must be list or hashmap" % self.name,
                processor.traceback()
            )
        if isinstance(container, list) and not (
            isinstance(index, int) and 0 <= index and index < len(container)
        ):
            raise CommandError(processor.IndexError,
                "%s: Invalid index" % self.name,
                processor.traceback()
            )
        if isinstance(container, dict) and index not in container:
            return
        del container[index]
    #-def
#-class

class Append(Trackable):
    """
    """
    __slots__ = [ 'l', 'v' ]

    def __init__(self, l, v):
        """
        """

        Trackable.__init__(self)
        self.l = l
        self.v = v
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.l, self.pushacc,
            self.v,
            self.do_append,
            Finalizer(ctx)
        )
    #-def

    def do_append(self, processor):
        """
        """

        v = processor.acc()
        l = processor.popval()

        if not isinstance(l, list):
            raise CommandError(processor.TypeError,
                "%s: A list was expected" % self.name,
                processor.traceback()
            )
        l.append(v)
    #-def
#-class

class Insert(Trackable):
    """
    """
    __slots__ = [ 'l', 'i', 'v' ]

    def __init__(self, l, i, v):
        """
        """

        Trackable.__init__(self)
        self.l = l
        self.i = i
        self.v = v
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.l, self.pushacc,
            self.i, self.pushacc,
            self.v,
            self.do_insert,
            Finalizer(ctx)
        )
    #-def

    def do_insert(self, processor):
        """
        """

        v = processor.acc()
        i = processor.popval()
        l = processor.popval()

        if not isinstance(l, list):
            raise CommandError(processor.TypeError,
                "%s: A list was expected" % self.name,
                processor.traceback()
            )
        if not (isinstance(i, int) and 0 <= i and i <= len(l)):
            raise CommandError(processor.IndexError,
                "%s: Bad index" % self.name,
                processor.traceback()
            )
        l.insert(i, v)
    #-def
#-class

class Remove(Trackable):
    """
    """
    __slots__ = [ 'l', 'x' ]

    def __init__(self, l, x):
        """
        """

        Trackable.__init__(self)
        self.l = l
        self.x = x
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.l, self.pushacc,
            self.x,
            self.do_remove,
            Finalizer(ctx)
        )
    #-def

    def do_remove(self, processor):
        """
        """

        x = processor.acc()
        l = processor.popval()

        if not isinstance(l, list):
            raise CommandError(processor.TypeError,
                "%s: A list was expected" % self.name,
                processor.traceback()
            )
        if x in l:
            l.remove(x)
    #-def
#-class

class RemoveAll(Trackable):
    """
    """
    __slots__ = [ 'l', 'x' ]

    def __init__(self, l, x):
        """
        """

        Trackable.__init__(self)
        self.l = l
        self.x = x
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.l, self.pushacc,
            self.x,
            self.do_removeall,
            Finalizer(ctx)
        )
    #-def

    def do_removeall(self, processor):
        """
        """

        x = processor.acc()
        l = processor.popval()

        if not isinstance(l, list):
            raise CommandError(processor.TypeError,
                "%s: A list was expected" % self.name,
                processor.traceback()
            )
        while x in l:
            l.remove(x)
    #-def
#-class

class Each(Trackable):
    """
    """
    __slots__ = [ 'l', 'f', 'args' ]

    def __init__(self, l, f, *args):
        """
        """

        Trackable.__init__(self)
        self.l = l
        self.f = f
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.l, self.pushacc,
            self.f,
            self.do_each,
            Finalizer(ctx)
        )
    #-def

    def do_each(self, processor):
        """
        """

        f = processor.acc()
        l = processor.popval()

        if not isinstance(l, list):
            raise CommandError(processor.TypeError,
                "%s: A list was expected" % self.name,
                processor.traceback()
            )
        if not isinstance(f, Procedure):
            raise CommandError(processor.TypeError,
                "%s: A function was expected" % self.name,
                processor.traceback()
            )
        state = {0: l.iterator(), 1: f, 2: List()}
        state[0].reset()
        processor.insertcode(state, self.pushacc, self.do_args, self.do_next)
    #-def

    def do_args(self, processor):
        """
        """

        code = []
        for x in self.args:
            code.extend([x, self.do_arg])
        processor.insertcode(*code)
    #-def

    def do_arg(self, processor):
        """
        """

        state = processor.topval()
        state[2].append(processor.acc())
    #-def

    def do_next(self, processor):
        """
        """

        state = processor.topval()
        x = state[0].next()
        if x is state[0]:
            processor.popval()
            return
        processor.insertcode(
            Call(state[1], x, *(state[2])), self.do_next
        )
    #-def
#-class

class Visit(Trackable):
    """
    """
    __slots__ = [ 'ut', 'f', 'args' ]

    def __init__(self, ut, f, *args):
        """
        """

        Trackable.__init__(self)
        self.ut = ut
        self.f = f
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.ut, self.pushacc,
            self.f,
            self.do_visit,
            Finalizer(ctx)
        )
    #-def

    def do_visit(self, processor):
        """
        """

        f = processor.acc()
        ut = processor.popval()

        if not isinstance(ut, UserType):
            raise CommandError(processor.TypeError,
                "%s: A UserType object was expected" % self.name,
                processor.traceback()
            )
        if not isinstance(f, Procedure):
            raise CommandError(processor.TypeError,
                "%s: A function was expected" % self.name,
                processor.traceback()
            )
        state = {0: ut, 1: f, 2: List()}
        processor.insertcode(state, self.pushacc, self.do_args, self.do_ivisit)
    #-def

    def do_args(self, processor):
        """
        """

        code = []
        for x in self.args:
            code.extend([x, self.do_arg])
        processor.insertcode(*code)
    #-def

    def do_arg(self, processor):
        """
        """

        state = processor.topval()
        state[2].append(processor.acc())
    #-def

    def do_ivisit(self, processor):
        """
        """

        state = processor.popval()
        state[0].do_visit(processor, state[1], *(state[2]))
    #-def
#-class

class Print(Trackable):
    """
    """
    __slots__ = [ 'args' ]

    def __init__(self, *args):
        """
        """

        Trackable.__init__(self)
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        code = [Initializer(ctx)]
        for arg in self.args:
            code.extend([ToStr(arg), self.do_print_arg])
        code.append(Finalizer(ctx))
        processor.insertcode(*code)
    #-def

    def do_print_arg(self, processor):
        """
        """

        processor.print_impl(processor.acc())
    #-def
#-class

class Module(Trackable):
    """
    """
    INIT = 0
    INITIALIZED = 1
    ERROR = 2
    THISVARNAME = 'this'
    __slots__ = [ 'body', 'outer', 'state', 'ctx' ]

    def __init__(self, name, qname, body, outer):
        """
        """

        Trackable.__init__(self)
        self.name = name
        self.qname = qname
        self.body = tuple(body)
        self.outer = outer
        self.state = self.__class__.INIT
        self.ctx = CommandContext(self)
    #-def

    def isfunc(self):
        """
        """

        return True
    #-def

    def enter(self, processor, inlz):
        """
        """

        if inlz.ctx.env is None:
            inlz.ctx.env = processor.newenv(self.outer)
        sthis = self.__class__.THISVARNAME
        inlz.ctx.env.setvar(sthis, self)
        inlz.ctx.env.meta[sthis].qname = "%s::%s" % (self.qname, sthis)
        inlz.ctx.nvals = processor.nvals()
        processor.pushctx(inlz.ctx)
    #-def

    def expand(self, processor):
        """
        """

        if self.state == self.__class__.INITIALIZED:
            processor.setacc(self)
            return
        inlz = Initializer(self.ctx)
        fnlz = Finalizer(self.ctx,
            after = [self.set_initialized], on_throw = self.set_error
        )
        processor.insertcode(*((inlz,) + self.body + (self.return_this, fnlz)))
    #-def

    def return_this(self, processor):
        """
        """

        processor.setacc(self)
    #-def

    def set_initialized(self, processor):
        """
        """

        self.state = self.__class__.INITIALIZED
    #-def

    def set_error(self, fnlz, processor, e):
        """
        """

        self.state = self.__class__.ERROR
    #-def
#-class

class MainModule(Module):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Module.__init__(self, "", "", [], None)
    #-def

    def enter(self, processor, inlz):
        """
        """

        inlz.ctx.env = processor.getenv()
        Module.enter(self, processor, inlz)
    #-def
#-class

class SetMember(Trackable):
    """
    """
    __slots__ = [ 'module', 'member', 'value' ]

    def __init__(self, module, member, value):
        """
        """

        Trackable.__init__(self)
        self.module = module
        self.member = member
        self.value = value
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.module, self.pushacc,
            self.value,
            self.do_setmember,
            Finalizer(ctx)
        )
    #-def

    def do_setmember(self, processor):
        """
        """

        value = processor.acc()
        module = processor.popval()

        if not isinstance(module, Module):
            raise CommandError(processor.TypeError,
                "%s: Module expected" % self.name,
                processor.traceback()
            )
        module.ctx.env.setvar(self.member, value)
        module.ctx.env.meta[self.member].qname = "%s::%s" % (
            module.qname, self.member
        )
    #-def
#-class

class GetMember(Trackable):
    """
    """
    __slots__ = [ 'module', 'member' ]

    def __init__(self, module, member):
        """
        """

        Trackable.__init__(self)
        self.module = module
        self.member = member
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            self.module,
            self.do_getmember,
            Finalizer(ctx)
        )
    #-def

    def do_getmember(self, processor):
        """
        """

        module = processor.acc()

        if not isinstance(module, Module):
            raise CommandError(processor.TypeError,
                "%s: Module expected" % self.name,
                processor.traceback()
            )
        if self.member not in module.ctx.env:
            raise CommandError(processor.NameError,
                "%s: Module %s (%s) has no member %s" % (
                    self.name, module.name, module.qname, self.member
                ),
                processor.traceback()
            )
        processor.setacc(module.ctx.env.getvar(self.member))
    #-def
#-class
