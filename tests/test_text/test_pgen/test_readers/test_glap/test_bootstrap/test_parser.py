#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/ \
#!              test_readers/test_glap/test_bootstrap/test_parser.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2017-05-15 15:16:20 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
GLAP bootstrap parser tests.\
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

from doit.support.cmd.runtime import \
    Location
from doit.support.cmd.commands import \
    Const, \
    MacroNode, MacroNodeSequence, MacroNodeAtom, MacroNodeParam, \
    Expand, \
    SetLocal, GetLocal, \
    DefMacro, Define, DefModule, \
    Add, Sub, Mul, Div, Mod, Neg, \
    BitAnd, BitOr, BitXor, ShiftL, ShiftR, Inv, \
    Lt, Gt, Le, Ge, Eq, Ne, Is, \
    And, Or, Not, \
    NewPair, NewList, NewHashMap, \
    Concat, Join, Merge, \
    Contains, \
    GetItem, \
    Lambda, \
    Block, If, Foreach, While, DoWhile, Break, Continue, \
    Call, Return, \
    TryCatchFinally, Throw, Rethrow, \
    SetItem, \
    SetMember, GetMember

from doit.text.pgen.errors import ParsingError

from doit.text.pgen.models.action import \
    Block as ABlock
from doit.text.pgen.models.cfgram import \
    Epsilon, Sym, Literal, Var, Range, Action, \
    DoNotRecord, Complement, \
    Iteration, PositiveIteration, Optional, \
    Label, Catenation, SetMinus, Alternation

from doit.text.pgen.readers.glap.bootstrap.pp.commands import \
    DefRule, DefGrammar

from doit.text.pgen.readers.glap.bootstrap import \
    make_location, SetLocation, \
    GlapLexError, GlapSyntaxError, \
    GlapContext, \
    GlapStream, \
    GlapParserActions

from doit.text.pgen.readers.glap.bootstrap.parser import \
    GLAP_ID, GLAP_INT, GLAP_FLOAT, GLAP_STR, \
    GLAP_INT_DEC, GLAP_INT_OCT, GLAP_INT_HEX, \
    GlapToken, \
    GlapLexer, \
    GlapParser

class FakeContext(object):
    __slots__ = [ 'stream', 'lexer' ]

    def __init__(self):
        self.stream = None
        self.lexer = None
    #-def
#-class

class FakeStream(object):
    __slots__ = [ 'context', 'name', 'data', 'pos', 'size' ]

    def __init__(self, ctx, name, s):
        ctx.stream = self
        self.context = ctx
        self.name = name
        self.data = s
        self.pos = 0
        self.size = len(s)
    #-def
#-class

class FakeToken(object):
    __slots__ = [ 'loc' ]

    def __init__(self):
        self.loc = -1
    #-def

    def position(self):
        return self.loc
    #-def
#-class

class FakeLexer(object):
    __slots__ = [ 'token' ]

    def __init__(self, ctx):
        ctx.lexer = self
        self.token = None
    #-def
#-class

class TestMakeLocationCase(unittest.TestCase):

    def test_make_location(self):
        ctx = FakeContext()
        stream = FakeStream(ctx, name_001, sample_001)

        self.assertEqual(make_location(ctx), (name_001, 1, 1))

        p = 26
        self.assertEqual(stream.data[p : p + 10], "sample_001")
        self.assertEqual(make_location(ctx, p), (name_001, 3, 8))

        p = 18
        stream.pos = p
        self.assertEqual(stream.data[p : p + 2], "\nm")
        self.assertEqual(make_location(ctx), (name_001, 2, 1))

        stream.pos = stream.size
        self.assertEqual(make_location(ctx), (name_001, 8, 1))
    #-def
#-class

class TestGlapErrorsCase(unittest.TestCase):

    def test_glap_errors(self):
        ctx = FakeContext()
        FakeStream(ctx, name_001, sample_001)
        FakeLexer(ctx)

        with self.assertRaises(ParsingError):
            raise GlapLexError(ctx, "Lex error")

        with self.assertRaises(ParsingError):
            raise GlapSyntaxError(ctx, "Syntax error")

        ctx.lexer.token = FakeToken()
        ctx.lexer.token.loc = 26
        with self.assertRaises(ParsingError):
            raise GlapSyntaxError(ctx, "Syntax error")
    #-def
#-class

class TestGlapContextCase(unittest.TestCase):

    def test_glap_context_members(self):
        ctx = GlapContext()
        ctx.stream
        ctx.lexer
        ctx.parser
        ctx.actions
        ctx.env
        ctx.processor
    #-def
#-class

class TestGlapStreamCase(unittest.TestCase):

    def test_ctor(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)

        self.assertIs(ctx.stream, stream)
        self.assertIs(stream.context, ctx)
        self.assertIs(stream.name, name_001)
        self.assertIs(stream.data, sample_001)
        self.assertEqual(stream.pos, 0)
        self.assertEqual(stream.size, len(sample_001))
    #-def

    def test_peek_and_next(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)

        self.assertEqual(stream.peek(1), sample_001[0])
        self.assertEqual(stream.peek(2), sample_001[0:2])
        self.assertEqual(stream.pos, 0)
        stream.next()
        self.assertEqual(stream.peek(1), sample_001[1])
        self.assertEqual(stream.peek(2), sample_001[1:3])
        self.assertEqual(stream.pos, 1)
        stream.next(2)
        self.assertEqual(stream.peek(1), sample_001[3])
        self.assertEqual(stream.peek(2), sample_001[3:5])
        self.assertEqual(stream.pos, 3)
    #-def

    def test_match(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)
        stream.next(26)

        with self.assertRaises(ParsingError):
            stream.match("sample#00152")

        self.assertEqual(stream.pos, 26)
        self.assertEqual(stream.match("sample_001"), "sample_001")
        self.assertEqual(stream.pos, 36)

        stream.pos = stream.size
        with self.assertRaises(ParsingError):
            stream.match("a")
    #-def

    def test_matchset(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)

        with self.assertRaises(ParsingError):
            stream.matchset([])
        with self.assertRaises(ParsingError):
            stream.matchset(['a', 'b', 'c'])
        with self.assertRaises(ParsingError):
            stream.matchset("")
        with self.assertRaises(ParsingError):
            stream.matchset("abc")

        self.assertEqual(stream.matchset(['-', ' ']), sample_001[0])

        stream.pos = stream.size - 1
        with self.assertRaises(ParsingError):
            stream.matchset(['a'])
        self.assertEqual(stream.matchset("\n\t"), sample_001[-1])
        self.assertEqual(stream.pos, stream.size)
        with self.assertRaises(ParsingError):
            stream.matchset("\n\t")
    #-def

    def test_matchif(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)
        WS = lambda x: x in [ '\n', '\t', ' ' ]
        WS_NAME = "white space"

        with self.assertRaises(ParsingError):
            stream.matchif(WS, WS_NAME)
        stream.pos = stream.size - 1
        self.assertEqual(stream.matchif(WS, WS_NAME), sample_001[-1])
        self.assertEqual(stream.pos, stream.size)
        with self.assertRaises(ParsingError):
            stream.matchif(WS, WS_NAME)
    #-def

    def test_matchmany(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)
        lcchars = "abcdefghijklmnopqrstuvwxyz"

        stream.pos = 19
        self.assertEqual(stream.matchmany(lcchars), "module")
        self.assertEqual(stream.pos, 25)
        self.assertEqual(stream.matchmany(lcchars), "")
        self.assertEqual(stream.pos, 25)
        stream.pos = stream.size
        self.assertEqual(stream.matchmany(lcchars), "")
        self.assertEqual(stream.pos, stream.size)
    #-def

    def test_matchmanyif(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)
        lcchars = lambda x: ord('a') <= ord(x) and ord(x) <= ord('z')

        stream.pos = 19
        self.assertEqual(stream.matchmanyif(lcchars), "module")
        self.assertEqual(stream.pos, 25)
        self.assertEqual(stream.matchmanyif(lcchars), "")
        self.assertEqual(stream.pos, 25)
        stream.pos = stream.size
        self.assertEqual(stream.matchmanyif(lcchars), "")
        self.assertEqual(stream.pos, stream.size)
    #-def

    def test_matchplus(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)
        lcchars = "abcdefghijklmnopqrstuvwxyz"
        lcchars_name = "lower case letter"

        stream.pos = 19
        self.assertEqual(stream.matchplus(lcchars), "module")
        self.assertEqual(stream.pos, 25)
        with self.assertRaises(ParsingError):
            stream.matchplus(lcchars)
        self.assertEqual(stream.pos, 25)
        stream.pos = stream.size
        with self.assertRaises(ParsingError):
            stream.matchplus(lcchars)
        self.assertEqual(stream.pos, stream.size)
    #-def

    def test_matchplusif(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)
        lcchars = lambda x: ord('a') <= ord(x) and ord(x) <= ord('z')
        lcchars_name = "lower case letter"

        stream.pos = 19
        self.assertEqual(stream.matchplusif(lcchars, lcchars_name), "module")
        self.assertEqual(stream.pos, 25)
        with self.assertRaises(ParsingError):
            stream.matchplusif(lcchars, lcchars_name)
        self.assertEqual(stream.pos, 25)
        stream.pos = stream.size
        with self.assertRaises(ParsingError):
            stream.matchplusif(lcchars, lcchars_name)
        self.assertEqual(stream.pos, stream.size)
    #-def

    def test_matchopt(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)

        stream.pos = 19
        self.assertEqual(stream.matchopt(['m'], '+'), "m")
        self.assertEqual(stream.pos, 20)
        self.assertEqual(stream.matchopt(['m'], '+'), "+")
        self.assertEqual(stream.pos, 20)
        stream.pos = stream.size - 1
        self.assertEqual(stream.matchopt(['m'], '+'), "+")
        self.assertEqual(stream.pos, stream.size - 1)
        self.assertEqual(stream.matchopt(['\n', '\r'], '+'), "\n")
        self.assertEqual(stream.pos, stream.size)
        self.assertEqual(stream.matchopt(['\n', '\r'], '+'), "+")
        self.assertEqual(stream.pos, stream.size)
    #-def

    def test_matchoptif(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_001, sample_001)
        f = lambda x: x in ['m']
        g = lambda x: x in ['\n', '\r']

        stream.pos = 19
        self.assertEqual(stream.matchoptif(f, '+'), "m")
        self.assertEqual(stream.pos, 20)
        self.assertEqual(stream.matchoptif(f, '+'), "+")
        self.assertEqual(stream.pos, 20)
        stream.pos = stream.size - 1
        self.assertEqual(stream.matchoptif(f, '+'), "+")
        self.assertEqual(stream.pos, stream.size - 1)
        self.assertEqual(stream.matchoptif(g, '+'), "\n")
        self.assertEqual(stream.pos, stream.size)
        self.assertEqual(stream.matchoptif(g, '+'), "+")
        self.assertEqual(stream.pos, stream.size)
    #-def

    def test_matchn(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_002, sample_002)
        xdigs = "0123456789abcdefABCDEF"

        stream.pos = 27
        self.assertEqual(stream.matchn(xdigs, 4), "012f")
        self.assertEqual(stream.pos, 31)

        stream.pos = stream.size - 4
        self.assertEqual(stream.matchn("\nden", 4), "end\n")
        self.assertEqual(stream.pos, stream.size)

        stream.pos = stream.size - 2
        with self.assertRaises(ParsingError):
            stream.matchn("\nden", 4)
        stream.pos = stream.size - 2
        with self.assertRaises(ParsingError):
            stream.matchn("\nden", 3)
        stream.pos = stream.size - 2
        self.assertEqual(stream.matchn("\nden", 2), "d\n")
        self.assertEqual(stream.pos, stream.size)

        stream.pos = 29
        with self.assertRaises(ParsingError):
            stream.matchn(xdigs, 4)
        stream.pos = 29
        with self.assertRaises(ParsingError):
            stream.matchn(xdigs, 3)
        stream.pos = 29
        self.assertEqual(stream.matchn(xdigs, 2), "2f")
    #-def

    def test_matchnif(self):
        ctx = GlapContext()
        stream = GlapStream(ctx, name_002, sample_002)
        xdigs = lambda x: x in list("0123456789abcdefABCDEF")
        xdigs_name = "hexadecimal digit"
        f = lambda x: x in list("\nedn")
        f_name = "one of '\\n', 'e', 'd', or 'n'"

        stream.pos = 27
        self.assertEqual(stream.matchnif(xdigs, 4, xdigs_name), "012f")
        self.assertEqual(stream.pos, 31)

        stream.pos = stream.size - 4
        self.assertEqual(stream.matchnif(f, 4, f_name), "end\n")
        self.assertEqual(stream.pos, stream.size)

        stream.pos = stream.size - 2
        with self.assertRaises(ParsingError):
            stream.matchnif(f, 4, f_name)
        stream.pos = stream.size - 2
        with self.assertRaises(ParsingError):
            stream.matchnif(f, 3, f_name)
        stream.pos = stream.size - 2
        self.assertEqual(stream.matchnif(f, 2, f_name), "d\n")
        self.assertEqual(stream.pos, stream.size)

        stream.pos = 29
        with self.assertRaises(ParsingError):
            stream.matchnif(xdigs, 4, xdigs_name)
        stream.pos = 29
        with self.assertRaises(ParsingError):
            stream.matchnif(xdigs, 3, xdigs_name)
        stream.pos = 29
        self.assertEqual(stream.matchnif(xdigs, 2, xdigs_name), "2f")
    #-def
#-class

class TestGlapTokenCase(unittest.TestCase):

    def test_glap_token_methods(self):
        p = 26
        t = GlapToken(GLAP_ID, p, sample_001[p : p + 10])

        self.assertEqual(t.ttype, GLAP_ID)
        self.assertEqual(t.position(), p)
        self.assertEqual(t.data[1], (sample_001[p : p + 10],))

        self.assertEqual(GlapToken.tokname("=="), "'=='")
        self.assertEqual(GlapToken.tokname(GLAP_ID), "identifier")
        self.assertEqual(GlapToken.tokname(0), "<unknown>")
    #-def
#-class

lex_sample_name_001 = "lex_sample_001.l"
lex_sample_data_001 = """\

-- Comment @#$%^&*()-_++=-abcdefghijklmnopqrstuvwxyz0123456789
-------------------------

-------------------------------------------------------------------------------
-- !! Anothe comment                                                         --
-------------------------------------------------------------------------------

  --Příliš žluťoučký kůň úpěl ďábelské ódy.--

"""
lex_sample_toks_001 = [
]

lex_sample_name_002 = "lex_sample_002.l"
lex_sample_data_002 = """\
i Ab -- Two identifiers

selection

t890 _0
4t 44t44 45tp_ij90 end

-- End of input.

"""
lex_sample_toks_002 = [
  GlapToken(GLAP_ID, 0, "i"),
  GlapToken(GLAP_ID, 2, "Ab"),
  GlapToken(GLAP_ID, 25, "selection"),
  GlapToken(GLAP_ID, 36, "t890"),
  GlapToken(GLAP_ID, 41, "_0"),
  GlapToken(GLAP_INT, 44, GLAP_INT_DEC, "4"),
  GlapToken(GLAP_ID, 45, "t"),
  GlapToken(GLAP_INT, 47, GLAP_INT_DEC, "44"),
  GlapToken(GLAP_ID, 49, "t44"),
  GlapToken(GLAP_INT, 53, GLAP_INT_DEC, "45"),
  GlapToken(GLAP_ID, 55, "tp_ij90"),
  GlapToken("end", 63)
]

lex_sample_name_003 = "lex_sample_003.l"
lex_sample_data_003 = """\
-- Decimal integers:
1 26 135 1234567890

-- Octal integers:
0 07 0777 01243567

-- Hexadecimal integers:
0x0 0x00 0X0000 0XaAbBcCdDEeFf01234567890

-- Mix:
08 0182 0x0g08
"""
lex_sample_toks_003 = [
  GlapToken(GLAP_INT, 21, GLAP_INT_DEC, "1"),
  GlapToken(GLAP_INT, 23, GLAP_INT_DEC, "26"),
  GlapToken(GLAP_INT, 26, GLAP_INT_DEC, "135"),
  GlapToken(GLAP_INT, 30, GLAP_INT_DEC, "1234567890"),
  GlapToken(GLAP_INT, 61, GLAP_INT_OCT, "0"),
  GlapToken(GLAP_INT, 63, GLAP_INT_OCT, "07"),
  GlapToken(GLAP_INT, 66, GLAP_INT_OCT, "0777"),
  GlapToken(GLAP_INT, 71, GLAP_INT_OCT, "01243567"),
  GlapToken(GLAP_INT, 106, GLAP_INT_HEX, "0"),
  GlapToken(GLAP_INT, 110, GLAP_INT_HEX, "00"),
  GlapToken(GLAP_INT, 115, GLAP_INT_HEX, "0000"),
  GlapToken(GLAP_INT, 122, GLAP_INT_HEX, "aAbBcCdDEeFf01234567890"),
  GlapToken(GLAP_INT, 157, GLAP_INT_OCT, "0"),
  GlapToken(GLAP_INT, 158, GLAP_INT_DEC, "8"),
  GlapToken(GLAP_INT, 160, GLAP_INT_OCT, "01"),
  GlapToken(GLAP_INT, 162, GLAP_INT_DEC, "82"),
  GlapToken(GLAP_INT, 165, GLAP_INT_HEX, "0"),
  GlapToken(GLAP_ID, 168, "g08")
]

lex_sample_name_004 = "lex_sample_004.l"
lex_sample_data_004 = ""
lex_sample_toks_004 = []

lex_sample_name_005 = "lex_sample_005.l"
lex_sample_data_005 = """\
-- Lex error in numbers:
0x
"""
lex_sample_toks_005 = [
]

lex_sample_name_006 = "lex_sample_006.l"
lex_sample_data_006 = """\
-- Lex error in numbers:
0X
"""
lex_sample_toks_006 = [
]

lex_sample_name_007 = "lex_sample_007.l"
lex_sample_data_007 = """\
-- Floats:
1.5 2.07 3e0 3E1 0.0 3e+0 0e-0 0E-1 0e-2
0.1 3.14 2.17 0.5E-15 0.0e+8 0.0e+0
123.456e-31
"""
lex_sample_toks_007 = [
  GlapToken(GLAP_FLOAT, 11, "1", "5", ""),
  GlapToken(GLAP_FLOAT, 15, "2", "07", ""),
  GlapToken(GLAP_FLOAT, 20, "3", "", "+0"),
  GlapToken(GLAP_FLOAT, 24, "3", "", "+1"),
  GlapToken(GLAP_FLOAT, 28, "0", "0", ""),
  GlapToken(GLAP_FLOAT, 32, "3", "", "+0"),
  GlapToken(GLAP_FLOAT, 37, "0", "", "-0"),
  GlapToken(GLAP_FLOAT, 42, "0", "", "-1"),
  GlapToken(GLAP_FLOAT, 47, "0", "", "-2"),
  GlapToken(GLAP_FLOAT, 52, "0", "1", ""),
  GlapToken(GLAP_FLOAT, 56, "3", "14", ""),
  GlapToken(GLAP_FLOAT, 61, "2", "17", ""),
  GlapToken(GLAP_FLOAT, 66, "0", "5", "-15"),
  GlapToken(GLAP_FLOAT, 74, "0", "0", "+8"),
  GlapToken(GLAP_FLOAT, 81, "0", "0", "+0"),
  GlapToken(GLAP_FLOAT, 88, "123", "456", "-31")
]

lex_sample_name_008 = "lex_sample_008.l"
lex_sample_data_008 = """\
-- Strings:
"" ""\"" "" "" " "
"a"  "A"  "_" "0" "Č"
"\\""  "\\\\"  "\\'"  "\\a" "\\b" "\\t" "\\n" "\\v" "\\f" "\\r"
"\\0" "\\1" "\\01" "\\77" "\\000" "\\007" "\\107" "\\087" "\\778"
"\\xff"  "\\u013f"  "abcd"
"\\na\\nb"   "\\"ab\\""   "\\'c\\'"  "'xxx'"   "\\"\""\\""
"\\a\\b\\t\\n\\v\\f\\r  \\\\\\'\\"  0a\\7ž\\x40\\u01FFABČ\\n"
"""
lex_sample_toks_008 = [
  GlapToken(GLAP_STR, 12, ""),
  GlapToken(GLAP_STR, 15, ""),
  GlapToken(GLAP_STR, 17, ""),
  GlapToken(GLAP_STR, 20, ""),
  GlapToken(GLAP_STR, 23, ""),
  GlapToken(GLAP_STR, 26, " "),
  GlapToken(GLAP_STR, 30, "a"),
  GlapToken(GLAP_STR, 35, "A"),
  GlapToken(GLAP_STR, 40, "_"),
  GlapToken(GLAP_STR, 44, "0"),
  GlapToken(GLAP_STR, 48, "Č"),
  GlapToken(GLAP_STR, 52, "\""),
  GlapToken(GLAP_STR, 58, "\\"),
  GlapToken(GLAP_STR, 64, "'"),
  GlapToken(GLAP_STR, 70, "\a"),
  GlapToken(GLAP_STR, 75, "\b"),
  GlapToken(GLAP_STR, 80, "\t"),
  GlapToken(GLAP_STR, 85, "\n"),
  GlapToken(GLAP_STR, 90, "\v"),
  GlapToken(GLAP_STR, 95, "\f"),
  GlapToken(GLAP_STR, 100, "\r"),
  GlapToken(GLAP_STR, 105, "\x00"),
  GlapToken(GLAP_STR, 110, "\x01"),
  GlapToken(GLAP_STR, 115, "\x01"),
  GlapToken(GLAP_STR, 121, "?"),
  GlapToken(GLAP_STR, 127, "\x00"),
  GlapToken(GLAP_STR, 134, "\x07"),
  GlapToken(GLAP_STR, 141, "G"),
  GlapToken(GLAP_STR, 148, "\x0087"),
  GlapToken(GLAP_STR, 155, "?8"),
  GlapToken(GLAP_STR, 162, "\xff"),
  GlapToken(GLAP_STR, 170, "\u013f"),
  GlapToken(GLAP_STR, 180, "abcd"),
  GlapToken(GLAP_STR, 187, "\na\nb"),
  GlapToken(GLAP_STR, 198, "\"ab\""),
  GlapToken(GLAP_STR, 209, "'c'"),
  GlapToken(GLAP_STR, 218, "'xxx'"),
  GlapToken(GLAP_STR, 228, "\""),
  GlapToken(GLAP_STR, 232, "\""),
  GlapToken(GLAP_STR, 237, "\a\b\t\n\v\f\r  \\'\"  0a\x07ž@\u01ffABČ\n")
]

lex_sample_name_009 = "lex_sample_009.l"
lex_sample_data_009 = """\
-+*/()=>===== =======+++for foreach if elif
"""
lex_sample_toks_009 = [
  GlapToken('-', 0),
  GlapToken('+', 1),
  GlapToken('*', 2),
  GlapToken('/', 3),
  GlapToken('(', 4),
  GlapToken(')', 5),
  GlapToken('=>', 6),
  GlapToken('===', 8),
  GlapToken('==', 11),
  GlapToken('===', 14),
  GlapToken('===', 17),
  GlapToken('=', 20),
  GlapToken('++', 21),
  GlapToken('+', 23),
  GlapToken('for', 24),
  GlapToken('foreach', 28),
  GlapToken('if', 36),
  GlapToken('elif', 39)
]

lex_samples = [
  (True, lex_sample_name_001, lex_sample_data_001, lex_sample_toks_001),
  (True, lex_sample_name_002, lex_sample_data_002, lex_sample_toks_002),
  (True, lex_sample_name_003, lex_sample_data_003, lex_sample_toks_003),
  (True, lex_sample_name_004, lex_sample_data_004, lex_sample_toks_004),
  (False, lex_sample_name_005, lex_sample_data_005, lex_sample_toks_005),
  (False, lex_sample_name_006, lex_sample_data_006, lex_sample_toks_006),
  (True, lex_sample_name_007, lex_sample_data_007, lex_sample_toks_007),
  (False, "error.l", "--\n  0.\n", []),
  (False, "error.l", "--\n \n 1.\n", []),
  (False, "error.l", "--\n \n  12.\n", []),
  (False, "error.l", "--\n  0.e5\n", []),
  (False, "error.l", "--\n  1.e5\n", []),
  (False, "error.l", "--\n \n  12.e5\n", []),
  (False, "error.l", "--\n 0e", []),
  (False, "error.l", "--\n 0E ", []),
  (False, "error.l", "--\n 0e+ ", []),
  (False, "error.l", "--\n \n0E+", []),
  (False, "error.l", "--\n \n0e-", []),
  (False, "error.l", "--\n  0E-", []),
  (False, "error.l", "--\n 1E-", []),
  (False, "error.l", "--\n 1e-", []),
  (False, "error.l", "--\n  1E+ ", []),
  (False, "error.l", "--\n  \n     2e+ ", []),
  (False, "error.l", "--\n  \n   3e", []),
  (False, "error.l", "--\n  \n    4E", []),
  (True, lex_sample_name_008, lex_sample_data_008, lex_sample_toks_008),
  (False, "error.l", "--\n \"", []),
  (False, "error.l", "--\n\"\n", []),
  (False, "error.l", "--\n \"abc", []),
  (False, "error.l", "--\n \"\\", []),
  (False, "error.l", "--\n \"\\\n\"", []),
  (False, "error.l", "--\n \"\\/\"", []),
  (False, "error.l", "--\n \"a\\zb\"", []),
  (False, "error.l", "--\n \"xy\\x\"", []),
  (False, "error.l", "--\n \"u\\x0", []),
  (False, "error.l", "--\n \"u\\x0\"", []),
  (False, "error.l", "--\n \"u\\x0t\"", []),
  (False, "error.l", "--\n \"\\8\"", []),
  (False, "error.l", "--\n \"\\8", []),
  (False, "error.l", "--\n \"\\u\"", []),
  (False, "error.l", "--\n \"\\u", []),
  (False, "error.l", "--\n \"\\u1\"", []),
  (False, "error.l", "--\n \"\\u1", []),
  (False, "error.l", "--\n  \"s\\u1Ag\"", []),
  (False, "error.l", "--\n \"tw\\u0AF", []),
  (False, "error.l", "--\n \"tw\\u0AF\"", []),
  (False, "error.l", "--\n  \"ty\\u0aFZ", []),
  (False, "error.l", "--\n   \"ty\\u0AFZ\"", []),
  (False, "error.l", "--\n  \"zz\\u0FF", []),
  (False, "error.l", "--\n \"\5a\"", []),
  (False, "error.l", "--\n    \"c\tb\"", []),
  (False, "error.l", "--\n  \"x\x14y\"", []),
  (False, "error.l", "--\n \"\x7fu\"", []),
  (False, "error.l", "--\n   \"c\x7f", []),
  (True, lex_sample_name_009, lex_sample_data_009, lex_sample_toks_009),
  (False, "error.l", "--\n @ r", [])
]

class TestGlapLexerCase(unittest.TestCase):

    def test_glap_lexer_ctor(self):
        ctx = GlapContext()
        GlapStream(ctx, "?", "abcd")
        lexer = GlapLexer(ctx)

        self.assertIs(ctx.lexer, lexer)
        self.assertIs(lexer.context, ctx)
        self.assertIsNone(lexer.token)
    #-def

    def test_asserteof(self):
        ctx = GlapContext()
        GlapStream(ctx, "?", "abcd--\n-- abcd")
        lexer = GlapLexer(ctx)

        with self.assertRaises(ParsingError):
            lexer.asserteof()
        lexer.next()
        lexer.asserteof()
    #-def

    def test_test(self):
        ctx = GlapContext()
        GlapStream(ctx, "?", ";")
        lexer = GlapLexer(ctx)

        self.assertFalse(lexer.test())
        self.assertTrue(lexer.test(";"))
        self.assertTrue(lexer.test(";", None))

        ctx = GlapContext()
        GlapStream(ctx, "?", "--;")
        lexer = GlapLexer(ctx)

        self.assertFalse(lexer.test())
        self.assertFalse(lexer.test(";"))
        self.assertTrue(lexer.test(";", None))
    #-def

    def test_match(self):
        ctx = GlapContext()
        GlapStream(ctx, "?", "abcd 123 #")
        lexer = GlapLexer(ctx)

        with self.assertRaises(ParsingError):
            lexer.match()
        with self.assertRaises(ParsingError):
            lexer.match(GLAP_STR, GLAP_FLOAT, GLAP_INT)
        with self.assertRaises(ParsingError):
            lexer.match(GLAP_STR, '=>', GLAP_INT)
        with self.assertRaises(ParsingError):
            lexer.match(GLAP_STR, GLAP_FLOAT)
        with self.assertRaises(ParsingError):
            lexer.match('#', GLAP_FLOAT)
        with self.assertRaises(ParsingError):
            lexer.match(GLAP_STR)
        with self.assertRaises(ParsingError):
            lexer.match('$')

        self.assertEqual(
            lexer.match(GLAP_INT, '#', ';', GLAP_ID),
            GlapToken(GLAP_ID, 0, "abcd")
        )
        self.assertEqual(
            lexer.match(GLAP_INT, '#', ';', GLAP_ID),
            GlapToken(GLAP_INT, 5, GLAP_INT_DEC, "123")
        )
        self.assertEqual(
            lexer.match(GLAP_INT, '#', ';', GLAP_ID),
            GlapToken('#', 9)
        )
        with self.assertRaises(ParsingError):
            lexer.match(GLAP_INT, '#', ';', GLAP_ID)
    #-def

    def test_tokenizing(self):
        for t in lex_samples:
            self.do_tokenizing_test(*t)
    #-def

    def do_tokenizing_test(self, should_succeed, name, data, toks):
        result = []
        if not should_succeed:
            with self.assertRaises(ParsingError):
                self.lex_tokenize(name, data, result)
        else:
            self.lex_tokenize(name, data, result)
        self.maxDiff = None
        self.assertEqual(result, toks)
    #-def

    def lex_tokenize(self, n, s, r):
        ctx = GlapContext()
        GlapStream(ctx, n, s)
        lexer = GlapLexer(ctx)

        while lexer.peek():
            r.append(lexer.peek())
            lexer.next()
    #-def
#-class

test_samples = []

name_001 = "sample_001.g"
sample_001 = """\
-- Sample grammar

module sample_001
  grammar X
    start -> "a"+;
  end
end
"""
ast_001 = DefModule("sample_001", [
    DefGrammar("X", [], [
        DefRule(
            "start",
            Sym("a") .set_location(name_001, 5, 14)\
            ['+']    .set_location(name_001, 5, 17),
            False
        ).set_location(name_001, 5, 5)
    ]).set_location(name_001, 4, 3)
]).set_location(name_001, 3, 1)
test_samples.append((True, name_001, sample_001, ast_001))

name_002 = "sample_002.g"
sample_002 = """\
module sample_002
  x = "\\u012f";
end
"""
ast_002 = DefModule("sample_002", [
    SetLocal(
        "x",
        Const("\u012f").set_location(name_002, 2, 7)
    ).set_location(name_002, 2, 5)
]).set_location(name_002, 1, 1)
test_samples.append((True, name_002, sample_002, ast_002))

name_003 = "sample_003.g"
sample_003 = """\
-- Module expected.
"""
ast_003 = None
test_samples.append((False, name_003, sample_003, ast_003))

name_004 = "sample_004.g"
sample_004 = """\
module A
end

-- Expected end of input.
module B
end
"""
ast_004 = None
test_samples.append((False, name_004, sample_004, ast_004))

name_005 = "sample_005.g"
sample_005 = """\
module
end
"""
ast_005 = None
test_samples.append((False, name_005, sample_005, ast_005))

name_006 = "sample_006.g"
sample_006 = """\
module A

"""
ast_006 = None
test_samples.append((False, name_006, sample_006, ast_006))

name_007 = "sample_007.g"
sample_007 = """\
module A

  module B
  end

  module C
  end

end
"""
ast_007 = DefModule("A", [
    DefModule("B", []).set_location(name_007, 3, 3),
    DefModule("C", []).set_location(name_007, 6, 3)
]).set_location(name_007, 1, 1)
test_samples.append((True, name_007, sample_007, ast_007))

name_008 = "sample_008.g"
sample_008 = """\
module A
  grammar 1 end
end
"""
ast_008 = None
test_samples.append((False, name_008, sample_008, ast_008))

name_009 = "sample_009.g"
sample_009 = """\
module A
  grammar G( end
end
"""
ast_009 = None
test_samples.append((False, name_009, sample_009, ast_009))

name_010 = "sample_010.g"
sample_010 = """\
module A
  grammar G () end
end
"""
ast_010 = DefModule("A", [
    DefGrammar("G", [], []).set_location(name_010, 2, 3)
]).set_location(name_010, 1, 1)
test_samples.append((True, name_010, sample_010, ast_010))

name_011 = "sample_011.g"
sample_011 = """\
module A
  grammar G (1) end
end
"""
ast_011 = None
test_samples.append((False, name_011, sample_011, ast_011))

name_012 = "sample_012.g"
sample_012 = """\
module A
  grammar G (G1) end
end
"""
ast_012 = DefModule("A", [
    DefGrammar("G", [("G1", Location(name_012, 2, 14))], [
    ]).set_location(name_012, 2, 3)
]).set_location(name_012, 1, 1)
test_samples.append((True, name_012, sample_012, ast_012))

name_013 = "sample_013.g"
sample_013 = """\
module A
  grammar G (G1,) end
end
"""
ast_013 = None
test_samples.append((False, name_013, sample_013, ast_013))

name_014 = "sample_014.g"
sample_014 = """\
module A
  grammar G (G1, G2) end
end
"""
ast_014 = DefModule("A", [
    DefGrammar("G", [
        ("G1", Location(name_014, 2, 14)),
        ("G2", Location(name_014, 2, 18))
    ], [
    ]).set_location(name_014, 2, 3)
]).set_location(name_014, 1, 1)
test_samples.append((True, name_014, sample_014, ast_014))

name_015 = "sample_015.g"
sample_015 = """\
module A
  grammar G
    .x = 1;
    a -> "b";
    .y = 2;
    .z = 3;
    b -> "c";
    c -> "d";
    d: "e";
  end
end
"""
ast_015 = DefModule("A", [
    DefGrammar("G", [], [
        SetLocal(
            "x",
            Const(1).set_location(name_015, 3, 10)
        ).set_location(name_015, 3, 8),
        DefRule(
            "a",
            Sym("b").set_location(name_015, 4, 10),
            False
        ).set_location(name_015, 4, 5),
        SetLocal(
            "y",
            Const(2).set_location(name_015, 5, 10)
        ).set_location(name_015, 5, 8),
        SetLocal(
            "z",
            Const(3).set_location(name_015, 6, 10)
        ).set_location(name_015, 6, 8),
        DefRule(
            "b",
            Sym("c").set_location(name_015, 7, 10),
            False
        ).set_location(name_015, 7, 5),
        DefRule(
            "c",
            Sym("d").set_location(name_015, 8, 10),
            False
        ).set_location(name_015, 8, 5),
        DefRule(
            "d",
            Sym("e").set_location(name_015, 9, 8),
            True
        ).set_location(name_015, 9, 5)
    ]).set_location(name_015, 2, 3)
]).set_location(name_015, 1, 1)
test_samples.append((True, name_015, sample_015, ast_015))

name_016 = "sample_016.g"
sample_016 = """\
module A
  grammar G
    a - "a";
  end
end
"""
ast_016 = None
test_samples.append((False, name_016, sample_016, ast_016))

name_017 = "sample_017.g"
sample_017 = """\
module A
  grammar G
    a -> "a" | "b";
    b -> "a" | "b" | "c";
  end
end
"""
ast_017 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Alternation(
                Sym("a").set_location(name_017, 3, 10),
                Sym("b").set_location(name_017, 3, 16)
            ).set_location(name_017, 3, 14),
            False
        ).set_location(name_017, 3, 5),
        DefRule(
            "b",
            Alternation(
                Alternation(
                    Sym("a").set_location(name_017, 4, 10),
                    Sym("b").set_location(name_017, 4, 16)
                ).set_location(name_017, 4, 14),
                Sym("c").set_location(name_017, 4, 22)
            ).set_location(name_017, 4, 20),
            False
        ).set_location(name_017, 4, 5)
    ]).set_location(name_017, 2, 3)
]).set_location(name_017, 1, 1)
test_samples.append((True, name_017, sample_017, ast_017))

name_018 = "sample_018.g"
sample_018 = """\
module A
  grammar G
    a -> "a" | "b" - "c" - "d";
  end
end
"""
ast_018 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Alternation(
                Sym("a").set_location(name_018, 3, 10),
                SetMinus(
                    SetMinus(
                        Sym("b").set_location(name_018, 3, 16),
                        Sym("c").set_location(name_018, 3, 22)
                    ).set_location(name_018, 3, 20),
                    Sym("d").set_location(name_018, 3, 28)
                ).set_location(name_018, 3, 26)
            ).set_location(name_018, 3, 14),
            False
        ).set_location(name_018, 3, 5)
    ]).set_location(name_018, 2, 3)
]).set_location(name_018, 1, 1)
test_samples.append((True, name_018, sample_018, ast_018))

name_019 = "sample_019.g"
sample_019 = """\
module A
  grammar G
    a->"a""b""c""d";
  end
end
"""
ast_019 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Catenation(
                Catenation(
                    Catenation(
                        Sym("a").set_location(name_019, 3, 8),
                        Sym("b").set_location(name_019, 3, 11)
                    ).set_location(name_019, 3, 11),
                    Sym("c").set_location(name_019, 3, 14)
                ).set_location(name_019, 3, 14),
                Sym("d").set_location(name_019, 3, 17)
            ).set_location(name_019, 3, 17),
            False
        ).set_location(name_019, 3, 5)
    ]).set_location(name_019, 2, 3)
]).set_location(name_019, 1, 1)
test_samples.append((True, name_019, sample_019, ast_019))

name_020 = "sample_020.g"
sample_020 = """\
module A
  grammar G(_G)
    a -> "a" - "b" "c" | "d";
  end
end
"""
ast_020 = DefModule("A", [
    DefGrammar("G", [("_G", Location(name_020, 2, 13))], [
        DefRule(
            "a",
            Alternation(
                SetMinus(
                    Sym("a").set_location(name_020, 3, 10),
                    Catenation(
                        Sym("b").set_location(name_020, 3, 16),
                        Sym("c").set_location(name_020, 3, 20)
                    ).set_location(name_020, 3, 20)
                ).set_location(name_020, 3, 14),
                Sym("d").set_location(name_020, 3, 26)
            ).set_location(name_020, 3, 24),
            False
        ).set_location(name_020, 3, 5)
    ]).set_location(name_020, 2, 3)
]).set_location(name_020, 1, 1)
test_samples.append((True, name_020, sample_020, ast_020))

name_021 = "sample_021.g"
sample_021 = """\
module A
  grammar G
    a -> "a"*;
  end
end
"""
ast_021 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Iteration(
                Sym("a").set_location(name_021, 3, 10)
            ).set_location(name_021, 3, 13),
            False
        ).set_location(name_021, 3, 5)
    ]).set_location(name_021, 2, 3)
]).set_location(name_021, 1, 1)
test_samples.append((True, name_021, sample_021, ast_021))

name_022 = "sample_022.g"
sample_022 = """\
module A
  grammar G
    a -> "a"+;
  end
end
"""
ast_022 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            PositiveIteration(
                Sym("a").set_location(name_022, 3, 10)
            ).set_location(name_022, 3, 13),
            False
        ).set_location(name_022, 3, 5)
    ]).set_location(name_022, 2, 3)
]).set_location(name_022, 1, 1)
test_samples.append((True, name_022, sample_022, ast_022))

name_023 = "sample_023.g"
sample_023 = """\
module A
  grammar G
    a -> "a" ?;
  end
end
"""
ast_023 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Optional(
                Sym("a").set_location(name_023, 3, 10)
            ).set_location(name_023, 3, 14),
            False
        ).set_location(name_023, 3, 5)
    ]).set_location(name_023, 2, 3)
]).set_location(name_023, 1, 1)
test_samples.append((True, name_023, sample_023, ast_023))

name_024 = "sample_024.g"
sample_024 = """\
module A
  grammar G
    a -> "a"* "b"? | "c"+ + - "d"*+?;
  end
end
"""
ast_024 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Alternation(
                Catenation(
                    Iteration(
                        Sym("a").set_location(name_024, 3, 10)
                    ).set_location(name_024, 3, 13),
                    Optional(
                        Sym("b").set_location(name_024, 3, 15)
                    ).set_location(name_024, 3, 18)
                ).set_location(name_024, 3, 15),
                SetMinus(
                    PositiveIteration(
                        PositiveIteration(
                            Sym("c").set_location(name_024, 3, 22)
                        ).set_location(name_024, 3, 25)
                    ).set_location(name_024, 3, 27),
                    Optional(
                        PositiveIteration(
                            Iteration(
                                Sym("d").set_location(name_024, 3, 31)
                            ).set_location(name_024, 3, 34)
                        ).set_location(name_024, 3, 35)
                    ).set_location(name_024, 3, 36)
                ).set_location(name_024, 3, 29)
            ).set_location(name_024, 3, 20),
            False
        ).set_location(name_024, 3, 5)
    ]).set_location(name_024, 2, 3)
]).set_location(name_024, 1, 1)
test_samples.append((True, name_024, sample_024, ast_024))

name_025 = "sample_025.g"
sample_025 = """\
module A
  grammar G
    a -> -"a";
    b -> ~"b";
  end
end
"""
ast_025 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            DoNotRecord(
                Sym("a").set_location(name_025, 3, 11)
            ).set_location(name_025, 3, 10),
            False
        ).set_location(name_025, 3, 5),
        DefRule(
            "b",
            Complement(
                Sym("b").set_location(name_025, 4, 11)
            ).set_location(name_025, 4, 10),
            False
        ).set_location(name_025, 4, 5)
    ]).set_location(name_025, 2, 3)
]).set_location(name_025, 1, 1)
test_samples.append((True, name_025, sample_025, ast_025))

name_026 = "sample_026.g"
sample_026 = """\
module A
  grammar G
    a -> -~"a" - - -"b";
  end
end
"""
ast_026 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            SetMinus(
                DoNotRecord(
                    Complement(
                        Sym("a").set_location(name_026, 3, 12)
                    ).set_location(name_026, 3, 11)
                ).set_location(name_026, 3, 10),
                DoNotRecord(
                    DoNotRecord(
                        Sym("b").set_location(name_026, 3, 21)
                    ).set_location(name_026, 3, 20)
                ).set_location(name_026, 3, 18)
            ).set_location(name_026, 3, 16),
            False
        ).set_location(name_026, 3, 5)
    ]).set_location(name_026, 2, 3)
]).set_location(name_026, 1, 1)
test_samples.append((True, name_026, sample_026, ast_026))

name_027 = "sample_027.g"
sample_027 = """\
module A
  grammar G
    a -> "a"'letter_a;
  end
end
"""
ast_027 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Label(
                Sym("a").set_location(name_027, 3, 10),
                Var("letter_a").set_location(name_027, 3, 14)
            ).set_location(name_027, 3, 13),
            False
        ).set_location(name_027, 3, 5)
    ]).set_location(name_027, 2, 3)
]).set_location(name_027, 1, 1)
test_samples.append((True, name_027, sample_027, ast_027))

name_028 = "sample_028.g"
sample_028 = """\
module A
  grammar G
    a -> "a" ' letter_a ' x;
  end
end
"""
ast_028 = None
test_samples.append((False, name_028, sample_028, ast_028))

name_029 = "sample_029.g"
sample_029 = """\
module A
  grammar G
    a -> "a"''letter_a;
  end
end
"""
ast_029 = None
test_samples.append((False, name_029, sample_029, ast_029))

name_030 = "sample_030.g"
sample_030 = """\
module A
  grammar G
    a -> letter_a;
    b -> eps;
    c -> (a);
    d -> {};
  end
end
"""
ast_030 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Var("letter_a").set_location(name_030, 3, 10),
            False
        ).set_location(name_030, 3, 5),
        DefRule(
            "b",
            Epsilon().set_location(name_030, 4, 10),
            False
        ).set_location(name_030, 4, 5),
        DefRule(
            "c",
            Var("a").set_location(name_030, 5, 11),
            False
        ).set_location(name_030, 5, 5),
        DefRule(
            "d",
            Action(
                ABlock([]).set_location(name_030, 6, 10)
            ).set_location(name_030, 6, 10),
            False
        ).set_location(name_030, 6, 5)
    ]).set_location(name_030, 2, 3)
]).set_location(name_030, 1, 1)
test_samples.append((True, name_030, sample_030, ast_030))

name_031 = "sample_031.g"
sample_031 = """\
module A
  grammar G
    a -> #
  end
end
"""
ast_031 = None
test_samples.append((False, name_031, sample_031, ast_031))

name_032 = "sample_032.g"
sample_032 = """\
module A
  grammar G
    a ->
"""
ast_032 = None
test_samples.append((False, name_032, sample_032, ast_032))

name_033 = "sample_033.g"
sample_033 = """\
module A
  grammar G
    a -> "b".."c";
  end
end
"""
ast_033 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Range(
                Sym("b").set_location(name_033, 3, 10),
                Sym("c").set_location(name_033, 3, 15)
            ).set_location(name_033, 3, 10),
            False
        ).set_location(name_033, 3, 5)
    ]).set_location(name_033, 2, 3)
]).set_location(name_033, 1, 1)
test_samples.append((True, name_033, sample_033, ast_033))

name_034 = "sample_034.g"
sample_034 = """\
module A
  grammar G
    a -> "" | "ab";
  end
end
"""
ast_034 = DefModule("A", [
    DefGrammar("G", [], [
        DefRule(
            "a",
            Alternation(
                Epsilon().set_location(name_034, 3, 10),
                Literal("ab").set_location(name_034, 3, 15)
            ).set_location(name_034, 3, 13),
            False
        ).set_location(name_034, 3, 5)
    ]).set_location(name_034, 2, 3)
]).set_location(name_034, 1, 1)
test_samples.append((True, name_034, sample_034, ast_034))

name_035 = "sample_035.g"
sample_035 = """\
module A
  grammar G
    a -> "" .. "a";
  end
end
"""
ast_035 = None
test_samples.append((False, name_035, sample_035, ast_035))

name_036 = "sample_036.g"
sample_036 = """\
module A
  grammar G
    a -> "ab" .. "a";
  end
end
"""
ast_036 = None
test_samples.append((False, name_036, sample_036, ast_036))

name_037 = "sample_037.g"
sample_037 = """\
module A
  grammar G
    a -> "a" .. "";
  end
end
"""
ast_037 = None
test_samples.append((False, name_037, sample_037, ast_037))

name_038 = "sample_038.g"
sample_038 = """\
module A
  grammar G
    a -> "a" .. "aa";
  end
end
"""
ast_038 = None
test_samples.append((False, name_038, sample_038, ast_038))

name_039 = "sample_039.g"
sample_039 = """\
module A
  grammar G
    a -> "b" .. "a";
  end
end
"""
ast_039 = None
test_samples.append((False, name_039, sample_039, ast_039))

name_040 = "sample_040.g"
sample_040 = """\
module A
  x = y;
end
"""
ast_040 = DefModule("A", [
    SetLocal(
        "x",
        GetLocal("y").set_location(name_040, 2, 7)
    ).set_location(name_040, 2, 5)
]).set_location(name_040, 1, 1)
test_samples.append((True, name_040, sample_040, ast_040))

name_041 = "sample_041.g"
sample_041 = """\
module A
  x += y;
end
"""
ast_041 = DefModule("A", [
    SetLocal(
        "x",
        Add(
            GetLocal("x").set_location(name_041, 2, 3),
            GetLocal("y").set_location(name_041, 2, 8)
        ).set_location(name_041, 2, 5)
    ).set_location(name_041, 2, 5)
]).set_location(name_041, 1, 1)
test_samples.append((True, name_041, sample_041, ast_041))

name_042 = "sample_042.g"
sample_042 = """\
module A
  x = y += z;
end
"""
ast_042 = DefModule("A", [
    SetLocal(
        "y",
        Add(
            GetLocal("y").set_location(name_042, 2, 7),
            GetLocal("z").set_location(name_042, 2, 12)
        ).set_location(name_042, 2, 9)
    ).set_location(name_042, 2, 9),
    SetLocal(
        "x",
        GetLocal("y").set_location(name_042, 2, 7)
    ).set_location(name_042, 2, 5)
]).set_location(name_042, 1, 1)
test_samples.append((True, name_042, sample_042, ast_042))

name_043 = "sample_043.g"
sample_043 = """\
module A
  x -= y;
end
"""
ast_043 = DefModule("A", [
    SetLocal(
        "x",
        Sub(
            GetLocal("x").set_location(name_043, 2, 3),
            GetLocal("y").set_location(name_043, 2, 8)
        ).set_location(name_043, 2, 5)
    ).set_location(name_043, 2, 5)
]).set_location(name_043, 1, 1)
test_samples.append((True, name_043, sample_043, ast_043))

name_044 = "sample_044.g"
sample_044 = """\
module A
  x *= y;
end
"""
ast_044 = DefModule("A", [
    SetLocal(
        "x",
        Mul(
            GetLocal("x").set_location(name_044, 2, 3),
            GetLocal("y").set_location(name_044, 2, 8)
        ).set_location(name_044, 2, 5)
    ).set_location(name_044, 2, 5)
]).set_location(name_044, 1, 1)
test_samples.append((True, name_044, sample_044, ast_044))

name_045 = "sample_045.g"
sample_045 = """\
module A
  x /= y;
end
"""
ast_045 = DefModule("A", [
    SetLocal(
        "x",
        Div(
            GetLocal("x").set_location(name_045, 2, 3),
            GetLocal("y").set_location(name_045, 2, 8)
        ).set_location(name_045, 2, 5)
    ).set_location(name_045, 2, 5)
]).set_location(name_045, 1, 1)
test_samples.append((True, name_045, sample_045, ast_045))

name_046 = "sample_046.g"
sample_046 = """\
module A
  x %= y;
end
"""
ast_046 = DefModule("A", [
    SetLocal(
        "x",
        Mod(
            GetLocal("x").set_location(name_046, 2, 3),
            GetLocal("y").set_location(name_046, 2, 8)
        ).set_location(name_046, 2, 5)
    ).set_location(name_046, 2, 5)
]).set_location(name_046, 1, 1)
test_samples.append((True, name_046, sample_046, ast_046))

name_047 = "sample_047.g"
sample_047 = """\
module A
  x &= y;
end
"""
ast_047 = DefModule("A", [
    SetLocal(
        "x",
        BitAnd(
            GetLocal("x").set_location(name_047, 2, 3),
            GetLocal("y").set_location(name_047, 2, 8)
        ).set_location(name_047, 2, 5)
    ).set_location(name_047, 2, 5)
]).set_location(name_047, 1, 1)
test_samples.append((True, name_047, sample_047, ast_047))

name_048 = "sample_048.g"
sample_048 = """\
module A
  x |= y;
end
"""
ast_048 = DefModule("A", [
    SetLocal(
        "x",
        BitOr(
            GetLocal("x").set_location(name_048, 2, 3),
            GetLocal("y").set_location(name_048, 2, 8)
        ).set_location(name_048, 2, 5)
    ).set_location(name_048, 2, 5)
]).set_location(name_048, 1, 1)
test_samples.append((True, name_048, sample_048, ast_048))

name_049 = "sample_049.g"
sample_049 = """\
module A
  x ^= y;
end
"""
ast_049 = DefModule("A", [
    SetLocal(
        "x",
        BitXor(
            GetLocal("x").set_location(name_049, 2, 3),
            GetLocal("y").set_location(name_049, 2, 8)
        ).set_location(name_049, 2, 5)
    ).set_location(name_049, 2, 5)
]).set_location(name_049, 1, 1)
test_samples.append((True, name_049, sample_049, ast_049))

name_050 = "sample_050.g"
sample_050 = """\
module A
  x <<= y;
end
"""
ast_050 = DefModule("A", [
    SetLocal(
        "x",
        ShiftL(
            GetLocal("x").set_location(name_050, 2, 3),
            GetLocal("y").set_location(name_050, 2, 9)
        ).set_location(name_050, 2, 5)
    ).set_location(name_050, 2, 5)
]).set_location(name_050, 1, 1)
test_samples.append((True, name_050, sample_050, ast_050))

name_051 = "sample_051.g"
sample_051 = """\
module A
  x >>= y;
end
"""
ast_051 = DefModule("A", [
    SetLocal(
        "x",
        ShiftR(
            GetLocal("x").set_location(name_051, 2, 3),
            GetLocal("y").set_location(name_051, 2, 9)
        ).set_location(name_051, 2, 5)
    ).set_location(name_051, 2, 5)
]).set_location(name_051, 1, 1)
test_samples.append((True, name_051, sample_051, ast_051))

name_052 = "sample_052.g"
sample_052 = """\
module A
  x &&= y;
end
"""
ast_052 = DefModule("A", [
    SetLocal(
        "x",
        And(
            GetLocal("x").set_location(name_052, 2, 3),
            GetLocal("y").set_location(name_052, 2, 9)
        ).set_location(name_052, 2, 5)
    ).set_location(name_052, 2, 5)
]).set_location(name_052, 1, 1)
test_samples.append((True, name_052, sample_052, ast_052))

name_053 = "sample_053.g"
sample_053 = """\
module A
  x ||= y;
end
"""
ast_053 = DefModule("A", [
    SetLocal(
        "x",
        Or(
            GetLocal("x").set_location(name_053, 2, 3),
            GetLocal("y").set_location(name_053, 2, 9)
        ).set_location(name_053, 2, 5)
    ).set_location(name_053, 2, 5)
]).set_location(name_053, 1, 1)
test_samples.append((True, name_053, sample_053, ast_053))

name_054 = "sample_054.g"
sample_054 = """\
module A
  x .= y;
end
"""
ast_054 = DefModule("A", [
    SetLocal(
        "x",
        Concat(
            GetLocal("x").set_location(name_054, 2, 3),
            GetLocal("y").set_location(name_054, 2, 8)
        ).set_location(name_054, 2, 5)
    ).set_location(name_054, 2, 5)
]).set_location(name_054, 1, 1)
test_samples.append((True, name_054, sample_054, ast_054))

name_055 = "sample_055.g"
sample_055 = """\
module A
  x ++= y;
end
"""
ast_055 = DefModule("A", [
    SetLocal(
        "x",
        Join(
            GetLocal("x").set_location(name_055, 2, 3),
            GetLocal("y").set_location(name_055, 2, 9)
        ).set_location(name_055, 2, 5)
    ).set_location(name_055, 2, 5)
]).set_location(name_055, 1, 1)
test_samples.append((True, name_055, sample_055, ast_055))

name_056 = "sample_056.g"
sample_056 = """\
module A
  x ~~= y;
end
"""
ast_056 = DefModule("A", [
    SetLocal(
        "x",
        Merge(
            GetLocal("x").set_location(name_056, 2, 3),
            GetLocal("y").set_location(name_056, 2, 9)
        ).set_location(name_056, 2, 5)
    ).set_location(name_056, 2, 5)
]).set_location(name_056, 1, 1)
test_samples.append((True, name_056, sample_056, ast_056))

name_057 = "sample_057.g"
sample_057 = """\
module A
  x || y;
end
"""
ast_057 = DefModule("A", [
    Or(
        GetLocal("x").set_location(name_057, 2, 3),
        GetLocal("y").set_location(name_057, 2, 8)
    ).set_location(name_057, 2, 5)
]).set_location(name_057, 1, 1)
test_samples.append((True, name_057, sample_057, ast_057))

name_058 = "sample_058.g"
sample_058 = """\
module A
  x && y;
end
"""
ast_058 = DefModule("A", [
    And(
        GetLocal("x").set_location(name_058, 2, 3),
        GetLocal("y").set_location(name_058, 2, 8)
    ).set_location(name_058, 2, 5)
]).set_location(name_058, 1, 1)
test_samples.append((True, name_058, sample_058, ast_058))

name_059 = "sample_059.g"
sample_059 = """\
module A
  a && b || c && d || e && f && g;
end
"""
ast_059 = DefModule("A", [
    Or(
        Or(
            And(
                GetLocal("a").set_location(name_059, 2, 3),
                GetLocal("b").set_location(name_059, 2, 8)
            ).set_location(name_059, 2, 5),
            And(
                GetLocal("c").set_location(name_059, 2, 13),
                GetLocal("d").set_location(name_059, 2, 18)
            ).set_location(name_059, 2, 15)
        ).set_location(name_059, 2, 10),
        And(
            And(
                GetLocal("e").set_location(name_059, 2, 23),
                GetLocal("f").set_location(name_059, 2, 28)
            ).set_location(name_059, 2, 25),
            GetLocal("g").set_location(name_059, 2, 33)
        ).set_location(name_059, 2, 30)
    ).set_location(name_059, 2, 20)
]).set_location(name_059, 1, 1)
test_samples.append((True, name_059, sample_059, ast_059))

name_060 = "sample_060.g"
sample_060 = """\
module A
  a < b;
end
"""
ast_060 = DefModule("A", [
    Lt(
        GetLocal("a").set_location(name_060, 2, 3),
        GetLocal("b").set_location(name_060, 2, 7)
    ).set_location(name_060, 2, 5)
]).set_location(name_060, 1, 1)
test_samples.append((True, name_060, sample_060, ast_060))

name_061 = "sample_061.g"
sample_061 = """\
module A
  a > b;
end
"""
ast_061 = DefModule("A", [
    Gt(
        GetLocal("a").set_location(name_061, 2, 3),
        GetLocal("b").set_location(name_061, 2, 7)
    ).set_location(name_061, 2, 5)
]).set_location(name_061, 1, 1)
test_samples.append((True, name_061, sample_061, ast_061))

name_062 = "sample_062.g"
sample_062 = """\
module A
  a <= b;
end
"""
ast_062 = DefModule("A", [
    Le(
        GetLocal("a").set_location(name_062, 2, 3),
        GetLocal("b").set_location(name_062, 2, 8)
    ).set_location(name_062, 2, 5)
]).set_location(name_062, 1, 1)
test_samples.append((True, name_062, sample_062, ast_062))

name_063 = "sample_063.g"
sample_063 = """\
module A
  a >= b;
end
"""
ast_063 = DefModule("A", [
    Ge(
        GetLocal("a").set_location(name_063, 2, 3),
        GetLocal("b").set_location(name_063, 2, 8)
    ).set_location(name_063, 2, 5)
]).set_location(name_063, 1, 1)
test_samples.append((True, name_063, sample_063, ast_063))

name_064 = "sample_064.g"
sample_064 = """\
module A
  a == b;
end
"""
ast_064 = DefModule("A", [
    Eq(
        GetLocal("a").set_location(name_064, 2, 3),
        GetLocal("b").set_location(name_064, 2, 8)
    ).set_location(name_064, 2, 5)
]).set_location(name_064, 1, 1)
test_samples.append((True, name_064, sample_064, ast_064))

name_065 = "sample_065.g"
sample_065 = """\
module A
  a != b;
end
"""
ast_065 = DefModule("A", [
    Ne(
        GetLocal("a").set_location(name_065, 2, 3),
        GetLocal("b").set_location(name_065, 2, 8)
    ).set_location(name_065, 2, 5)
]).set_location(name_065, 1, 1)
test_samples.append((True, name_065, sample_065, ast_065))

name_066 = "sample_066.g"
sample_066 = """\
module A
  a === b;
end
"""
ast_066 = DefModule("A", [
    Is(
        GetLocal("a").set_location(name_066, 2, 3),
        GetLocal("b").set_location(name_066, 2, 9)
    ).set_location(name_066, 2, 5)
]).set_location(name_066, 1, 1)
test_samples.append((True, name_066, sample_066, ast_066))

name_067 = "sample_067.g"
sample_067 = """\
module A
  a in b;
end
"""
ast_067 = DefModule("A", [
    Contains(
        GetLocal("a").set_location(name_067, 2, 3),
        GetLocal("b").set_location(name_067, 2, 8)
    ).set_location(name_067, 2, 5)
]).set_location(name_067, 1, 1)
test_samples.append((True, name_067, sample_067, ast_067))

name_068 = "sample_068.g"
sample_068 = """\
module A
  a < x && x < b;
end
"""
ast_068 = DefModule("A", [
    And(
        Lt(
            GetLocal("a").set_location(name_068, 2, 3),
            GetLocal("x").set_location(name_068, 2, 7)
        ).set_location(name_068, 2, 5),
        Lt(
            GetLocal("x").set_location(name_068, 2, 12),
            GetLocal("b").set_location(name_068, 2, 16)
        ).set_location(name_068, 2, 14)
    ).set_location(name_068, 2, 9)
]).set_location(name_068, 1, 1)
test_samples.append((True, name_068, sample_068, ast_068))

name_069 = "sample_069.g"
sample_069 = """\
module A
  a < x < b;
end
"""
ast_069 = None
test_samples.append((False, name_069, sample_069, ast_069))

name_070 = "sample_070.g"
sample_070 = """\
module A
  a | b;
end
"""
ast_070 = DefModule("A", [
    BitOr(
        GetLocal("a").set_location(name_070, 2, 3),
        GetLocal("b").set_location(name_070, 2, 7)
    ).set_location(name_070, 2, 5)
]).set_location(name_070, 1, 1)
test_samples.append((True, name_070, sample_070, ast_070))

name_071 = "sample_071.g"
sample_071 = """\
module A
  a & b;
end
"""
ast_071 = DefModule("A", [
    BitAnd(
        GetLocal("a").set_location(name_071, 2, 3),
        GetLocal("b").set_location(name_071, 2, 7)
    ).set_location(name_071, 2, 5)
]).set_location(name_071, 1, 1)
test_samples.append((True, name_071, sample_071, ast_071))

name_072 = "sample_072.g"
sample_072 = """\
module A
  a ^ b;
end
"""
ast_072 = DefModule("A", [
    BitXor(
        GetLocal("a").set_location(name_072, 2, 3),
        GetLocal("b").set_location(name_072, 2, 7)
    ).set_location(name_072, 2, 5)
]).set_location(name_072, 1, 1)
test_samples.append((True, name_072, sample_072, ast_072))

name_073 = "sample_073.g"
sample_073 = """\
module A
  a | b | c;
  a | b & c;
  a | b ^ c;

  a & b | c;
  a & b & c;
  a & b ^ c;

  a ^ b | c;
  a ^ b & c;
  a ^ b ^ c;
end
"""
ast_073 = DefModule("A", [
    # a | b | c == (a | b) | c
    BitOr(
        BitOr(
            GetLocal("a").set_location(name_073, 2, 3),
            GetLocal("b").set_location(name_073, 2, 7)
        ).set_location(name_073, 2, 5),
        GetLocal("c").set_location(name_073, 2, 11)
    ).set_location(name_073, 2, 9),
    # a | b & c == a | (b & c)
    BitOr(
        GetLocal("a").set_location(name_073, 3, 3),
        BitAnd(
            GetLocal("b").set_location(name_073, 3, 7),
            GetLocal("c").set_location(name_073, 3, 11)
        ).set_location(name_073, 3, 9)
    ).set_location(name_073, 3, 5),
    # a | b ^ c == a | (b ^ c)
    BitOr(
        GetLocal("a").set_location(name_073, 4, 3),
        BitXor(
            GetLocal("b").set_location(name_073, 4, 7),
            GetLocal("c").set_location(name_073, 4, 11)
        ).set_location(name_073, 4, 9)
    ).set_location(name_073, 4, 5),

    # a & b | c == (a & b) | c
    BitOr(
        BitAnd(
            GetLocal("a").set_location(name_073, 6, 3),
            GetLocal("b").set_location(name_073, 6, 7)
        ).set_location(name_073, 6, 5),
        GetLocal("c").set_location(name_073, 6, 11)
    ).set_location(name_073, 6, 9),
    # a & b & c == (a & b) & c
    BitAnd(
        BitAnd(
            GetLocal("a").set_location(name_073, 7, 3),
            GetLocal("b").set_location(name_073, 7, 7)
        ).set_location(name_073, 7, 5),
        GetLocal("c").set_location(name_073, 7, 11)
    ).set_location(name_073, 7, 9),
    # a & b ^ c == a & (b ^ c)
    BitAnd(
        GetLocal("a").set_location(name_073, 8, 3),
        BitXor(
            GetLocal("b").set_location(name_073, 8, 7),
            GetLocal("c").set_location(name_073, 8, 11)
        ).set_location(name_073, 8, 9)
    ).set_location(name_073, 8, 5),

    # a ^ b | c == (a ^ b) | c
    BitOr(
        BitXor(
            GetLocal("a").set_location(name_073, 10, 3),
            GetLocal("b").set_location(name_073, 10, 7)
        ).set_location(name_073, 10, 5),
        GetLocal("c").set_location(name_073, 10, 11)
    ).set_location(name_073, 10, 9),
    # a ^ b & c == (a ^ b) & c
    BitAnd(
        BitXor(
            GetLocal("a").set_location(name_073, 11, 3),
            GetLocal("b").set_location(name_073, 11, 7)
        ).set_location(name_073, 11, 5),
        GetLocal("c").set_location(name_073, 11, 11)
    ).set_location(name_073, 11, 9),
    # a ^ b ^ c == (a ^ b) ^ c
    BitXor(
        BitXor(
            GetLocal("a").set_location(name_073, 12, 3),
            GetLocal("b").set_location(name_073, 12, 7)
        ).set_location(name_073, 12, 5),
        GetLocal("c").set_location(name_073, 12, 11)
    ).set_location(name_073, 12, 9)
]).set_location(name_073, 1, 1)
test_samples.append((True, name_073, sample_073, ast_073))

name_074 = "sample_074.g"
sample_074 = """\
module A
  a << b;
end
"""
ast_074 = DefModule("A", [
    ShiftL(
        GetLocal("a").set_location(name_074, 2, 3),
        GetLocal("b").set_location(name_074, 2, 8)
    ).set_location(name_074, 2, 5)
]).set_location(name_074, 1, 1)
test_samples.append((True, name_074, sample_074, ast_074))

name_075 = "sample_075.g"
sample_075 = """\
module A
  a >> b;
end
"""
ast_075 = DefModule("A", [
    ShiftR(
        GetLocal("a").set_location(name_075, 2, 3),
        GetLocal("b").set_location(name_075, 2, 8)
    ).set_location(name_075, 2, 5)
]).set_location(name_075, 1, 1)
test_samples.append((True, name_075, sample_075, ast_075))

name_076 = "sample_076.g"
sample_076 = """\
module A
  a + b;
end
"""
ast_076 = DefModule("A", [
    Add(
        GetLocal("a").set_location(name_076, 2, 3),
        GetLocal("b").set_location(name_076, 2, 7)
    ).set_location(name_076, 2, 5)
]).set_location(name_076, 1, 1)
test_samples.append((True, name_076, sample_076, ast_076))

name_077 = "sample_077.g"
sample_077 = """\
module A
  a - b;
end
"""
ast_077 = DefModule("A", [
    Sub(
        GetLocal("a").set_location(name_077, 2, 3),
        GetLocal("b").set_location(name_077, 2, 7)
    ).set_location(name_077, 2, 5)
]).set_location(name_077, 1, 1)
test_samples.append((True, name_077, sample_077, ast_077))

name_078 = "sample_078.g"
sample_078 = """\
module A
  a . b;
end
"""
ast_078 = DefModule("A", [
    Concat(
        GetLocal("a").set_location(name_078, 2, 3),
        GetLocal("b").set_location(name_078, 2, 7)
    ).set_location(name_078, 2, 5)
]).set_location(name_078, 1, 1)
test_samples.append((True, name_078, sample_078, ast_078))

name_079 = "sample_079.g"
sample_079 = """\
module A
  a ++ b;
end
"""
ast_079 = DefModule("A", [
    Join(
        GetLocal("a").set_location(name_079, 2, 3),
        GetLocal("b").set_location(name_079, 2, 8)
    ).set_location(name_079, 2, 5)
]).set_location(name_079, 1, 1)
test_samples.append((True, name_079, sample_079, ast_079))

name_080 = "sample_080.g"
sample_080 = """\
module A
  a ~~ b;
end
"""
ast_080 = DefModule("A", [
    Merge(
        GetLocal("a").set_location(name_080, 2, 3),
        GetLocal("b").set_location(name_080, 2, 8)
    ).set_location(name_080, 2, 5)
]).set_location(name_080, 1, 1)
test_samples.append((True, name_080, sample_080, ast_080))

name_081 = "sample_081.g"
sample_081 = """\
module A
  a * b;
end
"""
ast_081 = DefModule("A", [
    Mul(
        GetLocal("a").set_location(name_081, 2, 3),
        GetLocal("b").set_location(name_081, 2, 7)
    ).set_location(name_081, 2, 5)
]).set_location(name_081, 1, 1)
test_samples.append((True, name_081, sample_081, ast_081))

name_082 = "sample_082.g"
sample_082 = """\
module A
  a / b;
end
"""
ast_082 = DefModule("A", [
    Div(
        GetLocal("a").set_location(name_082, 2, 3),
        GetLocal("b").set_location(name_082, 2, 7)
    ).set_location(name_082, 2, 5)
]).set_location(name_082, 1, 1)
test_samples.append((True, name_082, sample_082, ast_082))

name_083 = "sample_083.g"
sample_083 = """\
module A
  a % b;
end
"""
ast_083 = DefModule("A", [
    Mod(
        GetLocal("a").set_location(name_083, 2, 3),
        GetLocal("b").set_location(name_083, 2, 7)
    ).set_location(name_083, 2, 5)
]).set_location(name_083, 1, 1)
test_samples.append((True, name_083, sample_083, ast_083))

name_084 = "sample_084.g"
sample_084 = """\
module A
  a b;
end
"""
ast_084 = DefModule("A", [
    Call(
        GetLocal("a").set_location(name_084, 2, 3),
        GetLocal("b").set_location(name_084, 2, 5)
    ).set_location(name_084, 2, 5)
]).set_location(name_084, 1, 1)
test_samples.append((True, name_084, sample_084, ast_084))

name_085 = "sample_085.g"
sample_085 = """\
module A
  a b c;
end
"""
ast_085 = DefModule("A", [
    Call(
        GetLocal("a").set_location(name_085, 2, 3),
        GetLocal("b").set_location(name_085, 2, 5),
        GetLocal("c").set_location(name_085, 2, 7)
    ).set_location(name_085, 2, 5)
]).set_location(name_085, 1, 1)
test_samples.append((True, name_085, sample_085, ast_085))

name_086 = "sample_086.g"
sample_086 = """\
module A
  a b 'c;
end
"""
ast_086 = DefModule("A", [
    Call(
        GetLocal("a").set_location(name_086, 2, 3),
        GetLocal("b").set_location(name_086, 2, 5),
        GetLocal("c").set_location(name_086, 2, 8)
    ).set_location(name_086, 2, 5)
]).set_location(name_086, 1, 1)
test_samples.append((True, name_086, sample_086, ast_086))

name_087 = "sample_087.g"
sample_087 = """\
module A
  a 'b 'c;
end
"""
ast_087 = DefModule("A", [
    Call(
        GetLocal("a").set_location(name_087, 2, 3),
        GetLocal("b").set_location(name_087, 2, 6),
        GetLocal("c").set_location(name_087, 2, 9)
    ).set_location(name_087, 2, 5)
]).set_location(name_087, 1, 1)
test_samples.append((True, name_087, sample_087, ast_087))

name_088 = "sample_088.g"
sample_088 = """\
module A
  -a; !b; ~c; -!~d; e - - -f;
end
"""
ast_088 = DefModule("A", [
    Neg(
        GetLocal("a").set_location(name_088, 2, 4)
    ).set_location(name_088, 2, 3),
    Not(
        GetLocal("b").set_location(name_088, 2, 8)
    ).set_location(name_088, 2, 7),
    Inv(
        GetLocal("c").set_location(name_088, 2, 12)
    ).set_location(name_088, 2, 11),
    Neg(
        Not(
            Inv(
                GetLocal("d").set_location(name_088, 2, 18)
            ).set_location(name_088, 2, 17)
        ).set_location(name_088, 2, 16)
    ).set_location(name_088, 2, 15),
    Sub(
        GetLocal("e").set_location(name_088, 2, 21),
        Neg(
            Neg(
                GetLocal("f").set_location(name_088, 2, 28)
            ).set_location(name_088, 2, 27)
        ).set_location(name_088, 2, 25)
    ).set_location(name_088, 2, 23)
]).set_location(name_088, 1, 1)
test_samples.append((True, name_088, sample_088, ast_088))

name_089 = "sample_089.g"
sample_089 = """\
module A
  a[b]; c[d][e]; f[g[h]];
end
"""
ast_089 = DefModule("A", [
    GetItem(
        GetLocal("a").set_location(name_089, 2, 3),
        GetLocal("b").set_location(name_089, 2, 5)
    ).set_location(name_089, 2, 4),
    GetItem(
        GetItem(
            GetLocal("c").set_location(name_089, 2, 9),
            GetLocal("d").set_location(name_089, 2, 11)
        ).set_location(name_089, 2, 10),
        GetLocal("e").set_location(name_089, 2, 14)
    ).set_location(name_089, 2, 13),
    GetItem(
        GetLocal("f").set_location(name_089, 2, 18),
        GetItem(
            GetLocal("g").set_location(name_089, 2, 20),
            GetLocal("h").set_location(name_089, 2, 22)
        ).set_location(name_089, 2, 21)
    ).set_location(name_089, 2, 19)
]).set_location(name_089, 1, 1)
test_samples.append((True, name_089, sample_089, ast_089))

name_090 = "sample_090.g"
sample_090 = """\
module A
  a:b; c:d:e:f;
end
"""
ast_090 = DefModule("A", [
    GetMember(
        GetLocal("a").set_location(name_090, 2, 3), "b"
    ).set_location(name_090, 2, 4),
    GetMember(
        GetMember(
            GetMember(
                GetLocal("c").set_location(name_090, 2, 8),
                "d"
            ).set_location(name_090, 2, 9),
            "e"
        ).set_location(name_090, 2, 11),
        "f"
    ).set_location(name_090, 2, 13)
]).set_location(name_090, 1, 1)
test_samples.append((True, name_090, sample_090, ast_090))

name_091 = "sample_091.g"
sample_091 = """\
module A
  !
"""
ast_091 = None
test_samples.append((False, name_091, sample_091, ast_091))

name_092 = "sample_092.g"
sample_092 = """\
module A
  a;
end
"""
ast_092 = DefModule("A", [
    GetLocal("a").set_location(name_092, 2, 3)
]).set_location(name_092, 1, 1)
test_samples.append((True, name_092, sample_092, ast_092))

name_093 = "sample_093.g"
sample_093 = """\
module A
  $1;
end
"""
ast_093 = None
test_samples.append((False, name_093, sample_093, ast_093))

name_094 = "sample_094.g"
sample_094 = """\
module A
  $a;
end
"""
ast_094 = DefModule("A", [
    GetLocal("a").set_location(name_094, 2, 4)
]).set_location(name_094, 1, 1)
test_samples.append((True, name_094, sample_094, ast_094))

name_095 = "sample_095.g"
sample_095 = """\
module A
  #1;
end
"""
ast_095 = None
test_samples.append((False, name_095, sample_095, ast_095))

name_096 = "sample_096.g"
sample_096 = """\
module A
  #a;
end
"""
ast_096 = None
test_samples.append((False, name_096, sample_096, ast_096))

name_097 = "sample_097.g"
sample_097 = """\
module A
  $(a = 1);
end
"""
ast_097 = None
test_samples.append((False, name_097, sample_097, ast_097))

name_098 = "sample_098.g"
sample_098 = """\
module A
  $(a); $(a b); $(a `b);
end
"""
ast_098 = DefModule("A", [
    Expand(
        GetLocal("a").set_location(name_098, 2, 5)
    ).set_location(name_098, 2, 3),
    Expand(
        Call(
            GetLocal("a").set_location(name_098, 2, 11),
            GetLocal("b").set_location(name_098, 2, 13)
        ).set_location(name_098, 2, 13)
    ).set_location(name_098, 2, 9),
    Expand(
        GetLocal("a").set_location(name_098, 2, 19),
        GetLocal("b").set_location(name_098, 2, 22)
    ).set_location(name_098, 2, 17)
]).set_location(name_098, 1, 1)
test_samples.append((True, name_098, sample_098, ast_098))

name_099 = "sample_099.g"
sample_099 = """\
module A
  $(a `b = 1);
end
"""
ast_099 = None
test_samples.append((False, name_099, sample_099, ast_099))

name_100 = "sample_100.g"
sample_100 = """\
module A
  1; 1.5; "abc";
end
"""
ast_100 = DefModule("A", [
    Const(1).set_location(name_100, 2, 3),
    Const(1.5).set_location(name_100, 2, 6),
    Const("abc").set_location(name_100, 2, 11)
]).set_location(name_100, 1, 1)
test_samples.append((True, name_100, sample_100, ast_100))

name_101 = "sample_101.g"
sample_101 = """\
module A
  (a);
end
"""
ast_101 = DefModule("A", [
    GetLocal("a").set_location(name_101, 2, 4)
]).set_location(name_101, 1, 1)
test_samples.append((True, name_101, sample_101, ast_101))

name_102 = "sample_102.g"
sample_102 = """\
module A
  (a = 1);
end
"""
ast_102 = None
test_samples.append((False, name_102, sample_102, ast_102))

name_103 = "sample_103.g"
sample_103 = """\
module A
  (a, );
end
"""
ast_103 = None
test_samples.append((False, name_103, sample_103, ast_103))

name_104 = "sample_104.g"
sample_104 = """\
module A
  (a, b = 2);
end
"""
ast_104 = None
test_samples.append((False, name_104, sample_104, ast_104))

name_105 = "sample_105.g"
sample_105 = """\
module A
  (1, 2);
end
"""
ast_105 = DefModule("A", [
    NewPair(
        Const(1).set_location(name_105, 2, 4),
        Const(2).set_location(name_105, 2, 7)
    ).set_location(name_105, 2, 3)
]).set_location(name_105, 1, 1)
test_samples.append((True, name_105, sample_105, ast_105))

name_106 = "sample_106.g"
sample_106 = """\
module A
  (a, b, c);
end
"""
ast_106 = None
test_samples.append((False, name_106, sample_106, ast_106))

name_107 = "sample_107.g"
sample_107 = """\
module A
  [];
end
"""
ast_107 = DefModule("A", [
    NewList(
    ).set_location(name_107, 2, 3)
]).set_location(name_107, 1, 1)
test_samples.append((True, name_107, sample_107, ast_107))

name_108 = "sample_108.g"
sample_108 = """\
module A
  [
end
"""
ast_108 = None
test_samples.append((False, name_108, sample_108, ast_108))

name_109 = "sample_109.g"
sample_109 = """\
module A
  [1];
end
"""
ast_109 = DefModule("A", [
    NewList(
        Const(1).set_location(name_109, 2, 4)
    ).set_location(name_109, 2, 3)
]).set_location(name_109, 1, 1)
test_samples.append((True, name_109, sample_109, ast_109))

name_110 = "sample_110.g"
sample_110 = """\
module A
  [1
end
"""
ast_110 = None
test_samples.append((False, name_110, sample_110, ast_110))

name_111 = "sample_111.g"
sample_111 = """\
module A
  [a = 1];
end
"""
ast_111 = None
test_samples.append((False, name_111, sample_111, ast_111))

name_112 = "sample_112.g"
sample_112 = """\
module A
  [1, 2];
end
"""
ast_112 = DefModule("A", [
    NewList(
        Const(1).set_location(name_112, 2, 4),
        Const(2).set_location(name_112, 2, 7)
    ).set_location(name_112, 2, 3)
]).set_location(name_112, 1, 1)
test_samples.append((True, name_112, sample_112, ast_112))

name_113 = "sample_113.g"
sample_113 = """\
module A
  [1, 2, 3];
end
"""
ast_113 = DefModule("A", [
    NewList(
        Const(1).set_location(name_113, 2, 4),
        Const(2).set_location(name_113, 2, 7),
        Const(3).set_location(name_113, 2, 10)
    ).set_location(name_113, 2, 3)
]).set_location(name_113, 1, 1)
test_samples.append((True, name_113, sample_113, ast_113))

name_114 = "sample_114.g"
sample_114 = """\
module A
  [a,];
end
"""
ast_114 = None
test_samples.append((False, name_114, sample_114, ast_114))

name_115 = "sample_115.g"
sample_115 = """\
module A
  [a, b => c];
end
"""
ast_115 = None
test_samples.append((False, name_115, sample_115, ast_115))

name_116 = "sample_116.g"
sample_116 = """\
module A
  [a => ];
end
"""
ast_116 = None
test_samples.append((False, name_116, sample_116, ast_116))

name_117 = "sample_117.g"
sample_117 = """\
module A
  [1 => 2, 3];
end
"""
ast_117 = None
test_samples.append((False, name_117, sample_117, ast_117))

name_118 = "sample_118.g"
sample_118 = """\
module A
  [1 => 2];
  [3 => 4, 5 => 6];
  ["a" => "b", "c" => "d", "e" => "f"];
end
"""
ast_118 = DefModule("A", [
    NewHashMap(
        (
            Const(1).set_location(name_118, 2, 4),
            Const(2).set_location(name_118, 2, 9)
        )
    ).set_location(name_118, 2, 3),
    NewHashMap(
        (
            Const(3).set_location(name_118, 3, 4),
            Const(4).set_location(name_118, 3, 9)
        ),
        (
            Const(5).set_location(name_118, 3, 12),
            Const(6).set_location(name_118, 3, 17)
        )
    ).set_location(name_118, 3, 3),
    NewHashMap(
        (
            Const("a").set_location(name_118, 4, 4),
            Const("b").set_location(name_118, 4, 11)
        ),
        (
            Const("c").set_location(name_118, 4, 16),
            Const("d").set_location(name_118, 4, 23)
        ),
        (
            Const("e").set_location(name_118, 4, 28),
            Const("f").set_location(name_118, 4, 35)
        )
    ).set_location(name_118, 4, 3)
]).set_location(name_118, 1, 1)
test_samples.append((True, name_118, sample_118, ast_118))

name_119 = "sample_119.g"
sample_119 = """\
module A
  ({
end
"""
ast_119 = None
test_samples.append((False, name_119, sample_119, ast_119))

name_120 = "sample_120.g"
sample_120 = """\
module A
  ({|
end
"""
ast_120 = None
test_samples.append((False, name_120, sample_120, ast_120))

name_121 = "sample_121.g"
sample_121 = """\
module A
  ({|x
end
"""
ast_121 = None
test_samples.append((False, name_121, sample_121, ast_121))

name_122 = "sample_122.g"
sample_122 = """\
module A
  ({|x y
end
"""
ast_122 = None
test_samples.append((False, name_122, sample_122, ast_122))

name_123 = "sample_123.g"
sample_123 = """\
module A
  ({|x y ...
end
"""
ast_123 = None
test_samples.append((False, name_123, sample_123, ast_123))

name_124 = "sample_124.g"
sample_124 = """\
module A
  ({|x y ...z
end
"""
ast_124 = None
test_samples.append((False, name_124, sample_124, ast_124))

name_125 = "sample_125.g"
sample_125 = """\
module A
  ({|x ...
end
"""
ast_125 = None
test_samples.append((False, name_125, sample_125, ast_125))

name_126 = "sample_126.g"
sample_126 = """\
module A
  ({|x ...y
end
"""
ast_126 = None
test_samples.append((False, name_126, sample_126, ast_126))

name_127 = "sample_127.g"
sample_127 = """\
module A
  ({|...
end
"""
ast_127 = None
test_samples.append((False, name_127, sample_127, ast_127))

name_128 = "sample_128.g"
sample_128 = """\
module A
  ({|...x
end
"""
ast_128 = None
test_samples.append((False, name_128, sample_128, ast_128))

name_129 = "sample_129.g"
sample_129 = """\
module A
  ({|x ...y|
end
"""
ast_129 = None
test_samples.append((False, name_129, sample_129, ast_129))

name_130 = "sample_130.g"
sample_130 = """\
module A
  ({|x ...y| a = 2;});
end
"""
ast_130 = DefModule("A", [
    Lambda(
        ["x", "y"], True, [
            SetLocal(
                "a",
                Const(2).set_location(name_130, 2, 18)
            ).set_location(name_130, 2, 16)
        ], ["a"]
    ).set_location(name_130, 2, 4)
]).set_location(name_130, 1, 1)
test_samples.append((True, name_130, sample_130, ast_130))

name_131 = "sample_131.g"
sample_131 = """\
module A
  {a = 1;}
end
"""
ast_131 = DefModule("A", [
    Block(
        SetLocal(
            "a",
            Const(1).set_location(name_131, 2, 8)
        ).set_location(name_131, 2, 6)
    ).set_location(name_131, 2, 3)
]).set_location(name_131, 1, 1)
test_samples.append((True, name_131, sample_131, ast_131))

name_132 = "sample_132.g"
sample_132 = """\
module A
  {
"""
ast_132 = None
test_samples.append((False, name_132, sample_132, ast_132))

def sl_(n, f, l, c):
    n.deferred.append(SetLocation(f, l, c))
    return n
#-def

name_133 = "sample_133.g"
sample_133 = """\
module A
  defmacro mac x y (#x + #y;)
end
"""
ast_133 = DefModule("A", [
    DefMacro("mac", ["x", "y"], [
        sl_(MacroNode(Add,
            sl_(MacroNodeParam("x"), name_133, 2, 21),
            sl_(MacroNodeParam("y"), name_133, 2, 35)
        ), name_133, 2, 24)
    ]).set_location(name_133, 2, 3)
]).set_location(name_133, 1, 1)
test_samples.append((True, name_133, sample_133, ast_133))

name_134 = "sample_134.g"
sample_134 = """\
module A
  define f {
  }
end
"""
ast_134 = DefModule("A", [
    Define("f", [], [], False, []).set_location(name_134, 2, 3)
]).set_location(name_134, 1, 1)
test_samples.append((True, name_134, sample_134, ast_134))

name_135 = "sample_135.g"
sample_135 = """\
module A
  define f {
    defmacro m ()
  }
end
"""
ast_135 = None
test_samples.append((False, name_135, sample_135, ast_135))

name_136 = "sample_136.g"
sample_136 = """\
module A
  defmacro m1 (
    defmacro m2 ()
  )
end
"""
ast_136 = None
test_samples.append((False, name_136, sample_136, ast_136))

name_137 = "sample_137.g"
sample_137 = """\
module A
  defmacro m1 ()
  define f {}
  defmacro m2 ()
  define g {}
end
"""
ast_137 = DefModule("A", [
    DefMacro("m1", [], []).set_location(name_137, 2, 3),
    Define("f", [], [], False, []).set_location(name_137, 3, 3),
    DefMacro("m2", [], []).set_location(name_137, 4, 3),
    Define("g", [], [], False, []).set_location(name_137, 5, 3)
]).set_location(name_137, 1, 1)
test_samples.append((True, name_137, sample_137, ast_137))

name_138 = "sample_138.g"
sample_138 = """\
module A
  define f {}
  defmacro m1 ()
  define g {}
  defmacro m2 ()
end
"""
ast_138 = DefModule("A", [
    Define("f", [], [], False, []).set_location(name_138, 2, 3),
    DefMacro("m1", [], []).set_location(name_138, 3, 3),
    Define("g", [], [], False, []).set_location(name_138, 4, 3),
    DefMacro("m2", [], []).set_location(name_138, 5, 3)
]).set_location(name_138, 1, 1)
test_samples.append((True, name_138, sample_138, ast_138))

name_139 = "sample_139.g"
sample_139 = """\
module A
  defmacro m (
    define f {}
  )
end
"""
ast_139 = None
test_samples.append((False, name_139, sample_139, ast_139))

name_140 = "sample_140.g"
sample_140 = """\
module A
  define f x y ...z {
    t = x + y;
    {
      u = a + b;
    }
  }
end
"""
ast_140 = DefModule("A", [
    Define("f", ["t"], ["x", "y", "z"], True, [
        SetLocal(
            "t",
            Add(
                GetLocal("x").set_location(name_140, 3, 9),
                GetLocal("y").set_location(name_140, 3, 13)
            ).set_location(name_140, 3, 11)
        ).set_location(name_140, 3, 7),
        Block(
            SetLocal(
                "u",
                Add(
                    GetLocal("a").set_location(name_140, 5, 11),
                    GetLocal("b").set_location(name_140, 5, 15)
                ).set_location(name_140, 5, 13)
            ).set_location(name_140, 5, 9)
        ).set_location(name_140, 4, 5)
    ]).set_location(name_140, 2, 3)
]).set_location(name_140, 1, 1)
test_samples.append((True, name_140, sample_140, ast_140))

name_141 = "sample_141.g"
sample_141 = """\
module A            -- 1
  define f x y z {  -- 2
    if (x > y) {    -- 3
      t = z;        -- 4
    }               -- 5
    {               -- 6
      if (x > y) {  -- 7
        u = z;      -- 8
      }             -- 9
    }               -- 10
    if !z {         -- 11
      a = 1;        -- 12
    }               -- 13
    else {          -- 14
      b = 1;        -- 15
    }               -- 16
    if 1 {          -- 17
      a = 1;        -- 18
    }               -- 19
    elif 2 {        -- 20
      b = 2;        -- 21
    }               -- 22
  }                 -- 23
end                 -- 24
"""
ast_141 = DefModule("A", [
    Define("f", ["t", "a", "b"], ["x", "y", "z"], False, [
        If(
            Gt(
                GetLocal("x").set_location(name_141, 3, 9),
                GetLocal("y").set_location(name_141, 3, 13)
            ).set_location(name_141, 3, 11),
            [
                SetLocal(
                    "t",
                    GetLocal("z").set_location(name_141, 4, 11)
                ).set_location(name_141, 4, 9)
            ],
            []
        ).set_location(name_141, 3, 5),

        Block(
            If(
                Gt(
                    GetLocal("x").set_location(name_141, 7, 11),
                    GetLocal("y").set_location(name_141, 7, 15)
                ).set_location(name_141, 7, 13),
                [
                    SetLocal(
                        "u",
                        GetLocal("z").set_location(name_141, 8, 13)
                    ).set_location(name_141, 8, 11)
                ],
                []
            ).set_location(name_141, 7, 7)
        ).set_location(name_141, 6, 5),

        If(
            Not(
                GetLocal("z").set_location(name_141, 11, 9)
            ).set_location(name_141, 11, 8),
            [
                SetLocal(
                    "a",
                    Const(1).set_location(name_141, 12, 11)
                ).set_location(name_141, 12, 9)
            ],
            [
                SetLocal(
                    "b",
                    Const(1).set_location(name_141, 15, 11)
                ).set_location(name_141, 15, 9)
            ]
        ).set_location(name_141, 11, 5),

        If(
            Const(1).set_location(name_141, 17, 8),
            [
                SetLocal(
                    "a",
                    Const(1).set_location(name_141, 18, 11)
                ).set_location(name_141, 18, 9)
            ],
            [
                If(
                    Const(2).set_location(name_141, 20, 10),
                    [
                        SetLocal(
                            "b",
                            Const(2).set_location(name_141, 21, 11)
                        ).set_location(name_141, 21, 9)
                    ],
                    []
                ).set_location(name_141, 20, 5)
            ]
        ).set_location(name_141, 17, 5)
    ]).set_location(name_141, 2, 3)
]).set_location(name_141, 1, 1)
test_samples.append((True, name_141, sample_141, ast_141))

name_142 = "sample_142.g"
sample_142 = """\
module A
  if 1 {1;}
  elif 2 {2;}
  else {0;}
end
"""
ast_142 = DefModule("A", [
    If(
        Const(1).set_location(name_142, 2, 6),
        [Const(1).set_location(name_142, 2, 9)],
        [
            If(
                Const(2).set_location(name_142, 3, 8),
                [Const(2).set_location(name_142, 3, 11)],
                [Const(0).set_location(name_142, 4, 9)]
            ).set_location(name_142, 3, 3)
        ]
    ).set_location(name_142, 2, 3)
]).set_location(name_142, 1, 1)
test_samples.append((True, name_142, sample_142, ast_142))

name_143 = "sample_143.g"
sample_143 = """\
module A
  if 1 {1;}
  elif 2 {2;}
  elif 3 {3;}
end
"""
ast_143 = DefModule("A", [
    If(
        Const(1).set_location(name_143, 2, 6),
        [Const(1).set_location(name_143, 2, 9)],
        [
            If(
                Const(2).set_location(name_143, 3, 8),
                [Const(2).set_location(name_143, 3, 11)],
                [
                    If(
                        Const(3).set_location(name_143, 4, 8),
                        [Const(3).set_location(name_143, 4, 11)],
                        []
                    ).set_location(name_143, 4, 3)
                ]
            ).set_location(name_143, 3, 3)
        ]
    ).set_location(name_143, 2, 3)
]).set_location(name_143, 1, 1)
test_samples.append((True, name_143, sample_143, ast_143))

name_144 = "sample_144.g"
sample_144 = """\
module A
  if 1 {1;}
  elif 2 {2;}
  elif 3 {3;}
  else {0;}
end
"""
ast_144 = DefModule("A", [
    If(
        Const(1).set_location(name_144, 2, 6),
        [Const(1).set_location(name_144, 2, 9)],
        [
            If(
                Const(2).set_location(name_144, 3, 8),
                [Const(2).set_location(name_144, 3, 11)],
                [
                    If(
                        Const(3).set_location(name_144, 4, 8),
                        [Const(3).set_location(name_144, 4, 11)],
                        [Const(0).set_location(name_144, 5, 9)]
                    ).set_location(name_144, 4, 3)
                ]
            ).set_location(name_144, 3, 3)
        ]
    ).set_location(name_144, 2, 3)
]).set_location(name_144, 1, 1)
test_samples.append((True, name_144, sample_144, ast_144))

name_145 = "sample_145.g"
sample_145 = """\
module A
  if 1 {1;}
  elif 2 {2;}
  elif 3 {3;}
  elif 4 {4;}
  else {0;}
end
"""
ast_145 = DefModule("A", [
    If(
        Const(1).set_location(name_145, 2, 6),
        [Const(1).set_location(name_145, 2, 9)],
        [
            If(
                Const(2).set_location(name_145, 3, 8),
                [Const(2).set_location(name_145, 3, 11)],
                [
                    If(
                        Const(3).set_location(name_145, 4, 8),
                        [Const(3).set_location(name_145, 4, 11)],
                        [
                            If(
                                Const(4).set_location(name_145, 5, 8),
                                [Const(4).set_location(name_145, 5, 11)],
                                [Const(0).set_location(name_145, 6, 9)]
                            ).set_location(name_145, 5, 3)
                        ]
                    ).set_location(name_145, 4, 3)
                ]
            ).set_location(name_145, 3, 3)
        ]
    ).set_location(name_145, 2, 3)
]).set_location(name_145, 1, 1)
test_samples.append((True, name_145, sample_145, ast_145))

name_146 = "sample_146.g"
sample_146 = """\
module A
  define f ...args {
    foreach x args {
      u = x;
    }
    while 0 {
      v = 1;
    }
    do {
      w = 0;
    } while 1;
    break; continue;
    return;
    return 1;
  }
end
"""
ast_146 = DefModule("A", [
    Define("f", ["x", "u", "v", "w"], ["args"], True, [
        Foreach(
            "x",
            GetLocal("args").set_location(name_146, 3, 15),
            [
                SetLocal(
                    "u",
                    GetLocal("x").set_location(name_146, 4, 11)
                ).set_location(name_146, 4, 9)
            ]
        ).set_location(name_146, 3, 5),
        While(
            Const(0).set_location(name_146, 6, 11),
            [
                SetLocal(
                    "v",
                    Const(1).set_location(name_146, 7, 11)
                ).set_location(name_146, 7, 9)
            ]
        ).set_location(name_146, 6, 5),
        DoWhile(
            [
                SetLocal(
                    "w",
                    Const(0).set_location(name_146, 10, 11)
                ).set_location(name_146, 10, 9)
            ],
            Const(1).set_location(name_146, 11, 13)
        ).set_location(name_146, 9, 5),
        Break().set_location(name_146, 12, 5),
        Continue().set_location(name_146, 12, 12),
        Return().set_location(name_146, 13, 5),
        Return(
            Const(1).set_location(name_146, 14, 12)
        ).set_location(name_146, 14, 5)
    ]).set_location(name_146, 2, 3),
]).set_location(name_146, 1, 1)
test_samples.append((True, name_146, sample_146, ast_146))

name_147 = "sample_147.g"
sample_147 = """\
module A
  define f {
    try {
    }
  }
end
"""
ast_147 = DefModule("A", [
    Define("f", [], [], False, [
        TryCatchFinally(
            [], [], []
        ).set_location(name_147, 3, 5)
    ]).set_location(name_147, 2, 3)
]).set_location(name_147, 1, 1)
test_samples.append((True, name_147, sample_147, ast_147))

name_148 = "sample_148.g"
sample_148 = """\
module A
  define f {
    try {
      a = 1;
    }
    catch Error {
      b = 1;
    }
  }
end
"""
ast_148 = DefModule("A", [
    Define("f", ["a", "b"], [], False, [
        TryCatchFinally(
            [
                SetLocal(
                    "a",
                    Const(1).set_location(name_148, 4, 11)
                ).set_location(name_148, 4, 9)
            ],
            [
                ("Error", None, [
                    SetLocal(
                        "b",
                        Const(1).set_location(name_148, 7, 11)
                    ).set_location(name_148, 7, 9)
                ])
            ],
            []
        ).set_location(name_148, 3, 5)
    ]).set_location(name_148, 2, 3)
]).set_location(name_148, 1, 1)
test_samples.append((True, name_148, sample_148, ast_148))

name_149 = "sample_149.g"
sample_149 = """\
module A
  define f {
    try {
      a = 1;
    }
    catch Error e {
      b = 1;
    }
  }
end
"""
ast_149 = DefModule("A", [
    Define("f", ["a", "e", "b"], [], False, [
        TryCatchFinally(
            [
                SetLocal(
                    "a",
                    Const(1).set_location(name_149, 4, 11)
                ).set_location(name_149, 4, 9)
            ],
            [
                ("Error", "e", [
                    SetLocal(
                        "b",
                        Const(1).set_location(name_149, 7, 11)
                    ).set_location(name_149, 7, 9)
                ])
            ],
            []
        ).set_location(name_149, 3, 5)
    ]).set_location(name_149, 2, 3)
]).set_location(name_149, 1, 1)
test_samples.append((True, name_149, sample_149, ast_149))

name_150 = "sample_150.g"
sample_150 = """\
module A
  define f {
    try {
      a = 1;
    }
    finally {
      b = 1;
    }
  }
end
"""
ast_150 = DefModule("A", [
    Define("f", ["a", "b"], [], False, [
        TryCatchFinally(
            [
                SetLocal(
                    "a",
                    Const(1).set_location(name_150, 4, 11)
                ).set_location(name_150, 4, 9)
            ],
            [],
            [
                SetLocal(
                    "b",
                    Const(1).set_location(name_150, 7, 11)
                ).set_location(name_150, 7, 9)
            ]
        ).set_location(name_150, 3, 5)
    ]).set_location(name_150, 2, 3)
]).set_location(name_150, 1, 1)
test_samples.append((True, name_150, sample_150, ast_150))

name_151 = "sample_151.g"
sample_151 = """\
module A
  define f {
    try {
      a = 1;
    }
    catch Error {
      b = 1;
    }
    catch Error e {
      c = 1;
    }
    catch Error e {
      d = 1;
    }
    finally {
      e = 1;
    }
  }
end
"""
ast_151 = DefModule("A", [
    Define("f", ["a", "b", "e", "c", "d"], [], False, [
        TryCatchFinally(
            [
                SetLocal(
                    "a",
                    Const(1).set_location(name_151, 4, 11)
                ).set_location(name_151, 4, 9)
            ],
            [
                ("Error", None, [
                    SetLocal(
                        "b",
                        Const(1).set_location(name_151, 7, 11)
                    ).set_location(name_151, 7, 9)
                ]),
                ("Error", "e", [
                    SetLocal(
                        "c",
                        Const(1).set_location(name_151, 10, 11)
                    ).set_location(name_151, 10, 9)
                ]),
                ("Error", "e", [
                    SetLocal(
                        "d",
                        Const(1).set_location(name_151, 13, 11)
                    ).set_location(name_151, 13, 9)
                ])
            ],
            [
                SetLocal(
                    "e",
                    Const(1).set_location(name_151, 16, 11)
                ).set_location(name_151, 16, 9)
            ]
        ).set_location(name_151, 3, 5)
    ]).set_location(name_151, 2, 3)
]).set_location(name_151, 1, 1)
test_samples.append((True, name_151, sample_151, ast_151))

name_152 = "sample_152.g"
sample_152 = """\
module A
  throw e;
  throw Error, "Operation fails";
end
"""
ast_152 = DefModule("A", [
    Rethrow(
        GetLocal("e").set_location(name_152, 2, 9)
    ).set_location(name_152, 2, 3),
    Throw(
        GetLocal("Error").set_location(name_152, 3, 9),
        Const("Operation fails").set_location(name_152, 3, 16)
    ).set_location(name_152, 3, 3)
]).set_location(name_152, 1, 1)
test_samples.append((True, name_152, sample_152, ast_152))

name_153 = "sample_153.g"
sample_153 = """\
module A
  defmacro m (-1;)
end
"""
ast_153 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(Neg,
            sl_(MacroNode(Const,
                MacroNodeAtom(1)
            ), name_153, 2, 16)
        ), name_153, 2, 15)
    ]).set_location(name_153, 2, 3)
]).set_location(name_153, 1, 1)
test_samples.append((True, name_153, sample_153, ast_153))

name_154 = "sample_154.g"
sample_154 = """\
module A
  defmacro m (a[0];)
end
"""
ast_154 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(GetItem,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("a")
            ), name_154, 2, 15),
            sl_(MacroNode(Const,
                MacroNodeAtom(0)
            ), name_154, 2, 17)
        ), name_154, 2, 16)
    ]).set_location(name_154, 2, 3)
]).set_location(name_154, 1, 1)
test_samples.append((True, name_154, sample_154, ast_154))

name_155 = "sample_155.g"
sample_155 = """\
module A
  defmacro m (a:b;)
end
"""
ast_155 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(GetMember,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("a")
            ), name_155, 2, 15),
            MacroNodeAtom("b")
        ), name_155, 2, 16)
    ]).set_location(name_155, 2, 3)
]).set_location(name_155, 1, 1)
test_samples.append((True, name_155, sample_155, ast_155))

name_156 = "sample_156.g"
sample_156 = """\
module A
  defmacro m (x = y;)
end
"""
ast_156 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(SetLocal,
            MacroNodeAtom("x"),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("y")
            ), name_156, 2, 19)
        ), name_156, 2, 17)
    ]).set_location(name_156, 2, 3)
]).set_location(name_156, 1, 1)
test_samples.append((True, name_156, sample_156, ast_156))

name_157 = "sample_157.g"
sample_157 = """\
module A
  defmacro m (x += y;)
end
"""
ast_157 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(SetLocal,
            MacroNodeAtom("x"),
            sl_(MacroNode(Add,
                sl_(MacroNode(GetLocal,
                    MacroNodeAtom("x")
                ), name_157, 2, 15),
                sl_(MacroNode(GetLocal,
                    MacroNodeAtom("y")
                ), name_157, 2, 20)
            ), name_157, 2, 17)
        ), name_157, 2, 17)
    ]).set_location(name_157, 2, 3)
]).set_location(name_157, 1, 1)
test_samples.append((True, name_157, sample_157, ast_157))

name_158 = "sample_158.g"
sample_158 = """\
module A
  defmacro m (x[y] = z;)
  x[y] = z;
end
"""
ast_158 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(SetItem,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("x")
            ), name_158, 2, 15),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("y")
            ), name_158, 2, 17),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("z")
            ), name_158, 2, 22)
        ), name_158, 2, 20)
    ]).set_location(name_158, 2, 3),
    SetItem(
        GetLocal("x").set_location(name_158, 3, 3),
        GetLocal("y").set_location(name_158, 3, 5),
        GetLocal("z").set_location(name_158, 3, 10)
    ).set_location(name_158, 3, 8)
]).set_location(name_158, 1, 1)
test_samples.append((True, name_158, sample_158, ast_158))

name_159 = "sample_159.g"
sample_159 = """\
module A
  defmacro m (x[y] += z;)
  x[y] += z;
end
"""
ast_159 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(SetItem,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("x")
            ), name_159, 2, 15),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("y")
            ), name_159, 2, 17),
            sl_(MacroNode(Add,
                sl_(MacroNode(GetItem,
                    sl_(MacroNode(GetLocal,
                        MacroNodeAtom("x")
                    ), name_159, 2, 15),
                    sl_(MacroNode(GetLocal,
                        MacroNodeAtom("y")
                    ), name_159, 2, 17)
                ), name_159, 2, 16),
                sl_(MacroNode(GetLocal,
                    MacroNodeAtom("z")
                ), name_159, 2, 23)
            ), name_159, 2, 20)
        ), name_159, 2, 20)
    ]).set_location(name_159, 2, 3),
    SetItem(
        GetLocal("x").set_location(name_159, 3, 3),
        GetLocal("y").set_location(name_159, 3, 5),
        Add(
            GetItem(
                GetLocal("x").set_location(name_159, 3, 3),
                GetLocal("y").set_location(name_159, 3, 5)
            ).set_location(name_159, 3, 4),
            GetLocal("z").set_location(name_159, 3, 11)
        ).set_location(name_159, 3, 8)
    ).set_location(name_159, 3, 8)
]).set_location(name_159, 1, 1)
test_samples.append((True, name_159, sample_159, ast_159))

name_160 = "sample_160.g"
sample_160 = """\
module A
  defmacro m (x:y = z;)
  x:y = z;
end
"""
ast_160 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(SetMember,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("x")
            ), name_160, 2, 15),
            MacroNodeAtom("y"),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("z")
            ), name_160, 2, 21)
        ), name_160, 2, 19)
    ]).set_location(name_160, 2, 3),
    SetMember(
        GetLocal("x").set_location(name_160, 3, 3),
        "y",
        GetLocal("z").set_location(name_160, 3, 9)
    ).set_location(name_160, 3, 7)
]).set_location(name_160, 1, 1)
test_samples.append((True, name_160, sample_160, ast_160))

name_161 = "sample_161.g"
sample_161 = """\
module A
  defmacro m (x:y += z;)
  x:y += z;
end
"""
ast_161 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(SetMember,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("x")
            ), name_161, 2, 15),
            MacroNodeAtom("y"),
            sl_(MacroNode(Add,
                sl_(MacroNode(GetMember,
                    sl_(MacroNode(GetLocal,
                        MacroNodeAtom("x")
                    ), name_161, 2, 15),
                    MacroNodeAtom("y")
                ), name_161, 2, 16),
                sl_(MacroNode(GetLocal,
                    MacroNodeAtom("z")
                ), name_161, 2, 22)
            ), name_161, 2, 19)
        ), name_161, 2, 19)
    ]).set_location(name_161, 2, 3),
    SetMember(
        GetLocal("x").set_location(name_161, 3, 3),
        "y",
        Add(
            GetMember(
                GetLocal("x").set_location(name_161, 3, 3),
                "y"
            ).set_location(name_161, 3, 4),
            GetLocal("z").set_location(name_161, 3, 10)
        ).set_location(name_161, 3, 7)
    ).set_location(name_161, 3, 7)
]).set_location(name_161, 1, 1)
test_samples.append((True, name_161, sample_161, ast_161))

name_162 = "sample_162.g"
sample_162 = """\
module A
  1 = 2;
end
"""
ast_162 = None
test_samples.append((False, name_162, sample_162, ast_162))

name_163 = "sample_163.g"
sample_163 = """\
module A
  defmacro m (f a b $c;)
end
"""
ast_163 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(Call,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("f")
            ), name_163, 2, 15),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("a")
            ), name_163, 2, 17),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("b")
            ), name_163, 2, 19),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("c")
            ), name_163, 2, 22)
        ), name_163, 2, 17)
    ]).set_location(name_163, 2, 3)
]).set_location(name_163, 1, 1)
test_samples.append((True, name_163, sample_163, ast_163))

name_164 = "sample_164.g"
sample_164 = """\
module A
  defmacro m ($(m `a `b);)
end
"""
ast_164 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(Expand,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("m")
            ), name_164, 2, 17),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("a")
            ), name_164, 2, 20),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("b")
            ), name_164, 2, 23)
        ), name_164, 2, 15)
    ]).set_location(name_164, 2, 3)
]).set_location(name_164, 1, 1)
test_samples.append((True, name_164, sample_164, ast_164))

name_165 = "sample_165.g"
sample_165 = """\
module A
  defmacro m ((1, 2);)
end
"""
ast_165 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(NewPair,
            sl_(MacroNode(Const,
                MacroNodeAtom(1)
            ), name_165, 2, 16),
            sl_(MacroNode(Const,
                MacroNodeAtom(2)
            ), name_165, 2, 19)
        ), name_165, 2, 15)
    ]).set_location(name_165, 2, 3)
]).set_location(name_165, 1, 1)
test_samples.append((True, name_165, sample_165, ast_165))

name_166 = "sample_166.g"
sample_166 = """\
module A
  defmacro m ([1, 2];)
end
"""
ast_166 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(NewList,
            sl_(MacroNode(Const,
                MacroNodeAtom(1)
            ), name_166, 2, 16),
            sl_(MacroNode(Const,
                MacroNodeAtom(2)
            ), name_166, 2, 19)
        ), name_166, 2, 15)
    ]).set_location(name_166, 2, 3)
]).set_location(name_166, 1, 1)
test_samples.append((True, name_166, sample_166, ast_166))

name_167 = "sample_167.g"
sample_167 = """\
module A
  defmacro m ([1 => 2];)
end
"""
ast_167 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(NewHashMap,
            sl_(MacroNode(NewPair,
                sl_(MacroNode(Const,
                    MacroNodeAtom(1)
                ), name_167, 2, 16),
                sl_(MacroNode(Const,
                    MacroNodeAtom(2)
                ), name_167, 2, 21)
            ), name_167, 2, 16)
        ), name_167, 2, 15)
    ]).set_location(name_167, 2, 3)
]).set_location(name_167, 1, 1)
test_samples.append((True, name_167, sample_167, ast_167))

name_168 = "sample_168.g"
sample_168 = """\
module A
  defmacro m (({|x y ...z| t = 1; x = 2;});)
end
"""
ast_168 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(Lambda,
            MacroNodeAtom(["x", "y", "z"]),
            MacroNodeAtom(True),
            MacroNodeSequence(
                sl_(MacroNode(SetLocal,
                    MacroNodeAtom("t"),
                    sl_(MacroNode(Const,
                        MacroNodeAtom(1)
                    ), name_168, 2, 32)
                ), name_168, 2, 30),
                sl_(MacroNode(SetLocal,
                    MacroNodeAtom("x"),
                    sl_(MacroNode(Const,
                        MacroNodeAtom(2)
                    ), name_168, 2, 39)
                ), name_168, 2, 37)
            ),
            MacroNodeAtom(["t"])
        ), name_168, 2, 16)
    ]).set_location(name_168, 2, 3)
]).set_location(name_168, 1, 1)
test_samples.append((True, name_168, sample_168, ast_168))

name_169 = "sample_169.g"
sample_169 = """\
module A
  defmacro m ({1; 2; 3;})
end
"""
ast_169 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(Block,
            sl_(MacroNode(Const,
                MacroNodeAtom(1)
            ), name_169, 2, 16),
            sl_(MacroNode(Const,
                MacroNodeAtom(2)
            ), name_169, 2, 19),
            sl_(MacroNode(Const,
                MacroNodeAtom(3)
            ), name_169, 2, 22)
        ), name_169, 2, 15)
    ]).set_location(name_169, 2, 3)
]).set_location(name_169, 1, 1)
test_samples.append((True, name_169, sample_169, ast_169))

name_170 = "sample_170.g"
sample_170 = """\
module A
  defmacro m (
    if 1 {1;}
    elif 2 {2;}
    else {3;}
  )
end
"""
ast_170 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(If,
            sl_(MacroNode(Const,
                MacroNodeAtom(1)
            ), name_170, 3, 8),
            MacroNodeSequence(
                sl_(MacroNode(Const,
                    MacroNodeAtom(1)
                ), name_170, 3, 11)
            ),
            MacroNodeSequence(
                sl_(MacroNode(If,
                    sl_(MacroNode(Const,
                        MacroNodeAtom(2)
                    ), name_170, 4, 10),
                    MacroNodeSequence(
                        sl_(MacroNode(Const,
                            MacroNodeAtom(2)
                        ), name_170, 4, 13)
                    ),
                    MacroNodeSequence(
                        sl_(MacroNode(Const,
                            MacroNodeAtom(3)
                        ), name_170, 5, 11)
                    )
                ), name_170, 4, 5)
            )
        ), name_170, 3, 5)
    ]).set_location(name_170, 2, 3)
]).set_location(name_170, 1, 1)
test_samples.append((True, name_170, sample_170, ast_170))

name_171 = "sample_171.g"
sample_171 = """\
module A
  defmacro m (foreach i x {1;})
end
"""
ast_171 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(Foreach,
            MacroNodeAtom("i"),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("x")
            ), name_171, 2, 25),
            MacroNodeSequence(
                sl_(MacroNode(Const,
                    MacroNodeAtom(1)
                ), name_171, 2, 28)
            )
        ), name_171, 2, 15)
    ]).set_location(name_171, 2, 3)
]).set_location(name_171, 1, 1)
test_samples.append((True, name_171, sample_171, ast_171))

name_172 = "sample_172.g"
sample_172 = """\
module A
  defmacro m (while x {y;})
end
"""
ast_172 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(While,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("x")
            ), name_172, 2, 21),
            MacroNodeSequence(
                sl_(MacroNode(GetLocal,
                    MacroNodeAtom("y")
                ), name_172, 2, 24)
            )
        ), name_172, 2, 15)
    ]).set_location(name_172, 2, 3)
]).set_location(name_172, 1, 1)
test_samples.append((True, name_172, sample_172, ast_172))

name_173 = "sample_173.g"
sample_173 = """\
module A
  defmacro m (do {x;} while y;)
end
"""
ast_173 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(DoWhile,
            MacroNodeSequence(
                sl_(MacroNode(GetLocal,
                    MacroNodeAtom("x")
                ), name_173, 2, 19)
            ),
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("y")
            ), name_173, 2, 29)
        ), name_173, 2, 15)
    ]).set_location(name_173, 2, 3)
]).set_location(name_173, 1, 1)
test_samples.append((True, name_173, sample_173, ast_173))

name_174 = "sample_174.g"
sample_174 = """\
module A
  defmacro m (break; continue; return; return 0;)
end
"""
ast_174 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(Break), name_174, 2, 15),
        sl_(MacroNode(Continue), name_174, 2, 22),
        sl_(MacroNode(Return), name_174, 2, 32),
        sl_(MacroNode(Return,
            sl_(MacroNode(Const,
                MacroNodeAtom(0)
            ), name_174, 2, 47)
        ), name_174, 2, 40)
    ]).set_location(name_174, 2, 3)
]).set_location(name_174, 1, 1)
test_samples.append((True, name_174, sample_174, ast_174))

name_175 = "sample_175.g"
sample_175 = """\
module A
  defmacro m (
    try {
      1;
    }
    catch Error e {
      e;
    }
    finally {
      0;
    }
  )
end
"""
ast_175 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(TryCatchFinally,
            MacroNodeSequence(
                sl_(MacroNode(Const,
                    MacroNodeAtom(1)
                ), name_175, 4, 7)
            ),
            MacroNodeSequence(
                MacroNodeSequence(
                    MacroNodeAtom("Error"),
                    MacroNodeAtom("e"),
                    MacroNodeSequence(
                        sl_(MacroNode(GetLocal,
                            MacroNodeAtom("e")
                        ), name_175, 7, 7)
                    )
                )
            ),
            MacroNodeSequence(
                sl_(MacroNode(Const,
                    MacroNodeAtom(0)
                ), name_175, 10, 7)
            )
        ), name_175, 3, 5)
    ]).set_location(name_175, 2, 3)
]).set_location(name_175, 1, 1)
test_samples.append((True, name_175, sample_175, ast_175))

name_176 = "sample_176.g"
sample_176 = """\
module A
  defmacro m (throw e; throw Error, "failed";)
end
"""
ast_176 = DefModule("A", [
    DefMacro("m", [], [
        sl_(MacroNode(Rethrow,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("e")
            ), name_176, 2, 21)
        ), name_176, 2, 15),
        sl_(MacroNode(Throw,
            sl_(MacroNode(GetLocal,
                MacroNodeAtom("Error")
            ), name_176, 2, 30),
            sl_(MacroNode(Const,
                MacroNodeAtom("failed")
            ), name_176, 2, 37)
        ), name_176, 2, 24)
    ]).set_location(name_176, 2, 3)
]).set_location(name_176, 1, 1)
test_samples.append((True, name_176, sample_176, ast_176))

class TestGlapParserCase(unittest.TestCase):

    def test_parsing(self):
        for p in test_samples:
            self.do_parsing_test(*p)
    #-def

    def do_parsing_test(self, should_succeed, name, data, ast):
        result = None
        if not should_succeed:
            with self.assertRaises(ParsingError):
                result = self.parse_data(name, data)
        else:
            result = self.parse_data(name, data)
        self.maxDiff = None
        self.assertEqual(result, ast)
    #-def

    def parse_data(self, name, data):
        ctx = GlapContext()
        GlapStream(ctx, name, data)
        GlapLexer(ctx)
        parser = GlapParser(ctx)
        GlapParserActions(ctx)
        return parser.parse()
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMakeLocationCase))
    suite.addTest(unittest.makeSuite(TestGlapErrorsCase))
    suite.addTest(unittest.makeSuite(TestGlapContextCase))
    suite.addTest(unittest.makeSuite(TestGlapStreamCase))
    suite.addTest(unittest.makeSuite(TestGlapTokenCase))
    suite.addTest(unittest.makeSuite(TestGlapLexerCase))
    suite.addTest(unittest.makeSuite(TestGlapParserCase))
    return suite
#-def
