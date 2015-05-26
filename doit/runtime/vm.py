#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/runtime/vm.py
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

class Code(Memory, DoItAssembler):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Memory.__init__(self)
        DoItAssembler.__init__(self)
        self.used = self.membot
    #-def

    def emit(self, inst):
        """
        """

        if self.used >= self.memtop:
            self.sbrk(self.memtop + self.growstep)
        self[self.used] = inst
        self.used += 1
    #-def
#-class

class Interpreter(object):
    """
    """
    __slots__ = [ 'code' ]

    def __init__(self):
        """
        """

        # Frontend:
        self.globals = Object()
        self.locals = self.globals
        self.inputs = Inputs()
        # Backend:
        self.data = Memory()
        self.stack = Memory()
        self.sp = 0
        self.fp = 0
        self.ip = Pointer(self.code, 0)
    #-def

    def run(self, function):
        """
        """

        self.ip = function
        self.status = RUNNING
        while self.status == RUNNING:
            inst = self.ip.read()
            try:
                inst.execute(self)
            except AssertionError as e:
                ...
            self.ip += 1
    #-def
#-class
