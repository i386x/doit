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

from doit.text.pgen.errors import ParsingError

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

name_001 = "sample_001.g"
sample_001 = """\
-- Sample grammar

module sample_001
  grammar X
    start -> "a"+;
  end
end
"""
ast_001 = None

name_002 = "sample_002.g"
sample_002 = """\
module sample_002
  x = "\\u012f";
end
"""
ast_002 = None

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

test_samples = [
  (True, name_001, sample_001, ast_001),
  (True, name_002, sample_002, ast_002)
]

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
