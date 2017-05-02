#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/test_utils/test_tagengine.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2017-02-27 22:42:23 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Tag engine tests.\
"""

__license__ = """\
Copyright (c) 2014 - 2017 Jiří Kučera.

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

import unittest

from ....common import OPEN_FAIL, OpenContext

from doit.support.errors import DoItAssertionError

from doit.text.pgen.utils.tagengine import \
    OT_IMM, OT_REG, OT_STK, \
    TES_IDLE, TES_RUNNING, TES_PAUSED, TES_HALTED, TES_ERROR, \
    TagAbstractInput, TagTextInput, TagMatcher, \
    TagCommand, \
    Fail, \
    MatchSymbol, MatchAny, MatchWord, MatchSet, MatchRange, MatchIf, \
    MatchAtLeastOneSymbol, MatchAtLeastOneFromSet, MatchAtLeastOneFromRange, \
        MatchAtLeastOne, \
    MatchAtMostOneSymbol, MatchAtMostOneFromSet, MatchAtMostOneFromRange, \
        MatchAtMostOne, \
    MatchManySymbols, MatchManyFromSet, MatchManyFromRange, MatchAll, \
        MatchMany, \
    TestEof, TestSymbol, TestSet, TestRange, TestIf, \
    Branch, \
    SkipSymbol, SkipAny, SkipSet, SkipRange, SkipIf, \
    SkipAtLeastOneSymbol, SkipAtLeastOneFromSet, SkipAtLeastOneFromRange, \
        SkipAtLeastOne, \
    SkipAtMostOneSymbol, SkipAtMostOneFromSet, SkipAtMostOneFromRange, \
        SkipAtMostOne, \
    SkipManySymbols, SkipManyFromSet, SkipManyFromRange, SkipAll, SkipMany, \
    SkipTo, SkipToSet, SkipToRange, SkipUntilNot, \
    Push, PushMatch, PopMatch, Swap, \
    Operator, Concat, Join, \
    JTrue, JFalse, Jump, Call, ECall, Return, \
    Pause, Halt, \
    TagProgramEnvironment, TagProgram, \
    TagEngine, \
    TIC_UNUSED, TIC_SYMBOL, TIC_META, TIC_MATCH, \
    TagICElement, TagICMacro, TagICLabel, \
    TagICSymbolFactory, TagICSymbolTable, \
    TagICCompiler, \
    ACC, STK, \
    SYMBOL, SET, RANGE, DEFAULT, EOF, NULL, \
    FAIL, \
    MATCH, MATCH_ANY, MATCH_1N, MATCH_PLUS, MATCH_01, MATCH_OPT, MATCH_0N, \
        MATCH_MANY, MATCH_ALL, \
    TEST_EOF, TEST, BRANCH, \
    SKIP, SKIP_ANY, SKIP_1N, SKIP_PLUS, SKIP_01, SKIP_OPT, SKIP_0N, \
        SKIP_MANY, SKIP_ALL, SKIP_TO, \
    PUSH, PUSH_MATCH, POP_MATCH, SWAP, \
    CONCAT, JOIN, \
    JTRUE, JFALSE, JUMP, CALL, ECALL, RETURN, \
    PAUSE, HALT

class TestTagAbstractInputCase(unittest.TestCase):

    def test_interface(self):
        tai = TagAbstractInput()

        tai.peek()
        tai.peekn(1)
        tai.next()
        tai.nextn(1)
    #-def
#-class

class TestTagTextInputCase(unittest.TestCase):

    def test_no_input_loaded(self):
        ti1 = TagTextInput()
        ti2 = TagTextInput()

        self.assertEqual(ti1.peek(), (None, None))
        self.assertEqual(ti2.peekn(3), [])
        ti1.next()
        ti2.nextn(3)
        self.assertEqual(ti1.peek(), (None, None))
        self.assertEqual(ti2.peekn(3), [])
    #-def

    def test_input_from_string(self):
        ti = TagTextInput()

        ti.load_data_from_string("")
        self.assertEqual(ti.peek(), (None, None))
        ti.next()
        self.assertEqual(ti.peek(), (None, None))

        ti.load_data_from_string("")
        self.assertEqual(ti.peekn(2), "")
        ti.nextn(2)
        self.assertEqual(ti.peekn(2), "")
        self.assertEqual(ti.peekn(1), "")
        self.assertEqual(ti.peek(), (None, None))

        ti.load_data_from_string("abc")
        self.assertEqual(ti.peek(), ('a', 'a'))
        self.assertEqual(ti.peek(), ('a', 'a'))
        ti.next()
        self.assertEqual(ti.peek(), ('b', 'b'))
        self.assertEqual(ti.peek(), ('b', 'b'))
        self.assertEqual(ti.peek(), ('b', 'b'))
        ti.next()
        self.assertEqual(ti.peek(), ('c', 'c'))
        self.assertEqual(ti.peek(), ('c', 'c'))
        self.assertEqual(ti.peek(), ('c', 'c'))
        self.assertEqual(ti.peek(), ('c', 'c'))
        ti.next()
        self.assertEqual(ti.peek(), (None, None))
        self.assertEqual(ti.peek(), (None, None))
        self.assertEqual(ti.peek(), (None, None))
        self.assertEqual(ti.peek(), (None, None))
        ti.next()
        self.assertEqual(ti.peek(), (None, None))
        self.assertEqual(ti.peek(), (None, None))
        self.assertEqual(ti.peek(), (None, None))
        self.assertEqual(ti.peek(), (None, None))

        ti.load_data_from_string("abcdef")
        self.assertEqual(ti.peekn(4), "abcd")
        self.assertEqual(ti.peekn(3), "abc")
        self.assertEqual(ti.peekn(6), "abcdef")
        self.assertEqual(ti.peekn(7), "abcdef")
        self.assertEqual(ti.peekn(8), "abcdef")
        self.assertEqual(ti.peekn(16), "abcdef")
        self.assertEqual(ti.peek(), ("a", "a"))
        ti.nextn(2)
        self.assertEqual(ti.peekn(4), "cdef")
        self.assertEqual(ti.peekn(3), "cde")
        self.assertEqual(ti.peekn(6), "cdef")
        self.assertEqual(ti.peekn(7), "cdef")
        self.assertEqual(ti.peekn(8), "cdef")
        self.assertEqual(ti.peekn(16), "cdef")
        self.assertEqual(ti.peek(), ("c", "c"))
        ti.nextn(3)
        self.assertEqual(ti.peekn(4), "f")
        self.assertEqual(ti.peekn(3), "f")
        self.assertEqual(ti.peekn(6), "f")
        self.assertEqual(ti.peekn(7), "f")
        self.assertEqual(ti.peekn(8), "f")
        self.assertEqual(ti.peekn(16), "f")
        self.assertEqual(ti.peek(), ("f", "f"))
        ti.nextn(4)
        self.assertEqual(ti.peekn(4), "")
        self.assertEqual(ti.peekn(3), "")
        self.assertEqual(ti.peekn(6), "")
        self.assertEqual(ti.peekn(7), "")
        self.assertEqual(ti.peekn(8), "")
        self.assertEqual(ti.peekn(16), "")
        self.assertEqual(ti.peek(), (None, None))
        ti.nextn(5)
        self.assertEqual(ti.peekn(4), "")
        self.assertEqual(ti.peekn(3), "")
        self.assertEqual(ti.peekn(6), "")
        self.assertEqual(ti.peekn(7), "")
        self.assertEqual(ti.peekn(8), "")
        self.assertEqual(ti.peekn(16), "")
        self.assertEqual(ti.peek(), (None, None))
    #-def

    def test_input_from_file(self):
        ti = TagTextInput()

        with OpenContext(0, "", False):
            self.assertTrue(ti.load_data_from_file('foo'))
        self.assertEqual(ti.peek(), (None, None))

        with OpenContext(0, "xyz", False):
            self.assertTrue(ti.load_data_from_file('bar'))
        self.assertEqual(ti.peek(), ('x', 'x'))
        ti.nextn(2)
        self.assertEqual(ti.peek(), ('z', 'z'))
        ti.next()
        self.assertEqual(ti.peek(), (None, None))
        self.assertEqual(ti.peekn(3), "")

        with OpenContext(OPEN_FAIL, "abc", False):
            self.assertFalse(ti.load_data_from_file('baz'))
    #-def
#-class

class TestTagProgramEnvironmentCase(unittest.TestCase):

    def test_tag_program_environment_members(self):
        tpe = TagProgramEnvironment()

        self.assertIsNone(tpe.engine())
        tpe.attach_engine(1)
        self.assertEqual(tpe.engine(), 1)

        tpe = TagProgramEnvironment(2)
        self.assertEqual(tpe.engine(), 2)
        tpe.attach_engine(3)
        self.assertEqual(tpe.engine(), 3)
    #-def
#-class

class TestTagProgramCase(unittest.TestCase):

    def test_tag_program_members(self):
        tp = TagProgram('lexer')

        self.assertEqual(tp.name(), 'lexer')
        self.assertIs(tp.envclass(), TagProgramEnvironment)
        self.assertEqual(tp.code(), [])

        tp = TagProgram('x1', TagProgram)

        self.assertEqual(tp.name(), 'x1')
        self.assertIs(tp.envclass(), TagProgram)
        self.assertEqual(tp.code(), [])

        tp = TagProgram('y2', self, [1, 2, 4])

        self.assertEqual(tp.name(), 'y2')
        self.assertIs(tp.envclass(), self)
        self.assertEqual(tp.code(), [1, 2, 4])
    #-def
#-class

class TestTagEngineCase(unittest.TestCase):

    def check_tag_engine_members(self, te):
        self.assertEqual(te.program_name(), "")
        self.assertIsNone(te.env())
        self.assertIsNone(te.matcher())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.naddrs(), 0)
        self.assertEqual(te.code(), [])
        self.assertEqual(te.code_size(), 0)
        self.assertEqual(te.ip(), 0)
        self.assertIsNone(te.match())
        self.assertFalse(te.match_flag())
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.last_error_detail(), "")
    #-def

    def test_tag_engine_initialization_and_reset(self):
        te = TagEngine()

        self.check_tag_engine_members(te)
    #-def

    def test_load_none(self):
        te = TagEngine()
        te.load(None)

        self.check_tag_engine_members(te)
    #-def

    def test_load_program(self):
        te = TagEngine()
        te.load(TagProgram('tagprog', code = [ 'a', 'b', 'c' ]))

        self.assertEqual(te.program_name(), 'tagprog')
        self.assertIsInstance(te.env(), TagProgramEnvironment)
        self.assertEqual(te.code(), [ 'a', 'b', 'c' ])
        self.assertEqual(te.code_size(), 3)
    #-def

    def test_ip_is_not_out_of_range(self):
        te = TagEngine()
        te.load(TagProgram('tagprog', code = [ 'a', 'b', 'c' ]))

        te.set_ip(0)
        self.assertFalse(te.ip_is_out_of_range())
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.last_error_detail(), "")

        te.set_ip(2)
        self.assertFalse(te.ip_is_out_of_range())
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.last_error_detail(), "")
    #-def

    def test_ip_is_out_of_range_1(self):
        te = TagEngine()
        te.load(TagProgram('tagprog', code = [ 'a', 'b', 'c' ]))

        te.set_ip(3)
        self.assertTrue(te.ip_is_out_of_range())
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(),
            "Invalid tag engine instruction address (3)"
        )
    #-def

    def test_ip_is_out_of_range_2(self):
        te = TagEngine()
        te.load(TagProgram('tagprog', code = [ 'a', 'b', 'c' ]))

        te.set_ip(-1)
        self.assertTrue(te.ip_is_out_of_range())
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(),
            "Invalid tag engine instruction address (-1)"
        )
    #-def

    def test_initialize_run_1(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [Halt()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")
        te.set_state(TES_ERROR)

        self.assertFalse(te.initialize_run(tti, tp))
        self.assertEqual(te.state(), TES_ERROR)
        self.assertIsNone(te.matcher())
    #-def

    def test_initialize_run_2(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [Halt()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")
        te.set_state(TES_RUNNING)

        self.assertTrue(te.initialize_run(tti, tp))
        self.assertEqual(te.state(), TES_RUNNING)
        self.assertIsNone(te.matcher())
    #-def

    def test_initialize_run_3(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [Halt()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")
        te.set_state(TES_PAUSED)

        self.assertTrue(te.initialize_run(tti, tp))
        self.assertEqual(te.state(), TES_RUNNING)
        self.assertIsNone(te.matcher())
    #-def

    def test_initialize_run_4(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [Halt()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")
        te.set_state(TES_IDLE)

        self.assertTrue(te.initialize_run(tti, tp))
        self.assertEqual(te.state(), TES_RUNNING)
        self.assertIsNotNone(te.matcher())
    #-def

    def test_initialize_run_5(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [Halt()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")
        te.set_state(TES_HALTED)

        self.assertTrue(te.initialize_run(tti, tp))
        self.assertEqual(te.state(), TES_RUNNING)
        self.assertIsNotNone(te.matcher())
    #-def

    def test_run_1(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [Halt()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")
        te.set_state(TES_ERROR)

        te.run(tti, tp)
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "")
    #-def

    def test_run_2(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")

        te.run(tti, tp)
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(),
            "Invalid tag engine instruction address (0)"
        )
    #-def

    def test_run_3(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [Halt()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")

        te.run(tti, tp)
        self.assertEqual(te.state(), TES_HALTED)
    #-def

    def test_run_4(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [MatchAny()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")

        te.run(tti, tp)
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.match(), "a")
        self.assertEqual(te.last_error_detail(),
            "Invalid tag engine instruction address (1)"
        )
    #-def

    def test_run_5(self):
        te = TagEngine()
        tp = TagProgram('stub', code = [MatchAny(), Halt()])
        tti = TagTextInput()
        tti.load_data_from_string("abrakadabra")

        te.run(tti, tp)
        self.assertEqual(te.state(), TES_HALTED)
        self.assertEqual(te.match(), "a")
    #-def

    def test_valstack(self):
        te = TagEngine()

        te.reset()
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        te.set_match("abc")
        te.push_match()
        self.assertEqual(te.match(), "abc")
        self.assertEqual(te.nvals(), 1)
        te.set_match("xyz")
        te.push_match()
        self.assertEqual(te.match(), "xyz")
        self.assertEqual(te.nvals(), 2)
        te.set_match("uvw")
        self.assertEqual(te.match(), "uvw")
        te.pop_match()
        self.assertEqual(te.match(), "xyz")
        self.assertEqual(te.nvals(), 1)
        te.pop_match()
        self.assertEqual(te.match(), "abc")
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.state(), TES_IDLE)
        te.pop_match()
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")
        te.pop_match()
        self.assertEqual(te.state(), TES_ERROR)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")

        te.reset()
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        te.pushval("abc")
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 1)
        self.assertEqual(te.topval(), "abc")
        te.set_match("def")
        te.push_match()
        self.assertEqual(te.match(), "def")
        self.assertEqual(te.nvals(), 2)
        self.assertEqual(te.topval(), "def")
        self.assertEqual(te.popval(), "def")
        self.assertEqual(te.match(), "def")
        self.assertEqual(te.nvals(), 1)
        self.assertEqual(te.topval(), "abc")
        te.pop_match()
        self.assertEqual(te.match(), "abc")
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.popval())
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")
        self.assertIsNone(te.popval())
        self.assertEqual(te.state(), TES_ERROR)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")
        self.assertIsNone(te.topval())
        self.assertEqual(te.state(), TES_ERROR)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "Top applied on empty stack")

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")
        te.swap()
        self.assertEqual(te.state(), TES_ERROR)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(),
            "Swap needs at least two items on stack"
        )

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")
        te.pushval("a")
        te.swap()
        self.assertEqual(te.state(), TES_ERROR)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 1)
        self.assertEqual(te.last_error_detail(),
            "Swap needs at least two items on stack"
        )

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")
        te.pushval("a")
        te.pushval("b")
        te.swap()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 2)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.popval(), "a")
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 1)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.popval(), "b")
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")
        te.pushval("a")
        te.pushval("b")
        te.pushval("c")
        te.swap()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 3)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.popval(), "b")
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 2)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.popval(), "c")
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 1)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.popval(), "a")
        self.assertEqual(te.state(), TES_IDLE)
        self.assertIsNone(te.match())
        self.assertEqual(te.nvals(), 0)
        self.assertEqual(te.last_error_detail(), "")
    #-def

    def test_stack(self):
        te = TagEngine()

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.naddrs(), 0)
        self.assertEqual(te.last_error_detail(), "")
        te.popaddr()
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.naddrs(), 0)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.naddrs(), 0)
        self.assertEqual(te.last_error_detail(), "")
        te.topaddr()
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.naddrs(), 0)
        self.assertEqual(te.last_error_detail(), "Top applied on empty stack")

        te.reset()
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.naddrs(), 0)
        self.assertEqual(te.last_error_detail(), "")
        te.pushaddr(1)
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.naddrs(), 1)
        self.assertEqual(te.topaddr(), 1)
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.naddrs(), 1)
        te.pushaddr(7)
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.naddrs(), 2)
        self.assertEqual(te.topaddr(), 7)
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.naddrs(), 2)
        self.assertEqual(te.popaddr(), 7)
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.naddrs(), 1)
        self.assertEqual(te.popaddr(), 1)
        self.assertEqual(te.state(), TES_IDLE)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.naddrs(), 0)
        self.assertIsNone(te.popaddr())
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")
        self.assertEqual(te.naddrs(), 0)
    #-def

    def test_set_match_flag(self):
        te = TagEngine()

        te.reset()
        self.assertFalse(te.match_flag())
        te.set_match_flag(True)
        self.assertTrue(te.match_flag())
        te.set_match_flag(False)
        self.assertFalse(te.match_flag())
    #-def

    def test_set_error_detail(self):
        te = TagEngine()

        te.reset()
        self.assertEqual(te.last_error_detail(), "")
        te.set_error_detail("error detail")
        self.assertEqual(te.last_error_detail(), "error detail")
        te.set_error_detail("detailed error detail")
        self.assertEqual(te.last_error_detail(), "detailed error detail")
        te.set_error_detail("")
        self.assertEqual(te.last_error_detail(), "")
    #-def
#-class

class TestInstructionsCase(unittest.TestCase):

    def test_matcher_initialization(self):
        ti = TagTextInput()
        ti.load_data_from_string("Xoxoxo!")
        tm = TagMatcher(ti)

        self.assertIsNone(tm.last_match())
        self.assertEqual(tm.last_error_detail(), "")
    #-def

    def test_tag_command_interface(self):
        tc = TagCommand()
        tc(TagEngine())
    #-def

    def create_and_run_tag_engine(self, s, c):
        te = TagEngine()
        ti = TagTextInput()
        ti.load_data_from_string(s)
        tp = TagProgram('itester', code = c)
        te.run(ti, tp)
        return te, ti
    #-def

    def check_match_ok(self, te, ti, m, n):
        self.assertEqual(te.state(), TES_HALTED)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.ip(), 2)
        self.assertEqual(te.match(), m)
        self.assertEqual(ti.peek(), (n, n))
        self.assertTrue(te.match_flag())
    #-def

    def check_match_ko(self, te, ti, u):
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(),
            "Unexpected input symbol %r" % u
        )
        self.assertEqual(te.ip(), 1)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), (u, u))
        self.assertFalse(te.match_flag())
    #-def

    def check_match_word_ko(self, te, ti, m, e):
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(),
            "Unexpected word %r (need %r)" % (m, e)
        )
        self.assertEqual(te.ip(), 1)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), (m[0], m[0]))
        self.assertFalse(te.match_flag())
    #-def

    def check_match_eof(self, te, ti):
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "Unexpected end of input")
        self.assertEqual(te.ip(), 1)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), (None, None))
        self.assertFalse(te.match_flag())
    #-def

    def check_match_word_eof(self, te, ti, m, e):
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(),
            "Unexpected end of input (%r matched, %r needed)" % (m, e)
        )
        self.assertEqual(te.ip(), 1)
        self.assertIsNone(te.match())
        if m:
            self.assertEqual(ti.peek(), (m[0], m[0]))
        else:
            self.assertEqual(ti.peek(), (None, None))
        self.assertFalse(te.match_flag())
    #-def

    def check_test_result(self, te, ti, r, p):
        self.assertEqual(te.state(), TES_HALTED)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.ip(), 2)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), (p, p))
        if r:
            self.assertTrue(te.match_flag())
        else:
            self.assertFalse(te.match_flag())
    #-def

    def check_branch(self, te, ti, ip, p):
        self.assertEqual(te.state(), TES_HALTED)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.ip(), ip + 1)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), (p, p))
        self.assertFalse(te.match_flag())
    #-def

    def check_skip_ok(self, te, ti, p):
        self.assertEqual(te.state(), TES_HALTED)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.ip(), 2)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), (p, p))
        self.assertTrue(te.match_flag())
    #-def

    check_skip_ko = check_match_ko

    check_skip_eof = check_match_eof

    def test_Fail(self):
        te, ti = self.create_and_run_tag_engine("uvw", [
            Fail("Bang!")
        ])

        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "Bang!")
        self.assertEqual(te.ip(), 1)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), ('u', 'u'))
        self.assertFalse(te.match_flag())
    #-def

    def test_MatchSymbol_ok(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchSymbol('a'), Halt()
        ])

        self.check_match_ok(te, ti, "a", 'b')
    #-def

    def test_MatchSymbol_ko(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchSymbol('_'), Halt()
        ])

        self.check_match_ko(te, ti, 'a')
    #-def

    def test_MatchSymbol_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchSymbol('_'), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchAny_ok(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchAny(), Halt()
        ])

        self.check_match_ok(te, ti, "a", 'b')
    #-def

    def test_MatchAny_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAny(), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchWord_ok(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchWord("ab"), Halt()
        ])

        self.check_match_ok(te, ti, "ab", 'c')
    #-def

    def test_MatchWord_ko(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchWord("ac"), Halt()
        ])

        self.check_match_word_ko(te, ti, "ab", "ac")
    #-def

    def test_MatchWord_eof_1(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchWord("abcd"), Halt()
        ])

        self.check_match_word_eof(te, ti, "abc", "abcd")
    #-def

    def test_MatchWord_eof_2(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchWord("azcd"), Halt()
        ])

        self.check_match_word_eof(te, ti, "abc", "azcd")
    #-def

    def test_MatchWord_eof_3(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchWord("zbcd"), Halt()
        ])

        self.check_match_word_eof(te, ti, "abc", "zbcd")
    #-def

    def test_MatchWord_eof_4(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchWord("zbcd"), Halt()
        ])

        self.check_match_word_eof(te, ti, "", "zbcd")
    #-def

    def test_MatchSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchSet([ 'a', 'b', 'c', 'd' ]), Halt()
        ])

        self.check_match_ok(te, ti, "a", 'b')
    #-def

    def test_MatchSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine("cbc", [
            MatchSet([ 'a', 'b', 'c', 'd' ]), Halt()
        ])

        self.check_match_ok(te, ti, "c", 'b')
    #-def

    def test_MatchSet_ko(self):
        te, ti = self.create_and_run_tag_engine("xbc", [
            MatchSet([ 'a', 'b', 'c', 'd' ]), Halt()
        ])

        self.check_match_ko(te, ti, 'x')
    #-def

    def test_MatchSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchSet([ 'a', 'b', 'c', 'd' ]), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("017", [
            MatchRange('0', '9'), Halt()
        ])

        self.check_match_ok(te, ti, "0", '1')
    #-def

    def test_MatchRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("317", [
            MatchRange('0', '9'), Halt()
        ])

        self.check_match_ok(te, ti, "3", '1')
    #-def

    def test_MatchRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("917", [
            MatchRange('0', '9'), Halt()
        ])

        self.check_match_ok(te, ti, "9", '1')
    #-def

    def test_MatchRange_ko_1(self):
        te, ti = self.create_and_run_tag_engine("0917", [
            MatchRange('1', '9'), Halt()
        ])

        self.check_match_ko(te, ti, '0')
    #-def

    def test_MatchRange_ko_2(self):
        te, ti = self.create_and_run_tag_engine("917", [
            MatchRange('0', '7'), Halt()
        ])

        self.check_match_ko(te, ti, '9')
    #-def

    def test_MatchRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchRange('0', '7'), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchIf_ok(self):
        te, ti = self.create_and_run_tag_engine("917", [
            MatchIf(lambda c: c == '9'), Halt()
        ])

        self.check_match_ok(te, ti, "9", '1')
    #-def

    def test_MatchIf_ko(self):
        te, ti = self.create_and_run_tag_engine("917", [
            MatchIf(lambda c: c == '8'), Halt()
        ])

        self.check_match_ko(te, ti, '9')
    #-def

    def test_MatchIf_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchIf(lambda c: c == 'q'), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchAtLeastOneSymbol_ok_1(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchAtLeastOneSymbol('a'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'a' ], 'b')
    #-def

    def test_MatchAtLeastOneSymbol_ok_2(self):
        te, ti = self.create_and_run_tag_engine("aabc", [
            MatchAtLeastOneSymbol('a'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'a', 'a' ], 'b')
    #-def

    def test_MatchAtLeastOneSymbol_ok_3(self):
        te, ti = self.create_and_run_tag_engine("aaabc", [
            MatchAtLeastOneSymbol('a'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'a', 'a', 'a' ], 'b')
    #-def

    def test_MatchAtLeastOneSymbol_ko(self):
        te, ti = self.create_and_run_tag_engine("xaabc", [
            MatchAtLeastOneSymbol('a'), Halt()
        ])

        self.check_match_ko(te, ti, 'x')
    #-def

    def test_MatchAtLeastOneSymbol_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAtLeastOneSymbol('a'), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchAtLeastOneFromSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine("bxs", [
            MatchAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'b' ], 'x')
    #-def

    def test_MatchAtLeastOneFromSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine("bcxs", [
            MatchAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'b', 'c' ], 'x')
    #-def

    def test_MatchAtLeastOneFromSet_ok_3(self):
        te, ti = self.create_and_run_tag_engine("bcaxs", [
            MatchAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'b', 'c', 'a' ], 'x')
    #-def

    def test_MatchAtLeastOneFromSet_ko(self):
        te, ti = self.create_and_run_tag_engine("xbcaxs", [
            MatchAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_match_ko(te, ti, 'x')
    #-def

    def test_MatchAtLeastOneFromSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchAtLeastOneFromRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("1_", [
            MatchAtLeastOneFromRange('1', '9'), Halt()
        ])

        self.check_match_ok(te, ti, [ '1' ], '_')
    #-def

    def test_MatchAtLeastOneFromRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("91_", [
            MatchAtLeastOneFromRange('1', '9'), Halt()
        ])

        self.check_match_ok(te, ti, [ '9', '1' ], '_')
    #-def

    def test_MatchAtLeastOneFromRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("971_", [
            MatchAtLeastOneFromRange('1', '9'), Halt()
        ])

        self.check_match_ok(te, ti, [ '9', '7', '1' ], '_')
    #-def

    def test_MatchAtLeastOneFromRange_ko(self):
        te, ti = self.create_and_run_tag_engine("0_", [
            MatchAtLeastOneFromRange('1', '9'), Halt()
        ])

        self.check_match_ko(te, ti, '0')
    #-def

    def test_MatchAtLeastOneFromRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAtLeastOneFromRange('1', '9'), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchAtLeastOne_ok_1(self):
        te, ti = self.create_and_run_tag_engine("abc", [
            MatchAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'a' ], 'b')
    #-def

    def test_MatchAtLeastOne_ok_2(self):
        te, ti = self.create_and_run_tag_engine("aabc", [
            MatchAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'a', 'a' ], 'b')
    #-def

    def test_MatchAtLeastOne_ok_3(self):
        te, ti = self.create_and_run_tag_engine("aaabc", [
            MatchAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'a', 'a', 'a' ], 'b')
    #-def

    def test_MatchAtLeastOne_ko(self):
        te, ti = self.create_and_run_tag_engine("xaabc", [
            MatchAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_match_ko(te, ti, 'x')
    #-def

    def test_MatchAtLeastOne_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_match_eof(te, ti)
    #-def

    def test_MatchAtMostOneSymbol_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            MatchAtMostOneSymbol('a'), Halt()
        ])

        self.check_match_ok(te, ti, [], '_')
    #-def

    def test_MatchAtMostOneSymbol_ok_2(self):
        te, ti = self.create_and_run_tag_engine("a_", [
            MatchAtMostOneSymbol('a'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'a' ], '_')
    #-def

    def test_MatchAtMostOneSymbol_ok_3(self):
        te, ti = self.create_and_run_tag_engine("aa_", [
            MatchAtMostOneSymbol('a'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'a' ], 'a')
    #-def

    def test_MatchAtMostOneSymbol_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAtMostOneSymbol('a'), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_MatchAtMostOneFromSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            MatchAtMostOneFromSet([ 'a', 'b' ]), Halt()
        ])

        self.check_match_ok(te, ti, [], '_')
    #-def

    def test_MatchAtMostOneFromSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine("b_", [
            MatchAtMostOneFromSet([ 'a', 'b' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'b' ], '_')
    #-def

    def test_MatchAtMostOneFromSet_ok_3(self):
        te, ti = self.create_and_run_tag_engine("ba_", [
            MatchAtMostOneFromSet([ 'a', 'b' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'b' ], 'a')
    #-def

    def test_MatchAtMostOneFromSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAtMostOneFromSet([ 'a', 'b' ]), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_MatchAtMostOneFromRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            MatchAtMostOneFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [], '_')
    #-def

    def test_MatchAtMostOneFromRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("g_", [
            MatchAtMostOneFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'g' ], '_')
    #-def

    def test_MatchAtMostOneFromRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("gz_", [
            MatchAtMostOneFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'g' ], 'z')
    #-def

    def test_MatchAtMostOneFromRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAtMostOneFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_MatchAtMostOne_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            MatchAtMostOne(lambda c: c == 'x'), Halt()
        ])

        self.check_match_ok(te, ti, [], '_')
    #-def

    def test_MatchAtMostOne_ok_2(self):
        te, ti = self.create_and_run_tag_engine("x_", [
            MatchAtMostOne(lambda c: c == 'x'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'x' ], '_')
    #-def

    def test_MatchAtMostOne_ok_3(self):
        te, ti = self.create_and_run_tag_engine("xy_", [
            MatchAtMostOne(lambda c: c == 'x'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'x' ], 'y')
    #-def

    def test_MatchAtMostOne_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAtMostOne(lambda c: c == 'x'), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_MatchManySymbols_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            MatchManySymbols('d'), Halt()
        ])

        self.check_match_ok(te, ti, [], '_')
    #-def

    def test_MatchManySymbols_ok_2(self):
        te, ti = self.create_and_run_tag_engine("d_", [
            MatchManySymbols('d'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'd' ], '_')
    #-def

    def test_MatchManySymbols_ok_3(self):
        te, ti = self.create_and_run_tag_engine("dd_", [
            MatchManySymbols('d'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'd', 'd' ], '_')
    #-def

    def test_MatchManySymbols_ok_4(self):
        te, ti = self.create_and_run_tag_engine("ddd_", [
            MatchManySymbols('d'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'd', 'd', 'd' ], '_')
    #-def

    def test_MatchManySymbols_ok_5(self):
        te, ti = self.create_and_run_tag_engine("ddd", [
            MatchManySymbols('d'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'd', 'd', 'd' ], None)
    #-def

    def test_MatchManySymbols_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchManySymbols('d'), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_MatchManyFromSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            MatchManyFromSet([ 'u', 'w' ]), Halt()
        ])

        self.check_match_ok(te, ti, [], '_')
    #-def

    def test_MatchManyFromSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine("w_", [
            MatchManyFromSet([ 'u', 'w' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'w' ], '_')
    #-def

    def test_MatchManyFromSet_ok_3(self):
        te, ti = self.create_and_run_tag_engine("wu_", [
            MatchManyFromSet([ 'u', 'w' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'w', 'u' ], '_')
    #-def

    def test_MatchManyFromSet_ok_4(self):
        te, ti = self.create_and_run_tag_engine("wuw_", [
            MatchManyFromSet([ 'u', 'w' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'w', 'u', 'w' ], '_')
    #-def

    def test_MatchManyFromSet_ok_5(self):
        te, ti = self.create_and_run_tag_engine("wuww", [
            MatchManyFromSet([ 'u', 'w' ]), Halt()
        ])

        self.check_match_ok(te, ti, [ 'w', 'u', 'w', 'w' ], None)
    #-def

    def test_MatchManyFromSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchManyFromSet([ 'u', 'w' ]), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_MatchManyFromRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            MatchManyFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [], '_')
    #-def

    def test_MatchManyFromRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("h_", [
            MatchManyFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'h' ], '_')
    #-def

    def test_MatchManyFromRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("he_", [
            MatchManyFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'h', 'e' ], '_')
    #-def

    def test_MatchManyFromRange_ok_4(self):
        te, ti = self.create_and_run_tag_engine("hex_", [
            MatchManyFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'h', 'e', 'x' ], '_')
    #-def

    def test_MatchManyFromRange_ok_5(self):
        te, ti = self.create_and_run_tag_engine("quad", [
            MatchManyFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'q', 'u', 'a', 'd' ], None)
    #-def

    def test_MatchManyFromRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchManyFromRange('a', 'z'), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_MatchAll_ok_1(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchAll(), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_MatchAll_ok_2(self):
        te, ti = self.create_and_run_tag_engine(".", [
            MatchAll(), Halt()
        ])

        self.check_match_ok(te, ti, [ '.' ], None)
    #-def

    def test_MatchAll_ok_3(self):
        te, ti = self.create_and_run_tag_engine(".|", [
            MatchAll(), Halt()
        ])

        self.check_match_ok(te, ti, [ '.', '|' ], None)
    #-def

    def test_MatchAll_ok_4(self):
        te, ti = self.create_and_run_tag_engine(".|\n", [
            MatchAll(), Halt()
        ])

        self.check_match_ok(te, ti, [ '.', '|', '\n' ], None)
    #-def

    def test_MatchMany_ok_1(self):
        te, ti = self.create_and_run_tag_engine("u", [
            MatchMany(lambda c: c == 'f'), Halt()
        ])

        self.check_match_ok(te, ti, [], 'u')
    #-def

    def test_MatchMany_ok_2(self):
        te, ti = self.create_and_run_tag_engine("fu", [
            MatchMany(lambda c: c == 'f'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'f' ], 'u')
    #-def

    def test_MatchMany_ok_3(self):
        te, ti = self.create_and_run_tag_engine("ffu", [
            MatchMany(lambda c: c == 'f'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'f', 'f' ], 'u')
    #-def

    def test_MatchMany_ok_4(self):
        te, ti = self.create_and_run_tag_engine("fffu", [
            MatchMany(lambda c: c == 'f'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'f', 'f', 'f' ], 'u')
    #-def

    def test_MatchMany_ok_5(self):
        te, ti = self.create_and_run_tag_engine("ffff", [
            MatchMany(lambda c: c == 'f'), Halt()
        ])

        self.check_match_ok(te, ti, [ 'f', 'f', 'f', 'f' ], None)
    #-def

    def test_MatchMany_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            MatchMany(lambda c: c == 'f'), Halt()
        ])

        self.check_match_ok(te, ti, [], None)
    #-def

    def test_TestEof_1(self):
        te, ti = self.create_and_run_tag_engine("a", [
            TestEof(), Halt()
        ])

        self.check_test_result(te, ti, False, 'a')
    #-def

    def test_TestEof_2(self):
        te, ti = self.create_and_run_tag_engine("", [
            TestEof(), Halt()
        ])

        self.check_test_result(te, ti, True, None)
    #-def

    def test_TestSymbol_1(self):
        te, ti = self.create_and_run_tag_engine("a", [
            TestSymbol('a'), Halt()
        ])

        self.check_test_result(te, ti, True, 'a')
    #-def

    def test_TestSymbol_2(self):
        te, ti = self.create_and_run_tag_engine("x", [
            TestSymbol('a'), Halt()
        ])

        self.check_test_result(te, ti, False, 'x')
    #-def

    def test_TestSymbol_3(self):
        te, ti = self.create_and_run_tag_engine("", [
            TestSymbol('a'), Halt()
        ])

        self.check_test_result(te, ti, False, None)
    #-def

    def test_TestSet_1(self):
        te, ti = self.create_and_run_tag_engine("a", [
            TestSet([ 'a', 'b' ]), Halt()
        ])

        self.check_test_result(te, ti, True, 'a')
    #-def

    def test_TestSet_2(self):
        te, ti = self.create_and_run_tag_engine("b", [
            TestSet([ 'a', 'b' ]), Halt()
        ])

        self.check_test_result(te, ti, True, 'b')
    #-def

    def test_TestSet_3(self):
        te, ti = self.create_and_run_tag_engine("c", [
            TestSet([ 'a', 'b' ]), Halt()
        ])

        self.check_test_result(te, ti, False, 'c')
    #-def

    def test_TestSet_4(self):
        te, ti = self.create_and_run_tag_engine("", [
            TestSet([ 'a', 'b' ]), Halt()
        ])

        self.check_test_result(te, ti, False, None)
    #-def

    def test_TestRange_1(self):
        te, ti = self.create_and_run_tag_engine("1_", [
            TestRange('1', '5'), Halt()
        ])

        self.check_test_result(te, ti, True, '1')
    #-def

    def test_TestRange_2(self):
        te, ti = self.create_and_run_tag_engine("3_", [
            TestRange('1', '5'), Halt()
        ])

        self.check_test_result(te, ti, True, '3')
    #-def

    def test_TestRange_3(self):
        te, ti = self.create_and_run_tag_engine("5_", [
            TestRange('1', '5'), Halt()
        ])

        self.check_test_result(te, ti, True, '5')
    #-def

    def test_TestRange_4(self):
        te, ti = self.create_and_run_tag_engine("0_", [
            TestRange('1', '5'), Halt()
        ])

        self.check_test_result(te, ti, False, '0')
    #-def

    def test_TestRange_5(self):
        te, ti = self.create_and_run_tag_engine("7_", [
            TestRange('1', '5'), Halt()
        ])

        self.check_test_result(te, ti, False, '7')
    #-def

    def test_TestRange_6(self):
        te, ti = self.create_and_run_tag_engine("", [
            TestRange('1', '5'), Halt()
        ])

        self.check_test_result(te, ti, False, None)
    #-def

    def test_TestIf_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            TestIf(lambda c: c == '.'), Halt()
        ])

        self.check_test_result(te, ti, False, '_')
    #-def

    def test_TestIf_2(self):
        te, ti = self.create_and_run_tag_engine("._", [
            TestIf(lambda c: c == '.'), Halt()
        ])

        self.check_test_result(te, ti, True, '.')
    #-def

    def test_TestIf_3(self):
        te, ti = self.create_and_run_tag_engine("", [
            TestIf(lambda c: c == '.'), Halt()
        ])

        self.check_test_result(te, ti, False, None)
    #-def

    def test_Branch_1(self):
        te, ti = self.create_and_run_tag_engine("a_", [
            Branch({ 'a': 3, 'b': 4, 'c': 5 }, 6, 7), Halt(), Halt(), Halt(),
            Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.check_branch(te, ti, 3, 'a')
    #-def

    def test_Branch_2(self):
        te, ti = self.create_and_run_tag_engine("b_", [
            Branch({ 'a': 3, 'b': 4, 'c': 5 }, 6, 7), Halt(), Halt(), Halt(),
            Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.check_branch(te, ti, 4, 'b')
    #-def

    def test_Branch_3(self):
        te, ti = self.create_and_run_tag_engine("c_", [
            Branch({ 'a': 3, 'b': 4, 'c': 5 }, 6, 7), Halt(), Halt(), Halt(),
            Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.check_branch(te, ti, 5, 'c')
    #-def

    def test_Branch_4(self):
        te, ti = self.create_and_run_tag_engine("_", [
            Branch({ 'a': 3, 'b': 4, 'c': 5 }, 6, 7), Halt(), Halt(), Halt(),
            Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.check_branch(te, ti, 6, '_')
    #-def

    def test_Branch_5(self):
        te, ti = self.create_and_run_tag_engine("", [
            Branch({ 'a': 3, 'b': 4, 'c': 5 }, 6, 7), Halt(), Halt(), Halt(),
            Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.check_branch(te, ti, 7, None)
    #-def

    def test_SkipSymbol_ok(self):
        te, ti = self.create_and_run_tag_engine("a_", [
            SkipSymbol('a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipSymbol_ko(self):
        te, ti = self.create_and_run_tag_engine("ba_", [
            SkipSymbol('a'), Halt()
        ])

        self.check_skip_ko(te, ti, 'b')
    #-def

    def test_SkipSymbol_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipSymbol('a'), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipAny_ok(self):
        te, ti = self.create_and_run_tag_engine("..", [
            SkipAny(), Halt()
        ])

        self.check_skip_ok(te, ti, '.')
    #-def

    def test_SkipAny_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAny(), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine(".#", [
            SkipSet([ ';', '.' ]), Halt()
        ])

        self.check_skip_ok(te, ti, '#')
    #-def

    def test_SkipSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine(";#", [
            SkipSet([ ';', '.' ]), Halt()
        ])

        self.check_skip_ok(te, ti, '#')
    #-def

    def test_SkipSet_ko(self):
        te, ti = self.create_and_run_tag_engine("7.#", [
            SkipSet([ ';', '.' ]), Halt()
        ])

        self.check_skip_ko(te, ti, '7')
    #-def

    def test_SkipSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipSet([ ';', '.' ]), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("a_", [
            SkipRange('a', 'g'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("e_", [
            SkipRange('a', 'g'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("g_", [
            SkipRange('a', 'g'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipRange_ko_1(self):
        te, ti = self.create_and_run_tag_engine("@_", [
            SkipRange('a', 'g'), Halt()
        ])

        self.check_skip_ko(te, ti, '@')
    #-def

    def test_SkipRange_ko_2(self):
        te, ti = self.create_and_run_tag_engine("h_", [
            SkipRange('a', 'g'), Halt()
        ])

        self.check_skip_ko(te, ti, 'h')
    #-def

    def test_SkipRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipRange('a', 'g'), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipIf_ok(self):
        te, ti = self.create_and_run_tag_engine("@_", [
            SkipIf(lambda c: c == '@'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipIf_ko(self):
        te, ti = self.create_and_run_tag_engine("*_", [
            SkipIf(lambda c: c == '@'), Halt()
        ])

        self.check_skip_ko(te, ti, '*')
    #-def

    def test_SkipIf_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipIf(lambda c: c == '@'), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipAtLeastOneSymbol_ok_1(self):
        te, ti = self.create_and_run_tag_engine("ab", [
            SkipAtLeastOneSymbol('a'), Halt()
        ])

        self.check_skip_ok(te, ti, 'b')
    #-def

    def test_SkipAtLeastOneSymbol_ok_2(self):
        te, ti = self.create_and_run_tag_engine("aab", [
            SkipAtLeastOneSymbol('a'), Halt()
        ])

        self.check_skip_ok(te, ti, 'b')
    #-def

    def test_SkipAtLeastOneSymbol_ok_3(self):
        te, ti = self.create_and_run_tag_engine("aaab", [
            SkipAtLeastOneSymbol('a'), Halt()
        ])

        self.check_skip_ok(te, ti, 'b')
    #-def

    def test_SkipAtLeastOneSymbol_ko(self):
        te, ti = self.create_and_run_tag_engine("xaaab", [
            SkipAtLeastOneSymbol('a'), Halt()
        ])

        self.check_skip_ko(te, ti, 'x')
    #-def

    def test_SkipAtLeastOneSymbol_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAtLeastOneSymbol('a'), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipAtLeastOneFromSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine("ax", [
            SkipAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_skip_ok(te, ti, 'x')
    #-def

    def test_SkipAtLeastOneFromSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine("bax", [
            SkipAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_skip_ok(te, ti, 'x')
    #-def

    def test_SkipAtLeastOneFromSet_ok_3(self):
        te, ti = self.create_and_run_tag_engine("cbax", [
            SkipAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_skip_ok(te, ti, 'x')
    #-def

    def test_SkipAtLeastOneFromSet_ko(self):
        te, ti = self.create_and_run_tag_engine("pcbax", [
            SkipAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_skip_ko(te, ti, 'p')
    #-def

    def test_SkipAtLeastOneFromSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAtLeastOneFromSet([ 'a', 'b', 'c' ]), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipAtLeastOneFromRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("1.", [
            SkipAtLeastOneFromRange('1', '7'), Halt()
        ])

        self.check_skip_ok(te, ti, '.')
    #-def

    def test_SkipAtLeastOneFromRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("51.", [
            SkipAtLeastOneFromRange('1', '7'), Halt()
        ])

        self.check_skip_ok(te, ti, '.')
    #-def

    def test_SkipAtLeastOneFromRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("571.", [
            SkipAtLeastOneFromRange('1', '7'), Halt()
        ])

        self.check_skip_ok(te, ti, '.')
    #-def

    def test_SkipAtLeastOneFromRange_ko_1(self):
        te, ti = self.create_and_run_tag_engine("0571.", [
            SkipAtLeastOneFromRange('1', '7'), Halt()
        ])

        self.check_skip_ko(te, ti, '0')
    #-def

    def test_SkipAtLeastOneFromRange_ko_2(self):
        te, ti = self.create_and_run_tag_engine("90571.", [
            SkipAtLeastOneFromRange('1', '7'), Halt()
        ])

        self.check_skip_ko(te, ti, '9')
    #-def

    def test_SkipAtLeastOneFromRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAtLeastOneFromRange('1', '7'), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipAtLeastOne_ok_1(self):
        te, ti = self.create_and_run_tag_engine("a_", [
            SkipAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtLeastOne_ok_2(self):
        te, ti = self.create_and_run_tag_engine("aa_", [
            SkipAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtLeastOne_ok_3(self):
        te, ti = self.create_and_run_tag_engine("aaa_", [
            SkipAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtLeastOne_ko(self):
        te, ti = self.create_and_run_tag_engine("xaaa_", [
            SkipAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_skip_ko(te, ti, 'x')
    #-def

    def test_SkipAtLeastOne_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAtLeastOne(lambda c: c == 'a'), Halt()
        ])

        self.check_skip_eof(te, ti)
    #-def

    def test_SkipAtMostOneSymbol_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipAtMostOneSymbol('a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtMostOneSymbol_ok_2(self):
        te, ti = self.create_and_run_tag_engine("a_", [
            SkipAtMostOneSymbol('a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtMostOneSymbol_ok_3(self):
        te, ti = self.create_and_run_tag_engine("aa_", [
            SkipAtMostOneSymbol('a'), Halt()
        ])

        self.check_skip_ok(te, ti, 'a')
    #-def

    def test_SkipAtMostOneSymbol_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAtMostOneSymbol('a'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipAtMostOneFromSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipAtMostOneFromSet(['a', 'b']), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtMostOneFromSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine("a_", [
            SkipAtMostOneFromSet(['a', 'b']), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtMostOneFromSet_ok_3(self):
        te, ti = self.create_and_run_tag_engine("b_", [
            SkipAtMostOneFromSet(['a', 'b']), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtMostOneFromSet_ok_4(self):
        te, ti = self.create_and_run_tag_engine("ab_", [
            SkipAtMostOneFromSet(['a', 'b']), Halt()
        ])

        self.check_skip_ok(te, ti, 'b')
    #-def

    def test_SkipAtMostOneFromSet_ok_5(self):
        te, ti = self.create_and_run_tag_engine("ba_", [
            SkipAtMostOneFromSet(['a', 'b']), Halt()
        ])

        self.check_skip_ok(te, ti, 'a')
    #-def

    def test_SkipAtMostOneFromSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAtMostOneFromSet(['a', 'b']), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipAtMostOneFromRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("1_", [
            SkipAtMostOneFromRange('2', '5'), Halt()
        ])

        self.check_skip_ok(te, ti, '1')
    #-def

    def test_SkipAtMostOneFromRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("2_", [
            SkipAtMostOneFromRange('2', '5'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtMostOneFromRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("4_", [
            SkipAtMostOneFromRange('2', '5'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtMostOneFromRange_ok_4(self):
        te, ti = self.create_and_run_tag_engine("5_", [
            SkipAtMostOneFromRange('2', '5'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipAtMostOneFromRange_ok_5(self):
        te, ti = self.create_and_run_tag_engine("7_", [
            SkipAtMostOneFromRange('2', '5'), Halt()
        ])

        self.check_skip_ok(te, ti, '7')
    #-def

    def test_SkipAtMostOneFromRange_ok_6(self):
        te, ti = self.create_and_run_tag_engine("34_", [
            SkipAtMostOneFromRange('2', '5'), Halt()
        ])

        self.check_skip_ok(te, ti, '4')
    #-def

    def test_SkipAtMostOneFromRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAtMostOneFromRange('2', '5'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipAtMostOne_ok_1(self):
        te, ti = self.create_and_run_tag_engine("5u", [
            SkipAtMostOne(lambda c: c == '!'), Halt()
        ])

        self.check_skip_ok(te, ti, '5')
    #-def

    def test_SkipAtMostOne_ok_2(self):
        te, ti = self.create_and_run_tag_engine("!u", [
            SkipAtMostOne(lambda c: c == '!'), Halt()
        ])

        self.check_skip_ok(te, ti, 'u')
    #-def

    def test_SkipAtMostOne_ok_3(self):
        te, ti = self.create_and_run_tag_engine("!!u", [
            SkipAtMostOne(lambda c: c == '!'), Halt()
        ])

        self.check_skip_ok(te, ti, '!')
    #-def

    def test_SkipAtMostOne_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAtMostOne(lambda c: c == '!'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipManySymbols_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipManySymbols('a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManySymbols_ok_2(self):
        te, ti = self.create_and_run_tag_engine("a_", [
            SkipManySymbols('a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManySymbols_ok_3(self):
        te, ti = self.create_and_run_tag_engine("aa_", [
            SkipManySymbols('a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManySymbols_ok_4(self):
        te, ti = self.create_and_run_tag_engine("aaa_", [
            SkipManySymbols('a'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManySymbols_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipManySymbols('a'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipManyFromSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipManyFromSet(['e', 'q']), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManyFromSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine("q_", [
            SkipManyFromSet(['e', 'q']), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManyFromSet_ok_3(self):
        te, ti = self.create_and_run_tag_engine("qe_", [
            SkipManyFromSet(['e', 'q']), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManyFromSet_ok_4(self):
        te, ti = self.create_and_run_tag_engine("qeq_", [
            SkipManyFromSet(['e', 'q']), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManyFromSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipManyFromSet(['e', 'q']), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipManyFromRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipManyFromRange('2', '4'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManyFromRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("1_", [
            SkipManyFromRange('2', '4'), Halt()
        ])

        self.check_skip_ok(te, ti, '1')
    #-def

    def test_SkipManyFromRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("2_", [
            SkipManyFromRange('2', '4'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManyFromRange_ok_4(self):
        te, ti = self.create_and_run_tag_engine("32_", [
            SkipManyFromRange('2', '4'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManyFromRange_ok_5(self):
        te, ti = self.create_and_run_tag_engine("342_", [
            SkipManyFromRange('2', '4'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipManyFromRange_ok_6(self):
        te, ti = self.create_and_run_tag_engine("3452_", [
            SkipManyFromRange('2', '4'), Halt()
        ])

        self.check_skip_ok(te, ti, '5')
    #-def

    def test_SkipManyFromRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipManyFromRange('2', '4'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipAll_ok_1(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipAll(), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipAll_ok_2(self):
        te, ti = self.create_and_run_tag_engine("$", [
            SkipAll(), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipAll_ok_3(self):
        te, ti = self.create_and_run_tag_engine("$.", [
            SkipAll(), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipAll_ok_4(self):
        te, ti = self.create_and_run_tag_engine("$./><", [
            SkipAll(), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipMany_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipMany(lambda c: c == '+'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipMany_ok_2(self):
        te, ti = self.create_and_run_tag_engine("+_", [
            SkipMany(lambda c: c == '+'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipMany_ok_3(self):
        te, ti = self.create_and_run_tag_engine("++_", [
            SkipMany(lambda c: c == '+'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipMany_ok_4(self):
        te, ti = self.create_and_run_tag_engine("+++_", [
            SkipMany(lambda c: c == '+'), Halt()
        ])

        self.check_skip_ok(te, ti, '_')
    #-def

    def test_SkipMany_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipMany(lambda c: c == '+'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipTo_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipTo(';'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipTo_ok_2(self):
        te, ti = self.create_and_run_tag_engine(";_", [
            SkipTo(';'), Halt()
        ])

        self.check_skip_ok(te, ti, ';')
    #-def

    def test_SkipTo_ok_3(self):
        te, ti = self.create_and_run_tag_engine("a;", [
            SkipTo(';'), Halt()
        ])

        self.check_skip_ok(te, ti, ';')
    #-def

    def test_SkipTo_ok_4(self):
        te, ti = self.create_and_run_tag_engine("ab;_", [
            SkipTo(';'), Halt()
        ])

        self.check_skip_ok(te, ti, ';')
    #-def

    def test_SkipTo_ok_5(self):
        te, ti = self.create_and_run_tag_engine("abc;", [
            SkipTo(';'), Halt()
        ])

        self.check_skip_ok(te, ti, ';')
    #-def

    def test_SkipTo_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipTo(';'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipToSet_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipToSet(['e', 't']), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipToSet_ok_2(self):
        te, ti = self.create_and_run_tag_engine("e_", [
            SkipToSet(['e', 't']), Halt()
        ])

        self.check_skip_ok(te, ti, 'e')
    #-def

    def test_SkipToSet_ok_3(self):
        te, ti = self.create_and_run_tag_engine("t_", [
            SkipToSet(['e', 't']), Halt()
        ])

        self.check_skip_ok(te, ti, 't')
    #-def

    def test_SkipToSet_ok_4(self):
        te, ti = self.create_and_run_tag_engine("sdft_", [
            SkipToSet(['e', 't']), Halt()
        ])

        self.check_skip_ok(te, ti, 't')
    #-def

    def test_SkipToSet_ok_5(self):
        te, ti = self.create_and_run_tag_engine("sdeft_", [
            SkipToSet(['e', 't']), Halt()
        ])

        self.check_skip_ok(te, ti, 'e')
    #-def

    def test_SkipToSet_ok_6(self):
        te, ti = self.create_and_run_tag_engine("sdft", [
            SkipToSet(['e', 't']), Halt()
        ])

        self.check_skip_ok(te, ti, 't')
    #-def

    def test_SkipToSet_ok_7(self):
        te, ti = self.create_and_run_tag_engine("sdfe", [
            SkipToSet(['e', 't']), Halt()
        ])

        self.check_skip_ok(te, ti, 'e')
    #-def

    def test_SkipToSet_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipToSet(['e', 't']), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipToRange_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipToRange('1', '3'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipToRange_ok_2(self):
        te, ti = self.create_and_run_tag_engine("1_", [
            SkipToRange('1', '3'), Halt()
        ])

        self.check_skip_ok(te, ti, '1')
    #-def

    def test_SkipToRange_ok_3(self):
        te, ti = self.create_and_run_tag_engine("2", [
            SkipToRange('1', '3'), Halt()
        ])

        self.check_skip_ok(te, ti, '2')
    #-def

    def test_SkipToRange_ok_4(self):
        te, ti = self.create_and_run_tag_engine(".3", [
            SkipToRange('1', '3'), Halt()
        ])

        self.check_skip_ok(te, ti, '3')
    #-def

    def test_SkipToRange_ok_5(self):
        te, ti = self.create_and_run_tag_engine("efg1.3_", [
            SkipToRange('1', '3'), Halt()
        ])

        self.check_skip_ok(te, ti, '1')
    #-def

    def test_SkipToRange_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipToRange('1', '3'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipUntilNot_ok_1(self):
        te, ti = self.create_and_run_tag_engine("_", [
            SkipUntilNot(lambda c: c == ';'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_SkipUntilNot_ok_2(self):
        te, ti = self.create_and_run_tag_engine(";_", [
            SkipUntilNot(lambda c: c == ';'), Halt()
        ])

        self.check_skip_ok(te, ti, ';')
    #-def

    def test_SkipUntilNot_ok_3(self):
        te, ti = self.create_and_run_tag_engine("a;", [
            SkipUntilNot(lambda c: c == ';'), Halt()
        ])

        self.check_skip_ok(te, ti, ';')
    #-def

    def test_SkipUntilNot_ok_4(self):
        te, ti = self.create_and_run_tag_engine("ab;_", [
            SkipUntilNot(lambda c: c == ';'), Halt()
        ])

        self.check_skip_ok(te, ti, ';')
    #-def

    def test_SkipUntilNot_ok_5(self):
        te, ti = self.create_and_run_tag_engine("abc;", [
            SkipUntilNot(lambda c: c == ';'), Halt()
        ])

        self.check_skip_ok(te, ti, ';')
    #-def

    def test_SkipUntilNot_eof(self):
        te, ti = self.create_and_run_tag_engine("", [
            SkipUntilNot(lambda c: c == ';'), Halt()
        ])

        self.check_skip_ok(te, ti, None)
    #-def

    def test_Push(self):
        te, _ = self.create_and_run_tag_engine("", [
            Push("12xy"), Halt()
        ])

        self.assertEqual(te.topval(), "12xy")
    #-def

    def test_PushMatch(self):
        te, _ = self.create_and_run_tag_engine("12345_", [
            MatchManyFromRange('1', '9'), PushMatch(), Halt()
        ])

        self.assertEqual(te.topval(), [ '1', '2', '3', '4', '5' ])
    #-def

    def test_PopMatch(self):
        te, _ = self.create_and_run_tag_engine("", [
            Push("ugxy"), PopMatch(), Halt()
        ])

        self.assertEqual(te.match(), "ugxy")
    #-def

    def test_Swap(self):
        te, _ = self.create_and_run_tag_engine("", [
            Push("a"), Push("b"), Swap(), Halt()
        ])

        self.assertEqual(te.popval(), "a")
        self.assertEqual(te.popval(), "b")
    #-def

    def test_Operator_static_methods(self):
        te = TagEngine()

        te.reset()
        Operator.do_concat(te, "12", "345")
        self.assertEqual(te.topval(), "12345")

        te.reset()
        Operator.do_concat(te, "12", ["cd", "ef"])
        self.assertEqual(te.topval(), "12cdef")

        te.reset()
        Operator.do_concat(te, "12", ("cd", "ef"))
        self.assertEqual(te.topval(), "12cdef")

        te.reset()
        Operator.do_concat(te, ['a', 'b'], "cd")
        self.assertEqual(te.topval(), "abcd")

        te.reset()
        Operator.do_concat(te, ['a', 'b'], ["cd", "ef"])
        self.assertEqual(te.topval(), "abcdef")

        te.reset()
        Operator.do_concat(te, ['a', 'b'], ("cd", "ef"))
        self.assertEqual(te.topval(), "abcdef")

        te.reset()
        Operator.do_concat(te, ('a', 'b'), "cd")
        self.assertEqual(te.topval(), "abcd")

        te.reset()
        Operator.do_concat(te, ('a', 'b'), ["cd", "ef"])
        self.assertEqual(te.topval(), "abcdef")

        te.reset()
        Operator.do_concat(te, ('a', 'b'), ("cd", "ef"))
        self.assertEqual(te.topval(), "abcdef")

        te.reset()
        Operator.do_join(te, ['1'], ['2'])
        self.assertEqual(te.topval(), [ '1', '2' ])

        te.reset()
        Operator.do_join(te, ['1'], ('2', '3'))
        self.assertEqual(te.topval(), [ '1', '2', '3' ])

        te.reset()
        Operator.do_join(te, ['1'], "jhk")
        self.assertEqual(te.topval(), [ '1', "jhk" ])

        te.reset()
        Operator.do_join(te, ("ab", '1'), ['2'])
        self.assertEqual(te.topval(), [ "ab", '1', '2' ])

        te.reset()
        Operator.do_join(te, ("ab", '1'), ('2', 'a'))
        self.assertEqual(te.topval(), [ "ab", '1', '2', 'a' ])

        te.reset()
        Operator.do_join(te, ("ab", '1'), "_er")
        self.assertEqual(te.topval(), [ "ab", '1', "_er" ])

        te.reset()
        Operator.do_join(te, "xyz", ['2'])
        self.assertEqual(te.topval(), [ "xyz", '2' ])

        te.reset()
        Operator.do_join(te, "xyz", ('2', "$%"))
        self.assertEqual(te.topval(), [ "xyz", '2', "$%" ])

        te.reset()
        Operator.do_join(te, "xyz", "___")
        self.assertEqual(te.topval(), [ "xyz", "___" ])

        te.reset()
        self.assertEqual(Operator.load_operand(te, (OT_IMM, 42)), 42)
        self.assertEqual(te.state(), TES_IDLE)

        te.reset()
        te.set_match("abrakadabra")
        self.assertEqual(
            Operator.load_operand(te, (OT_REG, None)), "abrakadabra"
        )
        self.assertEqual(te.state(), TES_IDLE)

        te.reset()
        te.pushval("nut")
        self.assertEqual(Operator.load_operand(te, (OT_STK, None)), "nut")
        self.assertEqual(te.state(), TES_IDLE)

        te.reset()
        self.assertIsNone(Operator.load_operand(te, (-1, None)))
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(
            te.last_error_detail(), "Invalid type of instruction operand"
        )
    #-def

    def test_Concat_ko_1(self):
        te, _ = self.create_and_run_tag_engine("", [
            Concat((OT_STK, None), (OT_STK, None)), Halt()
        ])

        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")
    #-def

    def test_Concat_ko_2(self):
        te, _ = self.create_and_run_tag_engine("", [
            Concat((OT_IMM, "abraka"), (OT_STK, None)), Halt()
        ])

        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")
    #-def

    def test_Concat_ko_3(self):
        te, _ = self.create_and_run_tag_engine("", [
            Concat((OT_STK, None), (OT_IMM, "dabra")), Halt()
        ])

        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "Pop applied on empty stack")
    #-def

    def test_Concat_ok(self):
        te, _ = self.create_and_run_tag_engine("", [
            Concat((OT_IMM, "abraka"), (OT_IMM, "dabra")), Halt()
        ])

        self.assertEqual(te.topval(), "abrakadabra")
    #-def

    def test_Join_ok(self):
        te, _ = self.create_and_run_tag_engine("", [
            Push("abraka"), Push("dabra"),
            Join((OT_STK, None), (OT_STK, None)),
            Halt()
        ])

        self.assertEqual(te.topval(), [ "abraka", "dabra" ])
    #-def

    def test_JTrue_1(self):
        te, _ = self.create_and_run_tag_engine("x", [
            TestSymbol('_'), JTrue(5), Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.assertEqual(te.ip(), 3)
        self.assertEqual(te.state(), TES_HALTED)
    #-def

    def test_JTrue_2(self):
        te, _ = self.create_and_run_tag_engine("x", [
            TestSymbol('x'), JTrue(5), Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.assertEqual(te.ip(), 6)
        self.assertEqual(te.state(), TES_HALTED)
    #-def

    def test_JFalse_1(self):
        te, _ = self.create_and_run_tag_engine("x", [
            TestSymbol('_'), JFalse(5), Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.assertEqual(te.ip(), 6)
        self.assertEqual(te.state(), TES_HALTED)
    #-def

    def test_JFalse_2(self):
        te, _ = self.create_and_run_tag_engine("x", [
            TestSymbol('x'), JFalse(5), Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.assertEqual(te.ip(), 3)
        self.assertEqual(te.state(), TES_HALTED)
    #-def

    def test_Jump(self):
        te, _ = self.create_and_run_tag_engine("x", [
            Jump(5), Halt(), Halt(), Halt(), Halt(), Halt()
        ])

        self.assertEqual(te.ip(), 6)
        self.assertEqual(te.state(), TES_HALTED)
    #-def

    def test_Call(self):
        te, ti = self.create_and_run_tag_engine("xy", [
            Call(3), Halt(), Fail('?'), MatchSymbol('x'), Return(), Fail('??')
        ])

        self.assertEqual(te.match(), "x")
        self.assertEqual(ti.peek(), ('y', 'y'))
        self.assertTrue(te.match_flag())
        self.assertEqual(te.ip(), 2)
        self.assertEqual(te.state(), TES_HALTED)
        self.assertEqual(te.last_error_detail(), "")
    #-def

    def test_ECall(self):
        def f(te):
            te.set_match("Yipeee!")
        te, _ = self.create_and_run_tag_engine("x", [
            ECall(f), Halt()
        ])

        self.assertEqual(te.match(), "Yipeee!")
        self.assertEqual(te.state(), TES_HALTED)
    #-def

    def test_Pause(self):
        te, _ = self.create_and_run_tag_engine("x", [
            Pause(), Halt()
        ])

        self.assertEqual(te.state(), TES_PAUSED)
    #-def

    def test_Halt(self):
        te, _ = self.create_and_run_tag_engine("x", [
            Halt()
        ])

        self.assertEqual(te.state(), TES_HALTED)
    #-def
#-class

class TestTagICElementsCase(unittest.TestCase):

    def test_TagICElement(self):
        TagICElement()
    #-def

    def test_TagICMacro(self):
        f = {}
        b = [1]

        m = TagICMacro(f, "m")
        self.assertIs(m.factory(), f)
        self.assertEqual(m.name(), "m")
        self.assertEqual(m.body(), [])
        m.set_body(b)
        self.assertIs(m.body(), b)

        m = TagICMacro(f, "m", b)
        self.assertIs(m.factory(), f)
        self.assertEqual(m.name(), "m")
        self.assertIs(m.body(), b)
    #-def

    def test_TagICLabel(self):
        f = {}

        l = TagICLabel(f, "l")
        self.assertIs(l.factory(), f)
        self.assertEqual(l.name(), "l")
        self.assertEqual(l.position(), -1)
        l.set_position(3)
        self.assertEqual(l.position(), 3)

        l = TagICLabel(f, "l", 2)
        self.assertIs(l.factory(), f)
        self.assertEqual(l.name(), "l")
        self.assertEqual(l.position(), 2)
    #-def
#-class

class TestTagICSymbolFactoryCase(unittest.TestCase):

    def test_object_creating(self):
        c = {}
        f = TagICSymbolFactory(c, TagICLabel)

        self.assertIs(f.symbols(), c)
        with self.assertRaises(DoItAssertionError):
            f.LETTER
        f._label
        self.assertIs(c['label'].factory(), f)
        self.assertEqual(c['label'].name(), 'label')
        self.assertEqual(c['label'].position(), -1)
    #-def
#-class

class TestTagICSymbolTableCase(unittest.TestCase):

    def test_symbol_table_initialization(self):
        c = ()
        t = TagICSymbolTable(c)

        self.assertIs(t.compiler(), c)
        self.assertIsInstance(t.macro_factory(), TagICSymbolFactory)
        self.assertIsInstance(t.label_factory(), TagICSymbolFactory)
    #-def
#-class

class ResultHolderEnvironment(TagProgramEnvironment):
    __slots__ = [ 'result' ]

    def __init__(self, engine):
        TagProgramEnvironment.__init__(self, engine)
        self.result = 0
    #-def
#-class

class TestTagICCompilerCase(unittest.TestCase):

    def test_initialization(self):
        c = TagICCompiler()

        self.assertIsInstance(c.symbol_table(), TagICSymbolTable)
    #-def

    def test_define(self):
        c = TagICCompiler()
        M = c.symbol_table().macro_factory()

        with self.assertRaises(DoItAssertionError):
            c.define("mAcRo", "abc")

        c.define("X1")
        self.assertEqual(M.X1.body(), [])
        c.define("X2", "")
        self.assertEqual(M.X2.body(), [])
        c.define("X3", 'a')
        self.assertEqual(M.X3.body(), ['a'])
        c.define("X4", "bab")
        self.assertEqual(M.X4.body(), ['b', 'a'])

        c.define("Y1", [])
        self.assertEqual(M.Y1.body(), [])
        with self.assertRaises(DoItAssertionError):
            c.define("Y2", [1])
        with self.assertRaises(DoItAssertionError):
            c.define("Y3", [""])
        c.define("Y4", ['c'])
        self.assertEqual(M.Y4.body(), ['c'])
        with self.assertRaises(DoItAssertionError):
            c.define("Y5", ["abc"])

        c.define("X3", 'b')
        self.assertEqual(M.X3.body(), ['b'])

        c.define("Z1", ('a', 'a'))
        self.assertEqual(M.Z1.body(), ['a'])
        c.define("Z2", ('a', 'b'))
        self.assertEqual(M.Z2.body(), ['a', 'b'])
        with self.assertRaises(DoItAssertionError):
            c.define("Z3", ('b', 'a'))

        c.define("ODIGIT", ('0', '7'))
        self.assertEqual(M.ODIGIT.body(),
            ['0', '1', '2', '3', '4', '5', '6', '7']
        )
        c.define("DIGIT", M.ODIGIT, '8', '9')
        self.assertEqual(M.DIGIT.body(),
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        )

        c.define("A1", "ab")
        c.define("A2", M.A1, 'c')
        c.define("A1", "_")
        self.assertEqual(M.A1.body(), ['_'])
        self.assertEqual(M.A2.body(), ['a', 'b', 'c'])

        with self.assertRaises(DoItAssertionError):
            c.define("XX", 1)
    #-def

    def tc_emit_1(self, te):
        te.env().result = 1
    #-def

    def tc_emit_2(self, te):
        te.env().result = 2
    #-def

    def tc_emit_3(self, te):
        te.env().result = 3
    #-def

    def tc_emit_4(self, te):
        te.env().result = 4
    #-def

    def tc_emit_5(self, te):
        te.env().result = 5
    #-def

    def tc_run(self, p, s):
        i = TagTextInput()
        i.load_data_from_string(s)
        e = TagEngine()
        e.run(i, p)
        return e, i
    #-def

    def test_compile_1(self):
        icc = TagICCompiler()
        L = icc.symbol_table().label_factory()
        p = TagProgram("test", ResultHolderEnvironment, icc.compile([
          L._start,
            JUMP    (L._main),
          L._switch_table,
            SYMBOL  ('a', L._a),
            RANGE   ('b', 'd', L._b_to_d),
            SET     ("_;", L._score_semicolon),
            EOF     (L._eof),
            DEFAULT (L._default),
            NULL,
          L._main,
            BRANCH  (L._switch_table),
          L._exit,
            HALT,
          L._a,
            ECALL   (self.tc_emit_1),
            JUMP    (L._exit),
          L._b_to_d,
            ECALL   (self.tc_emit_2),
            JUMP    (L._exit),
          L._score_semicolon,
            ECALL   (self.tc_emit_3),
            JUMP    (L._exit),
          L._default,
            ECALL   (self.tc_emit_4),
            JUMP    (L._exit),
          L._eof,
            ECALL   (self.tc_emit_5),
            JUMP    (L._exit)
        ]))

        e, _ = self.tc_run(p, "")
        self.assertEqual(e.env().result, 5)

        e, _ = self.tc_run(p, "a")
        self.assertEqual(e.env().result, 1)

        e, _ = self.tc_run(p, "b")
        self.assertEqual(e.env().result, 2)

        e, _ = self.tc_run(p, "c")
        self.assertEqual(e.env().result, 2)

        e, _ = self.tc_run(p, "d")
        self.assertEqual(e.env().result, 2)

        e, _ = self.tc_run(p, "e")
        self.assertEqual(e.env().result, 4)

        e, _ = self.tc_run(p, "_")
        self.assertEqual(e.env().result, 3)

        e, _ = self.tc_run(p, ";")
        self.assertEqual(e.env().result, 3)
    #-def

    def test_compile_2(self):
        icc = TagICCompiler()
        L = icc.symbol_table().label_factory()
        p = TagProgram("test", ResultHolderEnvironment, icc.compile([
          L._start,
            BRANCH (L._t1),
            HALT,
          L._t1,
            SYMBOL ('a', L._a),
            NULL,
          L._a,
            SKIP   ('a'),
            BRANCH (L._t2),
            HALT,
          L._t2,
            SYMBOL ('x', L._x),
            NULL,
          L._x,
            SKIP   ('x'),
            ECALL  (self.tc_emit_3),
            HALT
        ]))

        e, _ = self.tc_run(p, "ax")
        self.assertEqual(e.env().result, 3)
    #-def

    def test_compile_3(self):
        icc = TagICCompiler()
        L = icc.symbol_table().label_factory()
        p = TagProgram("test", ResultHolderEnvironment, icc.compile([
          L._start,
            JUMP   (L._main),
          L._t1,
            SYMBOL ('a', L._1),
          L._t2,
          L._t3,
            SYMBOL ('v', L._2),
            NULL,
          L._main,
            BRANCH (L._t1),
            HALT,
          L._1,
            SKIP   (['a', 'v']),
            BRANCH (L._t2),
            ECALL  (self.tc_emit_2),
            HALT,
          L._2,
            SKIP   ('v'),
            ECALL  (self.tc_emit_4),
            HALT
        ]))

        e, i = self.tc_run(p, "av")
        self.assertEqual(e.env().result, 4)
        self.assertEqual(i.peek(), (None, None))

        e, i = self.tc_run(p, "va")
        self.assertEqual(e.env().result, 4)
        self.assertEqual(i.peek(), ('a', 'a'))

        e, i = self.tc_run(p, "aa")
        self.assertEqual(e.env().result, 2)
        self.assertEqual(i.peek(), ('a', 'a'))
    #-def

    def test_compile_4(self):
        icc = TagICCompiler()
        L = icc.symbol_table().label_factory()

        with self.assertRaises(DoItAssertionError):
            icc.compile([
              L._start,
                JUMP (L._main),
              L._main,
                HALT,
              L._main,
                PAUSE
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              JUMP (L._main)
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
                HALT,
              L._swt,
                PUSH   ('a'),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
                JUMP   (L._d),
              L._swt,
                RANGE  ('a', 'z', L._az),
                SYMBOL ('d', L._d),
                NULL,
              L._az,
              L._d,
                HALT
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
                JUMP   (L._x1),
              L._swt,
                RANGE  ('a', 'z', L._az),
                SET    (['x', '1'], L._x1),
                NULL,
              L._az,
              L._x1,
                HALT
            ])
        icc.compile([
            BRANCH (L._swt),
          L._1,
            HALT,
          L._swt,
            RANGE  ('b', 'b', L._1),
            NULL
        ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
              L._1,
                HALT,
              L._swt,
                RANGE  ('b', 'a', L._1),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
              L._1,
                HALT,
              L._swt,
                SYMBOL ('b', L._1),
                RANGE  ('a', 'b', L._1),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH  (L._swt),
              L._1,
                HALT,
              L._swt,
                DEFAULT (L._1),
                RANGE   ('a', 'b', L._1),
                DEFAULT (L._1),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
              L._1,
                HALT,
              L._swt,
                EOF    (L._1),
                RANGE  ('a', 'b', L._1),
                EOF    (L._1),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
              L._1,
                HALT,
              L._swt,
                SYMBOL ('a', L._1),
                (TIC_META, TIC_UNUSED, TIC_UNUSED, TIC_UNUSED),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
              L._1,
                HALT,
              L._swt,
                SYMBOL ('a', L._1)
            ])
    #-def

    def test_compile_5(self):
        icc = TagICCompiler()
        L = icc.symbol_table().label_factory()
        p = TagProgram('test', ResultHolderEnvironment, icc.compile([
          FAIL ("FAIL test"),
          HALT
        ]))

        with self.assertRaises(DoItAssertionError):
            icc.compile([
              FAIL (1),
              HALT
            ])

        e, i = self.tc_run(p, "fg")
        self.assertEqual(e.state(), TES_ERROR)
        self.assertEqual(e.last_error_detail(), "FAIL test")
        self.assertEqual(i.peek(), ('f', 'f'))
    #-def

    def test_compile_6(self):
        icc = TagICCompiler()
        icc.define("SYM", ".?")
        M = icc.symbol_table().macro_factory()
        p1 = TagProgram('test1', ResultHolderEnvironment, icc.compile([
          MATCH      ('a'),
          MATCH_ANY,
          MATCH      ("bc"),
          MATCH      (['.', '?']),
          MATCH      (M.SYM),
          MATCH      (('1', '3')),
          MATCH      (('1', '3')),
          MATCH      (('1', '3')),
          MATCH      (lambda c: c == '#'),
          MATCH_PLUS ('1'),
          MATCH_PLUS (M.SYM),
          MATCH_PLUS (('a', 'b')),
          MATCH_PLUS (lambda c: c == '$'),
          MATCH_OPT  ('+'),
          MATCH_OPT  (['+', '-']),
          MATCH_OPT  (('u', 'v')),
          MATCH_OPT  (lambda c: c == '%'),
          MATCH_MANY ('Z'),
          MATCH_MANY (M.SYM),
          MATCH_MANY (('0', '1')),
          MATCH_MANY (lambda c: c == '*'),
          MATCH_ALL,
          HALT
        ]))
        p2 = TagProgram('test2', ResultHolderEnvironment, icc.compile([
          TEST_EOF,
          HALT
        ]))
        p3 = TagProgram('test3', ResultHolderEnvironment, icc.compile([
          TEST ('a'),
          HALT
        ]))
        p4 = TagProgram('test4', ResultHolderEnvironment, icc.compile([
          TEST (M.SYM),
          HALT
        ]))
        p5 = TagProgram('test5', ResultHolderEnvironment, icc.compile([
          TEST (('a', 'b')),
          HALT
        ]))
        p6 = TagProgram('test6', ResultHolderEnvironment, icc.compile([
          TEST (lambda c: c == '$'),
          HALT
        ]))
        p7 = TagProgram('test7', ResultHolderEnvironment, icc.compile([
          SKIP      ('a'),
          SKIP_ANY,
          SKIP      ('b'),
          SKIP      ('c'),
          SKIP      (['.', '?']),
          SKIP      (M.SYM),
          SKIP      (('1', '3')),
          SKIP      (('1', '3')),
          SKIP      (('1', '3')),
          SKIP      (lambda c: c == '#'),
          SKIP_PLUS ('1'),
          SKIP_PLUS (M.SYM),
          SKIP_PLUS (('a', 'b')),
          SKIP_PLUS (lambda c: c == '$'),
          SKIP_OPT  ('+'),
          SKIP_OPT  (['+', '-']),
          SKIP_OPT  (('u', 'v')),
          SKIP_OPT  (lambda c: c == '%'),
          SKIP_MANY ('Z'),
          SKIP_MANY (M.SYM),
          SKIP_MANY (('0', '1')),
          SKIP_MANY (lambda c: c == '*'),
          SKIP_ALL,
          HALT
        ]))
        p7 = TagProgram('test7', ResultHolderEnvironment, icc.compile([
          SKIP_TO ('a'),
          SKIP_TO (M.SYM),
          SKIP_TO (('3', '4')),
          SKIP_TO (lambda c: c == '&'),
          HALT
        ]))

        for p, is_skip in ((p1, False), (p7, True)):
            e, i = self.tc_run(p, "a|bc?.312#11.?.bbaa$-vZZZ*///.<>{}")
            self.assertEqual(e.state(), TES_HALTED)
            if not is_skip:
                self.assertEqual(e.match(), list("///.<>{}"))
            self.assertEqual(i.peek(), (None, None))
        for p, s in ((p2, ""), (p3, "a"), (p4, "?"), (p5, "b"), (p6, "$")):
            e, i = self.tc_run(p, s)
            self.assertEqual(e.state(), TES_HALTED)
            self.assertTrue(e.match_flag())
        e, i = self.tc_run(p7, "aaaaa?.?.?.?.4356.asdf&")
        self.assertEqual(e.state(), TES_HALTED)
        self.assertEqual(i.peek(), ('&', '&'))
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              MATCH (100),
              HALT
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              (TIC_MATCH, TIC_SYMBOL, TIC_UNUSED, 100),
              HALT
            ])
    #-def

    def test_compile_7(self):
        icc = TagICCompiler()
        icc.define("X1", "abc")
        icc.define("X2", "cde")
        M = icc.symbol_table().macro_factory()
        L = icc.symbol_table().label_factory()

        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
              L._swt,
                SYMBOL ('a', L._1),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH (L._swt),
              L._swt,
                EOF    (L._1),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
                BRANCH  (L._swt),
              L._swt,
                DEFAULT (L._1),
                NULL
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              L._1,
                BRANCH (L._swt),
              L._swt,
                SET    (M.X1, L._1),
                SET    (M.X2, L._1),
                NULL
            ])

        p = TagProgram('test', ResultHolderEnvironment, icc.compile([
            BRANCH (L._swt),
            HALT,
          L._swt,
            NULL
        ]))
        q = TagProgram('test', ResultHolderEnvironment, icc.compile([
            BRANCH (L._swt),
            HALT,
          L._swt,
            SET    (M.X1, L._1),
            NULL,
          L._1,
            SKIP   (M.X1),
            HALT
        ]))

        e, i = self.tc_run(p, "")
        self.assertEqual(e.state(), TES_HALTED)

        e, i = self.tc_run(p, "x")
        self.assertEqual(e.state(), TES_HALTED)

        e, i = self.tc_run(q, "b")
        self.assertEqual(e.state(), TES_HALTED)
        self.assertEqual(i.peek(), (None, None))
    #-def

    def test_compile_8(self):
        icc = TagICCompiler()
        p1 = TagProgram('test1', ResultHolderEnvironment, icc.compile([
          PUSH ("abc"),
          PUSH (['a', "bc"]),
          HALT
        ]))
        p2 = TagProgram('test2', ResultHolderEnvironment, icc.compile([
          MATCH_ALL,
          PUSH_MATCH,
          HALT
        ]))
        p3 = TagProgram('test3', ResultHolderEnvironment, icc.compile([
          PUSH ("xyz"),
          POP_MATCH,
          HALT
        ]))
        p4 = TagProgram('test4', ResultHolderEnvironment, icc.compile([
          PUSH ('a'),
          PUSH ('b'),
          SWAP,
          HALT
        ]))

        e, _ = self.tc_run(p1, "")
        self.assertEqual(e.popval(), ['a', "bc"])
        self.assertEqual(e.popval(), "abc")

        with self.assertRaises(DoItAssertionError):
            icc.compile([
              PUSH (-11)
            ])

        e, _ = self.tc_run(p2, "abc")
        self.assertEqual(e.popval(), ['a', 'b', 'c'])

        e, _ = self.tc_run(p3, "")
        self.assertEqual(e.match(), "xyz")

        e, _ = self.tc_run(p4, "")
        self.assertEqual(e.topval(), 'a')
    #-def

    def test_compile_9(self):
        icc = TagICCompiler()
        p1 = TagProgram("test1", ResultHolderEnvironment, icc.compile([
          PUSH   ("bc"),
          POP_MATCH,
          CONCAT ("a", ACC),
          HALT
        ]))
        p2 = TagProgram("test2", ResultHolderEnvironment, icc.compile([
          PUSH   ("bc"),
          CONCAT ("a", STK),
          HALT
        ]))
        p3 = TagProgram("test3", ResultHolderEnvironment, icc.compile([
          CONCAT ("a", "xy"),
          HALT
        ]))
        p4 = TagProgram("test4", ResultHolderEnvironment, icc.compile([
          CONCAT ("a", ["ab", "", "xg"]),
          HALT
        ]))
        p5 = TagProgram("test5", ResultHolderEnvironment, icc.compile([
          PUSH   ("bc"),
          POP_MATCH,
          CONCAT (ACC, ['a', 'b']),
          HALT
        ]))
        p6 = TagProgram("test6", ResultHolderEnvironment, icc.compile([
          PUSH ('a'),
          PUSH ('b'),
          CONCAT (STK, STK),
          HALT
        ]))
        p7 = TagProgram("test7", ResultHolderEnvironment, icc.compile([
          CONCAT (["a", 'z'], ["ab", "", "xg"]),
          HALT
        ]))
        p8 = TagProgram("test8", ResultHolderEnvironment, icc.compile([
          JOIN (["a", 'z'], ["ab", "", "xg"]),
          HALT
        ]))

        e, _ = self.tc_run(p1, "")
        self.assertEqual(e.topval(), "abc")
        e, _ = self.tc_run(p2, "")
        self.assertEqual(e.topval(), "abc")
        e, _ = self.tc_run(p3, "")
        self.assertEqual(e.topval(), "axy")
        e, _ = self.tc_run(p4, "")
        self.assertEqual(e.topval(), "aabxg")
        e, _ = self.tc_run(p5, "")
        self.assertEqual(e.topval(), "bcab")
        e, _ = self.tc_run(p6, "")
        self.assertEqual(e.topval(), "ab")
        e, _ = self.tc_run(p7, "")
        self.assertEqual(e.topval(), "azabxg")
        e, _ = self.tc_run(p8, "")
        self.assertEqual(e.topval(), ["a", "z", "ab", "", "xg"])

        with self.assertRaises(DoItAssertionError):
            icc.compile([
              CONCAT ("a", 123),
              HALT
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              CONCAT (123, "b"),
              HALT
            ])
    #-def

    def test_comile_10(self):
        icc = TagICCompiler()
        L = icc.symbol_table().label_factory()
        p1 = TagProgram('test1', ResultHolderEnvironment, icc.compile([
            JUMP   (L._main),
            HALT,
          L._main,
            TEST_EOF,
            JFALSE (L._1),
            HALT,
          L._1,
            TEST   ('a'),
            JTRUE  (L._2),
            HALT,
          L._2,
            SKIP   ('a'),
            HALT
        ]))
        p2 = TagProgram('test2', ResultHolderEnvironment, icc.compile([
          PAUSE
        ]))

        e, i = self.tc_run(p1, "a")
        self.assertEqual(i.peek(), (None, None))

        e, _ = self.tc_run(p2, "a")
        self.assertEqual(e.state(), TES_PAUSED)

        with self.assertRaises(DoItAssertionError):
            icc.compile([
              JUMP (L._main)
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              ECALL (1),
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              (128, -1, -1, -1)
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              MATCH ("")
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              MATCH ([])
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              MATCH (('6', '1'))
            ])
        with self.assertRaises(DoItAssertionError):
            icc.compile([
              MATCH (128)
            ])
    #-def

    def test_compile_11(self):
        icc = TagICCompiler()
        L = icc.symbol_table().label_factory()
        p = TagProgram('test', ResultHolderEnvironment, icc.compile([
            CALL (L._test),
            HALT,
          L._test,
            PUSH ("Huray!"),
            RETURN
        ]))

        e, _ = self.tc_run(p, "")
        self.assertEqual(e.state(), TES_HALTED)
        self.assertEqual(e.nvals(), 1)
        self.assertEqual(e.topval(), "Huray!")
        self.assertEqual(e.naddrs(), 0)

        with self.assertRaises(DoItAssertionError):
            icc.compile([
              CALL(L._foo)
            ])
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTagAbstractInputCase))
    suite.addTest(unittest.makeSuite(TestTagTextInputCase))
    suite.addTest(unittest.makeSuite(TestTagProgramEnvironmentCase))
    suite.addTest(unittest.makeSuite(TestTagProgramCase))
    suite.addTest(unittest.makeSuite(TestTagEngineCase))
    suite.addTest(unittest.makeSuite(TestInstructionsCase))
    suite.addTest(unittest.makeSuite(TestTagICElementsCase))
    suite.addTest(unittest.makeSuite(TestTagICSymbolFactoryCase))
    suite.addTest(unittest.makeSuite(TestTagICSymbolTableCase))
    suite.addTest(unittest.makeSuite(TestTagICCompilerCase))
    return suite
#-def
