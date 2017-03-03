#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/utils/tagengine.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2017-02-25 01:17:26 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Tag engine.\
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

from doit.support.app.io import read_all

OT_IMM = 0
OT_REG = 1
OT_STK = 2

TES_IDLE = 0
TES_RUNNING = 1
TES_PAUSED = 2
TES_HALTED = 3
TES_ERROR = 4

class TagAbstractInput(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def

    def peek(self):
        """
        """

        return None
    #-def

    def peekn(self, n):
        """
        """

        return None
    #-def

    def next(self):
        """
        """

        pass
    #-def

    def nextn(self, n):
        """
        """

        pass
    #-def
#-class

class TagTextInput(TagAbstractInput):
    """
    """
    __slots__ = [ '__index', '__nitems', '__data' ]

    def __init__(self):
        """
        """

        TagAbstractInput.__init__(self)
        self.__index = 0
        self.__nitems = 0
        self.__data = []
    #-def

    def load_data_from_string(self, s):
        """
        """

        self.__data = s
        self.__nitems = len(self.__data)
        self.__index = 0
    #-def

    def load_data_from_file(self, path):
        """
        """

        s = read_all(path)
        if s is None:
            return False
        self.load_data_from_string(s)
        return True
    #-def

    def peek(self):
        """
        """

        if self.__index < self.__nitems:
            return self.__data[self.__index]
        return None
    #-def

    def peekn(self, n):
        """
        """

        return self.__data[self.__index : self.__index + n]
    #-def

    def next(self):
        """
        """

        self.__index += 1
        if self.__index >= self.__nitems:
            self.__index = self.__nitems
    #-def

    def nextn(self, n):
        """
        """

        self.__index += n
        if self.__index >= self.__nitems:
            self.__index = self.__nitems
    #-def
#-class

class TagMatcher(object):
    """
    """
    __slots__ = [ '__input', '__last_match', '__last_error_detail' ]

    def __init__(self, input):
        """
        """

        self.__input = input
        self.__last_match = None
        self.__last_error_detail = ""
    #-def

    def match_symbol(self, symbol):
        """
        """

        return self.match_if(lambda c: c == symbol)
    #-def

    def match_any(self):
        """
        """

        return self.match_if(lambda c: c is not None)
    #-def

    def match_word(self, word):
        """
        """

        n = len(word)
        w = self.__input.peekn(n)
        if w == word:
            self.__last_match = w
            self.__input.nextn(n)
            return True
        if w is None or len(w) < n:
            self.__last_error_detail = \
                "Unexpected end of input (%r matched, %r needed)" % (w, word)
        else:
            self.__last_error_detail = \
                "Unexpected word %r (need %r)" % (w, word)
        return False
    #-def

    def match_set(self, set):
        """
        """

        return self.match_if(lambda c: c in set)
    #-def

    def match_range(self, a, b):
        """
        """

        return self.match_if(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def match_if(self, p):
        """
        """

        c = self.__input.peek()
        if p(c):
            self.__last_match = c
            self.__input.next()
            return True
        return self.bad_match(c)
    #-def

    def match_at_least_one_symbol(self, symbol):
        """
        """

        return self.match_at_least_one(lambda c: c == symbol)
    #-def

    def match_at_least_one_from_set(self, set):
        """
        """

        return self.match_at_least_one(lambda c: c in set)
    #-def

    def match_at_least_one_from_range(self, a, b):
        """
        """

        return self.match_at_least_one(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def match_at_least_one(self, p):
        """
        """

        c = self.__input.peek()
        if not p(c):
            return self.bad_match(c)
        m = [c]
        self.__input.next()
        while True:
            c = self.__input.peek()
            if not p(c):
                break
            m.append(c)
            self.__input.next()
        self.__last_match = m
        return True
    #-def

    def match_at_most_one_symbol(self, symbol):
        """
        """

        return self.match_at_most_one(lambda c: c == symbol)
    #-def

    def match_at_most_one_from_set(self, set):
        """
        """

        return self.match_at_most_one(lambda c: c in set)
    #-def

    def match_at_most_one_from_range(self, a, b):
        """
        """

        return self.match_at_most_one(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def match_at_most_one(self, p):
        """
        """

        c = self.__input.peek()
        m = []
        if p(c):
            m.append(c)
            self.__input.next()
        self.__last_match = m
        return True
    #-def

    def match_many_symbols(self, symbol):
        """
        """

        return self.match_many(lambda c: c == symbol)
    #-def

    def match_many_from_set(self, set):
        """
        """

        return self.match_many(lambda c: c in set)
    #-def

    def match_many_from_range(self, a, b):
        """
        """

        return self.match_many(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def match_all(self):
        """
        """

        return self.match_many(lambda c: c is not None)
    #-def

    def match_many(self, p):
        """
        """

        m = []
        while True:
            c = self.__input.peek()
            if not p(c):
                break
            m.append(c)
            self.__input.next()
        self.__last_match = m
        return True
    #-def

    def test_eof(self):
        """
        """

        return self.test_if(lambda c: c is None)
    #-def

    def test_symbol(self, symbol):
        """
        """

        return self.test_if(lambda c: c == symbol)
    #-def

    def test_set(self, set):
        """
        """

        return self.test_if(lambda c: c in set)
    #-def

    def test_range(self, a, b):
        """
        """

        return self.test_if(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def test_if(self, p):
        """
        """

        return p(self.__input.peek())
    #-def

    def branch(self, table, default, eof):
        """
        """

        c = self.__input.peek()
        if c is None:
            return eof
        return table.get(c, default)
    #-def

    def skip_symbol(self, symbol):
        """
        """

        return self.skip_if(lambda c: c == symbol)
    #-def

    def skip_any(self):
        """
        """

        return self.skip_if(lambda c: c is not None)
    #-def

    def skip_set(self, set):
        """
        """

        return self.skip_if(lambda c: c in set)
    #-def

    def skip_range(self, a, b):
        """
        """

        return self.skip_if(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def skip_if(self, p):
        """
        """

        if p(self.__input.peek()):
            self.__input.next()
            return True
        return self.bad_match(self.__input.peek())
    #-def

    def skip_at_least_one_symbol(self, symbol):
        """
        """

        return self.skip_at_least_one(lambda c: c == symbol)
    #-def

    def skip_at_least_one_from_set(self, set):
        """
        """

        return self.skip_at_least_one(lambda c: c in set)
    #-def

    def skip_at_least_one_from_range(self, a, b):
        """
        """

        return self.skip_at_least_one(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def skip_at_least_one(self, p):
        """
        """

        if not p(self.__input.peek()):
            return self.bad_match(self.__input.peek())
        self.__input.next()
        while p(self.__input.peek()):
            self.__input.next()
        return True
    #-def

    def skip_at_most_one_symbol(self, symbol):
        """
        """

        return self.skip_at_most_one(lambda c: c == symbol)
    #-def

    def skip_at_most_one_from_set(self, set):
        """
        """

        return self.skip_at_most_one(lambda c: c in set)
    #-def

    def skip_at_most_one_from_range(self, a, b):
        """
        """

        return self.skip_at_most_one(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def skip_at_most_one(self, p):
        """
        """

        if p(self.__input.peek()):
            self.__input.next()
        return True
    #-def

    def skip_many_symbols(self, symbol):
        """
        """

        return self.skip_many(lambda c: c == symbol)
    #-def

    def skip_many_from_set(self, set):
        """
        """

        return self.skip_many(lambda c: c in set)
    #-def

    def skip_many_from_range(self, a, b):
        """
        """

        return self.skip_many(
            lambda c: c is not None and ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def skip_all(self):
        """
        """

        return self.skip_many(lambda c: c is not None)
    #-def

    def skip_many(self, p):
        """
        """

        while p(self.__input.peek()):
            self.__input.next()
        return True
    #-def

    def skip_to(self, symbol):
        """
        """

        return self.skip_until_not(lambda c: c == symbol)
    #-def

    def skip_to_set(self, set):
        """
        """

        return self.skip_until_not(lambda c: c in set)
    #-def

    def skip_to_range(self, a, b):
        """
        """

        return self.skip_until_not(
            lambda c: ord(a) <= ord(c) and ord(c) <= ord(b)
        )
    #-def

    def skip_until_not(self, p):
        """
        """

        while True:
            c = self.__input.peek()
            if c is None:
                break
            if p(c):
                break
            self.__input.next()
        return True
    #-def

    def bad_match(self, c):
        """
        """

        if c is not None:
            self.__last_error_detail = "Unexpected input symbol %r" % c
        else:
            self.__last_error_detail = "Unexpected end of input"
        return False
    #-def

    def last_match(self):
        """
        """

        return self.__last_match
    #-def

    def last_error_detail(self):
        """
        """

        return self.__last_error_detail
    #-def
#-class

class TagCommand(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def

    def __call__(self, tag_engine):
        """
        """

        pass
    #-def
#-class

class Fail(TagCommand):
    """
    """
    __slots__ = [ '__detail' ]

    def __init__(self, detail):
        """
        """

        TagCommand.__init__(self)
        self.__detail = detail
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.set_match_flag(False)
        tag_engine.set_error_detail(self.__detail)
        tag_engine.set_state(TES_ERROR)
    #-def
#-class

class MatchCommand(TagCommand):
    """
    """
    __slots__ = [ '__matcher_name', '__args' ]

    def __init__(self, matcher_name, *args):
        """
        """

        TagCommand.__init__(self)
        self.__matcher_name = matcher_name
        self.__args = args
    #-def

    def __call__(self, tag_engine):
        """
        """

        matcher = tag_engine.matcher()
        if not getattr(matcher, self.__matcher_name)(*self.__args):
            tag_engine.set_match_flag(False)
            tag_engine.set_error_detail(matcher.last_error_detail())
            tag_engine.set_state(TES_ERROR)
            return
        tag_engine.set_match_flag(True)
        tag_engine.set_match(matcher.last_match())
    #-def
#-class

class MatchSymbol(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        MatchCommand.__init__(self, 'match_symbol', symbol)
    #-def
#-class

class MatchAny(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        MatchCommand.__init__(self, 'match_any')
    #-def
#-class

class MatchWord(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, word):
        """
        """

        MatchCommand.__init__(self, 'match_word', word)
    #-def
#-class

class MatchSet(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        MatchCommand.__init__(self, 'match_set', set)
    #-def
#-class

class MatchRange(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        MatchCommand.__init__(self, 'match_range', a, b)
    #-def
#-class

class MatchIf(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        MatchCommand.__init__(self, 'match_if', p)
    #-def
#-class

class MatchAtLeastOneSymbol(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        MatchCommand.__init__(self, 'match_at_least_one_symbol', symbol)
    #-def
#-class

class MatchAtLeastOneFromSet(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        MatchCommand.__init__(self, 'match_at_least_one_from_set', set)
    #-def
#-class

class MatchAtLeastOneFromRange(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        MatchCommand.__init__(self, 'match_at_least_one_from_range', a, b)
    #-def
#-class

class MatchAtLeastOne(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        MatchCommand.__init__(self, 'match_at_least_one', p)
    #-def
#-class

class MatchAtMostOneSymbol(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        MatchCommand.__init__(self, 'match_at_most_one_symbol', symbol)
    #-def
#-class

class MatchAtMostOneFromSet(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        MatchCommand.__init__(self, 'match_at_most_one_from_set', set)
    #-def
#-class

class MatchAtMostOneFromRange(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        MatchCommand.__init__(self, 'match_at_most_one_from_range', a, b)
    #-def
#-class

class MatchAtMostOne(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        MatchCommand.__init__(self, 'match_at_most_one', p)
    #-def
#-class

class MatchManySymbols(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        MatchCommand.__init__(self, 'match_many_symbols', symbol)
    #-def
#-class

class MatchManyFromSet(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        MatchCommand.__init__(self, 'match_many_from_set', set)
    #-def
#-class

class MatchManyFromRange(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        MatchCommand.__init__(self, 'match_many_from_range', a, b)
    #-def
#-class

class MatchAll(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        MatchCommand.__init__(self, 'match_all')
    #-def
#-class

class MatchMany(MatchCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        MatchCommand.__init__(self, 'match_many', p)
    #-def
#-class

class TestCommand(TagCommand):
    """
    """
    __slots__ = [ '__tester_name', '__args' ]

    def __init__(self, tester_name, *args):
        """
        """

        TagCommand.__init__(self)
        self.__tester_name = tester_name
        self.__args = args
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.set_match_flag(
            getattr(tag_engine.matcher(), self.__tester_name)(*self.__args)
        )
    #-def
#-class

class TestEof(TestCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TestCommand.__init__(self, 'test_eof')
    #-def
#-class

class TestSymbol(TestCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        TestCommand.__init__(self, 'test_symbol', symbol)
    #-def
#-class

class TestSet(TestCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        TestCommand.__init__(self, 'test_set', set)
    #-def
#-class

class TestRange(TestCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        TestCommand.__init__(self, 'test_range', a, b)
    #-def
#-class

class TestIf(TestCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        TestCommand.__init__(self, 'test_if', p)
    #-def
#-class

class Branch(TagCommand):
    """
    """
    __slots__ = [ '__args' ]

    def __init__(self, table, default, eof):
        """
        """

        TagCommand.__init__(self)
        self.__args = (table, default, eof)
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.set_ip(tag_engine.matcher().branch(*self.__args) - 1)
    #-def
#-class

class SkipCommand(TagCommand):
    """
    """
    __slots__ = [ '__skipper_name', '__args' ]

    def __init__(self, skipper_name, *args):
        """
        """

        TagCommand.__init__(self)
        self.__skipper_name = skipper_name
        self.__args = args
    #-def

    def __call__(self, tag_engine):
        """
        """

        matcher = tag_engine.matcher()
        if not getattr(matcher, self.__skipper_name)(*self.__args):
            tag_engine.set_match_flag(False)
            tag_engine.set_error_detail(matcher.last_error_detail())
            tag_engine.set_state(TES_ERROR)
            return
        tag_engine.set_match_flag(True)
    #-def
#-class

class SkipSymbol(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        SkipCommand.__init__(self, 'skip_symbol', symbol)
    #-def
#-class

class SkipAny(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        SkipCommand.__init__(self, 'skip_any')
    #-def
#-class

class SkipSet(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        SkipCommand.__init__(self, 'skip_set', set)
    #-def
#-class

class SkipRange(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        SkipCommand.__init__(self, 'skip_range', a, b)
    #-def
#-class

class SkipIf(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        SkipCommand.__init__(self, 'skip_if', p)
    #-def
#-class

class SkipAtLeastOneSymbol(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        SkipCommand.__init__(self, 'skip_at_least_one_symbol', symbol)
    #-def
#-class

class SkipAtLeastOneFromSet(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        SkipCommand.__init__(self, 'skip_at_least_one_from_set', set)
    #-def
#-class

class SkipAtLeastOneFromRange(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        SkipCommand.__init__(self, 'skip_at_least_one_from_range', a, b)
    #-def
#-class

class SkipAtLeastOne(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        SkipCommand.__init__(self, 'skip_at_least_one', p)
    #-def
#-class

class SkipAtMostOneSymbol(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        SkipCommand.__init__(self, 'skip_at_most_one_symbol', symbol)
    #-def
#-class

class SkipAtMostOneFromSet(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        SkipCommand.__init__(self, 'skip_at_most_one_from_set', set)
    #-def
#-class

class SkipAtMostOneFromRange(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        SkipCommand.__init__(self, 'skip_at_most_one_from_range', a, b)
    #-def
#-class

class SkipAtMostOne(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        SkipCommand.__init__(self, 'skip_at_most_one', p)
    #-def
#-class

class SkipManySymbols(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        SkipCommand.__init__(self, 'skip_many_symbols', symbol)
    #-def
#-class

class SkipManyFromSet(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        SkipCommand.__init__(self, 'skip_many_from_set', set)
    #-def
#-class

class SkipManyFromRange(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        SkipCommand.__init__(self, 'skip_many_from_range', a, b)
    #-def
#-class

class SkipAll(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        SkipCommand.__init__(self, 'skip_all')
    #-def
#-class

class SkipMany(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        SkipCommand.__init__(self, 'skip_many', p)
    #-def
#-class

class SkipTo(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, symbol):
        """
        """

        SkipCommand.__init__(self, 'skip_to', symbol)
    #-def
#-class

class SkipToSet(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, set):
        """
        """

        SkipCommand.__init__(self, 'skip_to_set', set)
    #-def
#-class

class SkipToRange(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        SkipCommand.__init__(self, 'skip_to_range', a, b)
    #-def
#-class

class SkipUntilNot(SkipCommand):
    """
    """
    __slots__ = []

    def __init__(self, p):
        """
        """

        SkipCommand.__init__(self, 'skip_until_not', p)
    #-def
#-class

class Push(TagCommand):
    """
    """
    __slots__ = [ '__v' ]

    def __init__(self, v):
        """
        """

        TagCommand.__init__(self)
        self.__v = v
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.pushval(self.__v)
    #-def
#-class

class PushMatch(TagCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TagCommand.__init__(self)
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.push_match()
    #-def
#-class

class PopMatch(TagCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TagCommand.__init__(self)
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.pop_match()
    #-def
#-class

class Swap(TagCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TagCommand.__init__(self)
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.swap()
    #-def
#-class

class Operator(TagCommand):
    """
    """
    __slots__ = [ '__name', '__op1', '__op2' ]

    def __init__(self, name, op1, op2):
        """
        """

        TagCommand.__init__(self)
        self.__name = name
        self.__op1 = op1
        self.__op2 = op2
    #-def

    def __call__(self, tag_engine):
        """
        """

        op2 = self.load_operand(tag_engine, self.__op2)
        if tag_engine.state() == TES_ERROR:
            return
        op1 = self.load_operand(tag_engine, self.__op1)
        if tag_engine.state() == TES_ERROR:
            return
        getattr(self, 'do_%s' % self.__name)(tag_engine, op1, op2)
    #-def

    @staticmethod
    def do_concat(tag_engine, op1, op2):
        """
        """

        if isinstance(op1, (list, tuple)):
            op1 = ''.join(op1)
        if isinstance(op2, (list, tuple)):
            op2 = ''.join(op2)
        tag_engine.pushval(op1 + op2)
    #-def

    @staticmethod
    def do_join(tag_engine, op1, op2):
        """
        """

        if isinstance(op1, tuple):
            op1 = list(op1)
        if isinstance(op1, str):
            op1 = [op1]
        if isinstance(op2, tuple):
            op2 = list(op2)
        if isinstance(op2, str):
            op2 = [op2]
        tag_engine.pushval(op1 + op2)
    #-def

    @staticmethod
    def load_operand(tag_engine, operand):
        """
        """

        t, v = operand
        if t == OT_IMM:
            return v
        elif t == OT_REG:
            return tag_engine.match()
        elif t == OT_STK:
            return tag_engine.popval()
        tag_engine.set_error_detail("Invalid type of instruction operand")
        tag_engine.set_state(TES_ERROR)
        return None
    #-def
#-class

class Concat(Operator):
    """
    """
    __slots__ = []

    def __init__(self, op1, op2):
        """
        """

        Operator.__init__(self, 'concat', op1, op2)
    #-def
#-class

class Join(Operator):
    """
    """
    __slots__ = []

    def __init__(self, op1, op2):
        """
        """

        Operator.__init__(self, 'join', op1, op2)
    #-def
#-class

class JTrue(TagCommand):
    """
    """
    __slots__ = [ '__dest' ]

    def __init__(self, dest):
        """
        """

        TagCommand.__init__(self)
        self.__dest = dest - 1
    #-def

    def __call__(self, tag_engine):
        """
        """

        if tag_engine.match_flag():
            tag_engine.set_ip(self.__dest)
    #-def
#-class

class JFalse(TagCommand):
    """
    """
    __slots__ = [ '__dest' ]

    def __init__(self, dest):
        """
        """

        TagCommand.__init__(self)
        self.__dest = dest - 1
    #-def

    def __call__(self, tag_engine):
        """
        """

        if not tag_engine.match_flag():
            tag_engine.set_ip(self.__dest)
    #-def
#-class

class Jump(TagCommand):
    """
    """
    __slots__ = [ '__dest' ]

    def __init__(self, dest):
        """
        """

        TagCommand.__init__(self)
        self.__dest = dest - 1
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.set_ip(self.__dest)
    #-def
#-class

class Call(TagCommand):
    """
    """
    __slots__ = [ '__f' ]

    def __init__(self, f):
        """
        """

        TagCommand.__init__(self)
        self.__f = f
    #-def

    def __call__(self, tag_engine):
        """
        """

        self.__f(tag_engine)
    #-def
#-class

class Pause(TagCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TagCommand.__init__(self)
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.set_state(TES_PAUSED)
    #-def
#-class

class Halt(TagCommand):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        TagCommand.__init__(self)
    #-def

    def __call__(self, tag_engine):
        """
        """

        tag_engine.set_state(TES_HALTED)
    #-def
#-class

class TagProgramEnvironment(object):
    """
    """
    __slots__ = [ '__engine' ]

    def __init__(self, engine = None):
        """
        """

        self.__engine = engine
    #-def

    def attach_engine(self, engine):
        """
        """

        self.__engine = engine
    #-def

    def engine(self):
        """
        """

        return self.__engine
    #-def
#-class

class TagProgram(object):
    """
    """
    __slots__ = [ '__name', '__envclass', '__code' ]

    def __init__(self, name, envclass = TagProgramEnvironment, code = []):
        """
        """

        self.__name = name
        self.__envclass = envclass
        self.__code = code
    #-def

    def name(self):
        """
        """

        return self.__name
    #-def

    def envclass(self):
        """
        """

        return self.__envclass
    #-def

    def code(self):
        """
        """

        return self.__code
    #-def
#-class

class TagEngine(object):
    """
    """
    __slots__ = [
        '__program_name', '__env', '__matcher',
        '__valstack', '__code', '__code_size',
        '__ip', '__match', '__match_flag',
        '__state', '__last_error_detail'
    ]

    def __init__(self):
        """
        """

        self.reset()
    #-def

    def load(self, program):
        """
        """

        self.reset()
        if program is None:
            return
        self.__program_name = program.name()
        self.__env = program.envclass()(self)
        self.__code = program.code()
        self.__code_size = len(self.__code)
    #-def

    def ip_is_out_of_range(self):
        """
        """

        if 0 <= self.__ip and self.__ip < self.__code_size:
            return False
        self.__state = TES_ERROR
        self.__last_error_detail = \
            "Invalid tag engine instruction address (%r)" % self.__ip
        return True
    #-def

    def initialize_run(self, input, program):
        """
        """

        # TES_ERROR -> TES_ERROR
        if self.__state == TES_ERROR:
            return False
        # {TES_RUNNING, TES_PAUSED} -> TES_RUNNING
        elif self.__state in (TES_RUNNING, TES_PAUSED):
            self.__state = TES_RUNNING
            return True
        # {TES_IDLE, TES_HALTED} -> TES_IDLE -> TES_RUNNING
        self.load(program)
        self.__matcher = TagMatcher(input)
        self.__state = TES_RUNNING
        return True
    #-def

    def run(self, input, program = None):
        """
        """

        if not self.initialize_run(input, program):
            return
        while self.__state == TES_RUNNING:
            if self.ip_is_out_of_range():
                break
            self.__code[self.__ip](self)
            self.__ip += 1
    #-def

    def program_name(self):
        """
        """

        return self.__program_name
    #-def

    def env(self):
        """
        """

        return self.__env
    #-def

    def matcher(self):
        """
        """

        return self.__matcher
    #-def

    def push_match(self):
        """
        """

        self.__valstack.append(self.__match)
    #-def

    def pop_match(self):
        """
        """

        if not self.__valstack:
            self.__last_error_detail = "Pop applied on empty stack"
            self.__state = TES_ERROR
            return
        self.__match = self.__valstack.pop()
    #-def

    def pushval(self, v):
        """
        """

        self.__valstack.append(v)
    #-def

    def popval(self):
        """
        """

        if not self.__valstack:
            self.__last_error_detail = "Pop applied on empty stack"
            self.__state = TES_ERROR
            return None
        return self.__valstack.pop()
    #-def

    def topval(self):
        """
        """

        if not self.__valstack:
            self.__last_error_detail = "Top applied on empty stack"
            self.__state = TES_ERROR
            return None
        return self.__valstack[-1]
    #-def

    def swap(self):
        """
        """

        if self.nvals() < 2:
            self.__last_error_detail = "Swap needs at least two items on stack"
            self.__state = TES_ERROR
            return
        t = self.__valstack[-1]
        self.__valstack[-1] = self.__valstack[-2]
        self.__valstack[-2] = t
    #-def

    def nvals(self):
        """
        """

        return len(self.__valstack)
    #-def

    def code(self):
        """
        """

        return self.__code
    #-def

    def code_size(self):
        """
        """

        return self.__code_size
    #-def

    def set_ip(self, ip):
        """
        """

        self.__ip = ip
    #-def

    def ip(self):
        """
        """

        return self.__ip
    #-def

    def set_match(self, match):
        """
        """

        self.__match = match
    #-def

    def match(self):
        """
        """

        return self.__match
    #-def

    def set_match_flag(self, flag):
        """
        """

        self.__match_flag = flag
    #-def

    def match_flag(self):
        """
        """

        return self.__match_flag
    #-def

    def set_state(self, state):
        """
        """

        self.__state = state
    #-def

    def state(self):
        """
        """

        return self.__state
    #-def

    def set_error_detail(self, detail):
        """
        """

        self.__last_error_detail = detail
    #-def

    def last_error_detail(self):
        """
        """

        return self.__last_error_detail
    #-def

    def reset(self):
        """
        """

        self.__program_name = ""
        self.__env = None
        self.__matcher = None
        self.__valstack = []
        self.__code = []
        self.__code_size = 0
        self.__ip = 0
        self.__match = None
        self.__match_flag = False
        self.__state = TES_IDLE
        self.__last_error_detail = ""
    #-def
#-class
