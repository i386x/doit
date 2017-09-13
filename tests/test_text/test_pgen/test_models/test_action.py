#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/test_models/test_action.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-12-20 14:26:50 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Action nodes tests.\
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

import unittest

from doit.support.errors import DoItAssertionError

from doit.text.pgen.models.action import \
    eq, ne, \
    ActionNode, \
    Expr, LExpr, \
    AtomicExpr, \
    UnaryExpr, BinaryExpr, \
    AddExpr, SubExpr, MulExpr, DivExpr, ModExpr, \
    BitAndExpr, BitOrExpr, BitXorExpr, \
    ShiftLeftExpr, ShiftRightExpr, \
    NegExpr, InvExpr, \
    EqExpr, NotEqExpr, LtExpr, GtExpr, LeExpr, GeExpr, \
    LogAndExpr, LogOrExpr, NotExpr, \
    CallExpr, IndexExpr, AccessExpr, \
    Id, \
    Literal, IntLiteral, FloatLiteral, StringLiteral, \
    Statement, \
        Block, \
        AssignBase, \
            Assign, \
            InplaceAdd, InplaceSub, InplaceMul, InplaceDiv, InplaceMod, \
            InplaceBitAnd, InplaceBitOr, InplaceBitXor, \
            InplaceShiftLeft, InplaceShiftRight, \
        If, \
        Case, \
        For, While, DoWhile, \
        Continue, Break, \
        Return, ReturnWithValue

class TestActionNodeCase(unittest.TestCase):

    def test_equality(self):
        self.assertNotEqual(ActionNode(), 1)
        self.assertEqual(ActionNode(), ActionNode())
    #-def

    def test_action_node_initialization(self):
        ActionNode()
    #-def
#-class

class TestExprCase(unittest.TestCase):

    def test_equality(self):
        a = AtomicExpr(1)
        b = AtomicExpr(2)
        c = AtomicExpr(1)

        self.assertNotEqual(Expr(), 1)
        self.assertEqual(Expr(), Expr())

        self.assertNotEqual(LExpr(), 1)
        self.assertEqual(LExpr(), LExpr())
        self.assertNotEqual(LExpr(), Expr())

        self.assertNotEqual(a, 1)
        self.assertEqual(a, c)
        self.assertNotEqual(a, b)

        self.assertNotEqual(UnaryExpr(a), 1)
        self.assertNotEqual(UnaryExpr(a), UnaryExpr(b))
        self.assertEqual(UnaryExpr(a), UnaryExpr(c))

        self.assertNotEqual(BinaryExpr(a, b), 1)
        self.assertNotEqual(BinaryExpr(a, b), BinaryExpr(b, a))
        self.assertEqual(BinaryExpr(a, c), BinaryExpr(c, a))

        self.assertNotEqual(a + b, 1)
        self.assertNotEqual(a + b, b + a)
        self.assertEqual(a + c, c + a)
        self.assertNotEqual(a + c, c - a)

        self.assertNotEqual(a - b, 1)
        self.assertNotEqual(a - b, b - a)
        self.assertEqual(a - c, c - a)
        self.assertNotEqual(a - c, c * a)

        self.assertNotEqual(a * b, 1)
        self.assertNotEqual(a * b, b * a)
        self.assertEqual(a * c, c * a)
        self.assertNotEqual(a * c, c / a)

        self.assertNotEqual(a / b, 1)
        self.assertNotEqual(a / b, b / a)
        self.assertEqual(a / c, c / a)
        self.assertNotEqual(a / c, c % a)

        self.assertNotEqual(a % b, 1)
        self.assertNotEqual(a % b, b % a)
        self.assertEqual(a % c, c % a)
        self.assertNotEqual(a % c, c + a)

        self.assertNotEqual(a & b, 1)
        self.assertNotEqual(a & b, b & a)
        self.assertEqual(a & c, c & a)
        self.assertNotEqual(a & c, c + a)

        self.assertNotEqual(a | b, 1)
        self.assertNotEqual(a | b, b | a)
        self.assertEqual(a | c, c | a)
        self.assertNotEqual(a | c, c & a)

        self.assertNotEqual(a ^ b, 1)
        self.assertNotEqual(a ^ b, b ^ a)
        self.assertEqual(a ^ c, c ^ a)
        self.assertNotEqual(a ^ c, c | a)

        self.assertNotEqual(a << b, 1)
        self.assertNotEqual(a << b, b << a)
        self.assertEqual(a << c, c << a)
        self.assertNotEqual(a << c, c >> a)

        self.assertNotEqual(a >> b, 1)
        self.assertNotEqual(a >> b, b >> a)
        self.assertEqual(a >> c, c >> a)
        self.assertNotEqual(a >> c, c << a)

        self.assertNotEqual(-a, 1)
        self.assertNotEqual(-a, -b)
        self.assertEqual(-a, -c)
        self.assertNotEqual(-a, ~c)

        self.assertNotEqual(~a, 1)
        self.assertNotEqual(~a, ~b)
        self.assertEqual(~a, ~c)
        self.assertNotEqual(~a, -c)

        self.assertNotEqual(eq(a, b), 1)
        self.assertNotEqual(eq(a, b), eq(b, a))
        self.assertEqual(eq(a, c), eq(c, a))
        self.assertNotEqual(eq(a, c), ne(c, a))

        self.assertNotEqual(ne(a, b), 1)
        self.assertNotEqual(ne(a, b), ne(b, a))
        self.assertEqual(ne(a, c), ne(c, a))
        self.assertNotEqual(ne(a, c), eq(c, a))

        self.assertNotEqual(a < b, 1)
        self.assertNotEqual(a < b, b < a)
        self.assertEqual(a < c, c < a)
        self.assertNotEqual(a < c, c > a)

        self.assertNotEqual(a > b, 1)
        self.assertNotEqual(a > b, b > a)
        self.assertEqual(a > c, c > a)
        self.assertNotEqual(a > c, c < a)

        self.assertNotEqual(a <= b, 1)
        self.assertNotEqual(a <= b, b <= a)
        self.assertEqual(a <= c, c <= a)
        self.assertNotEqual(a <= c, c >= a)

        self.assertNotEqual(a >= b, 1)
        self.assertNotEqual(a >= b, b >= a)
        self.assertEqual(a >= c, c >= a)
        self.assertNotEqual(a >= c, c <= a)

        self.assertNotEqual(LogAndExpr(a, b), 1)
        self.assertNotEqual(LogAndExpr(a, b), LogAndExpr(b, a))
        self.assertEqual(LogAndExpr(a, c), LogAndExpr(c, a))
        self.assertNotEqual(LogAndExpr(a, c), LogOrExpr(c, a))

        self.assertNotEqual(LogOrExpr(a, b), 1)
        self.assertNotEqual(LogOrExpr(a, b), LogOrExpr(b, a))
        self.assertEqual(LogOrExpr(a, c), LogOrExpr(c, a))
        self.assertNotEqual(LogOrExpr(a, c), LogAndExpr(c, a))

        self.assertNotEqual(NotExpr(a), 1)
        self.assertNotEqual(NotExpr(a), NotExpr(b))
        self.assertEqual(NotExpr(a), NotExpr(c))
        self.assertNotEqual(NotExpr(a), -c)

        self.assertNotEqual(a(), 1)
        self.assertNotEqual(a(a), 1)
        self.assertNotEqual(a(a, b), 1)
        self.assertNotEqual(a(a, b, c), 1)
        self.assertNotEqual(a(), a(a))
        self.assertEqual(a(a), a(a))
        self.assertNotEqual(a(a, b), a(b, a))
        self.assertEqual(a(), c())
        self.assertEqual(a(a), c(c))
        self.assertEqual(a(c), c(a))
        self.assertEqual(a(a, c), a(c, a))
        self.assertNotEqual(a(a), a[a])

        self.assertNotEqual(a[b], 1)
        self.assertNotEqual(a[b], b[a])
        self.assertEqual(a[c], c[a])
        self.assertNotEqual(a[c], c(a))

        self.assertNotEqual(a.x_, 1)
        self.assertNotEqual(a.x_, b.x_)
        self.assertNotEqual(a.x_, a.y_)
        self.assertEqual(a.x_, a.x_)
        self.assertEqual(a.x_, c.x_)
        self.assertNotEqual(a.x_, a[b])
    #-def

    def test_expr_initialization(self):
        Expr()
    #-def

    def test_lexpr_initialization(self):
        LExpr()
    #-def

    def test_atomic_expr(self):
        AtomicExpr(1)
    #-def

    def test_unary_expr(self):
        with self.assertRaises(DoItAssertionError):
            UnaryExpr(1)
        with self.assertRaises(DoItAssertionError):
            UnaryExpr(Expr())
        UnaryExpr(AtomicExpr(""))
    #-def

    def test_binary_expr(self):
        e, a = Expr(), AtomicExpr(1)

        with self.assertRaises(DoItAssertionError):
            BinaryExpr(1, 1)
        with self.assertRaises(DoItAssertionError):
            BinaryExpr(1, e)
        with self.assertRaises(DoItAssertionError):
            BinaryExpr(1, a)
        with self.assertRaises(DoItAssertionError):
            BinaryExpr(e, 1)
        with self.assertRaises(DoItAssertionError):
            BinaryExpr(e, e)
        with self.assertRaises(DoItAssertionError):
            BinaryExpr(e, a)
        with self.assertRaises(DoItAssertionError):
            BinaryExpr(a, 1)
        with self.assertRaises(DoItAssertionError):
            BinaryExpr(a, e)
        BinaryExpr(a, a)
    #-def

    def test_expr_operators(self):
        e1, e2 = AtomicExpr(0), AtomicExpr(1)

        self.assertIsInstance(e1 + e2, AddExpr)
        self.assertIsInstance(e1 - e2, SubExpr)
        self.assertIsInstance(e1 * e2, MulExpr)
        self.assertIsInstance(e1 / e2, DivExpr)
        self.assertIsInstance(e1 % e2, ModExpr)
        self.assertIsInstance(e1 & e2, BitAndExpr)
        self.assertIsInstance(e1 | e2, BitOrExpr)
        self.assertIsInstance(e1 ^ e2, BitXorExpr)
        self.assertIsInstance(e1 << e2, ShiftLeftExpr)
        self.assertIsInstance(e1 >> e2, ShiftRightExpr)
        self.assertIsInstance(-e1, NegExpr)
        self.assertIsInstance(~e1, InvExpr)
        self.assertIsInstance(eq(e1, e2), EqExpr)
        self.assertIsInstance(ne(e1, e2), NotEqExpr)
        self.assertIsInstance(e1 < e2, LtExpr)
        self.assertIsInstance(e1 > e2, GtExpr)
        self.assertIsInstance(e1 <= e2, LeExpr)
        self.assertIsInstance(e1 >= e2, GeExpr)
        LogAndExpr(e1, e2)
        LogOrExpr(e1, e2)
        NotExpr(e1)
        self.assertIsInstance(e1(), CallExpr)
        self.assertIsInstance(e1(e2), CallExpr)
        self.assertIsInstance(e1(e2, e2), CallExpr)
        self.assertIsInstance(e1(e2, e2, e2), CallExpr)
        self.assertIsInstance(e1[e2], IndexExpr)
        self.assertIsInstance(e1.visit_, AccessExpr)
        self.assertNotIsInstance(e1.visit, AccessExpr)
    #-def
#-class

class TestCallExprCase(unittest.TestCase):

    def test_call_expr_initialization(self):
        e, a = Expr(), AtomicExpr(1)

        with self.assertRaises(DoItAssertionError):
            CallExpr(1, [])
        with self.assertRaises(DoItAssertionError):
            CallExpr(e, [])
        CallExpr(a, [])
        CallExpr(a, ())
        with self.assertRaises(DoItAssertionError):
            CallExpr(a, 1)
        with self.assertRaises(DoItAssertionError):
            CallExpr(a, [1])
        with self.assertRaises(DoItAssertionError):
            CallExpr(a, [e])
        CallExpr(a, [a])
    #-def

    def test_call_expr_visit_and_traverse(self):
        def f(node, *args):
            if isinstance(node, AtomicExpr):
                return "%s%s-%s" % (args[1], args[2], args[0])
            elif isinstance(node, CallExpr):
                return "<%s%s>%s(%s)" % (
                    args[2], args[3], args[0], ", ".join(args[1])
                )
            return "<bad node>"
        def t(node, *args):
            if isinstance(node, AtomicExpr):
                return "%s%s-%s" % (args[1], args[2], args[0])
            elif isinstance(node, CallExpr):
                x = args[0].traverse(t, args[2], args[3])
                y = [z.traverse(t, args[2], args[3]) for z in args[1]]
                return "<%s%s>%s(%s)" % (args[2], args[3], x, ", ".join(y))
            return "<bad node>"
        a1 = AtomicExpr("func")
        a2 = AtomicExpr("A")
        a3 = AtomicExpr("B")
        r = CallExpr(a1, [a2, a3]).visit(f, "p", "q")
        self.assertEqual(r, "<pq>pq-func(pq-A, pq-B)")
        s = CallExpr(a1, [a2, a3]).traverse(t, "u", "v")
        self.assertEqual(s, "<uv>uv-func(uv-A, uv-B)")
    #-def
#-class

class TestIndexExprCase(unittest.TestCase):

    def test_index_expr_initialization(self):
        e, a = Expr(), AtomicExpr(1)

        with self.assertRaises(DoItAssertionError):
            IndexExpr(1, a)
        with self.assertRaises(DoItAssertionError):
            IndexExpr(e, a)
        with self.assertRaises(DoItAssertionError):
            IndexExpr(a, 1)
        with self.assertRaises(DoItAssertionError):
            IndexExpr(a, e)
        IndexExpr(a, a)
    #-def
#-class

class TestAccessExprCase(unittest.TestCase):

    def test_access_expr_initialization(self):
        e, a, i = Expr(), AtomicExpr(1), Id("abc")

        with self.assertRaises(DoItAssertionError):
            AccessExpr(1, i)
        with self.assertRaises(DoItAssertionError):
            AccessExpr(e, i)
        with self.assertRaises(DoItAssertionError):
            AccessExpr(a, 1)
        with self.assertRaises(DoItAssertionError):
            AccessExpr(a, e)
        with self.assertRaises(DoItAssertionError):
            AccessExpr(a, a)
        AccessExpr(a, i)
        with self.assertRaises(DoItAssertionError):
            AccessExpr(i, 1)
        with self.assertRaises(DoItAssertionError):
            AccessExpr(i, e)
        with self.assertRaises(DoItAssertionError):
            AccessExpr(i, a)
        AccessExpr(i, i)
    #-def
#-class

class TestIdAndLiteralsCase(unittest.TestCase):

    def test_equality(self):
        self.assertNotEqual(Id("x"), 1)
        self.assertNotEqual(Id("x"), AtomicExpr("x"))
        self.assertNotEqual(Id("x"), Id("y"))
        self.assertEqual(Id("x"), Id("x"))

        self.assertNotEqual(Literal(1), 1)
        self.assertNotEqual(Literal("x"), AtomicExpr("x"))
        self.assertNotEqual(Literal(1), Literal(2))
        self.assertEqual(Literal(1), Literal(1))

        self.assertNotEqual(IntLiteral(1), 1)
        self.assertNotEqual(IntLiteral(1), AtomicExpr(1))
        self.assertNotEqual(IntLiteral(1), IntLiteral(2))
        self.assertEqual(IntLiteral(1), IntLiteral(1))

        self.assertNotEqual(FloatLiteral(1.0), 1.0)
        self.assertNotEqual(FloatLiteral(1.0), AtomicExpr(1.0))
        self.assertNotEqual(FloatLiteral(1.0), FloatLiteral(2.0))
        self.assertEqual(FloatLiteral(1.0), FloatLiteral(1.0))

        self.assertNotEqual(StringLiteral("1"), "1")
        self.assertNotEqual(StringLiteral("1"), AtomicExpr("1"))
        self.assertNotEqual(StringLiteral("1"), StringLiteral("2"))
        self.assertEqual(StringLiteral("1"), StringLiteral("1"))
    #-def

    def test_id_and_literals(self):
        Id("g")
        Literal(0.1)
        with self.assertRaises(DoItAssertionError):
            IntLiteral("")
        IntLiteral(5)
        with self.assertRaises(DoItAssertionError):
            FloatLiteral(2)
        FloatLiteral(.2)
        with self.assertRaises(DoItAssertionError):
            StringLiteral({})
        StringLiteral("abc")
    #-def
#-class

class TestStatementsCase(unittest.TestCase):

    def test_equality(self):
        self.assertNotEqual(Statement(), 1)
        self.assertEqual(Statement(), Statement())

        self.assertNotEqual(Block([]), Statement())
        self.assertNotEqual(Block([]), Block([Literal(1)]))
        self.assertNotEqual(Block([Literal(1)]), Block([Literal(2)]))
        self.assertEqual(Block([Literal(1)]), Block([Literal(1)]))

        self.assertNotEqual(AssignBase(Id("a"), Literal(1)), Statement())
        self.assertNotEqual(
            AssignBase(Id("a"), Literal(1)),
            AssignBase(Id("b"), Literal(1))
        )
        self.assertNotEqual(
            AssignBase(Id("a"), Literal(1)),
            AssignBase(Id("a"), Literal(2))
        )
        self.assertEqual(
            AssignBase(Id("a"), Literal(1)),
            AssignBase(Id("a"), Literal(1))
        )

        self.assertNotEqual(Assign(Id("a"), Literal(1)), Statement())
        self.assertNotEqual(
            Assign(Id("a"), Literal(1)),
            Assign(Id("b"), Literal(1))
        )
        self.assertNotEqual(
            Assign(Id("a"), Literal(1)),
            Assign(Id("a"), Literal(2))
        )
        self.assertEqual(
            Assign(Id("a"), Literal(1)),
            Assign(Id("a"), Literal(1))
        )

        for cls in (
            InplaceAdd, InplaceSub, InplaceMul, InplaceDiv, InplaceMod,
            InplaceBitAnd, InplaceBitOr, InplaceBitXor,
            InplaceShiftLeft, InplaceShiftRight
        ):
            self.assertNotEqual(cls(Id("a"), Literal(1)), Statement())
            self.assertNotEqual(
                cls(Id("a"), Literal(1)),
                cls(Id("b"), Literal(1))
            )
            self.assertNotEqual(
                cls(Id("a"), Literal(1)),
                cls(Id("a"), Literal(2))
            )
            self.assertEqual(
                cls(Id("a"), Literal(1)),
                cls(Id("a"), Literal(1))
            )

        self.assertNotEqual(
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], Id("e")),
            Statement()
        )
        self.assertNotEqual(
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], Id("e")),
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], None)
        )
        self.assertEqual(
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], None),
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], None)
        )
        self.assertNotEqual(
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], Id("e")),
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], Id("f"))
        )
        self.assertNotEqual(
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], Id("e")),
            If(Id("a"), Block([Id("b")]), [(Id("c_"), Id("d"))], Id("e"))
        )
        self.assertEqual(
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], Id("e")),
            If(Id("a"), Block([Id("b")]), [(Id("c"), Id("d"))], Id("e"))
        )

        self.assertNotEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Statement()
        )
        self.assertNotEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Case(Id("a"), [(Id("b"), [Id("c")])], None)
        )
        self.assertNotEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d_")])
        )
        self.assertNotEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Case(Id("a"), [(Id("b"), [])], [Id("d")])
        )
        self.assertNotEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Case(Id("a"), [], [Id("d")])
        )
        self.assertNotEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Case(Id("a"), [(Id("b"), [Id("c_")])], [Id("d")])
        )
        self.assertNotEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Case(Id("a_"), [(Id("b"), [Id("c")])], [Id("d")])
        )
        self.assertNotEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Case(Id("a"), [(Id("b_"), [Id("c")])], [Id("d")])
        )
        self.assertEqual(
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")]),
            Case(Id("a"), [(Id("b"), [Id("c")])], [Id("d")])
        )

        self.assertNotEqual(
            For(Id("a"), Id("b"), Id("c")),
            Statement()
        )
        self.assertNotEqual(
            For(Id("a"), Id("b"), Id("c")),
            For(Id("a"), Id("b"), Id("c_"))
        )
        self.assertNotEqual(
            For(Id("a"), Id("b"), Id("c")),
            For(Id("a"), Id("b_"), Id("c"))
        )
        self.assertNotEqual(
            For(Id("a"), Id("b"), Id("c")),
            For(Id("a_"), Id("b"), Id("c"))
        )
        self.assertEqual(
            For(Id("a"), Id("b"), Id("c")),
            For(Id("a"), Id("b"), Id("c"))
        )

        self.assertNotEqual(
            While(Id("a"), Id("b")),
            Statement()
        )
        self.assertNotEqual(
            While(Id("a"), Id("b")),
            While(Id("a"), Id("b_"))
        )
        self.assertNotEqual(
            While(Id("a"), Id("b")),
            While(Id("a_"), Id("b"))
        )
        self.assertEqual(
            While(Id("a"), Id("b")),
            While(Id("a"), Id("b"))
        )

        self.assertNotEqual(
            DoWhile(Id("a"), Id("b")),
            Statement()
        )
        self.assertNotEqual(
            DoWhile(Id("a"), Id("b")),
            DoWhile(Id("a"), Id("b_"))
        )
        self.assertNotEqual(
            DoWhile(Id("a"), Id("b")),
            DoWhile(Id("a_"), Id("b"))
        )
        self.assertEqual(
            DoWhile(Id("a"), Id("b")),
            DoWhile(Id("a"), Id("b"))
        )

        self.assertNotEqual(Break(), Statement())
        self.assertEqual(Break(), Break())

        self.assertNotEqual(Continue(), Statement())
        self.assertEqual(Continue(), Continue())

        self.assertNotEqual(Return(), Statement())
        self.assertEqual(Return(), Return())

        self.assertNotEqual(ReturnWithValue(Id("a")), Statement())
        self.assertNotEqual(ReturnWithValue(Id("a")), ReturnWithValue(Id("b")))
        self.assertEqual(ReturnWithValue(Id("a")), ReturnWithValue(Id("a")))
    #-def

    def test_statement_initialization(self):
        Statement()
    #-def

    def test_block_statement_initialization(self):
        s1 = Assign(Id("x"), Id("y"))
        s2 = Assign(Id("y"), Id("z"))

        with self.assertRaises(DoItAssertionError):
            Block(0)
        Block(())
        Block([])
        with self.assertRaises(DoItAssertionError):
            Block([1])
        with self.assertRaises(DoItAssertionError):
            Block([Statement()])
        with self.assertRaises(DoItAssertionError):
            Block([1, s1])
        Block([s1])
        Block([s1, s2])
    #-def

    def test_block_statement_visit_and_traverse(self):
        s1 = Assign(Id("x"), Id("y"))
        s2 = Assign(Id("y"), Id("z"))

        def f(node, *args):
            if isinstance(node, Id):
                return "%s%s%s" % (args[1], args[0], args[2])
            elif isinstance(node, Assign):
                return "%s = %s" % (args[0], args[1])
            elif isinstance(node, Block):
                return "{%s}" % ("; ".join(args[0]),)
            return "<bad node>"
        def t(node, *args):
            if isinstance(node, Id):
                return "%s%s%s" % (args[1], args[0], args[2])
            elif isinstance(node, Assign):
                l = args[0].traverse(t, args[2], args[3])
                r = args[1].traverse(t, args[2], args[3])
                return "%s = %s" % (l, r)
            elif isinstance(node, Block):
                cs = "; ".join([
                    x.traverse(t, args[1], args[2]) for x in args[0]
                ])
                return "{%s}" % cs
            return "<bad node>"
        self.assertEqual(Block([]).visit(f, "_", "_"), "{}")
        self.assertEqual(Block([s1]).visit(f, "_", "_"), "{_x_ = _y_}")
        self.assertEqual(
            Block([s1, s2]).visit(f, "_", "_"), "{_x_ = _y_; _y_ = _z_}"
        )
        self.assertEqual(Block([]).traverse(t, "_", "_"), "{}")
        self.assertEqual(Block([s1]).traverse(t, "_", "_"), "{_x_ = _y_}")
        self.assertEqual(
            Block([s1, s2]).traverse(t, "_", "_"), "{_x_ = _y_; _y_ = _z_}"
        )
    #-def

    def test_assign_base_initialization(self):
        e, a, i = Expr(), AtomicExpr(1), Id("x")

        with self.assertRaises(DoItAssertionError):
            AssignBase(1, a)
        with self.assertRaises(DoItAssertionError):
            AssignBase(e, a)
        with self.assertRaises(DoItAssertionError):
            AssignBase(a, a)
        with self.assertRaises(DoItAssertionError):
            AssignBase(i, 1)
        with self.assertRaises(DoItAssertionError):
            AssignBase(i, e)
        AssignBase(i, a)
        AssignBase(i, i)
    #-def

    def test_assign_statement_initialization(self):
        Assign(Id("a"), Id("b"))
        InplaceAdd(Id("a"), Id("b"))
        InplaceSub(Id("a"), Id("b"))
        InplaceMul(Id("a"), Id("b"))
        InplaceDiv(Id("a"), Id("b"))
        InplaceMod(Id("a"), Id("b"))
        InplaceBitAnd(Id("a"), Id("b"))
        InplaceBitOr(Id("a"), Id("b"))
        InplaceBitXor(Id("a"), Id("b"))
        InplaceShiftLeft(Id("a"), Id("b"))
        InplaceShiftRight(Id("a"), Id("b"))
    #-def

    def test_if_statement_initialization(self):
        e, a, i = Expr(), AtomicExpr(0), Id("a")
        s1 = Assign(Id("a"), Id("b"))

        with self.assertRaises(DoItAssertionError):
            If(1, s1, [], None)
        with self.assertRaises(DoItAssertionError):
            If(e, s1, [], None)
        If(a, s1, [], None)
        If(i, s1, [], None)
        with self.assertRaises(DoItAssertionError):
            If(a, 1, [], None)
        with self.assertRaises(DoItAssertionError):
            If(a, Statement(), [], None)
        with self.assertRaises(DoItAssertionError):
            If(i, s1, 1, None)
        If(i, s1, (), None)
        with self.assertRaises(DoItAssertionError):
            If(i, s1, (1,), None)
        with self.assertRaises(DoItAssertionError):
            If(i, s1, [1,], None)
        with self.assertRaises(DoItAssertionError):
            If(i, s1, [[]], None)
        with self.assertRaises(DoItAssertionError):
            If(i, s1, [()], None)
        with self.assertRaises(DoItAssertionError):
            If(a, s1, [(1, s1)], None)
        with self.assertRaises(DoItAssertionError):
            If(a, s1, [(e, s1)], None)
        with self.assertRaises(DoItAssertionError):
            If(a, s1, [(a, 1)], None)
        with self.assertRaises(DoItAssertionError):
            If(a, s1, [(a, Statement())], None)
        If(a, s1, [(a, s1)], None)
        with self.assertRaises(DoItAssertionError):
            If(a, s1, [(a, s1)], 1)
        with self.assertRaises(DoItAssertionError):
            If(a, s1, [(a, s1)], Statement())
        If(a, s1, [(a, s1)], s1)
    #-def

    def test_if_statement_visit_and_traverse(self):
        c1 = Id("x")
        c2 = Id("b")
        s1 = Assign(Id("y"), Id("z"))
        s2 = Assign(Id("f"), Id("g"))
        s3 = Assign(Id("i"), Id("j"))

        def v(node, *args):
            if isinstance(node, Id):
                return "%s%s" % (args[1], args[0])
            elif isinstance(node, Assign):
                return "%s = %s" % (args[0], args[1])
            elif isinstance(node, If):
                r = "if (%s)" % args[0]
                r = "%s then %s" % (r, args[1])
                for e, s in args[2]:
                    r = "%s elif (%s) then %s" % (r, e, s)
                if args[3] is not None:
                    r = "%s else %s" % (r, args[3])
                return r
            return "<bad node>"
        def t(node, *args):
            if isinstance(node, Id):
                return "%s%s" % (args[1], args[0])
            elif isinstance(node, Assign):
                l = args[0].traverse(t, args[2])
                r = args[1].traverse(t, args[2])
                return "%s = %s" % (l, r)
            elif isinstance(node, If):
                r = "if (%s)" % args[0].traverse(t, args[4])
                r = "%s then %s" % (r, args[1].traverse(t, args[4]))
                for cc_, tt_ in args[2]:
                    r = "%s elif (%s) then %s" % (
                        r, cc_.traverse(t, args[4]), tt_.traverse(t, args[4])
                    )
                if args[3] is not None:
                    r = "%s else %s" % (r, args[3].traverse(t, args[4]))
                return r
            return "<bad node>"
        self.assertEqual(
            If(c1, s1, [], None).visit(v, "_"), "if (_x) then _y = _z"
        )
        self.assertEqual(
            If(c1, s1, [], None).traverse(t, "."), "if (.x) then .y = .z"
        )
        self.assertEqual(
            If(c1, s1, [], s3).visit(v, "_"),
            "if (_x) then _y = _z else _i = _j"
        )
        self.assertEqual(
            If(c1, s1, [], s3).traverse(t, "'"),
            "if ('x) then 'y = 'z else 'i = 'j"
        )
        self.assertEqual(
            If(c1, s1, [(c2, s2)], None).visit(v, "_"),
            "if (_x) then _y = _z elif (_b) then _f = _g"
        )
        self.assertEqual(
            If(c1, s1, [(c2, s2)], None).traverse(t, "'"),
            "if ('x) then 'y = 'z elif ('b) then 'f = 'g"
        )
        self.assertEqual(
            If(c1, s1, [(c2, s2)], s3).visit(v, "_"),
            "if (_x) then _y = _z elif (_b) then _f = _g else _i = _j"
        )
        self.assertEqual(
            If(c1, s1, [(c2, s2)], s3).traverse(t, "/"),
            "if (/x) then /y = /z elif (/b) then /f = /g else /i = /j"
        )
    #-def

    def test_case_statement_initialization(self):
        e, a, b = Expr(), AtomicExpr(0), Block([])

        with self.assertRaises(DoItAssertionError):
            Case(1, [], b)
        with self.assertRaises(DoItAssertionError):
            Case(e, [], b)
        with self.assertRaises(DoItAssertionError):
            Case(a, 1, b)
        Case(a, (), [b])
        Case(a, [], [b])
        with self.assertRaises(DoItAssertionError):
            Case(a, (1,), b)
        with self.assertRaises(DoItAssertionError):
            Case(a, [()], b)
        with self.assertRaises(DoItAssertionError):
            Case(a, [[]], b)
        with self.assertRaises(DoItAssertionError):
            Case(a, [(1, b)], b)
        with self.assertRaises(DoItAssertionError):
            Case(a, [(e, b)], b)
        with self.assertRaises(DoItAssertionError):
            Case(a, [(a, 1)], b)
        with self.assertRaises(DoItAssertionError):
            Case(a, [(a, Statement())], b)
        with self.assertRaises(DoItAssertionError):
            Case(a, [(a, b)], 1)
        with self.assertRaises(DoItAssertionError):
            Case(a, [(a, b)], Statement())
        Case(a, [(a, [b])], [b])
    #-def

    def test_case_statement_visit_and_traverse(self):
        w = Id("w")
        n1, n2 = IntLiteral(1), IntLiteral(2)
        s1, s2 = Assign(Id("a"), Id("b")), Assign(Id("c"), Id("d"))
        d = Assign(Id("a"), IntLiteral(3))

        def v(node, *args):
            if isinstance(node, Id):
                return "%s%s" % (args[0], args[1])
            elif isinstance(node, IntLiteral):
                return "%d" % args[0]
            elif isinstance(node, Assign):
                return "%s = %s" % (args[0], args[1])
            elif isinstance(node, Case):
                r = "case (%s) of" % args[0]
                for n, s in args[1]:
                    r = "%s %s:" % (r, n)
                    for x in s:
                        r = "%s %s;" % (r, x)
                if args[2] is not None:
                    r = "%s default:" % r
                    for x in args[2]:
                        r = "%s %s;" % (r, x)
                return "%s esac" % r
            return "<bad node>"
        def t(node, *args):
            if isinstance(node, Id):
                return "%s%s" % (args[1], args[0])
            elif isinstance(node, IntLiteral):
                return "%d" % args[0]
            elif isinstance(node, Assign):
                l = args[0].traverse(t, args[2])
                r = args[1].traverse(t, args[2])
                return "%s = %s" % (l, r)
            elif isinstance(node, Case):
                r = "case (%s) of" % args[0].traverse(t, args[3])
                for n, s in args[1]:
                    r = "%s %s:" % (r, n.traverse(t, args[3]))
                    for x in s:
                        r = "%s %s;" % (r, x.traverse(t, args[3]))
                if args[2] is not None:
                    r = "%s default:" % r
                    for x in args[2]:
                        r = "%s %s;" % (r, x.traverse(t, args[3]))
                return "%s esac" % r
            return "<bad node>"
        self.assertEqual(
            Case(w, [], [d]).visit(v, "'"),
            "case (w') of default: a' = 3; esac"
        )
        self.assertEqual(
            Case(w, [], [d]).traverse(t, "*"),
            "case (*w) of default: *a = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, [s1])], [d]).visit(v, "'"),
            "case (w') of 1: a' = b'; default: a' = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, [s1])], [d]).traverse(t, "*"),
            "case (*w) of 1: *a = *b; default: *a = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, [s1]), (n2, [s2])], [d]).visit(v, "'"),
            "case (w') of 1: a' = b'; 2: c' = d'; default: a' = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, [s1]), (n2, [s2])], [d]).traverse(t, "*"),
            "case (*w) of 1: *a = *b; 2: *c = *d; default: *a = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, [s1]), (n2, [s2])], None).visit(v, "'"),
            "case (w') of 1: a' = b'; 2: c' = d'; esac"
        )
        self.assertEqual(
            Case(w, [(n1, [s1]), (n2, [s2])], None).traverse(t, "*"),
            "case (*w) of 1: *a = *b; 2: *c = *d; esac"
        )
        self.assertEqual(
            Case(w, [(n1, [s1, s2])], [d]).visit(v, "'"),
            "case (w') of 1: a' = b'; c' = d'; default: a' = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, [s1, s2])], [d]).traverse(t, "*"),
            "case (*w) of 1: *a = *b; *c = *d; default: *a = 3; esac"
        )
    #-def

    def test_for_statement_initialization(self):
        with self.assertRaises(DoItAssertionError):
            For(1, AtomicExpr(0), Block([]))
        with self.assertRaises(DoItAssertionError):
            For(Id("z"), 1, Block([]))
        with self.assertRaises(DoItAssertionError):
            For(Id("z"), Expr(), Block([]))
        with self.assertRaises(DoItAssertionError):
            For(Id("z"), AtomicExpr(0), 1)
        with self.assertRaises(DoItAssertionError):
            For(Id("z"), AtomicExpr(0), Statement())
        For(Id("z"), AtomicExpr(0), Block([]))
    #-def

    def test_while_statement_initialization(self):
        with self.assertRaises(DoItAssertionError):
            While(1, Block([]))
        with self.assertRaises(DoItAssertionError):
            While(Expr(), Block([]))
        with self.assertRaises(DoItAssertionError):
            While(AtomicExpr(0), 1)
        with self.assertRaises(DoItAssertionError):
            While(AtomicExpr(0), Statement())
        While(AtomicExpr(0), Block([]))
    #-def

    def test_dowhile_statement_initialization(self):
        with self.assertRaises(DoItAssertionError):
            DoWhile(1, AtomicExpr(0))
        with self.assertRaises(DoItAssertionError):
            DoWhile(Statement(), AtomicExpr(0))
        with self.assertRaises(DoItAssertionError):
            DoWhile(Block([]), 1)
        with self.assertRaises(DoItAssertionError):
            DoWhile(Block([]), Expr())
        DoWhile(Block([]), AtomicExpr(0))
    #-def

    def test_continue_and_break_statements_initialization(self):
        Continue()
        Break()
    #-def

    def test_return_statement_initialization(self):
        Return()
        with self.assertRaises(DoItAssertionError):
            ReturnWithValue(1)
        with self.assertRaises(DoItAssertionError):
            ReturnWithValue(Expr())
        ReturnWithValue(AtomicExpr(0))
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestActionNodeCase))
    suite.addTest(unittest.makeSuite(TestExprCase))
    suite.addTest(unittest.makeSuite(TestCallExprCase))
    suite.addTest(unittest.makeSuite(TestIndexExprCase))
    suite.addTest(unittest.makeSuite(TestAccessExprCase))
    suite.addTest(unittest.makeSuite(TestIdAndLiteralsCase))
    suite.addTest(unittest.makeSuite(TestStatementsCase))
    return suite
#-def
