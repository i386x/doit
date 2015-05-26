#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/asm/doit_asm.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-04-22 13:16:12 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
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

class RegisterSP(BaseRegister):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        BaseRegister.__init__(self)
    #-def

    def eval(self, env):
        """
        """

        return env.sp
    #-def
#-class

class RegisterFP(BaseRegister):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        BaseRegister.__init__(self)
    #-def

    def eval(self, env):
        """
        """

        return env.fp
    #-def
#-class

class RegisterDS(SegmentRegister):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        SegmentRegister.__init__(self)
    #-def

    def eval(self, env):
        """
        """

        return env.data
    #-def
#-class

class RegisterSS(SegmentRegister):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        SegmentRegister.__init__(self)
    #-def

    def eval(self, env):
        """
        """

        return env.stack
    #-def
#-class

class DoItAssembler(AbstractAssembler):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        AbstractAssembler.__init__(self)
        self.sp = RegisterSP()
        self.fp = RegisterFP()
        self.ds = RegisterDS()
        self.ss = RegisterSS()
    #-def

    def push(self, *args):
        """
        """

        self.emit(Push(*args))
    #-def
#-class
