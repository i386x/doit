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
    UserType, \
    ExceptionClass, \
    Procedure

from doit.text.pgen.readers.glap.cmd.commands import \
    Location, \
    CommandContext, \
    Command, \
    SetLocal, \
    GetLocal, \
    Define, \
    Operation, \
    Add, Sub, Mul, Div, Mod, Neg, \
    BitAnd, BitOr, BitXor, ShiftL, ShiftR, Inv, \
    Lt, Gt, Le, Ge, Eq, Ne, Is, \
    And, Or, Not, \
    NewPair, \
    Copy, Slice, Concat, Join, Merge, \
    Strlen, Size, Empty, Contains, Count, \
    IsDigit, IsUpper, IsLower, IsAlpha, IsLetter, IsAlnum, IsWord, \
    Keys, Values, \
    First, Second, GetItem, \
    Substr, Find, RFind, \
    LStrip, RStrip, Strip, ToUpper, ToLower, Subst, Trans, \
    Sort, Reverse, Unique, \
    Split, \
    ToBool, ToInt, ToFlt, ToStr, ToPair, ToList, ToHash, \
    All, Any, SeqOp, Map, Filter, \
    Lambda, \
    Block, If, Foreach, \
    Call, ECall, Return, \
    SetItem, DelItem, Append, Insert, Remove, RemoveAll, \
    Each, Visit, \
    Print

from doit.text.pgen.readers.glap.cmd.eval import \
    Environment, \
    CommandProcessor

class UT_000(UserType):
    __slots__ = [ 'left', 'right' ]

    def __init__(self):
        UserType.__init__(self)
        self.left = UT_001(3)
        self.right = UT_001(7)
    #-def

    def to_bool(self, processor):
        return False
    #-def

    def to_int(self, processor):
        return 8
    #-def

    def to_float(self, processor):
        return 1.8
    #-def

    def to_str(self, processor):
        return "what"
    #-def

    def to_pair(self, processor):
        return Pair('x', 9)
    #-def

    def to_list(self, processor):
        return List(['a', 4, 'z'])
    #-def

    def to_hash(self, processor):
        return HashMap({1.25: "gosh!"})
    #-def

    def visit(self, processor, f, *args):
        processor.insertcode(
            Call(f,
                0,
                ECall(self.left.visit, processor, f, *args),
                ECall(self.right.visit, processor, f, *args),
                *args
            )
        )
    #-def
#-class

class UT_001(UserType):
    __slots__ = [ 'v' ]

    def __init__(self, v):
        UserType.__init__(self)
        self.v = v
    #-def

    def visit(self, processor, f, *args):
        processor.insertcode(
            Call(f, 1, self.v, *args)
        )
    #-def
#-class

class Printer(CommandProcessor):
    __slots__ = [ 'output' ]

    def __init__(self, env = None):
        CommandProcessor.__init__(self, env)
        self.output = ""
    #-def

    def print_impl(self, s):
        self.output += s
    #-def
#-class

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
        ctx = CommandContext(c)

        self.assertEqual(c.name, 'command')
        self.assertEqual(c.location, Location())
        self.assertFalse(c.isfunc())
        c.set_location("X.f", 5, 8)
        self.assertEqual(str(c), '"command" at ["X.f":5:8]')
        c.help(p)
        c.enter(p, ctx)
        c.expand(p)
        c.leave(p, ctx)
        p.setacc(56)
        c.pushacc(p)
        self.assertEqual(p.popval(), 56)
        self.assertIsNone(
            c.find_exception_handler(ctx, CommandError(p.TypeError, ""))
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

    def test_arity(self):
        p = CommandProcessor()
        add1 = Operation(1, 2, 3)
        add1.name = 'add'
        add2 = Operation(1)
        add2.name = 'add'
        add3 = Operation()
        add3.name = 'add'

        with self.assertRaises(CommandProcessorError):
            p.run([add1])
        with self.assertRaises(CommandProcessorError):
            p.run([add2])
        with self.assertRaises(CommandProcessorError):
            p.run([add3])
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

    def test_NewPair(self):
        p = CommandProcessor()

        p.run([
            SetLocal('a', 1),
            SetLocal('v', "***"),
            NewPair(GetLocal('a'), GetLocal('v'))
        ])
        self.assertEqual(p.acc(), (1, "***"))
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

    def test_ToBool(self):
        p = CommandProcessor()

        p.run([ToBool(True)])
        self.assertIs(p.acc(), True)
        p.run([ToBool(False)])
        self.assertIs(p.acc(), False)
        p.run([ToBool(0)])
        self.assertIs(p.acc(), False)
        p.run([ToBool(0.0)])
        self.assertIs(p.acc(), False)
        p.run([ToBool(12)])
        self.assertIs(p.acc(), True)
        p.run([ToBool(1.2)])
        self.assertIs(p.acc(), True)
        p.run([ToBool("")])
        self.assertIs(p.acc(), False)
        p.run([ToBool("asd")])
        self.assertIs(p.acc(), True)
        p.run([ToBool((1, 2))])
        self.assertIs(p.acc(), True)
        p.run([ToBool([])])
        self.assertIs(p.acc(), False)
        p.run([ToBool([[]])])
        self.assertIs(p.acc(), True)
        p.run([ToBool({})])
        self.assertIs(p.acc(), False)
        p.run([ToBool({1: 2, 'a': 4})])
        self.assertIs(p.acc(), True)
        p.run([ToBool(UserType())])
        self.assertIs(p.acc(), True)
        p.run([ToBool(UT_000())])
        self.assertIs(p.acc(), False)
        p.run([ToBool(Procedure(1, 2, 3, 4, 5, 6))])
        self.assertIs(p.acc(), True)
        p.run([ToBool(p.Null)])
        self.assertIs(p.acc(), False)
    #-def

    def test_ToInt(self):
        p = CommandProcessor()

        p.run([ToInt(False)])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), 0)
        p.run([ToInt(True)])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), 1)
        p.run([ToInt(2)])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), 2)
        p.run([ToInt(-1.5)])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), -1)
        p.run([ToInt("2")])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), 2)
        p.run([ToInt("-1.5")])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), -1)
        with self.assertRaises(CommandProcessorError):
            p.run([ToInt("-1.5x")])
        with self.assertRaises(CommandProcessorError):
            p.run([ToInt(UserType())])
        p.run([ToInt(UT_000())])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), 8)
        with self.assertRaises(CommandProcessorError):
            p.run([ToInt({})])
    #-def

    def test_ToFlt(self):
        p = CommandProcessor()

        p.run([ToFlt(False)])
        self.assertIsInstance(p.acc(), float)
        self.assertEqual(p.acc(), 0.0)
        p.run([ToFlt(True)])
        self.assertIsInstance(p.acc(), float)
        self.assertEqual(p.acc(), 1.0)
        p.run([ToFlt(1)])
        self.assertIsInstance(p.acc(), float)
        self.assertEqual(p.acc(), 1.0)
        p.run([ToFlt(1.2)])
        self.assertIsInstance(p.acc(), float)
        self.assertEqual(p.acc(), 1.2)
        p.run([ToFlt("1.2")])
        self.assertIsInstance(p.acc(), float)
        self.assertEqual(p.acc(), 1.2)
        p.run([ToFlt("1")])
        self.assertIsInstance(p.acc(), float)
        self.assertEqual(p.acc(), 1.0)
        with self.assertRaises(CommandProcessorError):
            p.run([ToFlt("1.5x")])
        with self.assertRaises(CommandProcessorError):
            p.run([ToFlt(UserType())])
        p.run([ToFlt(UT_000())])
        self.assertIsInstance(p.acc(), float)
        self.assertEqual(p.acc(), 1.8)
        with self.assertRaises(CommandProcessorError):
            p.run([ToFlt({})])
    #-def

    def test_ToStr(self):
        p = CommandProcessor()

        # invalid specs:
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(1, 2)])
        # bool:
        # - defaults:
        p.run([ToStr(True)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "true")
        p.run([ToStr(False)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "false")
        # - custom:
        s = dict(strue = "X", sfalse = "Y")
        p.run([ToStr(True, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "X")
        p.run([ToStr(False, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "Y")
        # - invalid:
        s = dict(sfalse = 1)
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(True, s)])
        # int:
        # - defaults:
        p.run([ToStr(14)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "14")
        # - common flags:
        s = dict(flags = "+")
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "+14")
        # - specific flags:
        s = dict(iflags = " ", flags = "+")
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), " 14")
        # - invalid flags:
        s = dict(iflags = 0)
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(0, s)])
        s = dict(iflags = " -+0*")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(0, s)])
        # - common size:
        s = dict(size = 4)
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "  14")
        # - specific size:
        s = dict(size = 4, isize = 6)
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "    14")
        # - invalid size:
        s = dict(isize = "0")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(0, s)])
        # - common precision:
        s = dict(prec = 3)
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "014")
        # - specific precision:
        s = dict(prec = 3, iprec = 4)
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "0014")
        # - invalid precision:
        s = dict(iprec = "0")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(0, s)])
        # - display types:
        s = dict(itype = "o")
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "16")
        s = dict(itype = "x")
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "e")
        s = dict(itype = "X")
        p.run([ToStr(14, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "E")
        # - invalid display type:
        s = dict(itype = "?")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(14, s)])
        # - all specs together:
        s = dict(flags = " -+0", size = 8, prec = 4, itype = "X")
        p.run([ToStr(1408, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "+0580   ")
        # float:
        # - defaults:
        p.run([ToStr(1.25)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "1.250000")
        # - common flags:
        s = dict(flags = "+")
        p.run([ToStr(1.25, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "+1.250000")
        # - specific flags:
        s = dict(fflags = " ", flags = "+")
        p.run([ToStr(1.25, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), " 1.250000")
        # - invalid flags:
        s = dict(fflags = 0)
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(1.5, s)])
        s = dict(fflags = " -+0*")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(1.5, s)])
        # - common size:
        s = dict(size = 6, prec = 2)
        p.run([ToStr(1.25, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "  1.25")
        # - specific size:
        s = dict(size = 6, fsize = 8, prec = 3)
        p.run([ToStr(1.125, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "   1.125")
        # - invalid size:
        s = dict(fsize = "0")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(0.1, s)])
        # - common precision:
        s = dict(prec = 3)
        p.run([ToStr(1.5, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "1.500")
        # - specific precision:
        s = dict(prec = 3, fprec = 4)
        p.run([ToStr(1.5, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "1.5000")
        # - invalid precision:
        s = dict(fprec = "0")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(0.1, s)])
        # - display types:
        s = dict(ftype = "e")
        p.run([ToStr(0.0625, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "6.250000e-02")
        s = dict(ftype = "E")
        p.run([ToStr(0.0625, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "6.250000E-02")
        # - invalid display type:
        s = dict(ftype = "g")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(0.1, s)])
        # - all specs together:
        s = dict(flags = "+0", size = 15, prec = 7, ftype = "E")
        p.run([ToStr(1.0/128, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "+07.8125000E-03")
        # str:
        p.run([ToStr("abc")])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "abc")
        # user type:
        p.run([ToStr(UT_000())])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "what")
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(UserType())])
        # procedure:
        p.run([ToStr(Procedure("f1", 0, 0, 0, 0, 0))])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "f1")
        # null:
        # - defaults:
        p.run([ToStr(p.Null)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "null")
        # - custom:
        s = dict(snull = "nope")
        p.run([ToStr(p.Null, s)])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "nope")
        # - invalid:
        s = dict(snull = 1)
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr(p.Null, s)])
        # unconvertible:
        with self.assertRaises(CommandProcessorError):
            p.run([ToStr({})])
    #-def

    def test_ToPair(self):
        p = CommandProcessor()

        p.run([ToPair("ab")])
        self.assertIsInstance(p.acc(), Pair)
        self.assertEqual(p.acc(), ('a', 'b'))
        p.run([ToPair((1, "xyx"))])
        self.assertIsInstance(p.acc(), Pair)
        self.assertEqual(p.acc(), (1, "xyx"))
        p.run([ToPair([2, "uxv"])])
        self.assertIsInstance(p.acc(), Pair)
        self.assertEqual(p.acc(), (2, "uxv"))
        p.run([ToPair(UT_000())])
        self.assertIsInstance(p.acc(), Pair)
        self.assertEqual(p.acc(), ('x', 9))
        with self.assertRaises(CommandProcessorError):
            p.run([ToPair(UserType())])
        with self.assertRaises(CommandProcessorError):
            p.run([ToPair([1, 2, 3])])
        with self.assertRaises(CommandProcessorError):
            p.run([ToPair(0)])
    #-def

    def test_ToList(self):
        p = CommandProcessor()

        p.run([ToList("abcd")])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), ['a', 'b', 'c', 'd'])
        p.run([ToList((2, 7))])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [2, 7])
        p.run([ToList([1, 'a', 0.5])])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [1, 'a', 0.5])
        p.run([ToList({0.25: "uv"})])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [(0.25, "uv")])
        p.run([ToList(UT_000())])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), ['a', 4, 'z'])
        with self.assertRaises(CommandProcessorError):
            p.run([ToList(UserType())])
        with self.assertRaises(CommandProcessorError):
            p.run([ToList(0)])
    #-def

    def test_ToHash(self):
        p = CommandProcessor()

        p.run([ToHash(('a', 0.5))])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {'a': 0.5})
        with self.assertRaises(CommandProcessorError):
            p.run([ToHash([(1, 2), "a"])])
        with self.assertRaises(CommandProcessorError):
            p.run([ToHash([(1, 2), (1, 2, 3)])])
        with self.assertRaises(CommandProcessorError):
            p.run([ToHash([(1, 2), Procedure(1, 2, 3, 4, 5, 6)])])
        p.run([ToHash([])])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {})
        p.run([ToHash([('a', 0.5), (1, "uv")])])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {1: "uv", 'a': 0.5})
        p.run([ToHash({1: 2, 3: 4})])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {3: 4, 1: 2})
        p.run([ToHash(UT_000())])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {1.25: "gosh!"})
        with self.assertRaises(CommandProcessorError):
            p.run([ToHash(UserType())])
        with self.assertRaises(CommandProcessorError):
            p.run([ToHash(0)])
    #-def

    def test_Quantifier(self):
        p = CommandProcessor()
        prog = [
            Define("even", [], ["x"], False, [
                Return(Eq(Mod(GetLocal("x"), 2), 0))
            ]),
            Define("islower", [], ["c"], False, [
                Return(IsLower(GetLocal("c")))
            ]),
            Define("p", [], ["x"], False, [
                If(Ne(GetLocal("x"), 0), [
                    Return(True)
                ], [
                    Return({})
                ])
            ])
        ]

        p.run(prog)
        p.run([All([], GetLocal("even"))])
        self.assertTrue(p.acc())
        p.run([All([0], GetLocal("even"))])
        self.assertTrue(p.acc())
        p.run([All([0, 2, 4, 6], GetLocal("even"))])
        self.assertTrue(p.acc())
        p.run([All([0, 2, 4, 6, 11, 8, 12], GetLocal("even"))])
        self.assertFalse(p.acc())
        p.run([All([0, 2, 4, 6, 11, 8, 12, 1], GetLocal("even"))])
        self.assertFalse(p.acc())
        p.run([All("", GetLocal("islower"))])
        self.assertTrue(p.acc())
        p.run([All("abcdefgh", GetLocal("islower"))])
        self.assertTrue(p.acc())
        p.run([All("abcdefGh", GetLocal("islower"))])
        self.assertFalse(p.acc())
        with self.assertRaises(CommandProcessorError):
            p.run([All("", 0)])
        with self.assertRaises(CommandProcessorError):
            p.run([All(0, GetLocal("even"))])
        with self.assertRaises(CommandProcessorError):
            p.run([All([0, 2, 4, 6, 11, 8, 12, 1, "av"], GetLocal("even"))])
        p.run([All([], GetLocal("p"))])
        self.assertTrue(p.acc())
        with self.assertRaises(CommandProcessorError):
            p.run([All(['a', "uv", 0.25, 0], GetLocal("p"))])
        p.run([Any([], GetLocal("even"))])
        self.assertFalse(p.acc())
        p.run([Any([3, 1, 5, 7, 11], GetLocal("even"))])
        self.assertFalse(p.acc())
        p.run([Any([3, 1, 5, 7, 11, 2, 99, 101], GetLocal("even"))])
        self.assertTrue(p.acc())
        p.run([Any([3, 1, 5, 7, 11, 2, 99, 101, 4, 1], GetLocal("even"))])
        self.assertTrue(p.acc())
    #-def

    def test_SeqOp(self):
        p = CommandProcessor()
        prog = [
            Define("even", [], ["x"], False, [
                Return(Eq(Mod(GetLocal("x"), 2), 0))
            ]),
            Define("incr", [], ["x"], False, [
                Return(Add(GetLocal("x"), 1))
            ]),
            Define("upper", [], ["x"], False, [
                Return(ToUpper(GetLocal("x")))
            ])
        ]

        p.run(prog)
        with self.assertRaises(CommandProcessorError):
            p.run([Map([], 0)])
        with self.assertRaises(CommandProcessorError):
            p.run([Map(0, GetLocal("incr"))])
        p.run([Map("abc", GetLocal("upper"))])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), ['A', 'B', 'C'])
        p.run([Map("", GetLocal("incr"))])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [])
        with self.assertRaises(CommandProcessorError):
            p.run([SeqOp((1, 2), GetLocal("incr"), Lambda(["x", "y"], False, [
                Return(0)
            ], []))])
        with self.assertRaises(CommandProcessorError):
            p.run([SeqOp((1, 2), GetLocal("incr"), Lambda(["x", "y"], False, [
                Return(NewPair(0, 1))
            ], []))])
        p.run([Map((3, 4), GetLocal("incr"))])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [4, 5])
        with self.assertRaises(CommandProcessorError):
            p.run([Filter((3, 4), GetLocal("incr"))])
        p.run([Filter((3, 4), GetLocal("even"))])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [4])
        p.run([Filter([1, 3, 5], GetLocal("even"))])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [])
        p.run([Filter([], GetLocal("even"))])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [])
        p.run([Filter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], GetLocal("even"))])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [0, 2, 4, 6, 8])
    #-def
#-class

class TestBlockCase(unittest.TestCase):

    def test_Block(self):
        p = CommandProcessor()

        p.run([
            SetLocal("x", "abc"),
            Block(
                SetLocal("x", "def"),
                SetLocal("y", 1)
            )
        ])
        self.assertEqual(p.getenv().getvar("x"), "abc")
        with self.assertRaises(CommandError):
            p.getenv().getvar("y")
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

class TestForeachCase(unittest.TestCase):

    def test_Foreach(self):
        p = CommandProcessor()

        p.run([
            SetLocal("x", 0),
            Foreach("i", [], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ])
        ])
        self.assertEqual(p.getenv()["x"], 0)
        with self.assertRaises(CommandError):
            p.getenv().getvar("i")
        p.run([
            SetLocal("x", 0),
            Foreach("i", [1], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ])
        ])
        self.assertEqual(p.getenv()["x"], 1)
        self.assertEqual(p.getenv()["i"], 1)
        p.run([
            SetLocal("x", 2),
            Foreach("j", [1, 8, 5], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("j")))
            ])
        ])
        self.assertEqual(p.getenv()["x"], 16)
        self.assertEqual(p.getenv()["i"], 1)
        self.assertEqual(p.getenv()["j"], 5)
        p.run([
            SetLocal("x", 2),
            Foreach("k", "", [
                SetLocal("x", Add(GetLocal("x"), GetLocal("k")))
            ])
        ])
        self.assertEqual(p.getenv()["x"], 2)
        self.assertEqual(p.getenv()["i"], 1)
        self.assertEqual(p.getenv()["j"], 5)
        with self.assertRaises(CommandError):
            p.getenv().getvar("k")
        p.run([
            SetLocal("x", 2),
            Foreach("k", "uiv", [
                SetLocal("x", Add(GetLocal("x"), 1))
            ])
        ])
        self.assertEqual(p.getenv()["x"], 5)
        self.assertEqual(p.getenv()["i"], 1)
        self.assertEqual(p.getenv()["j"], 5)
        self.assertEqual(p.getenv()["k"], "v")
        with self.assertRaises(CommandProcessorError):
            p.run([
                SetLocal("x", 2),
                Foreach("l", 0, [
                    SetLocal("x", Add(GetLocal("x"), 1))
                ])
            ])
        self.assertEqual(p.getenv()["x"], 2)
        self.assertEqual(p.getenv()["i"], 1)
        self.assertEqual(p.getenv()["j"], 5)
        self.assertEqual(p.getenv()["k"], "v")
    #-def
#-class

class TestCallCase(unittest.TestCase):

    def test_Call(self):
        p = CommandProcessor()

        # no proc
        program = [
            SetLocal("my_proc", 0),
            Call(GetLocal("my_proc"))
        ]
        with self.assertRaises(CommandProcessorError):
            p.run(program)
        # args (no vararg)
        program = [
            Define("sum", [], ["a", "b"], False, [
                Return(Add(GetLocal("a"), GetLocal("b")))
            ])
        ]
        p.run(program)
        with self.assertRaises(CommandProcessorError):
            p.run([Call(GetLocal("sum"))])
        with self.assertRaises(CommandProcessorError):
            p.run([Call(GetLocal("sum"), 1)])
        p.run([Call(GetLocal("sum"), 1, 2)])
        self.assertEqual(p.acc(), 3)
        with self.assertRaises(CommandProcessorError):
            p.run([Call(GetLocal("sum"), 1, 2, 3)])
        with self.assertRaises(CommandProcessorError):
            p.run([Call(GetLocal("sum"), 1, 2, 3, 4)])
        # args (vararg)
        program = [
            Define("reflect", [], ["args"], True, [
                Return(GetLocal("args"))
            ]),
            Define("reflect_as_pair", [], ["x", "args"], True, [
                Return(NewPair(GetLocal("x"), GetLocal("args")))
            ])
        ]
        p.run(program)
        p.run([Call(GetLocal("reflect"))])
        self.assertEqual(p.acc(), [])
        p.run([Call(GetLocal("reflect"), 1, 'a', 0.25, {'p': 1.5})])
        self.assertEqual(p.acc(), [1, 'a', 0.25, {'p': 1.5}])
        with self.assertRaises(CommandProcessorError):
            p.run([Call(GetLocal("reflect_as_pair"))])
        p.run([Call(GetLocal("reflect_as_pair"), 'z')])
        self.assertEqual(p.acc(), ('z', []))
        p.run([Call(GetLocal("reflect_as_pair"), 'z', 4)])
        self.assertEqual(p.acc(), ('z', [4]))
        p.run([Call(GetLocal("reflect_as_pair"), 'z', 4, "uv")])
        self.assertEqual(p.acc(), ('z', [4, "uv"]))
        # bounds: 0, params: 0, varargs: 0, return: 0
        program = [
            Define("get_leaf", [], [], False, [
                0x1e4f
            ]),
            Call(GetLocal("get_leaf"))
        ]
        p.run(program)
        self.assertEqual(p.acc(), 0x1e4f)
        # bounds: 0, params: 0, varargs: 0, return: 1
        program = [
            Define("get_result", [], [], False, [
                Return(Concat(ToStr(Mul(2, 6)), " apes"))
            ]),
            Call(GetLocal("get_result"))
        ]
        p.run(program)
        self.assertEqual(p.acc(), "12 apes")
        # bounds: 1, params: 1, varargs: 0, return: 1
        program = [
            SetLocal("t", "<t>"),
            SetLocal("x", "<x>"),
            SetLocal("y", "<y>"),
            Define("f", ["t"], ["x", "y"], False, [
                If(Lt(GetLocal("x"), GetLocal("y")), [
                    Return(GetLocal("t"))
                ], [
                    SetLocal("t", Sub(GetLocal("x"), GetLocal("y"))),
                    Return(GetLocal("t"))
                ])
            ]),
            SetLocal("be_null", Call(GetLocal("f"), 0, 1)),
            SetLocal("be_seven", Call(GetLocal("f"), 21, 14))
        ]
        p.run(program)
        self.assertEqual(p.getenv()["t"], "<t>")
        self.assertEqual(p.getenv()["x"], "<x>")
        self.assertEqual(p.getenv()["y"], "<y>")
        self.assertIs(p.getenv()["be_null"], p.Null)
        self.assertEqual(p.getenv()["be_seven"], 7)
        # function as argument
        program = [
            Define("times", [], ["x", "y"], False, [
                Return(Mul(GetLocal("x"), GetLocal("y")))
            ]),
            Define("summ", [], ["x", "y"], False, [
                Return(Add(GetLocal("x"), GetLocal("y")))
            ]),
            Define("binop", [], ["f", "x", "y"], False, [
                Return(Call(GetLocal("f"), GetLocal("x"), GetLocal("y")))
            ])
        ]
        p.run(program)
        p.run([Call(GetLocal("binop"), GetLocal("times"), 3, 4)])
        self.assertEqual(p.acc(), 12)
        p.run([Call(GetLocal("binop"), GetLocal("summ"), 3, 4)])
        self.assertEqual(p.acc(), 7)
        # recursion
        program = [
            Define("fibo", [], ["n"], False, [
                If(Le(GetLocal("n"), 1), [
                    Return(GetLocal("n"))
                ], [
                    Return(Add(
                        Call(GetLocal("fibo"), Sub(GetLocal("n"), 2)),
                        Call(GetLocal("fibo"), Sub(GetLocal("n"), 1))
                    ))
                ])
            ])
        ]
        p.run(program)
        p.run([Call(GetLocal("fibo"), 10)])
        self.assertEqual(p.acc(), 55)
        # high order functions + outer bound
        program = [
            Define("new_counter", [], ["x"], False, [
                Return(Lambda([], False, [
                    SetLocal("x", Add(GetLocal("x"), 1), 1),
                    Return(GetLocal("x"))
                ], []))
            ])
        ]
        p.run(program)
        p.run([
            SetLocal("x", "!!!"),
            SetLocal("cf", Call(GetLocal("new_counter"), 0)),
            SetLocal("cg", Call(GetLocal("new_counter"), 5)),
            SetLocal("be_1", Call(GetLocal("cf"))),
            SetLocal("be_6", Call(GetLocal("cg"))),
            SetLocal("be_2", Call(GetLocal("cf"))),
            SetLocal("be_3", Call(GetLocal("cf"))),
            SetLocal("be_7", Call(GetLocal("cg"))),
            SetLocal("be_8", Call(GetLocal("cg")))
        ])
        self.assertEqual(p.getenv()["x"], "!!!")
        self.assertEqual(p.getenv()["be_1"], 1)
        self.assertEqual(p.getenv()["be_2"], 2)
        self.assertEqual(p.getenv()["be_3"], 3)
        self.assertEqual(p.getenv()["be_6"], 6)
        self.assertEqual(p.getenv()["be_7"], 7)
        self.assertEqual(p.getenv()["be_8"], 8)
        program = [
            SetLocal("__x", 3),
            SetLocal("__y", 2),
            SetLocal("__c", 1),
            SetLocal("__z", 0),
            Define("__g", [], ["__x"], False, [
                If(Gt(GetLocal("__x"), 0), [Block(
                    SetLocal("__y", Add(GetLocal("__x"), 1)),
                    SetLocal("__c", Call(GetLocal("__g"), Mod(
                        Mul(GetLocal("__y"), 2), 7
                    ))),
                    Return(GetLocal("__c"))
                )], [Block(
                    SetLocal("__z", GetLocal("__y")),
                    Return(GetLocal("__z"))
                )])
            ])
        ]
        p.run(program)
        p.run([Call(GetLocal("__g"), 9)])
        self.assertEqual(p.acc(), 2)
        self.assertEqual(p.getenv()["__x"], 3)
        self.assertEqual(p.getenv()["__y"], 2)
        self.assertEqual(p.getenv()["__c"], 1)
        self.assertEqual(p.getenv()["__z"], 0)
    #-def

    def test_ECall(self):
        p = CommandProcessor()
        def f_():
            pass
        def g_(a, b, c):
            pass

        with self.assertRaises(CommandProcessorError):
            p.run([ECall(0)])
        with self.assertRaises(CommandProcessorError):
            p.run([ECall((lambda a, b: a / b), "a", 2)])
        with self.assertRaises(CommandProcessorError):
            p.run([ECall((lambda a, b: a / b), 1, 2, 3)])
        p.run([ECall(f_)])
        self.assertIs(p.acc(), p.Null)
        p.run([ECall((lambda a, b: a / b), 1, 2)])
        self.assertEqual(p.acc(), 0.5)
        p.run([ECall(g_, 0, 1, {})])
        self.assertIs(p.acc(), p.Null)
    #-def
#-class

class TestSetItemCase(unittest.TestCase):

    def test_SetItem(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([
                SetLocal('x', 0),
                SetItem(GetLocal('x'), 1, "u")
            ])
        with self.assertRaises(CommandProcessorError):
            p.run([
                SetLocal('x', [1, 2, 3]),
                SetItem(GetLocal('x'), 'a', "u")
            ])
        with self.assertRaises(CommandProcessorError):
            p.run([
                SetLocal('x', [1, 2, 3]),
                SetItem(GetLocal('x'), -1, "u")
            ])
        with self.assertRaises(CommandProcessorError):
            p.run([
                SetLocal('x', [1, 2, 3]),
                SetItem(GetLocal('x'), 3, "u")
            ])
        p.run([
            SetLocal('x', [1, 2, 3]),
            SetLocal('y', {}),
            SetItem(GetLocal('x'), 1, "u"),
            SetItem(GetLocal('y'), "abc", 1),
            SetItem(GetLocal('y'), "abc", 2),
            SetItem(GetLocal('y'), 3, "uv")
        ])
        self.assertEqual(p.getenv()['x'], [1, "u", 3])
        self.assertEqual(p.getenv()['y'], {"abc": 2, 3: "uv"})
    #-def
#-class

class TestDelItemCase(unittest.TestCase):

    def test_DelItem(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([DelItem(0, "c")])
        with self.assertRaises(CommandProcessorError):
            p.run([DelItem([0], "v")])
        with self.assertRaises(CommandProcessorError):
            p.run([DelItem([0], -1)])
        with self.assertRaises(CommandProcessorError):
            p.run([DelItem([0], 1)])
        p.run([
            SetLocal('x', [1, 2, 3]),
            DelItem(GetLocal('x'), 1),
            SetLocal('y', {1: 'a', "xy": 2, 0.25: "uv"}),
            DelItem(GetLocal('y'), "zz"),
            DelItem(GetLocal('y'), "xy"),
            DelItem(GetLocal('y'), "xy")
        ])
        self.assertEqual(p.getenv()['x'], [1, 3])
        self.assertEqual(p.getenv()['y'], {1: 'a', 0.25: "uv"})
    #-def
#-class

class TestAppendCase(unittest.TestCase):

    def test_Append(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([Append(0, 0)])
        with self.assertRaises(CommandProcessorError):
            p.run([Append({}, 0)])
        p.run([
            SetLocal('x', ["uy"]),
            Append(GetLocal('x'), 42),
            Append(GetLocal('x'), 1.5)
        ])
        self.assertEqual(p.getenv()['x'], ["uy", 42, 1.5])
    #-def
#-class

class TestInsertCase(unittest.TestCase):

    def test_Insert(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([Insert({}, 0, 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Insert([1, 2], 'a', 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Insert([1, 2], -1, 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Insert([1, 2], 3, 1)])
        p.run([
            SetLocal('x', ['a', 'b', 'c']),
            Insert(GetLocal('x'), 0, '_'),
            Insert(GetLocal('x'), 0, {1: 'i'}),
            Insert(GetLocal('x'), 5, 12),
            Insert(GetLocal('x'), 6, 13),
            Insert(GetLocal('x'), 3, '|')
        ])
        self.assertEqual(
            p.getenv()['x'], [{1: 'i'}, '_', 'a', '|', 'b', 'c', 12, 13]
        )
    #-def
#-class

class TestRemoveCase(unittest.TestCase):

    def test_Remove(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([Remove({}, 0)])
        p.run([
            SetLocal('x', [1, 2, 3, 1]),
            Remove(GetLocal('x'), 'a'),
            Remove(GetLocal('x'), 1),
            Remove(GetLocal('x'), 3),
            Remove(GetLocal('x'), 1),
            Remove(GetLocal('x'), 1)
        ])
        self.assertEqual(p.getenv()['x'], [2])
    #-def
#-class

class TestRemoveAllCase(unittest.TestCase):

    def test_RemoveAll(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([RemoveAll({}, 0)])
        p.run([
            SetLocal('x', [1, 2, 1, 1, 3, 1, 1, 2, 1]),
            RemoveAll(GetLocal('x'), 'a'),
            RemoveAll(GetLocal('x'), 1),
            RemoveAll(GetLocal('x'), 3)
        ])
        self.assertEqual(p.getenv()['x'], [2, 2])
    #-def
#-class

class TestEachCase(unittest.TestCase):

    def test_Each(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([Each({}, Lambda([], False, [Return()], []), 0, 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Each([], 0, 0, 1)])
        p.run([Each([], Lambda([], False, [Return()], []))])
        p.run([Each([], Lambda([], False, [Return()], []), 0, 1)])
        with self.assertRaises(CommandProcessorError):
            p.run([Each([1], Lambda([], False, [Return()], []), 0, 1)])
        p.run([
            Each([1], Lambda(['x', 'y', 'z'], False, [Return()], []), 0, 1)
        ])
        with self.assertRaises(CommandProcessorError):
            p.run([
                Each([1], Lambda(
                    ['x', 'y', 'z'], False, [Return()], []
                ), 0, 1, 2)
            ])
        p.run([
            SetLocal('x', []),
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x'))
        ])
        self.assertEqual(p.getenv()['x'], [18, 50, 98])
    #-def
#-class

class TestVisitCase(unittest.TestCase):

    def test_Visit(self):
        p = CommandProcessor()
        u = UT_000()
        f = Lambda(['n', 'args'], True, [
            If(Eq(GetLocal('n'), 0), [
                Return(
                    Concat("(0: ",
                    Concat(GetItem(GetLocal('args'), 0),
                    Concat(" ",
                    Concat(GetItem(GetLocal('args'), 1),
                    Concat(" ",
                    Concat(ToStr(GetItem(GetLocal('args'), 2)),
                    Concat(" ",
                    Concat(GetItem(GetLocal('args'), 3), ")"
                    ))))))))
                )
            ], [If(Eq(GetLocal('n'), 1), [
                Return(
                    Concat("(1: ",
                    Concat(ToStr(GetItem(GetLocal('args'), 0)),
                    Concat(" ",
                    Concat(ToStr(GetItem(GetLocal('args'), 1)),
                    Concat(" ",
                    Concat(GetItem(GetLocal('args'), 2), ")"
                    ))))))
                )
            ], [
                Return()
            ])])
        ], [])

        with self.assertRaises(CommandProcessorError):
            p.run([Visit([], Lambda([], False, [Return()], []), "x", "y")])
        with self.assertRaises(CommandProcessorError):
            p.run([Visit(u, 0)])
        p.run([Visit(u, f, 0, "x", "y")])
        self.assertEqual(p.acc(), "(0: (1: 3 0 x) (1: 7 0 x) 0 x)")
    #-def
#-class

class TestPrintCase(unittest.TestCase):

    def test_Print(self):
        p = Printer()

        p.run([SetLocal("x", 2), Print(
            "(", 1, " + ", GetLocal("x"), " = ", Add(1, GetLocal("x")), ")"
        )])
        self.assertEqual(p.output, "(1 + 2 = 3)")
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLocationCase))
    suite.addTest(unittest.makeSuite(TestCommandCase))
    suite.addTest(unittest.makeSuite(TestSetLocalCase))
    suite.addTest(unittest.makeSuite(TestGetLocalCase))
    suite.addTest(unittest.makeSuite(TestOperationsCase))
    suite.addTest(unittest.makeSuite(TestBlockCase))
    suite.addTest(unittest.makeSuite(TestIfCase))
    suite.addTest(unittest.makeSuite(TestForeachCase))
    suite.addTest(unittest.makeSuite(TestCallCase))
    suite.addTest(unittest.makeSuite(TestSetItemCase))
    suite.addTest(unittest.makeSuite(TestDelItemCase))
    suite.addTest(unittest.makeSuite(TestAppendCase))
    suite.addTest(unittest.makeSuite(TestInsertCase))
    suite.addTest(unittest.makeSuite(TestRemoveCase))
    suite.addTest(unittest.makeSuite(TestRemoveAllCase))
    suite.addTest(unittest.makeSuite(TestEachCase))
    suite.addTest(unittest.makeSuite(TestVisitCase))
    suite.addTest(unittest.makeSuite(TestPrintCase))
    return suite
#-def
