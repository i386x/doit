#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_cmd/test_commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-05-10 13:16:59 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor's commands module tests.\
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

from doit.config.version import DOIT_VERSION as DV

from doit.support.cmd.errors import \
    CommandProcessorError, \
    CommandError

from doit.support.cmd.runtime import \
    Location, \
    Pair, \
    List, \
    HashMap, \
    UserType, \
    ExceptionClass, \
    Procedure

from doit.support.cmd.commands import \
    CommandContext, \
    Initializer, Finalizer, \
    Command, \
    Const, \
    Version, \
    MacroNode as _n, MacroNodeSequence as _s, MacroNodeAtom as _a, \
        MacroNodeParam as _p, \
    Expand, \
    SetLocal, \
    GetLocal, \
    DefMacro, DefError, Define, DefModule, \
    Operation, \
    Add, Sub, Mul, Div, Mod, Neg, \
    BitAnd, BitOr, BitXor, ShiftL, ShiftR, Inv, \
    Lt, Gt, Le, Ge, Eq, Ne, Is, \
    And, Or, Not, \
    NewPair, NewList, NewHashMap, \
    Copy, Slice, Concat, Join, Merge, \
    Type, InstanceOf, Strlen, Size, Empty, Contains, Count, \
    IsDigit, IsUpper, IsLower, IsAlpha, IsLetter, IsAlnum, IsWord, \
    Keys, Values, \
    First, Second, GetItem, \
    Substr, Find, RFind, \
    LStrip, RStrip, Strip, ToUpper, ToLower, Subst, Trans, \
    Head, Tail, \
    Sort, Reverse, Unique, \
    Split, \
    ToBool, ToInt, ToFlt, ToStr, ToPair, ToList, ToHash, \
    All, Any, SeqOp, Map, Filter, \
    Lambda, \
    Block, If, Foreach, While, DoWhile, Break, Continue, \
    Call, ECall, Return, \
    TryCatchFinally, Throw, Rethrow, \
    SetItem, DelItem, Append, Insert, Remove, RemoveAll, \
    Each, Visit, \
    Print, \
    Module, SetMember, GetMember

from doit.support.cmd.eval import \
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

    def do_visit(self, processor, f, *args):
        processor.insertcode(
            Call(f,
                0,
                ECall(self.left.do_visit, processor, f, *args),
                ECall(self.right.do_visit, processor, f, *args),
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

    def do_visit(self, processor, f, *args):
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
        c.enter(p, Initializer(ctx))
        c.expand(p)
        c.leave(p, Finalizer(ctx))
        p.setacc(56)
        c.pushacc(p)
        self.assertEqual(p.popval(), 56)
        self.assertIsNone(
            c.find_exception_handler(
                ctx, CommandError(p.TypeError, "", p.traceback())
            )
        )
    #-def

    def test_equality(self):
        c1 = Command()
        c2 = Command()
        c3 = Command()
        c3.set_location("a", 1, 2)
        c3.properties[1] = 2
        c3.name = "MyCmd"
        c3.qname = "::MyCmd"
        c4 = Command()
        c4.set_location("b", 1, 2)
        c4.properties[1] = 2
        c4.name = "MyCmd"
        c4.qname = "::MyCmd"
        c5 = Command()
        c5.set_location("a", 1, 2)
        c5.properties[1] = 2
        c5.name = "MyCmd"
        c5.qname = "::MyCmd"

        self.assertEqual(c1, c1)
        self.assertEqual(c1, c2)
        self.assertNotEqual(c3, c4)
        self.assertEqual(c3, c5)
    #-def
#-class

class TestConstCase(unittest.TestCase):

    def test_equality(self):
        self.assertEqual(Const(1), Const(1))
        self.assertNotEqual(Const(1), Const(2))
    #-def
#-class

class TestVersionCase(unittest.TestCase):

    def test_version(self):
        dv = (DV.major * 10000 + DV.minor * 100 + DV.patchlevel, DV.date)
        p = CommandProcessor()

        p.run([Version()])
        self.assertEqual(p.acc(), dv)
    #-def
#-class

class TestExpandCase(unittest.TestCase):

    def test_equality(self):
        # MacroNode
        n1 = _n(Return, _a(1))
        n1.deferred.append(1)
        n1.deferred.append(2)
        n2 = _n(Return, _a(1))
        n2.deferred.append(1)
        n2.deferred.append(3)
        n3 = _n(Return, _a(1))
        n3.deferred.append(1)
        n3.deferred.append(3)

        self.assertNotEqual(_n(Return), Return)
        self.assertNotEqual(_n(Return), _n(Throw))
        self.assertNotEqual(_n(Return), _n(Return, _a(1)))
        self.assertNotEqual(_n(Return, _a(1)), _n(Return, _a(2)))
        self.assertNotEqual(n1, n2)
        self.assertEqual(_n(Return), _n(Return))
        self.assertEqual(n2, n3)

        # MacroNodeSequence
        nn1 = _n(Block, _s(_n(Return), _n(Throw, _a(1))))
        nn2 = _n(Block, _s(_n(Return), _n(Throw, _a(1))))
        nn3 = _s(_n(Return, _a(1)), _n(Return, _a(2)), _s(_n(Throw)))
        nn3.deferred.append(1)
        nn4 = _s(_n(Return, _a(1)), _n(Return, _a(2)), _s(_n(Throw)))
        nn4.deferred.append(1)
        nn5 = _s(_n(Return, _a(1)), _n(Return, _a(2)), _s(_n(Throw)))
        nn5.deferred.append(2)
        nn6 = _s(_n(Return, _a(1)), _n(Return, _a(2)))
        nn7 = _s(_n(Return, _a(1)), _n(Return, _a(3)), _s(_n(Throw)))
        nn7.deferred.append(1)
        nn8 = _s(_n(Return, _a(1)), _n(Return, _a(2)), _s(_n(Throw)))

        self.assertNotEqual(nn1, 0)
        self.assertEqual(nn1, nn2)
        self.assertEqual(nn3, nn4)
        self.assertNotEqual(nn4, nn5)
        self.assertNotEqual(nn4, nn6)
        self.assertNotEqual(nn4, nn7)
        self.assertNotEqual(nn4, nn8)

        # MacroNodeAtom
        self.assertNotEqual(_a(1), _s(_a(1)))
        self.assertNotEqual(_a((1, 2)), _a([1, 2, 3]))
        self.assertEqual(_a((1, 2)), _a([1, 2]))

        # MacroNodeParam
        self.assertNotEqual(_p('t'), _a('t'))
        self.assertNotEqual(_p('t'), _p('p'))
        self.assertEqual(_p('t'), _p('t'))

        # Expand
        self.assertNotEqual(Expand(1, 2, 3), 1)
        self.assertNotEqual(Expand(1, 2, 3), Expand(1, 2))
        self.assertEqual(Expand(1, 2, 3), Expand(1, 2, 3))

        # DefMacro
        self.assertNotEqual(
            DefMacro('x', ['a', 'b'], _s(_p('a'), _p('b'))), 1
        )
        self.assertNotEqual(
            DefMacro('x', ['a', 'b'], _s(_p('a'), _p('b'))),
            DefMacro('x', ['a', 'b'], _s(_p('a'), _p('c')))
        )
        self.assertEqual(
            DefMacro('x', ['a', 'b'], _s(_p('a'), _p('b'))),
            DefMacro('x', ['a', 'b'], _s(_p('a'), _p('b')))
        )
    #-def

    def test_macros(self):
        p = Printer()

        mo = _n(Throw, _n(GetLocal, _a("Exception")), _a("error"))
        mo.deferred.append(lambda n: n.set_location("f1.g", 3, 7))
        p.run([
            DefMacro('T', [], [mo]),
            DefMacro('M', [], [_n(GetLocal, _a('z'))]),
            DefMacro('m', ['x', 'y'], [
                _n(Foreach, _p('x'), _a([1, 2, 3]), _s(
                    _n(Print, _p('y')),
                    _n(Print, _n(GetLocal, _p('x')))
                ))
            ]),
            DefMacro('bad', ['x'], [_p('y')])
        ])
        self.assertEqual(p.output, "")

        with self.assertRaises(CommandProcessorError) as e:
            p.run([Expand(GetLocal('T'))])
        self.assertEqual(
            str(e.exception.traceback),
            "In <main>:\n" \
            "> At [\"f1.g\":3:7]:"
        )

        p.run([
            Expand(GetLocal('m'), "z", Expand(GetLocal('M')))
        ])
        self.assertEqual(p.output, "112233")
        self.assertEqual(p.getenv()['z'], 3)

        with self.assertRaises(CommandProcessorError):
            p.run([Expand(GetLocal('bad'), 0)])
        with self.assertRaises(CommandProcessorError):
            p.run([Expand(0)])
        with self.assertRaises(CommandProcessorError):
            p.run([Expand(GetLocal('m'))])
        with self.assertRaises(CommandProcessorError):
            p.run([Expand(GetLocal('M'), 1)])
    #-def
#-class

class TestSetLocalCase(unittest.TestCase):

    def test_equality(self):
        x = SetLocal('a', 'b', 3)
        x.set_location("f", 1, 2)

        self.assertNotEqual(SetLocal('a', 'b', 3), 1)
        self.assertNotEqual(SetLocal('a', 'b', 3), SetLocal('a', 'b', 2))
        self.assertNotEqual(SetLocal('a', 'b', 3), SetLocal('a', 'x', 3))
        self.assertNotEqual(SetLocal('a', 'b', 3), SetLocal('b', 'b', 3))
        self.assertEqual(SetLocal('a', 'b', 3), SetLocal('a', 'b', 3))
        self.assertNotEqual(SetLocal('a', 'b', 3), x)
    #-def

    def test_SetLocal(self):
        p = CommandProcessor()

        with self.assertRaises(CommandError):
            p.getenv().getvar('z')
        p.run([SetLocal('z', "hello")])
        self.assertEqual(p.getenv().getvar('z'), "hello")
    #-def
#-class

class TestGetLocalCase(unittest.TestCase):

    def test_equality(self):
        self.assertNotEqual(GetLocal('a'), 1)
        self.assertNotEqual(GetLocal('a'), GetLocal('b'))
        self.assertEqual(GetLocal('a'), GetLocal('a'))
    #-def

    def test_GetLocal(self):
        p = CommandProcessor()

        p.run([SetLocal('v', 751), GetLocal('v')])
        self.assertEqual(p.acc(), 751)
    #-def
#-class

class TestOperationsCase(unittest.TestCase):

    def test_equality(self):
        self.assertNotEqual(Add(1, 2), Sub(1, 2))
        self.assertNotEqual(Add(1, 2), Add(1, 3))
        self.assertEqual(Add(1, 2), Add(1, 2))
    #-def

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
        self.assertIs(p.acc(), p.Null)
        p.run([And(True, None)])
        self.assertIs(p.acc(), p.Null)
        p.run([And(None, None)])
        self.assertIs(p.acc(), p.Null)

        # Short evaluation:
        p.run([And("", Add("a", "b"))])
        self.assertIsInstance(p.acc(), str)
        self.assertEqual(p.acc(), "")
        p.run([And(1, 0)])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), 0)
        p.run([And(1, 2)])
        self.assertIsInstance(p.acc(), int)
        self.assertEqual(p.acc(), 2)
        with self.assertRaises(CommandProcessorError):
            p.run([And(1, Add("a", "b"))])
    #-def

    def test_Or(self):
        p = CommandProcessor()

        p.run([Or(None, True)])
        self.assertTrue(p.acc())

        # Short evaluation:
        p.run([Or("a", "b")])
        self.assertEqual(p.acc(), "a")
        p.run([Or("a", Neg(""))])
        self.assertEqual(p.acc(), "a")
        with self.assertRaises(CommandProcessorError):
            p.run([Or(0, Neg(""))])
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
        self.assertIsInstance(p.acc(), Pair)
        self.assertEqual(p.acc(), (1, "***"))
    #-def

    def test_NewList(self):
        p = CommandProcessor()

        p.run([
            SetLocal('x', 1),
            SetLocal('y', "o"),
            SetLocal('z', 1.25),
            NewList(GetLocal('x'), GetLocal('y'), GetLocal('z'))
        ])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [1, "o", 1.25])
        p.run([NewList()])
        self.assertIsInstance(p.acc(), List)
        self.assertEqual(p.acc(), [])
    #-def

    def test_NewHashMap(self):
        p = CommandProcessor()

        p.run([
            SetLocal('x', NewPair('x', 1)),
            NewHashMap((1, 2), GetLocal('x'), NewPair(0.25, 'z'))
        ])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {1: 2, 'x': 1, 0.25: 'z'})
        p.run([NewHashMap()])
        self.assertIsInstance(p.acc(), HashMap)
        self.assertEqual(p.acc(), {})
        with self.assertRaises(CommandProcessorError):
            p.run([NewHashMap((1, 'a'), NewList(1, 2))])
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

    def test_Type(self):
        p = CommandProcessor()

        p.run([Type(p.Null)])
        self.assertIs(p.acc(), p.NullType)
        p.run([Type(None)])
        self.assertIs(p.acc(), p.NullType)
        p.run([Type(True)])
        self.assertIs(p.acc(), p.Boolean)
        p.run([Type(False)])
        self.assertIs(p.acc(), p.Boolean)
        p.run([Type(-1)])
        self.assertIs(p.acc(), p.Integer)
        p.run([Type(0.5)])
        self.assertIs(p.acc(), p.Float)
        p.run([Type("sd")])
        self.assertIs(p.acc(), p.String)
        p.run([Type((1, 2))])
        self.assertIs(p.acc(), p.Pair)
        p.run([Type(Pair(1, 2))])
        self.assertIs(p.acc(), p.Pair)
        p.run([Type([])])
        self.assertIs(p.acc(), p.List)
        p.run([Type(List())])
        self.assertIs(p.acc(), p.List)
        p.run([Type({})])
        self.assertIs(p.acc(), p.HashMap)
        p.run([Type(HashMap())])
        self.assertIs(p.acc(), p.HashMap)
        p.run([Type(UT_000())])
        self.assertIs(p.acc(), p.UserType)
        p.run([Type(GetLocal('Exception'))])
        self.assertIs(p.acc(), p.ErrorClass)
        p.run([
            TryCatchFinally([
                Add("1", "2")
            ], [('TypeError', 'e', [
                SetLocal('e', Type(GetLocal('e')))
            ])], [])
        ])
        self.assertIs(p.getenv()['e'], p.Error)
        p.run([
            DefMacro("M", [], []),
            Type(GetLocal("M"))
        ])
        self.assertIs(p.acc(), p.Macro)
        p.run([
            Define("f", [], [], False, []),
            Type(GetLocal("f"))
        ])
        self.assertIs(p.acc(), p.Proc)
        p.run([
            DefModule("A", []),
            Type(GetLocal("A"))
        ])
        self.assertIs(p.acc(), p.Module)
    #-def

    def test_InstanceOf(self):
        p = CommandProcessor()

        p.run([InstanceOf(1, Const(p.Integer))])
        self.assertTrue(p.acc())
        p.run([InstanceOf(1, Const(p.List))])
        self.assertFalse(p.acc())
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

    def test_Head(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([Head("")])
        with self.assertRaises(CommandProcessorError):
            p.run([Head([])])
        p.run([Head("a")])
        self.assertEqual(p.acc(), 'a')
        p.run([Head("ba")])
        self.assertEqual(p.acc(), 'b')
        p.run([Head("cba")])
        self.assertEqual(p.acc(), 'c')
        p.run([Head(('x', 2))])
        self.assertEqual(p.acc(), 'x')
        p.run([Head([1])])
        self.assertEqual(p.acc(), 1)
        p.run([Head([2, 1])])
        self.assertEqual(p.acc(), 2)
        p.run([Head([3, 2, 1])])
        self.assertEqual(p.acc(), 3)
    #-def

    def test_Tail(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([Tail("")])
        with self.assertRaises(CommandProcessorError):
            p.run([Tail([])])
        p.run([Tail("a")])
        self.assertEqual(p.acc(), "")
        p.run([Tail("ba")])
        self.assertEqual(p.acc(), "a")
        p.run([Tail("cba")])
        self.assertEqual(p.acc(), "ba")
        p.run([Tail(('x', 2))])
        self.assertEqual(p.acc(), [2])
        p.run([Tail([1])])
        self.assertEqual(p.acc(), [])
        p.run([Tail([2, 1])])
        self.assertEqual(p.acc(), [1])
        p.run([Tail([3, 2, 1])])
        self.assertEqual(p.acc(), [2, 1])
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
        p.run([ToBool(Procedure(1, 2, 3, 4, 5, 6, 7))])
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
        p.run([ToStr(Procedure("f1", "::f1", 0, 0, 0, 0, 0))])
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
            p.run([ToHash([(1, 2), Procedure(1, 2, 3, 4, 5, 6, 7)])])
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

    def test_equality(self):
        self.assertNotEqual(
            Block(
                SetLocal("x", "def"),
                SetLocal("y", 1)
            ),
            SetLocal("y", 1)
        )
        self.assertNotEqual(
            Block(
                SetLocal("x", "def"),
                SetLocal("y", 1)
            ),
            Block(
                SetLocal("x", "def"),
                SetLocal("y", 2)
            )
        )
        self.assertEqual(
            Block(
                SetLocal("x", "def"),
                SetLocal("y", 1)
            ),
            Block(
                SetLocal("x", "def"),
                SetLocal("y", 1)
            )
        )
    #-def

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

    def test_equality(self):
        self.assertNotEqual(
            If(True, [1], [2]), 1
        )
        self.assertNotEqual(
            If(True, [1], [2]), If(False, [1], [2])
        )
        self.assertNotEqual(
            If(True, [1], [2]), If(True, [0], [2])
        )
        self.assertNotEqual(
            If(True, [1], [2]), If(True, [1], [1])
        )
        self.assertEqual(
            If(True, [1], [2]), If(True, [1], [2])
        )
    #-def

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

class TestLoopCase(unittest.TestCase):

    def test_equality(self):
        # Foreach
        self.assertNotEqual(
            Foreach("i", [], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ]),
            1
        )
        self.assertNotEqual(
            Foreach("i", [], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ]),
            Foreach("j", [], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ])
        )
        self.assertNotEqual(
            Foreach("i", [1, 2], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ]),
            Foreach("i", [1, 3], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ])
        )
        self.assertNotEqual(
            Foreach("i", [1, 2], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ]),
            Foreach("i", [1, 2], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("j")))
            ])
        )
        self.assertEqual(
            Foreach("i", [1, 2], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ]),
            Foreach("i", [1, 2], [
                SetLocal("x", Add(GetLocal("x"), GetLocal("i")))
            ])
        )

        # While
        self.assertNotEqual(
            While(Gt(GetLocal('x'), 0), [
                SetLocal('x', Sub(GetLocal('x'), 1))
            ]),
            0
        )
        self.assertNotEqual(
            While(Gt(GetLocal('x'), 0), [
                SetLocal('x', Sub(GetLocal('x'), 1))
            ]),
            While(Gt(GetLocal('x'), 1), [
                SetLocal('x', Sub(GetLocal('x'), 1))
            ])
        )
        self.assertNotEqual(
            While(Gt(GetLocal('x'), 0), [
                SetLocal('x', Sub(GetLocal('x'), 1))
            ]),
            While(Gt(GetLocal('x'), 0), [
                SetLocal('x', Sub(GetLocal('y'), 1))
            ])
        )
        self.assertEqual(
            While(Gt(GetLocal('x'), 0), [
                SetLocal('x', Sub(GetLocal('x'), 1))
            ]),
            While(Gt(GetLocal('x'), 0), [
                SetLocal('x', Sub(GetLocal('x'), 1))
            ])
        )

        # DoWhile
        self.assertNotEqual(
            DoWhile([
                SetLocal('x', 2)
            ], False),
            1
        )
        self.assertNotEqual(
            DoWhile([
                SetLocal('x', 2)
            ], False),
            DoWhile([
                SetLocal('x', 0)
            ], False)
        )
        self.assertNotEqual(
            DoWhile([
                SetLocal('x', 2)
            ], False),
            DoWhile([
                SetLocal('x', 2)
            ], True)
        )
        self.assertEqual(
            DoWhile([
                SetLocal('x', 2)
            ], False),
            DoWhile([
                SetLocal('x', 2)
            ], False)
        )
    #-def

    def test_Foreach(self):
        p = CommandProcessor()

        # foreach:
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

        # break, continue:
        p.run([
            SetLocal('x', []),
            SetLocal('y', ""),
            Foreach('c', "abc   def    ghi\n jkl   mno", [
                If(IsAlpha(GetLocal('c')), [
                    SetLocal('y', Concat(GetLocal('y'), GetLocal('c'))),
                    Continue()
                ], []),
                If(Eq(GetLocal('c'), ' '), [
                    If(ToBool(GetLocal('y')), [
                        Append(GetLocal('x'), GetLocal('y')),
                        SetLocal('y', "")
                    ], []),
                    Continue()
                ], []),
                If(ToBool(GetLocal('y')), [
                    Append(GetLocal('x'), GetLocal('y')),
                    SetLocal('y', "")
                ], []),
                Break()
            ])
        ])
        self.assertEqual(p.getenv()['x'], ["abc", "def", "ghi"])
    #-def

    def test_While(self):
        p = CommandProcessor()

        p.run([
            SetLocal('x', 10),
            While(Gt(GetLocal('x'), 0), [
                SetLocal('x', Sub(GetLocal('x'), 1))
            ])
        ])
        self.assertEqual(p.getenv()['x'], 0)

        p.run([
            SetLocal('x', 1),
            While(False, [
                SetLocal('x', 2)
            ])
        ])
        self.assertEqual(p.getenv()['x'], 1)

        p.run([
            SetLocal('x', 10),
            While(True, [
                If(Gt(GetLocal('x'), 0), [
                    SetLocal('x', Sub(GetLocal('x'), 1)),
                    Continue()
                ], []),
                Break(),
                Continue()
            ])
        ])
        self.assertEqual(p.getenv()['x'], 0)
    #-def

    def test_DoWhile(self):
        p = CommandProcessor()

        p.run([
            SetLocal('x', 1),
            DoWhile([
                SetLocal('x', 2)
            ], False)
        ])
        self.assertEqual(p.getenv()['x'], 2)

        p.run([
            SetLocal('x', 0),
            SetLocal('y', 10),
            DoWhile([
                SetLocal('x', Add(GetLocal('x'), 1)),
                SetLocal('y', Sub(GetLocal('y'), 1))
            ], Gt(GetLocal('y'), 0))
        ])
        self.assertEqual(p.getenv()['x'], 10)

        p.run([
            SetLocal('x', 10),
            DoWhile([
                If(Gt(GetLocal('x'), 0), [
                    SetLocal('x', Sub(GetLocal('x'), 1)),
                    Continue()
                ], []),
                Break(),
                Continue()
            ], True)
        ])
        self.assertEqual(p.getenv()['x'], 0)

        p.run([
            SetLocal('x', 10),
            DoWhile([
                If(Gt(GetLocal('x'), 0), [
                    SetLocal('x', Sub(GetLocal('x'), 1)),
                    Continue()
                ], []),
                Break(),
                Continue()
            ], False)
        ])
        self.assertEqual(p.getenv()['x'], 9)
    #-def

    def test_nested_loops(self):
        p = CommandProcessor()

        # l = []
        # foreach x [1, 2, -1, 3, 0, 8]
        #   if (x < 0)
        #     continue
        #   y = x
        #   if y == 0
        #     break
        #   do
        #     z = 0
        #     while true
        #       if z < y
        #         z += 1
        #         continue
        #       l += z
        #       break
        #     end
        #     y -= 1
        #     if y < 0
        #       break
        #   while true
        # end
        p.run([
            SetLocal('l', []),
            Foreach('x', [1, 2, -1, 3, 0, 8], [
                If(Lt(GetLocal('x'), 0), [
                    Continue()
                ], []),
                SetLocal('y', GetLocal('x')),
                If(Eq(GetLocal('y'), 0), [
                    Break()
                ], []),
                DoWhile([
                    SetLocal('z', 0),
                    While(True, [
                        If(Lt(GetLocal('z'), GetLocal('y')), [
                            SetLocal('z', Add(GetLocal('z'), 1)),
                            Continue()
                        ], []),
                        Append(GetLocal('l'), GetLocal('z')),
                        Break()
                    ]),
                    SetLocal('y', Sub(GetLocal('y'), 1)),
                    If(Lt(GetLocal('y'), 0), [
                        Break()
                    ], [])
                ], True)
            ])
        ])
        self.assertEqual(p.getenv()['l'], [1, 0, 2, 1, 0, 3, 2, 1, 0])
    #-def

    def test_bad_cases(self):
        p = CommandProcessor()

        p.run([
            Define("f", [], [], False, [
                Break(), Return(0)
            ]),
            Define("g", [], [], False, [
                Continue(), Return(1)
            ])
        ])
        with self.assertRaises(CommandProcessorError):
            p.run([
                DoWhile([
                    Call(GetLocal("f"))
                ], False)
            ])
        with self.assertRaises(CommandProcessorError):
            p.run([
                DoWhile([
                    Call(GetLocal("g"))
                ], False)
            ])
        with self.assertRaises(CommandProcessorError):
            p.run([Break(), Add(1, 2), Continue()])
        with self.assertRaises(CommandProcessorError):
            p.run([Continue(), Add(1, 2), Break()])
    #-def
#-class

class TestCallCase(unittest.TestCase):

    def test_equality(self):
        # Define
        x = Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")])
        x.set_location("f", 1, 2)

        self.assertNotEqual(
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")]),
            GetLocal("a")
        )
        self.assertNotEqual(
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")]),
            x
        )
        self.assertNotEqual(
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")]),
            Define("diff", ["a"], ["x", "y"], True, [GetLocal("a")])
        )
        self.assertNotEqual(
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")]),
            Define("sum", ["b"], ["x", "y"], True, [GetLocal("a")])
        )
        self.assertNotEqual(
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")]),
            Define("sum", ["a"], ["x", "z"], True, [GetLocal("a")])
        )
        self.assertNotEqual(
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")]),
            Define("sum", ["a"], ["x", "y"], False, [GetLocal("a")])
        )
        self.assertNotEqual(
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")]),
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("b")])
        )
        self.assertEqual(
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")]),
            Define("sum", ["a"], ["x", "y"], True, [GetLocal("a")])
        )

        # Call
        self.assertNotEqual(
            Call(GetLocal("my_proc")), 1
        )
        self.assertNotEqual(
            Call(GetLocal("my_proc"), 1, 2),
            Call(GetLocal("my_proc_"), 1, 2)
        )
        self.assertNotEqual(
            Call(GetLocal("my_proc"), 1, 2),
            Call(GetLocal("my_proc"), 1, 2, 3)
        )
        self.assertEqual(
            Call(GetLocal("my_proc"), 1, 2),
            Call(GetLocal("my_proc"), 1, 2)
        )

        # ECall
        self.assertNotEqual(
            ECall(GetLocal("my_proc")), 1
        )
        self.assertNotEqual(
            ECall(GetLocal("my_proc"), 1, 2),
            ECall(GetLocal("my_proc_"), 1, 2)
        )
        self.assertNotEqual(
            ECall(GetLocal("my_proc"), 1, 2),
            ECall(GetLocal("my_proc"), 1, 2, 3)
        )
        self.assertEqual(
            ECall(GetLocal("my_proc"), 1, 2),
            ECall(GetLocal("my_proc"), 1, 2)
        )

        # Return
        self.assertNotEqual(
            Return(GetLocal("x")), 1
        )
        self.assertNotEqual(
            Return(GetLocal("x")), Return()
        )
        self.assertNotEqual(
            Return(GetLocal("x")), Return(GetLocal("y"))
        )
        self.assertEqual(
            Return(GetLocal("x")), Return(GetLocal("x"))
        )
        self.assertEqual(
            Return(), Return()
        )
    #-def

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

class TestTryCatchFinallyCase(unittest.TestCase):

    def test_equality(self):
        # DefError
        self.assertNotEqual(DefError('E', GetLocal('E')), GetLocal('E'))
        self.assertNotEqual(
            DefError('E', GetLocal('E')), DefError('E', GetLocal('F'))
        )
        self.assertEqual(
            DefError('E', GetLocal('E')), DefError('E', GetLocal('E'))
        )

        # TryCatchFinally
        self.assertNotEqual(
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ]),
            1
        )
        self.assertNotEqual(
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ]),
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ])
        )
        self.assertNotEqual(
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ]),
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('y', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ])
        )
        self.assertNotEqual(
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ]),
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('x', 3)
            ])
        )
        self.assertEqual(
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ]),
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ])
        )

        # Throw
        self.assertNotEqual(
            Throw(GetLocal('TypeError'), "catch me!"), 1
        )
        self.assertNotEqual(
            Throw(GetLocal('TypeError'), "catch me!"),
            Throw(GetLocal('TypeError'), "catch me?")
        )
        self.assertNotEqual(
            Throw(GetLocal('TypeError'), "catch me!"),
            Throw(GetLocal('Error'), "catch me!")
        )
        self.assertEqual(
            Throw(GetLocal('TypeError'), "catch me!"),
            Throw(GetLocal('TypeError'), "catch me!")
        )

        # Rethrow
        self.assertNotEqual(
            Rethrow(GetLocal("e")), 1
        )
        self.assertNotEqual(
            Rethrow(GetLocal("e")), Rethrow(GetLocal("f"))
        )
        self.assertEqual(
            Rethrow(GetLocal("e")), Rethrow(GetLocal("e"))
        )
    #-def

    def test_TryCatchFinally(self):
        p = CommandProcessor()

        # try
        #   <code>
        # catch TypeError, e
        #   <code>
        # finally
        #   <code>
        # end
        p.run([
            SetLocal('x', 1),
            SetLocal('y', 2),
            TryCatchFinally([
                Add(1, 2),
                Sub(4, 3),
                Div(0, "z"),
                Mod(4, 3),
                Break(),
                Return(),
                Continue()
            ], [
                ('TypeError', 'e', [
                    SetLocal('x', GetLocal('e'))
                ])
            ], [
                SetLocal('y', 3)
            ])
        ])
        self.assertIs(p.getenv()['x'], p.getenv()['e'])
        self.assertEqual(p.getenv()['y'], 3)

        # function f(x, y, l)
        #   try
        #     if (x < 0)
        #       throw ValueError("x must be non-negative")
        #     if (y < 0)
        #       throw KeyError("")
        #     throw TypeError("catch me!")
        #     l += "never get here!"
        #   catch TypeError, e
        #     l += 1
        #   catch ValueError, e
        #     l += 2
        #     rethrow e
        #   catch Exception, e
        #     l += 3
        #     try
        #       try
        #         if (y == -1)
        #           l += 4
        #           throw ValueError("y is -1")
        #         if (y == -2)
        #           l += 5
        #           throw TypeError("")
        #         l += 6
        #         return 0
        #       catch ValueError, e
        #         l += 7
        #         return 1
        #       finally
        #         l += 8
        #         return 2
        #       end
        #     catch TypeError, e
        #       l += 9
        #       return 3
        #     finally
        #       l += 10
        #       throw SyntaxError("catch me to!")
        #     end
        #   catch KeyError, e
        #     l += "never get here! (2)"
        #   finally
        #     l += 11
        #     return 5
        #   end
        #   l += 12
        #   return 6
        # end
        p.run([
            Define("f", ["e"], ["x", "y", "l"], False, [
                TryCatchFinally([
                    If(Lt(GetLocal('x'), 0), [
                        Throw(GetLocal('ValueError'), "x must be non-negative")
                    ], []),
                    If(Lt(GetLocal('y'), 0), [
                        Throw(GetLocal('KeyError'), "")
                    ], []),
                    Throw(GetLocal('TypeError'), "catch me!"),
                    Append(GetLocal('l'), "never get here!")
                ], [('TypeError', 'e', [
                    Append(GetLocal('l'), 1)
                ]), ('ValueError', 'e', [
                    Append(GetLocal('l'), 2),
                    Rethrow(GetLocal('e'))
                ]), ('Exception', 'e', [
                    Append(GetLocal('l'), 3),
                    TryCatchFinally([
                        TryCatchFinally([
                            If(Eq(GetLocal('y'), -1), [
                                Append(GetLocal('l'), 4),
                                Throw(GetLocal('ValueError'), "y is -1")
                            ], []),
                            If(Eq(GetLocal('y'), -2), [
                                Append(GetLocal('l'), 5),
                                Throw(GetLocal('TypeError'), "")
                            ], []),
                            Append(GetLocal('l'), 6),
                            Return(0)
                        ], [('ValueError', 'e', [
                            Append(GetLocal('l'), 7),
                            Return(1)
                        ])], [
                            Append(GetLocal('l'), 8),
                            Return(2)
                        ])
                    ], [('TypeError', 'e', [
                        Append(GetLocal('l'), 9),
                        Return(3)
                    ])], [
                        Append(GetLocal('l'), 10),
                        Throw(GetLocal('SyntaxError'), "catch me too!")
                    ])
                ]), ('KeyError', 'e', [
                    Append(GetLocal('l'), "never get here! (2)")
                ])], [
                    Append(GetLocal('l'), 11),
                    Return(5)
                ]),
                Append(GetLocal('l'), 12),
                Return(6)
            ])
        ])

        # f(1, 1, l)
        # > l == [1, 11], r == 5
        p.run([
            SetLocal('l', []),
            SetLocal('r', Call(GetLocal("f"), 1, 1, GetLocal("l")))
        ])
        self.assertEqual(p.getenv()['l'], [1, 11])
        self.assertEqual(p.getenv()['r'], 5)
        # f(1, -1, l)
        # > l == [3, 4, 7, 8, 10, 11], r == 5
        p.run([
            SetLocal('l', []),
            SetLocal('r', Call(GetLocal("f"), 1, -1, GetLocal("l")))
        ])
        self.assertEqual(p.getenv()['l'], [3, 4, 7, 8, 10, 11])
        self.assertEqual(p.getenv()['r'], 5)
        # f(1, -2, l)
        # > l == [3, 5, 8, 10, 11], r == 5
        p.run([
            SetLocal('l', []),
            SetLocal('r', Call(GetLocal("f"), 1, -2, GetLocal("l")))
        ])
        self.assertEqual(p.getenv()['l'], [3, 5, 8, 10, 11])
        self.assertEqual(p.getenv()['r'], 5)
        # f(1, -3, l)
        # > l == [3, 6, 8, 10, 11], r == 5
        p.run([
            SetLocal('l', []),
            SetLocal('r', Call(GetLocal("f"), 1, -3, GetLocal("l")))
        ])
        self.assertEqual(p.getenv()['l'], [3, 6, 8, 10, 11])
        self.assertEqual(p.getenv()['r'], 5)
        # f(-1, -3, l)
        # > l == [2, 11], r == 5
        p.run([
            SetLocal('l', []),
            SetLocal('r', Call(GetLocal("f"), -1, -3, GetLocal("l")))
        ])
        self.assertEqual(p.getenv()['l'], [2, 11])
        self.assertEqual(p.getenv()['r'], 5)

        # function g(x)
        #   try
        #     if (x < 0)
        #       throw ValueError("")
        #     return 1
        #   catch ValueError, e
        #     if (x < -1)
        #         rethrow e
        #     return 2
        #   end
        # end
        p.run([
            Define("g", ["e"], ["x"], False, [
                TryCatchFinally([
                    If(Lt(GetLocal("x"), 0), [
                        Throw(GetLocal("ValueError"), "")
                    ], []),
                    Return(1)
                ], [('ValueError', 'e', [
                    If(Lt(GetLocal("x"), -1), [
                        Rethrow(GetLocal("e"))
                    ], []),
                    Return(2)
                ])], [])
            ])
        ])
        # g(0)
        # > 1
        p.run([Call(GetLocal("g"), 0)])
        self.assertEqual(p.acc(), 1)
        # g(-1)
        # > 2
        p.run([Call(GetLocal("g"), -1)])
        self.assertEqual(p.acc(), 2)
        # g(-2)
        # > ValueError
        with self.assertRaises(CommandProcessorError):
            p.run([Call(GetLocal("g"), -2)])

        # try
        #   throw ValueError("")
        # catch KeyError
        # end
        code = [
            TryCatchFinally([
                Throw(GetLocal("ValueError"), "")
            ], [
                ('KeyError', "", [])
            ], [])
        ]
        with self.assertRaises(CommandProcessorError):
            p.run(code)

        # try
        #   throw KeyError("")
        # catch KeyError
        #   throw ValueError("")
        # end
        code = [
            TryCatchFinally([
                Throw(GetLocal("KeyError"), "")
            ], [('KeyError', "", [
                Throw(GetLocal("ValueError"), "")
            ])], [])
        ]
        with self.assertRaises(CommandProcessorError):
            p.run(code)

        # function h()
        #   try
        #     throw KeyError("")
        #   catch KeyError
        #     return 1
        #   end
        #   return 2
        # end
        code = [
            Define("h", [], [], False, [
                TryCatchFinally([
                    Throw(GetLocal("KeyError"), "")
                ], [("KeyError", "", [
                    Return(1)
                ])], []),
                Return(2)
            ]),
            Call(GetLocal("h"))
        ]
        p.run(code)
        self.assertEqual(p.acc(), 1)

        # l = []
        # while true
        #   try
        #     throw KeyError("")
        #   catch KeyError
        #     l += 1
        #     break
        #   end
        #   l += 2
        #   continue
        # end
        code = [
            SetLocal('l', []),
            While(True, [
                TryCatchFinally([
                    Throw(GetLocal("KeyError"), "")
                ], [("KeyError", "", [
                    Append(GetLocal('l'), 1),
                    Break()
                ])], []),
                Append(GetLocal('l'), 2),
                Continue()
            ])
        ]
        p.run(code)
        self.assertEqual(p.getenv()['l'], [1])

        # l = []
        # foreach x [1, 2, 3]
        #   try
        #     throw KeyError("")
        #   catch KeyError
        #     l += 1
        #     continue
        #   end
        #   l += 2
        # end
        code = [
            SetLocal('l', []),
            Foreach('x', [1, 2, 3], [
                TryCatchFinally([
                    Throw(GetLocal("KeyError"), "")
                ], [("KeyError", "", [
                    Append(GetLocal('l'), 1),
                    Continue()
                ])], []),
                Append(GetLocal('l'), 2)
            ])
        ]
        p.run(code)
        self.assertEqual(p.getenv()['l'], [1, 1, 1])

        # l = []
        # try
        #   throw KeyError("")
        # catch KeyError
        #   l += 1
        # end
        code = [
            SetLocal('l', []),
            TryCatchFinally([
                Throw(GetLocal("KeyError"), "")
            ], [("KeyError", "", [
                Append(GetLocal('l'), 1)
            ])], [])
        ]
        p.run(code)
        self.assertEqual(p.getenv()['l'], [1])

        # function fg()
        #   try
        #     return 1
        #   catch BaseError
        #   end
        #   return 0
        # end
        code = [
            Define("fg", [], [], False, [
                TryCatchFinally([
                    Return(1)
                ], [
                    ('BaseError', "", [])
                ], []),
                Return(0)
            ]),
            Call(GetLocal("fg"))
        ]
        p.run(code)
        self.assertEqual(p.acc(), 1)

        # while true
        #   try
        #     break
        #   end
        # end
        code = [
            While(True, [
                TryCatchFinally([Break()], [], [])
            ])
        ]
        p.run(code)

        # l = []
        # foreach x [1, 2, 3]
        #   try
        #     continue
        #     l += x
        #   end
        # end
        code = [
            SetLocal('l', []),
            Foreach('x', [1, 2, 3], [
                TryCatchFinally([
                    Continue(),
                    Append(GetLocal('l'), GetLocal('x'))
                ], [], [])
            ])
        ]
        p.run(code)
        self.assertEqual(p.getenv()['l'], [])

        # try
        # end
        p.run([TryCatchFinally([], [], [])])

        # try
        #   return 1
        # finally
        #   throw KeyError("")
        # end
        code = [
            TryCatchFinally([
                Return(1)
            ], [], [
                Throw(GetLocal("KeyError"), "")
            ])
        ]
        with self.assertRaises(CommandProcessorError):
            p.run(code)

        # while true
        #   try
        #     continue
        #   finally
        #     break
        #   end
        # end
        code = [
            While(True, [
                TryCatchFinally([
                    Continue()
                ], [], [
                    Break()
                ])
            ])
        ]
        p.run(code)

        # while true
        #   try
        #     throw KeyError("")
        #   catch KeyError
        #     continue
        #   finally
        #     break
        #   end
        # end
        code = [
            While(True, [
                TryCatchFinally([
                    Throw(GetLocal("KeyError"), "")
                ], [('KeyError', "", [Continue()])], [
                    Break()
                ])
            ])
        ]
        p.run(code)

        # try
        #   throw KeyError("")
        # catch KeyError
        #   continue
        # finally
        #   break
        # end
        code = [
            TryCatchFinally([
                Throw(GetLocal("KeyError"), "")
            ], [('KeyError', "", [Continue()])], [
                Break()
            ])
        ]
        with self.assertRaises(CommandProcessorError):
            p.run(code)

        # try
        #   throw KeyError("")
        # catch KeyError
        #   break
        # finally
        #   continue
        # end
        code = [
            TryCatchFinally([
                Throw(GetLocal("KeyError"), "")
            ], [('KeyError', "", [Break()])], [
                Continue()
            ])
        ]
        with self.assertRaises(CommandProcessorError):
            p.run(code)

        # foreach x [1, 2, 3]
        #   try
        #     break
        #   finally
        #     continue
        #   end
        # end
        code = [
            Foreach('x', [1, 2, 3, "abc"], [
                TryCatchFinally([Break()], [], [Continue()])
            ])
        ]
        p.run(code)
        self.assertEqual(p.getenv()['x'], "abc")

        # foreach x [1, 2, 3]
        #   try
        #     throw KeyError("")
        #   catch KeyError
        #     break
        #   finally
        #     continue
        #   end
        # end
        code = [
            Foreach('x', [1, 2, "def"], [
                TryCatchFinally([
                    Throw(GetLocal("KeyError"), "")
                ], [
                    ('KeyError', "", [Break()])
                ], [
                    Continue()
                ])
            ])
        ]
        p.run(code)
        self.assertEqual(p.getenv()['x'], "def")
    #-def

    def test_bad_cases(self):
        p = CommandProcessor()

        with self.assertRaises(CommandProcessorError):
            p.run([Throw(1, "")])
        with self.assertRaises(CommandProcessorError):
            p.run([Throw(GetLocal("KeyError"), 0)])
        with self.assertRaises(CommandProcessorError):
            p.run([Rethrow(0)])
    #-def

    def test_deferror(self):
        m = "Oook!"
        p = CommandProcessor()
        env = p.getenv()

        p.run([
            DefError('MyError', GetLocal('Exception')),
            TryCatchFinally([
                Throw(GetLocal('MyError'), m)
            ], [
                ('MyError', 'e', [SetLocal('x', GetLocal('e'))])
            ], [])
        ])
        self.assertIs(env.getvar('x').ecls, env.getvar('MyError'))
        self.assertEqual(env.getvar('x').emsg, m)

        p.run([
            TryCatchFinally([
                DefError('MySecondError', GetLocal('u'))
            ], [
                ('NameError', "", [SetLocal('x', 42)])
            ], [])
        ])
        self.assertEqual(env.getvar('x'), 42)

        p.run([
            TryCatchFinally([
                DefError('MySecondError', GetLocal('x'))
            ], [
                ('TypeError', "", [SetLocal('x', 43)])
            ], [])
        ])
        self.assertEqual(env.getvar('x'), 43)

        p.run([
            DefError('E', GetLocal('Exception')),
            Block(
                DefError('E', GetLocal('Exception')),
                SetLocal('X', GetLocal('E'), 1)
            ),
            TryCatchFinally([
                Throw(GetLocal('E'), "1")
            ], [
                ('X', "", [SetLocal('a', 11)]),
                ('E', "", [SetLocal('a', 12)])
            ], []),
            TryCatchFinally([
                Throw(GetLocal('X'), "2")
            ], [
                ('E', "", [SetLocal('b', 13)]),
                ('X', "", [SetLocal('b', 14)])
            ], [])
        ])
        self.assertEqual(env.getvar('a'), 12)
        self.assertEqual(env.getvar('b'), 14)
    #-def
#-class

class TestSetItemCase(unittest.TestCase):

    def test_equality(self):
        self.assertNotEqual(
            SetItem(GetLocal('x'), 1, "u"), 1
        )
        self.assertNotEqual(
            SetItem(GetLocal('x'), 1, "u"),
            SetItem(GetLocal('y'), 1, "u")
        )
        self.assertNotEqual(
            SetItem(GetLocal('x'), 1, "u"),
            SetItem(GetLocal('x'), 2, "u")
        )
        self.assertNotEqual(
            SetItem(GetLocal('x'), 1, "u"),
            SetItem(GetLocal('x'), 1, "v")
        )
        self.assertEqual(
            SetItem(GetLocal('x'), 1, "u"),
            SetItem(GetLocal('x'), 1, "u")
        )
    #-def

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

    def test_equality(self):
        self.assertNotEqual(
            DelItem(0, "c"), 1
        )
        self.assertNotEqual(
            DelItem(0, "c"), DelItem(1, "c")
        )
        self.assertNotEqual(
            DelItem(0, "c"), DelItem(0, "d")
        )
        self.assertEqual(
            DelItem(0, "c"), DelItem(0, "c")
        )
    #-def

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

    def test_equality(self):
        self.assertNotEqual(
            Append(GetLocal('x'), 42), 1
        )
        self.assertNotEqual(
            Append(GetLocal('x'), 42), Append(GetLocal('y'), 42)
        )
        self.assertNotEqual(
            Append(GetLocal('x'), 42), Append(GetLocal('x'), 41)
        )
        self.assertEqual(
            Append(GetLocal('x'), 42), Append(GetLocal('x'), 42)
        )
    #-def

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

    def test_equality(self):
        self.assertNotEqual(
            Insert([1, 2], 3, 1), 1
        )
        self.assertNotEqual(
            Insert([1, 2], 3, 1), Insert([1, 2, 3], 3, 1)
        )
        self.assertNotEqual(
            Insert([1, 2], 3, 1), Insert([1, 2], 4, 1)
        )
        self.assertNotEqual(
            Insert([1, 2], 3, 1), Insert([1, 2], 3, 0)
        )
        self.assertEqual(
            Insert([1, 2], 3, 1), Insert([1, 2], 3, 1)
        )
    #-def

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

    def test_equality(self):
        self.assertNotEqual(
            Remove(GetLocal('x'), 'a'), 1
        )
        self.assertNotEqual(
            Remove(GetLocal('x'), 'a'), Remove(GetLocal('y'), 'a')
        )
        self.assertNotEqual(
            Remove(GetLocal('x'), 'a'), Remove(GetLocal('x'), 'b')
        )
        self.assertEqual(
            Remove(GetLocal('x'), 'a'), Remove(GetLocal('x'), 'a')
        )
    #-def

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

    def test_equality(self):
        self.assertNotEqual(
            RemoveAll(GetLocal('x'), 'a'), 1
        )
        self.assertNotEqual(
            RemoveAll(GetLocal('x'), 'a'), RemoveAll(GetLocal('y'), 'a')
        )
        self.assertNotEqual(
            RemoveAll(GetLocal('x'), 'a'), RemoveAll(GetLocal('x'), 'b')
        )
        self.assertEqual(
            RemoveAll(GetLocal('x'), 'a'), RemoveAll(GetLocal('x'), 'a')
        )
    #-def

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

    def test_equality(self):
        self.assertNotEqual(
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x')),
            1
        )
        self.assertNotEqual(
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x')),
            Each([3, 5, 7, 9], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x'))
        )
        self.assertNotEqual(
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x')),
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('y'))
                ))
            ], []), 2, GetLocal('x'))
        )
        self.assertNotEqual(
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x')),
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 3, GetLocal('x'))
        )
        self.assertNotEqual(
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x')),
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('y'))
        )
        self.assertEqual(
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x')),
            Each([3, 5, 7], Lambda(['x', 'k', 'l'], False, [
                Append(GetLocal('l'), Mul(
                    GetLocal('k'), Mul(GetLocal('x'), GetLocal('x'))
                ))
            ], []), 2, GetLocal('x'))
        )
    #-def

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

    def test_equality(self):
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
        g = Lambda(['n', 'args'], True, [
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
                    Concat(GetItem(GetLocal('args'), 2), ")."
                    ))))))
                )
            ], [
                Return()
            ])])
        ], [])

        self.assertNotEqual(
            Visit(u, f, 0, "x", "y"), 1
        )
        self.assertNotEqual(
            Visit(0, f, 0, "x", "y"), Visit(u, f, 0, "x", "y")
        )
        self.assertNotEqual(
            Visit(u, f, 0, "x", "y"), Visit(u, g, 0, "x", "y")
        )
        self.assertNotEqual(
            Visit(u, f, 0, "x", "y"), Visit(u, f, 1, "x", "y")
        )
        self.assertNotEqual(
            Visit(u, f, 0, "x", "y"), Visit(u, f, 0, "_x", "y")
        )
        self.assertNotEqual(
            Visit(u, f, 0, "x", "y"), Visit(u, f, 0, "x", "_y")
        )
        self.assertEqual(
            Visit(u, f, 0, "x", "y"), Visit(u, f, 0, "x", "y")
        )
    #-def

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

    def test_equality(self):
        self.assertNotEqual(
            Print(
                "(", 1, " + ", GetLocal("x"), " = ", Add(1, GetLocal("x")), ")"
            ),
            1
        )
        self.assertNotEqual(
            Print(
                "(", 1, " + ", GetLocal("x"), " = ", Add(1, GetLocal("x")), ")"
            ),
            Print(
                "(", 1, " + ", GetLocal("x"), " = ", Add(1, GetLocal("x"))
            )
        )
        self.assertEqual(
            Print(
                "(", 1, " + ", GetLocal("x"), " = ", Add(1, GetLocal("x")), ")"
            ),
            Print(
                "(", 1, " + ", GetLocal("x"), " = ", Add(1, GetLocal("x")), ")"
            )
        )
    #-def

    def test_Print(self):
        p = Printer()

        p.run([SetLocal("x", 2), Print(
            "(", 1, " + ", GetLocal("x"), " = ", Add(1, GetLocal("x")), ")"
        )])
        self.assertEqual(p.output, "(1 + 2 = 3)")
    #-def
#-class

class TestModuleCase(unittest.TestCase):

    def test_equality(self):
        # DefModule
        self.assertNotEqual(DefModule("m", [GetLocal("u")]), SetLocal("m", 1))
        self.assertNotEqual(
            DefModule("m", [GetLocal("u")]), DefModule("M", [GetLocal("u")])
        )
        self.assertNotEqual(
            DefModule("m", [GetLocal("t")]), DefModule("m", [GetLocal("u")])
        )
        self.assertEqual(
            DefModule("m", [GetLocal("u")]), DefModule("m", [GetLocal("u")])
        )

        # SetMember
        self.assertNotEqual(
            SetMember(GetMember(GetLocal('E'), 'F'), 'p', 42),
            1
        )
        self.assertNotEqual(
            SetMember(GetMember(GetLocal('E'), 'F'), 'p', 42),
            SetMember(GetMember(GetLocal('E'), 'X'), 'p', 42)
        )
        self.assertNotEqual(
            SetMember(GetMember(GetLocal('E'), 'F'), 'p', 42),
            SetMember(GetMember(GetLocal('E'), 'F'), '_p', 42)
        )
        self.assertNotEqual(
            SetMember(GetMember(GetLocal('E'), 'F'), 'p', 42),
            SetMember(GetMember(GetLocal('E'), 'F'), 'p', 41)
        )
        self.assertEqual(
            SetMember(GetMember(GetLocal('E'), 'F'), 'p', 42),
            SetMember(GetMember(GetLocal('E'), 'F'), 'p', 42)
        )

        # GetMember
        self.assertNotEqual(
            GetMember(GetMember(GetLocal(""), 'A'), 'x'), 1
        )
        self.assertNotEqual(
            GetMember(GetMember(GetLocal(""), 'A'), 'x'),
            GetMember(GetMember(GetLocal(""), 'B'), 'x')
        )
        self.assertNotEqual(
            GetMember(GetMember(GetLocal(""), 'A'), 'x'),
            GetMember(GetMember(GetLocal(""), 'A'), 'y')
        )
        self.assertEqual(
            GetMember(GetMember(GetLocal(""), 'A'), 'x'),
            GetMember(GetMember(GetLocal(""), 'A'), 'x')
        )
    #-def

    def test_modules(self):
        p = Printer()

        self.assertIs(p.getenv()[""], p.getenv()["this"])
        self.assertIsInstance(p.getenv()[""], Module)

        # x = 1
        # module A
        #   x = 2
        #   module B
        #     x = 3
        #     function f()
        #       x = 4
        #       print :x :A:x :A:B:x A:x A:B:x B:x this:x x
        #     end
        #   end
        # end
        p.run([
            SetLocal('x', 1),
            DefModule("A", [
                SetLocal('x', 2),
                DefModule("B", [
                    SetLocal('x', 3),
                    Define("f", [], [], False, [
                        SetLocal('x', 4),
                        Print(
                            GetMember(GetLocal(""), 'x'),
                            GetMember(GetMember(GetLocal(""), 'A'), 'x'),
                            GetMember(
                                GetMember(GetMember(GetLocal(""), 'A'), 'B'),
                                'x'
                            ),
                            GetMember(GetLocal('A'), 'x'),
                            GetMember(GetMember(GetLocal('A'), 'B'), 'x'),
                            GetMember(GetLocal('B'), 'x'),
                            GetMember(GetLocal('this'), 'x'),
                            GetLocal('x')
                        )
                    ])
                ])
            ])
        ])

        p.run([
            Call(GetMember(GetMember(GetLocal('A'), 'B'), 'f'))
        ])
        self.assertEqual(p.output, "12323334")
        p.run([p.getenv()['A']])
        self.assertIsInstance(p.acc(), Module)
        self.assertIs(p.acc(), p.getenv()['A'])

        with self.assertRaises(CommandProcessorError):
            p.run([
                DefModule('_', [
                    Break()
                ])
            ])
        with self.assertRaises(CommandProcessorError):
            p.run([
                DefModule('_1', [
                    DefModule('_2', [
                        DefModule('_3', [
                            DefModule('_4', [
                                Continue()
                            ])
                        ])
                    ])
                ])
            ])

        p.run([
            DefModule('C', [
                Return(42),
                SetLocal('z', 8)
            ])
        ])
        self.assertEqual(p.acc(), 42)
        with self.assertRaises(CommandProcessorError):
            p.run([GetMember(GetLocal('C'), 'z')])

        p.run([
            SetLocal('_z', 3),
            DefModule('D', [
                Return(GetLocal('_z'))
            ])
        ])
        self.assertEqual(p.acc(), 3)
        with self.assertRaises(CommandProcessorError):
            p.run([GetMember(GetLocal('D'), '_z')])

        p.run([
            SetLocal('p', 4),
            DefModule('E', [
                DefModule('F', [
                    SetLocal("t", 'a'),
                    Define("g", [], [], False, [
                        Return(GetLocal("t"))
                    ]),
                    Define("_g", [], [], False, [
                        Return(GetMember(GetLocal("this"), 't'))
                    ])
                ])
            ])
        ])
        with self.assertRaises(CommandProcessorError):
            p.run([GetMember(GetMember(GetLocal('E'), 'F'), 'p')])
        p.run([SetMember(GetMember(GetLocal('E'), 'F'), 'p', 42)])
        p.run([GetMember(GetMember(GetLocal('E'), 'F'), 'p')])
        self.assertEqual(p.acc(), 42)
        p.run([GetMember(GetMember(GetLocal('E'), 'F'), 't')])
        self.assertEqual(p.acc(), 'a')
        p.run([
            Call(GetMember(GetMember(GetLocal('E'), 'F'), 'g'))
        ])
        self.assertEqual(p.acc(), 'a')
        p.run([
            Call(GetMember(GetMember(GetLocal('E'), 'F'), '_g'))
        ])
        self.assertEqual(p.acc(), 'a')

        with self.assertRaises(CommandProcessorError):
            p.run([GetMember(1, 'x')])
        with self.assertRaises(CommandProcessorError):
            p.run([SetMember(1, 'x', 0)])
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommandCase))
    suite.addTest(unittest.makeSuite(TestConstCase))
    suite.addTest(unittest.makeSuite(TestVersionCase))
    suite.addTest(unittest.makeSuite(TestExpandCase))
    suite.addTest(unittest.makeSuite(TestSetLocalCase))
    suite.addTest(unittest.makeSuite(TestGetLocalCase))
    suite.addTest(unittest.makeSuite(TestOperationsCase))
    suite.addTest(unittest.makeSuite(TestBlockCase))
    suite.addTest(unittest.makeSuite(TestIfCase))
    suite.addTest(unittest.makeSuite(TestLoopCase))
    suite.addTest(unittest.makeSuite(TestCallCase))
    suite.addTest(unittest.makeSuite(TestTryCatchFinallyCase))
    suite.addTest(unittest.makeSuite(TestSetItemCase))
    suite.addTest(unittest.makeSuite(TestDelItemCase))
    suite.addTest(unittest.makeSuite(TestAppendCase))
    suite.addTest(unittest.makeSuite(TestInsertCase))
    suite.addTest(unittest.makeSuite(TestRemoveCase))
    suite.addTest(unittest.makeSuite(TestRemoveAllCase))
    suite.addTest(unittest.makeSuite(TestEachCase))
    suite.addTest(unittest.makeSuite(TestVisitCase))
    suite.addTest(unittest.makeSuite(TestPrintCase))
    suite.addTest(unittest.makeSuite(TestModuleCase))
    return suite
#-def
