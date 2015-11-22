#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_asm/test_doit_asm.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-10-30 00:30:18 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! doit_asm module tests.\
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

import collections
import unittest

from doit.support.errors import DoItNotImplementedError, \
                                DoItRuntimeError, \
                                DoItLinkerError
from doit.runtime.memory import Memory

from doit.asm.doit_asm import DoItInstructionOperand, \
                              Register, BaseRegister, \
                              SegmentRegister, DetectSegmentRegister, \
                              RegisterCS, RegisterDS, RegisterSS, \
                              RegisterSP, RegisterFP, \
                              Immediate, BasePlusOffset, MemoryLocation

class FooVm(object):
    __slots__ = [ 'cs', 'ds', 'ss', 'sp', 'fp' ]

    def __init__(self):
        self.cs = Memory()
        self.cs.sbrk(16)
        self.ds = Memory()
        self.ds.sbrk(16)
        self.ss = Memory()
        self.ss.sbrk(16)
        self.sp = 0
        self.fp = 0
        for i in range(0, 16):
            self.cs[i] = 256 + i
            self.ds[i] = 512 + i
            self.ss[i] = 1024 + i
    #-def
#-class

class TestDoItInstructionOperandCase(unittest.TestCase):

    def test_doit_instruction_operand_methods(self):
        iop = DoItInstructionOperand()

        with self.assertRaises(DoItNotImplementedError):
            iop.setval(None, None)
        with self.assertRaises(DoItNotImplementedError):
            iop.getval(None)
        iop.update(None)
        self.assertFalse(iop.is_immediate())
    #-def
#-class

class TestRegistersCase(unittest.TestCase):

    def test_registers(self):
        Register(), BaseRegister(), SegmentRegister(), DetectSegmentRegister()
        cs, ds, ss = RegisterCS(), RegisterDS(), RegisterSS()
        sp, fp = RegisterSP(), RegisterFP()
        mcs, mds, mss = Memory(), Memory(), Memory()
        mcs.sbrk(1), mds.sbrk(1), mss.sbrk(1)
        mcs[0] = 1; mds[0] = 2; mss[0] = 3
        vm = FooVm()

        cs.setval(vm, mcs)
        with self.assertRaises(DoItRuntimeError):
            cs.setval(vm, None)
        self.assertIs(cs.getval(vm), mcs)
        ds.setval(vm, mds)
        with self.assertRaises(DoItRuntimeError):
            ds.setval(vm, None)
        self.assertIs(ds.getval(vm), mds)
        ss.setval(vm, mss)
        with self.assertRaises(DoItRuntimeError):
            ss.setval(vm, None)
        self.assertIs(ss.getval(vm), mss)
        sp.setval(vm, 4)
        with self.assertRaises(DoItRuntimeError):
            sp.setval(vm, None)
        self.assertEqual(sp.getval(vm), 4)
        fp.setval(vm, 5)
        with self.assertRaises(DoItRuntimeError):
            fp.setval(vm, None)
        self.assertEqual(fp.getval(vm), 5)
    #-def
#-class

class TestInstructionOperandsCase(unittest.TestCase):

    def test_immediate_methods(self):
        symbols = collections.OrderedDict([
          ("memcmp", (".code", 0, None)),
          ("memcmp.loop", (".code", 23, None)),
          ("print", (".code", 64, None)),
          ("print.print_int", (".code", 151, None)),
          ("print.print_str", (".code", 223, None)),
          ("hextab", (".data", 0, None)),
          ("msgtab", (".data", 16, None)),
          ("msgtab.m1", (".data", 16, None)),
          ("msgtab.m2", (".data", 52, None))
        ])

        i = Immediate("", 0)
        self.assertTrue(i.is_immediate())
        self.assertEqual(i.getval(None), 0)
        i.update(symbols)
        self.assertEqual(i.getval(None), 0)

        i = Immediate("msgtab.m2", 0)
        self.assertEqual(i.getval(None), 0)
        i.update(symbols)
        self.assertEqual(i.getval(None), 52)

        i = Immediate("", -1)
        self.assertEqual(i.getval(None), 0)
        i.update(symbols)
        self.assertEqual(i.getval(None), -1)

        i = Immediate("print.print_str", -1)
        self.assertEqual(i.getval(None), 0)
        i.update(symbols)
        self.assertEqual(i.getval(None), 222)

        i = Immediate("print", 2)              # 64  +   2 = 66
        i += Immediate("", 43)                 # 66  +  43 = 109
        i -= Immediate("memcmp.loop", 0)       # 109 -  23 = 86
        i -= Immediate("", 1)                  # 86  -   1 = 85
        i -= Immediate("", -2)                 # 85  +   2 = 87
        i += Immediate("", 0)                  # 87  +   0 = 87
        i -= Immediate("", 0)                  # 87  -   0 = 87
        i += Immediate("print.print_int", 10)  # 87  + 161 = 248
        self.assertEqual(i.getval(None), 0)
        i.update(symbols)
        self.assertEqual(i.getval(None), 248)

        i = Immediate("", 0)
        i += Immediate("hextab", 1)
        i += Immediate("msgtab.m2", 0)
        i += Immediate("msgtab.m2", 0)
        i -= Immediate("msgtab.m2", 0)
        i += Immediate("msgtab", 0)
        i += Immediate("msgtab", 0)
        i += Immediate("msgtab", 0)
        i -= Immediate("", 36)
        i += Immediate("", -1)
        i.update(symbols)
        self.assertEqual(i.getval(None), 64)

        i = Immediate("msgtab", 1)
        i -= Immediate("memcmp", 2)
        with self.assertRaises(DoItLinkerError):
            i.update(symbols)

        i = Immediate("memcpy", 0)
        with self.assertRaises(DoItLinkerError):
            i.update(symbols)

        i = Immediate("msgtab", 3)
        with self.assertRaises(DoItLinkerError):
            i.update({})
    #-def

    def test_base_plus_offset_methods(self):
        symbols = collections.OrderedDict([
          ("xsym", (".xsec", 3, None)),
          ("ysym", (".xsec", 4, None)),
          ("zsym", (".xsec", 5, None))
        ])
        vm = FooVm()
        vm.sp = 2
        sp = RegisterSP()
        bpo = BasePlusOffset(sp, Immediate("xsym", 1))
        bpo += Immediate("ysym", 2)
        bpo -= Immediate("zsym", 3)
        bpo.update(symbols)

        self.assertEqual(bpo.getval(vm), 4)
    #-def

    def test_memory_location_methods(self):
        ml = MemoryLocation(RegisterDS(), Immediate("", 1))
        ml.update({})
        vm = FooVm()

        self.assertEqual(ml.getval(vm), 513)
        ml.setval(vm, -6)
        self.assertEqual(ml.getval(vm), -6)
    #-def
#-class

class TestInsOpCompilerCase(unittest.TestCase):

    def test_instruction_operand_compiler(self):
        ...
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDoItInstructionOperandCase))
    suite.addTest(unittest.makeSuite(TestRegistersCase))
    suite.addTest(unittest.makeSuite(TestInstructionOperandsCase))
    return suite
#-def
