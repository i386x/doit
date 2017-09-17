#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/bootstrap/__init__.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-12-19 02:04:45 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
GLAP bootstrap.\
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

from doit.support.utils import \
    Functor

from doit.support.cmd.runtime import \
    Location

from doit.support.cmd.commands import \
    Const, \
    MacroNode, MacroNodeSequence, MacroNodeAtom, MacroNodeParam, \
    Expand, \
    SetLocal, GetLocal, \
    DefMacro, Define, DefModule, \
    Add, Sub, Mul, Div, Mod, Neg, \
    BitAnd, BitOr, BitXor, ShiftL, ShiftR, Inv, \
    Lt, Gt, Le, Ge, Eq, Ne, Is, \
    And, Or, Not, \
    NewPair, NewList, NewHashMap, \
    Concat, Join, Merge, \
    Contains, \
    GetItem, \
    Lambda, \
    Block, If, Foreach, While, DoWhile, Break, Continue, \
    Call, Return, \
    TryCatchFinally, Throw, Rethrow, \
    SetItem, \
    SetMember, GetMember

from doit.text.pgen.errors import \
    ParsingError

from doit.text.pgen.readers.reader import \
    Reader

from doit.text.pgen.models.action import \
    AddExpr as AAddExpr, SubExpr as ASubExpr, MulExpr as AMulExpr, \
        DivExpr as ADivExpr, ModExpr as AModExpr, \
    BitAndExpr as ABitAndExpr, BitOrExpr as ABitOrExpr, \
        BitXorExpr as ABitXorExpr, \
    ShiftLeftExpr as AShiftLeftExpr, ShiftRightExpr as AShiftRightExpr, \
    NegExpr as ANegExpr, InvExpr as AInvExpr, \
    EqExpr as AEqExpr, NotEqExpr as ANotEqExpr, LtExpr as ALtExpr, \
        GtExpr as AGtExpr, LeExpr as ALeExpr, GeExpr as AGeExpr, \
    LogAndExpr as ALogAndExpr, LogOrExpr as ALogOrExpr, NotExpr as ANotExpr, \
    CallExpr as ACallExpr, \
    IndexExpr as AIndexExpr, AccessExpr as AAccessExpr, \
    Id as AId, IntLiteral as AIntLiteral, FloatLiteral as AFloatLiteral, \
        StringLiteral as AStringLiteral, \
    Block as ABlock, \
    Assign as AAssign, InplaceAdd as AInplaceAdd, InplaceSub as AInplaceSub, \
        InplaceMul as AInplaceMul, InplaceDiv as AInplaceDiv, \
        InplaceMod as AInplaceMod, InplaceBitAnd as AInplaceBitAnd, \
        InplaceBitOr as AInplaceBitOr, InplaceBitXor as AInplaceBitXor, \
        InplaceShiftLeft as AInplaceShiftLeft, \
        InplaceShiftRight as AInplaceShiftRight, \
    If as AIf, Case as ACase, For as AFor, While as AWhile, \
        DoWhile as ADoWhile, Continue as AContinue, Break as ABreak, \
        Return as AReturn, ReturnWithValue as AReturnWithValue

from doit.text.pgen.models.cfgram import \
    Epsilon, Sym, Literal, Var, Range, Action, \
    SetMinus

from doit.text.pgen.readers.glap.bootstrap.pp.commands import \
    DefRule, DefGrammar

ie_ = lambda msg: "%s (%s; %s)" % (
    msg,
    "internal error",
    "if you see this text, the command compiler is probably buggy"
)
mn_ = lambda ncls, ctx, loc, *args: (
    ncls(*args).set_location(*make_location(ctx, loc))
)

def make_location(context, loc = -1):
    """
    """

    stream = context.stream
    if loc < 0:
        loc = stream.pos
    s = stream.data[0 : loc]
    lineno = s.count('\n') + 1
    if lineno > 1:
        s = s.split('\n')[-1]
    colno = len(s) + 1
    return stream.name, lineno, colno
#-def

class SetLocation(Functor):
    """
    """
    __slots__ = []

    def __init__(self, file, lineno, colno):
        """
        """

        Functor.__init__(self, file, lineno, colno)
    #-def

    def __call__(self, node):
        """
        """

        node.set_location(*self.args)
    #-def
#-class

class GlapLexError(ParsingError):
    """
    """
    __slots__ = []

    def __init__(self, context, detail, loc = -1):
        """
        """

        name, lineno, colno = make_location(context, loc)
        ParsingError.__init__(self, "In <%s> at [%d:%d]: %s" % (
            name, lineno, colno, detail
        ))
    #-def
#-class

class GlapSyntaxError(ParsingError):
    """
    """
    __slots__ = []

    def __init__(self, context, detail, loc = -1):
        """
        """

        p = context.lexer.token.position() if context.lexer.token else -1
        name, lineno, colno = make_location(context, p if loc < 0 else loc)
        ParsingError.__init__(self, "In <%s> at [%d:%d]: %s" % (
            name, lineno, colno, detail
        ))
    #-def
#-class

class GlapContext(object):
    """
    """
    __slots__ = [ 'stream', 'lexer', 'parser', 'actions', 'env', 'processor' ]

    def __init__(self):
        """
        """

        self.stream = None
        self.lexer = None
        self.parser = None
        self.actions = None
        self.env = None
        self.processor = None
    #-def
#-class

class GlapStream(object):
    """
    """
    __slots__ = [ 'context', 'name', 'data', 'pos', 'size' ]

    def __init__(self, context, name, s):
        """
        """

        context.stream = self
        self.context = context
        self.name = name
        self.data = s
        self.pos = 0
        self.size = len(s)
    #-def

    def peek(self, n):
        """
        """

        return self.data[self.pos : self.pos + n]
    #-def

    def next(self, n = 1):
        """
        """

        self.pos += n
    #-def

    def match(self, p):
        """
        """

        if self.peek(len(p)) != p:
            raise GlapLexError(self.context, "Expected %r" % p)
        self.pos += len(p)
        return p
    #-def

    def matchset(self, set):
        """
        """

        if self.pos < self.size and self.data[self.pos] in set:
            self.pos += 1
            return self.data[self.pos - 1]
        raise GlapLexError(self.context,
            "Expected one of [%s]" % repr(set)[1:-1]
        )
    #-def

    def matchif(self, f, fname):
        """
        """

        if self.pos < self.size and f(self.data[self.pos]):
            self.pos += 1
            return self.data[self.pos - 1]
        raise GlapLexError(self.context, "Expected %s" % fname)
    #-def

    def matchmany(self, set):
        """
        """

        p = self.pos
        while self.pos < self.size and self.data[self.pos] in set:
            self.pos += 1
        return self.data[p : self.pos]
    #-def

    def matchmanyif(self, f):
        """
        """

        p = self.pos
        while self.pos < self.size and f(self.data[self.pos]):
            self.pos += 1
        return self.data[p : self.pos]
    #-def

    def matchplus(self, set):
        """
        """

        m = self.matchset(set)
        return "%s%s" % (m, self.matchmany(set))
    #-def

    def matchplusif(self, f, fname):
        """
        """

        m = self.matchif(f, fname)
        return "%s%s" % (m, self.matchmanyif(f))
    #-def

    def matchopt(self, set, default):
        """
        """

        if self.pos < self.size and self.data[self.pos] in set:
            self.pos += 1
            return self.data[self.pos - 1]
        return default
    #-def

    def matchoptif(self, f, default):
        """
        """

        if self.pos < self.size and f(self.data[self.pos]):
            self.pos += 1
            return self.data[self.pos - 1]
        return default
    #-def

    def matchn(self, set, n):
        """
        """

        p = self.pos
        while n > 0 and self.pos < self.size and self.data[self.pos] in set:
            self.pos += 1
            n -= 1
        if n > 0:
            raise GlapLexError(self.context,
                "Expected one of [%s]" % repr(set)[1:-1]
            )
        return self.data[p : self.pos]
    #-def

    def matchnif(self, f, n, fname):
        """
        """

        p = self.pos
        while n > 0 and self.pos < self.size and f(self.data[self.pos]):
            self.pos += 1
            n -= 1
        if n > 0:
            raise GlapLexError(self.context, "Expected %s" % fname)
        return self.data[p : self.pos]
    #-def
#-class

class GlapCompileCmdHelper(object):
    """
    """
    UNSPECIFIED = -1
    NULLARY_EXPR = 0
    UNARY_EXPR = 1
    BINARY_EXPR = 2
    INDEX_EXPR = 3
    ACCESS_EXPR = 4
    ASSIGN_EXPR = 5
    NARY_EXPR = 6
    CALL_EXPR = 7
    LAMBDA_EXPR = 8
    EXPAND = 9
    VARIABLE = 10
    STATEMENT = 11
    DEFMACRO_STATEMENT = 12
    DEFINE_STATEMENT = 13
    MACRO_NODE_NULLARY = 14
    MACRO_NODE_UNARY = 15
    MACRO_NODE_BINARY = 16
    MACRO_NODE_INDEX = 17
    MACRO_NODE_ACCESS = 18
    MACRO_NODE_ASSIGN = 19
    MACRO_NODE_NARY = 20
    MACRO_NODE_CALL = 21
    MACRO_NODE_LAMBDA = 22
    MACRO_EXPAND = 23
    MACRO_VARIABLE = 24
    MACRO_PARAM = 25
    MACRO_STATEMENT = 26
    __slots__ = [
      'kind', 'node', 'code', 'vars', 'value_holder', 'context', 'location',
      'errmsg'
    ]

    def __init__(self, context, location, errmsg):
        """
        """

        self.kind = self.UNSPECIFIED
        self.node = None
        self.code = []
        self.vars = []
        self.value_holder = None
        self.context = context
        self.location = location
        self.errmsg = errmsg
    #-def

    def remove_duplicated_vars(self):
        """
        """

        vars = []
        for v in self.vars:
            if v not in vars:
                vars.append(v)
        self.vars = vars
    #-def

    def value_expr(self):
        """
        """

        if self.value_holder is None:
            raise GlapSyntaxError(self.context, self.errmsg, self.location)
        return self.value_holder
    #-def

    @classmethod
    def checknode(cls, context, loc, node):
        """
        """

        errmsg = ""
        inmacro = context.actions.inmacro
        if node.kind >= cls.MACRO_NODE_NULLARY and not inmacro:
            errmsg = "Macro node was detected outside macro definition"
        if node.kind < cls.MACRO_NODE_NULLARY and inmacro:
            errmsg = "Non-macro node was detected inside macro definition"
        if errmsg != "":
            raise GlapSyntaxError(context, ie_(errmsg), loc)
    #-def

    @classmethod
    def make_unary(cls, context, loc, expr, unop):
        """
        """

        cls.checknode(context, loc, expr)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_UNARY
            o.node = MacroNode(unop, expr.value_expr())
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.UNARY_EXPR
            o.node = unop(expr.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(expr.code)
        o.vars.extend(expr.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_binary(cls, context, loc, lhs, rhs, binop):
        """
        """

        cls.checknode(context, loc, lhs)
        cls.checknode(context, loc, rhs)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_BINARY
            o.node = MacroNode(binop, lhs.value_expr(), rhs.value_expr())
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.BINARY_EXPR
            o.node = binop(lhs.value_expr(), rhs.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(lhs.code)
        o.code.extend(rhs.code)
        o.vars.extend(lhs.vars)
        o.vars.extend(rhs.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_index(cls, context, loc, expr, idx):
        """
        """

        cls.checknode(context, loc, expr)
        cls.checknode(context, loc, idx)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_INDEX
            o.node = MacroNode(GetItem, expr.value_expr(), idx.value_expr())
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.INDEX_EXPR
            o.node = GetItem(expr.value_expr(), idx.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(expr.code)
        o.code.extend(idx.code)
        o.vars.extend(expr.vars)
        o.vars.extend(idx.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_access(cls, context, loc, module, member):
        """
        """

        cls.checknode(context, loc, module)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_ACCESS
            o.node = MacroNode(
                GetMember, module.value_expr(), MacroNodeAtom(member.value())
            )
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.ACCESS_EXPR
            o.node = GetMember(module.value_expr(), member.value())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(module.code)
        o.vars.extend(module.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_assign(cls, context, loc, lhs, rhs, inplaceop = None):
        """
        """

        cls.checknode(context, loc, lhs)
        cls.checknode(context, loc, rhs)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_ASSIGN
        else:
            o.kind = cls.ASSIGN_EXPR
        if lhs.kind in (cls.VARIABLE, cls.MACRO_VARIABLE):
            if inplaceop:
                if inmacro:
                    a = MacroNode(GetLocal, MacroNodeAtom(lhs.node.value()))
                    a.deferred.append(SetLocation(*make_location(
                        context, lhs.node.position()
                    )))
                    ve = MacroNode(inplaceop, a, rhs.value_expr())
                    ve.deferred.append(SetLocation(*make_location(
                        context, loc
                    )))
                    o.node = MacroNode(
                        SetLocal, MacroNodeAtom(lhs.node.value()), ve
                    )
                else:
                    a = GetLocal(lhs.node.value())
                    a.set_location(*make_location(
                        context, lhs.node.position()
                    ))
                    ve = inplaceop(a, rhs.value_expr())
                    ve.set_location(*make_location(context, loc))
                    o.node = SetLocal(lhs.node.value(), ve)
            else:
                if inmacro:
                    o.node = MacroNode(
                        SetLocal,
                        MacroNodeAtom(lhs.node.value()),
                        rhs.value_expr()
                    )
                else:
                    o.node = SetLocal(lhs.node.value(), rhs.value_expr())
        elif lhs.kind in (cls.INDEX_EXPR, cls.MACRO_NODE_INDEX):
            if inplaceop:
                if inmacro:
                    ve = MacroNode(inplaceop, lhs.node, rhs.value_expr())
                    ve.deferred.append(SetLocation(*make_location(
                        context, loc
                    )))
                    o.node = MacroNode(
                        SetItem, lhs.node.nodes[0], lhs.node.nodes[1], ve
                    )
                else:
                    ve = inplaceop(lhs.node, rhs.value_expr())
                    ve.set_location(*make_location(context, loc))
                    o.node = SetItem(
                        lhs.node.operands[0], lhs.node.operands[1], ve
                    )
            else:
                if inmacro:
                    o.node = MacroNode(
                        SetItem,
                        lhs.node.nodes[0],
                        lhs.node.nodes[1],
                        rhs.value_expr()
                    )
                else:
                    o.node = SetItem(
                        lhs.node.operands[0],
                        lhs.node.operands[1],
                        rhs.value_expr()
                    )
        elif lhs.kind in (cls.ACCESS_EXPR, cls.MACRO_NODE_ACCESS):
            if inplaceop:
                if inmacro:
                    ve = MacroNode(inplaceop, lhs.node, rhs.value_expr())
                    ve.deferred.append(SetLocation(*make_location(
                        context, loc
                    )))
                    o.node = MacroNode(
                        SetMember, lhs.node.nodes[0], lhs.node.nodes[1], ve
                    )
                else:
                    ve = inplaceop(lhs.node, rhs.value_expr())
                    ve.set_location(*make_location(context, loc))
                    o.node = SetMember(lhs.node.module, lhs.node.member, ve)
            else:
                if inmacro:
                    o.node = MacroNode(
                        SetMember,
                        lhs.node.nodes[0],
                        lhs.node.nodes[1],
                        rhs.value_expr()
                    )
                else:
                    o.node = SetMember(
                        lhs.node.module, lhs.node.member, rhs.value_expr()
                    )
        else:
            raise GlapSyntaxError(context,
                "Left-hand side of assignment must be l-value", loc
            )
        if inmacro:
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.node.set_location(*make_location(context, loc))
        o.code.extend(lhs.code)
        o.code.extend(rhs.code)
        o.code.append(o.node)
        o.vars.extend(rhs.vars)
        if lhs.kind in (cls.VARIABLE, cls.MACRO_VARIABLE):
            o.vars.insert(0, lhs.node.value())
            if inmacro:
                o.value_holder = MacroNode(
                    GetLocal, MacroNodeAtom(lhs.node.value())
                )
                o.value_holder.deferred.append(SetLocation(*make_location(
                    context, lhs.node.position()
                )))
            else:
                o.value_holder = GetLocal(lhs.node.value())
                o.value_holder.set_location(
                    *make_location(context, lhs.node.position())
                )
        else:
            o.value_holder = lhs.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_call(cls, context, loc, f, fargs):
        """
        """

        cls.checknode(context, loc, f)
        for x in fargs:
            cls.checknode(context, loc, x)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_CALL
            o.node = MacroNode(
                Call, f.value_expr(), *[x.value_expr() for x in fargs]
            )
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.CALL_EXPR
            o.node = Call(f.value_expr(), *[x.value_expr() for x in fargs])
            o.node.set_location(*make_location(context, loc))
        o.code.extend(f.code)
        o.vars.extend(f.vars)
        for x in fargs:
            o.code.extend(x.code)
            o.vars.extend(x.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_variable(cls, context, var):
        """
        """

        o = cls(context, var.position(), "")
        o.node = var
        if context.actions.inmacro:
            o.kind = cls.MACRO_VARIABLE
            o.value_holder = MacroNode(GetLocal, MacroNodeAtom(var.value()))
            o.value_holder.deferred.append(
                SetLocation(*make_location(context, var.position()))
            )
        else:
            o.kind = cls.VARIABLE
            o.value_holder = GetLocal(var.value())
            o.value_holder.set_location(
                *make_location(context, var.position())
            )
        return o
    #-def

    @classmethod
    def make_getvalue(cls, context, var):
        """
        """

        o = cls(context, var.position(), "")
        if context.actions.inmacro:
            o.kind = cls.MACRO_NODE_NULLARY
            o.node = MacroNode(GetLocal, MacroNodeAtom(var.value()))
            o.node.deferred.append(SetLocation(*make_location(
                context, var.position()
            )))
        else:
            o.kind = cls.NULLARY_EXPR
            o.node = GetLocal(var.value())
            o.node.set_location(*make_location(context, var.position()))
        o.value_holder = o.node
        return o
    #-def

    @classmethod
    def make_macroparam(cls, context, var):
        """
        """

        if not context.actions.inmacro:
            raise GlapSyntaxError(context,
                "Macro parameter must be used only inside macro body",
                var.position()
            )
        o = cls(context, var.position(), "")
        o.kind = cls.MACRO_PARAM
        o.node = MacroNodeParam(var.value())
        o.node.deferred.append(SetLocation(*make_location(
            context, var.position()
        )))
        o.value_holder = o.node
        return o
    #-def

    @classmethod
    def make_expand(cls, context, loc, m, margs):
        """
        """

        cls.checknode(context, loc, m)
        for x in margs:
            cls.checknode(context, loc, x)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_EXPAND
            o.node = MacroNode(
                Expand, m.value_expr(), *[x.value_expr() for x in margs]
            )
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.EXPAND
            o.node = Expand(m.value_expr(), *[x.value_expr() for x in margs])
            o.node.set_location(*make_location(context, loc))
        o.code.extend(m.code)
        o.vars.extend(m.vars)
        for x in margs:
            o.code.extend(x.code)
            o.vars.extend(x.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_literal(cls, context, t):
        """
        """

        o = cls(context, t.position(), "")
        if context.actions.inmacro:
            o.kind = cls.MACRO_NODE_NULLARY
            o.node = MacroNode(Const, MacroNodeAtom(t.value(True)))
            o.node.deferred.append(SetLocation(*make_location(
                context, t.position()
            )))
        else:
            o.kind = cls.NULLARY_EXPR
            o.node = Const(t.value(True))
            o.node.set_location(*make_location(context, t.position()))
        o.value_holder = o.node
        return o
    #-def

    @classmethod
    def make_pair(cls, context, loc, x, y):
        """
        """

        cls.checknode(context, loc, x)
        cls.checknode(context, loc, y)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_BINARY
            o.node = MacroNode(NewPair, x.value_expr(), y.value_expr())
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.BINARY_EXPR
            o.node = NewPair(x.value_expr(), y.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(x.code)
        o.code.extend(y.code)
        o.vars.extend(x.vars)
        o.vars.extend(y.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_list(cls, context, loc, items):
        """
        """

        for i in items:
            cls.checknode(context, loc, i)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_NARY
            o.node = MacroNode(NewList, *[i.value_expr() for i in items])
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.NARY_EXPR
            o.node = NewList(*[i.value_expr() for i in items])
            o.node.set_location(*make_location(context, loc))
        for i in items:
            o.code.extend(i.code)
            o.vars.extend(i.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_hash(cls, context, loc, items):
        """
        """

        for k, v in items:
            cls.checknode(context, loc, k)
            cls.checknode(context, loc, v)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_NARY
            items_ = []
            for k, v in items:
                p = MacroNode(NewPair, k.value_expr(), v.value_expr())
                p.deferred.append(k.value_expr().deferred[0])
                items_.append(p)
            o.node = MacroNode(NewHashMap, *items_)
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.NARY_EXPR
            o.node = NewHashMap(*[
                (k.value_expr(), v.value_expr()) for k, v in items
            ])
            o.node.set_location(*make_location(context, loc))
        for k, v in items:
            o.code.extend(k.code)
            o.code.extend(v.code)
            o.vars.extend(k.vars)
            o.vars.extend(v.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_lambda(cls, context, loc, fargs, has_varargs, commands):
        """
        """

        if context.actions.procedure_nesting_level <= 0:
            raise GlapSyntaxError(context,
                ie_("Unballanced `define's"), loc
            )
        for cmd in commands:
            cls.checknode(context, loc, cmd)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        body = []
        bvars = []
        for cmd in commands:
            body.extend(cmd.code)
            if cmd.kind not in (cls.ASSIGN_EXPR, cls.MACRO_NODE_ASSIGN):
                body.append(cmd.value_expr())
            bvars.extend(cmd.vars)
        fargs_ = [x.value() for x in fargs]
        bvars_ = [x for x in bvars if x not in fargs_]
        if inmacro:
            o.kind = cls.MACRO_NODE_LAMBDA
            o.node = MacroNode(
                Lambda,
                MacroNodeAtom(fargs_),
                MacroNodeAtom(has_varargs),
                MacroNodeSequence(*body),
                MacroNodeAtom(bvars_)
            )
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.LAMBDA_EXPR
            o.node = Lambda(fargs_, has_varargs, body, bvars_)
            o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        context.actions.procedure_nesting_level -= 1
        return o
    #-def

    @classmethod
    def make_block(cls, context, loc, commands, keep_varinfo = False):
        """
        """

        for cmd in commands:
            cls.checknode(context, loc, cmd)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        body = []
        for cmd in commands:
            body.extend(cmd.code)
            if keep_varinfo:
                o.vars.extend(cmd.vars)
            if cmd.kind not in (cls.ASSIGN_EXPR, cls.MACRO_NODE_ASSIGN):
                body.append(cmd.value_expr())
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(Block, *body)
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            o.node = Block(*body)
            o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_defmacro(cls, context, loc, name, params, body):
        """
        """

        if not context.actions.inmacro:
            raise GlapSyntaxError(context,
                ie_("Macro body is outside `defmacro'"), loc
            )
        if context.actions.procedure_nesting_level != 0:
            raise GlapSyntaxError(context,
                ie_("Macro body is inside function"), loc
            )
        for node in body:
            cls.checknode(context, loc, node)
        o = cls(context, loc, "")
        o.kind = cls.DEFMACRO_STATEMENT
        mbody = []
        for node in body:
            mbody.extend(node.code)
            if node.kind not in (cls.ASSIGN_EXPR, cls.MACRO_NODE_ASSIGN):
                mbody.append(node.value_expr())
        o.node = DefMacro(name.value(), [p.value() for p in params], mbody)
        o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        context.actions.inmacro = False
        return o
    #-def

    @classmethod
    def make_define(cls, context, loc, name, params, has_varargs, body):
        """
        """

        if context.actions.inmacro:
            raise GlapSyntaxError(context,
                ie_("Function definition is inside macro"), loc
            )
        if context.actions.procedure_nesting_level <= 0:
            raise GlapSyntaxError(context,
                ie_("Unballanced `define's"), loc
            )
        cls.checknode(context, loc, body)
        params_ = [p.value() for p in params]
        bvars_ = [v for v in body.vars if v not in params_]
        body_ = body.value_expr().commands
        o = cls(context, loc, "")
        o.kind = cls.DEFINE_STATEMENT
        o.node = Define(name.value(), bvars_, params_, has_varargs, body_)
        o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        context.actions.procedure_nesting_level -= 1
        return o
    #-def

    @classmethod
    def make_if(cls, context, loc, cond, then_part, elif_parts, else_part):
        """
        """

        inmacro = context.actions.inmacro
        if_then_parts = [(loc, cond, then_part)]
        if_then_parts.extend(elif_parts)
        node = None
        vars = []
        while if_then_parts:
            l, c, t = if_then_parts.pop()
            if node is None:
                node = []
                if else_part:
                    ll, else_node = else_part[0]
                    cls.checknode(context, ll, else_node)
                    if inmacro:
                        node.extend(else_node.value_expr().nodes)
                    else:
                        node.extend(else_node.value_expr().commands)
                    vars.extend(else_node.vars)
            # `node' is either [] or [commands] or [macro nodes]
            cls.checknode(context, l, c)
            cls.checknode(context, l, t)
            if inmacro:
                node = c.code + [MacroNode(
                    If,
                    c.value_expr(),
                    MacroNodeSequence(*t.value_expr().nodes),
                    MacroNodeSequence(*node)
                )]
                node[-1].deferred.append(SetLocation(*make_location(
                    context, l
                )))
            else:
                node = c.code + [If(
                    c.value_expr(),
                    t.value_expr().commands,
                    node
                )]
                node[-1].set_location(*make_location(context, l))
            vars_ = []
            vars_.extend(c.vars)
            vars_.extend(t.vars)
            vars_.extend(vars)
            vars = vars_
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
        else:
            o.kind = cls.STATEMENT
        o.node = node[-1]
        o.code = node[:-1]
        o.vars = vars
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_foreach(cls, context, loc, var, ie, body):
        """
        """

        cls.checknode(context, loc, ie)
        cls.checknode(context, loc, body)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(
                Foreach,
                MacroNodeAtom(var.value()),
                ie.value_expr(),
                MacroNodeSequence(*body.value_expr().nodes)
            )
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            o.node = Foreach(
                var.value(), ie.value_expr(), body.value_expr().commands
            )
            o.node.set_location(*make_location(context, loc))
        o.code.extend(ie.code)
        o.vars.append(var.value())
        o.vars.extend(ie.vars)
        o.vars.extend(body.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_while(cls, context, loc, cond, body):
        """
        """

        cls.checknode(context, loc, cond)
        if cond.code:
            raise GlapSyntaxError(
                context,
                ie_("More then one commands in while-condition expression"),
                loc
            )
        cls.checknode(context, loc, body)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(
                While,
                cond.value_expr(),
                MacroNodeSequence(*body.value_expr().nodes)
            )
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            o.node = While(
                cond.value_expr(), body.value_expr().commands
            )
            o.node.set_location(*make_location(context, loc))
        o.vars.extend(cond.vars)
        o.vars.extend(body.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_dowhile(cls, context, loc, body, cond):
        """
        """

        cls.checknode(context, loc, body)
        cls.checknode(context, loc, cond)
        if cond.code:
            raise GlapSyntaxError(
                context,
                ie_("More then one commands in while-condition expression"),
                loc
            )
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(
                DoWhile,
                MacroNodeSequence(*body.value_expr().nodes),
                cond.value_expr()
            )
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            o.node = DoWhile(
                body.value_expr().commands, cond.value_expr()
            )
            o.node.set_location(*make_location(context, loc))
        o.vars.extend(body.vars)
        o.vars.extend(cond.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_break(cls, context, loc):
        """
        """

        o = cls(context, loc, "")
        if context.actions.inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(Break)
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            o.node = Break()
            o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        return o
    #-def

    @classmethod
    def make_continue(cls, context, loc):
        """
        """

        o = cls(context, loc, "")
        if context.actions.inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(Continue)
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            o.node = Continue()
            o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        return o
    #-def

    @classmethod
    def make_return(cls, context, loc):
        """
        """

        o = cls(context, loc, "")
        if context.actions.inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(Return)
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            o.node = Return()
            o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        return o
    #-def

    @classmethod
    def make_return_with_value(cls, context, loc, rv):
        """
        """

        cls.checknode(context, loc, rv)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(Return, rv.value_expr())
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            o.node = Return(rv.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(rv.code)
        o.vars.extend(rv.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_try(cls, context, loc, tryblock, catches, fnly):
        """
        """

        cls.checknode(context, loc, tryblock)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
            b = tryblock.value_expr().nodes
            o.vars.extend(tryblock.vars)
            c = []
            for ll, ee, ev, hh in catches:
                cls.checknode(context, ll, hh)
                if ev:
                    ev = ev.value()
                    o.vars.append(ev)
                c.append(MacroNodeSequence(
                    MacroNodeAtom(ee.value()),
                    MacroNodeAtom(ev),
                    MacroNodeSequence(*hh.value_expr().nodes)
                ))
                o.vars.extend(hh.vars)
            f = []
            if fnly:
                ll, ff = fnly[0]
                cls.checknode(context, ll, ff)
                f.extend(ff.value_expr().nodes)
                o.vars.extend(ff.vars)
            o.node = MacroNode(
                TryCatchFinally,
                MacroNodeSequence(*b),
                MacroNodeSequence(*c),
                MacroNodeSequence(*f)
            )
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            b = tryblock.value_expr().commands
            o.vars.extend(tryblock.vars)
            c = []
            for ll, ee, ev, hh in catches:
                cls.checknode(context, ll, hh)
                if ev:
                    ev = ev.value()
                    o.vars.append(ev)
                c.append((ee.value(), ev, hh.value_expr().commands))
                o.vars.extend(hh.vars)
            f = []
            if fnly:
                ll, ff = fnly[0]
                cls.checknode(context, ll, ff)
                f.extend(ff.value_expr().commands)
                o.vars.extend(ff.vars)
            o.node = TryCatchFinally(b, c, f)
            o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def

    @classmethod
    def make_throw(cls, context, loc, ee, em):
        """
        """

        cls.checknode(context, loc, ee)
        if em:
            cls.checknode(context, loc, em)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
            if em:
                o.node = MacroNode(Throw, ee.value_expr(), em.value_expr())
            else:
                o.node = MacroNode(Rethrow, ee.value_expr())
            o.node.deferred.append(SetLocation(*make_location(context, loc)))
        else:
            o.kind = cls.STATEMENT
            if em:
                o.node = Throw(ee.value_expr(), em.value_expr())
            else:
                o.node = Rethrow(ee.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(ee.code)
        o.vars.extend(ee.vars)
        if em:
            o.code.extend(em.code)
            o.vars.extend(em.vars)
        o.value_holder = o.node
        o.remove_duplicated_vars()
        return o
    #-def
#-class

class GlapParserActions(object):
    """
    """
    __slots__ = [ 'context', 'inmacro', 'procedure_nesting_level', 'actions' ]

    def __init__(self, context):
        """
        """

        context.actions = self
        self.context = context
        self.inmacro = False
        self.procedure_nesting_level = 0
        self.actions = {
          'start': self.on_start,
          'module': self.on_module,
          'grammar': self.on_grammar,
          'rule': self.on_rule,
          'rule_rhs_expr(_|_)': self.on_rule_rhs_expr_alt,
          'rule_rhs_expr(_-_)': self.on_rule_rhs_expr_sub,
          'rule_rhs_expr(_ _)': self.on_rule_rhs_expr_cat,
          'rule_rhs_expr(_*)': self.on_rule_rhs_expr_star,
          'rule_rhs_expr(_+)': self.on_rule_rhs_expr_plus,
          'rule_rhs_expr(_?)': self.on_rule_rhs_expr_opt,
          'rule_rhs_expr(-_)': self.on_rule_rhs_expr_neg,
          'rule_rhs_expr(~_)': self.on_rule_rhs_expr_inv,
          'rule_rhs_expr(_\'_)': self.on_rule_rhs_expr_label,
          'rule_rhs_expr_atom(ID)': self.on_rule_rhs_expr_atom_var,
          'rule_rhs_expr_atom(STR)': self.on_rule_rhs_expr_atom_str,
          'rule_rhs_expr_atom(STR..STR)': self.on_rule_rhs_expr_atom_range,
          'rule_rhs_expr_atom(eps)': self.on_rule_rhs_expr_atom_epsilon,
          'rule_rhs_expr_atom(action)': self.on_rule_rhs_expr_atom_action,
          'c_expr(_=_)': (lambda *args:
              GlapCompileCmdHelper.make_assign(*args)
          ),
          'c_expr(_+=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Add)
          ),
          'c_expr(_-=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Sub)
          ),
          'c_expr(_*=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Mul)
          ),
          'c_expr(_/=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Div)
          ),
          'c_expr(_%=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Mod)
          ),
          'c_expr(_&=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, BitAnd)
          ),
          'c_expr(_|=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, BitOr)
          ),
          'c_expr(_^=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, BitXor)
          ),
          'c_expr(_<<=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, ShiftL)
          ),
          'c_expr(_>>=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, ShiftR)
          ),
          'c_expr(_&&=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, And)
          ),
          'c_expr(_||=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Or)
          ),
          'c_expr(_.=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Concat)
          ),
          'c_expr(_++=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Join)
          ),
          'c_expr(_~~=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_assign(c, l, x, y, Merge)
          ),
          'c_expr(_||_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Or)
          ),
          'c_expr(_&&_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, And)
          ),
          'c_expr(_<_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Lt)
          ),
          'c_expr(_>_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Gt)
          ),
          'c_expr(_<=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Le)
          ),
          'c_expr(_>=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Ge)
          ),
          'c_expr(_==_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Eq)
          ),
          'c_expr(_!=_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Ne)
          ),
          'c_expr(_===_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Is)
          ),
          'c_expr(_in_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Contains)
          ),
          'c_expr(_|_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, BitOr)
          ),
          'c_expr(_&_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, BitAnd)
          ),
          'c_expr(_^_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, BitXor)
          ),
          'c_expr(_<<_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, ShiftL)
          ),
          'c_expr(_>>_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, ShiftR)
          ),
          'c_expr(_+_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Add)
          ),
          'c_expr(_-_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Sub)
          ),
          'c_expr(_._)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Concat)
          ),
          'c_expr(_++_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Join)
          ),
          'c_expr(_~~_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Merge)
          ),
          'c_expr(_*_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Mul)
          ),
          'c_expr(_/_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Div)
          ),
          'c_expr(_%_)': (lambda c, l, x, y:
              GlapCompileCmdHelper.make_binary(c, l, x, y, Mod)
          ),
          'c_expr(_ _)': (lambda *args:
              GlapCompileCmdHelper.make_call(*args)
          ),
          'c_expr(-_)': (lambda c, l, e:
              GlapCompileCmdHelper.make_unary(c, l, e, Neg)
          ),
          'c_expr(!_)': (lambda c, l, e:
              GlapCompileCmdHelper.make_unary(c, l, e, Not)
          ),
          'c_expr(~_)': (lambda c, l, e:
              GlapCompileCmdHelper.make_unary(c, l, e, Inv)
          ),
          'c_expr(_[_])': (lambda *args:
              GlapCompileCmdHelper.make_index(*args)
          ),
          'c_expr(_:ID)': (lambda *args:
              GlapCompileCmdHelper.make_access(*args)
          ),
          'c_expr_atom(ID)': (lambda *args:
              GlapCompileCmdHelper.make_variable(*args)
          ),
          'c_expr_atom($ID)': (lambda *args:
              GlapCompileCmdHelper.make_getvalue(*args)
          ),
          'c_expr_atom(#ID)': (lambda *args:
              GlapCompileCmdHelper.make_macroparam(*args)
          ),
          'c_expr_atom($(_ _))': (lambda *args:
              GlapCompileCmdHelper.make_expand(*args)
          ),
          'c_expr_atom(INT)': (lambda *args:
              GlapCompileCmdHelper.make_literal(*args)
          ),
          'c_expr_atom(FLOAT)': (lambda *args:
              GlapCompileCmdHelper.make_literal(*args)
          ),
          'c_expr_atom(STR)': (lambda *args:
              GlapCompileCmdHelper.make_literal(*args)
          ),
          'c_expr_atom(pair)': (lambda *args:
              GlapCompileCmdHelper.make_pair(*args)
          ),
          'c_expr_atom(list)': (lambda *args:
              GlapCompileCmdHelper.make_list(*args)
          ),
          'c_expr_atom(hash)': (lambda *args:
              GlapCompileCmdHelper.make_hash(*args)
          ),
          'c_expr_atom(lambda)': (lambda *args:
              GlapCompileCmdHelper.make_lambda(*args)
          ),
          'c_stmt(block)': (lambda *args:
              GlapCompileCmdHelper.make_block(*args)
          ),
          'c_stmt(defmacro)': (lambda *args:
              GlapCompileCmdHelper.make_defmacro(*args)
          ),
          'c_stmt(define)': (lambda *args:
              GlapCompileCmdHelper.make_define(*args)
          ),
          'c_stmt(if)': (lambda *args:
              GlapCompileCmdHelper.make_if(*args)
          ),
          'c_stmt(foreach)': (lambda *args:
              GlapCompileCmdHelper.make_foreach(*args)
          ),
          'c_stmt(while)': (lambda *args:
              GlapCompileCmdHelper.make_while(*args)
          ),
          'c_stmt(do-while)': (lambda *args:
              GlapCompileCmdHelper.make_dowhile(*args)
          ),
          'c_stmt(break)': (lambda *args:
              GlapCompileCmdHelper.make_break(*args)
          ),
          'c_stmt(continue)': (lambda *args:
              GlapCompileCmdHelper.make_continue(*args)
          ),
          'c_stmt(return)': (lambda *args:
              GlapCompileCmdHelper.make_return(*args)
          ),
          'c_stmt(return(expr))': (lambda *args:
              GlapCompileCmdHelper.make_return_with_value(*args)
          ),
          'c_stmt(try)': (lambda *args:
              GlapCompileCmdHelper.make_try(*args)
          ),
          'c_stmt(throw)': (lambda *args:
              GlapCompileCmdHelper.make_throw(*args)
          ),
          'a_stmt(block)': (lambda *args: mn_(ABlock, *args)),
          'a_stmt(expr)': (lambda ctx, loc, e: e),
          'a_stmt(_=_)': (lambda *args: mn_(AAssign, *args)),
          'a_stmt(_+=_)': (lambda *args: mn_(AInplaceAdd, *args)),
          'a_stmt(_-=_)': (lambda *args: mn_(AInplaceSub, *args)),
          'a_stmt(_*=_)': (lambda *args: mn_(AInplaceMul, *args)),
          'a_stmt(_/=_)': (lambda *args: mn_(AInplaceDiv, *args)),
          'a_stmt(_%=_)': (lambda *args: mn_(AInplaceMod, *args)),
          'a_stmt(_&=_)': (lambda *args: mn_(AInplaceBitAnd, *args)),
          'a_stmt(_|=_)': (lambda *args: mn_(AInplaceBitOr, *args)),
          'a_stmt(_^=_)': (lambda *args: mn_(AInplaceBitXor, *args)),
          'a_stmt(_<<=_)': (lambda *args: mn_(AInplaceShiftLeft, *args)),
          'a_stmt(_>>=_)': (lambda *args: mn_(AInplaceShiftRight, *args)),
          'a_stmt(if)': (lambda *args: mn_(AIf, *args)),
          'a_stmt(case)': (lambda *args: mn_(ACase, *args)),
          'a_stmt(for)': (lambda ctx, loc, v, e, b:
              AFor(
                  AId(v.value()).set_location(
                      *make_location(ctx, v.position())
                  ),
                  e, b
              ).set_location(*make_location(ctx, loc))
          ),
          'a_stmt(while)': (lambda *args: mn_(AWhile, *args)),
          'a_stmt(do-while)': (lambda *args: mn_(ADoWhile, *args)),
          'a_stmt(break)': (lambda *args: mn_(ABreak, *args)),
          'a_stmt(continue)': (lambda *args: mn_(AContinue, *args)),
          'a_stmt(return)': (lambda *args: mn_(AReturn, *args)),
          'a_stmt(return(expr))': (lambda *args: mn_(AReturnWithValue, *args)),
          'a_expr(_||_)': (lambda *args: mn_(ALogOrExpr, *args)),
          'a_expr(_&&_)': (lambda *args: mn_(ALogAndExpr, *args)),
          'a_expr(_<_)': (lambda *args: mn_(ALtExpr, *args)),
          'a_expr(_>_)': (lambda *args: mn_(AGtExpr, *args)),
          'a_expr(_<=_)': (lambda *args: mn_(ALeExpr, *args)),
          'a_expr(_>=_)': (lambda *args: mn_(AGeExpr, *args)),
          'a_expr(_==_)': (lambda *args: mn_(AEqExpr, *args)),
          'a_expr(_!=_)': (lambda *args: mn_(ANotEqExpr, *args)),
          'a_expr(_|_)': (lambda *args: mn_(ABitOrExpr, *args)),
          'a_expr(_&_)': (lambda *args: mn_(ABitAndExpr, *args)),
          'a_expr(_^_)': (lambda *args: mn_(ABitXorExpr, *args)),
          'a_expr(_<<_)': (lambda *args: mn_(AShiftLeftExpr, *args)),
          'a_expr(_>>_)': (lambda *args: mn_(AShiftRightExpr, *args)),
          'a_expr(_+_)': (lambda *args: mn_(AAddExpr, *args)),
          'a_expr(_-_)': (lambda *args: mn_(ASubExpr, *args)),
          'a_expr(_*_)': (lambda *args: mn_(AMulExpr, *args)),
          'a_expr(_/_)': (lambda *args: mn_(ADivExpr, *args)),
          'a_expr(_%_)': (lambda *args: mn_(AModExpr, *args)),
          'a_expr(-_)': (lambda *args: mn_(ANegExpr, *args)),
          'a_expr(~_)': (lambda *args: mn_(AInvExpr, *args)),
          'a_expr(!_)': (lambda *args: mn_(ANotExpr, *args)),
          'a_expr(_(_))': (lambda *args: mn_(ACallExpr, *args)),
          'a_expr(_[_])': (lambda *args: mn_(AIndexExpr, *args)),
          'a_expr(_.ID)': (lambda ctx, loc, lhs, rhs:
              AAccessExpr(
                  lhs,
                  AId(rhs.value()).set_location(
                      *make_location(ctx, rhs.position())
                  )
              ).set_location(*make_location(ctx, loc))
          ),
          'a_expr_atom(ID)': (lambda *args: mn_(AId, *args)),
          'a_expr_atom(INT)': (lambda *args: mn_(AIntLiteral, *args)),
          'a_expr_atom(FLOAT)': (lambda *args: mn_(AFloatLiteral, *args)),
          'a_expr_atom(STR)': (lambda *args: mn_(AStringLiteral, *args)),
          'unwrap': self.on_unwrap
        }
    #-def

    def on_start(self, context, module):
        """
        """

        return module
    #-def

    def on_module(self, context, loc, name, module_units):
        """
        """

        node = DefModule(name.value(), module_units)
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_grammar(
        self, context, loc, name, grammar_type_spec, rules_and_commands
    ):
        """
        """

        node = DefGrammar(
            name.value(),
            [
                (x.value(), Location(*make_location(context, x.position())))
                for x in grammar_type_spec
            ],
            rules_and_commands
        )
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule(self, context, lhs, leftarrow, rhs):
        """
        """

        node = DefRule(lhs.value(), rhs, leftarrow.value() == ":")
        node.set_location(*make_location(context, lhs.position()))
        return node
    #-def

    def on_rule_rhs_expr_alt(self, context, loc, lhs, rhs):
        """
        """

        node = lhs | rhs
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_sub(self, context, loc, lhs, rhs):
        """
        """

        node = SetMinus(lhs, rhs)
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_cat(self, context, loc, lhs, rhs):
        """
        """

        node = lhs + rhs
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_star(self, context, loc, lhs):
        """
        """

        node = lhs['*']
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_plus(self, context, loc, lhs):
        """
        """

        node = lhs['+']
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_opt(self, context, loc, lhs):
        """
        """

        node = lhs['?']
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_neg(self, context, loc, rhs):
        """
        """

        node = -rhs
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_inv(self, context, loc, rhs):
        """
        """

        node = ~rhs
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_label(self, context, loc, lhs, rhs):
        """
        """

        node = lhs % rhs
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_atom_var(self, context, t):
        """
        """

        node = Var(t.value())
        node.set_location(*make_location(context, t.position()))
        return node
    #-def

    def on_rule_rhs_expr_atom_str(self, context, t):
        """
        """

        v = t.value(True)
        if v == "":
            node = Epsilon()
        elif len(v) == 1:
            node = Sym(v)
        else:
            node = Literal(v)
        node.set_location(*make_location(context, t.position()))
        return node
    #-def

    def on_rule_rhs_expr_atom_range(self, context, t, u):
        """
        """

        if len(t.value()) != 1:
            raise GlapSyntaxError(context,
                "Character was expected", t.position()
            )
        if len(u.value()) != 1:
            raise GlapSyntaxError(context,
                "Character was expected", u.position()
            )
        if ord(t.value()) > ord(u.value()):
            raise GlapSyntaxError(context,
                "Invalid range literal (%r > %r)" % (t.value(), u.value()),
                t.position()
            )
        a = Sym(t.value())
        a.set_location(*make_location(context, t.position()))
        b = Sym(u.value())
        b.set_location(*make_location(context, u.position()))
        node = Range(a, b)
        node.set_location(*make_location(context, t.position()))
        return node
    #-def

    def on_rule_rhs_expr_atom_epsilon(self, context, loc):
        """
        """

        node = Epsilon()
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_rule_rhs_expr_atom_action(self, context, loc, actions):
        """
        """

        l = make_location(context, loc)
        action = ABlock(actions)
        action.set_location(*l)
        node = Action(action)
        node.set_location(*l)
        return node
    #-def

    def on_unwrap(self, context, command):
        """
        """

        if self.inmacro:
            raise GlapSyntaxError(context, ie_("Unfinished macro definition"))
        elif self.procedure_nesting_level != 0:
            raise GlapSyntaxError(
                context, ie_("Unfinished function definition")
            )
        kind = command.kind
        if kind < 0:
            raise GlapSyntaxError(context, ie_("Unspecified node"))
        elif kind <= GlapCompileCmdHelper.VARIABLE:
            unwrapped = []
            unwrapped.extend(command.code)
            if kind != GlapCompileCmdHelper.ASSIGN_EXPR:
                unwrapped.append(command.value_expr())
            return unwrapped
        elif kind <= GlapCompileCmdHelper.DEFINE_STATEMENT:
            return [command.value_expr()]
        raise GlapSyntaxError(context,
            ie_("Macro nodes was detected outside macro definition scope")
        )
    #-def

    def run(self, action, context, *args):
        """
        """

        if action not in self.actions:
            raise ParsingError("Action %r does not exist" % action)
        return self.actions[action](context, *args)
    #-def
#-class

class GlapReader(Reader):
    """
    """
    __slots__ = []

    def read(self, source, *args, **opts):
        """
        """

        data, name = self.load_source(source, **opts)
        if data is None:
            return None
        ctx = GlapContext()
        GlapStream(ctx, name, data)
        GlapLexer(ctx)
        GlapParser(ctx)
        GlapActions(ctx)
    #-def
#-class

def get_reader_class():
    """
    """

    return GlapReader
#-def
