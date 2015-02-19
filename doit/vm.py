#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/vm.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-06-07 15:37:52 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! virtual machine.\
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

import errors
from enums import InstructionCode

class Stack(list):
    """Evaluation stack.
    """
    __slots__ = [ 'sp', 'fp' ]

    def __init__(*args):
        """Stack(...) -> instance of Stack

        Constructor.
        """

        list.__init__(*args)
        self = args[0]
        self.sp = 0
        self.fp = 0
    #-def

    def push(self, value):
        """
        """

        list.append(self, value)
        self.sp += 1
    #-def

    def pop(self):
        """
        """

        list.pop(self)
        self.sp -= 1
    #-def
#-class

class Context(object):
    """Keeps the command interpreter state.
    """
    __slots__ = [ 'globals', 'locals', 'inputs', 'stack', 'vm' ]

    def __init__(self):
        """Context() -> instance of Context

        Constructor.
        """

        # Commands & variables.
        self.globals = Environment(None)
        self.locals = self.globals
        # Inputs.
        self.inputs = Inputs()
        # Evaluation stack.
        self.stack = Stack()
        # Interpreter.
        self.vm = Interpreter(self)
    #-def

    def newgvar(self, name, value = None):
        """newgvar(name[, value = None])

        Define new or change global variable.
        """

        self.globals.newvar(name, value)
    #-def

    def setgvar(self, var):
        """
        """

        self.globals.setvar(var)
    #-def

    def getgvar(self, name):
        """
        """

        return self.globals.getvar(name)
    #-def

    def getipos(self, offset = -1):
        """
        """

        input = self.inputstack[-1]
        return (input.name,) + input.position(offset)
    #-def
#-class

class Instruction(tuple):
    """
    """
    __slots__ = [ 'opcode', 'op1', 'op2' ]

    def __init__(self, opcode, op1 = None, op2 = None):
        """
        """

        tuple.__init__(self, [opcode, op1, op2])
        self.opcode = opcode
        self.op1 = op1
        self.op2 = op2
    #-def
#-class

class Interpreter(object):
    """
    """
    __slots__ = [ '__context' ]

    def __init__(self, ctx):
        """
        """

        self.__context = ctx
        self.__stack = self.__context.stack
        self.__cmpresult = 0
        self.__retval = Null()
        self.__code = []
        self.__codesize = 0
        self.__ip = 0
    #-def

    def safe_push(self, a, b):
        """
        """

        self.check_type(a, Value)
        self.fast_push(a, b)
    #-def

    def fast_push(self, a, b):
        """
        """

        self.__stack.push(a)
    #-def

    def safe_pop(self, a, b):
        """
        """

        self.check_type(a, int)
        self.check(a > 0)
        self.check_stack_space(a)
        while a > 0:
            self.check_type(self.__stack[-1], Value)
            self.__stack.pop()
            a -= 1
    #-def

    def fast_pop(self, a, b):
        """
        """

        while a > 0:
            self.__stack.pop()
            a -= 1
    #-def

    def safe_move(self, a, b):
        """
        """

        self.check_type(a, int)
        self.check_type(b, int)
        self.check(a >= 0 and b >= 0)
        self.check_stack_space(a + 1)
        self.check_stack_space(b + 1)
        self.check_type(self.__stack[a], Value)
        self.check_type(self.__stack[b], Value)
        self.fast_move(a, b)
    #-def

    def fast_move(self, a, b):
        """
        """

        self.__stack[a] = self.__stack[b]
    #-def

    def safe_pushfrom(self, a, b):
        """
        """

        self.check_type(a, int)
        self.check(a >= 0)
        self.check_stack_space(a + 1)
        self.check_type(self.__stack[a], Value)
        self.fast_pushfrom(a, b)
    #-def

    def fast_pushfrom(self, a, b):
        """
        """

        self.__stack.push(self.__stack[a])
    #-def

    def safe_popto(self, a, b):
        """
        """

        self.check_type(a, int)
        self.check(a >= 0)
        self.check_stack_space(a + 1)
        self.check_type(self.__stack[a], Value)
        self.fast_popto(a, b)
    #-def

    def fast_popto(self, a, b):
        """
        """

        self.__stack[a] = self.__stack[-1]
        self.__stack.pop()
    #-def

    def safe_pushfromvar(self, a, b):
        """
        """

        self.check_type(a, str)
        self.check_localvar(a)
        self.check_type(self.__context.locals[a], Item)
        self.safe_push(self.__context.locals[a].value, b)
    #-def

    def fast_pushfromvar(self, a, b):
        """
        """

        self.__stack.push(self.__context.locals[a].value)
    #-def

    def safe_poptovar(self, a, b):
        """
        """

        self.check_type(a, str)
        self.check_localvar(a)
        self.check_type(self.__context.locals[a], Item)
        self.check_type(self.__context.locals[a].value, Value)
        self.fast_poptovar(a, b)
    #-def

    def fast_poptovar(self, a, b):
        """
        """

        self.__context.locals[a].value = self.__stack[-1]
        self.__stack.pop()
    #-def

    def safe_load(self, a, b):
        """
        """

        self.check_type(a, int)
        self.check(a >= 0)
        self.check_stack_space(a + 1)
        self.check_type(self.__stack[a], Value)
        self.check_type(b, str)
        self.check_localvar(b)
        self.check_type(self.__context.locals[b], Item)
        self.check_type(self.__context.locals[b].value, Value)
        self.fast_load(a, b)
    #-def

    def fast_load(self, a, b):
        """
        """

        self.__stack[a] = self.__context.locals[b].value
    #-def

    def safe_store(self, a, b):
        """
        """

        self.check_type(a, int)
        self.check(a >= 0)
        self.check_stack_space(a + 1)
        self.check_type(self.__stack[a], Value)
        self.check_type(b, str)
        self.check_localvar(b)
        self.check_type(self.__context.locals[b], Item)
        self.check_type(self.__context.locals[b].value, Value)
        self.fast_store(a, b)
    #-def

    def fast_store(self, a, b):
        """
        """

        self.__context.locals[b].value = self.__stack[a]
    #-def

    def safe_apicall(self, a, b):
        """
        """

        self.check_type(a, str)
        self.check_localvar(a)
        self.check_type(self.__context.locals[a], Item)
        self.check_callable(self.__context.locals[a].value)
        self.fast_apicall(a, b)
    #-def

    def fast_apicall(self, a, b):
        """
        """

        self.__context.locals[a].value(self.__context)
    #-def

    def run(self, code):
        """
        """

        self.__code = code
        self.__codesize = len(self.__code)
        self.__ip = 0
        while self.__ip < self.__codesize:
            name, a, b = self.__code[self.__ip]
            inst = self.__iset.get(name, None)
            if inst is None:
                raise errors.RuntimeError(
                    name, self.__ip, "Invalid instruction"
                )
            inst(a, b)
            self.__ip += 1
    #-def

    def check_type(self, v, t):
        """
        """

        if not isinstance(v, t):
            raise errors.RuntimeError(
                self.__code[self.__ip].opcode.name(),
                self.__ip,
                "Instruction operand must be %s" % t.__class__.__name__
            )
    #-def

    def check_localvar(self, name):
        """
        """

        if self.__context.locals[name] is None:
            raise errors.RuntimeError(
                self.__code[self.__ip].opcode.name(),
                self.__ip,
                "Undefined variable '%s'" % name
            )
    #-def

    def check_stack_space(self, n):
        """
        """

        if self.__stack.sp < n:
            raise errors.RuntimeError(
                self.__code[self.__ip].opcode.name(),
                self.__ip,
                "Bad index to stack. Access denied"
            )
    #-def

    def check(self, cond):
        """
        """

        if not cond:
            raise errors.RuntimeError(
                self.__code[self.__ip].opcode.name(),
                self.__ip,
                "Bad instruction operand"
            )
    #-def

    def __initialize_tables(self, safemode):
        """
        """

        self.__iset = {
            InstructionCode.PUSH:
                safemode and self.safe_push or self.fast_push,
            InstructionCode.POP:
                safemode and self.safe_pop or self.fast_pop,
            InstructionCode.MOVE:
                safemode and self.safe_move or self.fast_move,
            InstructionCode.PUSHFROM:
                safemode and self.safe_pushfrom or self.fast_pushfrom,
            InstructionCode.POPTO:
                safemode and self.safe_popto or self.fast_popto,
            InstructionCode.PUSHFROMVAR:
                safemode and self.safe_pushvar or self.fast_pushvar,
            InstructionCode.POPTOVAR:
                safemode and self.safe_popvar or self.fast_popvar,
            InstructionCode.LOAD:
                safemode and self.safe_load or self.fast_load,
            InstructionCode.STORE:
                safemode and self.safe_store or self.fast_store,
            InstructionCode.APICALL:
                safemode and self.safe_apicall or self.fast_apicall
        }
    #-def

    def run(self, code):
        """
        """

        ctx = self.__context
        stack = ctx.stack
        clen = len(code)
        ip = 0
        while ip < clen:
            name, a, b = code[ip]
            # =================================================================
            # == INSTRUCTION PROCESSING
            # -----------------------------------------------------------------
            # -- A) Stack manipulation:
            if name is InstructionCode.PUSH:
                # PUSH a
                # ; Push value `a' onto the stack.
                if not isinstance(a, Value):
                    return vm_error(ctx, name, ip,\
                        "Only values can be pushed onto the evaluation stack"\
                    )
                stack.push(a)
            elif name is InstructionCode.POP:
                # POP n
                # ; Pop `n' values out of the stack.
                if stack.sp < a:
                    return vm_error(ctx, name, ip, "Empty stack")
                while a > 0:
                    if not isinstance(stack[-1], Value):
                        return vm_error(ctx, name, ip, "Access denied")
                    stack.pop()
                #-while
            elif name is InstructionCode.MOVE:
                # MOVE a, b
                # ; Move value from `stack[b]' to `stack[a]'.
                if stack.sp <= a or stack.sp <= b or a < 0 or b < 0\
                or not isinstance(stack[a], Value)\
                or not isinstance(stack[b], Value):
                    return vm_error(ctx, name, ip, "Access denied")
                stack[a] = stack[b]
            elif name is InstructionCode.PUSHVAR\
            or name is InstructionCode.POPVAR\
            or name is InstructionCode.LOAD\
            or name is InstructionCode.STORE:
                # PUSHVAR var
                # ; Push the value from variable `var' onto the stack.
                # POPVAR var
                # ; Pop the value from the stack and store it to variable
                # ; `var'.
                # LOAD a, var
                # ; Load value of variable `var' to `stack[a]'.
                # STORE a, var
                # ; Store value at `stack[a]' to variable `var'.
                if name is InstructionCode.LOAD\
                or name is InstructionCode.STORE:
                    if stack.sp <= a or a < 0\
                    or not isinstance(stack[a], Value):
                        return vm_error(ctx, name, ip, "Access denied")
                    varname = b
                else:
                    varname = a
                ###
                if isinstance(varname, Value):
                    varname = varname.data()
                if not isinstance(varname, str):
                    return vm_error(ctx, name, ip,\
                        "Variable name must be a string value"\
                    )
                var = ctx.locals.getvar(varname)
                if var is None:
                    return vm_error(ctx, name, ip,\
                        "Undefined variable '%s'" % varname\
                    )
                ###
                if name is InstructionCode.PUSHVAR:
                    stack.push(var.getvalue())
                elif name is InstructionCode.POPVAR:
                    if stack.sp < 1:
                        return vm_error(ctx, name, ip, "Empty stack")
                    if not isinstance(stack[-1], Value):
                        return vm_error(ctx, name, ip, "Access denied")
                    var.setvalue(stack[-1])
                    stack.pop()
                elif name is InstructionCode.LOAD:
                    stack[a] = var.getvalue()
                elif name is InstructionCode.STORE:
                    var.setvalue(stack[a])
                else:
                    return vm_error(ctx, name, ip, "Unexpected instruction")
            # -----------------------------------------------------------------
            # -- B) Values manipulation:
            elif name is InstructionCode.TYPE:
                # TYPE
                # ; Extract the type of the value of the top item onto
                # ; the stack.
                if stack.sp < 1:
                    return vm_error(ctx, name, ip, "Empty stack")
                if not isinstance(stack[-1], Value):
                    return vm_error(ctx, name, ip, "Access denied")
                stack[-1] = HostString(stack[-1].type())
            # -----------------------------------------------------------------
            # -- C) Variables manipulation:
            elif name is InstructionCode.GETVAR\
            or name is InstructionCode.HASVAR:
                # GETVAR
                # ; Get the reference to variable.
                # HASVAR
                # ; Set the conditional flag to true if variable is defined.
                if stack.sp < 1:
                    return vm_error(ctx, name, ip, "Empty stack")
                if not isinstance(stack[-1], HostString):
                    return vm_error(ctx, name, ip, "HostString expected")
                var = ctx.locals.getvar(stack[-1].data())
                if name is InstructionCode.GETVAR:
                    stack[-1] = var and Reference(var) or Null()
                elif name is InstructionCode.HASVAR:
                    self.__cmpflag = var and 1 or 0
                    stack.pop()
                else:
                    return vm_error(ctx, name, ip, "Unexpected instruction")
            elif name is InstructionCode.SETVAR:
                # SETVAR
                # ; Set the variable from reference.
                if stack.sp < 1:
                    return vm_error(ctx, name, ip, "Empty stack")
                if not isinstance(stack[-1], Reference):
                    return vm_error(ctx, name, ip, "Reference expected")
                ctx.locals.setvar(stack[-1].data())
                stack.pop()
            # -----------------------------------------------------------------
            # -- D) Member variables manipulation:
            elif name is InstructionCode.GETMVAR\
            or name is InstructionCode.HASMVAR:
                # GETMVAR
                # ; Get the reference to member variable.
                # HASMVAR
                # ; Set the conditional flag to true if member variable
                # ; is defined.
                if stack.sp < 2:
                    return vm_error(ctx, name, ip, "Empty stack")
                if not isinstance(stack[-2], Object):
                    return vm_error(ctx, name, ip, "Object expected")
                if not isinstance(stack[-1], HostString):
                    return vm_error(ctx, name, ip, "HostString expected")
                mvar = stack[-2].get(stack[-1].data())
                stack.pop()
                if name is InstructionCode.GETMVAR:
                    stack[-1] = mvar and Reference(mvar) or Null()
                elif name is InstructionCode.HASMVAR:
                    self.__cmpflag = mvar and 1 or 0
                    stack.pop()
                else:
                    return vm_error(ctx, name, ip, "Unexpected instruction")
            elif name is InstructionCode.SETMVAR:
                # SETMVAR
                # ; Set the member variable from reference.
                if stack.sp < 2:
                    return vm_error(ctx, name, ip, "Empty stack")
                if not isinstance(stack[-2], Object):
                    return vm_error(ctx, name, ip, "Object expected")
                if not isinstance(stack[-1], Reference):
                    return vm_error(ctx, name, ip, "Reference expected")
                stack[-2][stack[-1].data().name()] = stack[-1].data()
                stack.pop()
                stack.pop()
            elif name is InstructionCode.GETMACS:
            elif name is InstructionCode.GETOWNER:
            elif name is Instruction.SEND:
            elif name is Instruction.JUMP:
            elif name is Instruction.JCOND:
            elif name is Instruction.SET:
            elif name is Instruction.RESET:
            elif name is Instruction.CALL:
            elif name is Instruction.ECALL:
            elif name is Instruction.ENTER:
            elif name is Instruction.LEAVE:
            elif name is Instruction.RETURN:
            elif name is Instruction.PUSHSCOPE:
            elif name is Instruction.POPSCOPE:
            elif name is Instruction.THROW:
            elif name is Instruction.VMID:
            elif name is Instruction.HALT:
            else:
                return vm_error(ctx, "Invalid instruction at [ip = %d]." % ip)
            ##############################
            ip += 1
        #-while
        return 0
    #-def
#-class
