#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/utils.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-02-27 18:26:58 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! utilities.\
"""

__license__ = """\
Copyright (c) 2014 Jiří Kučera.

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

import os

def sys2path(p):
    """sys2path(p) -> str

    Return a system path p converted to DoIt! universal path.
    """

    d = os.path.dirname(p)
    b = os.path.basename(p)
    if d == '':
        return b
    d = d.replace(os.sep, '/').replace(os.pardir, '..').replace(os.curdir, '.')
    return "%s/%s" % (d, b)
#-def

def path2sys(p):
    """path2sys(p) -> str

    Return a universal DoIt! path p converted to system path. Universal DoIt!
    path can be only relative.
    """

    if p.startswith("./"):
        p = p[2:]
    def f(x):
        if x == '.':
            return os.curdir
        elif x == '..':
            return os.pardir
        return x
    return os.path.join(*[f(x) for x in p.split('/')])
#-def

class Input(object):
    """Base class for input reader.
    """
    __slots__ = [ 'name', 'line', '__buffer' ]

    def __init__(self, name):
        """Input() -> instance of Input

        Constructor.
        """

        self.name = name
        self.line = 0
        self.__buffer = ""
    #-def

    def getc(self):
        """getc() -> str

        Return one character from buffer if there is one. If not, then read and
        return one character from attached source.
        """

        if self.__buffer:
            c = self.__buffer[0]
            self.__buffer = self.__buffer[1:]
            return c
        return self.getchar()
    #-def

    def ungets(self, s):
        """ungets(s)

        Return characters s back into the buffer.
        """

        self.__buffer = s + self.__buffer
    #-def

    def getchar(self):
        """getchar() -> str

        Return one character from attached source or empty string if all
        characters were consumed. To be implemented by user.
        """

        raise NotImplementedError
    #-def
#-class

class StrInput(Input):
    """Input from string.
    """
    __slots__ = [ '__s', '__l', '__i' ]

    def __init__(self, s, name):
        """StrInput(s, name) -> instance of Input

        Constructor. Attach string s to input.
        """

        Input.__init__(self, name)
        self.__s = s
        self.__l = len(s)
        self.__i = 0
    #-def

    def getchar(self):
        """getchar() -> str

        Return the character at the current position in string and move to the
        next position. If the current position is the end of attached string,
        the empty string is returned.
        """

        if self.__i < self.__l:
            c = self.__s[self.__i]
            self.__i += 1
            return c
        return ""
    #-def
#-class

class FileInput(Input):
    """Input from file.
    """
    __slots__ = [ '__fd' ]

    def __init__(self, fd):
        """FileInput(fd) -> instance of Input

        Constructor. Attach file object fd to input.
        """

        Input.__init__(self, fd.name)
        self.__fd = fd
    #-def

    def getchar(self):
        """getchar() -> str

        Read one character from the attached file and return it or return the
        empty string if all characters were consumend.
        """

        return self.__fd.read(1)
    #-def
#-class

class Token(object):
    """Base class for tokens.
    """
    __slots__ = [ 'type', 'value', 'line' ]

    def __init__(self, t, v, l):
        """Token(t, v, l) -> instance of Token

        Constructor. Initialize the token with type t, value v, and line number
        l.
        """

        self.type = t
        self.value = v
        self.line = l
    #-def

    def __eq__(self, rhs):
        """__eq__(rhs) -> bool

        Return True if this token and rhs are of the same type.
        """

        return self.type == rhs.type
    #-def

    def __ne__(self, rhs):
        """__ne__(rhs) -> bool

        Return True if this token and rhs have different types.
        """

        return self.type != rhs.type
    #-def

    def __repr__(self):
        """__repr__() -> str

        Return the string representation of this token.
        """

        return "Token(%s, %s)" % (self.type, self.value)
    #-def

    def __str__(self):
        """__str__() -> str

        Actually alias for repr.
        """

        return repr(self)
    #-def
#-class

class Lexer(object):
    """Base class for lexical analyzer.
    """
    __slots__ = [ 'input', 'current', 'last' ]

    def __init__(self, input):
        """Lexer(input) -> instance of Lexer

        Constructor. Initialize lexer with given input.
        """

        self.input = input
        self.current = None
        self.last = None
    #-def

    def peek(self):
        """peek() -> instance of Token

        Return the current token at input or None if end was reached.
        """

        if self.current is not None:
            return self.current
        self.current = self.scan()
        return self.current
    #-def

    def next(self):
        """next()

        Move to the next token keeping the last one.
        """

        if self.current is not None:
            self.last = self.current
        self.current = self.scan()
    #-def

    def scan(self):
        """scan() -> instance of Token

        User defined scanning routine. Return the next token from input or None
        if end of input was reached.
        """

        raise NotImplementedError
    #-def
#-class

class Parser(object):
    """Parser combinator base class.
    """
    __slots__ = []

    def __init__(self):
        """Parser() -> instance of Parser

        Constructor.
        """

        pass
    #-def

    def parse(self, source, result):
        """parse(source, result)

        Analyze and parse source and update the result of parsing.
        """

        raise NotImplementedError
    #-def

    def predict(self):
        """predict() -> list of instances of Token

        Return the Predict(A -> x) set of this (A -> x) parser.
        """

        raise NotImplementedError
    #-def

    def __add__(self, rhs):
        """__add__(rhs) -> instance of Concat

        Allow to concatenate parsers using an operator for addition.
        """

        if self.__class__ is Concat:
            self.append(rhs)
            return self
        return Concat(self, rhs)
    #-def

    def __or__(self, rhs):
        """__or__(rhs) -> instance to Alternative

        Allow to make a decision table using an operator for bitwise addition.
        """

        if self.__class__ is Alternative:
            self.merge(rhs)
            return self
        return Alternative(self, rhs)
    #-def
#-class

class Symbol(Parser):
    """Parser combinator which recognizes one terminal symbol.
    """
    __slots__ = [ '__symbol' ]

    def __init__(self, symbol):
        """Symbol(symbol) -> instance of Parser

        Constructor.
        """

        Parser.__init__(self)
        self.__symbol = symbol
    #-def

    def parse(self, source, result):
        """parse(source, result)

        Parse one symbol at input begining.
        """

        symbol = source.peek()
        if symbol != self.__symbol:
            raise ParseError(source, "%s expected" % str(self.__symbol))
        result.make_leaf(symbol)
        source.next()
    #-def

    def predict(self):
        """predict() -> list of instances of Token

        Return the Predict(A -> x) set of this (A -> x) parser.
        """

        return [self.__symbol]
    #-def
#-class

class Concat(Parser):
    """Parser combinator which keeps a list of parsers which are applied
       consecutively to string to be parsed.
    """
    __slots__ = [ 'parsers' ]

    def __init__(self, p1, p2):
        """Concat(p1, p2) -> instance of Parser

        Constructor. Stores p1 and p2 to the list of parsers.
        """

        Parser.__init__(self)
        self.parsers = [p1, p2]
    #-def

    def parse(self, state):
        """parse(state)

        Consecutively apply parsers from the list of parsers to state.
        """

        for p in self.parsers:
            p.parse(state)
    #-def

    def predict(self):
        """predict() -> list of instances of Token

        Return the Predict(A -> x) set of this (A -> x) parser.
        """

        return self.parsers[0].predict()
    #-def
#-class

class Alternative(Parser):
    """
    """
    __slots__ = [ '__choices' ]

    def __init__(self, p1, p2):
        """
        """

        Parser.__init__(self)
        self.__choices = {}
        self.merge(p1)
        self.merge(p2)
    #-def

    def merge(self, parser):
        """
        """

        for symbol in parser.predict():
            if self.__choices.get(symbol, None) is not None:
                raise ParserConstructionError(\
                    "Nondeterminism detected at %s while constructing "\
                    "the parser" % str(symbol)\
                )
            self.__choices[symbol] = parser
    #-def

    def parse(self, source, result):
        """
        """

        symbol = source.peek()
        parser = self.__choices.get(symbol, None)
        if parser is None:
            raise ParseError(state, "Unexpected symbol %s" % str(symbol))
        parser.parse(source, result)
    #-def

    def predict(self):
        """
        """

        return list(self.choices.keys())
    #-def
#-class

class ArgParser(Parser):
    """Argument parser base class.
    """
    __slots__ = []

    def __init__(self):
        """ArgParser() -> instance of ArgParser

        Constructor.
        """

        Parser.__init__(self)
    #-def

    def parse(self, ctx):
        """parse(ctx) -> result

        Validate and parse argument list args according to parser definition.
        """

        raise NotImplementedError
    #-def

    def __radd__(self, rhs):
        """__radd__(rhs) -> instance of ArgParser

        Concatenate argument parser lhs with argument parser rhs.
        """

        return _seq(self, rhs)
    #-def
#-class

class _cmd(ArgParser):
    """
    """

    def parse(self, state):
        """
        """

        if state.result.get(0, None) is not None:
            raise ArgParserError()
        state.result[0] = self.__name
    #-def
#-class

class _separg(ArgParser):
    """
    """
#-class

class _seq(ArgParser):
    """
    """
#-class
