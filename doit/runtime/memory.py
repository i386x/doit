#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/runtime/memory.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-04-14 20:16:23 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! VM's memory.\
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

class Memory(list):
    """
    """
    __slots__ = [ 'membot', 'memtop' ]

    def __init__(self):
        """
        """

        list.__init__(self, [])
        self.membot = 0
        self.memtop = len(self)
    #-def

    def sbrk(self, brk):
        """
        """

        assert brk >= self.membot, "Invalid memory break value (%d)." % brk
        if brk > len(self):
            list.extend(self, [None]*(brk - len(self)))
        self.memtop = brk
    #-def

    def __setitem__(self, i, v):
        """
        """

        assert i >= self.membot and i < self.memtop, \
            "Memory write error at %d." % i
        list.__setitem__(self, i - self.membot, v)
    #-def

    def __getitem__(self, i):
        """
        """

        assert i >= self.membot and i < self.memtop, \
            "Memory read error at %d." % i
        return list.__getitem__(self, i - self.membot)
    #-def
#-class
