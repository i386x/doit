#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/runtime/inst.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-03-27 22:42:45 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! VM instruction set.\
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

from doit.support.errors import not_implemented
from doit.asm.asm import Instruction

class DoItInstruction(Instruction):
    """`DoIt!` instruction base class.

    Member variables:

    * `op1` (:class:`DoItInstructionOperand \
        <doit.asm.doit_asm.DoItInstructionOperand>`) -- 1st operand
    * `op2` (:class:`DoItInstructionOperand \
        <doit.asm.doit_asm.DoItInstructionOperand>`) -- 2nd operand
    * `op3` (:class:`DoItInstructionOperand \
        <doit.asm.doit_asm.DoItInstructionOperand>`) -- 3rd operand
    """
    __slots__ = [ 'op1', 'op2', 'op3' ]

    def __init__(self, op1 = None, op2 = None, op3 = None):
        """Initializes the instruction.

        :param op1: A first instruction operand.
        :type op1: :class:`DoItInstructionOperand \
            <doit.asm.doit_asm.DoItInstructionOperand>`
        :param op2: A second instruction operand.
        :type op2: :class:`DoItInstructionOperand \
            <doit.asm.doit_asm.DoItInstructionOperand>`
        :param op3: A third instruction operand.
        :type op3: :class:`DoItInstructionOperand \
            <doit.asm.doit_asm.DoItInstructionOperand>`
        """

        Instruction.__init__(self)
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
    #-def

    def execute(self, vm):
        """Executes this instruction.

        :param vm: A virtual machine.
        :type vm: :class:`Interpreter <doit.runtime.vm.Interpreter>`

        :raises ~doit.support.errors.DoItNotImplementedError: If this method \
            is not implemented.
        :raises ~doit.support.errors.DoItError: If the execution fails.
        """

        not_implemented()
    #-def
#-class

class Push(DoItInstruction):
    """Implements the ``PUSH`` instruction.
    """
    __slots__ = []

    def __init__(self, op):
        """Initializes the instruction.

        :param op: An instruction operand.
        :type op: :class:`Immediate <doit.asm.doit_asm.Immediate>` or \
            :class:`Register <doit.asm.doit_asm.Register>` or \
            :class:`MemoryLocation <doit.asm.doit_asm.MemoryLocation>`
        """

        DoItInstruction.__init__(self, op)
    #-def

    def execute(self, vm):
        """See :meth:`DoItInstruction.execute(vm) \
        <doit.runtime.inst.DoItInstruction.execute>`.
        """

        vm.stack[vm.sp] = self.op1.getval(vm)
        vm.sp += 1
    #-def
#-class

class Pop(DoItInstruction):
    """Implements the ``POP`` instruction.
    """
    __slots__ = []

    def __init__(self, op):
        """Initializes the instruction.

        :param op: An instruction operand.
        :type op: :class:`Immediate <doit.asm.doit_asm.Immediate>` or \
            :class:`Register <doit.asm.doit_asm.Register>` or \
            :class:`MemoryLocation <doit.asm.doit_asm.MemoryLocation>`
        """

        DoItInstruction.__init__(self, op)
    #-def

    def execute(self, vm):
        """See :meth:`DoItInstruction.execute(vm) \
        <doit.runtime.inst.DoItInstruction.execute>`.
        """

        if self.op1.is_immediate():
            vm.sp -= self.op1.getval(vm)
        else:
            vm.sp -= 1
            self.op1.setval(vm, vm.stack[vm.sp])
    #-def
#-class

class Move(DoItInstruction):
    """Implements the ``MOVE`` instruction.
    """
    __slots__ = []

    def __init__(self, op1, op2):
        """Initializes the instruction.

        :param op1: A first instruction operand.
        :type op1: :class:`Register <doit.asm.doit_asm.Register>` or \
            :class:`MemoryLocation <doit.asm.doit_asm.MemoryLocation>`
        :param op2: A second instruction operand.
        :type op2: :class:`Immediate <doit.asm.doit_asm.Immediate>` or \
            :class:`Register <doit.asm.doit_asm.Register>` or \
            :class:`MemoryLocation <doit.asm.doit_asm.MemoryLocation>`
        """

        DoItInstruction.__init__(self, op1, op2)
    #-def

    def execute(self, vm):
        """See :meth:`DoItInstruction.execute(vm) \
        <doit.runtime.inst.DoItInstruction.execute>`.
        """

        self.op1.setval(vm, self.op2.getval(vm))
    #-def
#-class
