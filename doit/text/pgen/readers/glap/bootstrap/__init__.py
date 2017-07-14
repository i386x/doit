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

class GlapCmdExprHelper(object):
    """
    """
    UNSPECIFIED = -1
    NULLARY_EPXR = 0
    UNARY_EXPR = 1
    BINARY_EXPR = 2
    INDEX_EXPR = 3
    ACCESS_EXPR = 4
    ASSIGN_EXPR = 5
    CALL_EXPR = 6
    VARIABLE = 7
    LITERAL = 8
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
    def make_unary(cls, context, loc, expr, unop):
        """
        """

        o = cls(context, loc, "")
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

        o = cls(context, loc, "")
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

        o = cls(context, loc, "")
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

        o = cls(context, loc, "")
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

        o = cls(context, loc, "")
        o.kind = cls.ASSIGN_EXPR
        if lhs.kind == cls.VARIABLE:
            if inplaceop:
                a = GetLocal(lhs.node.value())
                a.set_location(*make_location(context, lhs.node.position()))
                ve = inplaceop(a, rhs.value_expr())
                ve.set_location(*make_location(context, loc))
                o.node = SetLocal(lhs.node.value(), ve)
            else:
                o.node = SetLocal(lhs.node.value(), rhs.value_expr())
        elif lhs.kind == cls.INDEX_EXPR:
            if inplaceop:
                ve = inplaceop(lhs.node, rhs.value_expr())
                ve.set_location(*make_location(context, loc))
                o.node = SetItem(
                    lhs.node.operands[0], lhs.node.operands[1], ve
                )
            else:
                o.node = SetItem(
                    lhs.node.operands[0],
                    lhs.node.operands[1],
                    rhs.value_expr()
                )
        elif lhs.kind == cls.ACCESS_EXPR:
            if inplaceop:
                ve = inplaceop(lhs.node, rhs.value_expr())
                ve.set_location(*make_location(context, loc))
                o.node = SetMember(lhs.node.module, lhs.node.member, ve)
            else:
                o.node = SetMember(
                    lhs.node.module, lhs.node.member, rhs.value_expr()
                )
        else:
            raise GlapSyntaxError(context,
                "Left-hand side of assignment must be l-value", loc
            )
        o.node.set_location(*make_location(context, loc))
        o.code.extend(lhs.code)
        o.code.extend(rhs.code)
        o.code.append(o.node)
        o.vars.extend(rhs.vars)
        if lhs.kind == cls.VARIABLE:
            o.vars.insert(0, lhs.node.value())
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

        o = cls(context, loc, "")
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
        o.kind = cls.VARIABLE
        o.node = var
        return o
    #-def

    @classmethod
    def make_getvalue(cls, context, var):
        """
        """

        o = cls(context, var.position(), "")
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

        actions = context.actions
        if actions.macro_nest_level <= 0:
            raise GlapSyntaxError(context,
                "Macro parameter must be used only inside macro body",
                var.position()
            )
        o = cls(context, var.position())
    #-def
#-class

class GlapParserActions(object):
    """
    """
    __slots__ = [ 'context', 'actions' ]

    def __init__(self, context):
        """
        """

        context.actions = self
        self.context = context
        self.macro_nest_level = 0
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

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs)
    #-def

    def on_c_expr_iadd(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Add)
    #-def

    def on_c_expr_isub(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Sub)
    #-def

    def on_c_expr_imult(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Mul)
    #-def

    def on_c_expr_idiv(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Div)
    #-def

    def on_c_expr_imod(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Mod)
    #-def

    def on_c_expr_iband(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, BitAnd)
    #-def

    def on_c_expr_ibor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, BitOr)
    #-def

    def on_c_expr_ibxor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, BitXor)
    #-def

    def on_c_expr_ibshl(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, ShiftL)
    #-def

    def on_c_expr_ibshr(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, ShiftR)
    #-def

    def on_c_expr_iland(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, And)
    #-def

    def on_c_expr_ilor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Or)
    #-def

    def on_c_expr_icat(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Concat)
    #-def

    def on_c_expr_ijoin(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Join)
    #-def

    def on_c_expr_imerge(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_assign(context, loc, lhs, rhs, Merge)
    #-def

    def on_c_expr_lor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Or)
    #-def

    def on_c_expr_land(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, And)
    #-def

    def on_c_expr_lt(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Lt)
    #-def

    def on_c_expr_gt(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Gt)
    #-def

    def on_c_expr_le(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Le)
    #-def

    def on_c_expr_ge(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Ge)
    #-def

    def on_c_expr_eq(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Eq)
    #-def

    def on_c_expr_ne(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Ne)
    #-def

    def on_c_expr_is(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Is)
    #-def

    def on_c_expr_in(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Contains)
    #-def

    def on_c_expr_bor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, BitOr)
    #-def

    def on_c_expr_band(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, BitAnd)
    #-def

    def on_c_expr_bxor(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, BitXor)
    #-def

    def on_c_expr_bshl(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, ShiftL)
    #-def

    def on_c_expr_bshr(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, ShiftR)
    #-def

    def on_c_expr_add(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Add)
    #-def

    def on_c_expr_sub(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Sub)
    #-def

    def on_c_expr_cat(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Concat)
    #-def

    def on_c_expr_join(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Join)
    #-def

    def on_c_expr_merge(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Merge)
    #-def

    def on_c_expr_mult(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Mul)
    #-def

    def on_c_expr_div(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Div)
    #-def

    def on_c_expr_mod(self, context, loc, lhs, rhs):
        """
        """

        return GlapCmdExprHelper.make_binary(context, loc, lhs, rhs, Mod)
    #-def

    def on_c_expr_call(self, context, loc, f, fargs):
        """
        """

        return GlapCmdExprHelper.make_call(context, loc, f, fargs)
    #-def

    def on_c_expr_neg(self, context, loc, expr):
        """
        """

        return GlapCmdExprHelper.make_unary(context, loc, expr, Neg)
    #-def

    def on_c_expr_lnot(self, context, loc, expr):
        """
        """

        return GlapCmdExprHelper.make_unary(context, loc, expr, Not)
    #-def

    def on_c_expr_binv(self, context, loc, expr):
        """
        """

        return GlapCmdExprHelper.make_unary(context, loc, expr, Inv)
    #-def

    def on_c_expr_index(self, context, loc, expr, idx):
        """
        """

        return GlapCmdExprHelper.make_index(context, loc, expr, idx)
    #-def

    def on_c_expr_access(self, context, loc, module, member):
        """
        """

        return GlapCmdExprHelper.make_access(context, loc, module, member)
    #-def

    def on_c_expr_atom_var(self, context, var):
        """
        """

        return GlapCmdExprHelper.make_variable(var)
    #-def

    def on_c_expr_atom_getval(self, context, var):
        """
        """

        return GlapCmdExprHelper.make_getvalue(context, var)
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
