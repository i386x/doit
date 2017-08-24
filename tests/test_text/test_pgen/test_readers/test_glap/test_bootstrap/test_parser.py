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
    SetLocal, \
    DefModule

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
    make_location, \
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
