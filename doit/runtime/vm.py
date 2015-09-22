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

from doit.support.errors import ERROR_UNKNOWN, DoItError, doit_assert
from doit.support.utils import Collection
from doit.runtime.memory import Memory

_assert = doit_assert

Collection.unlock()

STOPPED = Collection('VM').Status.STOPPED
RUNNING = Collection('VM').Status.RUNNING
ABORTED = Collection('VM').Status.ABORTED

Collection.lock()

ZF = 1 << 0
SF = 1 << 1
EF = 1 << 2

class Interpreter(object):
    """The `DoIt!` virtual machine.

    Member variables:

    * `cs` (:class:`Memory <doit.runtime.memory.Memory>`) -- code segment
    * `ds` (:class:`Memory <doit.runtime.memory.Memory>`) -- data segment
    * `ss` (:class:`Memory <doit.runtime.memory.Memory>`) -- stack segment
    * `sp` (:class:`int`) -- stack pointer
    * `fp` (:class:`int`) -- frame pointer
    * `ip` (:class:`int`) -- instruction pointer
    * `flags` (:class:`int`) -- execution flags
    * `status` (:class:`Collection <doit.support.utils.Collection>`) -- the \
        state of virtual machine
    * `eh` (:class:`int`) -- error handler pointer
    """
    __slots__ = []

    def __init__(self):
        """Initializes the virtual machine.
        """

        self.cs = Memory()
        self.ds = Memory()
        self.ss = Memory()
        self.sp = 0
        self.fp = 0
        self.ip = 0
        self.flags = 0
        self.status = STOPPED
        self.eh = 0
    #-def

    def run(self):
        """Starts the virtual machine.
        """

        self.status = RUNNING
        while self.status is RUNNING:
            try:
                self.cs[self.ip].execute(self)
            except DoItError as e:
                self.__raise(e.errcode, e.detail)
            except:
                self.__abort()
            self.ip += 1
        #-while
    #-def

    def __raise(self, ecode, emsg):
        """Raises an exception on the virtual machine level.

        :param int ecode: An error code.
        :param str emsg: An error message.
        """

        try:
            _assert((self.flags & EF) == 0, "Error flag (EF) is set")
            ss = self.ss
            sp = self.sp
            ss[sp] = self.flags
            ss[sp + 1] = self.ip
            ss[sp + 2] = self.fp
            ss[sp + 3] = sp
            ss[sp + 4] = ss
            ss[sp + 5] = self.ds
            ss[sp + 6] = self.cs
            ss[sp + 7] = emsg
            ss[sp + 8] = ecode
            # Next instruction - 1
            ss[sp + 9] = self.ip
            ss[sp + 10] = self.fp
            self.sp += 11
            self.fp = self.sp
            self.ip = self.eh - 1
            self.flags |= EF
        except DoItError as e:
            self.__abort(e.errcode, e.detail)
        except:
            self.__abort()
    #-def

    def __abort(self, ecode = ERROR_UNKNOWN, emsg = "Mysteriously aborted"):
        """Abnormally aborts the virtual machine.

        :param int ecode: An error code.
        :param str emsg: An error message.
        """

        self.status = ABORTED
        self.ip -= 1
        self.on_abort(ecode, emsg)
    #-def

    def on_abort(self, ecode, emsg):
        """Called when virtual machine is abnormally aborted.

        :param int ecode: An error code.
        :param str emsg: An error message.
        """

        pass
    #-def
#-class

del _assert
