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

from doit.support.errors import doit_assert as _assert

from doit.support.app.io import read_all

OT_IMM = 0
OT_REG = 1
OT_STK = 2

TES_IDLE = 0
TES_RUNNING = 1
TES_PAUSED = 2
TES_HALTED = 3
TES_ERROR = 4

try:
    callable
except NameError:
    callable = lambda f: hasattr(f, '__call__')
#-try

iscallable = callable

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

# General opcodes:
TIC_UNUSED = -1
TIC_NULL   = 0

# Operand types:
TIC_EOF     = 1
TIC_SYMBOL  = 2
TIC_WORD    = 3
TIC_SET     = 4
TIC_RANGE   = 5
TIC_PRED    = 6
TIC_ANY     = 7
TIC_DEFAULT = 8

# Quantifiers:
TIC_1N = 1
TIC_01 = 2
TIC_0N = 3

# Instruction opcodes:
TIC_META       = 1
TIC_FAIL       = 2
TIC_MATCH      = 3
TIC_TEST       = 4
TIC_BRANCH     = 5
TIC_SKIP       = 6
TIC_SKIPTO     = 7
TIC_PUSH       = 8
TIC_PUSH_MATCH = 9
TIC_POP_MATCH  = 10
TIC_SWAP       = 11
TIC_CONCAT     = 12
TIC_JOIN       = 13
TIC_JTRUE      = 14
TIC_JFALSE     = 15
TIC_JUMP       = 16
TIC_CALL       = 17
TIC_PAUSE      = 18
TIC_HALT       = 19

class TagICElement(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def
#-class

class TagICMacro(TagICElement):
    """
    """
    __slots__ = [ '__factory', '__name', '__body' ]

    def __init__(self, factory, name, body = []):
        """
        """

        TagICElement.__init__(self)
        self.__factory = factory
        self.__name = name
        self.__body = body
    #-def

    def factory(self):
        """
        """

        return self.__factory
    #-def

    def name(self):
        """
        """

        return self.__name
    #-def

    def set_body(self, body):
        """
        """

        self.__body = body
    #-def

    def body(self):
        """
        """

        return self.__body
    #-def
#-class

class TagICLabel(TagICElement):
    """
    """
    __slots__ = [ '__factory', '__name', '__position' ]

    def __init__(self, factory, name, position = -1):
        """
        """

        TagICElement.__init__(self)
        self.__factory = factory
        self.__name = name
        self.__position = position
    #-def

    def factory(self):
        """
        """

        return self.__factory
    #-def

    def name(self):
        """
        """

        return self.__name
    #-def

    def set_position(self, position):
        """
        """

        self.__position = position
    #-def

    def position(self):
        """
        """

        return self.__position
    #-def
#-class

class TagICSymbolFactory(object):
    """
    """
    __slots__ = [ '__container', '__symbol_class' ]

    def __init__(self, container, symbol_class):
        """
        """

        self.__container = container
        self.__symbol_class = symbol_class
    #-def

    def __getattr__(self, value):
        """
        """

        if value.startswith("__") \
        or (value[0] != '_' and not value[0].isupper()):
            return object.__getattribute__(self, value)
        _assert(value[0] == '_' or value in self.__container,
            "Undefined symbol %s" % value
        )
        if value[0] == '_':
            value = value[1:]
        if value not in self.__container:
            self.__container[value] = self.__symbol_class(self, value)
        return self.__container[value]
    #-def

    def symbols(self):
        """
        """

        return self.__container
    #-def
#-class

class TagICSymbolTable(object):
    """
    """
    __slots__ = [ '__compiler', '__macro_factory', '__label_factory' ]

    def __init__(self, compiler):
        """
        """

        self.__compiler = compiler
        self.__macro_factory = TagICSymbolFactory({}, TagICMacro)
        self.__label_factory = TagICSymbolFactory({}, TagICLabel)
    #-def

    def compiler(self):
        """
        """

        return self.__compiler
    #-def

    def macro_factory(self):
        """
        """

        return self.__macro_factory
    #-def

    def label_factory(self):
        """
        """

        return self.__label_factory
    #-def
#-class

class TagICCompiler(object):
    """
    """
    __slots__ = [ '__symbol_table' ]

    def __init__(self):
        """
        """

        self.__symbol_table = TagICSymbolTable(self)
    #-def

    def define(self, name, *body):
        """
        """

        _assert(name[0].isupper(),
            "Macro name must start with upper case letter"
        )
        macros = self.__symbol_table.macro_factory().symbols()
        macros[name] = TagICMacro(
            self.__symbol_table, name, self.makecset(body)
        )
        return macros[name]
    #-def

    def compile(self, iclist):
        """
        """

        bt = {}
        code = []
        self.__compile_compute_addresses(iclist)
        self.__compile_inspect_branches(bt, iclist)
        self.__compile_make_branch_tables(bt, iclist)
        self.__compile_assemble(bt, code, iclist)
        return code
    #-def

    def __compile_compute_addresses(self, iclist):
        """
        """

        i = 0
        for inst in iclist:
            if isinstance(inst, TagICLabel):
                inst.set_position(i)
            elif isinstance(inst, tuple):
                if inst[0] > TIC_META:
                    i += 1
    #-def

    def __compile_inspect_branches(self, bt, iclist):
        """
        """

        for inst in iclist:
            if isinstance(inst, tuple) and inst[0] == TIC_BRANCH:
                bt[inst[3]] = {'table': {}, 'default': None, 'eof': None}
    #-def

    def __compile_make_branch_tables(self, bt, iclist):
        """
        """

        i = 0
        while i < len(iclist):
            if iclist[i] in bt:
                i = self.__compile_make_one_branch_table(bt, iclist, i)
                continue
            i += 1
    #-def

    def __compile_make_one_branch_table(self, bt, iclist, i):
        """
        """

        k = iclist[i]
        while i < len(iclist):
            if isinstance(iclist[i], tuple):
                if iclist[i][0] == TIC_NULL:
                    return i + 1
                _assert(iclist[i][0] == TIC_META,
                    "Invalid branch table definition"
                )
                if iclist[i][1] == TIC_SYMBOL:
                    _assert(iclist[i][3] not in bt[k]['table'],
                        "Ambiguous branch table definition"
                    )
                    bt[k]['table'][iclist[i][3]] = iclist[i][2]
                elif iclist[i][1] == TIC_SET:
                    for sym in iclist[i][3]:
                        _assert(sym not in bt[k]['table'],
                            "Ambiguous branch table definition"
                        )
                        bt[k]['table'][sym] = iclist[i][2]
                elif iclist[i][1] == TIC_RANGE:
                    _assert(ord(iclist[i][3][0]) <= ord(iclist[i][3][1]),
                        "%r > %r" % iclist[i][3]
                    )
                    for x in range(
                        ord(iclist[i][3][0]), ord(iclist[i][3][1]) + 1
                    ):
                        _assert(chr(x) not in bt[k]['table'],
                            "Ambiguous branch table definition"
                        )
                        bt[k]['table'][chr(x)] = iclist[i][2]
                elif iclist[i][1] == TIC_DEFAULT:
                    _assert(bt[k]['default'] is None,
                        "Ambiguous branch table definition"
                    )
                    bt[k]['default'] = iclist[i][2]
                elif iclist[i][1] == TIC_EOF:
                    _assert(bt[k]['eof'] is None,
                        "Ambiguous branch table definition"
                    )
                    bt[k]['eof'] = iclist[i][2]
                else:
                    _assert(False, "Invalid item in branch table definition")
            i += 1
        _assert(False, "End reached while processing branch table definition")
    #-def

    def __compile_assemble(self, bt, code, iclist):
        """
        """

        for inst in iclist:
            if not isinstance(inst, tuple):
                continue
            opcode, optype, qae, arg = inst
            if opcode <= TIC_META:
                continue
            elif opcode == TIC_FAIL:
                code.append(Fail())
            elif opcode in (TIC_MATCH, TIC_TEST, TIC_SKIP, TIC_SKIPTO):
                icls = TTT_MATCHER.get((opcode, optype, qae))
                # Fails if `icls' is None.
                if arg == TIC_UNUSED:
                    code.append(icls())
                else:
                    _assert(isinstance(arg, (str, list)) or iscallable(arg),
                        "Invalid instruction operand type"
                    )
                    code.append(icls(arg))
            elif opcode == TIC_BRANCH:
                t = bt.get(arg)
                # Fails if `t' is None.
                swt = {}
                for k in t['table']:
                    _assert(t['table'][k].position() >= 0,
                        "Unused label %s" % t['table'][k].name()
                    )
                    swt[k] = t['table'][k].position()
                d = t['default']
                if d is None:
                    d = len(code) + 1
                else:
                    _assert(d.position() >= 0, "Unused label %s" % d.name())
                    d = d.position()
                e = t['eof']
                if e is None:
                    e = len(code) + 1
                else:
                    _assert(e.position() >= 0, "Unused label %s" % e.name())
                    e = e.position()
                code.append(Branch(swt, d, e))
            elif opcode == TIC_PUSH:
                _assert(isinstance(arg, (str, list)),
                    "Invalid instruction operand type"
                )
                code.append(Push(arg))
            elif opcode == TIC_PUSH_MATCH:
                code.append(PushMatch())
            elif opcode == TIC_POP_MATCH:
                code.append(PopMatch())
            elif opcode == TIC_SWAP:
                code.append(Swap())
            elif opcode in (TIC_CONCAT, TIC_JOIN):
                if arg in (OT_REG, OT_STK):
                    arg = (arg, None)
                elif isinstance(arg, (str, list)):
                    arg = (OT_IMM, arg)
                else:
                    _assert(False, "Invalid instruction operand type")
                if qae in (OT_REG, OT_STK):
                    qae = (qae, None)
                elif isinstance(qae, (str, list)):
                    qae = (OT_IMM, qae)
                else:
                    _assert(False, "Invalid instruction operand type")
                if opcode == TIC_CONCAT:
                    code.append(Concat(arg, qae))
                else:
                    code.append(Join(arg, qae))
            elif opcode in (TIC_JTRUE, TIC_JFALSE, TIC_JUMP):
                _assert(arg.position() >= 0, "Unused label %s" % arg.name())
                if opcode == TIC_JTRUE:
                    code.append(JTrue(arg.position()))
                elif opcode == TIC_JFALSE:
                    code.append(JFalse(arg.position()))
                else:
                    code.append(Jump(arg.position()))
            elif opcode == TIC_CALL:
                _assert(iscallable(arg), "Invalid instruction operand type")
                code.append(Call(arg))
            elif opcode == TIC_PAUSE:
                code.append(Pause())
            elif opcode == TIC_HALT:
                code.append(Halt())
            else:
                _assert(False, "Invalid opcode %r" % opcode)
    #-def

    def symbol_table(self):
        """
        """

        return self.__symbol_table
    #-def

    @staticmethod
    def makecset(spec):
        """
        """

        cset = []
        for x in spec:
            if isinstance(x, (str, list)):
                for c in x:
                    if c not in cset:
                        _assert(isinstance(c, str) and len(c) == 1,
                            "Character expected"
                        )
                        cset.append(c)
            elif isinstance(x, tuple):
                _assert(ord(x[0]) <= ord(x[1]), "%r > %r" % x)
                for c in range(ord(x[0]), ord(x[1]) + 1):
                    if chr(c) not in cset:
                        cset.append(chr(c))
            elif isinstance(x, TagICMacro):
                for c in x.body():
                    if c not in cset:
                        cset.append(c)
            else:
                _assert(False, "Ill-formed spec")
        return cset
    #-def
#-class

# Translation table for matching instructions:
TTT_MATCHER = {
    (TIC_MATCH, TIC_SYMBOL, TIC_UNUSED): MatchSymbol,
    (TIC_MATCH, TIC_ANY, TIC_UNUSED): MatchAny,
    (TIC_MATCH, TIC_WORD, TIC_UNUSED): MatchWord,
    (TIC_MATCH, TIC_SET, TIC_UNUSED): MatchSet,
    (TIC_MATCH, TIC_RANGE, TIC_UNUSED): MatchRange,
    (TIC_MATCH, TIC_PRED, TIC_UNUSED): MatchIf,
    (TIC_MATCH, TIC_SYMBOL, TIC_1N): MatchAtLeastOneSymbol,
    (TIC_MATCH, TIC_SET, TIC_1N): MatchAtLeastOneFromSet,
    (TIC_MATCH, TIC_RANGE, TIC_1N): MatchAtLeastOneFromRange,
    (TIC_MATCH, TIC_PRED, TIC_1N): MatchAtLeastOne,
    (TIC_MATCH, TIC_SYMBOL, TIC_01): MatchAtMostOneSymbol,
    (TIC_MATCH, TIC_SET, TIC_01): MatchAtMostOneFromSet,
    (TIC_MATCH, TIC_RANGE, TIC_01): MatchAtMostOneFromRange,
    (TIC_MATCH, TIC_PRED, TIC_01): MatchAtMostOne,
    (TIC_MATCH, TIC_SYMBOL, TIC_0N): MatchManySymbols,
    (TIC_MATCH, TIC_SET, TIC_0N): MatchManyFromSet,
    (TIC_MATCH, TIC_RANGE, TIC_0N): MatchManyFromRange,
    (TIC_MATCH, TIC_ANY, TIC_0N): MatchAll,
    (TIC_MATCH, TIC_PRED, TIC_0N): MatchMany,
    (TIC_TEST, TIC_EOF, TIC_UNUSED): TestEof,
    (TIC_TEST, TIC_SYMBOL, TIC_UNUSED): TestSymbol,
    (TIC_TEST, TIC_SET, TIC_UNUSED): TestSet,
    (TIC_TEST, TIC_RANGE, TIC_UNUSED): TestRange,
    (TIC_TEST, TIC_PRED, TIC_UNUSED): TestIf,
    (TIC_SKIP, TIC_SYMBOL, TIC_UNUSED): SkipSymbol,
    (TIC_SKIP, TIC_ANY, TIC_UNUSED): SkipAny,
    (TIC_SKIP, TIC_SET, TIC_UNUSED): SkipSet,
    (TIC_SKIP, TIC_RANGE, TIC_UNUSED): SkipRange,
    (TIC_SKIP, TIC_PRED, TIC_UNUSED): SkipIf,
    (TIC_SKIP, TIC_SYMBOL, TIC_1N): SkipAtLeastOneSymbol,
    (TIC_SKIP, TIC_SET, TIC_1N): SkipAtLeastOneFromSet,
    (TIC_SKIP, TIC_RANGE, TIC_1N): SkipAtLeastOneFromRange,
    (TIC_SKIP, TIC_PRED, TIC_1N): SkipAtLeastOne,
    (TIC_SKIP, TIC_SYMBOL, TIC_01): SkipAtMostOneSymbol,
    (TIC_SKIP, TIC_SET, TIC_01): SkipAtMostOneFromSet,
    (TIC_SKIP, TIC_RANGE, TIC_01): SkipAtMostOneFromRange,
    (TIC_SKIP, TIC_PRED, TIC_01): SkipAtMostOne,
    (TIC_SKIP, TIC_SYMBOL, TIC_0N): SkipManySymbols,
    (TIC_SKIP, TIC_SET, TIC_0N): SkipManyFromSet,
    (TIC_SKIP, TIC_RANGE, TIC_0N): SkipManyFromRange,
    (TIC_SKIP, TIC_ANY, TIC_0N): SkipAll,
    (TIC_SKIP, TIC_PRED, TIC_0N): SkipMany,
    (TIC_SKIPTO, TIC_SYMBOL, TIC_UNUSED): SkipTo,
    (TIC_SKIPTO, TIC_SET, TIC_UNUSED): SkipToSet,
    (TIC_SKIPTO, TIC_RANGE, TIC_UNUSED): SkipToRange,
    (TIC_SKIPTO, TIC_PRED, TIC_UNUSED): SkipUntilNot
}

def makeinst(opcode, qtype, arg):
    """
    """

    if arg in (TIC_EOF, TIC_ANY):
        return (opcode, arg, qtype, TIC_UNUSED)
    elif isinstance(arg, str):
        _assert(len(arg) > 0, "Empty word")
        if len(arg) == 1:
            return (opcode, TIC_SYMBOL, qtype, arg)
        return (opcode, TIC_WORD, qtype, arg)
    elif isinstance(arg, list):
        _assert(len(arg) > 0, "Empty set")
        return (opcode, TIC_SET, qtype, TagICCompiler.makecset(arg))
    elif isinstance(arg, tuple):
        _assert(ord(arg[0]) <= ord(arg[1]), "%r > %r" % arg)
        return (opcode, TIC_RANGE, qtype, arg)
    elif iscallable(arg):
        return (opcode, TIC_PRED, qtype, arg)
    else:
        _assert(False, "Invalid type of argument")
#-def

# Instruction encoding format:
#
#   (opcode,  operand type,  quantifier/address/extra argument,  argument)
#
ACC        = OT_REG
STK        = OT_STK
SYMBOL     = lambda x, y: (TIC_META, TIC_SYMBOL, y, x)
SET        = lambda x, y: (TIC_META, TIC_SET, y, x)
RANGE      = lambda x, y, z: (TIC_META, TIC_RANGE, z, (x, y))
DEFAULT    = lambda x: (TIC_META, TIC_DEFAULT, x, TIC_UNUSED)
EOF        = lambda x: (TIC_META, TIC_EOF, x, TIC_UNUSED)
NULL       = (TIC_NULL, TIC_UNUSED, TIC_UNUSED, TIC_UNUSED)
FAIL       = (TIC_FAIL, TIC_UNUSED, TIC_UNUSED, TIC_UNUSED)
MATCH      = lambda x: makeinst(TIC_MATCH, TIC_UNUSED, x)
MATCH_ANY  = (TIC_MATCH, TIC_ANY, TIC_UNUSED, TIC_UNUSED)
MATCH_1N   = lambda x: makeinst(TIC_MATCH, TIC_1N, x)
MATCH_PLUS = MATCH_1N
MATCH_01   = lambda x: makeinst(TIC_MATCH, TIC_01, x)
MATCH_OPT  = MATCH_01
MATCH_0N   = lambda x: makeinst(TIC_MATCH, TIC_0N, x)
MATCH_MANY = MATCH_0N
MATCH_ALL  = (TIC_MATCH, TIC_ANY, TIC_0N, TIC_UNUSED)
TEST_EOF   = (TIC_TEST, TIC_EOF, TIC_UNUSED, TIC_UNUSED)
TEST       = lambda x: makeinst(TIC_TEST, TIC_UNUSED, x)
BRANCH     = lambda x: (TIC_BRANCH, TIC_UNUSED, TIC_UNUSED, x)
SKIP       = lambda x: makeinst(TIC_SKIP, TIC_UNUSED, x)
SKIP_ANY   = (TIC_SKIP, TIC_ANY, TIC_UNUSED, TIC_UNUSED)
SKIP_1N    = lambda x: makeinst(TIC_SKIP, TIC_1N, x)
SKIP_PLUS  = SKIP_1N
SKIP_01    = lambda x: makeinst(TIC_SKIP, TIC_01, x)
SKIP_OPT   = SKIP_01
SKIP_0N    = lambda x: makeinst(TIC_SKIP, TIC_0N, x)
SKIP_MANY  = SKIP_0N
SKIP_ALL   = (TIC_SKIP, TIC_ANY, TIC_0N, TIC_UNUSED)
SKIP_TO    = lambda x: makeinst(TIC_SKIPTO, TIC_UNUSED, x)
PUSH       = lambda x: (TIC_PUSH, TIC_UNUSED, TIC_UNUSED, x)
PUSH_MATCH = (TIC_PUSH_MATCH, TIC_UNUSED, TIC_UNUSED, TIC_UNUSED)
POP_MATCH  = (TIC_POP_MATCH, TIC_UNUSED, TIC_UNUSED, TIC_UNUSED)
SWAP       = (TIC_SWAP, TIC_UNUSED, TIC_UNUSED, TIC_UNUSED)
CONCAT     = lambda x, y: (TIC_CONCAT, TIC_UNUSED, y, x)
JOIN       = lambda x, y: (TIC_JOIN, TIC_UNUSED, y, x)
JTRUE      = lambda x: (TIC_JTRUE, TIC_UNUSED, TIC_UNUSED, x)
JFALSE     = lambda x: (TIC_JFALSE, TIC_UNUSED, TIC_UNUSED, x)
JUMP       = lambda x: (TIC_JUMP, TIC_UNUSED, TIC_UNUSED, x)
CALL       = lambda x: (TIC_CALL, TIC_UNUSED, TIC_UNUSED, x)
PAUSE      = (TIC_PAUSE, TIC_UNUSED, TIC_UNUSED, TIC_UNUSED)
HALT       = (TIC_HALT, TIC_UNUSED, TIC_UNUSED, TIC_UNUSED)
