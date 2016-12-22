#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/test_models/test_action.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-12-20 14:26:50 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Action nodes tests.\
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

import unittest

from doit.support.errors import DoItAssertionError

from doit.text.pgen.models.action import \
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
        Return

class TestActionNodeCase(unittest.TestCase):

    def test_action_node_initialization(self):
        ActionNode()
    #-def
#-class

class TestExprCase(unittest.TestCase):

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
        self.assertIsInstance(e1 == e2, EqExpr)
        self.assertIsInstance(e1 != e2, NotEqExpr)
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
        Case(a, (), b)
        Case(a, [], b)
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
        Case(a, [(a, b)], b)
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
                    r = "%s %s: %s;" % (r, n, s)
                return "%s default: %s; esac" % (r, args[2])
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
                    r = "%s %s: %s;" % (
                        r, n.traverse(t, args[3]), s.traverse(t, args[3])
                    )
                return "%s default: %s; esac" % (
                    r, args[2].traverse(t, args[3])
                )
            return "<bad node>"
        self.assertEqual(
            Case(w, [], d).visit(v, "'"),
            "case (w') of default: a' = 3; esac"
        )
        self.assertEqual(
            Case(w, [], d).traverse(t, "*"),
            "case (*w) of default: *a = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, s1)], d).visit(v, "'"),
            "case (w') of 1: a' = b'; default: a' = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, s1)], d).traverse(t, "*"),
            "case (*w) of 1: *a = *b; default: *a = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, s1), (n2, s2)], d).visit(v, "'"),
            "case (w') of 1: a' = b'; 2: c' = d'; default: a' = 3; esac"
        )
        self.assertEqual(
            Case(w, [(n1, s1), (n2, s2)], d).traverse(t, "*"),
            "case (*w) of 1: *a = *b; 2: *c = *d; default: *a = 3; esac"
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
        with self.assertRaises(DoItAssertionError):
            Return(1)
        with self.assertRaises(DoItAssertionError):
            Return(Expr())
        Return(AtomicExpr(0))
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
