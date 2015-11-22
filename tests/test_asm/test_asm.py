#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_asm/test_asm.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-10-30 09:58:08 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! asm module tests.\
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
                                DoItAssemblerError

from doit.asm.asm import InstructionOperandExpression, \
                         ConstNode, RegisterNode, BinOpNode, \
                         AddNode, SubNode, MultNode, IndexNode, \
                         NodeVisitor, \
                         InstructionOperand, Instruction, \
                         AsmCommon, \
                         BufferMixinBase, DataWriterMixinBase, \
                         Section, Sections, Assembler

class Unreachable(Exception):
    pass

class UndefinedSymbol(Exception):
    pass

class R0(RegisterNode):
    __slots__ = []

    def __init__(self):
        RegisterNode.__init__(self)
    #-def
#-class

class R1(RegisterNode):
    __slots__ = []

    def __init__(self):
        RegisterNode.__init__(self)
    #-def
#-class

class ExpressionCompiler(NodeVisitor):
    __slots__ = [ '__stack' ]

    def __init__(self):
        NodeVisitor.__init__(self)
        self.__stack = []
    #-def

    def __call__(self, node):
        if isinstance(node, R0):
            self.__stack.append("R0")
        elif isinstance(node, R1):
            self.__stack.append("R1")
        elif isinstance(node, int):
            self.__stack.append("%d" % node)
        elif isinstance(node, AddNode):
            op2 = self.__stack.pop()
            op1 = self.__stack[-1]
            self.__stack[-1] = "%s + %s" % (op1, op2)
        elif isinstance(node, SubNode):
            op2 = self.__stack.pop()
            op1 = self.__stack[-1]
            self.__stack[-1] = "%s - %s" % (op1, op2)
        elif isinstance(node, MultNode):
            op2 = self.__stack.pop()
            op1 = self.__stack[-1]
            self.__stack[-1] = "%s*%s" % (op1, op2)
        elif isinstance(node, IndexNode):
            op2 = self.__stack.pop()
            op1 = self.__stack[-1]
            self.__stack[-1] = "%s[%s]" % (op1, op2)
        else:
            raise Unreachable()
    #-def

    def result(self):
        assert len(self.__stack) == 1
        return self.__stack[-1]
    #-def
#-class

class DummySections(Sections):
    __slots__ = []

    def __init__(self, creator):
        Sections.__init__(self, creator)
    #-def
#-class

class DummyAsm(Assembler):
    __slots__ = []

    def __init__(self):
        Assembler.__init__(self)
    #-def

    def create_sections(self):
        return DummySections(self)
    #-def
#-class

class FooBufferMixin(BufferMixinBase):
    __slots__ = []

    def __init__(self):
        BufferMixinBase.__init__(self)
    #-def

    def __setitem__(self, index, data):
        self.data_[index] = data
    #-def

    def __getitem__(self, index):
        return self.data_[index]
    #-def

    def __len__(self):
        return len(self.data_)
    #-def

    def data(self):
        return self.data_
    #-def
#-class

class FooSectionBase(FooBufferMixin, Section):
    __slots__ = [ 'data_' ]

    def __init__(self, creator, name, properties):
        FooBufferMixin.__init__(self)
        Section.__init__(self, creator, name, properties)
        self.data_ = []
    #-def

    def label(self, name):
        sectsobj = self.creator()
        sectsobj.set_scope(name)
        sectsobj.add_symbol(name, self, self.size())
        return self
    #-def

    def on_end_section(self):
        sz = self.size()
        for k in self.properties():
            self.data_.append("%s: %d" % (k, self.properties()[k]))
        self.data_.append(".size: %d" % sz)
        self.data_.append(".end_%s" % self.name())
    #-def
#-class

class FooLabel(object):
    __slots__ = [ 'label' ]

    def __init__(self, section, label):
        self.label = section.creator().full_symbol_name(label)
    #-def
#-class

class FooSection(FooSectionBase):
    __slots__ = []

    def __init__(self, creator, name, properties):
        FooSectionBase.__init__(self, creator, name, properties)
    #-def

    def foo(self):
        self.data_.append("FOO")
        return self
    #-def

    def jfoo(self, label):
        self.data_.append("JFOO")
        self.data_.append(FooLabel(self, label))
        return self
    #-def
#-class

class BarSection(FooSectionBase):
    __slots__ = []

    def __init__(self, creator, name, properties):
        FooSectionBase.__init__(self, creator, name, properties)
    #-def

    def bar(self):
        self.data_.append("BAR")
        return self
    #-def

    def jbar(self, label):
        self.data_.append("JBAR")
        self.data_.append(FooLabel(self, label))
        return self
    #-def
#-class

class FooAsmSections(Sections):
    name2section = {
      ".foo": FooSection,
      ".bar": BarSection
    }
    __slots__ = [ '__base' ]

    def __init__(self, creator):
        Sections.__init__(self, creator)
        self.__base = 0
    #-def

    def on_end(self):
        sects = self.sections()
        syms = self.symbols()
        for secname in sects:
            i = 0
            sec = sects[secname]
            while i < len(sec):
                if isinstance(sec[i], FooLabel):
                    l = sec[i].label
                    if l not in syms:
                        raise UndefinedSymbol(l)
                    symsec, sympos = syms[l]
                    origin = symsec.properties()['.org']
                    sec[i] = "%d" % (origin + sympos)
                i += 1
            #-while
        #-def
    #-def

    def on_section(self, name, properties):
        sects = self.sections()
        last = None
        if len(sects) > 1:
            last = tuple(sects.values())[-2]
        if not last:
            self.__base = 0
        else:
            self.__base += self.align(last.size())
        properties['.org'] = self.__base
    #-def

    @staticmethod
    def align(size, align = 256):
        return (size + align - 1) & ~(align - 1)
    #-def

    def create_section(self, name, properties):
        if name not in self.__class__.name2section:
            raise UndefinedSection(name)
        return self.__class__.name2section[name](self, name, properties)
    #-def
#-class

class FooAsm(Assembler):
    __slots__ = []

    def __init__(self):
        Assembler.__init__(self)
    #-def

    def on_start(self):
        self.sections().clear()
    #-def

    def create_sections(self):
        return FooAsmSections(self)
    #-def
#-class

class TestInstructionOperandExpressionCase(unittest.TestCase):

    def test_traverse_is_not_implemented(self):
        with self.assertRaises(DoItNotImplementedError):
            InstructionOperandExpression().traverse(None)
    #-def

    def test_node_visitor_methods(self):
        NodeVisitor()(None)
    #-def

    def test_expression_traversing(self):
        A, B = R0(), R1()
        c = ExpressionCompiler()
        e = 7*ConstNode(4)[A[8*B[1] + 2] - 3]*6 + 5*B[A]
        e.traverse(c)
        self.assertEqual(c.result(), "7*4[R0[8*R1[1] + 2] - 3]*6 + 5*R1[R0]")
    #-def
#-class

class TestAssemblerInterfaceCase(unittest.TestCase):

    def test_instruction_operand_initialization(self):
        InstructionOperand()
    #-def

    def test_instruction_initialization(self):
        Instruction()
    #-def

    def test_asm_comment(self):
        AsmCommon().comment("hello").comment("asm")
    #-def

    def test_buffer_mixin_base_methods(self):
        bm = BufferMixinBase()

        with self.assertRaises(DoItNotImplementedError):
            bm[0] = 1
        with self.assertRaises(DoItNotImplementedError):
            bm[0]
        with self.assertRaises(DoItNotImplementedError):
            len(bm)
        with self.assertRaises(DoItNotImplementedError):
            bm.data()
    #-def

    def test_data_writer_mixin_base_methods(self):
        dwm = DataWriterMixinBase()

        with self.assertRaises(DoItNotImplementedError):
            dwm.emit(1, 2, 3)
    #-def

    def test_section_methods(self):
        name = ".dummy"
        props = {'x': 1, 'y': 2}
        sec = Section(None, name, props)

        self.assertIsNone(sec.end_section())
        sec.on_end_section()
        self.assertIsNone(sec.creator())
        self.assertIs(sec.name(), name)
        self.assertIs(sec.properties(), props)
    #-def

    def test_sections_methods(self):
        lab0 = "..start"
        lab1 = "f"
        lab2 = ".L0"
        lab02 = "%s%s" % (lab0, lab2)
        lab12 = "%s%s" % (lab1, lab2)
        sects = Sections(None)

        self.assertIsNone(sects.end())
        sects.on_end()
        sects.on_section("", {})
        with self.assertRaises(DoItNotImplementedError):
            sects.create_section("", {})
        self.assertEqual(sects.full_symbol_name(lab0), lab0)
        self.assertEqual(sects.full_symbol_name(lab1), lab1)
        self.assertEqual(sects.full_symbol_name(lab2), lab2)
        sects.set_scope(lab1)
        self.assertEqual(sects.full_symbol_name(lab0), lab0)
        self.assertEqual(sects.full_symbol_name(lab1), lab1)
        self.assertEqual(sects.full_symbol_name(lab2), lab12)
        sects.set_scope(lab2)
        self.assertEqual(sects.full_symbol_name(lab0), lab0)
        self.assertEqual(sects.full_symbol_name(lab1), lab1)
        self.assertEqual(sects.full_symbol_name(lab2), lab12)
        sects.set_scope(lab0)
        self.assertEqual(sects.full_symbol_name(lab0), lab0)
        self.assertEqual(sects.full_symbol_name(lab1), lab1)
        self.assertEqual(sects.full_symbol_name(lab2), lab02)
        sects.set_scope("")
        self.assertEqual(sects.full_symbol_name(lab0), lab0)
        self.assertEqual(sects.full_symbol_name(lab1), lab1)
        self.assertEqual(sects.full_symbol_name(lab2), lab2)
        sects.add_symbol(lab0, 1, 2)
        with self.assertRaises(DoItAssemblerError):
            sects.add_symbol(lab0, 3, 4)
        sects.set_scope(lab0)
        sects.add_symbol(lab2, 3, 4)
        sects.add_symbol(lab1, 5, 6)
        sects.set_scope(lab1)
        sects.add_symbol(lab2, 7, 8)
        self.assertIsNone(sects.creator())
        self.assertEqual(sects.sections(), collections.OrderedDict())
        self.assertEqual(sects.symbols(), collections.OrderedDict([
            (lab0, (1, 2)),
            (lab02, (3, 4)),
            (lab1, (5, 6)),
            (lab12, (7, 8))
        ]))
    #-def

    def test_assembler_methods(self):
        asm = DummyAsm()

        with self.assertRaises(DoItNotImplementedError):
            Assembler()
        self.assertIsInstance(asm.start(), DummySections)
        asm.on_start()
        self.assertIs(asm.sections(), asm.start())
    #-def

    def test_assembler(self):
        asm = FooAsm()

        asm.start() \
          .section(".foo") \
            .comment("Foo section") \
              .foo() \
              .jfoo("..start") \
              .jfoo("..start.next") \
            .label("fence").comment("5") \
              .foo() \
              .jfoo("zmem.l0") \
              .foo() \
            .label(".l0").comment("9") \
              .jfoo("zmem") \
              .foo() \
              .jfoo("fence") \
              .jfoo(".l0") \
              .jfoo("fence.l0") \
            .label("zmem").comment("18") \
              .foo() \
            .label(".l0").comment("19") \
              .foo() \
              .jfoo(".l1") \
              .jfoo(".l0") \
              .foo() \
            .label(".l1").comment("25") \
              .foo() \
          .end_section() \
          .section(".bar") \
              .bar() \
              .bar() \
              .jbar("fence") \
              .jbar("zmem.l1") \
            .label("..start").comment("6") \
              .bar() \
            .label(".next").comment("7") \
          .end_section() \
        .end()
        sections = asm.sections().sections()

        self.assertEqual(len(sections), 2)

        code = sections[".foo"].data() + sections[".bar"].data()

        self.assertEqual(code, [
            "FOO",
            "JFOO", "%d" % (256 + 6),
            "JFOO", "%d" % (256 + 7),
            "FOO",
            "JFOO", "%d" % (19),
            "FOO",
            "JFOO", "%d" % (18),
            "FOO",
            "JFOO", "%d" % (5),
            "JFOO", "%d" % (9),
            "JFOO", "%d" % (9),
            "FOO",
            "FOO",
            "JFOO", "%d" % (25),
            "JFOO", "%d" % (19),
            "FOO",
            "FOO",
            ".org: 0",
            ".size: 26",
            ".end_.foo",
            "BAR",
            "BAR",
            "JBAR", "%d" % (5),
            "JBAR", "%d" % (25),
            "BAR",
            ".org: 256",
            ".size: 7",
            ".end_.bar"
        ])

        # Test clear:
        scope = asm.sections().scope()
        symbols = asm.sections().symbols()
        self.assertGreater(len(sections), 0)
        self.assertNotEqual(asm.sections().scope(), "")
        self.assertGreater(len(symbols), 0)
        asm.start() \
          .section(".foo") \
            .label("memcmp") \
            .foo() \
          .end_section() \
        .end()
        self.assertEqual(len(sections), 0)
        self.assertNotEqual(asm.sections().scope(), "")
        self.assertEqual(len(symbols), 0)
        asm.sections().clear()
        self.assertEqual(asm.sections().scope(), "")

        # Test reinitialize:
        asm.start() \
          .section(".bar") \
            .label("xcall") \
              .bar() \
          .end_section() \
        .end()
        sections = asm.sections().sections()
        symbols = asm.sections().symbols()
        self.assertGreater(len(sections), 0)
        self.assertNotEqual(asm.sections().scope(), "")
        self.assertGreater(len(symbols), 0)
        asm.sections().reinitialize()
        self.assertGreater(len(sections), 0)
        self.assertGreater(len(symbols), 0)
        sections = asm.sections().sections()
        symbols = asm.sections().symbols()
        self.assertEqual(len(sections), 0)
        self.assertEqual(asm.sections().scope(), "")
        self.assertEqual(len(symbols), 0)

        with self.assertRaises(DoItAssemblerError):
            asm.start() \
              .section(".foo") \
              .end_section() \
              .section(".foo") \
              .end_section() \
            .end()
        with self.assertRaises(DoItAssemblerError):
            asm.start() \
              .section(".bar") \
                .label("l1") \
                .label("l1") \
              .end_section() \
            .end()
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInstructionOperandExpressionCase))
    suite.addTest(unittest.makeSuite(TestAssemblerInterfaceCase))
    return suite
#-def
