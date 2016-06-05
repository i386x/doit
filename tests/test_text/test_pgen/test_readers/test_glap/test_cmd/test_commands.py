#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/ \
#!              test_readers/test_glap/test_cmd/test_commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-05-10 13:16:59 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Glap reader command processor commands module tests.\
"""

__license__ = """\
Copyright (c) 2014 - 2016 Jiří Kučera.

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

from doit.text.pgen.readers.glap.cmd.errors import \
    CommandProcessorError, \
    CommandError

from doit.text.pgen.readers.glap.cmd.runtime import \
    Pair, \
    List, \
    HashMap, \
    ExceptionClass

from doit.text.pgen.readers.glap.cmd.commands import \
    Location, \
    Command, \
    SetLocal, \
    GetLocal, \
    Operation, \
    Add, Sub, Mul, Div, Mod, Neg, \
    BitAnd, BitOr, BitXor, ShiftL, ShiftR, Inv, \
    Lt, Gt, Le, Ge, Eq, Ne, Is, \
    And, Or, Not, \
    Copy, Slice, Concat, Join, Merge, \
    Strlen, Size, Empty, Contains, Count, \
    IsDigit, IsUpper, IsLower, IsAlpha, IsLetter, IsAlnum, IsWord, \
    Keys, Values, \
    First, Second, GetItem, \
    Substr, Find, RFind, \
    LStrip, RStrip, Strip, ToUpper, ToLower, Subst, Trans, \
    Sort, Reverse, Unique, \
    Split, \
    If

from doit.text.pgen.readers.glap.cmd.eval import \
    Environment, \
    CommandProcessor

class TestLocationCase(unittest.TestCase):

    def test_methods(self):
        loc0 = Location()
        loc1 = Location("A", 1, 2)

        self.assertIsNone(loc0.file())
        self.assertEqual(loc0.line(), -1)
        self.assertEqual(loc0.column(), -1)
        self.assertEqual(loc0, (None, -1, -1))
        x, y, z = loc0
        self.assertEqual((x, y, z), (None, -1, -1))
        self.assertEqual(str(loc0), "(internal)")

        self.assertEqual(loc1.file(), "A")
        self.assertEqual(loc1.line(), 1)
        self.assertEqual(loc1.column(), 2)
        self.assertEqual(loc1, ("A", 1, 2))
        x, y, z = loc1
        self.assertEqual((x, y, z), ("A", 1, 2))
        self.assertEqual(str(loc1), 'at ["A":1:2]')
    #-def
#-class

class TestCommandCase(unittest.TestCase):

    def test_command_methods(self):
        p = CommandProcessor()
        c = Command()

        self.assertEqual(c.name, 'command')
        self.assertEqual(c.location, Location())
        self.assertIsNone(c.env)
        self.assertFalse(c.isfunc())
        c.set_location("X.f", 5, 8)
        self.assertEqual(str(c), '"command" at ["X.f":5:8]')
        c.help(p)
        c.enter(p)
        c.expand(p)
        c.leave(p)
        p.setacc(56)
        c.pushacc(p)
        self.assertEqual(p.popval(), 56)
        self.assertIsNone(
            c.find_exception_handler(CommandError(p.TypeError, ""))
        )
    #-def
#-class

class TestSetLocalCase(unittest.TestCase):

    def test_SetLocal(self):
        p = CommandProcessor()

        with self.assertRaises(CommandError):
            p.getenv().getvar('z')
        p.run([SetLocal('z', "hello")])
        self.assertEqual(p.getenv().getvar('z'), "hello")
    #-def
#-class

class TestGetLocalCase(unittest.TestCase):

    def test_GetLocal(self):
        p = CommandProcessor()

        p.run([SetLocal('v', 751), GetLocal('v')])
        self.assertEqual(p.acc(), 751)
    #-def
#-class

class TestOperationsCase(unittest.TestCase):

    def test_unknown_operation(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([Operation()])
    #-def

    def test_Add(self):
        p = CommandProcessor()

        p.run([Add(1, 2)])
        self.assertEqual(p.acc(), 3)
        p.run([Add(1, 2.5)])
        self.assertEqual(p.acc(), 3.5)
        p.run([Add(1.25, 2)])
        self.assertEqual(p.acc(), 3.25)
        p.run([Add(-1.5, 2.5)])
        self.assertEqual(p.acc(), 1)

        with self.assertRaises(CommandProcessorError):
            p.run([Add("c", 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Add(2.1, "1")])
        with self.assertRaises(CommandProcessorError):
            p.run([Add("c", "1")])
    #-def

    def test_Sub(self):
        p = CommandProcessor()

        p.run([Sub(1, 2)])
        self.assertEqual(p.acc(), -1)
    #-def

    def test_Mul(self):
        p = CommandProcessor()

        p.run([Mul(4, 5.2)])
        self.assertEqual(p.acc(), 20.8)
    #-def

    def test_Div(self):
        p = CommandProcessor()

        p.run([Div(5, 2)])
        self.assertEqual(p.acc(), 2.5)
        p.run([Div(0, 2)])
        self.assertEqual(p.acc(), 0)
        with self.assertRaises(CommandProcessorError):
            p.run([Div(1, 0)])
    #-def

    def test_Mod(self):
        p = CommandProcessor()

        p.run([Mod(5, 3)])
        self.assertEqual(p.acc(), 2)
        p.run([Mod(5.5, 2)])
        self.assertEqual(p.acc(), 1.5)
        p.run([Mod(5, 3.5)])
        self.assertEqual(p.acc(), 1.5)
        p.run([Mod(7.5, 3.5)])
        self.assertEqual(p.acc(), 0.5)
        p.run([Mod(0, 3)])
        self.assertEqual(p.acc(), 0)
        with self.assertRaises(CommandProcessorError):
            p.run([Mod(1, 0)])
    #-def

    def test_Neg(self):
        p = CommandProcessor()

        p.run([Neg(-4)])
        self.assertEqual(p.acc(), 4)
    #-def

    def test_BitAnd(self):
        p = CommandProcessor()

        p.run([BitAnd(7, 6)])
        self.assertEqual(p.acc(), 6)
    #-def

    def test_BitOr(self):
        p = CommandProcessor()

        p.run([BitOr(7, 6)])
        self.assertEqual(p.acc(), 7)
    #-def

    def test_BitXor(self):
        p = CommandProcessor()

        p.run([BitXor(7, 6)])
        self.assertEqual(p.acc(), 1)
    #-def

    def test_ShiftL(self):
        p = CommandProcessor()

        p.run([ShiftL(1, 3)])
        self.assertEqual(p.acc(), 8)
        p.run([ShiftL(-3, 3)])
        self.assertEqual(p.acc(), -24)
        p.run([ShiftL(3, 0)])
        self.assertEqual(p.acc(), 3)
        with self.assertRaises(CommandProcessorError):
            p.run([ShiftL(3, -1)])
    #-def

    def test_ShiftR(self):
        p = CommandProcessor()

        p.run([ShiftR(31, 3)])
        self.assertEqual(p.acc(), 3)
        p.run([ShiftR(-31, 3)])
        self.assertEqual(p.acc(), -4)
        p.run([ShiftR(3, 0)])
        self.assertEqual(p.acc(), 3)
        with self.assertRaises(CommandProcessorError):
            p.run([ShiftR(3, -1)])
    #-def

    def test_Inv(self):
        p = CommandProcessor()

        p.run([Inv(5)])
        self.assertEqual(p.acc(), -6)
        p.run([Inv(-3)])
        self.assertEqual(p.acc(), 2)
    #-def

    def test_Lt(self):
        p = CommandProcessor()

        p.run([Lt(1, 2)])
        self.assertTrue(p.acc())
        p.run([Lt(2.2, 2)])
        self.assertFalse(p.acc())
        p.run([Lt(2, 2)])
        self.assertFalse(p.acc())
        p.run([Lt("xy", "z")])
        self.assertTrue(p.acc())
        p.run([Lt("xy", "a")])
        self.assertFalse(p.acc())
        p.run([Lt("z", "z")])
        self.assertFalse(p.acc())
        with self.assertRaises(CommandProcessorError):
            p.run([Lt("x", 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Lt(1.0, "y")])
        with self.assertRaises(CommandProcessorError):
            p.run([Lt([], 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Lt(1.0, {})])
        with self.assertRaises(CommandProcessorError):
            p.run([Lt({}, [])])
    #-def

    def test_Gt(self):
        p = CommandProcessor()

        p.run([Gt(1, 2)])
        self.assertFalse(p.acc())
        p.run([Gt(3, 2)])
        self.assertTrue(p.acc())
        p.run([Gt(3, 3)])
        self.assertFalse(p.acc())
        p.run([Gt('a', 'b')])
        self.assertFalse(p.acc())
        p.run([Gt('x', 'a')])
        self.assertTrue(p.acc())
        p.run([Gt('c', 'c')])
        self.assertFalse(p.acc())
    #-def

    def test_Le(self):
        p = CommandProcessor()

        p.run([Le(1, 2)])
        self.assertTrue(p.acc())
        p.run([Le(3, 2)])
        self.assertFalse(p.acc())
        p.run([Le(3, 3)])
        self.assertTrue(p.acc())
        p.run([Le('a', 'b')])
        self.assertTrue(p.acc())
        p.run([Le('x', 'a')])
        self.assertFalse(p.acc())
        p.run([Le('c', 'c')])
        self.assertTrue(p.acc())
    #-def

    def test_Ge(self):
        p = CommandProcessor()

        p.run([Ge(1, 2)])
        self.assertFalse(p.acc())
        p.run([Ge(3.0, 2)])
        self.assertTrue(p.acc())
        p.run([Ge(3, 3.0)])
        self.assertTrue(p.acc())
        p.run([Ge('a', 'b')])
        self.assertFalse(p.acc())
        p.run([Ge('x', 'a')])
        self.assertTrue(p.acc())
        p.run([Ge('c', 'c')])
        self.assertTrue(p.acc())
    #-def

    def test_Eq(self):
        p = CommandProcessor()

        p.run([Eq({}, [])])
        self.assertFalse(p.acc())
        p.run([Eq((1, 2), (1, 2))])
        self.assertTrue(p.acc())
        p.run([Eq(1, 1.0)])
        self.assertTrue(p.acc())
        p.run([Eq("a", ("a", "a"))])
        self.assertFalse(p.acc())
    #-def

    def test_Ne(self):
        p = CommandProcessor()

        p.run([Ne({}, [])])
        self.assertTrue(p.acc())
        p.run([Ne((1, 2), (1, 2))])
        self.assertFalse(p.acc())
        p.run([Ne(1, 1.0)])
        self.assertFalse(p.acc())
        p.run([Ne("a", ("a", "a"))])
        self.assertTrue(p.acc())
    #-def

    def test_Is(self):
        p = CommandProcessor()

        p.run([Is(None, None)])
        self.assertTrue(p.acc())
        p.run([Is((1, 2), (1, 2))])
        self.assertFalse(p.acc())
        p.run([Is(1, 1)])
        self.assertTrue(p.acc())
    #-def

    def test_And(self):
        p = CommandProcessor()

        p.run([And(True, True)])
        self.assertTrue(p.acc())
        p.run([And(None, True)])
        self.assertFalse(p.acc())
        p.run([And(True, None)])
        self.assertFalse(p.acc())
        p.run([And(None, None)])
        self.assertFalse(p.acc())
    #-def

    def test_Or(self):
        p = CommandProcessor()

        p.run([Or(None, True)])
        self.assertTrue(p.acc())
    #-def

    def test_Not(self):
        p = CommandProcessor()

        p.run([Not(None)])
        self.assertTrue(p.acc())
        p.run([Not(True)])
        self.assertFalse(p.acc())
    #-def

    def test_Copy(self):
        p = CommandProcessor()

        p.run([
            SetLocal('x', "abc"),
            SetLocal('y', Copy(GetLocal('x'))),
            Eq(GetLocal('x'), GetLocal('y'))
        ])
        self.assertTrue(p.acc())
        self.assertIsInstance(p.getenv()['y'], str)
        for o, t in [
            ((1, 2), Pair),
            (['a', "bc"], List),
            ({1.4: 'u', False: [3]}, HashMap)
        ]:
            p.run([
                SetLocal('x', o),
                SetLocal('y', Copy(GetLocal('x'))),
                Eq(GetLocal('x'), GetLocal('y'))
            ])
            self.assertTrue(p.acc())
            p.run([Is(GetLocal('x'), GetLocal('y'))])
            self.assertFalse(p.acc())
            self.assertIsInstance(p.getenv()['y'], t)
        with self.assertRaises(CommandProcessorError):
            p.run([Copy(1)])
    #-def

    def test_Slice(self):
        p = CommandProcessor()

        p.run([Slice("abcdefgh", 2, 5)])
        self.assertEqual(p.acc(), "cde")
        self.assertIsInstance(p.acc(), str)
        p.run([Slice([1, 2, 3], 1, 2)])
        self.assertEqual(p.acc(), [2])
        self.assertIsInstance(p.acc(), List)
        with self.assertRaises(CommandProcessorError):
            p.run([Slice((1, 1), 0, 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Slice({}, 0, 0)])
        with self.assertRaises(CommandProcessorError):
            p.run([Slice([5, 6, 7], 0, 'x')])
    #-def

    def test_Concat(self):
        p = CommandProcessor()

        p.run([Concat("ab", "cd")])
        self.assertEqual(p.acc(), "abcd")
        self.assertIsInstance(p.acc(), str)
    #-def

    def test_Join(self):
        p = CommandProcessor()

        p.run([Join(['a', 1.5], [(1, 3), -9])])
        self.assertEqual(p.acc(), ['a', 1.5, (1, 3), -9])
        self.assertIsInstance(p.acc(), List)
    #-def

    def test_Merge(self):
        d1 = {'a': 1, 2: 'b', False: 0.25}
        d2 = {'u': 3, 2: 0.5, True: 'z'}
        d1d2 = {'a': 1, 2: 0.5, False: 0.25, 'u': 3, True: 'z'}
        d2d1 = {'u': 3, 2: 'b', True: 'z', 'a': 1, False: 0.25}
        p = CommandProcessor()

        p.run([Merge(d1, d2)])
        self.assertEqual(p.acc(), d1d2)
        self.assertIsInstance(p.acc(), HashMap)
        p.run([Merge(d2, d1)])
        self.assertEqual(p.acc(), d2d1)
        self.assertIsInstance(p.acc(), HashMap)
    #-def

    def test_Strlen(self):
        p = CommandProcessor()

        p.run([Strlen("123a")])
        self.assertEqual(p.acc(), 4)
    #-def

    def test_Size(self):
        p = CommandProcessor()

        p.run([Size("abcdefg")])
        self.assertEqual(p.acc(), 7)
        p.run([Size(('a', 1))])
        self.assertEqual(p.acc(), 2)
        p.run([Size([1, "", ()])])
        self.assertEqual(p.acc(), 3)
        p.run([Size({1: 2, 'a': 'b', 0.9: None, False: str})])
        self.assertEqual(p.acc(), 4)
    #-def

    def test_Empty(self):
        p = CommandProcessor()

        p.run([Empty("")])
        self.assertTrue(p.acc())
        p.run([Empty("-*+")])
        self.assertFalse(p.acc())
        p.run([Empty(('i', 'j'))])
        self.assertFalse(p.acc())
        p.run([Empty([])])
        self.assertTrue(p.acc())
        p.run([Empty([1])])
        self.assertFalse(p.acc())
        p.run([Empty({})])
        self.assertTrue(p.acc())
        p.run([Empty({1: 2, 3: 4})])
        self.assertFalse(p.acc())
    #-def

    def test_Contains(self):
        p = CommandProcessor()

        p.run([Contains("abc", "a")])
        self.assertTrue(p.acc())
        with self.assertRaises(CommandProcessorError):
            p.run([Contains("abc", -1)])
        p.run([Contains("abc", "d")])
        self.assertFalse(p.acc())
        p.run([Contains((11, 2), None)])
        self.assertFalse(p.acc())
        p.run([Contains((11, 2), 2)])
        self.assertTrue(p.acc())
        p.run([Contains([11, 2, ('a', 'b')], ('a', 'b'))])
        self.assertTrue(p.acc())
        p.run([Contains([11, 2, ('a', 'b')], 0.125)])
        self.assertFalse(p.acc())
        p.run([Contains({'a': 4}, -1)])
        self.assertFalse(p.acc())
        p.run([Contains({'a': 4}, 'a')])
        self.assertTrue(p.acc())
    #-def

    def test_Count(self):
        p = CommandProcessor()

        p.run([Count("abaca", "a")])
        self.assertEqual(p.acc(), 3)
        with self.assertRaises(CommandProcessorError):
            p.run([Count("abc", -1)])
        p.run([Count("abc", "d")])
        self.assertEqual(p.acc(), 0)
        p.run([Count((11, 2), None)])
        self.assertEqual(p.acc(), 0)
        p.run([Count((11, 2), 2)])
        self.assertEqual(p.acc(), 1)
        p.run([Count((2, 2), 2)])
        self.assertEqual(p.acc(), 2)
        p.run([Count([11, 2, ('a', 'b')], ('a', 'b'))])
        self.assertEqual(p.acc(), 1)
        p.run([Count([11, 2, ('a', 'b')], 0.125)])
        self.assertEqual(p.acc(), 0)
        p.run([Count([11, 2, ('a', 'b'), 2], 2)])
        self.assertEqual(p.acc(), 2)
        with self.assertRaises(CommandProcessorError):
            p.run([Count({'a': 4}, 'a')])
    #-def

    def test_IsDigit(self):
        p = CommandProcessor()

        p.run([IsDigit('1')])
        self.assertTrue(p.acc())
        p.run([IsDigit("_1")])
        self.assertFalse(p.acc())
        p.run([IsDigit("")])
        self.assertFalse(p.acc())
    #-def

    def test_IsUpper(self):
        p = CommandProcessor()

        p.run([IsUpper("A_")])
        self.assertTrue(p.acc())
        p.run([IsUpper("aA")])
        self.assertFalse(p.acc())
        p.run([IsUpper("")])
        self.assertFalse(p.acc())
    #-def

    def test_IsLower(self):
        p = CommandProcessor()

        p.run([IsLower('a')])
        self.assertTrue(p.acc())
        p.run([IsLower("Aa")])
        self.assertFalse(p.acc())
        p.run([IsLower("")])
        self.assertFalse(p.acc())
    #-def

    def test_IsAlpha(self):
        p = CommandProcessor()

        p.run([IsAlpha('a')])
        self.assertTrue(p.acc())
        p.run([IsAlpha("A*")])
        self.assertTrue(p.acc())
        p.run([IsAlpha("*A")])
        self.assertFalse(p.acc())
        p.run([IsAlpha("")])
        self.assertFalse(p.acc())
    #-def

    def test_IsLetter(self):
        p = CommandProcessor()

        p.run([IsLetter('a')])
        self.assertTrue(p.acc())
        p.run([IsLetter("A*")])
        self.assertTrue(p.acc())
        p.run([IsLetter("_A*")])
        self.assertTrue(p.acc())
        p.run([IsLetter("*A")])
        self.assertFalse(p.acc())
        p.run([IsLetter("")])
        self.assertFalse(p.acc())
    #-def

    def test_IsAlnum(self):
        p = CommandProcessor()

        p.run([IsAlnum('1')])
        self.assertTrue(p.acc())
        p.run([IsAlnum("A*")])
        self.assertTrue(p.acc())
        p.run([IsAlnum("aA*")])
        self.assertTrue(p.acc())
        p.run([IsAlnum("*A")])
        self.assertFalse(p.acc())
        p.run([IsAlnum("")])
        self.assertFalse(p.acc())
    #-def

    def test_IsWord(self):
        p = CommandProcessor()

        p.run([IsWord('1')])
        self.assertTrue(p.acc())
        p.run([IsWord("A*")])
        self.assertTrue(p.acc())
        p.run([IsWord("_A*")])
        self.assertTrue(p.acc())
        p.run([IsWord("*A")])
        self.assertFalse(p.acc())
        p.run([IsWord("b*A")])
        self.assertTrue(p.acc())
        p.run([IsWord("")])
        self.assertFalse(p.acc())
    #-def

    def test_Keys(self):
        p = CommandProcessor()

        p.run([Keys({'a': 'b'})])
        self.assertEqual(p.acc(), ['a'])
        self.assertIsInstance(p.acc(), List)
    #-def

    def test_Values(self):
        p = CommandProcessor()

        p.run([Values({'a': 'b'})])
        self.assertEqual(p.acc(), ['b'])
        self.assertIsInstance(p.acc(), List)
    #-def

    def test_First(self):
        p = CommandProcessor()

        p.run([First(('x', 7))])
        self.assertEqual(p.acc(), 'x')
    #-def

    def test_Second(self):
        p = CommandProcessor()

        p.run([Second(('x', 7))])
        self.assertEqual(p.acc(), 7)
    #-def

    def test_GetItem(self):
        p = CommandProcessor()

        p.run([GetItem("abc", 1)])
        self.assertEqual(p.acc(), 'b')
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem("abc", "cs")])
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem("abc", -1)])
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem("abc", 4)])
        p.run([GetItem(('x', 7), 0)])
        self.assertEqual(p.acc(), 'x')
        p.run([GetItem(('x', 7), 1)])
        self.assertEqual(p.acc(), 7)
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem(('x', 7), 1.0)])
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem(('x', 7), -1)])
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem(('x', 7), 4)])
        p.run([GetItem([0.5, 'x', 7, "sd", 11], 3)])
        self.assertEqual(p.acc(), "sd")
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem([0.5, 'x', 7, "sd", 11], 'x')])
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem([0.5, 'x', 7, "sd", 11], -2)])
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem([0.5, 'x', 7, "sd", 11], 5)])
        p.run([GetItem({'a': 2}, 'a')])
        self.assertEqual(p.acc(), 2)
        with self.assertRaises(CommandProcessorError):
            p.run([GetItem({'a': 2}, -1)])
    #-def

    def test_Substr(self):
        p = CommandProcessor()

        p.run([Substr("hello", "ll")])
        self.assertEqual(p.acc(), 2)
        p.run([Substr("hello", "lw")])
        self.assertEqual(p.acc(), -1)
    #-def

    def test_Find(self):
        p = CommandProcessor()

        p.run([Find("abrakadabra", "bra", 1, 7)])
        self.assertEqual(p.acc(), 1)
        p.run([Find("abrakadabra", "bra", 2, 7)])
        self.assertEqual(p.acc(), -1)
        p.run([Find("abrakadabra", "e", 0, 11)])
        self.assertEqual(p.acc(), -1)
        p.run([Find("abrakadabra", "abrakadabra", 0, 11)])
        self.assertEqual(p.acc(), 0)
    #-def

    def test_RFind(self):
        p = CommandProcessor()

        p.run([RFind("abrakadabra", "bra", 1, 11)])
        self.assertEqual(p.acc(), 8)
        p.run([RFind("abrakadabra", "bra", 1, 10)])
        self.assertEqual(p.acc(), 1)
        p.run([RFind("abrakadabra", "bra", 2, 10)])
        self.assertEqual(p.acc(), -1)
        p.run([RFind("abrakadabra", "ar", 0, 11)])
        self.assertEqual(p.acc(), -1)
        p.run([RFind("abrakadabra", "abrakadabra", 0, 11)])
        self.assertEqual(p.acc(), 0)
    #-def

    def test_LStrip(self):
        p = CommandProcessor()

        p.run([LStrip("  x a  ")])
        self.assertEqual(p.acc(), "x a  ")
        p.run([LStrip("x a  ")])
        self.assertEqual(p.acc(), "x a  ")
    #-def

    def test_RStrip(self):
        p = CommandProcessor()

        p.run([RStrip("  x a  ")])
        self.assertEqual(p.acc(), "  x a")
        p.run([RStrip("  x a")])
        self.assertEqual(p.acc(), "  x a")
    #-def

    def test_Strip(self):
        p = CommandProcessor()

        p.run([Strip("  x a  ")])
        self.assertEqual(p.acc(), "x a")
        p.run([Strip("  x a")])
        self.assertEqual(p.acc(), "x a")
        p.run([Strip("x a  ")])
        self.assertEqual(p.acc(), "x a")
        p.run([Strip("x a")])
        self.assertEqual(p.acc(), "x a")
    #-def

    def test_ToUpper(self):
        p = CommandProcessor()

        p.run([ToUpper("(_1_aBcDeF_1_)")])
        self.assertEqual(p.acc(), "(_1_ABCDEF_1_)")
    #-def

    def test_ToLower(self):
        p = CommandProcessor()

        p.run([ToLower("(_1_aBcDeF_1_)")])
        self.assertEqual(p.acc(), "(_1_abcdef_1_)")
    #-def

    def test_Subst(self):
        p = CommandProcessor()

        p.run([Subst("a--b--c-", "--", "[+]")])
        self.assertEqual(p.acc(), "a[+]b[+]c-")
    #-def

    def test_Trans(self):
        tab = {"a": "?0", 1: "4f", "de": "XX", "d": "<Z>"}
        p = CommandProcessor()

        p.run([Trans("abcdefgh", tab)])
        self.assertEqual(p.acc(), "?0bc<Z>efgh")
    #-def

    def test_Sort(self):
        p = CommandProcessor()

        p.run([
            SetLocal('x', [2, 1, 4, 3]),
            SetLocal('y', Sort(GetLocal('x')))
        ])
        self.assertNotEqual(p.getenv()['x'], p.getenv()['y'])
        self.assertEqual(p.getenv()['y'], [1, 2, 3, 4])
        self.assertIsInstance(p.getenv()['y'], List)
    #-def

    def test_Reverse(self):
        p = CommandProcessor()

        p.run([
            SetLocal('x', [1, 'a', 0.25, "uu"]),
            SetLocal('y', Reverse(GetLocal('x')))
        ])
        self.assertNotEqual(p.getenv()['x'], p.getenv()['y'])
        self.assertEqual(p.getenv()['y'], ["uu", 0.25, 'a', 1])
        self.assertIsInstance(p.getenv()['y'], List)
    #-def

    def test_Unique(self):
        p = CommandProcessor()

        p.run([Unique([1, 2, 3, 2, 4, 5, 4])])
        self.assertEqual(p.acc(), [1, 2, 3, 4, 5])
        self.assertIsInstance(p.acc(), List)
        p.run([Unique([1, 3, 2])])
        self.assertEqual(p.acc(), [1, 3, 2])
        self.assertIsInstance(p.acc(), List)
    #-def

    def test_Split(self):
        p = CommandProcessor()

        p.run([Split("a..b..c. ..", "..")])
        self.assertEqual(p.acc(), ["a", "b", "c. ", ""])
        self.assertIsInstance(p.acc(), List)
    #-def
#-class

class TestIfCase(unittest.TestCase):

    def test_If(self):
        p = CommandProcessor()

        p.run([
            If(True, [1], [2])
        ])
        self.assertEqual(p.acc(), 1)
        p.run([
            If(False, [1], [2])
        ])
        self.assertEqual(p.acc(), 2)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLocationCase))
    suite.addTest(unittest.makeSuite(TestCommandCase))
    suite.addTest(unittest.makeSuite(TestSetLocalCase))
    suite.addTest(unittest.makeSuite(TestGetLocalCase))
    suite.addTest(unittest.makeSuite(TestOperationsCase))
    suite.addTest(unittest.makeSuite(TestIfCase))
    return suite
#-def
