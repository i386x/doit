#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/models/action.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-01-07 18:11:58 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Action nodes.\
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

from doit.support.errors import \
    doit_assert as _assert

from doit.support.utils import \
    deep_eq

from doit.support.visitnode import \
    VisitableNode, VisitableLeaf, \
    NullaryVisitableNode, UnaryVisitableNode, BinaryVisitableNode, \
        TernaryVisitableNode

from doit.text.pgen.models.ast import \
    AbstractSyntaxTree

def eq(x, y):
    """
    """

    return EqExpr(x, y)
#-def

def ne(x, y):
    """
    """

    return NotEqExpr(x, y)
#-def

class ActionNode(AbstractSyntaxTree):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        AbstractSyntaxTree.__init__(self)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AbstractSyntaxTree.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Expr(ActionNode):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        ActionNode.__init__(self)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and ActionNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def

    def __add__(self, rhs):
        """
        """

        return AddExpr(self, rhs)
    #-def

    def __sub__(self, rhs):
        """
        """

        return SubExpr(self, rhs)
    #-def

    def __mul__(self, rhs):
        """
        """

        return MulExpr(self, rhs)
    #-def

    def __truediv__(self, rhs):
        """
        """

        return DivExpr(self, rhs)
    #-def

    def __mod__(self, rhs):
        """
        """

        return ModExpr(self, rhs)
    #-def

    def __and__(self, rhs):
        """
        """

        return BitAndExpr(self, rhs)
    #-def

    def __or__(self, rhs):
        """
        """

        return BitOrExpr(self, rhs)
    #-def

    def __xor__(self, rhs):
        """
        """

        return BitXorExpr(self, rhs)
    #-def

    def __lshift__(self, rhs):
        """
        """

        return ShiftLeftExpr(self, rhs)
    #-def

    def __rshift__(self, rhs):
        """
        """

        return ShiftRightExpr(self, rhs)
    #-def

    def __neg__(self):
        """
        """

        return NegExpr(self)
    #-def

    def __invert__(self):
        """
        """

        return InvExpr(self)
    #-def

    def __lt__(self, rhs):
        """
        """

        return LtExpr(self, rhs)
    #-def

    def __gt__(self, rhs):
        """
        """

        return GtExpr(self, rhs)
    #-def

    def __le__(self, rhs):
        """
        """

        return LeExpr(self, rhs)
    #-def

    def __ge__(self, rhs):
        """
        """

        return GeExpr(self, rhs)
    #-def

    def __call__(self, *args):
        """
        """

        return CallExpr(self, args)
    #-def

    def __getitem__(self, item):
        """
        """

        return IndexExpr(self, item)
    #-def

    def __getattr__(self, attr):
        """
        """

        if attr[-1] == '_':
            return AccessExpr(self, Id(attr[:-1]))
        return object.__getattribute__(self, attr)
    #-def
#-class

class LExpr(Expr):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Expr.__init__(self)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Expr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class AtomicExpr(Expr, VisitableLeaf):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        Expr.__init__(self)
        VisitableLeaf.__init__(self, v)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Expr.__eq__(self, other) \
        and VisitableLeaf.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class UnaryExpr(Expr, UnaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, n):
        """
        """

        _assert(isinstance(n, Expr) and isinstance(n, VisitableNode),
            "Visitable expression expected"
        )
        Expr.__init__(self)
        UnaryVisitableNode.__init__(self, n)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Expr.__eq__(self, other) \
        and UnaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class BinaryExpr(Expr, BinaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        _assert(isinstance(lhs, Expr) and isinstance(lhs, VisitableNode),
            "Visitable expression expected"
        )
        _assert(isinstance(rhs, Expr) and isinstance(rhs, VisitableNode),
            "Visitable expression expected"
        )
        Expr.__init__(self)
        BinaryVisitableNode.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Expr.__eq__(self, other) \
        and BinaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class AddExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class SubExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class MulExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class DivExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class ModExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class BitAndExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class BitOrExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class BitXorExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class ShiftLeftExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class ShiftRightExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class NegExpr(UnaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, n):
        """
        """

        UnaryExpr.__init__(self, n)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and UnaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InvExpr(UnaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, n):
        """
        """

        UnaryExpr.__init__(self, n)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and UnaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class EqExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class NotEqExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class LtExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class GtExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class LeExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class GeExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class LogAndExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class LogOrExpr(BinaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryExpr.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and BinaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class NotExpr(UnaryExpr):
    """
    """
    __slots__ = []

    def __init__(self, n):
        """
        """

        UnaryExpr.__init__(self, n)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and UnaryExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class CallExpr(Expr, VisitableNode):
    """
    """
    __slots__ = [ '__fexpr', '__args' ]

    def __init__(self, fexpr, args):
        """
        """

        _assert(isinstance(fexpr, Expr) and isinstance(fexpr, VisitableNode),
            "Visitable expression expected"
        )
        _assert(isinstance(args, (list, tuple)), "List or tuple expected")
        for arg in args:
            _assert(isinstance(arg, Expr) and isinstance(arg, VisitableNode),
                "Visitable expression expected"
            )
        Expr.__init__(self)
        VisitableNode.__init__(self)
        self.__fexpr = fexpr
        self.__args = args
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Expr.__eq__(self, other) \
        and VisitableNode.__eq__(self, other) \
        and self.__fexpr == other.__fexpr \
        and deep_eq(self.__args, other.__args)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def

    def visit(self, f, *args):
        """
        """

        rf = self.__fexpr.visit(f, *args)
        ras = []
        for arg in self.__args:
            ras.append(arg.visit(f, *args))
        return f(self, rf, ras, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(self, self.__fexpr, self.__args, *args)
    #-def
#-class

class IndexExpr(LExpr, BinaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        _assert(isinstance(lhs, Expr) and isinstance(lhs, VisitableNode),
            "Visitable expression expected"
        )
        _assert(isinstance(rhs, Expr) and isinstance(rhs, VisitableNode),
            "Visitable expression expected"
        )
        LExpr.__init__(self)
        BinaryVisitableNode.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and LExpr.__eq__(self, other) \
        and BinaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class AccessExpr(LExpr, BinaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        _assert(isinstance(lhs, Expr) and isinstance(lhs, VisitableNode),
            "Visitable expression expected"
        )
        _assert(isinstance(rhs, Id), "Identifier expected")
        LExpr.__init__(self)
        BinaryVisitableNode.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and LExpr.__eq__(self, other) \
        and BinaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Id(LExpr, AtomicExpr):
    """
    """
    __slots__ = []

    def __init__(self, name):
        """
        """

        LExpr.__init__(self)
        AtomicExpr.__init__(self, name)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and LExpr.__eq__(self, other) \
        and AtomicExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Literal(AtomicExpr):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        AtomicExpr.__init__(self, v)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AtomicExpr.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class IntLiteral(Literal):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        _assert(isinstance(v, int), "Int expected")
        Literal.__init__(self, v)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Literal.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class FloatLiteral(Literal):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        _assert(isinstance(v, float), "Float expected")
        Literal.__init__(self, v)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Literal.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class StringLiteral(Literal):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        _assert(isinstance(v, str), "String expected")
        Literal.__init__(self, v)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Literal.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Statement(ActionNode):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        ActionNode.__init__(self)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and ActionNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Block(Statement, VisitableNode):
    """
    """
    __slots__ = [ '__stmts' ]

    def __init__(self, stmts):
        """
        """

        _assert(isinstance(stmts, (list, tuple)), "List or tuple expected")
        for stmt in stmts:
            _assert(
                isinstance(stmt, (Expr, Statement))
                and isinstance(stmt, VisitableNode),
                "Visitable statement or expression expected"
            )
        Statement.__init__(self)
        VisitableNode.__init__(self)
        self.__stmts = stmts
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and VisitableNode.__eq__(self, other) \
        and deep_eq(self.__stmts, other.__stmts)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def

    def visit(self, f, *args):
        """
        """

        r = []
        for stmt in self.__stmts:
            r.append(stmt.visit(f, *args))
        return f(self, r, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(self, self.__stmts, *args)
    #-def
#-class

class AssignBase(Statement, BinaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        _assert(isinstance(lhs, LExpr) and isinstance(lhs, VisitableNode),
            "Visitable l-expression expected"
        )
        _assert(isinstance(rhs, Expr) and isinstance(rhs, VisitableNode),
            "Visitable expression expected"
        )
        Statement.__init__(self)
        BinaryVisitableNode.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and BinaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Assign(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceAdd(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceSub(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceMul(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceDiv(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceMod(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceBitAnd(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceBitOr(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceBitXor(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceShiftLeft(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class InplaceShiftRight(AssignBase):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        AssignBase.__init__(self, lhs, rhs)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and AssignBase.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class If(Statement, VisitableNode):
    """
    """
    __slots__ = [ '__condition', '__then_part', '__elif_parts', '__else_part' ]

    def __init__(self, c, t, eict, e):
        """
        """

        _assert(isinstance(c, Expr) and isinstance(c, VisitableNode),
            "Visitable expression expected"
        )
        _assert(
            isinstance(t, (Expr, Statement)) and isinstance(t, VisitableNode),
            "Visitable statement or expression expected"
        )
        _assert(isinstance(eict, (list, tuple)), "List or tuple expected")
        for v in eict:
            _assert(isinstance(v, (list, tuple)), "List or tuple expected")
            _assert(len(v) == 2, "A pair of expr-stmt expected")
            x, y = v
            _assert(isinstance(x, Expr) and isinstance(x, VisitableNode),
                "Visitable expression expected"
            )
            _assert(
                isinstance(y, (Expr, Statement)) \
                and isinstance(y, VisitableNode),
                "Visitable statement or expression expected"
            )
        if e is not None:
            _assert(
                isinstance(e, (Expr, Statement)) \
                and isinstance(e, VisitableNode),
                "Visitable statement or expression expected"
            )
        Statement.__init__(self)
        VisitableNode.__init__(self)
        self.__condition = c
        self.__then_part = t
        self.__elif_parts = eict
        self.__else_part = e
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and VisitableNode.__eq__(self, other) \
        and self.__condition == other.__condition \
        and self.__then_part == other.__then_part \
        and deep_eq(self.__elif_parts, other.__elif_parts) \
        and self.__else_part == other.__else_part
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def

    def visit(self, f, *args):
        """
        """

        rc = self.__condition.visit(f, *args)
        rt = self.__then_part.visit(f, *args)
        rei = []
        for c, t in self.__elif_parts:
            reic = c.visit(f, *args)
            reit = t.visit(f, *args)
            rei.append((reic, reit))
        re = None
        if self.__else_part is not None:
            re = self.__else_part.visit(f, *args)
        return f(self, rc, rt, rei, re, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(
            self,
            self.__condition,
            self.__then_part,
            self.__elif_parts,
            self.__else_part,
            *args
        )
    #-def
#-class

class Case(Statement, VisitableNode):
    """
    """
    __slots__ = [ '__switch_expr', '__cases', '__default' ]

    def __init__(self, se, cs, d):
        """
        """

        _assert(isinstance(se, Expr) and isinstance(se, VisitableNode),
            "Visitable expression expected"
        )
        _assert(isinstance(cs, (list, tuple)), "List or tuple expected")
        for cecb in cs:
            _assert(isinstance(cecb, (list, tuple)), "List or tuple expected")
            _assert(len(cecb) == 2, "A pair of expr-stmt expected")
            ce, cb = cecb
            _assert(isinstance(ce, Expr) and isinstance(ce, VisitableNode),
                "Visitable expression expected"
            )
            _assert(isinstance(cb, (list, tuple)), "List or tuple expected")
            for s_ in cb:
                _assert(
                    isinstance(s_, (Expr, Statement)) \
                    and isinstance(s_, VisitableNode),
                    "Visitable statement or expression expected"
                )
        if d is not None:
            _assert(isinstance(d, (list, tuple)), "List or tuple expected")
            for x in d:
                _assert(
                    isinstance(x, (Expr, Statement)) \
                    and isinstance(x, VisitableNode),
                    "Visitable statement or expression expected"
                )
        Statement.__init__(self)
        VisitableNode.__init__(self)
        self.__switch_expr = se
        self.__cases = cs
        self.__default = d
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and VisitableNode.__eq__(self, other) \
        and self.__switch_expr == other.__switch_expr \
        and deep_eq(self.__cases, other.__cases) \
        and deep_eq(self.__default, other.__default)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def

    def visit(self, f, *args):
        """
        """

        rse = self.__switch_expr.visit(f, *args)
        rcs = []
        for ce, cb in self.__cases:
            rce = ce.visit(f, *args)
            rcb = []
            for x in cb:
                rcb.append(x.visit(f, *args))
            rcs.append((rce, rcb))
        rd = None
        if self.__default is not None:
            rd = []
            for x in self.__default:
                rd.append(x.visit(f, *args))
        return f(self, rse, rcs, rd, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(self, self.__switch_expr, self.__cases, self.__default, *args)
    #-def
#-class

class For(Statement, TernaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, v, e, b):
        """
        """

        _assert(isinstance(v, Id), "Identifier expected")
        _assert(isinstance(e, Expr) and isinstance(e, VisitableNode),
            "Visitable expression expected"
        )
        _assert(
            isinstance(b, (Expr, Statement)) and isinstance(b, VisitableNode),
            "Visitable statement or expression expected"
        )
        Statement.__init__(self)
        TernaryVisitableNode.__init__(self, v, e, b)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and TernaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class While(Statement, BinaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, c, b):
        """
        """

        _assert(isinstance(c, Expr) and isinstance(c, VisitableNode),
            "Visitable expression expected"
        )
        _assert(
            isinstance(b, (Expr, Statement)) and isinstance(b, VisitableNode),
            "Visitable statement or expression expected"
        )
        Statement.__init__(self)
        BinaryVisitableNode.__init__(self, c, b)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and BinaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class DoWhile(Statement, BinaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, b, c):
        """
        """

        _assert(
            isinstance(b, (Expr, Statement)) and isinstance(b, VisitableNode),
            "Visitable statement or expression expected"
        )
        _assert(isinstance(c, Expr) and isinstance(c, VisitableNode),
            "Visitable expression expected"
        )
        Statement.__init__(self)
        BinaryVisitableNode.__init__(self, b, c)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and BinaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Continue(Statement, NullaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Statement.__init__(self)
        NullaryVisitableNode.__init__(self)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and NullaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Break(Statement, NullaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Statement.__init__(self)
        NullaryVisitableNode.__init__(self)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and NullaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class Return(Statement, NullaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Statement.__init__(self)
        NullaryVisitableNode.__init__(self)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and NullaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

class ReturnWithValue(Statement, UnaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, e):
        """
        """

        _assert(isinstance(e, Expr) and isinstance(e, VisitableNode),
            "Visitable expression expected"
        )
        Statement.__init__(self)
        UnaryVisitableNode.__init__(self, e)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Statement.__eq__(self, other) \
        and UnaryVisitableNode.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class
