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

from doit.text.pgen.utils.tagengine import \
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
    Halt, \
    TagProgramEnvironment, TagProgram, \
    TagEngine

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

        self.assertIsNone(ti1.peek())
        self.assertEqual(ti2.peekn(3), [])
        ti1.next()
        ti2.nextn(3)
        self.assertIsNone(ti1.peek())
        self.assertEqual(ti2.peekn(3), [])
    #-def

    def test_input_from_string(self):
        ti = TagTextInput()

        ti.load_data_from_string("")
        self.assertIsNone(ti.peek())
        ti.next()
        self.assertIsNone(ti.peek())

        ti.load_data_from_string("")
        self.assertEqual(ti.peekn(2), "")
        ti.nextn(2)
        self.assertEqual(ti.peekn(2), "")
        self.assertEqual(ti.peekn(1), "")
        self.assertIsNone(ti.peek())

        ti.load_data_from_string("abc")
        self.assertEqual(ti.peek(), 'a')
        self.assertEqual(ti.peek(), 'a')
        ti.next()
        self.assertEqual(ti.peek(), 'b')
        self.assertEqual(ti.peek(), 'b')
        self.assertEqual(ti.peek(), 'b')
        ti.next()
        self.assertEqual(ti.peek(), 'c')
        self.assertEqual(ti.peek(), 'c')
        self.assertEqual(ti.peek(), 'c')
        self.assertEqual(ti.peek(), 'c')
        ti.next()
        self.assertIsNone(ti.peek())
        self.assertIsNone(ti.peek())
        self.assertIsNone(ti.peek())
        self.assertIsNone(ti.peek())
        ti.next()
        self.assertIsNone(ti.peek())
        self.assertIsNone(ti.peek())
        self.assertIsNone(ti.peek())
        self.assertIsNone(ti.peek())

        ti.load_data_from_string("abcdef")
        self.assertEqual(ti.peekn(4), "abcd")
        self.assertEqual(ti.peekn(3), "abc")
        self.assertEqual(ti.peekn(6), "abcdef")
        self.assertEqual(ti.peekn(7), "abcdef")
        self.assertEqual(ti.peekn(8), "abcdef")
        self.assertEqual(ti.peekn(16), "abcdef")
        self.assertEqual(ti.peek(), "a")
        ti.nextn(2)
        self.assertEqual(ti.peekn(4), "cdef")
        self.assertEqual(ti.peekn(3), "cde")
        self.assertEqual(ti.peekn(6), "cdef")
        self.assertEqual(ti.peekn(7), "cdef")
        self.assertEqual(ti.peekn(8), "cdef")
        self.assertEqual(ti.peekn(16), "cdef")
        self.assertEqual(ti.peek(), "c")
        ti.nextn(3)
        self.assertEqual(ti.peekn(4), "f")
        self.assertEqual(ti.peekn(3), "f")
        self.assertEqual(ti.peekn(6), "f")
        self.assertEqual(ti.peekn(7), "f")
        self.assertEqual(ti.peekn(8), "f")
        self.assertEqual(ti.peekn(16), "f")
        self.assertEqual(ti.peek(), "f")
        ti.nextn(4)
        self.assertEqual(ti.peekn(4), "")
        self.assertEqual(ti.peekn(3), "")
        self.assertEqual(ti.peekn(6), "")
        self.assertEqual(ti.peekn(7), "")
        self.assertEqual(ti.peekn(8), "")
        self.assertEqual(ti.peekn(16), "")
        self.assertIsNone(ti.peek())
        ti.nextn(5)
        self.assertEqual(ti.peekn(4), "")
        self.assertEqual(ti.peekn(3), "")
        self.assertEqual(ti.peekn(6), "")
        self.assertEqual(ti.peekn(7), "")
        self.assertEqual(ti.peekn(8), "")
        self.assertEqual(ti.peekn(16), "")
        self.assertIsNone(ti.peek())
    #-def

    def test_input_from_file(self):
        ti = TagTextInput()

        with OpenContext(0, "", False):
            self.assertTrue(ti.load_data_from_file('foo'))
        self.assertIsNone(ti.peek())

        with OpenContext(0, "xyz", False):
            self.assertTrue(ti.load_data_from_file('bar'))
        self.assertEqual(ti.peek(), 'x')
        ti.nextn(2)
        self.assertEqual(ti.peek(), 'z')
        ti.next()
        self.assertIsNone(ti.peek())
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
        if n is None:
            self.assertIsNone(ti.peek())
        else:
            self.assertEqual(ti.peek(), n)
        self.assertTrue(te.match_flag())
    #-def

    def check_match_ko(self, te, ti, u):
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(),
            "Unexpected input symbol %r" % u
        )
        self.assertEqual(te.ip(), 1)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), u)
        self.assertFalse(te.match_flag())
    #-def

    def check_match_word_ko(self, te, ti, m, e):
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(),
            "Unexpected word %r (need %r)" % (m, e)
        )
        self.assertEqual(te.ip(), 1)
        self.assertIsNone(te.match())
        self.assertEqual(ti.peek(), m[0])
        self.assertFalse(te.match_flag())
    #-def

    def check_match_eof(self, te, ti):
        self.assertEqual(te.state(), TES_ERROR)
        self.assertEqual(te.last_error_detail(), "Unexpected end of input")
        self.assertEqual(te.ip(), 1)
        self.assertIsNone(te.match())
        self.assertIsNone(ti.peek())
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
            self.assertEqual(ti.peek(), m[0])
        else:
            self.assertIsNone(ti.peek())
        self.assertFalse(te.match_flag())
    #-def

    def check_test_result(self, te, ti, r, p):
        self.assertEqual(te.state(), TES_HALTED)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.ip(), 2)
        self.assertIsNone(te.match())
        if p is None:
            self.assertIsNone(ti.peek())
        else:
            self.assertEqual(ti.peek(), p)
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
        if p is None:
            self.assertIsNone(ti.peek())
        else:
            self.assertEqual(ti.peek(), p)
        self.assertFalse(te.match_flag())
    #-def

    def check_skip_ok(self, te, ti, p):
        self.assertEqual(te.state(), TES_HALTED)
        self.assertEqual(te.last_error_detail(), "")
        self.assertEqual(te.ip(), 2)
        self.assertIsNone(te.match())
        if p is None:
            self.assertIsNone(ti.peek())
        else:
            self.assertEqual(ti.peek(), p)
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
        self.assertEqual(ti.peek(), 'u')
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
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTagAbstractInputCase))
    suite.addTest(unittest.makeSuite(TestTagTextInputCase))
    suite.addTest(unittest.makeSuite(TestTagProgramEnvironmentCase))
    suite.addTest(unittest.makeSuite(TestTagProgramCase))
    suite.addTest(unittest.makeSuite(TestTagEngineCase))
    suite.addTest(unittest.makeSuite(TestInstructionsCase))
    return suite
#-def
