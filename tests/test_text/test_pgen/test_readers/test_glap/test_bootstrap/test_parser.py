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
    GlapStream

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

    def location(self):
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

name_002 = "sample_002.g"
sample_002 = """\
module sample_002
  x = "\\u012f";
end
"""

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMakeLocationCase))
    suite.addTest(unittest.makeSuite(TestGlapErrorsCase))
    suite.addTest(unittest.makeSuite(TestGlapContextCase))
    suite.addTest(unittest.makeSuite(TestGlapStreamCase))
    return suite
#-def
