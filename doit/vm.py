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
Copyright (c) 2014 Jiří Kučera.

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

from enums import ErrorType, Exceptions

def enter(cmd):
    """
    """

    cmd.scope = Environment(cmd.parent.scope)
#-def

def leave(cmd):
    """
    """

    cmd.scope.clear()
    cmd.scope = None
#-def

def peval(cmd, ctx):
    """peval(cmd, ctx)

    Evaluate command cmd with context ctx in protected mode; that is, possibly
    raised exceptions are catched and translated to the DoIt! error format.
    """

    try:
        cmd(ctx)
    except Exception as e:
        if ctx.error[0] == ErrorType.ERR_OK:
            ctx.set_error(
                ErrorType.ERR_EXCEPTION,
                Exceptions.InternalError,
                "%s: %s" % (type(e).__name__, str(e))
            )
        # We suppose that if ctx.etype != ErrorType.ERR_OK, then the only
        # AssertionError was raised (see CommandProcessor.run()).
#-def

def geteh(ip, ehs, ncmds):
    """geteh(ip, ehs, ncmds) -> integer

    Given an instruction pointer, ip, a list of exception handlers, ehs, and
    an instruction list size, ncmds, this function return a nearest exception
    handler and return it, or return ncmds if there is no such handler in ehs.
    """

    for eh in ehs:
        if eh > ip:
            return eh
    return ncmds
#-def

class Context(object):
    """Keeps the command interpreter state.
    """
    __slots__ = [
        'configuration',
        'globals',
        'inputstack',
        'parser',
        'callstack',
        'result',
        'error',
        'traceback'
    ]

    def __init__(self):
        """Context() -> instance of Context

        Constructor.
        """

        # Interpreter settings.
        self.configuration = Configuration()
        # Global commands & variables.
        self.globals = Environment(None)
        # Inputs.
        self.inputstack = []
        # Parser.
        self.parser = None
        # Callstack.
        self.callstack = []
        # Last evaluated command result.
        self.result = None
        # Last error type, subtype, detail, and traceback
        self.clear_error()
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

    def pushinput(self, input):
        """pushinput(input)

        Store input on the top of input stack.
        """

        self.inputstack.append(input)
    #-def

    def popinput(self):
        """popinput() -> instance of Input or None

        Remove input from the top of stack and return it.
        """

        if self.inputstack:
            return self.inputstack.pop()
        return None
    #-def

    def getipos(self, offset = -1):
        """
        """

        input = self.inputstack[-1]
        return (input.name,) + input.position(offset)
    #-def

    def pushcall(self, cmdname, srcpos):
        """
        """

        self.callstack.append((cmdname, srcpos[0], srcpos[1]))
    #-def

    def popcall(self):
        """
        """

        self.callstack.pop()
    #-def

    def set_error_no_traceback(self, et, es, ed):
        """
        """

        self.error = (et, es, ed)
    #-def

    def set_error(self, et, es, ed):
        """
        """

        self.set_error_no_traceback(et, es, ed)
        self.traceback = self.callstack[:]
    #-def

    def clear_error(self):
        """
        """

        self.set_error_no_traceback(ErrorType.ERR_OK, None, "")
        self.traceback = []
    #-def
#-class

class CommandProcessor(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        self.on_enter = enter
        self.on_leave = leave
    #-def

    def run(self, ctx):
        """
        """

        ctx.pushcall(self.name(), self.position)
        self.on_enter(self)
        cmds = self.trees
        ncmds = self.ntrees
        ehs = self.ehs
        ip = 0
        while ip < ncmds:
            peval(cmds[ip].eval, ctx)
            et = ctx.error[0]
            if et == ErrorType.ERR_OK:
                ip += 1
            elif et == ErrorType.ERR_EXCEPTION:
                ip = geteh(ip, ehs, ncmds)
            elif et == ErrorType.ERR_FATAL:
                break
        self.on_leave(self)
        ctx.popcall()
        assert ctx.error[0] == ErrorType.ERR_OK
    #-def
#-class
