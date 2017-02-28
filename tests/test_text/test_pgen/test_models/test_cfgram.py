#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/test_models/test_cfgram.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-12-22 12:04:34 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Context-free grammar tests.\
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

from doit.support.cmd.eval import CommandProcessor
from doit.support.cmd.commands import \
    Const, GetLocal, Concat, InstanceOf, GetItem, ToStr, Lambda, If, Return, \
    Visit

from doit.text.pgen.models.action import Block
from doit.text.pgen.models.cfgram import \
    RuleNode, \
    TerminalNode, UnaryNode, BinaryNode, \
    Epsilon, Sym, Var, Range, Action, \
    Alias, DoNotRecord, Complement, Iteration, PositiveIteration, Optional, \
    Label, Catenation, Alternation, \
    Grammar

class TestRuleNodeCase(unittest.TestCase):

    def test_rule_node_initialization(self):
        RuleNode()
    #-def

    def test_rule_node_operators(self):
        e1, e2 = Epsilon(), Epsilon()
        sa, sb = Sym('a'), Sym('b')

        self.assertIsInstance(e1 + e2, Catenation)
        self.assertIsInstance(sa - sb, Range)
        self.assertIsInstance(sa % "x", Label)
        self.assertIsInstance(e1 | sa, Alternation)
        self.assertIsInstance(-sa, DoNotRecord)
        self.assertIsInstance(~e1, Complement)
        with self.assertRaises(DoItAssertionError):
            sa[1]
        self.assertIsInstance(e1['*'], Iteration)
        self.assertIsInstance(e1['+'], PositiveIteration)
        self.assertIsInstance(e1['?'], Optional)
    #-def
#-class

class TestTerminalNodeCase(unittest.TestCase):

    def test_terminal_node_initialization(self):
        TerminalNode('a')
    #-def

    def test_terminal_node_visitor(self):
        p = CommandProcessor()
        n = TerminalNode('a')
        f = Lambda(['n', 'args'], True, [
            If(InstanceOf(GetLocal('n'), Const(TerminalNode)), [
                Return(Concat(
                    GetItem(GetLocal('args'), 1),
                    GetItem(GetLocal('args'), 0)
                ))
            ], [
                Return("<bad node>")
            ])
        ], [])

        p.run([Visit(n, f, "^")])
        self.assertEqual(p.acc(), "^a")
    #-def
#-class

class TestUnaryNodeCase(unittest.TestCase):

    def test_unary_node_initialization(self):
        UnaryNode(TerminalNode('x'))
    #-def

    def test_unary_node_visitor(self):
        p = CommandProcessor()
        n = UnaryNode(TerminalNode('b'))
        f = Lambda(['n', 'args'], True, [
            If(InstanceOf(GetLocal('n'), Const(TerminalNode)), [
                Return(Concat(
                    GetItem(GetLocal('args'), 1),
                    GetItem(GetLocal('args'), 0)
                ))
            ], [If(InstanceOf(GetLocal('n'), Const(UnaryNode)), [
                Return(Concat(
                    GetItem(GetLocal('args'), 0),
                    "()"
                ))
            ], [
                Return("<bad node>")
            ])])
        ], [])

        p.run([Visit(n, f, "**")])
        self.assertEqual(p.acc(), "**b()")
    #-def
#-class

class TestBinaryNodeCase(unittest.TestCase):

    def test_binary_node_initialization(self):
        BinaryNode(TerminalNode('a'), TerminalNode('b'))
    #-def

    def test_binary_node_visitor(self):
        p = CommandProcessor()
        n = BinaryNode(TerminalNode('a'), TerminalNode('b'))
        f = Lambda(['n', 'args'], True, [
            If(InstanceOf(GetLocal('n'), Const(TerminalNode)), [
                Return(Concat(
                    GetItem(GetLocal('args'), 1),
                    GetItem(GetLocal('args'), 0)
                ))
            ], [If(InstanceOf(GetLocal('n'), Const(BinaryNode)), [
                Return(
                    Concat(
                        GetItem(GetLocal('args'), 0),
                    Concat(
                        " <+> ",
                        GetItem(GetLocal('args'), 1)
                    ))
                )
            ], [
                Return("<bad node>")
            ])])
        ], [])

        p.run([Visit(n, f, "#")])
        self.assertEqual(p.acc(), "#a <+> #b")
    #-def
#-class

class TestNodesCase(unittest.TestCase):

    def test_nodes(self):
        Epsilon()
        with self.assertRaises(DoItAssertionError):
            Sym(1)
        with self.assertRaises(DoItAssertionError):
            Sym("ab")
        with self.assertRaises(DoItAssertionError):
            Sym("")
        self.assertEqual(int(Sym('@')), ord('@'))
        Var('x')
        with self.assertRaises(DoItAssertionError):
            Range(1, 1)
        with self.assertRaises(DoItAssertionError):
            Range(Sym('a'), 1)
        with self.assertRaises(DoItAssertionError):
            Range(1, Sym('z'))
        with self.assertRaises(DoItAssertionError):
            Range(Sym('9'), Sym('0'))
        with self.assertRaises(DoItAssertionError):
            Range(Sym('+'), Sym('+'))
        Range(Sym('a'), Sym('z'))
        with self.assertRaises(DoItAssertionError):
            Action(1)
        Action(Block([]))
        Alias(Sym('a'))
        DoNotRecord(Sym('a'))
        Complement(Sym('a'))
        Iteration(Sym('a'))
        PositiveIteration(Sym('a'))
        Optional(Sym('a'))
        Label(Sym('a'), 1)
        Catenation(Sym('a'), Sym('b'))
        Alternation(Sym('a'), Sym('b'))
    #-def
#-class

class TestGrammarCase(unittest.TestCase):

    def test_grammar_initialization(self):
        g = Grammar()
        h = Grammar("init")

        self.assertEqual(g.start(), "start")
        self.assertEqual(g.rules(), {})
        self.assertEqual(g.cache, {})
        self.assertEqual(g.properties, {})
        self.assertEqual(h.start(), "init")
    #-def

    def test_grammar_set_start(self):
        g = Grammar()

        self.assertEqual(g.start(), "start")
        g.set_start("init")
        self.assertEqual(g.start(), "init")
    #-def

    def test_grammar_adding_rules(self):
        p = CommandProcessor()
        g = Grammar()
        g["start"] = Var('A') + Var('B')
        g['A'] = Sym('a')
        g['B'] = Sym('b')
        g['A'] = Sym('c')
        g["start"] = Var('A')
        g["start"] = Var('B') + Sym('c') | Sym('d')
        fmt = {'itype': 'X', 'size': 2, 'flags': "0"}
        f = Lambda(['n', 'args'], True, [
            If(InstanceOf(GetLocal('n'), Const(Var)), [
                Return(GetItem(GetLocal('args'), 0))
            ], [If(InstanceOf(GetLocal('n'), Const(Sym)), [
                Return(Concat(
                    "#", ToStr(GetItem(GetLocal('args'), 0), fmt)
                ))
            ], [If(InstanceOf(GetLocal('n'), Const(Catenation)), [
                Return(
                    Concat(
                        "(",
                    Concat(
                        GetItem(GetLocal('args'), 0),
                    Concat(
                        GetItem(GetLocal('args'), 1),
                        ")"
                    )))
                )
            ], [If(InstanceOf(GetLocal('n'), Const(Alternation)), [
                Return(
                    Concat(
                        "(",
                    Concat(
                        GetItem(GetLocal('args'), 0),
                    Concat(
                        " | ",
                    Concat(
                        GetItem(GetLocal('args'), 1),
                        ")"
                    ))))
                )
            ], [
                Return("<bad node>")
            ])])])])
        ], [])

        p.run([Visit(g.rules()["start"], f)])
        self.assertEqual(p.acc(), "(((AB) | A) | ((B#63) | #64))")
        p.run([Visit(g.rules()["A"], f)])
        self.assertEqual(p.acc(), "(#61 | #63)")
        p.run([Visit(g.rules()["B"], f)])
        self.assertEqual(p.acc(), "#62")
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRuleNodeCase))
    suite.addTest(unittest.makeSuite(TestTerminalNodeCase))
    suite.addTest(unittest.makeSuite(TestUnaryNodeCase))
    suite.addTest(unittest.makeSuite(TestBinaryNodeCase))
    suite.addTest(unittest.makeSuite(TestNodesCase))
    suite.addTest(unittest.makeSuite(TestGrammarCase))
    return suite
#-def
