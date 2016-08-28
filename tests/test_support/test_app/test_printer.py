#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_app/test_printer.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-26 10:30:17 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Printer tests.\
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

from doit.text.fmt.format import \
    FormatError, \
    TextTerminal, \
    TextOp, Indent, \
    Block, \
    Formatter

from doit.support.app.printer import \
    BreakToLines, Table, TRow, TabSep, End, \
    PageFormatter, \
    Word, THeader, \
    TableBuilder, PageBuilder

wc_help = """\
Usage: wc [OPTION]... [FILE]...

Print newline, word, and byte counts for each FILE, and a total line if more
than one FILE is specified. With no FILE, or when FILE is -, read standard
input.

  -c, --bytes            print the byte counts
  -m, --chars            print the character counts
  -l, --lines            print the newline counts
  -L, --max-line-length  print the length of the longest line
  -w, --words            print the word counts
      --help             display this help and exit
      --version          output version information and exit

Report bugs to <bug-coreutils@gnu.org>.

"""

class NonWord(TextTerminal):
    __slots__ = []

    def __init__(self):
        TextTerminal.__init__(self, 'NONWORD', None)
    #-def
#-class

class Foo(TextOp):
    __slots__ = []

    def __init__(self):
        TextOp.__init__(self, '%foo', None)
    #-def
#-class

class Output(object):
    __slots__ = [ 'data' ]

    def __init__(self):
        self.data = ""
    #-def

    def write(self, s):
        self.data += s
    #-def
#-class

class FormatterA(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.indentation = 2
        r.line_limit = 80
    #-def
#-class

class _THeader(THeader):
    __slots__ = []

    def __init__(self, **spec):
        THeader.__init__(self, **spec)
    #-def

    def next_column_start(self, column):
        return 1
    #-def
#-class

class TestBreakToLinesCase(unittest.TestCase):

    def setUp(self):
        s = "ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"
        s = "%s%s%s" % (s, s, s)
        self.blockA = Block([
            Indent(), BreakToLines(),
            Word("THE"), Word("SOFTWARE"), Word("IS"), Word("PROVIDED"),
            Foo(),
            Word("\"AS IS\","), Word("WITHOUT"), Word("WARRANTY"), Word("OF"),
            NonWord(),
            Word("ANY"), Word("KIND,"), Word("EXPRESS"), Word("OR"),
            NonWord(), Foo(),
            Word("IMPLIED,"), Word("INCLUDING"), Word("BUT"), Word("NOT"),
            Word("LIMITED"), Word("TO"), Word("THE"), Word("WARRANTIES"),
            Foo(),
            Word("OF"), Word("MERCHANTABILITY,"), Word("FITNESS"), Word("FOR"),
            NonWord(),
            Word("A"), Word("PARTICULAR"), Word("PURPOSE"), Word("AND"),
            Foo(),
            Word("NONINFRINGEMENT."), End()
        ], 1)
        self.blockB = Block([
            BreakToLines(), Foo(), Word(s), End()
        ], 0)
    #-def

    def test_with_indent(self):
        formatter = FormatterA()
        input = self.blockA.elements[:]
        output = []

        output.append(input.pop(0))
        input.pop(0).run(self.blockA, formatter, input, output)
        self.assertEqual([repr(x) for x in output], [
            '%indent',
            "WORD('THE')", '%space(1)', "WORD('SOFTWARE')", '%space(1)',
                "WORD('IS')", '%space(1)', "WORD('PROVIDED')", '%foo',
                '%space(1)', "WORD('\"AS IS\",')", '%space(1)',
                "WORD('WITHOUT')", '%space(1)', "WORD('WARRANTY')",
                '%space(1)', "WORD('OF')", '%space(1)', "WORD('ANY')",
                '%space(1)', "WORD('KIND,')", '%space(1)', "WORD('EXPRESS')",
                '%space(1)', "WORD('OR')", '%foo', '%linebreak(0)',
            "WORD('IMPLIED,')", '%space(1)', "WORD('INCLUDING')", '%space(1)',
                "WORD('BUT')", '%space(1)', "WORD('NOT')", '%space(1)',
                "WORD('LIMITED')", '%space(1)', "WORD('TO')", '%space(1)',
                "WORD('THE')", '%space(1)', "WORD('WARRANTIES')", '%foo',
                '%space(1)', "WORD('OF')", '%space(1)',
                "WORD('MERCHANTABILITY,')", '%linebreak(0)',
            "WORD('FITNESS')", '%space(1)', "WORD('FOR')", '%space(1)',
                "WORD('A')", '%space(1)', "WORD('PARTICULAR')", '%space(1)',
                "WORD('PURPOSE')", '%space(1)', "WORD('AND')", '%foo',
                '%space(1)', "WORD('NONINFRINGEMENT.')", '%linebreak(0)'
        ])
    #-def

    def test_without_indent(self):
        formatter = FormatterA()
        input = self.blockA.elements[:]
        output = []

        input.pop(0)
        input.pop(0).run(self.blockA, formatter, input, output)
        self.assertEqual([repr(x) for x in output], [
            "WORD('THE')", '%space(1)', "WORD('SOFTWARE')", '%space(1)',
                "WORD('IS')", '%space(1)', "WORD('PROVIDED')", '%foo',
                '%space(1)', "WORD('\"AS IS\",')", '%space(1)',
                "WORD('WITHOUT')", '%space(1)', "WORD('WARRANTY')",
                '%space(1)', "WORD('OF')", '%space(1)', "WORD('ANY')",
                '%space(1)', "WORD('KIND,')", '%space(1)', "WORD('EXPRESS')",
                '%space(1)', "WORD('OR')", '%foo', '%linebreak(0)',
            "WORD('IMPLIED,')", '%space(1)', "WORD('INCLUDING')", '%space(1)',
                "WORD('BUT')", '%space(1)', "WORD('NOT')", '%space(1)',
                "WORD('LIMITED')", '%space(1)', "WORD('TO')", '%space(1)',
                "WORD('THE')", '%space(1)', "WORD('WARRANTIES')", '%foo',
                '%space(1)', "WORD('OF')", '%space(1)',
                "WORD('MERCHANTABILITY,')", '%linebreak(0)',
            "WORD('FITNESS')", '%space(1)', "WORD('FOR')", '%space(1)',
                "WORD('A')", '%space(1)', "WORD('PARTICULAR')", '%space(1)',
                "WORD('PURPOSE')", '%space(1)', "WORD('AND')", '%foo',
                '%space(1)', "WORD('NONINFRINGEMENT.')", '%linebreak(0)'
        ])
    #-def

    def test_lines_too_long(self):
        formatter = FormatterA()
        input = self.blockB.elements[:]
        output = []

        with self.assertRaises(FormatError):
            input.pop(0).run(self.blockB, formatter, input, output)
    #-def
#-class

class TestTHeaderCase(unittest.TestCase):

    def test_bad_spec(self):
        with self.assertRaises(FormatError):
            THeader()
        with self.assertRaises(FormatError):
            THeader(a = 1, b = 2)
        with self.assertRaises(FormatError):
            THeader(a = 1)
        with self.assertRaises(FormatError):
            THeader(col0 = 1, col1 = 2, sep1 = 3)
        with self.assertRaises(FormatError):
            THeader(col0 = "")
        with self.assertRaises(FormatError):
            THeader(col0 = 0)
        with self.assertRaises(FormatError):
            THeader(col0 = 1, sep0 = 2, col1 = 1, sep1 = 0, col2 = 3)
    #-def

    def test_integrity(self):
        h1 = THeader(col0 = 1)
        h2 = THeader(col0 = 10, sep0 = 2, col1 = 3)
        h3 = THeader(col0 = 20, sep0 = 3, col1 = 15, sep1 = 2, col2 = 40)

        self.assertEqual(h1.ncols, 1)
        self.assertEqual(h1.nseps, 0)
        self.assertEqual(h1.cols, [1])
        self.assertEqual(h1.seps, [])
        self.assertEqual(h1.row_limit, 1)

        self.assertEqual(h2.ncols, 2)
        self.assertEqual(h2.nseps, 1)
        self.assertEqual(h2.cols, [10, 3])
        self.assertEqual(h2.seps, [2])
        self.assertEqual(h2.row_limit, 15)

        self.assertEqual(h3.ncols, 3)
        self.assertEqual(h3.nseps, 2)
        self.assertEqual(h3.cols, [20, 15, 40])
        self.assertEqual(h3.seps, [3, 2])
        self.assertEqual(h3.row_limit, 80)

        with self.assertRaises(FormatError):
            h1.column_start(-1)
        with self.assertRaises(FormatError):
            h1.column_start(1)
        h1.column_start(0)
        with self.assertRaises(FormatError):
            h1.column_end(-1)
        with self.assertRaises(FormatError):
            h1.column_end(1)
        h1.column_end(0)
        with self.assertRaises(FormatError):
            h1.next_column_start(-1)
        with self.assertRaises(FormatError):
            h1.next_column_start(1)
        with self.assertRaises(FormatError):
            h1.next_column_start(0)
        self.assertEqual(h1.column_start_cache, {0: 0})
        self.assertEqual(h1.column_end_cache, {0: 1})
        self.assertEqual(h1.next_column_start_cache, {})

        with self.assertRaises(FormatError):
            h2.column_start(-1)
        h2.column_start(0)
        h2.column_start(1)
        with self.assertRaises(FormatError):
            h2.column_start(2)
        with self.assertRaises(FormatError):
            h2.column_end(-1)
        h2.column_end(0)
        h2.column_end(1)
        with self.assertRaises(FormatError):
            h2.column_end(2)
        with self.assertRaises(FormatError):
            h2.next_column_start(-1)
        h2.next_column_start(0)
        with self.assertRaises(FormatError):
            h2.next_column_start(1)
        with self.assertRaises(FormatError):
            h2.next_column_start(2)
        self.assertEqual(h2.column_start_cache, {0: 0, 1: 12})
        self.assertEqual(h2.column_end_cache, {0: 10, 1: 15})
        self.assertEqual(h2.next_column_start_cache, {0: 12})

        with self.assertRaises(FormatError):
            h3.column_start(-1)
        h3.column_start(0)
        h3.column_start(1)
        h3.column_start(2)
        with self.assertRaises(FormatError):
            h3.column_start(3)
        with self.assertRaises(FormatError):
            h3.column_end(-1)
        h3.column_end(0)
        h3.column_end(1)
        h3.column_end(2)
        with self.assertRaises(FormatError):
            h3.column_end(3)
        with self.assertRaises(FormatError):
            h3.next_column_start(-1)
        h3.next_column_start(0)
        h3.next_column_start(1)
        with self.assertRaises(FormatError):
            h3.next_column_start(2)
        self.assertEqual(h3.column_start_cache, {0: 0, 1: 23, 2: 40})
        self.assertEqual(h3.column_end_cache, {0: 20, 1: 38, 2: 80})
        self.assertEqual(h3.next_column_start_cache, {0: 23, 1: 40})
    #-def
#-class

#
# blockA:
# -------
#   ---------+---------+-----|---|---------+---------+---------+---------|
#   abcdefgh abcd abc wooord      abcdefghijklmno abcdefghijklmno abcdef
#   a12345 b12345 c12345 dddd     123-456-789 lkj-mno-pg895 z-z-z-w-W-Uio
#   a a a s s s                   lolo-trolo trololololol olol
#
class TestTableCase(unittest.TestCase):

    def setUp(self):
        self.blockA = Block([
            Indent(),
            Table(),
            THeader(col0 = 26, sep0 = 4, col1 = 40),
            TRow(),
            Word("abcdefgh"), Word("abcd"), Word("abc"), Word("wooord"),
            TabSep(),
            Word("abcdefghijklmno"), NonWord(), Word("abcdefghijklmno"), Foo(),
            Word("abcdef"),
            End(),
            TRow(),
            Word("a12345"), Word("b12345"), Foo(), Word("c12345"),
            Word("dddd"), Foo(),
            TabSep(),
            Foo(), NonWord(), Word("123-456-789"), Word("lkj-mno-pg895"),
            Word("z-z-z-w-W-Uio"), NonWord(), Foo(),
            End(),
            TRow(),
            Word("a"), Word("a"), Foo(), Word("a"), NonWord(), Word("s"),
            Word("s"), NonWord(), Word("s"), NonWord(),
            TabSep(),
            Word("lolo-trolo"), Word("trololololol"), Word("olol"), Foo(),
            End(),
            End()
        ], 1)
        self.blockB = Block([
            Table(),
            THeader(col0 = 15, sep0 = 2, col1 = 20),
            TRow(),
            Word("0123456789abcd"), Word("0123456789abcdefgh"),
            TabSep(),
            Word("abcd"), Word("efghijkl"), Word("mnopq"),
            End(),
            End()
        ])
    #-def

    def test_content_fits(self):
        formatter = FormatterA()
        input = self.blockA.elements[:]
        output = []

        output.append(input.pop(0))
        input.pop(0).run(self.blockA, formatter, input, output)
        self.assertEqual([repr(x) for x in output], [
            '%indent',
            "WORD('abcdefgh')", '%space(1)', "WORD('abcd')", '%space(1)',
                "WORD('abc')", '%space(1)', "WORD('wooord')", '%space(6)',
                "WORD('abcdefghijklmno')", '%space(1)',
                "WORD('abcdefghijklmno')", '%foo', '%space(1)',
                "WORD('abcdef')", '%linebreak(0)',
            "WORD('a12345')", '%space(1)', "WORD('b12345')", '%foo',
                '%space(1)', "WORD('c12345')", '%space(1)', "WORD('dddd')",
                '%foo', '%space(5)', '%foo', "WORD('123-456-789')",
                '%space(1)', "WORD('lkj-mno-pg895')", '%space(1)',
                "WORD('z-z-z-w-W-Uio')", '%foo', '%linebreak(0)',
            "WORD('a')", '%space(1)', "WORD('a')", '%foo', '%space(1)',
                "WORD('a')", '%space(1)', "WORD('s')", '%space(1)',
                "WORD('s')", '%space(1)', "WORD('s')", '%space(19)',
                "WORD('lolo-trolo')", '%space(1)', "WORD('trololololol')",
                '%space(1)', "WORD('olol')", '%foo', '%linebreak(0)'
        ])
    #-def

    def test_bad_theader(self):
        with self.assertRaises(FormatError):
            Table().run(Block([]), FormatterA(), [], [])
        with self.assertRaises(FormatError):
            Table().run(Block([]), FormatterA(), [1], [])
    #-def

    def test_bad_trow(self):
        with self.assertRaises(FormatError):
            Table().run(Block([]), FormatterA(), [THeader(col0 = 1), 1], [])
    #-def

    def test_content_not_fits_1(self):
        formatter = FormatterA()
        input = self.blockB.elements[:]
        output = []

        input.pop(0).run(self.blockB, formatter, input, output)
        self.assertEqual([repr(x) for x in output], [
            "WORD('0123456789abcd')", '%linebreak(0)',
            "WORD('0123456789abcdefgh')", '%linebreak(0)',
            "WORD('')", '%space(17)',
            "WORD('abcd')", '%space(1)', "WORD('efghijkl')", '%space(1)',
            "WORD('mnopq')", '%linebreak(0)'
        ])
    #-def

    def test_content_not_fits_2(self):
        s = "ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"
        s = "%s%s%s" % (s, s, s)
        with self.assertRaises(FormatError):
            Table().run(Block([]), FormatterA(), [
                THeader(col0 = 40, sep0 = 10, col1 = 25),
                TRow(), Word('a'), TabSep(), Word(s), End(),
                End()
            ], [])
    #-def

    def test_content_not_fits_3(self):
        with self.assertRaises(FormatError):
            Table().run(Block([]), FormatterA(), [
                THeader(col0 = 4, sep0 = 79, col1 = 25),
                TRow(), Word('abcde'), TabSep(), Word('a'), End(),
                End()
            ], [])
    #-def

    def test_content_not_fits_4(self):
        with self.assertRaises(FormatError):
            Table().run(Block([]), FormatterA(), [
                _THeader(col0 = 20, sep0 = 2, col1 = 20),
                TRow(), Word('a'), TabSep(), Word('b'), End(),
                End()
            ], [])
    #-def

    def test_content_not_fits_5(self):
        output = []
        Table().run(Block([]), FormatterA(), [
            THeader(col0 = 50, sep0 = 10, col1 = 18),
            TRow(),
            Word('aaaaaaaaa'), Word('bbbbbbbbb'), Word('ccccccccc'),
            Word('ddddddddd'), Word('eeeee'),
            Word('aaaaaaaaaabbbbbbbbbbccccccccccdddddddddd'),
            TabSep(),
            Word('x'),
            End(),
            End()
        ], output)
        self.assertEqual([repr(x) for x in output], [
            "WORD('aaaaaaaaa')", '%space(1)', "WORD('bbbbbbbbb')", '%space(1)',
                "WORD('ccccccccc')", '%space(1)', "WORD('ddddddddd')",
                '%space(1)', "WORD('eeeee')", '%linebreak(0)',
            "WORD('aaaaaaaaaabbbbbbbbbbccccccccccdddddddddd')", '%space(20)',
                "WORD('x')", '%linebreak(0)'
        ])
    #-def

    def test_invisible_content_1(self):
        output = []
        Table().run(Block([]), FormatterA(), [
            THeader(col0 = 40, sep0 = 2, col1 = 20),
            TRow(), Foo(), TabSep(), Foo(), End(),
            End()
        ], output)
        self.assertEqual([repr(x) for x in output], [
            '%foo', '%foo'
        ])
    #-def

    def test_invisible_content_2(self):
        output = []
        Table().run(Block([]), FormatterA(), [
            THeader(col0 = 40, sep0 = 2, col1 = 20),
            TRow(), Word('a'), TabSep(), Word('b'), End(),
            TRow(), Foo(), TabSep(), Foo(), End(),
            End()
        ], output)
        self.assertEqual([repr(x) for x in output], [
            "WORD('a')", '%space(41)', "WORD('b')",
            '%foo', '%foo', '%linebreak(0)'
        ])
    #-def
#-class

class TestPageBuilderCase(unittest.TestCase):

    def test_to_words(self):
        cases = [
            ("", []),
            ("\\", []),
            ("a\\", ["WORD('a')"]),
            ("  \\  ", ["WORD(' ')"]),
            ("  \\a  ", ["WORD('a')"]),
            ("  a   bc  ", ["WORD('a')", "WORD('bc')"]),
            ("aa", ["WORD('aa')"]),
            ("aa b", ["WORD('aa')", "WORD('b')"]),
            ("  a b", ["WORD('a')", "WORD('b')"]),
            ("a  ", ["WORD('a')"]),
            ("aa  ", ["WORD('aa')"]),
            ("  aa   bb   ", ["WORD('aa')", "WORD('bb')"]),
            ("  aa\\ bb cc d e\\ f\\ g  ", [
                "WORD('aa bb')", "WORD('cc')", "WORD('d')", "WORD('e f g')"
            ]),
            ("  aa\\ bb cc d e\\ f\\ g", [
                "WORD('aa bb')", "WORD('cc')", "WORD('d')", "WORD('e f g')"
            ]),
            ("aa\\ bb cc d e\\ f\\ g  ", [
                "WORD('aa bb')", "WORD('cc')", "WORD('d')", "WORD('e f g')"
            ]),
            ("aa\\ bb cc d e\\ f\\ g", [
                "WORD('aa bb')", "WORD('cc')", "WORD('d')", "WORD('e f g')"
            ])
        ]

        for case in cases:
            self.assertEqual(
                [repr(x) for x in PageBuilder.to_words(case[0])], case[1]
            )
    #-def

    def test_page_building(self):
        output, output_ = Output(), Output()
        formatter = PageFormatter()
        page = PageBuilder()
        self.assertTrue(page.empty())
        page.paragraph("Usage: wc\\ [OPTION]...\\ [FILE]...")
        page.paragraph("""
            Print newline, word, and byte counts for each FILE, and a total
            line if more than one FILE is specified. With no FILE, or when FILE
            is -, read standard input.
        """)
        table = TableBuilder(
            col0 = 3, sep0 = 1, col1 = 18, sep1 = 1, col2 = 40
        )
        self.assertTrue(table.empty())
        page.table(table)
        table.row(
            [Word("-c,")],
            [Word("--bytes")],
            [Word("print"), Word("the"), Word("byte"), Word("counts")]
        )
        table.row(
            [Word("-m,")],
            [Word("--chars")],
            [Word("print"), Word("the"), Word("character"), Word("counts")]
        )
        table.row(
            [Word("-l,")],
            [Word("--lines")],
            [Word("print"), Word("the"), Word("newline"), Word("counts")]
        )
        table.row(
            [Word("-L,")],
            [Word("--max-line-length")],
            [
                Word("print"), Word("the"), Word("length"), Word("of"),
                Word("the"), Word("longest"), Word("line")
            ]
        )
        table.row(
            [Word("-w,")],
            [Word("--words")],
            [Word("print"), Word("the"), Word("word"), Word("counts")]
        )
        table.row(
            [Word("")], [Word("--help")],
            [
                Word("display"), Word("this"), Word("help"), Word("and"),
                Word("exit")
            ]
        )
        table.row(
            [Word("")], [Word("--version")],
            [
                Word("output"), Word("version"), Word("information"),
                Word("and"), Word("exit")
            ]
        )
        with self.assertRaises(FormatError):
            table.row([Word("")])
        self.assertFalse(table.empty())
        page.table(table)
        page.paragraph("Report bugs to <bug-coreutils@gnu.org>.")
        page.paragraph("")
        self.assertFalse(page.empty())
        formatter.format(page.page, output)
        formatter.format(page.page, output_)
        self.assertEqual(output.data, wc_help)
        self.assertEqual(output_.data, wc_help)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBreakToLinesCase))
    suite.addTest(unittest.makeSuite(TestTHeaderCase))
    suite.addTest(unittest.makeSuite(TestTableCase))
    suite.addTest(unittest.makeSuite(TestPageBuilderCase))
    return suite
#-def
