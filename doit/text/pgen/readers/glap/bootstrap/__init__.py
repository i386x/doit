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

from doit.support.cmd.commands import DefModule

from doit.text.pgen.errors import ParsingError
from doit.text.pgen.readers.reader import Reader

from doit.text.pgen.models.cfgram import \
    Epsilon, Sym, Literal

from doit.text.pgen.readers.glap.bootstrap.pp.commands import \
    DefRule, DefGrammar

ie_ = lambda msg: "%s (%s; %s)" % (
    msg,
    "internal error",
    "if you see this text, the command compiler is probably buggy"
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
    NULLARY_EPXR = 0
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
    __slots__ = [ 'kind', 'node', 'code', 'vars', 'value_holder' ]

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
        if node.kind < MACRO_NODE_NULLARY and inmacro:
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
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.UNARY_EXPR
            o.node = unop(expr.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(expr.code)
        o.vars.extend(expr.vars)
        o.value_holder = o.node
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
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.BINARY_EXPR
            o.node = binop(lhs.value_expr(), rhs.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(lhs.code)
        o.code.extend(rhs.code)
        o.vars.extend(lhs.vars)
        o.vars.extend(rhs.vars)
        o.value_holder = o.node
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
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.INDEX_EXPR
            o.node = GetItem(expr.value_expr(), idx.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(expr.code)
        o.code.extend(idx.code)
        o.vars.extend(expr.vars)
        o.vars.extend(idx.vars)
        o.value_holder = o.node
        return o
    #-def

    @classmethod
    def make_access(cls, context, loc, module, member):
        """
        """

        cls.checknode(context, loc, module)
        cls.checknode(context, loc, member)
        inmacro = context.actions.inmacro
        o = cls(context, loc, "")
        if inmacro:
            o.kind = cls.MACRO_NODE_ACCESS
            o.node = MacroNode(
                GetMember, module.value_expr(), member.node.value()
            )
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.ACCESS_EXPR
            o.node = GetMember(module.value_expr(), member.node.value())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(module.code)
        o.vars.extend(module.vars)
        o.value_holder = o.node
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
                    l1 = make_location(context, lhs.node.position())
                    a.deferred.append(lambda n: n.set_location(*l1))
                    ve = MacroNode(inplaceop, a, rhs.value_expr())
                    l2 = make_location(context, loc)
                    ve.deferred.append(lambda n: n.set_location(*l2))
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
                    l1 = make_location(context, loc)
                    ve.deferred.append(lambda n: n.set_location(*l1))
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
                    l1 = make_location(context, loc)
                    ve.deferred.append(lambda n: n.set_location(*l1))
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
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
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
                l3 = make_location(context, lhs.node.position())
                o.value_holder.deferred.append(lambda n: n.set_location(*l3))
            else:
                o.value_holder = GetLocal(lhs.node.value())
                o.value_holder.set_location(
                    *make_location(context, lhs.node.position())
                )
        else:
            o.value_holder = lhs.node
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
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
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
        return o
    #-def

    @classmethod
    def make_variable(cls, context, var):
        """
        """

        o = cls(context, var.position(), "Missing '$' before variable's name")
        if context.actions.inmacro:
            o.kind = cls.MACRO_VARIABLE
        else:
            o.kind = cls.VARIABLE
        o.node = var
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
            l = make_location(context, var.position())
            o.node.deferred.append(lambda n: n.set_location(*l))
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
        l = make_location(context, var.position())
        o.node.deferred.append(lambda n: n.set_location(*l))
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
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
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
        return o
    #-def

    @classmethod
    def make_literal(cls, context, t):
        """
        """

        o = cls(context, t.position(), "")
        if context.actions.inmacro:
            o.kind = cls.MACRO_NODE_NULLARY
            o.node = MacroNode(Const, MacroNodeAtom(t.value()))
            l = make_location(context, t.position())
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.NULLARY_EXPR
            o.node = Const(t.value())
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
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.BINARY_EXPR
            o.node = NewPair(x.value_expr(), y.value_expr())
            o.node.set_location(*make_location(context, loc))
        o.code.extend(x.code)
        o.code.extend(y.code)
        o.vars.extend(x.vars)
        o.vars.extend(y.vars)
        o.value_holder = o.node
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
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.NARY_EXPR
            o.node = NewList(*[i.value_expr() for i in items])
            o.node.set_location(*make_location(context, loc))
        for i in items:
            o.code.extend(i.code)
            o.vars.extend(i.vars)
        o.value_holder = o.node
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
            o.node = MacroNode(NewHash, *items_)
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.NARY_EXPR
            o.node = NewHash(*[
                (k.value_expr(), v.value_expr()) for k, v in items
            ])
            o.node.set_location(*make_location(context, loc))
        for k, v in items:
            o.code.extend(k.code)
            o.code.extend(v.code)
            o.vars.extend(k.vars)
            o.vars.extend(v.vars)
        o.value_holder = o.node
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
            body.append(cmd.value_expr())
            bvars.extend(cmd.vars)
        if inmacro:
            o.kind = cls.MACRO_NODE_LAMBDA
            o.node = MacroNode(
                Lambda,
                MacroNodeAtom([x.value() for x in fargs]),
                MacroNodeAtom(has_varargs),
                MacroNodeSequence(*body),
                MacroNodeAtom(bvars)
            )
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.LAMBDA_EXPR
            o.node = Lambda(
                [x.value() for x in fargs], has_varargs, body, bvars
            )
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
            body.append(cmd.value_expr())
        if inmacro:
            o.kind = cls.MACRO_STATEMENT
            o.node = MacroNode(Block, *body)
            l = make_location(context, loc)
            o.node.deferred.append(lambda n: n.set_location(*l))
        else:
            o.kind = cls.STATEMENT
            o.node = Block(*body)
            o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
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
        body_ = body.value_expr().commands
        o = cls(context, loc, "")
        o.kind = cls.DEFINE_STATEMENT
        o.node = Define(
            name.value(), body.vars, [p.value() for p in params], has_varargs,
            body_
        )
        o.node.set_location(*make_location(context, loc))
        o.value_holder = o.node
        context.actions.procedure_nesting_level -= 1
        return o
    #-def
#-class

class GlapParserActions(object):
    """
    """
    __slots__ = [ 'context', 'inmacro', 'inproc', 'actions' ]

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
          'c_expr(_=_)': self.on_c_expr_assign,
          'c_expr(_+=_)': self.on_c_expr_iadd,
          'c_expr(_-=_)': self.on_c_expr_isub,
          'c_expr(_*=_)': self.on_c_expr_imult,
          'c_expr(_/=_)': self.on_c_expr_idiv,
          'c_expr(_%=_)': self.on_c_expr_imod,
          'c_expr(_&=_)': self.on_c_expr_iband,
          'c_expr(_|=_)': self.on_c_expr_ibor,
          'c_expr(_^=_)': self.on_c_expr_ibxor,
          'c_expr(_<<=_)': self.on_c_expr_ibshl,
          'c_expr(_>>=_)': self.on_c_expr_ibshr,
          'c_expr(_&&=_)': self.on_c_expr_iland,
          'c_expr(_||=_)': self.on_c_expr_ilor,
          'c_expr(_.=_)': self.on_c_expr_icat,
          'c_expr(_++=_)': self.on_c_expr_ijoin,
          'c_expr(_~~=_)': self.on_c_expr_imerge,
          'c_expr(_||_)': self.on_c_expr_lor,
          'c_expr(_&&_)': self.on_c_expr_land,
          'c_expr(_<_)': self.on_c_expr_lt,
          'c_expr(_>_)': self.on_c_expr_gt,
          'c_expr(_<=_)': self.on_c_expr_le,
          'c_expr(_>=_)': self.on_c_expr_ge,
          'c_expr(_==_)': self.on_c_expr_eq,
          'c_expr(_!=_)': self.on_c_expr_ne,
          'c_expr(_===_)': self.on_c_expr_is,
          'c_expr(_in_)': self.on_c_expr_in,
          'c_expr(_|_)': self.on_c_expr_bor,
          'c_expr(_&_)': self.on_c_expr_band,
          'c_expr(_^_)': self.on_c_expr_bxor,
          'c_expr(_<<_)': self.on_c_expr_bshl,
          'c_expr(_>>_)': self.on_c_expr_bshr,
          'c_expr(_+_)': self.on_c_expr_add,
          'c_expr(_-_)': self.on_c_expr_sub,
          'c_expr(_._)': self.on_c_expr_cat,
          'c_expr(_++_)': self.on_c_expr_join,
          'c_expr(_~~_)': self.on_c_expr_merge,
          'c_expr(_*_)': self.on_c_expr_mult,
          'c_expr(_/_)': self.on_c_expr_div,
          'c_expr(_%_)': self.on_c_expr_mod,
          'c_expr(_ _)': self.on_c_expr_call,
          'c_expr(-_)': self.on_c_expr_neg,
          'c_expr(!_)': self.on_c_expr_lnot,
          'c_expr(~_)': self.on_c_expr_binv,
          'c_expr(_[_])': self.on_c_expr_index,
          'c_expr(_:ID)': self.on_c_expr_access,
          'c_expr_atom(ID)': self.on_c_expr_atom_var,
          'c_expr_atom($ID)': self.on_c_expr_atom_getval,
          'c_expr_atom(#ID)': self.on_c_expr_atom_macpar,
          'c_expr_atom($(_ _))': self.on_c_expr_atom_expand,
          'c_expr_atom(INT)': self.on_c_expr_atom_int,
          'c_expr_atom(FLOAT)': self.on_c_expr_atom_float,
          'c_expr_atom(STR)': self.on_c_expr_atom_str,
          'c_expr_atom(pair)': self.on_c_expr_atom_pair,
          'c_expr_atom(list)': self.on_c_expr_atom_list,
          'c_expr_atom(hash)': self.on_c_expr_atom_hash,
          'c_expr_atom(lambda)': self.on_c_expr_atom_lambda,
          'c_stmt(block)': self.on_c_stmt_block,
          'c_stmt(defmacro)': self.on_c_stmt_defmacro,
          'c_stmt(define)': self.on_c_stmt_define,
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

        v = t.value()
        if v == "":
            node = Epsilon()
        elif len(v) == 1:
            node = Sym(v)
        else:
            node = Literal(t)
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

    def on_rule_rhs_expr_atom_action(self, context, loc, action):
        """
        """

        node = Action(action)
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def on_c_expr_assign(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs)
    #-def

    def on_c_expr_iadd(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Add)
    #-def

    def on_c_expr_isub(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Sub)
    #-def

    def on_c_expr_imult(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Mul)
    #-def

    def on_c_expr_idiv(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Div)
    #-def

    def on_c_expr_imod(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Mod)
    #-def

    def on_c_expr_iband(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, BitAnd)
    #-def

    def on_c_expr_ibor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, BitOr)
    #-def

    def on_c_expr_ibxor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, BitXor)
    #-def

    def on_c_expr_ibshl(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, ShiftL)
    #-def

    def on_c_expr_ibshr(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, ShiftR)
    #-def

    def on_c_expr_iland(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, And)
    #-def

    def on_c_expr_ilor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Or)
    #-def

    def on_c_expr_icat(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Concat)
    #-def

    def on_c_expr_ijoin(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Join)
    #-def

    def on_c_expr_imerge(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_assign(context, loc, lhs, rhs, Merge)
    #-def

    def on_c_expr_lor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Or)
    #-def

    def on_c_expr_land(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, And)
    #-def

    def on_c_expr_lt(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Lt)
    #-def

    def on_c_expr_gt(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Gt)
    #-def

    def on_c_expr_le(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Le)
    #-def

    def on_c_expr_ge(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Ge)
    #-def

    def on_c_expr_eq(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Eq)
    #-def

    def on_c_expr_ne(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Ne)
    #-def

    def on_c_expr_is(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Is)
    #-def

    def on_c_expr_in(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Contains)
    #-def

    def on_c_expr_bor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, BitOr)
    #-def

    def on_c_expr_band(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, BitAnd)
    #-def

    def on_c_expr_bxor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, BitXor)
    #-def

    def on_c_expr_bshl(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, ShiftL)
    #-def

    def on_c_expr_bshr(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, ShiftR)
    #-def

    def on_c_expr_add(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Add)
    #-def

    def on_c_expr_sub(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Sub)
    #-def

    def on_c_expr_cat(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Concat)
    #-def

    def on_c_expr_join(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Join)
    #-def

    def on_c_expr_merge(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Merge)
    #-def

    def on_c_expr_mult(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Mul)
    #-def

    def on_c_expr_div(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Div)
    #-def

    def on_c_expr_mod(self, context, loc, lhs, rhs):
        """
        """

        return GlapCompileCmdHelper.make_binary(context, loc, lhs, rhs, Mod)
    #-def

    def on_c_expr_call(self, context, loc, f, fargs):
        """
        """

        return GlapCompileCmdHelper.make_call(context, loc, f, fargs)
    #-def

    def on_c_expr_neg(self, context, loc, expr):
        """
        """

        return GlapCompileCmdHelper.make_unary(context, loc, expr, Neg)
    #-def

    def on_c_expr_lnot(self, context, loc, expr):
        """
        """

        return GlapCompileCmdHelper.make_unary(context, loc, expr, Not)
    #-def

    def on_c_expr_binv(self, context, loc, expr):
        """
        """

        return GlapCompileCmdHelper.make_unary(context, loc, expr, Inv)
    #-def

    def on_c_expr_index(self, context, loc, expr, idx):
        """
        """

        return GlapCompileCmdHelper.make_index(context, loc, expr, idx)
    #-def

    def on_c_expr_access(self, context, loc, module, member):
        """
        """

        return GlapCompileCmdHelper.make_access(context, loc, module, member)
    #-def

    def on_c_expr_atom_var(self, context, var):
        """
        """

        return GlapCompileCmdHelper.make_variable(var)
    #-def

    def on_c_expr_atom_getval(self, context, var):
        """
        """

        return GlapCompileCmdHelper.make_getvalue(context, var)
    #-def

    def on_c_expr_atom_macpar(self, context, var):
        """
        """

        return GlapCompileCmdHelper.make_macroparam(context, var)
    #-def

    def on_c_expr_atom_expand(self, context, loc, m, margs):
        """
        """

        return GlapCompileCmdHelper.make_expand(context, loc, m, margs)
    #-def

    def on_c_expr_atom_int(self, context, t):
        """
        """

        return GlapCompileCmdHelper.make_literal(context, t)
    #-def

    def on_c_expr_atom_float(self, context, t):
        """
        """

        return GlapCompileCmdHelper.make_literal(context, t)
    #-def

    def on_c_expr_atom_str(self, context, t):
        """
        """

        return GlapCompileCmdHelper.make_literal(context, t)
    #-def

    def on_c_expr_atom_pair(self, context, loc, x, y):
        """
        """

        return GlapCompileCmdHelper.make_pair(context, loc, x, y)
    #-def

    def on_c_expr_atom_list(self, context, loc, items):
        """
        """

        return GlapCompileCmdHelper.make_list(context, loc, items)
    #-def

    def on_c_expr_atom_hash(self, context, loc, items):
        """
        """

        return GlapCompileCmdHelper.make_hash(context, loc, items)
    #-def

    def on_c_expr_atom_lambda(
        self, context, loc, fargs, has_varargs, commands
    ):
        """
        """

        return GlapCompileCmdHelper.make_lambda(
            context, loc, fargs, has_varargs, commands
        )
    #-def

    def on_c_stmt_block(self, context, loc, commands):
        """
        """

        return GlapCompileCmdHelper.make_block(context, loc, commands)
    #-def

    def on_c_stmt_defmacro(self, context, loc, name, params, body):
        """
        """

        return GlapCompileCmdHelper.make_defmacro(
            context, loc, name, params, body
        )
    #-def

    def on_c_stmt_define(self, context, loc, name, params, has_varargs, body):
        """
        """

        return GlapCompileCmdHelper.make_define(
            context, loc, name, params, has_varargs, body
        )
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
        elif kind <= GlapCompileCmdHelper.EXPAND:
            unwrapped = []
            unwrapped.extend(command.code)
            unwrapped.append(command.value_expr())
            return unwrapped
        elif kind == GlapCompileCmdHelper.VARIABLE:
            raise GlapSyntaxError(context, ie_("Standalone variable"))
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
