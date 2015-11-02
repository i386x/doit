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
DoIt! general assembler interfaces.\
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

from doit.support.errors import DoItAssemblerError, \
                                doit_assert, not_implemented

_assert = lambda cond, emsg: doit_assert(cond, emsg, DoItAssemblerError, 2)

SECTION_INFO = ".info"
SECTION_TEXT = ".text"
SECTION_DATA = ".data"
SECTION_SYMBOLS = ".symbols"

class InstructionOperandExpression(object):
    """Base class for instruction operand expressions.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the instruction operand expression.
        """

        pass
    #-def

    def traverse(self, v):
        """Visits the nodes of this tree in postorder applying `v` on each
        visited node (including the node representing this tree).

        :param v: A visitor object.
        :type v: :class:`NodeVisitor <doit.asm.asm.NodeVisitor>`

        :raises ~doit.support.errors.DoItNotImplementedError: If this method \
            is not implemented.
        """

        not_implemented()
    #-def

    def __add__(self, rhs):
        """Handle the ``self + rhs`` expression.

        :param object rhs: A right-hand side.

        :returns: The node/tree for ``self + rhs`` expression \
            (:class:`AddNode <doit.asm.asm.AddNode>`).
        """

        return AddNode(self, rhs)
    #-def

    def __sub__(self, rhs):
        """Handle the ``self - rhs`` expression.

        :param object rhs: A right-hand side.

        :returns: The node/tree for ``self - rhs`` expression \
            (:class:`SubNode <doit.asm.asm.SubNode>`).
        """

        return SubNode(self, rhs)
    #-def

    def __mul__(self, rhs):
        """Handle the ``self * rhs`` expression.

        :param object rhs: A right-hand side.

        :returns: The node/tree for ``self * rhs`` expression \
            (:class:`MultNode <doit.asm.asm.MultNode>`).
        """

        return MultNode(self, rhs)
    #-def

    def __rmul__(self, lhs):
        """Handle the ``lhs * self`` expression.

        :param object lhs: A left-hand side.

        :returns: The node/tree for ``lhs * self`` expression \
            (:class:`MultNode <doit.asm.asm.MultNode>`).
        """

        return MultNode(lhs, self)
    #-def

    def __getitem__(self, idx):
        """Handle the ``self[idx]`` expression.

        :param object idx: An index expression.

        :returns: The node/tree for ``self[idx]`` expression \
            (:class:`IndexNode <doit.asm.asm.IndexNode>`).
        """

        return IndexNode(self, idx)
    #-def
#-class

class ConstNode(InstructionOperandExpression):
    """Base class for instruction operand expression constant value nodes.
    """
    __slots__ = [ '__value' ]

    def __init__(self, value):
        """Initializes the constant value node.

        :param object value: The kept value.
        """

        InstructionOperandExpression.__init__(self)
        self.__value = value
    #-def

    def traverse(self, v):
        """See :meth:`InstructionOperandExpression.traverse(v) \
        <doit.asm.asm.InstructionOperandExpression.traverse>`.
        """

        v(self.__value)
    #-def
#-class

class RegisterNode(InstructionOperandExpression):
    """Base class for register nodes.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register node.
        """

        InstructionOperandExpression.__init__(self)
    #-def

    def traverse(self, v):
        """See :meth:`InstructionOperandExpression.traverse(v) \
        <doit.asm.asm.InstructionOperandExpression.traverse>`.
        """

        v(self)
    #-def
#-class

class BinOpNode(InstructionOperandExpression):
    """Base class for binary operator nodes.
    """
    __slots__ = [ '__lhs', '__rhs' ]

    def __init__(self, lhs, rhs):
        """Initializes the binary operator node.

        :param object lhs: A left-hand side.
        :param object rhs: A right-hand side.
        """

        InstructionOperandExpression.__init__(self)
        self.__lhs = lhs
        self.__rhs = rhs
    #-def

    def traverse(self, v):
        """See :meth:`InstructionOperandExpression.traverse(v) \
        <doit.asm.asm.InstructionOperandExpression.traverse>`.
        """

        if isinstance(self.__lhs, InstructionOperandExpression):
            self.__lhs.traverse(v)
        else:
            v(self.__lhs)
        if isinstance(self.__rhs, InstructionOperandExpression):
            self.__rhs.traverse(v)
        else:
            v(self.__rhs)
        v(self)
    #-def
#-class

class AddNode(BinOpNode):
    """Base class for addition nodes.
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """Initializes the addition node.

        For parameters description, see :meth:`BinOpNode.__init__(lhs, rhs) \
        <doit.asm.asm.BinOpNode.__init__>`.
        """

        BinOpNode.__init__(self, lhs, rhs)
    #-def
#-class

class SubNode(BinOpNode):
    """Base class for subtraction nodes.
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """Initializes the subtraction node.

        For parameters description, see :meth:`BinOpNode.__init__(lhs, rhs) \
        <doit.asm.asm.BinOpNode.__init__>`.
        """

        BinOpNode.__init__(self, lhs, rhs)
    #-def
#-class

class MultNode(BinOpNode):
    """Base class for multiplication nodes.
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """Initializes the multiplication node.

        For parameters description, see :meth:`BinOpNode.__init__(lhs, rhs) \
        <doit.asm.asm.BinOpNode.__init__>`.
        """

        BinOpNode.__init__(self, lhs, rhs)
    #-def
#-class

class IndexNode(BinOpNode):
    """Base class for index nodes.
    """
    __slots__ = []

    def __init__(self, lhs, rhs):
        """Initializes the index node.

        For parameters description, see :meth:`BinOpNode.__init__(lhs, rhs) \
        <doit.asm.asm.BinOpNode.__init__>`.
        """

        BinOpNode.__init__(self, lhs, rhs)
    #-def
#-class

class NodeVisitor(object):
    """Base class for the visitors of :class:`InstructionOperandExpression \
    <doit.asm.asm.InstructionOperandExpression>` nodes.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the node visitor.
        """

        pass
    #-def

    def __call__(self, node):
        """Do specified action on the visited `node`.

        :param node: The visited node.
        :type node: :class:`InstructionOperandExpression \
            <doit.asm.asm.InstructionOperandExpression>`
        """

        pass
    #-def
#-class

class InstructionOperand(object):
    """Base class for instruction operands.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the instruction operand.
        """

        pass
    #-def
#-class

class Instruction(object):
    """Base class for instructions.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the instruction.
        """

        pass
    #-def
#-class

class AsmCommon(object):
    """Common assembler interface.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the common parts of assembler.
        """

        pass
    #-def

    def comment(self, s):
        """Allow to document what is produced by assembler methods call chain.

        :param str s: A string with comment.

        :returns: This object (:class:`AsmCommon <doit.asm.asm.AsmCommon>`).

        Since in Python this is not a valid::

            x86asm \\
              .section(".text") \\
                # Push a parameter onto the stack: \\
                .push(eax) \\
              .end_section() \\
            .end()

        we must use the following::

            x86asm \\
              .section(".text") \\
                .comment( \\
                "Push a parameter onto the stack:") \\
                .push(eax) \\
              .end_section() \\
            .end()
        """

        return self
    #-def
#-class

class BufferMixinBase(AsmCommon):
    """Base class for buffer mixins.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the mixin.
        """

        AsmCommon.__init__(self)
    #-def

    def __setitem__(self, key, value):
        """Stores `value` under the `key`.

        :param object key: A key.
        :param object value: A value to be stored.

        :raises ~doit.support.errors.DoItNotImplementedError: If the method \
            is not implemented.
        :raises ~doit.support.errors.DoItAssemblerError: If the operation \
            cannot be performed.
        """

        not_implemented()
    #-def

    def __getitem__(self, key):
        """Reads a value stored under the `key`.

        :param object key: A key.

        :returns: The stored value (:class:`object`).

        :raises ~doit.support.errors.DoItNotImplementedError: If the method \
            is not implemented.
        :raises ~doit.support.errors.DoItAssemblerError: If the operation \
            cannot be performed.
        """

        not_implemented()
    #-def

    def __len__(self):
        """Get the size of the stored data.

        :returns: The size of the stored data (:class:`int`).

        :raises ~doit.support.errors.DoItNotImplementedError: If the method \
            is not implemented.
        """

        not_implemented()
    #-def

    def data(self):
        """Gets the stored data.

        :returns: The stored data (:class:`object` -- must be iterable).

        :raises ~doit.support.errors.DoItNotImplementedError: If the method \
            is not implemented.
        """

        not_implemented()
    #-def
#-class

class DataWriterMixinBase(AsmCommon):
    """Base class for mixins that determine the way how to write a data to the
    buffer.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the data writer mixin.
        """

        AsmCommon.__init__(self)
    #-def

    def emit(self, data, *args):
        """Writes the `data` to the buffer.

        :param object data: A data to be written.
        :param tuple args: An additional arguments.

        :raises ~doit.support.errors.DoItNotImplementedError: If the method \
            is not implemented.
        :raises ~doit.support.errors.DoItAssemblerError: If the operation \
            cannot be performed.
        """

        not_implemented()
    #-def
#-class

class Section(AsmCommon):
    """Base class for assembler sections (like ``.info``, ``.text`` or
    ``.data``).
    """
    __slots__ = [ '__creator', '__name', '__properties' ]

    def __init__(self, creator, name, properties):
        """Initializes the section.

        :param creator: An owner of this section.
        :type creator: :class:`Sections <doit.asm.asm.Sections>`
        :param str name: A section name.
        :param dict properties: A section properties.
        """

        AsmCommon.__init__(self)
        self.__creator = creator
        self.__name = name
        self.__properties = properties
    #-def

    def end_section(self):
        """Close this section.

        :returns: The owner of this section (:class:`Sections \
            <doit.asm.asm.Sections>`).
        """

        self.on_end_section()
        return self.__creator
    #-def

    def on_end_section(self):
        """Called by :meth:`end_section() <doit.asm.asm.Section.end_section>`.
        """

        pass
    #-def

    def size(self):
        """Get the size of this section.

        :returns: The size of this section (:class:`int`).
        """

        return len(self)
    #-def

    def creator(self):
        """Get the owner of this section.

        :returns: The owner of this section (:class:`Sections \
            <doit.asm.asm.Sections>`).
        """

        return self.__creator
    #-def

    def name(self):
        """Get the name of this section.

        :returns: The name of this section (:class:`str`).
        """

        return self.__name
    #-def

    def properties(self):
        """Get the properties of this section.

        :returns: The properties of this section (:class:`dict`).
        """

        return self.__properties
    #-def
#-class

class Sections(object):
    """Base class for section containers.
    """
    __slots__ = [
        '__creator', '__sections', '__name2pos', '__scope', '__symbols'
    ]

    def __init__(self, creator):
        """Initializes the container.

        :param creator: An owner of this container.
        :type creator: :class:`Assembler <doit.asm.asm.Assembler>`
        """

        self.__creator = creator
        self.reinitialize()
    #-def

    def end(self):
        """Close the container of sections (ends the definition of sections).

        :returns: The owner of this container (:class:`Assembler \
            <doit.asm.asm.Assembler>`).

        :raises ~doit.support.errors.DoItAssemblerError: If the assembling \
            process fails.
        """

        self.on_end()
        return self.__creator
    #-def

    def section(self, name, **properties):
        """Starts a new section.

        :param str name: A section name.
        :param dict properties: A properties of section.

        :returns: The new section (:class:`Section <doit.asm.asm.Section>`).

        :raises ~doit.support.errors.DoItAssemblerError: If the section with \
            the name `name` was already started.
        """

        _assert(
            name not in self.__name2pos,
            "Section %s already exists" % repr(name)
        )
        s = self.create_section(name, properties)
        self.__name2pos[name] = len(self.__sections)
        self.__sections.append(s)
        self.on_section(name, properties)
        return s
    #-def

    def on_end(self):
        """Called by :meth:`end() <doit.asm.asm.Sections.end>`.

        :raises ~doit.support.errors.DoItAssemblerError: If the assembling \
            process fails.
        """

        pass
    #-def

    def on_section(self, name, properties):
        """Called by :meth:`section(name, **properties) \
        <doit.asm.asm.Sections.section>` just before the new section is
        returned.

        :param str name: A name of section.
        :param dict properties: A properties of section.
        """

        pass
    #-def

    def create_section(self, name, properties):
        """Called by :meth:`section(name, **properties) \
        <doit.asm.asm.Sections.section>` to create a new section.

        :param str name: A name of section.
        :param dict properties: A properties of section.

        :returns: The new section (:class:`Section <doit.asm.asm.Section>`).

        :raises ~doit.support.errors.DoItNotImplementedError: If this method \
            is not implemented.
        """

        not_implemented()
    #-def

    def add_symbol(self, name, *data):
        """Add a new symbol `name` to the symbol table.

        :param str name: A name of symbol.
        :param tuple data: An additional informations.

        :raises ~doit.support.errors.DoItAssemblerError: If a symbol was \
            already defined.
        """

        name = self.full_symbol_name(name)
        _assert(
            name not in self.__symbols,
            "Symbol %s is already defined" % repr(name)
        )
        self.__symbols[name] = data
    #-def

    def full_symbol_name(self, name):
        """Get the full (qualified) name of the symbol.

        :param str name: A name of the symbol.

        :returns: The full (qualified) name of the symbol (:class:`str`).
        """

        if self.__is_local_name(name):
            name = "%s%s" % (self.__scope, name)
        return name
    #-def

    def set_scope(self, scope):
        """Set the scope name.

        :param str scope: A scope name.
        """

        if self.__is_local_name(scope):
            return
        self.__scope = scope
    #-def

    def reinitialize(self):
        """Reinitializes the container.
        """

        self.__sections = []
        self.__name2pos = {}
        self.__scope = ""
        self.__symbols = {}
    #-def

    def clear(self):
        """Clear the container of sections (including symbol table).
        """

        self.__sections.clear()
        self.__name2pos.clear()
        self.__scope = ""
        self.__symbols.clear()
    #-def

    def creator(self):
        """Get the owner of this container.

        :returns: The owner of this container of sections (:class:`Assembler \
            <doit.asm.asm.Assembler>`).
        """

        return self.__creator
    #-def

    def sections(self):
        """Get the kept sections.

        :returns: A pair containing a list of sections and a name of section \
            to index to list of sections dictionary (:class:`tuple`).
        """

        return self.__sections, self.__name2pos
    #-def

    def scope(self):
        """Get the recent scope name.

        :returns: The recent scope name (:class:`str`).
        """

        return self.__scope
    #-def

    def symbols(self):
        """Get the symbol table.

        :returns: The symbol table (:class:`dict`).
        """

        return self.__symbols
    #-def

    @staticmethod
    def __is_local_name(name):
        """Test whether `name` is local.

        :param str name: A name.

        :returns: :obj:`True` if `name` is local (:class:`bool`).

        Local names begins with one dot, eg. ``.label``, ``.foo``, but not
        ``..bar``.
        """

        return name.startswith('.') and not name.startswith('..')
    #-def
#-class

class Assembler(object):
    """Base class for assemblers.
    """
    __slots__ = [ '__sections' ]

    def __init__(self):
        """Initializes the assembler.
        """

        self.__sections = self.create_sections()
    #-def

    def start(self):
        """Starts the definition of sections.

        :returns: The container of sections (:class:`Sections \
            <doit.asm.asm.Sections>`).
        """

        self.on_start()
        self.__sections.reinitialize()
        return self.__sections
    #-def

    def on_start(self):
        """Called by :meth:`start() <doit.asm.asm.Assembler.start>`.
        """

        pass
    #-def

    def create_sections(self):
        """Called by :meth:`constructor <doit.asm.asm.Assembler.__init__>` to
        create a new container of sections.

        :returns: The new container of sections (:class:`Sections \
            <doit.asm.asm.Sections>`).

        :raises ~doit.support.errors.DoItNotImplementedError: If this method \
            is not implemented.
        """

        not_implemented()
    #-def

    def sections(self):
        """Get the container of sections.

        :returns: The container of sections (:class:`Sections \
            <doit.asm.asm.Sections>`).
        """

        return self.__sections
    #-def
#-class
