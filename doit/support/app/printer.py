#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/app/printer.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-18 11:35:36 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Formatted printing services.\
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

from doit.text.fmt.format import \
    FormatError, \
    TextBlock, TextTerminal, \
    Var as _V, Term as _T, TextCommand, Indent, Dedent, Space, LineBreak, \
    Formatter

# Labels:
PAGE_2_PAR_PAGE = 0
PAGE_2_PAR = 1
PAR_2_WORDS = 0
PAR_2_TABLE = 1
WORDS_2_UWORDS = 0
UWORDS_2_WORD_UWORDS = 0
UWORDS_2_WORD = 1
TABLE_2_TBODY = 0
TBODY_2_TROW_TBODY = 0
TBODY_2_TROW = 1
TROW_2_UTROW = 0
UTROW_2_UWORDS_UTROW = 0
UTROW_2_UWORDS = 1

def escape(s):
    """
    """

    return s.replace('\\', "\\\\").replace(' ', "\\ ")
#-def

class BreakToLines(TextCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TextCommand.__init__(self)
        self.name = '%break_to_lines'
    #-def

    def run(self, block, formatter, input, output):
        """
        """

        # Synopsis:
        #   %indent? %break_to_lines WORD+ %end
        # Method:
        # 1) Handle indentation:
        indent = block.indentation_level * formatter.rules.indentation
        if output and isinstance(output[0], Indent):
            indent += formatter.rules.indentation
        # 2) Break to lines:
        limit = formatter.rules.line_limit
        line = []
        line_sz = 0
        while input:
            w = input[0]
            if isinstance(w, End):
                input.pop(0)
                break
            elif not isinstance(w, TextTerminal):
                line.append(input.pop(0))
            elif w.name != 'WORD':
                input.pop(0)
            elif line_sz > 0 and line_sz + 1 + len(w.data) < limit:
                line.append(Space())
                line.append(w)
                line_sz += 1 + len(w.data)
                input.pop(0)
            elif line_sz == 0 and indent + len(w.data) < limit:
                line.append(w)
                line_sz = indent + len(w.data)
                input.pop(0)
            elif not line:
                raise FormatError("Breaking to lines failed (too long line)")
            else:
                output.extend(line)
                output.append(LineBreak(0))
                line = []
                line_sz = 0
        if line:
            output.extend(line)
            output.append(LineBreak(0))
    #-def
#-class

class Table(TextCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TextCommand.__init__(self)
    #-def

    def run(self, block, formatter, input, output):
        """
        """

        # Synopsis:
        #   %indent?
        #   %table THEADER
        #     (%trow WORD+ (%tabsep WORD+)* %end)+
        #   %end
        # Method:
        # 1) Handle indentation:
        indent = block.indentation_level * formatter.rules.indentation
        if output and isinstance(output[0], Indent):
            indent += formatter.rules.indentation
        # 2) Get the table header:
        if not input or not isinstance(input[0], THeader):
            raise FormatError("Table header was expected")
        theader = input.pop(0)
        # 3) Process table rows (there is at least one):
        while input:
            if isinstance(input[0], End):
                input.pop(0)
                break
            self.process_trow(indent, formatter, theader, input, output)
    #-def

    def process_trow(self, indent, formatter, theader, input, output):
        """
        """

        if not (input and isinstance(input[0], TRow)):
            raise FormatError("%trow was expected")
        input.pop(0)
        line_limit = formatter.rules.line_limit
        line = []
        line_sz = 0
        is_blank = True
        col = 0
        new_col = True
        while input:
            e = input[0]
            if isinstance(e, End):
                input.pop(0)
                break
            elif isinstance(e, TabSep):
                # We are sure that %tabsep is predecessed by at least one word.
                next_col_start = theader.next_column_start(col)
                # The situation so far:
                # - The WORD before %tabsep does not fit to the current column
                #   and hence the whole line was emitted. In this case, we have
                #   line == [] and line_sz == 0.
                # - The WORD before %tabsep fits to the current column and we
                #   have line[-1] == WORD and line_sz > 0.
                if line_sz == 0:
                    # <indent> WORD("") SPACES |
                    #  the next column start --^
                    if indent + next_col_start >= line_limit:
                        raise FormatError("Table row is too long")
                    line_sz = indent
                    line.append(Word(""))
                    line.append(Space(next_col_start))
                    line_sz += next_col_start
                    is_blank = True
                else:
                    # <indent> <row_content_so_far> SPACES |
                    #              the next column start --^
                    padding = next_col_start - (line_sz - indent)
                    if padding < 1:
                        raise FormatError(
                            "Padding to the next column start has failed"
                        )
                    line.append(Space(padding))
                    line_sz += padding # (line_sz = indent + next_col_start)
                col += 1
                new_col = True
                input.pop(0)
            elif not isinstance(e, TextTerminal):
                line.append(input.pop(0))
            elif e.name != 'WORD':
                input.pop(0)
            # Test whether we fit to the line limit (non-empty line):
            elif line_sz > 0 and line_sz + 1 + len(e.data) < line_limit:
                # We fit. Test if we fit also to column:
                col_end = theader.column_end(col)
                if line_sz - indent + 1 + len(e.data) <= col_end:
                    # We fit.
                    if not new_col:
                        line.append(Space())
                        line_sz += 1
                    line.append(e)
                    line_sz += len(e.data)
                    is_blank = False
                    new_col = False
                    input.pop(0)
                else:
                    # We not fit. Finish the line:
                    line.append(LineBreak(0))
                    output.extend(line)
                    # There can be remaining words, so we prepare for them:
                    col_start = theader.column_start(col)
                    if col_start > 0:
                        line = [Word(""), Space(col_start)]
                    else:
                        line = []
                    line_sz = indent + col_start
                    is_blank = True
                    new_col = True
            # The same test but the line is empty:
            elif line_sz == 0 and indent + len(e.data) < line_limit:
                col_end = theader.column_end(col)
                if len(e.data) <= col_end:
                    line.append(e)
                    line_sz += indent + len(e.data)
                    is_blank = False
                    new_col = False
                else:
                    line.append(e)
                    line.append(LineBreak(0))
                    output.extend(line)
                    # We are still at 0th column:
                    line = []
                    line_sz = 0
                    is_blank = True
                    new_col = True
                input.pop(0)
            elif line_sz == 0 or is_blank:
                raise FormatError("Word is too long")
            # line and not is_blank:
            else:
                line.append(LineBreak(0))
                output.extend(line)
                if col == 0:
                    line = []
                    line_sz = 0
                    is_blank = True
                else:
                    col_start = theader.column_start(col)
                    line = [Word(""), Space(col_start)]
                    line_sz = indent + col_start
                    is_blank = True
                new_col = True
        if line and is_blank:
            # Filter out added blanks ("", ' ', '\n'):
            line = [
                e for e in line if not isinstance(e, (Word, Space, LineBreak))
            ]
            # Append the remaing non-terminals to the previous line:
            if line:
                output[-1:-1] = line
        elif line and not is_blank:
            line.append(LineBreak(0))
            output.extend(line)
    #-def
#-class

class TRow(TextCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TextCommand.__init__(self)
    #-def
#-class

class TabSep(TextCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TextCommand.__init__(self)
    #-def
#-class

class End(TextCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TextCommand.__init__(self)
    #-def
#-class

class PageFormatter(Formatter):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Formatter.__init__(self)
        r = self.rules
        r.indentation = 2
        r.line_limit = 80
        # page -> paragraph %linebreak(0) page
        r.add(PAGE_2_PAR_PAGE, 'page', [
            _V('paragraph'), LineBreak(0), _V('page')
        ])
        # page -> paragraph %linebreak(0)
        r.add(PAGE_2_PAR, 'page', [
            _V('paragraph') # LineBreak(0) is added automatically by `format`
        ])
        # paragraph -> words
        r.add(PAR_2_WORDS, 'paragraph', [
            _V('words')
        ])
        # paragraph -> %indent table %dedent
        r.add(PAR_2_TABLE, 'paragraph', [
            Indent(), _V('table'), Dedent()
        ])
        # words -> %break_to_lines _words %end
        r.add(WORDS_2_UWORDS, 'words', [
            BreakToLines(), _V('_words'), End()
        ])
        # _words -> WORD _words
        r.add(UWORDS_2_WORD_UWORDS, '_words', [
            _T('WORD'), _V('_words')
        ])
        # _words -> WORD
        r.add(UWORDS_2_WORD, '_words', [
            _T('WORD')
        ])
        # table -> %table THEADER tbody %end
        r.add(TABLE_2_TBODY, 'table', [
            Table(), _T('THEADER'), _V('tbody'), End()
        ])
        # tbody -> trow tbody
        r.add(TBODY_2_TROW_TBODY, 'tbody', [
            _V('trow'), _V('tbody')
        ])
        # tbody -> trow
        r.add(TBODY_2_TROW, 'tbody', [
            _V('trow')
        ])
        # trow -> %trow _trow %end
        r.add(TROW_2_UTROW, 'trow', [
            TRow(), _V('_trow'), End()
        ])
        # _trow -> _words %tabsep _trow
        r.add(UTROW_2_UWORDS_UTROW, '_trow', [
            _V('_words'), TabSep(), _V('_trow')
        ])
        # _trow -> _words
        r.add(UTROW_2_UWORDS, '_trow', [
            _V('_words')
        ])
    #-def
#-class

class Word(TextTerminal):
    """
    """
    __slots__ = []

    def __init__(self, w):
        """
        """

        TextTerminal.__init__(self, self.__class__.__name__.upper(), w)
    #-def
#-class

class THeader(TextTerminal):
    """
    """
    __slots__ = [
        'ncols', 'cols', 'nseps', 'seps', 'row_limit', 'column_start_cache',
        'column_end_cache', 'next_column_start_cache'
    ]

    def __init__(self, **spec):
        """
        """

        TextTerminal.__init__(self, self.__class__.__name__.upper())
        # spec format:
        #   col0 sep0 col1 sep1 ... colN
        self.set_and_verify_spec(spec)
        self.row_limit = 0
        for k in spec:
            self.row_limit += spec[k]
        self.data = self
        self.column_start_cache = {}
        self.column_end_cache = {}
        self.next_column_start_cache = {}
    #-def

    def set_and_verify_spec(self, spec):
        """
        """

        if len(spec) % 2 != 1:
            raise FormatError(
                "The number of specifiers in table header must be odd"
            )
        self.nseps = (len(spec) - 1) // 2
        self.check_spec_items(spec, "sep", self.nseps)
        self.ncols = self.nseps + 1
        self.check_spec_items(spec, "col", self.ncols)
        self.cols = [spec['col%d' % i] for i in range(self.ncols)]
        self.seps = [spec['sep%d' % i] for i in range(self.nseps)]
    #-def

    def check_spec_items(self, spec, p, n):
        """
        """

        for i in range(n):
            k = '%s%d' % (p, i)
            if k not in spec:
                raise FormatError("I expect %s in table header specifier" % k)
            if not isinstance(spec[k], int) or spec[k] <= 0:
                raise FormatError("%s must be positive integer" % k)
    #-def

    def column_start(self, column):
        """
        """

        if column in self.column_start_cache:
            return self.column_start_cache[column]
        if not (0 <= column and column < self.ncols):
            raise FormatError("Bad column number")
        i, x = 0, 0
        while i < column:
            x += self.cols[i] + self.seps[i]
            i += 1
        self.column_start_cache[column] = x
        return x
    #-def

    def column_end(self, column):
        """
        """

        if column in self.column_end_cache:
            return self.column_end_cache[column]
        x = self.column_start(column)
        # The sum is splitted since column_start checks the borders.
        x += self.cols[column]
        self.column_end_cache[column] = x
        return x
    #-def

    def next_column_start(self, column):
        """
        """

        if column in self.next_column_start_cache:
            return self.next_column_start_cache[column]
        # Checks the borders.
        self.column_start(column)
        x = self.column_start(column + 1)
        self.next_column_start_cache[column] = x
        return x
    #-def
#-class

class TableBuilder(object):
    """
    """
    __slots__ = [ 'table', 'theader', 'tbody', 'tbody_tail' ]

    def __init__(self, **spec):
        """
        """

        self.table = None
        self.theader = THeader(**spec)
        self.tbody = None
        self.tbody_tail = None
    #-def

    def empty(self):
        """
        """

        return self.table is None
    #-def

    def row(self, *cols):
        """
        """

        ncols = self.theader.ncols
        if len(cols) != ncols:
            raise FormatError("I expect %d%s columns in a row" % (
                ncols, "" if ncols == 1 else 's')
            )
        cols = list(cols)
        _trow = TextBlock('_trow', [
            PageBuilder.to_uwords(cols.pop(0)[:])
        ], UTROW_2_UWORDS)
        tail = _trow
        while cols:
            tail.elements.append(
                TextBlock('_trow', [
                    PageBuilder.to_uwords(cols.pop(0)[:])
                ], UTROW_2_UWORDS)
            )
            tail.alternative = UTROW_2_UWORDS_UTROW
            tail = tail.elements[-1]
        trow = TextBlock('trow', [_trow], TROW_2_UTROW)
        self.contribute(trow)
    #-def

    def contribute(self, trow):
        """
        """

        if self.table is None:
            self.tbody = TextBlock('tbody', [trow], TBODY_2_TROW)
            self.tbody_tail = self.tbody
            self.table = TextBlock(
                'table', [self.theader, self.tbody], TABLE_2_TBODY
            )
            return
        self.tbody_tail.elements.append(
            TextBlock('tbody', [trow], TBODY_2_TROW)
        )
        self.tbody_tail.alternative = TBODY_2_TROW_TBODY
        self.tbody_tail = self.tbody_tail.elements[-1]
    #-def
#-class

class PageBuilder(object):
    """
    """
    __slots__ = [ 'page', 'page_tail' ]

    def __init__(self):
        """
        """

        self.page = None
        self.page_tail = None
    #-def

    def empty(self):
        """
        """

        return self.page is None
    #-def

    def contribute(self, par):
        """
        """

        if self.empty():
            self.page = TextBlock('page', [par], PAGE_2_PAR)
            self.page_tail = self.page
            return
        self.page_tail.elements.append(TextBlock('page', [par], PAGE_2_PAR))
        self.page_tail.alternative = PAGE_2_PAR_PAGE
        self.page_tail = self.page_tail.elements[-1]
    #-def

    def paragraph(self, text):
        """
        """

        words = self.to_words(text)
        if not words:
            return
        words = TextBlock('words', [self.to_uwords(words[:])], WORDS_2_UWORDS)
        par = TextBlock('paragraph', [words], PAR_2_WORDS)
        self.contribute(par)
    #-def

    def table(self, table):
        """
        """

        if table.empty():
            return
        par = TextBlock('paragraph', [table.table], PAR_2_TABLE)
        self.contribute(par)
    #-def

    @staticmethod
    def to_uwords(words):
        """
        """

        _words = TextBlock('_words', [words.pop(0)], UWORDS_2_WORD)
        tail = _words
        while words:
            tail.elements.append(
                TextBlock('_words', [words.pop(0)], UWORDS_2_WORD)
            )
            tail.alternative = UWORDS_2_WORD_UWORDS
            tail = tail.elements[-1]
        return _words
    #-def

    @staticmethod
    def to_words(text):
        """
        """

        words, i = [], 0
        while True:
            word, i = PageBuilder.get_word(text, i)
            if word is None:
                break
            words.append(word)
        return words
    #-def

    @staticmethod
    def get_word(s, i):
        """
        """

        while i < len(s) and s[i].isspace():
            i += 1
        w = ""
        while i < len(s) and not s[i].isspace():
            if s[i] == '\\':
                i += 1
                if i >= len(s):
                    break
            w += s[i]
            i += 1
        return (Word(w) if w else None, i)
    #-def
#-class
