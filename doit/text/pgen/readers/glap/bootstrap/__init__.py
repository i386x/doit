#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/bootstrap/__init__.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-12-19 02:04:45 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
GLAP bootstrap.\
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

def make_location(context, loc = -1):
    """
    """

    istream = context.istream
    if loc < 0:
        loc = istream.pos
    s = istream.data[0 : loc]
    lineno = s.count('\n') + 1
    if lineno > 1:
        s = s.split('\n')[-1]
    colno = len(s) + 1
    return istream.name, lineno, colno
#-def

class GlapLexError(ParsingError):
    """
    """
    __slots__ = []

    def __init__(self, context, detail):
        """
        """

        name, lineno, colno = make_location(context)
        ParsingError.__init__(self, "In <%s> at [%d:%d]: %s" % (
            name, lineno, colno, detail
        ))
    #-def
#-class

class GlapSyntaxError(ParsingError):
    """
    """
    __slots__ = []

    def __init__(self, context, detail):
        """
        """

        loc = context.lexer.token.location() if context.lexer.token else -1
        name, lineno, colno = make_location(context, loc)
        ParsingError.__init__(self, "In <%s> at [%d:%d]: %s" % (
            name, lineno, colno, detail
        ))
    #-def
#-class

class GlapContext(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        self.stream = None
        self.lexer = None
        self.parser = None
        self.actions = None
        self.env = None
        self.processor = None
    #-def
#-class

class GlapStream(object):
    """
    """
    __slots__ = [ 'name', 'data', 'pos', 'size' ]

    def __init__(self, context, name, s):
        """
        """

        context.stream = self
        self.context = context
        self.name = name
        self.data = s
        self.pos = 0
        self.size = len(s)
    #-def

    def peek(self, n):
        """
        """

        return self.data[self.pos : self.pos + n]
    #-def

    def next(self, n = 1):
        """
        """

        self.pos += n
    #-def

    def match(self, p):
        """
        """

        if self.peek(len(p)) != p:
            raise GlapLexError(self, "Expected %r" % p)
        self.pos += len(p)
        return p
    #-def

    def matchset(self, set):
        """
        """

        if self.pos < self.size and self.data[self.pos] in set:
            self.pos += 1
            return self.data[self.pos - 1]
        raise GlapLexError(self, "Expected one of [%s]" % repr(set)[1:-1])
    #-def

    def matchif(self, f, fname):
        """
        """

        if self.pos < self.size and f(self.data[self.pos]):
            self.pos += 1
            return self.data[self.pos - 1]
        raise GlapLexError(self, "Expected %s" % fname)
    #-def

    def matchmany(self, set):
        """
        """

        p = self.pos
        while self.pos < self.size and self.data[self.pos] in set:
            self.pos += 1
        return self.data[p : self.pos]
    #-def

    def matchmanyif(self, f):
        """
        """

        p = self.pos
        while self.pos < self.size and f(self.data[self.pos]):
            self.pos += 1
        return self.data[p : self.pos]
    #-def

    def matchplus(self, set):
        """
        """

        m = self.matchset(set)
        return "%s%s" % (m, self.matchmany(set))
    #-def

    def matchplusif(self, f, fname):
        """
        """

        m = self.matchif(f, fname)
        return "%s%s" % (m, self.matchmanyif(f))
    #-def

    def matchopt(self, set, default):
        """
        """

        if self.pos < self.size and self.data[self.pos] in set:
            self.pos += 1
            return self.data[self.pos - 1]
        return default
    #-def

    def matchoptif(self, f, default):
        """
        """

        if self.pos < self.size and f(self.data[self.pos]):
            self.pos += 1
            return self.data[self.pos - 1]
        return default
    #-def

    def matchn(self, set, n):
        """
        """

        p = self.pos
        while n > 0 and self.pos < self.size and self.data[self.pos] in set:
            self.pos += 1
            n -= 1
        if n > 0:
            raise GlapLexError(self, "Expected one of [%s]" % repr(set)[1:-1])
        return self.data[p : self.pos]
    #-def

    def matchnif(self, f, n, fname):
        """
        """

        p = self.pos
        while n > 0 and self.pos < self.size and f(self.data[self.pos]):
            self.pos += 1
            n -= 1
        if n > 0:
            raise GlapLexError(self, "Expected %s" % fname)
        return self.data[p : self.pos]
    #-def
#-class

class GlapParserActions(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        self.actions = {
          'start': self.on_start,
          'module': self.on_module
        }
    #-def

    def on_start(self, context, module):
        """
        """

        return module
    #-def

    def on_module(self, context, loc, name, module_units):
        """
        """

        node = DefModule(name.value(), module_units)
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def run(self, action, context, *args):
        """
        """

        if action not in self.actions:
            raise ParsingError("Action %r does not exist" % action)
        return self.actions[action](context, *args)
    #-def
#-class

class GlapReader(Reader):
    """
    """
    __slots__ = []

    def read(self, source, *args, **opts):
        """
        """

        data, name = self.load_source(source, **opts)
        if data is None:
            return None
        ctx = GlapContext()
        GlapStream(ctx, name, data)
        GlapLexer(ctx)
        GlapParser(ctx)
        GlapActions(ctx)
    #-def
#-class

def get_reader_class():
    """
    """

    return GlapReader
#-def
