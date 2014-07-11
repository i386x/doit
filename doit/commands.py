#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-02-27 20:35:32 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! commands.\
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

from vm import CommandProcessor
from lang import AbstractSyntaxTree

def is_exception_handler(cmd):
    """
    """

    return isinstance(cmd, ExceptionHandler)
#-def

def freevars(cmd):
    """
    """
#-def

def substitute(ctx, cmd):
    """
    """

    substitues = cmd.get_substitues([])
#-def

class Command(CommandProcessor, AbstractSyntaxTree):
    """
    """
    __slots__ = [ 'scope', 'ehs' ]

    def __init__(self, parent, pos):
        """
        """

        AbstractSyntaxTree.__init__(self, parent, pos)
        CommandProcessor.__init__(self)
        self.scope = parent.scope
        self.ehs = []
    #-def

    def name(self):
        """
        """

        raise NotImplementedError
    #-def

    def add_command(self, cmd):
        """
        """

        self.add_tree(command)
        if is_exception_handler(command):
            self.ehs.append(self.ntrees - 1)
    #-def

    def eval(self, ctx):
        """
        """

        raise NotImplementedError
    #-def

    def get_freevars(self, varnames):
        """
        """

        return []
    #-def
#-class

class ExceptionHandler(Command):
    """
    """
    __slots__ = []

    def __init__(self, pos):
        """
        """

        Command.__init__(self, pos)
    #-def
#-class

class UserDefinedCommand(Command):
    """
    """
    __slots__ = []

    def __init__(self, parent, pos, name, argspec, body):
        """
        """

        Command.__init__(self, parent, pos)
        self.__name = name
        self.__argspec = argspec
        self.__body = body
    #-def

    def eval(self, ctx):
        """
        """

        # Precondition: all free variables are now substituted.
        # Evaluate arguments.
        for i in range(self.ntrees):
            self.trees[i].run(ctx):
            self.scope.newvar(self.__argspec.argnames[i], ctx.result)
        # Run the commands in body.
        self.__body.run(ctx)
    #-def
#-class

@buildin_command
class DefCommand(Command):
    """
    """
    __slots__ = []

    def __init__(self, parent, pos):
        """
        """

        Command.__init__(self, parent, pos)
    #-def

    def name(self):
        """
        """

        return ":"
    #-def

    def eval(self, ctx):
        """
        """

        # 1st subtree is command name
        cmd_name = substitute(ctx, self.trees[0])
        # 2nd subtree is arguments parser
        arg_parser = substitute(ctx, self.trees[1])
        # 3rd subtree is list of commands
        cmd_list = substitute(ctx, self.trees[2])
        # Define new, or redefine old, command
        cmd = UserDefinedCommand()
    #-def
#-class
