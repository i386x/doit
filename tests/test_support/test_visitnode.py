#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_visitnode.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-01-24 11:47:09 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Visitable node module tests.\
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

from doit.support.errors import DoItAssertionError, DoItNotImplementedError, \
                                doit_assert
from doit.support.visitnode import VisitableNode, \
                                   VisitableLeaf, \
                                   NullaryVisitableNode, \
                                   UnaryVisitableNode, \
                                   BinaryVisitableNode, \
                                   TernaryVisitableNode

def visitor(node, *args):
    if isinstance(node, Atom):
        v, s = args
        return "%s(%d)" % (s, v)
    elif isinstance(node, Break):
        return "%s()" % args
    elif isinstance(node, Neg):
        return "-(%s)" % args[0]
    elif isinstance(node, Add):
        v1, v2, _ = args
        return "(%s + %s)" % (v1, v2)
    elif isinstance(node, If):
        v1, v2, v3, _ = args
        return "if (%s) then %s else %s" % (v1, v2, v3)
    else:
        doit_assert(False, "Unexpected node")
    return None
#-def

def traverser(node, *args):
    if isinstance(node, Atom):
        v, s = args
        return "%s[%d]" % (s, v)
    elif isinstance(node, Break):
        return "%s[]" % args
    elif isinstance(node, Neg):
        n = args[0]
        r = n.traverse(traverser, *(args[1:]))
        return "-[%s]" % r
    elif isinstance(node, Add):
        n1, n2 = args[0], args[1]
        r1 = n1.traverse(traverser, *(args[2:]))
        r2 = n2.traverse(traverser, *(args[2:]))
        return "[%s + %s]" % (r1, r2)
    elif isinstance(node, If):
        n1, n2, n3 = args[0], args[1], args[2]
        r1 = n1.traverse(traverser, *(args[3:]))
        r2 = n2.traverse(traverser, *(args[3:]))
        r3 = n3.traverse(traverser, *(args[3:]))
        return "if [%s] then %s else %s" % (r1, r2, r3)
    else:
        doit_assert(False, "Unexpected node")
    return None
#-def

class Atom(VisitableLeaf):
    __slots__ = []

    def __init__(self, v):
        VisitableLeaf.__init__(self, v)
    #-def
#-class

class Break(NullaryVisitableNode):
    __slots__ = []

    def __init__(self):
        NullaryVisitableNode.__init__(self)
    #-def
#-class

class Neg(UnaryVisitableNode):
    __slots__ = []

    def __init__(self, n):
        UnaryVisitableNode.__init__(self, n)
    #-def
#-class

class Add(BinaryVisitableNode):
    __slots__ = []

    def __init__(self, n1, n2):
        BinaryVisitableNode.__init__(self, n1, n2)
    #-def
#-class

class If(TernaryVisitableNode):
    __slots__ = []

    def __init__(self, n1, n2, n3):
        TernaryVisitableNode.__init__(self, n1, n2, n3)
    #-def
#-class

class TestVisitableNodeCase(unittest.TestCase):

    def test_visit_is_not_implemented(self):
        n = VisitableNode()

        with self.assertRaises(DoItNotImplementedError):
            n.visit((lambda x: None), 1, 2, 3)
    #-def

    def test_traverse_is_not_implemented(self):
        n = VisitableNode()

        with self.assertRaises(DoItNotImplementedError):
            n.traverse((lambda x: None), 1, 2, 3)
    #-def
#-class

class TestVisitableLeafCase(unittest.TestCase):

    def test_visit_and_traverse(self):
        n = Atom(42)

        self.assertEqual(n.visit(visitor, "x"), "x(42)")
        self.assertEqual(n.traverse(traverser, "y"), "y[42]")
    #-def
#-class

class TestNullaryVisitableNodeCase(unittest.TestCase):

    def test_visit_and_traverse(self):
        n = Break()

        self.assertEqual(n.visit(visitor, "x"), "x()")
        self.assertEqual(n.traverse(traverser, "y"), "y[]")
    #-def
#-class

class TestUnaryVisitableNodeCase(unittest.TestCase):

    def test_bad_node(self):
        with self.assertRaises(DoItAssertionError):
            Neg(0)
    #-def

    def test_visit_and_traverse(self):
        n1 = Neg(Atom(42))
        n2 = Neg(Break())
        n3 = Neg(Neg(Atom(84)))

        self.assertEqual(n1.visit(visitor, "x"), "-(x(42))")
        self.assertEqual(n1.traverse(traverser, "y"), "-[y[42]]")
    #-def
#-class

class TestBinaryVisitableNodeCase(unittest.TestCase):

    def test_bad_node(self):
        with self.assertRaises(DoItAssertionError):
            Add(1, Atom(2))
        with self.assertRaises(DoItAssertionError):
            Add(Atom(1), 2)
    #-def

    def test_visit_and_traverse(self):
        n1 = Add(Atom(1), Atom(2))
        n2 = Add(Add(Neg(Atom(3)), Break()), Add(Atom(4), Neg(Break())))

        self.assertEqual(n1.visit(visitor, "x"), "(x(1) + x(2))")
        self.assertEqual(n2.visit(visitor, "x"),
            "((-(x(3)) + x()) + (x(4) + -(x())))"
        )
        self.assertEqual(n1.traverse(traverser, "y"), "[y[1] + y[2]]")
        self.assertEqual(n2.traverse(traverser, "y"),
            "[[-[y[3]] + y[]] + [y[4] + -[y[]]]]"
        )
    #-def
#-class

class TestTernaryVisitableNodeCase(unittest.TestCase):

    def test_bad_node(self):
        with self.assertRaises(DoItAssertionError):
            If(1, Atom(2), Atom(3))
        with self.assertRaises(DoItAssertionError):
            If(Atom(1), 2, Atom(3))
        with self.assertRaises(DoItAssertionError):
            If(Atom(1), Atom(2), 3)
    #-def

    def test_visit_and_traverse(self):
        n = If(Add(Atom(1), Atom(2)), Break(), Neg(Add(Atom(3), Break())))

        self.assertEqual(n.visit(visitor, "x"),
            "if ((x(1) + x(2))) then x() else -((x(3) + x()))"
        )
        self.assertEqual(n.traverse(traverser, "y"),
            "if [[y[1] + y[2]]] then y[] else -[[y[3] + y[]]]"
        )
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestVisitableNodeCase))
    suite.addTest(unittest.makeSuite(TestVisitableLeafCase))
    suite.addTest(unittest.makeSuite(TestNullaryVisitableNodeCase))
    suite.addTest(unittest.makeSuite(TestUnaryVisitableNodeCase))
    suite.addTest(unittest.makeSuite(TestBinaryVisitableNodeCase))
    suite.addTest(unittest.makeSuite(TestTernaryVisitableNodeCase))
    return suite
#-def
