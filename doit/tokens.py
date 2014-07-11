#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/tokens.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-06-29 00:17:16 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! tokens.\
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

class Token(object):
    """Base class for tokens.
    """
    __slots__ = [ 'lexer', 'position', 'type', 'value' ]

    def __init__(self, l, p, t, v = None):
        """Token(l, p, t[, v]) -> instance of Token

        Constructor. Initialize the token with lexer l, position p, type t,
        and value v.
        """

        self.lexer = l
        self.position = l.context.getipos(p)
        self.type = t
        self.value = v
    #-def

    def __eq__(self, rhs):
        """__eq__(rhs) -> bool

        type(rhs) is type(x) ==>
            x.__eq__(rhs) <==> x.type == rhs.type
        type(rhs) is type([]) ==>
            x.__eq__(rhs) <==> x == rhs[0] or x == rhs[1] or ...
        type(rhs) not in [type(x), type([])] ==>
            x.__eq__(rhs) <==> x.type == rhs
        """

        if type(rhs) is type(self):
            return self.type == rhs.type
        elif type(rhs) is type([]):
            for t in rhs:
                if self == t:
                    return True
            return False
        else:
            return self.type == rhs
        return False
    #-def

    def __ne__(self, rhs):
        """__ne__(rhs) -> bool

        x.__ne__(rhs) <==> not (x == rhs)
        """

        return not (self == rhs)
    #-def

    def __repr__(self):
        """__repr__() -> str

        Return the string representation of this token.
        """

        m = "Token(%s, %d, %d" % self.position
        if type(self.type) is type(Collection()):
            m += self.type.qname
        else:
            m += repr(self.type)
        if self.value is not None:
            m += ", %s" % repr(self.value)
        m += ")"
        return m
    #-def

    def __str__(self):
        """__str__() -> str

        Actually alias for repr.
        """

        return repr(self)
    #-def
#-class

class TIdentifier(Token):
    """Identifier token class.
    """
    __slots__ = [ '__is_cmd', '__is_var', '__is_varuse', '__is_clearname' ]

    def __init__(self, lexer, pos, wl):
        """TIdentifier(lexer, pos, wl) -> instance of Token

        Constructor.
        """

        Token.__init__(self, lexer, pos, TokenType.Identifier, wl)
        self.__verify()
        self.__is_varuse = (len(self.value) == 1 and self.value[0] == '$')
        self.__is_clearname = ([x for x in self.value if x[0] == '$'] == [])
    #-def

    def __verify(self):
        """__verify()

        Check if identifier name is valid.
        """

        snovars = ''.join([x for x in self.value if x[0] != '$'])
        have_dash = '-' in snovars
        have_score = '_' in snovars
        if have_dash and have_score:
            parse_error(self.lexer.context, self.position,
                " You can use either '-' (for command names) or '_'"\
                " (for variable names) in identifier '%s'."\
                % ''.join(wordlist)
            )
        have_ucletter = ([x for x in snovars if x.isupper()] != [])
        if have_dash and have_ucletter:
            parse_error(self.lexer.context, self.position,
                "Upper case letters in command names are not allowed."
            )
        self.__is_cmd = have_dash or not (have_score or have_ucletter)
        self.__is_var = have_score or have_ucletter or not have_dash
    #-def

    def is_cmd(self):
        """is_cmd() -> bool

        Return True if identifier contains only lower-case letters, digits, or
        '-'.
        """

        return self.__is_cmd
    #-def

    def is_var(self):
        """is_var() -> bool

        Return True if identifier contains only letters, digits, or '_'.
        """

        return self.__is_var
    #-def

    def is_varuse(self):
        """is_varuse() -> bool

        Return True if identifier is of the form '$[A-Za-z_][0-9A-Za-z_]*'.
        """

        return self.__is_varuse
    #-def

    def is_clearname(self):
        """is_clearname() -> bool

        Return True if identifier do not contains $-parts.
        """

        return self.__is_clearname
    #-def
#-class

class TInt(Token):
    """Integer token class.
    """
    __slots__ = []

    def __init__(self, lexer, pos, val):
        """TInt(lexer, pos, val) -> instance of Token

        Constructor.
        """

        Token.__init__(self, lexer, pos, TokenType.Int, val)
    #-def
#-class

class TMultiInt(Token):
    """Multipart integer token class.
    """
    __slots__ = []

    def __init__(self, lexer, pos, val):
        """TMultiInt(lexer, pos, val) -> instance of Token

        Constructor.
        """

        Token.__init__(self, lexer, pos, TokenType.MultiInt, val)
    #-def
#-class

class TFloat(Token):
    """Floating point number token class.
    """
    __slots__ = []

    def __init__(self, lexer, pos, val):
        """TFloat(lexer, pos, val) -> instance of Token

        Constructor.
        """

        Token.__init__(self, lexer, pos, TokenType.Float, val)
    #-def
#-class

class TSqStr(Token):
    """Single quoted string token class.
    """
    __slots__ = []

    def __init__(self, lexer, pos, val):
        """TSqStr(lexer, pos, val) -> instance of Token

        Constructor.
        """

        Token.__init__(self, lexer, pos, TokenType.SqStr, val)
    #-def
#-class

class TDqStr(Token):
    """Double quoted string token class.
    """
    __slots__ = []

    def __init__(self, lexer, pos, val, vp):
        """TDqStr(lexer, pos, val, vp) -> instance of Token

        Constructor.
        """

        Token.__init__(self, lexer, pos, TokenType.DqStr, (val, vp))
    #-def
#-class

class TPath(Token):
    """Path token class.
    """
    __slots__ = []

    def __init__(self, lexer, pos, val, vp):
        """TPath(lexer, pos, val, vp) -> instance of Token

        Constructor.
        """

        Token.__init__(self, lexer, pos, TokenType.Path, (val, vp))
    #-def
#-class

class TBrace(Token):
    """Base class for brace tokens.
    """
    __slots__ = []

    def __init__(self, lexer, pos, type, val):
        """TBrace(lexer, pos, type, val) -> instance of Token

        Constructor.
        """

        check(lexer.context, type in TokenType.Brace,
            "The type of token must be brace."
        )
        Token.__init__(self, lexer, pos, type, val)
    #-def

    def left(self):
        """left() -> str

        Return left brace.
        """

        return self.value[0]
    #-def

    def right(self):
        """right() -> str

        Return right brace.
        """

        return self.value[1]
    #-def

    def group(self):
        """group() -> str

        Return group name.
        """

        return self.value[2]
    #-def
#-class

class TLeftBrace(TBrace):
    """Left brace token class.
    """
    __slots__ = []

    def __init__(self, lexer, pos, val):
        """TLeftBrace(lexer, pos, val) -> instance of Token

        Constructor.
        """

        TBrace.__init__(self, lexer, pos, TokenType.Brace.Left, val)
    #-def
#-class

class TRightBrace(TBrace):
    """Right brace token class.
    """
    __slots__ = []

    def __init__(self, lexer, pos, val):
        """TRightBrace(lexer, pos, val) -> instance of Token

        Constructor.
        """

        TBrace.__init__(self, lexer, pos, TokenType.Brace.Right, val)
    #-def
#-class

class TOperator(Token):
    """Operator token class.
    """
    __slots__ = []
    OTYPE_TO_TTYPE = {
        Operator.Prefix:   TokenType.Operator.Unary.Prefix,
        Operator.Postfix:  TokenType.Operator.Unary.Postfix,
        Operator.Left:     TokenType.Operator.Binary.Left,
        Operator.Right:    TokenType.Operator.Binary.Right,
        Operator.NoAssoc:  TokenType.Operator.Binary.NoAssoc
    }

    def __init__(self, lexer, pos, invoker, otype):
        """TOperator(lexer, pos, invoker, otype) -> instance of Token

        Constructor.
        """

        check(lexer.context, otype in self.OTYPE_TO_TTYPE.keys(),
            "Invalid type of operator."
        )
        Token.__init__(self, lexer, pos, self.OTYPE_TO_TTYPE[otype], invoker)
    #-def
#-class
