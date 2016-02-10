#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/models/cfgram.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-12-21 20:50:49 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Context-free grammar.\
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

class RuleNode(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def

    def __add__(self, rhs):
        """
        """

        return Catenation(self, rhs)
    #-def

    def __sub__(self, rhs):
        """
        """

        return Range(self, rhs)
    #-def

    def __mod__(self, rhs):
        """
        """

        return Label(self, rhs)
    #-def

    def __or__(self, rhs):
        """
        """

        return Alternation(self, rhs)
    #-def

    def __neg__(self):
        """
        """

        return DoNotRecord(self)
    #-def

    def __invert__(self):
        """
        """

        return Complement(self)
    #-def

    def __getitem__(self, i):
        """
        """

        _assert(i in [ '*', '+', '?' ], "Quantifier expected")
        return {
          '*': Iteration,
          '+': PositiveIteration,
          '?': Optional
        }[i](self)
    #-def
#-class

class TerminalNode(RuleNode, VisitableLeaf):
    """
    """
    __slots__ = []

    def __init__(self, value):
        """
        """

        RuleNode.__init__(self)
        VisitableLeaf.__init__(self, value)
    #-def
#-class

class UnaryNode(RuleNode, UnaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, node):
        """
        """

        RuleNode.__init__(self)
        UnaryVisitableNode.__init__(self, node)
    #-def
#-class

class BinaryNode(RuleNode, BinaryVisitableNode):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        RuleNode.__init__(self)
        BinaryVisitableNode.__init__(self, lhs, rhs)
    #-def
#-class

class Epsilon(TerminalNode):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TerminalNode.__init__(self, "")
    #-def
#-class

class Sym(TerminalNode):
    """
    """
    __slots__ = []

    def __init__(self, v):
        """
        """

        _assert(isinstance(v, str) and len(v) == 1, "Character expected")
        TerminalNode.__init__(self, ord(v))
    #-def

    def __int__(self):
        """
        """

        return self.visit(lambda n, v: v)
    #-def
#-class

class Var(TerminalNode):
    """
    """
    __slots__ = []

    def __init__(self, name):
        """
        """

        TerminalNode.__init__(self, name)
    #-def
#-class

class Range(TerminalNode):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        _assert(isinstance(a, Sym) and isinstance(b, Sym), "Symbol expected")
        _assert(int(a) > int(b), "'a' must be greater than 'b'")
        TerminalNode.__init__(self, (int(a), int(b)))
    #-def
#-class

class Action(TerminalNode):
    """
    """
    __slots__ = []

    def __init__(self, action):
        """
        """

        _assert(isinstance(action, ActionNode), "Action expected")
        TerminalNode.__init__(self, action)
    #-def
#-class

class Alias(UnaryNode):
    """
    """
    __slots__ = []

    def __init__(self, node):
        """
        """

        UnaryNode.__init__(self, node)
    #-def
#-class

class DoNotRecord(UnaryNode):
    """
    """
    __slots__ = []

    def __init__(self, node):
        """
        """

        UnaryNode.__init__(self, node)
    #-def
#-class

class Complement(UnaryNode):
    """
    """
    __slots__ = []

    def __init__(self, node):
        """
        """

        UnaryNode.__init__(self, node)
    #-def
#-class

class Iteration(UnaryNode):
    """
    """
    __slots__ = []

    def __init__(self, node):
        """
        """

        UnaryNode.__init__(self, node)
    #-def
#-class

class PositiveIteration(UnaryNode):
    """
    """
    __slots__ = []

    def __init__(self, node):
        """
        """

        UnaryNode.__init__(self, node)
    #-def
#-class

class Optional(UnaryNode):
    """
    """
    __slots__ = []

    def __init__(self, node):
        """
        """

        UnaryNode.__init__(self, node)
    #-def
#-class

class Label(BinaryNode):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryNode.__init__(self, lhs, Var(rhs))
    #-def
#-class

class Catenation(BinaryNode):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryNode.__init__(self, lhs, rhs)
    #-def
#-class

class Alternation(BinaryNode):
    """
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """
        """

        BinaryNode.__init__(self, lhs, rhs)
    #-def
#-class

class Grammar(object):
    """
    """
    __slots__ = [ '__start', '__rules', 'cache' ]

    def __init__(self, start = "start"):
        """
        """

        self.__start = start
        self.__rules = collections.OrderedDict()
        self.cache = {}
    #-def

    def __setitem__(self, key, value):
        """
        """

        if key in self.__rules:
            value = self[key] | value
        self.__rules[key] = value
    #-def

    def get_start(self):
        """
        """

        return self.__start
    #-def

    def get_rules(self):
        """
        """

        return self.__rules
    #-def
#-class