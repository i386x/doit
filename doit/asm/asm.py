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

class AbstractOperand(object):
    """Base class for all instruction operand expressions.

    This class defines operations ``+``, ``-``, ``*``, and ``[]`` to make more
    complex instruction operands from the simple ones according to following
    rules:

    * :class:`BaseRegister <doit.asm.asm.BaseRegister>` (``+`` or ``-``) \
        :class:`int` gives :class:`Offset <doit.asm.asm.Offset>`
    * :class:`Scale <doit.asm.asm.Scale>` (``+`` or ``-``) :class:`int` gives \
        :class:`Offset <doit.asm.asm.Offset>`
    * :class:`BaseRegister <doit.asm.asm.BaseRegister>` ``*`` :class:`int` \
        gives :class:`Scale <doit.asm.asm.Scale>`
    * :class:`int` ``*`` :class:`BaseRegister <doit.asm.asm.BaseRegister>` \
        gives :class:`Scale <doit.asm.asm.Scale>`
    * :class:`SegmentRegister <doit.asm.asm.SegmentRegister>` ``[`` \
        :class:`int` ``]`` gives :class:`Address <doit.asm.asm.Address>`
    * :class:`SegmentRegister <doit.asm.asm.SegmentRegister>` ``[`` \
        :class:`BaseRegister <doit.asm.asm.BaseRegister>` ``]`` gives \
        :class:`Address <doit.asm.asm.Address>`
    * :class:`SegmentRegister <doit.asm.asm.SegmentRegister>` ``[`` \
        :class:`Scale <doit.asm.asm.Scale>` ``]`` gives \
        :class:`Address <doit.asm.asm.Address>`
    * :class:`SegmentRegister <doit.asm.asm.SegmentRegister>` ``[`` \
        :class:`Offset <doit.asm.asm.Offset>` ``]`` gives \
        :class:`Address <doit.asm.asm.Address>`
    """
    __slots__ = []

    def __init__(self):
        """Initializes the instruction operand expression.
        """

        pass
    #-def

    def __add__(self, rhs):
        """Handle the ``base + offset`` instruction operand expression.

        :param int rhs: Right-hand side of expression which specifies the \
            offset value.

        :returns: The offset-expression node (:class:`Offset \
            <doit.asm.asm.Offset>`).

        :raises AssertionError: If left-hand side of expression is not \
            :class:`BaseRegister <doit.asm.asm.BaseRegister>` or \
            :class:`Scale <doit.asm.asm.Scale>`, or if right-hand side is not \
            :class:`int`.
        """

        assert isinstance(self, BaseRegister) or isinstance(self, Scale), \
            "Left-hand side must be a (scaled) base register."
        assert isinstance(rhs, int), "Right-hand side must be int."
        return Offset(self, rhs)
    #-def

    def __sub__(self, rhs):
        """Handle the ``base - offset`` instruction operand expression.

        :param int rhs: Right-hand side of expression which specifies the \
            offset value.

        :returns: The offset-expression node (:class:`Offset \
            <doit.asm.asm.Offset>`).

        :raises AssertionError: If left-hand side of expression is not \
            :class:`BaseRegister <doit.asm.asm.BaseRegister>` or \
            :class:`Scale <doit.asm.asm.Scale>`, or if right-hand side is not \
            :class:`int`.
        """

        assert isinstance(self, BaseRegister) or isinstance(self, Scale), \
            "Left-hand side must be a (scaled) base register."
        assert isinstance(rhs, int), "Right-hand side must be int."
        return Offset(self, -rhs)
    #-def

    def __mul__(self, rhs):
        """Handle the ``base * scale`` instruction operand expression.

        :param int rhs: Right-hand side of expression which specifies the \
            scale. Must be power of two.

        :returns: The scale-expression node (:class:`Scale \
            <doit.asm.asm.Scale>`).

        :raises AssertionError: If left-hand side of expression is not \
            :class:`BaseRegister <doit.asm.asm.BaseRegister>`, or if \
            right-hand side is not a power of two.
        """

        assert isinstance(self, BaseRegister), \
            "Left-hand side must be a base register."
        assert isinstance(rhs, int) and rhs > 0 and (rhs & (rhs - 1)) == 0, \
            "Right-hand side must be the power-of-two int."
        return Scale(self, rhs)
    #-def

    def __rmul__(self, lhs):
        """Handle the ``scale * base`` instruction operand expression.

        :param int lhs: Left-hand side of expression which specifies the \
            scale. Must be power of two.

        :returns: The scale-expression node (:class:`Scale \
            <doit.asm.asm.Scale>`).

        :raises AssertionError: If right-hand side of expression is not \
            :class:`BaseRegister <doit.asm.asm.BaseRegister>`, or if \
            left-hand side is not a power of two.
        """

        assert isinstance(self, BaseRegister), \
            "Right-hand side must be a base register."
        assert isinstance(lhs, int) and lhs > 0 and (lhs & (lhs - 1)) == 0, \
            "Left-hand side must be the power-of-two int."
        return Scale(self, lhs)
    #-def

    def __getitem__(self, expr):
        """Handle the ``segment[int]``, ``segment[base_register]``,
        ``segment[scale]``, or ``segment[offset]`` address-expressions.

        :param expr: Expression between ``[`` and ``]``.
        :type expr: :class:`int` or :class:`BaseRegister \
            <doit.asm.asm.BaseRegister>` or :class:`Scale \
            <doit.asm.asm.Scale>` or :class:`Offset <doit.asm.asm.Offset>`.

        :returns: The address-expression node (:class:`Address \
            <doit.asm.asm.Address>`).

        :raises AssertionError: If in expression ``x[y]``, ``x`` is not \
            :class:`SegmentRegister <doit.asm.asm.SegmentRegister>`, or if \
            ``y`` is not one of :class:`int`, \
            :class:`BaseRegister <doit.asm.asm.BaseRegister>`, \
            :class:`Scale <doit.asm.asm.Scale>` or \
            :class:`Offset <doit.asm.asm.Offset>`.
        """

        assert isinstance(self, SegmentRegister), \
            "In x[y], x must be a segment register."
        assert isinstance(expr, int) or isinstance(expr, BaseRegister) \
            or isinstance(expr, Scale) or isinstance(expr, Offset), \
            "In x[y], y must be the valid address expression."
        return Address(self, expr)
    #-def

    def eval(self, env):
        """Get the operand value. The operand value should be computed when the
        instruction is invoked since it depends on the current state of `env`.
        This method is not implemented as default.

        :param env: Runtime environment.
        :type env: mostly :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The computed value (mostly :class:`int` or :class:`Pointer \
            <doit.runtime.atoms.Pointer>`).

        :raises NotImplementedError: If this method is not implemented.
        """

        raise NotImplementedError(
            "%s.eval is not implemented." % self.__class__.__name__
        )
    #-def

    def __repr__(self):
        """Returns the representation of operand suitable for its storage as
        persistent object.

        :returns: This object representation (mostly :class:`str`).

        :raises NotImplementedError: If this method is not implemented.
        """

        raise NotImplementedError(
            "repr(%s) is not implemented." % self.__class__.__name__
        )
    #-def

    def __str__(self):
        """Returns the text representation of operand. The default
        implementation is an alias for :meth:`AbstractOperand.__repr__() \
        <doit.asm.asm.AbstractOperand.__repr__>`.

        :returns: This object text representation (:class:`str`).

        :raises NotImplementedError: If this method implementation is the \
            default implementation and :meth:`AbstractOperand.__repr__() \
            <doit.asm.asm.AbstractOperand.__repr__>` method is not implemented.
        """

        return repr(self)
    #-def

    def base(self):
        """Returns the base register. The default value is :obj:`None`.

        :returns: Base register (:class:`BaseRegister \
            <doit.asm.asm.BaseRegister>` or :obj:`None`).

        From ``segreg[scale*basereg + offset]`` returns ``basereg``.
        """

        return None
    #-def

    def offset(self):
        """Returns the offset. The default value is 0.

        :returns: Offset (:class:`int`).

        From ``segreg[scale*basereg + offset]`` returns ``offset``.
        """

        return 0
    #-def

    def scale(self):
        """Returns the scale. The default value is 1.

        :returns: Scale (:class:`int`).

        From ``segreg[scale*basereg + offset]`` returns ``scale``.
        """

        return 1
    #-def

    def segment(self):
        """Returns the segment register. The default value is :obj:`None`.

        :returns: Segment register (:class:`SegmentRegister \
            <doit.asm.asm.SegmentRegister>` or :obj:`None`).

        From ``segreg[scale*basereg + offset]`` returns ``segreg``.
        """

        return None
    #-def
#-class

class Register(AbstractOperand):
    """Base class for ``register`` operand expressions.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the ``register`` operand expression.
        """

        AbstractOperand.__init__(self)
    #-def
#-class

class BaseRegister(Register):
    """Base class for ``base`` operand expressions.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the ``base`` operand expression.
        """

        Register.__init__(self)
    #-def

    def base(self):
        """Concrete implementation of :meth:`AbstractOperand.base() \
        <doit.asm.asm.AbstractOperand.base>`.

        :returns: This object (:class:`BaseRegister \
            <doit.asm.asm.BaseRegister>`).
        """

        return self
    #-def
#-class

class SegmentRegister(Register):
    """Base class for ``segment`` operand expressions.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the ``segment`` operand expression.
        """

        Register.__init__(self)
    #-def

    def segment(self):
        """Concrete implementation of :meth:`AbstractOperand.segment() \
        <doit.asm.asm.AbstractOperand.segment>`.

        :returns: This object (:class:`SegmentRegister \
            <doit.asm.asm.SegmentRegister>`).
        """

        return self
    #-def
#-class

class Scale(AbstractOperand):
    """Base class for ``scale*base`` operand expressions.
    """
    __slots__ = [ '__base', '__scale' ]

    def __init__(self, base, scale):
        """Initializes the ``scale*base`` operand expression.

        :param base: Base register.
        :type base: :class:`BaseRegister <doit.asm.asm.BaseRegister>`
        :param int scale: Scale.
        """

        AbstractOperand.__init__(self)
        self.__base = base
        self.__scale = scale
    #-def

    def base(self):
        """Concrete implementation of :meth:`AbstractOperand.base() \
        <doit.asm.asm.AbstractOperand.base>`.

        :returns: The base part of this operand expression \
            (:class:`BaseRegister <doit.asm.asm.BaseRegister>`).
        """

        return self.__base.base()
    #-def

    def scale(self):
        """Concrete implementation of :meth:`AbstractOperand.scale() \
        <doit.asm.asm.AbstractOperand.scale>`.

        :returns: The scale part of this operand expression (:class:`int`).
        """

        return self.__scale
    #-def
#-class

class Offset(AbstractOperand):
    """Base class for ``scale*base + offset`` operand expressions.
    """
    __slots__ = [ '__base', '__offset' ]

    def __init__(self, base, offset):
        """Initializes the ``scale*base + offset`` operand expression.

        :param base: Base register or scale operand expression.
        :type base: :class:`BaseRegister <doit.asm.asm.BaseRegister>` or \
            :class:`Scale <doit.asm.asm.Scale>`
        :param int offset: Offset.
        """

        AbstractOperand.__init__(self)
        self.__base = base
        self.__offset = offset
    #-def

    def base(self):
        """Concrete implementation of :meth:`AbstractOperand.base() \
        <doit.asm.asm.AbstractOperand.base>`.

        :returns: The base part of this operand expression \
            (:class:`BaseRegister <doit.asm.asm.BaseRegister>`).
        """

        return self.__base.base()
    #-def

    def offset(self):
        """Concrete implementation of :meth:`AbstractOperand.offset() \
        <doit.asm.asm.AbstractOperand.offset>`.

        :returns: The offset part of this operand expression (:class:`int`).
        """

        return self.__offset
    #-def

    def scale(self):
        """Concrete implementation of :meth:`AbstractOperand.scale() \
        <doit.asm.asm.AbstractOperand.scale>`.

        :returns: The scale part of this operand expression (:class:`int`).
        """

        return self.__base.scale()
    #-def
#-class

class Address(AbstractOperand):
    """Base class for ``segment[scale*base + offset]`` operand expressions.
    """
    __slots__ = [ '__segment', '__offset' ]

    def __init__(self, segment, offset):
        """Initializes the ``segment[scale*base + offset]`` operand expression.

        :param segment: Segment.
        :type segment: :class:`SegmentRegister <doit.asm.asm.SegmentRegister>`
        :param offset: Base register or scale operand expression or offset \
            operand expression.
        :type offset: :class:`BaseRegister <doit.asm.asm.BaseRegister>` or \
            :class:`Scale <doit.asm.asm.Scale>` or :class:`Offset \
            <doit.asm.asm.Offset>`
        """

        AbstractOperand.__init__(self)
        self.__segment = segment
        self.__offset = offset
    #-def

    def base(self):
        """Concrete implementation of :meth:`AbstractOperand.base() \
        <doit.asm.asm.AbstractOperand.base>`.

        :returns: The base part of this operand expression \
            (:class:`BaseRegister <doit.asm.asm.BaseRegister>`).
        """

        return self.__offset.base()
    #-def

    def offset(self):
        """Concrete implementation of :meth:`AbstractOperand.offset() \
        <doit.asm.asm.AbstractOperand.offset>`.

        :returns: The offset part of this operand expression (:class:`int`).
        """

        return self.__offset.offset()
    #-def

    def scale(self):
        """Concrete implementation of :meth:`AbstractOperand.scale() \
        <doit.asm.asm.AbstractOperand.scale>`.

        :returns: The scale part of this operand expression (:class:`int`).
        """

        return self.__offset.scale()
    #-def

    def segment(self):
        """Concrete implementation of :meth:`AbstractOperand.segment() \
        <doit.asm.asm.AbstractOperand.segment>`.

        :returns: The segment part of this operand expression \
            (:class:`SegmentRegister <doit.asm.asm.SegmentRegister`).
        """

        return self.__segment.segment()
    #-def

    def eval(self, env):
        """
        """

        return Pointer(self.__segment.eval(env), self.__offset.eval(env))
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
#-class
