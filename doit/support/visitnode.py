#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/visitnode.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-01-08 17:50:32 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Visitable nodes.\
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

from doit.support.errors import doit_assert, not_implemented

_assert = doit_assert

class VisitableNode(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def

    def visit(self, f, *args):
        """
        """

        not_implemented()
    #-def

    def traverse(self, f, *args):
        """
        """

        not_implemented()
    #-def
#-class

class VisitableLeaf(VisitableNode):
    """
    """
    __slots__ = [ '__value' ]

    def __init__(self, value):
        """
        """

        VisitableNode.__init__(self)
        self.__value = value
    #-def

    def visit(self, f, *args):
        """
        """

        return f(self, self.__value, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(self, self.__value, *args)
    #-def
#-class

class NullaryVisitableNode(VisitableNode):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        VisitableNode.__init__(self)
    #-def

    def visit(self, f, *args):
        """
        """

        return f(self, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(self, *args)
    #-def
#-class

class UnaryVisitableNode(VisitableNode):
    """
    """
    __slots__ = [ '__node' ]

    def __init__(self, node):
        """
        """

        _assert(isinstance(node, VisitableNode), "Visitable node expected")
        VisitableNode.__init__(self)
        self.__node = node
    #-def

    def visit(self, f, *args):
        """
        """

        r = self.__node.visit(f, *args)
        return f(self, r, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(self, self.__node, *args)
    #-def
#-class

class BinaryVisitableNode(VisitableNode):
    """
    """
    __slots__ = [ '__node1', '__node2' ]

    def __init__(self, node1, node2):
        """
        """

        _assert(isinstance(node1, VisitableNode), "Visitable node expected")
        _assert(isinstance(node2, VisitableNode), "Visitable node expected")
        VisitableNode.__init__(self)
        self.__node1 = node1
        self.__node2 = node2
    #-def

    def visit(self, f, *args):
        """
        """

        r1 = self.__node1.visit(f, *args)
        r2 = self.__node2.visit(f, *args)
        return f(self, r1, r2, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(self, self.__node1, self.__node2, *args)
    #-def
#-class

class TernaryVisitableNode(VisitableNode):
    """
    """
    __slots__ = [ '__node1', '__node2', '__node3' ]

    def __init__(self, node1, node2, node3):
        """
        """

        _assert(isinstance(node1, VisitableNode), "Visitable node expected")
        _assert(isinstance(node2, VisitableNode), "Visitable node expected")
        _assert(isinstance(node3, VisitableNode), "Visitable node expected")
        VisitableNode.__init__(self)
        self.__node1 = node1
        self.__node2 = node2
        self.__node3 = node3
    #-def

    def visit(self, f, *args):
        """
        """

        r1 = self.__node1.visit(f, *args)
        r2 = self.__node2.visit(f, *args)
        r3 = self.__node3.visit(f, *args)
        return f(self, r1, r2, r3, *args)
    #-def

    def traverse(self, f, *args):
        """
        """

        return f(self, self.__node1, self.__node2, self.__node3, *args)
    #-def
#-class
