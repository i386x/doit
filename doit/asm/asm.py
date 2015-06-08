#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/asm/asm.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-04-08 15:36:25 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! abstract assembler.\
"""

__license__ = """\
Copyright (c) 2014 - 2015 Jiří Kučera.

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

class InstructionOperand(object):
    """Base class for all instruction operands.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the instruction operand object.
        """

        pass
    #-def

    def traverse(self, f):
        """Visits the nodes of this tree in postorder applying `f` on each
        visited node (including the node representing this tree).

        :param f: Functor which, when applied, takes \
            :class:`InstructionOperand <doit.asm.asm.InstructionOperand>` \
            instance as its argument.
        :type f: callable object

        :raises NotImplementedError: If this method is not implemented.
        """

        raise NotImplementedError(
            "%s.traverse(f) is not implemented." % self.__class__.__name__
        )
    #-def

    def __add__(self, rhs):
        """Handle the ``self + rhs`` expression.

        :param rhs: Right-hand side.
        :type rhs: any type

        :returns: The node/tree for ``self + rhs`` expression \
            (:class:`AddNode <doit.asm.asm.AddNode>`).
        """

        return AddNode(self, rhs)
    #-def

    def __sub__(self, rhs):
        """Handle the ``self - rhs`` expression.

        :param rhs: Right-hand side.
        :type rhs: any type

        :returns: The node/tree for ``self - rhs`` expression \
            (:class:`SubNode <doit.asm.asm.SubNode>`).
        """

        return SubNode(self, rhs)
    #-def

    def __mul__(self, rhs):
        """Handle the ``self * rhs`` expression.

        :param rhs: Right-hand side.
        :type rhs: any type

        :returns: The node/tree for ``self * rhs`` expression \
            (:class:`MultNode <doit.asm.asm.MultNode>`).
        """

        return MultNode(self, rhs)
    #-def

    def __rmul__(self, lhs):
        """Handle the ``lhs * self`` expression.

        :param lhs: Left-hand side.
        :type lhs: any type

        :returns: The node/tree for ``lhs * self`` expression \
            (:class:`MultNode <doit.asm.asm.MultNode>`).
        """

        return MultNode(lhs, self):
    #-def

    def __getitem__(self, idx):
        """Handle the ``self[idx]`` expression.

        :param idx: Index expression.
        :type idx: any type

        :returns: The node/tree for ``self[idx]`` expression \
            (:class:`IndexNode <doit.asm.asm.IndexNode>`).
        """

        return IndexNode(self, idx)
    #-def
#-class

class Register(InstructionOperand):
    """Base class for all registers.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register object.
        """

        InstructionOperand.__init__(self)
    #-def
#-class

class BinOpNode(InstructionOperand):
    """Base class for binary operator node.
    """
    __slots__ = [ '__lhs', '__rhs' ]

    def __init__(self, lhs, rhs):
        """Initializes the binary operator node.

        :param lhs: Left-hand side.
        :type lhs: any type
        :param rhs: Right-hand side.
        :type rhs: any type
        """

        InstructionOperand.__init__(self)
        self.__lhs = lhs
        self.__rhs = rhs
    #-def

    def traverse(self, f):
        """See :meth:`InstructionOperand.traverse(f) \
        <doit.asm.asm.InstructionOperand.traverse>`.
        """

        if isinstance(self.__lhs, InstructionOperand):
            self.__lhs.traverse(f)
        else:
            f(self.__lhs)
        if isinstance(self.__rhs, InstructionOperand):
            self.__rhs.traverse(f)
        else:
            f(self.__rhs)
        f(self)
    #-def
#-class

class AddNode(BinOpNode):
    """Base class for addition node.
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """Initializes the addition node object.
        """

        BinOpNode.__init__(self, lhs, rhs)
    #-def
#-class

class SubNode(BinOpNode):
    """Base class for subtraction node.
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """Initializes the subtraction node object.
        """

        BinOpNode.__init__(self, lhs, rhs)
    #-def
#-class

class MultNode(BinOpNode):
    """Base class for multiplication node.
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """Initializes the multiplication node object.
        """

        BinOpNode.__init__(self, lhs, rhs)
    #-def
#-class

class IndexNode(BinOpNode):
    """Base class for index node.
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """Initializes the index node object.
        """

        BinOpNode.__init__(self, lhs, rhs)
    #-def
#-class

class AbstractAssembler(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        self.__labels = []
        self.__links = {}
    #-def

    def comment(self, s):
        """
        """

        return self
    #-def

    def label(self, l):
        """
        """

        assert l not in self.__labels, "Label %s is still used." % repr(l)
        self.__labels.append(l)
        self.__links[l] = len(self.buffer)
        return self
    #-def

    def end_section(self, name):
        """
        """

    #-def
#-class

def section(obj, name):
    """
    """

    obj.start_section(name)
    return obj
#-def
