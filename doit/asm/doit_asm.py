#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/asm/doit_asm.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-04-22 13:16:12 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! assembler.\
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

import time

from doit.support.errors import DoItRuntimeError, DoItAssemblerError, \
                                  DoItLinkerError, \
                                doit_assert, not_implemented

from doit.asm.asm import SECTION_INFO, SECTION_TEXT, SECTION_DATA, \
                           SECTION_SYMBOLS, \
                         ConstNode, RegisterNode, AddNode, SubNode, \
                           IndexNode, \
                         NodeVisitor, \
                         InstructionOperand, \
                         BufferMixinBase, Section, \
                         Sections, Assembler

from doit.config.version import DOIT_VERSION

_assert = lambda cond, emsg: doit_assert(cond, emsg, DoItAssemblerError, 2)
_fail = lambda emsg: doit_assert(False, emsg, DoItAssemblerError, 2)
_reraise = lambda exc: doit_assert(False, str(exc), DoItAssemblerError, 2)
_lassert = lambda cond, emsg: doit_assert(cond, emsg, DoItLinkerError, 2)
_rtassert = lambda cond, emsg: doit_assert(cond, emsg, DoItRuntimeError, 2)

class DoItInstructionOperand(InstructionOperand):
    """`DoIt!` instruction operand base class.
    """
    __slots__ = []

    def __init__(self):
        """Initializes `DoIt!` instruction operand.
        """

        InstructionOperand.__init__(self)
    #-def

    def setval(self, vm, value):
        """Set the value of `DoIt!` instruction operand.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`
        :param object value: A value of instruction operand.

        :raises ~doit.support.errors.DoItNotImplementedError: If this method \
            is not implemented.
        """

        not_implemented()
    #-def

    def getval(self, vm):
        """Get the value of `DoIt!` instruction operand.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of instruction operand (:class:`object`).

        :raises ~doit.support.errors.DoItNotImplementedError: If this method \
            is not implemented.
        """

        not_implemented()
    #-def

    def update(self, symbols):
        """Computes the final value of `DoIt!` instruction operand.

        :param dict symbols: A symbol table.

        :raises ~doit.support.errors.DoItLinkerError: If the final value \
            cannot be computed.

        This method is called during linking process by linker.
        """

        pass
    #-def

    def is_immediate(self):
        """Test if the instruction operand is an immediate operand.

        :returns: :obj:`True` if the instruction operand is an immediate \
            operand (:class:`bool`).
        """

        return False
    #-def
#-class

class Register(RegisterNode, DoItInstructionOperand):
    """Register operand base class.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register.
        """

        RegisterNode.__init__(self)
        DoItInstructionOperand.__init__(self)
    #-def
#-class

class BaseRegister(Register):
    """Base register operand base class.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the base register.
        """

        Register.__init__(self)
    #-def
#-class

class SegmentRegister(Register):
    """Segment register operand base class.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the segment register.
        """

        Register.__init__(self)
    #-def
#-class

class DetectSegmentRegister(SegmentRegister):
    """Used by :class:`InsOpCompiler <doit.asm.doit_asm.InsOpCompiler>` to
    detect which segment register has been used by :class:`MemoryLocation \
    <doit.asm.doit_asm.MemoryLocation>`.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register.
        """

        SegmentRegister.__init__(self)
    #-def
#-class

class RegisterCS(SegmentRegister):
    """Code segment register.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register.
        """

        SegmentRegister.__init__(self)
    #-def

    def setval(self, vm, value):
        """Set the value of the code segment register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`
        :param value: A new value of the code segment register.
        :type value: :class:`Memory <doit.runtime.memory.Memory>`

        :raises ~doit.support.errors.DoItRuntimeError: If `value` is not the \
            instance of :class:`Memory <doit.runtime.memory.Memory>`.
        """

        _rtassert(isinstance(value, Memory), "Memory segment was expected")
        vm.cs = value
    #-def

    def getval(self, vm):
        """Get the value of the code segment register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of the code segment register (:class:`Memory \
            <doit.runtime.memory.Memory>`).
        """

        return vm.cs
    #-def
#-class

class RegisterDS(SegmentRegister):
    """Data segment register.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register.
        """

        SegmentRegister.__init__(self)
    #-def

    def setval(self, vm, value):
        """Set the value of the data segment register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`
        :param value: A new value of the data segment register.
        :type value: :class:`Memory <doit.runtime.memory.Memory>`

        :raises ~doit.support.errors.DoItRuntimeError: If `value` is not the \
            instance of :class:`Memory <doit.runtime.memory.Memory>`.
        """

        _rtassert(isinstance(value, Memory), "Memory segment was expected")
        vm.ds = value
    #-def

    def getval(self, vm):
        """Get the value of the data segment register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of the data segment register (:class:`Memory \
            <doit.runtime.memory.Memory>`).
        """

        return vm.ds
    #-def
#-class

class RegisterSS(SegmentRegister):
    """Stack segment register.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register.
        """

        SegmentRegister.__init__(self)
    #-def

    def setval(self, vm, value):
        """Set the value of the stack segment register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`
        :param value: A new value of the stack segment register.
        :type value: :class:`Memory <doit.runtime.memory.Memory>`

        :raises ~doit.support.errors.DoItRuntimeError: If `value` is not the \
            instance of :class:`Memory <doit.runtime.memory.Memory>`.
        """

        _rtassert(isinstance(value, Memory), "Memory segment was expected")
        vm.ss = value
    #-def

    def getval(self, vm):
        """Get the value of the stack segment register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of the stack segment register (:class:`Memory \
            <doit.runtime.memory.Memory>`).
        """

        return vm.ss
    #-def
#-class

class RegisterSP(BaseRegister):
    """Stack pointer register.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register.
        """

        BaseRegister.__init__(self)
    #-def

    def setval(self, vm, value):
        """Set the value of the stack pointer register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`
        :param int value: A new value of the stack pointer register.

        :raises ~doit.support.errors.DoItRuntimeError: If `value` is not \
            integer.
        """

        _rtassert(isinstance(value, int), "Integer was expected")
        vm.sp = value
    #-def

    def getval(self, vm):
        """Get the value of the stack pointer register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of the stack pointer register (:class:`int`).
        """

        return vm.sp
    #-def
#-class

class RegisterFP(BaseRegister):
    """Frame pointer register.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the register.
        """

        BaseRegister.__init__(self)
    #-def

    def setval(self, vm, value):
        """Set the value of the frame pointer register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`
        :param int value: A new value of the frame pointer register.

        :raises ~doit.support.errors.DoItRuntimeError: If `value` is not \
            integer.
        """

        _rtassert(isinstance(value, int), "Integer was expected")
        vm.fp = value
    #-def

    def getval(self, vm):
        """Get the value of the frame pointer register.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of the frame pointer register (:class:`int`).
        """

        return vm.fp
    #-def
#-class

class Immediate(DoItInstructionOperand):
    """Implements immediate instruction operand.
    """
    __slots__ = [ '__relocable_parts', '__constant_part', '__value' ]

    def __init__(self, relocable, constant):
        """Initializes the operand.

        :param str relocable: A relocable part of the operand (mostly a lable \
            name).
        :param int constant: A constant part of the operand.
        """

        DoItInstructionOperand.__init__(self)
        self.__relocable_parts = {relocable: 1}
        self.__constant_part = constant
        self.__value = 0
    #-def

    def getval(self, vm):
        """Get the value of the operand.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of the operand (:class:`int`).
        """

        return self.__value
    #-def

    def __iadd__(self, rhs):
        """Implements the ``+=`` operator (adds the value of right-hand side
        immediate operand to this one).

        :param rhs: A right-hand side immediate operand.
        :type rhs: :class:`Immediate <doit.asm.doit_asm.Immediate>`

        :returns: This object (:class:`Immediate \
            <doit.asm.doit_asm.Immediate>`).
        """

        return self.__add(rhs, 1)
    #-def

    def __isub__(self, rhs):
        """Implements the ``-=`` operator (subtracts the value of right-hand \
        side immediate operand from this one).

        :param rhs: A right-hand side immediate operand.
        :type rhs: :class:`Immediate <doit.asm.doit_asm.Immediate>`

        :returns: This object (:class:`Immediate \
            <doit.asm.doit_asm.Immediate>`).
        """

        return self.__add(rhs, -1)
    #-def

    def __add(self, rhs, sgn):
        """Adds the value of `rhs` immediate operand to this one.

        :param rhs: A right-hand side immediate operand.
        :type rhs: :class:`Immediate <doit.asm.doit_asm.Immediate>`
        :param int sgn: A right-hand side operand sign (can be 1 or -1).

        :returns: This object (:class:`Immediate \
            <doit.asm.doit_asm.Immediate>`).
        """

        relocable_parts = rhs.get_relocable_parts()
        for name in relocable_parts:
            if name not in self.__relocable_parts:
                self.__relocable_parts[name] = 0
            self.__relocable_parts[name] += sgn*relocable_parts[name]
        self.__constant_part += sgn*rhs.get_constant_part()
        return self
    #-def

    def update(self, symbols):
        """See :meth:`DoItInstructionOperand.update(symbols) \
        <doit.asm.doit_asm.DoItInstructionOperand.update>`.
        """

        rp = self.__relocable_parts
        # Discard the useless entries.
        self.__relocable_parts = dict([(k, rp[k]) for k in rp if k and rp[k]])
        self.__value = self.__constant_part
        sec_ = ""
        for r in self.__relocable_parts:
            # All symbols must be defined.
            _lassert(r in symbols, "Undefined symbol %s" % repr(r))
            sec, loc = symbols[r]
            sec_ = sec if not sec_ else sec_
            # All symbols used in one instruction operand expression must be
            # from the same section.
            _lassert(
                sec and sec_ == sec,
                "Symbol %s is from section %s instead of %s" \
                % (repr(r), repr(sec), repr(sec_))
            )
            # Add the offset of `r` times the number of its occurences.
            self.__value += loc*self.__relocable_parts[r]
        #-for
    #-def

    def is_immediate(self):
        """See :meth:`DoItInstructionOperand.is_immediate() \
        <doit.asm.doit_asm.DoItInstructionOperand.is_immediate>`.
        """

        return True
    #-def
#-class

class BasePlusOffset(DoItInstructionOperand):
    """Implements ``base + offset`` instruction operand. Can be used only as
    a part of :class:`MemoryLocation <doit.asm.doit_asm.MemoryLocation>`.
    """
    __slots__ = [ '__base', '__offset' ]

    def __init__(self, base, offset):
        """Initializes the operand.

        :param base: A base register.
        :type base: :class:`BaseRegister <doit.asm.doit_asm.BaseRegister>`
        :param offset: An offset.
        :type offset: :class:`Immediate <doit.asm.doit_asm.Immediate>`
        """

        DoItInstructionOperand.__init__(self)
        self.__base = base
        self.__offset = offset
    #-def

    def getval(self, vm):
        """Get the value of the operand.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of the operand (:class:`int`).

        The value of the operand is given by the value of the base register
        plus offset.
        """

        return self.__base.getval(vm) + self.__offset.getval(vm)
    #-def

    def update(self, symbols):
        """See :meth:`DoItInstructionOperand.update(symbols) \
        <doit.asm.doit_asm.DoItInstructionOperand.update>`.
        """

        self.__offset.update(symbols)
    #-def

    def __iadd__(self, rhs):
        """Implements the ``+=`` operator (adds the value of right-hand side
        immediate operand to the offset part of this one).

        :param rhs: A right-hand side immediate operand.
        :type rhs: :class:`Immediate <doit.asm.doit_asm.Immediate>`

        :returns: This object (:class:`BasePlusOffset \
            <doit.asm.doit_asm.BasePlusOffset>`).
        """

        self.__offset += rhs
        return self
    #-def

    def __isub__(self, rhs):
        """Implements the ``-=`` operator (subtracts the value of right-hand \
        side immediate operand from the offset part of this one).

        :param rhs: A right-hand side immediate operand.
        :type rhs: :class:`Immediate <doit.asm.doit_asm.Immediate>`

        :returns: This object (:class:`BasePlusOffset \
            <doit.asm.doit_asm.BasePlusOffset>`).
        """

        self.__offset -= rhs
        return self
    #-def
#-class

class MemoryLocation(DoItInstructionOperand):
    """Implements memory location (``[...]``) instruction operand.
    """
    __slots__ = [ '__segment', '__offset' ]

    def __init__(self, segment, offset):
        """Initializes the operand.

        :param segment: A segment part.
        :type segment: :class:`SegmentRegister \
            <doit.asm.doit_asm.SegmentRegister>`
        :param offset: An offset part.
        :type offset: :class:`Immediate <doit.asm.doit_asm.Immediate>`
        """

        DoItInstructionOperand.__init__(self)
        self.__segment = segment
        self.__offset = offset
    #-def

    def setval(self, vm, value):
        """Set the value of memory cell at the kept memory location.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`
        :param object value: A value to be set.

        :raises ~doit.support.errors.DoItMemoryAccessError: If the memory \
            location is invalid.
        """

        self.__segment.getval(vm)[self.__offset.getval(vm)] = value
    #-def

    def getval(self, vm):
        """Get the value of memory cell at the kept memory location.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :returns: The value of memory cell at the kept memory location \
            (:class:`object`).

        :raises ~doit.support.errors.DoItMemoryAccessError: If the memory \
            location is invalid.
        """

        return self.__segment.getval(vm)[self.__offset.getval(vm)]
    #-def

    def update(self, symbols):
        """See :meth:`DoItInstructionOperand.update(symbols) \
        <doit.asm.doit_asm.DoItInstructionOperand.update>`.
        """

        self.__offset.update(symbols)
    #-def
#-class

class InsOpCompiler(NodeVisitor):
    """A visitor that compiles instruction operand expression tree into the
    instruction operand.
    """
    __slots__ = [ '__full_symbol_name', '__stack' ]

    def __init__(self, section):
        """Initializes the compiler.

        :param section: A section to which the instruction with the \
            instruction operand expression to be compiled belongs to.
        :type section: :class:`TextOrDataSection \
            <doit.asm.doit_asm.TextOrDataSection>`
        """

        NodeVisitor.__init__(self)
        self.__full_symbol_name = section.creator().full_symbol_name
        self.__stack = []
    #-def

    def __call__(self, node):
        """Performs a one compilation step on a visited `node`.

        :param node: A visited node.
        :type node: :class:`int`, :class:`str`, or \
            :class:`InstructionOperandExpression \
            <doit.asm.asm.InstructionOperandExpression>`

        :raises ~doit.support.errors.DoItAssemblerError: If the instruction \
            operand expression is ill-formed.
        """

        if isinstance(node, str):
            self.__stack.append(Immediate(self.__full_symbol_name(node), 0))
        elif isinstance(node, int):
            self.__stack.append(Immediate('', node))
        elif isinstance(node, RegisterNode):
            self.__stack.append(node)
        elif isinstance(node, AddNode):
            self.__compile_add()
        elif isinstance(node, SubNode):
            self.__compile_sub()
        elif isinstance(node, IndexNode):
            self.__compile_mem()
        else:
            _fail("Invalid instruction operand expression node")
    #-def

    def __compile_add(self):
        """Handle the binary ``+`` operator.

        :raises ~doit.support.errors.DoItAssemblerError: In the case of \
            invalid operands.
        """

        o2 = self.__stack.pop()
        o1 = self.__stack[-1]
        if isinstance(o1, Immediate) and isinstance(o2, Immediate):
            self.__stack[-1] += o2
        elif isinstance(o1, BaseRegister) and isinstance(o2, Immediate):
            self.__stack[-1] = BasePlusOffset(o1, o2)
        elif isinstance(o2, BaseRegister) and isinstance(o1, Immediate):
            self.__stack[-1] = BasePlusOffset(o2, o1)
        elif isinstance(o1, BasePlusOffset) and isinstance(o2, Immediate):
            self.__stack[-1] += o2
        elif isinstance(o2, BasePlusOffset) and isinstance(o1, Immediate):
            o2 += o1
            self.__stack[-1] = o2
        else:
            _fail("Invalid operands of `+` binary operator")
    #-def

    def __compile_sub(self):
        """Handle the binary ``-`` operator.

        :raises ~doit.support.errors.DoItAssemblerError: In the case of \
            invalid operands.
        """

        o2 = self.__stack.pop()
        o1 = self.__stack[-1]
        if isinstance(o1, Immediate) and isinstance(o2, Immediate):
            self.__stack[-1] -= o2
        elif isinstance(o1, BaseRegister) and isinstance(o2, Immediate):
            self.__stack[-1] = BasePlusOffset(o1, Immediate('', 0))
            self.__stack[-1] -= o2
        elif isinstance(o1, BasePlusOffset) and isinstance(o2, Immediate):
            self.__stack[-1] -= o2
        else:
            _fail("Invalid operands of `-` binary operator")
    #-def

    def __compile_mem(self):
        """Handle the index (``[...]``) operator.

        :raises ~doit.support.errors.DoItAssemblerError: In the case of \
            invalid operands.
        """

        o2 = self.__stack.pop()
        o1 = self.__stack[-1]
        _assert(isinstance(o1, SegmentRegister), "Segment register expected")
        _assert(
            isinstance(o2, (Immediate, BaseRegister, BasePlusOffset)),
            "Invalid operand"
        )
        if isinstance(o1, DetectSegmentRegister):
            if isinstance(o2, Immediate):
                o1 = RegisterDS()
            elif isinstance(o2, BaseRegister) \
            or isinstance(o2, BasePlusOffset):
                o1 = RegisterSS()
            else:
                _fail("Invalid combination of operands")
        self.__stack[-1] = MemoryLocation(o1, o2)
    #-def

    def result(self):
        """Get the compiled instruction operand.

        :returns: The compiled instruction operand \
            (:class:`DoItInstructionOperand \
            <doit.asm.doit_asm.DoItInstructionOperand>`).

        :raises ~doit.support.errors.DoItAssemblerError: If the instruction \
            operand expression was ill-formed.
        """

        _assert(
            len(self.__stack) == 1, "Invalid instruction operand expression"
        )
        return self.__stack[-1]
    #-def
#-class

class ListLikeBufferMixin(BufferMixinBase):
    """Buffer mixin that implements :class:`list` behaviour.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the buffer mixin.
        """

        BufferMixinBase.__init__(self)
    #-def

    def __setitem__(self, idx, value):
        """Writes `value` to the buffer on the position `idx`.

        :param int idx: An index to the buffer.
        :param object value: A value to be written.

        :raises ~doit.support.errors.DoItAssemblerError: If the index is out \
            of range.
        """

        try:
            self.data_[idx] = value
        except IndexError as e:
            _reraise(e)
    #-def

    def __getitem__(self, idx):
        """Reads a value stored at `idx` in the buffer.

        :param int idx: An index to the buffer.

        :returns: The stored value (:class:`object`).

        :raises ~doit.support.errors.DoItAssemblerError: If the index is out \
            of range.
        """

        try:
            return self.data_[idx]
        except IndexError as e:
            _reraise(e)
    #-def

    def append(self, value):
        """Appends `value` to the end of the buffer.

        :param object value: A value to be appended.
        """

        self.data_.append(value)
    #-def

    def __len__(self):
        """See :meth:`BufferMixinBase.__len__() \
        <doit.asm.asm.BufferMixinBase.__len__>`.
        """

        return len(self.data_)
    #-def

    def data(self):
        """Get the stored data.

        :returns: The stored data (:class:`list`).
        """

        return self.data_
    #-def
#-class

class DictLikeBufferMixin(BufferMixinBase):
    """Buffer mixin that behaves like :class:`dict`.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the buffer mixin.
        """

        BufferMixinBase.__init__(self)
    #-def

    def __setitem__(self, key, value):
        """Stores `value` under the `key`.

        :param object key: A key.
        :param object value: A value to be stored.

        :raises ~doit.support.errors.DoItAssemblerError: If `key` is not \
            hashable.
        """

        try:
            self.data_[key] = value
        except TypeError as e:
            _reraise(e)
    #-def

    def __getitem__(self, key):
        """Get the value stored under the `key`.

        :param object key: A key.

        :returns: The stored value (:class:`object`).

        :raises ~doit.support.errors.DoItAssemblerError: If `key` is not \
            hashable or there are no data stored under the `key`.
        """

        try:
            return self.data_[key]
        except (TypeError, KeyError) as e:
            _reraise(e)
    #-def

    def __len__(self):
        """See :meth:`BufferMixinBase.__len__() \
        <doit.asm.asm.BufferMixinBase.__len__>`.
        """

        return len(self.data_)
    #-def

    def data(self):
        """Get the stored data.

        :returns: The stored data (:class:`dict`).
        """

        return self.data_
    #-def
#-class

class InfoSection(DictLikeBufferMixin, Section):
    """Implements the ``.info`` section.
    """
    ARCH_FIELD = 'arch'
    ARCH_VERSION_FIELD = 'arch_version'
    PLATFORM_FIELD = 'platform'
    PLATFORM_VERSION_FIELD = 'platform_version'
    ASM_FIELD = 'asm'
    VERSION_FIELD = 'version'
    TIMEDATE_FIELD = 'timedate'
    __slots__ = [ 'data_' ]

    def __init__(self, creator, name, properties):
        """Initializes the section.

        :param creator: An owner of this section.
        :type creator: :class:`DoItSections <doit.asm.doit_asm.DoItSections>`
        :param str name: A section name.
        :param dict properties: A section properties.
        """

        DictLikeBufferMixin.__init__(self)
        Section.__init__(self, creator, name, properties)
        self.data_ = self.properties()
    #-def

    def arch(self, arch_name):
        """Implements the ``arch`` pseudo instruction.

        :param str arch_name: A name of target architecture.

        :returns: This object (:class:`InfoSection \
            <doit.asm.doit_asm.InfoSection>`).
        """

        self[self.__class__.ARCH_FIELD] = arch_name
        return self
    #-def

    def arch_version(self, major, minor, patchlevel, date, info):
        """Implements the ``arch_version`` pseudo instruction.

        :param int major: A major version number.
        :param int minor: A minor version number.
        :param int patchlevel: A patch level.
        :param int date: A date (``10000*year + 100*month + day``).
        :param str info: An additional informations.

        :returns: This object (:class:`InfoSection \
            <doit.asm.doit_asm.InfoSection>`).
        """

        self[self.__class__.ARCH_VERSION_FIELD] = Version(
            major, minor, patchlevel, date, info
        )
        return self
    #-def

    def platform(self, platform_name):
        """Implements the ``platform`` pseudo instruction.

        :param str platform_name: A name of target platform.

        :returns: This object (:class:`InfoSection \
            <doit.asm.doit_asm.InfoSection>`).
        """

        self[self.__class__.PLATFORM_FIELD] = platform_name
        return self
    #-def

    def platform_version(self, major, minor, patchlevel, date, info):
        """Implements the ``platform_version`` pseudo instruction.

        :param int major: A major version number.
        :param int minor: A minor version number.
        :param int patchlevel: A patch level.
        :param int date: A date (``10000*year + 100*month + day``).
        :param str info: An additional informations.

        :returns: This object (:class:`InfoSection \
            <doit.asm.doit_asm.InfoSection>`).
        """

        self[self.__class__.PLATFORM_VERSION_FIELD] = Version(
            major, minor, patchlevel, date, info
        )
        return self
    #-def

    def asm(self, asm_name):
        """Implements the ``asm`` pseudo instruction.

        :param str asm_name: A name of used assembler.

        :returns: This object (:class:`InfoSection \
            <doit.asm.doit_asm.InfoSection>`).
        """

        self[self.__class__.ASM_FIELD] = asm_name
        return self
    #-def

    def version(self, major, minor, patchlevel, date, info):
        """Implements the ``version`` pseudo instruction.

        :param int major: A major version number.
        :param int minor: A minor version number.
        :param int patchlevel: A patch level.
        :param int date: A date (``10000*year + 100*month + day``).
        :param str info: An additional informations.

        :returns: This object (:class:`InfoSection \
            <doit.asm.doit_asm.InfoSection>`).
        """

        self[self.__class__.VERSION_FIELD] = Version(
            major, minor, patchlevel, date, info
        )
        return self
    #-def

    def timedate(self, now = -1):
        """Implements the ``timedate`` pseudo instruction.

        :param int now: A time (in seconds since epoch) to be set.

        :returns: This object (:class:`InfoSection \
            <doit.asm.doit_asm.InfoSection>`).

        If now is negative, it is set by assembler at the end of assembling
        process.
        """

        self[self.__class__.TIMEDATE_FIELD] = now
        return self
    #-def
#-class

class TextOrDataSection(ListLikeBufferMixin, Section):
    """Implements the ``.text`` and ``.data`` sections.
    """
    __slots__ = [ 'data_' ]

    def __init__(self, creator, name, properties):
        """Initializes the section.

        :param creator: An owner of this section.
        :type creator: :class:`DoItSections <doit.asm.doit_asm.DoItSections>`
        :param str name: A section name.
        :param dict properties: A section properties.
        """

        ListLikeBufferMixin.__init__(self)
        Section.__init__(self, creator, name, properties)
        self.data_ = []
    #-def

    def label(self, name):
        """Define a new label.

        :param str name: A label name.

        :returns: This object (:class:`TextOrDataSection \
            <doit.asm.doit_asm.TextOrDataSection>`).

        :raises ~doit.support.errors.DoItAssemblerError: If a label cannot be \
            defined.
        """

        self.creator().add_symbol(name, self.name(), len(self))
        return self
    #-def

    def push(self, ioe):
        """Emits the ``PUSH`` instruction.

        :param ioe: An instruction operand expression.
        :type ioe: :class:`InstructionOperandExpression \
            <doit.asm.asm.InstructionOperandExpression>`

        :returns: This object (:class:`TextOrDataSection \
            <doit.asm.doit_asm.TextOrDataSection>`).

        :raises ~doit.support.errors.DoItAssemblerError: If the instruction \
            operand expression is not valid.
        """

        self.append(Push(self.__compile(ioe)))
        return self
    #-def

    def __compile(self, ioe):
        """Compiles an instruction operand expression.

        :param ioe: An instruction operand expression.
        :type ioe: :class:`InstructionOperandExpression \
            <doit.asm.asm.InstructionOperandExpression>`

        :returns: The compiled instruction operand expression \
            (:class:`DoItInstructionOperand \
            <doit.asm.doit_asm.DoItInstructionOperand>`).

        :raises ~doit.support.errors.DoItAssemblerError: If the instruction \
            operand expression is not valid.
        """

        if isinstance(ioe, (int, str)):
            ioe = ConstNode(ioe)
        elif isinstance(ioe, list):
            ioe = IndexNode(DetectSegmentRegister(), ioe[0])
        f = InsOpCompiler(self)
        ioe.traverse(f)
        return f.result()
    #-def
#-class

class SymbolsSection(DictLikeBufferMixin, Section):
    """Implements the ``.symbols`` section.
    """
    __slots__ = [ 'data_' ]

    def __init__(self, creator, name, properties):
        """Initializes the section.

        :param creator: An owner of this section.
        :type creator: :class:`DoItSections <doit.asm.doit_asm.DoItSections>`
        :param str name: A section name.
        :param dict properties: A section properties.
        """

        DictLikeBufferMixin.__init__(self)
        Section.__init__(self, creator, name, properties)
        self.data_ = self.creator().symbols()
    #-def
#-class

class DoItSections(Sections):
    """Implements `DoIt!` assembler section container.
    """
    name2section = {
        SECTION_INFO: InfoSection,
        SECTION_TEXT: TextOrDataSection,
        SECTION_DATA: TextOrDataSection,
        SECTION_SYMBOLS: SymbolsSection
    }
    __slots__ = []

    def __init__(self, creator):
        """Initializes the container.

        :param creator: An owner of this container.
        :type creator: :class:`DoItAssembler <doit.asm.doit_asm.DoItAssembler>`
        """

        Sections.__init__(self, creator)
    #-def

    def on_end(self):
        """Updates the time information.
        """

        sections, name2pos = self.sections()
        info = sections[name2pos[SECTION_INFO]]
        if info[InfoSection.TIMEDATE_FIELD] < 0:
            info.timedate(int(time.mktime(time.gmtime())))
    #-def

    def create_section(self, name, properties):
        """Creates a new section.

        :param str name: A name of a new section.
        :param dict properties: A properties of a new section.

        :returns: The new section (:class:`Section <doit.asm.asm.Section>`).

        :raises AssertionError: If the section cannot be created.
        """

        section = self.__class__.name2section.get(name, None)
        _assert(section is not None, "Unsupported section `%s`" % name)
        return section(self, name, properties)
    #-def
#-class

class DoItAssembler(Assembler):
    """Implements `DoIt!` assembler.

    Class members:

    * `registers` (:class:`tuple`) -- a tuple of 5 registers ( \
          :class:`code segment <doit.asm.doit_asm.RegisterCS>`, \
          :class:`data segment <doit.asm.doit_asm.RegisterDS>`, \
          :class:`stack segment <doit.asm.doit_asm.RegisterSS>`, \
          :class:`stack pointer <doit.asm.doit_asm.RegisterSP>` \
          and :class:`frame pointer <doit.asm.doit_asm.RegisterFP>`)
    """
    sections = tuple(DoItSections.name2section.keys())
    registers = (
        RegisterCS(), RegisterDS(), RegisterSS(), RegisterSP(), RegisterFP()
    )
    version = DOIT_VERSION
    __slots__ = []

    def __init__(self):
        """Initializes the assembler.
        """

        Assembler.__init__(self)
        # Section container is created now - add an .info section:
        self.sections().section(
            SECTION_INFO,
            arch = ARCH_NAME,
            arch_version = ARCH_VERSION,
            platform = PLATFORM_ANY,
            platform_version = VERSION_UNUSED,
            timedate = -1,
            asm = self.__class__.__name__,
            version = self.__class__.version
        )
        # Add a .symbols section:
        self.sections().section(SECTION_SYMBOLS)
    #-def

    def create_sections(self):
        """Creates a section container.

        :returns: The section container (:class:`DoItSections \
            <doit.asm.doit_asm.DoItSections>`).
        """

        return DoItSections(self)
    #-def
#-class
