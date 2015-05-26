#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/inst.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-03-27 22:42:45 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! VM's instruction set.\
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

class Instruction(tuple):
    """
    """
    __slots__ = []

    def __init__(self, *args):
        """
        """

        tuple.__init__(self, args)
    #-def

    @staticmethod
    def operand_decode_read(vm, operand):
        """
        """

        if isinstance(operand, InstructionOperandExpression):
            operand = operand.eval(vm)
            if isinstance(operand, Pointer):
                operand = operand.read()
        if isinstance(operand, int):
            operand = HostInt(operand)
        assert isinstance(operand, Value), "Expected Value."
        return operand
    #-def

    @staticmethod
    def operand_decode_write(vm, operand, value):
        """
        """

        assert isinstance(operand, MemoryAccessNode), \
            "Memory expression required."
        operand.eval(vm).write(value)
    #-def

    def execute(self, vm):
        """
        """

        raise NotImplementedError("Instuction.execute is not implemented.")
    #-def

    def __repr__(self):
        """
        """

        raise NotImplementedError("Instuction.__repr__ is not implemented.")
    #-def

    def __str__(self):
        """
        """

        return repr(self)
    #-def
#-class

class Push(Instruction):
    """
    PUSH imm
    PUSH mem
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        operand = self.operand_decode_read(vm, self[0])
        stack = vm.stack
        if vm.sp >= len(stack):
            stack.grow(STACK_GROWSTEP)
        stack[vm.sp] = operand.copy()
        vm.sp += 1
    #-def

    def __repr__(self):
        """
        """

        return "PUSH %s" % repr(self[0])
    #-def
#-class

class Pop(Instruction):
    """
    POP n
    POP mem
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        operand = self[0]
        if not isinstance(operand, MemoryAccessNode):
            operand = self.operand_decode_read(vm, operand)
            assert isinstance(operand, HostInt), "HostInt expected."
            operand = operand.data
            assert operand > 0, "Expected positive integer."
            assert vm.sp >= operand, "Stack violation error."
            vm.sp -= operand
            return
        assert vm.sp > 0, "Stack violation error."
        vm.sp -= 1
        self.operand_decode_write(vm, operand, vm.stack[vm.sp].copy())
    #-def

    def __repr__(self):
        """
        """

        return "POP %d" % self
    #-def
#-class

class Move(Instruction):
    """
    MOVE mem, imm
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        dest, src = self
        self.operand_decode_write(
            vm, dest, self.operand_decode_read(vm, src).copy()
        )
    #-def

    def __repr__(self):
        """
        """

        return "MOVE %d, %d" % (self.op1, self.op2)
    #-def
#-class

class Typename(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp - 1
        value = stack[sp]
        assert isinstance(value, Value), "Value expected."
        stack[sp] = HostString(value.type)
    #-def

    def __repr__(self):
        """
        """

        return "TYPENAME"
    #-def
#-class

class PushNull(Push):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Push.__init__(self, Null())
    #-def

    def __repr__(self):
        """
        """

        return "PUSHNULL"
    #-def
#-class

class PushUndefined(Push):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Push.__init__(self, Undefined())
    #-def

    def __repr__(self):
        """
        """

        return "PUSHUNDEFINED"
    #-def
#-class

class PushObj(Push):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Push.__init__(self, Object())
    #-def

    def __repr__(self):
        """
        """

        return "PUSHOBJ"
    #-def
#-class

class DefVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        obj = stack[sp - 3]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 2]
        assert isinstance(name, HostString), "HostString expected."
        obj.defvar(name.data, stack[sp - 1])
        vm.sp -= 3
    #-def

    def __repr__(self):
        """
        """

        return "DEFVAR"
    #-def
#-class

class DefMetaVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        config = vm.config
        obj = stack[sp - 3]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 2]
        assert isinstance(name, HostString), "HostString expected."
        obj.defvar("%s%s" % (name.data, config.METAVAR_PREFIX), stack[sp - 1])
        vm.sp -= 3
    #-def

    def __repr__(self):
        """
        """

        return "DEFMETAVAR"
    #-def
#-class

class UndefVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        obj = stack[sp - 2]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 1]
        assert isinstance(name, HostString), "HostString expected."
        obj.undefvar(name.data)
        vm.sp -= 2
    #-def

    def __repr__(self):
        """
        """

        return "UNDEFVAR"
    #-def
#-class

class UndefMetaVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        config = vm.config
        obj = stack[sp - 2]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 1]
        assert isinstance(name, HostString), "HostString expected."
        obj.undefvar("%s%s" % (name.data, config.METAVAR_PREFIX))
        vm.sp -= 2
    #-def

    def __repr__(self):
        """
        """

        return "UNDEFMETAVAR"
    #-def
#-class

class SetVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        obj = stack[sp - 3]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 2]
        assert isinstance(name, HostString), "HostString expected."
        obj.setvar(name.data, stack[sp - 1])
        vm.sp -= 3
    #-def

    def __repr__(self):
        """
        """

        return "SETVAR"
    #-def
#-class

class SetMetaVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        config = vm.config
        obj = stack[sp - 3]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 2]
        assert isinstance(name, HostString), "HostString expected."
        obj.setvar("%s%s" % (name.data, config.METAVAR_PREFIX), stack[sp - 1])
        vm.sp -= 3
    #-def

    def __repr__(self):
        """
        """

        return "SETMETAVAR"
    #-def
#-class

class GetVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        obj = stack[sp - 2]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 1]
        assert isinstance(name, HostString), "HostString expected."
        stack[sp - 2] = obj.getvar(name.data)
        vm.sp -= 1
    #-def

    def __repr__(self):
        """
        """

        return "GETVAR"
    #-def
#-class

class GetMetaVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        config = vm.config
        obj = stack[sp - 2]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 1]
        assert isinstance(name, HostString), "HostString expected."
        stack[sp - 2] = obj.getvar("%s%s" % (name.data, config.METAVAR_PREFIX))
        vm.sp -= 1
    #-def

    def __repr__(self):
        """
        """

        return "GETMETAVAR"
    #-def
#-class

class HasVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        obj = stack[sp - 2]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 1]
        assert isinstance(name, HostString), "HostString expected."
        stack[sp - 2] = HostBool(obj.hasvar(name.data))
        vm.sp -= 1
    #-def

    def __repr__(self):
        """
        """

        return "HASVAR"
    #-def
#-class

class HasMetaVar(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        config = vm.config
        obj = stack[sp - 2]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 1]
        assert isinstance(name, HostString), "HostString expected."
        stack[sp - 2] = HostBool(
            obj.hasvar("%s%s" % (name.data, config.METAVAR_PREFIX))
        )
        vm.sp -= 1
    #-def

    def __repr__(self):
        """
        """

        return "HASMETAVAR"
    #-def
#-class

class Bind(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        obj = stack[sp - 3]
        assert isinstance(obj, Object), "Object expected."
        name = stack[sp - 2]
        assert isinstance(name, HostString), "HostString expected."
        f = stack[sp - 1]
        assert isinstance(f, Pointer), "Pointer expected."
        obj.bind(name.data, f)
        vm.sp -= 3
    #-def

    def __repr__(self):
        """
        """

        return "BIND"
    #-def
#-class

class Clear(Instruction):
    """
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        stack = vm.stack
        sp = vm.sp
        obj = stack[sp - 1]
        assert isinstance(obj, Object), "Object expected."
        obj.clear()
        vm.sp -= 1
    #-def

    def __repr__(self):
        """
        """

        return "CLEAR"
    #-def
#-class

class Send(Instruction):
    """
    SEND imm, imm, imm
    SEND
    """
    __slots__ = []

    def __init__(*args):
        """
        """

        Instruction.__init__(*args)
    #-def

    def execute(self, vm):
        """
        """

        receiver, message, sender = self
        receiver = self.operand_decode_read(vm, receiver)
        assert isinstance(receiver, Object), "Object expected."
        f = receiver.getvar(MRESOLVER)(vm)
        assert isinstance(f, Undefined), \
            "%s has no member %s." % (repr(receiver), repr(message))
        assert isinstance(f, Pointer), \
            "%s.%s is not callable." % (repr(receiver), repr(message))
        stack = vm.stack
        if vm.sp >= len(stack):
            stack.grow(STACK_GROWSTEP)
        stack[vm.sp] = vm.ip + 1
        vm.sp += 1
        vm.ip = f - 1
    #-def

    def __repr__(self):
        """
        """

        return "SEND"
    #-def
#-class
