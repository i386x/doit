#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/bootstrap/parser.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-11 10:19:52 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
GLAP lexer and parser (bootstrap version).\
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
from doit.text.pgen.models.token import Token
from doit.text.pgen.readers.glap.bootstrap import GlapLexError, GlapSyntaxError

GLAP_ID    = 1
GLAP_INT   = 2
GLAP_FLOAT = 3
GLAP_STR   = 4

GLAP_INT_DEC = 10
GLAP_INT_OCT = 8
GLAP_INT_HEX = 16

class GlapToken(Token):
    """
    """
    NAMES = {
      GLAP_ID: "identifier",
      GLAP_INT: "int literal",
      GLAP_FLOAT: "float literal",
      GLAP_STR: "string literal"
    }
    __slots__ = []

    def __init__(self, ttype, position, *data):
        """
        """

        Token.__init__(self, ttype, position, data)
    #-def

    def position(self):
        """
        """

        return self.data[0]
    #-def

    def value(self, evaluate = False):
        """
        """

        tt = self.ttype
        data = self.data[1]
        if tt in (GLAP_ID, GLAP_STR):
            return data[0]
        elif tt == GLAP_INT:
            if evaluate:
                base, sval = data
                return int(sval, base)
            return data
        elif tt == GLAP_FLOAT:
            if evaluate:
                sval, fpart, epart = data
                if fpart:
                    sval += ".%s" % fpart
                if epart:
                    sval += "E%s" % epart
                return float(sval)
            return data
        return tt
    #-def

    @classmethod
    def tokname(cls, ttype):
        """
        """

        if isinstance(ttype, str):
            return repr(ttype)
        return cls.NAMES.get(ttype, "<unknown>")
    #-def
#-class

class Symbols(object):
    """
    """
    __slots__ = [ 'symbols' ]

    def __init__(self, *symbols):
        """
        """

        self.symbols = {}
        for symbol in symbols:
            self.add_symbol(symbol)
    #-def

    def add_symbol(self, symbol):
        """
        """

        node = self.symbols
        i = 0
        while i < len(symbol):
            if symbol[i] not in node:
                node[symbol[i]] = {}
            node = node[symbol[i]]
            i += 1
        if self not in node:
            node[self] = symbol
    #-def

    def scan_symbol(self, c, stream):
        """
        """

        p = stream.pos
        node = self.symbols
        while c in node:
            node = node[c]
            stream.next()
            c = stream.peek(1)
        _assert(self in node,
            "Symbol %r cannot be retrieved" % stream.data[p : stream.pos]
        )
        _assert(node[self] == stream.data[p : stream.pos],
            "GlapLexer.SYMBOLS: %r != %r" % (
                node[self], stream.data[p : stream.pos]
            )
        )
        return GlapToken(node[self], p)
    #-def
#-class

class GlapLexer(object):
    """
    """
    WS = "\n "
    ASCIICHAR = lambda c: ord(' ') <= ord(c) and ord(c) <= ord('~')
    COMMENTCHAR = lambda c: GlapLexer.ASCIICHAR(c) or ord(c) >= 128
    SOURCECHAR = lambda c: c == '\n' or GlapLexer.COMMENTCHAR(c)
    ODIGIT = "01234567"
    DIGIT = "0123456789"
    XDIGIT = "%sABCDEFabcdef" % DIGIT
    IDCHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
    IDCHARNUM = "%s%s" % (DIGIT, IDCHAR)
    KEYWORDS = [
      "break",
      "case", "catch", "continue",
      "default", "define", "defmacro", "do",
      "elif", "else", "end", "eps",
      "finally", "for", "foreach",
      "grammar",
      "if", "in",
      "module",
      "of",
      "return",
      "throw", "try",
      "while"
    ]
    STRCHAR = lambda c: GlapLexer.COMMENTCHAR(c) and c not in ('"', '\\')
    ESCAPECHAR2CHAR = {
      'a': '\a',
      'b': '\b',
      't': '\t',
      'n': '\n',
      'v': '\v',
      'f': '\f',
      'r': '\r',
      '"': '"',
      '\'': '\'',
      '\\': '\\'
    }
    SYMBOLS = Symbols(
      # Parenthesis:
      '(', '$(', ')', '[', ']', '{', '}',
      # Punctation:
      ',', ';',
      # Accessors:
      '.', ':',
      # Decorators:
      '$', '#', '...', '`',
      # Operators:
      # - grammar rule builders:
      '->', '..', '?', '\'',
      # - assignments:
      '=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '&&=',
        '||=', '.=', '++=', '~~=',
      # - logical:
      '||', '&&', '!',
      # - relational:
      '<', '>', '<=', '>=', '==', '!=', '===',
      # - bitwise:
      '|', '&', '^', '<<', '>>', '~',
      # - additive:
      '+', '-', '++', '~~',
      # - multiplicative:
      '*', '/', '%',
      # - hashmap item builders:
      '=>'
    )
    __slots__ = [ 'context', 'token' ]

    def __init__(self, context):
        """
        """

        context.lexer = self
        self.context = context
        self.token = None
    #-def

    def peek(self):
        """
        """

        if self.token is None:
            self.next()
        return self.token
    #-def

    def asserteof(self):
        """
        """

        if self.peek():
            raise GlapSyntaxError(self.context, "Expected end of input")
    #-def

    def test(self, *ts):
        """
        """

        if self.peek():
            return self.token.ttype in ts
        return None in ts
    #-def

    def match(self, *ts):
        """
        """

        if not self.peek() or self.token.ttype not in ts:
            if not ts:
                what = "Unexpected token"
            else:
                what = "Expected %s" % GlapToken.tokname(ts[0])
                i, l, n = 1, len(ts) - 1, len(ts)
                while i < n:
                    t = GlapToken.tokname(ts[i])
                    what += (", %s" if i < l else " or %s") % t
                    i += 1
            raise GlapSyntaxError(self.context, what)
        t = self.token
        self.next()
        return t
    #-def

    def next(self):
        """
        """

        stream = self.context.stream
        self.skip_spaces(stream)
        c = stream.peek(1)
        if c == "":
            self.token = None
        elif c in self.IDCHAR:
            self.token = self.scan_ID(c, stream)
        elif c in self.DIGIT:
            self.token = self.scan_NUMBER(c, stream)
        elif c == '"':
            self.token = self.scan_STR(c, stream)
        elif c in self.SYMBOLS.symbols:
            self.token = self.SYMBOLS.scan_symbol(c, stream)
        else:
            raise GlapLexError(self.context, "Unexpected symbol %r" % c)
    #-def

    def skip_spaces(self, stream):
        """
        """

        # ( [ ' ', '\n' ]* | "--" COMMENTCHAR* )*
        while True:
            p = stream.pos
            stream.matchmany(self.WS)
            self.skip_comment(stream)
            if p < stream.pos:
                continue
            break
    #-def

    def skip_comment(self, stream):
        """
        """

        if stream.peek(2) != "--":
            return
        stream.next(2)
        stream.matchmanyif(GlapLexer.COMMENTCHAR)
    #-def

    def scan_ID(self, c, stream):
        """
        """

        # IDCHAR IDCHARNUM*
        p = stream.pos
        m = stream.matchmany(self.IDCHARNUM)
        if m in self.KEYWORDS:
            return GlapToken(m, p)
        return GlapToken(GLAP_ID, p, m)
    #-def

    def scan_NUMBER(self, c, stream):
        """
        """

        # ( (DIGIT - '0') DIGIT* | '0' )
        #   ( '.' DIGIT+ )?
        #   ( ( 'E' | 'e' ) ( '+' | '-' )? DIGIT+ )?
        # '0' ODIGIT*
        # '0' ( 'X' | 'x' ) XDIGIT+
        p = stream.pos
        stream.next()
        if c != '0' or stream.peek(1) in [ '.', 'E', 'e' ]:
            # Non-zero digit, or zero-only, case - match integral part:
            ipart = "%s%s" % (c, stream.matchmany(self.DIGIT))
            c = stream.peek(1)
            if c not in [ '.', 'E', 'e' ]:
                return GlapToken(GLAP_INT, p, GLAP_INT_DEC, ipart)
            # Floating-point number - try match fraction part:
            fpart, epart = "", ""
            if c == '.':
                stream.next()
                fpart = stream.matchplus(self.DIGIT)
                # Repeek:
                c = stream.peek(1)
            # Try match exponent part:
            if c in [ 'E', 'e' ]:
                stream.next()
                epart = stream.matchopt(['+', '-'], '+')
                epart += stream.matchplus(self.DIGIT)
            return GlapToken(GLAP_FLOAT, p, ipart, fpart, epart)
        # '0' - octal or hexadecimal number:
        if stream.peek(1) in [ 'X', 'x' ]:
            stream.next()
            return GlapToken(
                GLAP_INT, p, GLAP_INT_HEX, stream.matchplus(self.XDIGIT)
            )
        return GlapToken(
            GLAP_INT, p, GLAP_INT_OCT, "0" + stream.matchmany(self.ODIGIT)
        )
    #-def

    def scan_STR(self, c, stream):
        """
        """

        # '"' ( '\\' ESCAPE_SEQUENCE | STRCHAR )* '"'
        p = stream.pos
        stream.next()
        s = ""
        while True:
            c = stream.peek(1)
            if c in ("", '"'):
                break
            elif c == '\\':
                stream.next()
                s += self.scan_ESCAPE_SEQUENCE(stream.peek(1), stream)
            elif GlapLexer.STRCHAR(c):
                s += c
                stream.next()
            else:
                raise GlapLexError(self.context, "Unexpected symbol %r" % c)
        stream.match('"')
        return GlapToken(GLAP_STR, p, s)
    #-def

    def scan_ESCAPE_SEQUENCE(self, c, stream):
        """
        """

        # ESCAPECHAR
        # ODIGIT ODIGIT? ODIGIT?
        # 'x' XDIGIT{2}
        # 'u' XDIGIT{4}
        if c == "":
            raise GlapLexError(self.context, "Unexpected end of input")
        elif c in self.ESCAPECHAR2CHAR:
            stream.next()
            return self.ESCAPECHAR2CHAR[c]
        elif c in self.ODIGIT:
            x = stream.matchset(self.ODIGIT)
            x += stream.matchopt(self.ODIGIT, "")
            x += stream.matchopt(self.ODIGIT, "")
            return chr(int(x, 8))
        elif c == 'x':
            stream.next()
            return chr(int(stream.matchn(self.XDIGIT, 2), 16))
        elif c == 'u':
            stream.next()
            return chr(int(stream.matchn(self.XDIGIT, 4), 16))
        raise GlapLexError(self.context, "Invalid symbol (%r) after '\\'" % c)
    #-def
#-class

class Operator(object):
    """
    """
    __slots__ = [ 'level', 'name', 'mask', 'lbp', 'rbp' ]

    def __init__(self, level, lbp, name, rbp):
        """
        """

        self.level = level
        self.name = name
        slbp = "_" if lbp >= 0 else ""
        srbp = "_" if rbp >= 0 else ""
        self.mask = "%s%s%s" % (slbp, name or " ", srbp)
        self.lbp = lbp
        self.rbp = rbp
    #-def
#-class

class OperatorTable(object):
    """
    """
    __slots__ = [ 'prefixops', 'operators', 'atomlevel', 'opts' ]

    def __init__(self, *spec, **opts):
        """
        """

        self.prefixops = {}
        self.operators = {}
        self.atomlevel = -1
        self.opts = opts
        for x in spec:
            self.add_operator(*x)
    #-def

    def add_operator(self, level, lbp, name, rbp):
        """
        """

        if lbp < 0 and rbp < 0:
            if level > self.atomlevel:
                self.atomlevel = level
            return
        elif lbp < 0:
            _assert(name not in self.prefixops,
                "%r has been already added to operator table" % name
            )
            self.prefixops[name] = Operator(level, lbp, name, rbp)
            if rbp > self.atomlevel:
                self.atomlevel = rbp
            return
        _assert(name not in self.operators,
            "%r has been already added to operator table" % name
        )
        self.operators[name] = Operator(level, lbp, name, rbp)
        if lbp > self.atomlevel:
            self.atomlevel = lbp
        if rbp > self.atomlevel:
            self.atomlevel = rbp
    #-def

    def peekprefix(self, lexer):
        """
        """

        t = lexer.peek()
        if not t:
            return None
        return self.prefixops.get(t.ttype, None)
    #-def

    def peekoperator(self, lexer):
        """
        """

        t = lexer.peek()
        if not t:
            return None
        o = self.operators.get(t.ttype, None)
        if o:
            return o
        if t.ttype in self.opts.get('first', []):
            return self.operators.get("", None)
        return None
    #-def

    def operandfollows(self, lexer):
        """
        """

        t = lexer.peek()
        return t and t.ttype in self.opts.get('first', [])
    #-def
#-class

def expression_parser(*spec, **opts):
    """
    """

    def expression_parser_installer(method):
        method.optab = OperatorTable(*spec, **opts)
        return method
    return expression_parser_installer
#-def

class GlapParser(object):
    """
    """
    __slots__ = [ 'context' ]

    def __init__(self, context):
        """
        """

        context.parser = self
        self.context = context
    #-def

    def parse(self):
        """
        """

        # start -> module
        lexer = self.context.lexer
        actions = self.context.actions
        module = self.parse_module(lexer, actions)
        lexer.asserteof()
        return actions.run("start", self.context, module)
    #-def

    def parse_module(self, lexer, actions):
        """
        """

        # module -> "module" ID module_unit* "end"
        p = lexer.match("module").position()
        name = lexer.match(GLAP_ID)
        module_units = []
        while lexer.peek() and not lexer.test("end"):
            module_units.extend(self.parse_module_unit(lexer, actions))
        lexer.match("end")
        return actions.run("module", self.context, p, name, module_units)
    #-def

    def parse_module_unit(self, lexer, actions):
        """
        """

        # module_unit -> module | grammar | command
        t = lexer.peek()
        if not t:
            raise GlapSyntaxError(self.context, "Unexpected end of input")
        t = t.ttype
        if t == "module":
            return [self.parse_module(lexer, actions)]
        elif t == "grammar":
            return [self.parse_grammar(lexer, actions)]
        return actions.run(
            "unwrap", self.context, self.parse_command(lexer, actions)
        )
    #-def

    def parse_grammar(self, lexer, actions):
        """
        """

        # grammar -> "grammar" ID grammar_type_spec?
        #              ( rule | "." command )*
        #            "end"
        p = lexer.match("grammar").position()
        name = lexer.match(GLAP_ID)
        grammar_type_spec = []
        if lexer.test("("):
            grammar_type_spec = self.parse_grammar_type_spec(lexer, actions)
        rules_and_commands = []
        while lexer.peek() and not lexer.test("end"):
            if lexer.test("."):
                lexer.next()
                rules_and_commands.extend(actions.run(
                    "unwrap", self.context, self.parse_command(lexer, actions)
                ))
                continue
            rules_and_commands.append(self.parse_rule(lexer, actions))
        lexer.match("end")
        return actions.run("grammar",
            self.context, p, name, grammar_type_spec, rules_and_commands
        )
    #-def

    def parse_grammar_type_spec(self, lexer, actions):
        """
        """

        # grammar_type_spec -> "(" ( ID ( "," ID )* )? ")"
        lexer.match("(")
        l = []
        if lexer.test(GLAP_ID):
            l.append(lexer.match(GLAP_ID))
            while lexer.test(","):
                lexer.next()
                l.append(lexer.match(GLAP_ID))
        lexer.match(")")
        return l
    #-def

    def parse_rule(self, lexer, actions):
        """
        """

        # rule -> ID ( "->" | ":" ) rule_rhs_expr ";"
        lhs = lexer.match(GLAP_ID)
        leftarrow = lexer.match("->", ":")
        rhs = self.parse_rule_rhs_expr(lexer, actions)
        lexer.match(";")
        return actions.run("rule", self.context, lhs, leftarrow, rhs)
    #-def

    @expression_parser(
      (0, 0, "|", 1),
      (1, 1, "-", 2),
      (2, 2, "", 3),
      (3, 3, "*", -1),
      (3, 3, "+", -1),
      (3, 3, "?", -1),
      (4, -1, "-", 4),
      (4, -1, "~", 4),
      (5, 6, "'", 6),
      first = [ "-", "~", GLAP_ID, GLAP_STR, "eps", "{", "(" ]
    )
    def parse_rule_rhs_expr(self, lexer, actions, level = 0):
        """
        """

        # rule_rhs_expr[0] -> rule_rhs_expr[0] "|" rule_rhs_expr[1]
        #                   | rule_rhs_expr[1]
        # rule_rhs_expr[1] -> rule_rhs_expr[1] "-" rule_rhs_expr[2]
        #                   | rule_rhs_expr[2]
        # rule_rhs_expr[2] -> rule_rhs_expr[2] "" rule_rhs_expr[3]
        #                   | rule_rhs_expr[3]
        # rule_rhs_expr[3] -> rule_rhs_expr[3] ( "*" | "+" | "?" )
        #                   | rule_rhs_expr[4]
        # rule_rhs_expr[4] -> ( "-" | "~" ) rule_rhs_expr[4]
        #                   | rule_rhs_expr[5]
        # rule_rhs_expr[5] -> rule_rhs_expr[6] "'" rule_rhs_expr[6]
        #                   | rule_rhs_expr[6]
        # rule_rhs_expr[6] -> rule_rhs_expr_atom
        optab = self.parse_rule_rhs_expr.optab
        # Peek for prefix operator.
        op = optab.peekprefix(lexer)
        # It is a prefix operator reachable from the current level?
        if op and op.level >= level:
            # Yes, it is.
            p = lexer.token.position()
            lexer.next()
            # Parse right-hand side:
            result = self.parse_rule_rhs_expr(lexer, actions, op.rbp)
            result = actions.run(
                "rule_rhs_expr(%s)" % op.mask, self.context, p, result
            )
            oplvl = op.level
        else:
            # No, it isn't. It is either atom or binary/postfix operator or it
            # is a prefix operator that is unreachable from this level (only
            # atom pass here).
            result = self.parse_rule_rhs_expr_atom(lexer, actions)
            oplvl = optab.atomlevel
        while True:
            op = optab.peekoperator(lexer)
            # `op' is not operator => stop
            # previous operator/atom cannot be reached (derived) => stop
            # current operator has lower priority (level) => stop
            if not op or op.lbp > oplvl or op.level < level:
                break
            p = lexer.token.position()
            # "Invisible" operator treatment.
            if op.name:
                lexer.next()
            # Binary operator?
            if op.rbp >= 0:
                rhs = self.parse_rule_rhs_expr(lexer, actions, op.rbp)
                result = actions.run(
                    "rule_rhs_expr(%s)" % op.mask, self.context, p, result, rhs
                )
            else:
                # Unary postfix.
                result = actions.run(
                    "rule_rhs_expr(%s)" % op.mask, self.context, p, result
                )
            # Update previous operator level.
            oplvl = op.level
        return result
    #-def

    def parse_rule_rhs_expr_atom(self, lexer, actions):
        """
        """

        # rule_rhs_expr_atom -> ID | STR ( ".." STR )? | "eps"
        #                     | "{" a_start "}" | "(" rule_rhs_expr[0] ")"
        t = lexer.peek()
        if t is None:
            raise GlapSyntaxError(self.context, "Unexpected end of input")
        ttype = t.ttype
        if ttype == GLAP_ID:
            lexer.next()
            return actions.run("rule_rhs_expr_atom(ID)", self.context, t)
        elif ttype == GLAP_STR:
            lexer.next()
            if lexer.test(".."):
                lexer.next()
                u = lexer.match(GLAP_STR)
                return actions.run(
                    "rule_rhs_expr_atom(STR..STR)", self.context, t, u
                )
            return actions.run("rule_rhs_expr_atom(STR)", self.context, t)
        elif ttype == "eps":
            lexer.next()
            return actions.run(
                "rule_rhs_expr_atom(eps)", self.context, t.position()
            )
        elif ttype == "{":
            lexer.next()
            r = self.parse_a_start(lexer, actions)
            lexer.match("}")
            return actions.run(
                "rule_rhs_expr_atom(action)", self.context, t.position(), r
            )
        elif ttype == "(":
            lexer.next()
            r = self.parse_rule_rhs_expr(lexer, actions, 0)
            lexer.match(")")
            return r
        raise GlapSyntaxError(self.context,
            "Atom (primary expression) was expected"
        )
    #-def

    # -------------------------------------------------------------------------
    # -- Commands
    # -------------------------------------------------------------------------

    def parse_command(self, lexer, actions):
        """
        """

        # command -> c_expr ";"
        #          | c_stmt
        if lexer.test(
            "{", "defmacro", "define", "if", "foreach", "while", "do", "break",
            "continue", "return", "try", "throw"
        ):
            return self.parse_c_stmt(lexer, actions)
        r, _ = self.parse_c_expr(lexer, actions, 0, False)
        lexer.match(";")
        return r
    #-def

    @expression_parser(
      (0, 12, "=", 0),   # assign
      (0, 12, "+=", 0),  # in-place add
      (0, 12, "-=", 0),  # in-place sub
      (0, 12, "*=", 0),  # in-place mult
      (0, 12, "/=", 0),  # in-place div
      (0, 12, "%=", 0),  # in-place mod
      (0, 12, "&=", 0),  # in-place bitand
      (0, 12, "|=", 0),  # in-place bitor
      (0, 12, "^=", 0),  # in-place bitxor
      (0, 12, "<<=", 0), # in-place bitwise shift to the left
      (0, 12, ">>=", 0), # in-place bitwise shift to the right
      (0, 12, "&&=", 0), # in-place logical and
      (0, 12, "||=", 0), # in-place logical or
      (0, 12, ".=", 0),  # in-place string concatenation
      (0, 12, "++=", 0), # in-place list join
      (0, 12, "~~=", 0), # in-place hash table merge
      (1, 1, "||", 2),   # logical or
      (2, 2, "&&", 3),   # logical and
      (3, 4, "<", 4),    # less than
      (3, 4, ">", 4),    # greater than
      (3, 4, "<=", 4),   # less or equal
      (3, 4, ">=", 4),   # greater or equal
      (3, 4, "==", 4),   # equal
      (3, 4, "!=", 4),   # not equal
      (3, 4, "===", 4),  # is identical
      (3, 4, "in", 4),   # contains
      (4, 4, "|", 5),    # bitor
      (5, 5, "&", 6),    # bitand
      (6, 6, "^", 7),    # bitxor
      (7, 7, "<<", 8),   # bitwise shift to the left
      (7, 7, ">>", 8),   # bitwise shift to the right
      (8, 8, "+", 9),    # add
      (8, 8, "-", 9),    # sub
      (8, 8, ".", 9),    # concat
      (8, 8, "++", 9),   # join
      (8, 8, "~~", 9),   # merge
      (9, 9, "*", 10),   # mul
      (9, 9, "/", 10),   # div
      (9, 9, "%", 10),   # mod
      (10, 11, "", -1),  # call
      (11, -1, "-", 11), # negation
      (11, -1, "!", 11), # logical not
      (11, -1, "~", 11), # bitinvert
      (12, 12, "[", -1), # index
      (12, 12, ":", -1), # access
      first = [
        "-", "!", "~", GLAP_ID, "$", "#", "$(", GLAP_INT, GLAP_FLOAT, GLAP_STR,
        "(", "[", "{"
      ]
    )
    def parse_c_expr(self, lexer, actions, level = 0, lambdas = False):
        """
        """

        # c_expr[0] -> c_expr[12] assignop c_expr[0] | c_expr[1]
        # assignop -> "="   | "+=" | "-="  | "*="  | "/="  | "%="  | "&="
        #           | "|="  | "^=" | "<<=" | ">>=" | "&&=" | "||=" | ".="
        #           | "++=" | "~~="
        # c_expr[1] -> c_expr[1] "||" c_expr[2] | c_expr[2]
        # c_expr[2] -> c_expr[2] "&&" c_expr[3] | c_expr[3]
        # c_expr[3] -> c_expr[4] relop c_expr[4] | c_expr[4]
        # relop -> "<" | ">" | "<=" | ">=" | "==" | "!=" | "===" | "in"
        # c_expr[4] -> c_expr[4] "|" c_expr[5] | c_expr[5]
        # c_expr[5] -> c_expr[5] "&" c_expr[6] | c_expr[6]
        # c_expr[6] -> c_expr[6] "^" c_expr[7] | c_expr[7]
        # c_expr[7] -> c_expr[7] bitshiftop c_expr[8] | c_expr[8]
        # bitshiftop -> "<<" | ">>"
        # c_expr[8] -> c_expr[8] addop c_expr[9] | c_expr[9]
        # addop -> "+" | "-" | "." | "++" | "~~"
        # c_expr[9] -> c_expr[9] mulop c_expr[10] | c_expr[10]
        # mulop -> "*" | "/" | "%"
        # c_expr[10] -> c_expr[11] ("'"? c_expr[11])*
        # c_expr[11] -> uop c_expr[11] | c_expr[12]
        # uop -> "-" | "!" | "~"
        # c_expr[12] -> c_expr[12] postop | c_expr_atom
        # postop -> "[" c_expr[1] "]" | ":" ID
        optab = self.parse_c_expr.optab
        op = optab.peekprefix(lexer)
        if op and op.level >= level:
            p = lexer.token.position()
            lexer.next()
            result, _ = self.parse_c_expr(lexer, actions, op.rbp, True)
            result = actions.run(
                "c_expr(%s)" % op.mask, self.context, p, result
            )
            oplvl = op.level
        else:
            result = self.parse_c_expr_atom(lexer, actions, lambdas)
            oplvl = optab.atomlevel
        while True:
            op = optab.peekoperator(lexer)
            # Fix the "a 'b" case:
            if not op and lexer.test("'"):
                op = optab.operators.get("", None)
            if not op or op.lbp > oplvl or op.level < level:
                break
            if not lambdas and lexer.token.ttype == "{":
                # "{" denotes a block instead of lambda
                break
            # Handle operators here.
            if op.name == "":
                # Call expression.
                p = lexer.token.position()
                fargs = []
                while True:
                    if not optab.operandfollows(lexer) and not lexer.test("'"):
                        break
                    lambdas_ = lambdas
                    if lexer.test("'"):
                        lambdas_ = True
                        lexer.next()
                    farg, _ = self.parse_c_expr(
                        lexer, actions, op.lbp, lambdas_
                    )
                    fargs.append(farg)
                result = actions.run(
                    "c_expr(_ _)", self.context, p, result, fargs
                )
            elif op.name == "[":
                # Index expression.
                p = lexer.token.position()
                lexer.next()
                iexpr, _ = self.parse_c_expr(lexer, actions, 1, True)
                lexer.match("]")
                result = actions.run(
                    "c_expr(_[_])", self.context, p, result, iexpr
                )
            elif op.name == ":":
                # Access expression.
                p = lexer.token.position()
                lexer.next()
                t_ID = lexer.match(GLAP_ID)
                result = actions.run(
                    "c_expr(_:ID)", self.context, p, result, t_ID
                )
            elif op.rbp < 0:
                # Other unary expression.
                p = lexer.token.position()
                lexer.next()
                result = actions.run(
                    "c_expr(%s)" % op.mask, self.context, p, result
                )
            else:
                # Binary operator.
                p = lexer.token.position()
                lexer.next()
                rhs, _ = self.parse_c_expr(lexer, actions, op.rbp, True)
                result = actions.run(
                    "c_expr(%s)" % op.mask, self.context, p, result, rhs
                )
            oplvl = op.level
        return result, oplvl
    #-def

    def parse_c_expr_atom(self, lexer, actions, lambdas):
        """
        """

        # c_expr_atom -> ID                   -- identifier
        #              | "$" ID               -- get value
        #              | "#" ID               -- get macro parameter content
        #              | "$(" c_maccall ")"   -- expand macro with params
        #              | INT
        #              | FLOAT
        #              | STR
        #              | "(" c_expr[1] "," c_expr[1] ")"   -- pair
        #              | "[" c_list_items? "]"             -- list
        #              | "[" c_hash_items  "]"             -- hash
        #              | "{" "|" c_fargs "|" command* "}"  -- lambda
        #              | "(" c_expr[1] ")"
        #
        # c_list_items -> c_expr[1] ( "," c_expr[1] )*
        # c_hash_items -> c_hash_item ( "," c_hash_item )*
        # c_hash_item -> c_expr[1] "=>" c_expr[1]
        # c_fargs -> ID+ ( "..." ID )?
        t = lexer.peek()
        if t is None:
            raise GlapSyntaxError(self.context, "Unexpected end of input")
        ttype = t.ttype
        if ttype == GLAP_ID:
            lexer.next()
            return actions.run("c_expr_atom(ID)", self.context, t)
        elif ttype == "$":
            lexer.next()
            t = lexer.match(GLAP_ID)
            return actions.run("c_expr_atom($ID)", self.context, t)
        elif ttype == "#":
            lexer.next()
            t = lexer.match(GLAP_ID)
            return actions.run("c_expr_atom(#ID)", self.context, t)
        elif ttype == "$(":
            lexer.next()
            m, margs = self.parse_c_maccall(lexer, actions)
            lexer.match(")")
            return actions.run(
                "c_expr_atom($(_ _))", self.context, t.position(), m, margs
            )
        elif ttype == GLAP_INT:
            lexer.next()
            return actions.run("c_expr_atom(INT)", self.context, t)
        elif ttype == GLAP_FLOAT:
            lexer.next()
            return actions.run("c_expr_atom(FLOAT)", self.context, t)
        elif ttype == GLAP_STR:
            lexer.next()
            return actions.run("c_expr_atom(STR)", self.context, t)
        elif ttype == "(":
            lexer.next()
            r, l = self.parse_c_expr(lexer, actions, 1, True)
            if lexer.test(","):
                lexer.next()
                e, _ = self.parse_c_expr(lexer, actions, 1, True)
                r = actions.run(
                    "c_expr_atom(pair)", self.context, t.position(), r, e
                )
            lexer.match(")")
            return r
        elif ttype == "[":
            lexer.next()
            is_hash = False
            items = []
            while not lexer.test("]", None):
                if items:
                    lexer.match(",")
                item, _ = self.parse_c_expr(lexer, actions, 1, True)
                if not items and lexer.test("=>"):
                    is_hash = True
                if is_hash:
                    lexer.match("=>")
                    v, _ = self.parse_c_expr(lexer, actions, 1, True)
                    item = (item, v)
                items.append(item)
            lexer.match("]")
            return actions.run(
                "c_expr_atom(%s)" % ("hash" if is_hash else "list"),
                self.context, t.position(), items
            )
        elif ttype == "{":
            if not lambdas:
                raise GlapSyntaxError(self.context,
                    "Atom (primary expression) was expected, but block found"
                )
            lexer.next()
            actions.procedure_nesting_level += 1
            lexer.match("|")
            fargs = [lexer.match(GLAP_ID)]
            has_varargs = False
            while lexer.test(GLAP_ID):
                fargs.append(lexer.match(GLAP_ID))
            if lexer.test("..."):
                lexer.next()
                fargs.append(lexer.match(GLAP_ID))
                has_varargs = True
            lexer.match("|")
            commands = []
            while not lexer.test("}", None):
                commands.append(self.parse_command(lexer, actions))
            lexer.match("}")
            # actions.procedure_nesting_level -= 1
            return actions.run(
                "c_expr_atom(lambda)",
                self.context, t.position(), fargs, has_varargs, commands
            )
        raise GlapSyntaxError(self.context,
            "Atom (primary expression) was expected"
        )
    #-def

    def parse_c_maccall(self, lexer, actions):
        """
        """

        # c_maccall -> c_expr[1] ("`" c_expr[1])*
        m, _ = self.parse_c_expr(lexer, actions, 1, True)
        margs = []
        while lexer.test("`"):
            lexer.next()
            marg, _ = self.parse_c_expr(lexer, actions, 1, True)
            margs.append(marg)
        return m, margs
    #-def

    def parse_c_stmt(self, lexer, actions):
        """
        """

        # c_stmt -> c_block
        # c_stmt -> "defmacro" ID ID* "(" command* ")"
        # c_stmt -> "define" ID ID* ( "..." ID )? c_block
        # c_stmt -> "if" c_expr[1] c_block
        #           ( "elif" c_expr[1] c_block )*
        #           ( "else" c_block )?
        # c_stmt -> "foreach" ID c_expr[1] c_block
        # c_stmt -> "while" c_expr[1] c_block
        # c_stmt -> "do" c_block "while" c_expr[1] ";"
        # c_stmt -> "break" ";"
        # c_stmt -> "continue" ";"
        # c_stmt -> "return" ( c_expr[1] )? ";"
        # c_stmt -> "try" c_block
        #           ( "catch" ID ID? c_block )*
        #           ( "finally" c_block )?
        # c_stmt -> "throw" c_expr[1] ( "," c_expr[1] )? ";"
        t = lexer.peek()
        if t is None:
            raise GlapSyntaxError(self.context, "Unexpected end of input")
        tt = t.ttype
        if tt == "{":
            return self.parse_c_block(lexer, actions)
        elif tt == "defmacro":
            if actions.inmacro:
                raise GlapSyntaxError(self.context,
                    "Nested macros are not allowed"
                )
            if actions.procedure_nesting_level != 0:
                raise GlapSyntaxError(self.context,
                    "Macros inside functions are not allowed"
                )
            lexer.next()
            actions.inmacro = True
            name = lexer.match(GLAP_ID)
            params = []
            while lexer.test(GLAP_ID):
                params.append(lexer.match(GLAP_ID))
            lexer.match("(")
            body = []
            while not lexer.test(")", None):
                body.append(self.parse_command(lexer, actions))
            lexer.match(")")
            # actions.inmacro = False
            return actions.run(
                "c_stmt(defmacro)",
                self.context, t.position(), name, params, body
            )
        elif tt == "define":
            if actions.inmacro:
                raise GlapSyntaxError(self.context,
                    "Function definition inside macro is not allowed"
                )
            lexer.next()
            actions.procedure_nesting_level += 1
            name = lexer.match(GLAP_ID)
            params = []
            while lexer.test(GLAP_ID):
                params.append(lexer.match(GLAP_ID))
            has_varargs = False
            if lexer.test("..."):
                lexer.next()
                params.append(lexer.match(GLAP_ID))
                has_varargs = True
            body = self.parse_c_block(lexer, actions, True)
            # actions.procedure_nesting_level -= 1
            return actions.run(
                "c_stmt(define)",
                self.context, t.position(), name, params, has_varargs, body
            )
        elif tt == "if":
            lexer.next()
            cond, _ = self.parse_c_expr(lexer, actions, 1, False)
            then_part = self.parse_c_block(lexer, actions, True)
            elif_parts = []
            while lexer.test("elif"):
                l = lexer.token.position()
                lexer.next()
                ei_cond, _ = self.parse_c_expr(lexer, actions, 1, False)
                ei_body = self.parse_c_block(lexer, actions, True)
                elif_parts.append((l, ei_cond, ei_body))
            else_part = []
            if lexer.test("else"):
                l = lexer.token.position()
                lexer.next()
                else_part.append((l, self.parse_c_block(lexer, actions, True)))
            return actions.run(
                "c_stmt(if)",
                self.context, t.position(),
                cond, then_part, elif_parts, else_part
            )
        elif tt == "foreach":
            lexer.next()
            var = lexer.match(GLAP_ID)
            ie, _ = self.parse_c_expr(lexer, actions, 1, False)
            body = self.parse_c_block(lexer, actions, True)
            return actions.run(
                "c_stmt(foreach)",
                self.context, t.position(), var, ie, body
            )
        elif tt == "while":
            lexer.next()
            cond, _ = self.parse_c_expr(lexer, actions, 1, False)
            body = self.parse_c_block(lexer, actions, True)
            return actions.run(
                "c_stmt(while)", self.context, t.position(), cond, body
            )
        elif tt == "do":
            lexer.next()
            body = self.parse_c_block(lexer, actions, True)
            lexer.match("while")
            cond, _ = self.parse_c_expr(lexer, actions, 1, False)
            lexer.match(";")
            return actions.run(
                "c_stmt(do-while)", self.context, t.position(), body, cond
            )
        elif tt in ["break", "continue"]:
            lexer.next()
            lexer.match(";")
            return actions.run("c_stmt(%s)" % tt, self.context, t.position())
        elif tt == "return":
            lexer.next()
            if lexer.test(";"):
                lexer.next()
                return actions.run(
                    "c_stmt(return)", self.context, t.position()
                )
            rv, _ = self.parse_c_expr(lexer, actions, 1, False)
            lexer.match(";")
            return actions.run(
                "c_stmt(return(expr))", self.context, t.position(), rv
            )
        elif tt == "try":
            lexer.next()
            tryblock = self.parse_c_block(lexer, actions, True)
            catches = []
            while lexer.test("catch"):
                l = lexer.token.position()
                lexer.next()
                exc = lexer.match(GLAP_ID)
                excvar = None
                if lexer.test(GLAP_ID):
                    excvar = lexer.match(GLAP_ID)
                catchblock = self.parse_c_block(lexer, actions, True)
                catches.append((l, exc, excvar, catchblock))
            fnly = []
            if lexer.test("finally"):
                l = lexer.token.position()
                lexer.next()
                fnly.append((l, self.parse_c_block(lexer, actions, True)))
            return actions.run(
                "c_stmt(try)",
                self.context, t.position(), tryblock, catches, fnly
            )
        elif tt == "throw":
            lexer.next()
            ee, _ = self.parse_c_expr(lexer, actions, 1, True)
            em = None
            if lexer.test(","):
                lexer.next()
                em, _ = self.parse_c_expr(lexer, actions, 1, True)
            lexer.match(";")
            return actions.run(
                "c_stmt(throw)", self.context, t.position(), ee, em
            )
        raise GlapSyntaxError(self.context, "Statement was expected")
    #-def

    def parse_c_block(self, lexer, actions, keep_varinfo = False):
        """
        """

        # c_block -> "{" command* "}"
        loc = lexer.match("{").position()
        commands = []
        while not lexer.test("}", None):
            commands.append(self.parse_command(lexer, actions))
        lexer.match("}")
        return actions.run(
            "c_stmt(block)", self.context, loc, commands, keep_varinfo
        )
    #-def

    # -------------------------------------------------------------------------
    # -- Actions
    # -------------------------------------------------------------------------

    def parse_a_start(self, lexer, actions):
        """
        """

        # a_start -> a_stmt*
        alist = []
        while not lexer.test("}", None):
            stmt, _ = self.parse_a_stmt(lexer, actions)
            alist.append(stmt)
        return alist
    #-def

    def parse_a_stmt(self, lexer, actions, labels = False):
        """
        """

        # a_stmt -> a_block
        # a_stmt -> a_expr ";"
        # a_stmt -> a_lexpr a_assign_op a_expr ";"
        # a_stmt -> "if" a_expr a_block
        #           ( "elif" a_expr a_block )*
        #           ( "else" a_block )?
        # a_stmt -> "case" a_expr "of" "{"
        #             ( a_expr ":" a_stmt* )*
        #             ( "default" ":" a_stmt* )?
        #           "}"
        # a_stmt -> "for" ID ":" a_expr a_block
        # a_stmt -> "while" a_expr a_block
        # a_stmt -> "do" a_block "while" a_expr ";"
        # a_stmt -> "break" ";"
        # a_stmt -> "continue" ";"
        # a_stmt -> "return" a_expr? ";"
        # a_lexpr -> a_expr[10] "[" a_expr[0] "]"
        #          | a_expr[10] "." ID
        #          | ID
        #          | "(" a_lexpr ")"
        t = lexer.peek()
        if t is None:
            raise GlapSyntaxError(self.context, "Unexpected end of input")
        tt = t.ttype
        if tt == "{":
            return self.parse_a_block(lexer, actions), False
        elif self.parse_a_expr.optab.operandfollows(lexer):
            expr, is_lexpr = self.parse_a_expr(lexer, actions)
            action = ["a_stmt(expr)", self.context, -1, expr]
            t = lexer.peek()
            if t is None:
                raise GlapSyntaxError(self.context, "Unexpected end of input")
            tt = t.ttype
            if tt == ":" and labels:
                lexer.next()
                return actions.run(*action), True
            elif tt in [
                "=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=",
                ">>="
            ]:
                if not is_lexpr:
                    raise GlapSyntaxError(
                        self.context, "L-expression was expected"
                    )
                lexer.next()
                expr, _ = self.parse_a_expr(lexer, actions)
                action[0] = "a_stmt(_%s_)" % tt
                action[2] = t.position()
                action.append(expr)
            lexer.match(";")
            return actions.run(*action), False
        elif tt == "if":
            lexer.next()
            cond, _ = self.parse_a_expr(lexer, actions)
            then_part = self.parse_a_block(lexer, actions)
            elif_parts = []
            while lexer.test("elif"):
                lexer.next()
                eic, _ = self.parse_a_expr(lexer, actions)
                eib = self.parse_a_block(lexer, actions)
                elif_parts.append((eic, eib))
            else_part = None
            if lexer.test("else"):
                lexer.next()
                else_part = self.parse_a_block(lexer, actions)
            return actions.run(
                "a_stmt(if)", self.context, t.position(),
                cond, then_part, elif_parts, else_part
            ), False
        elif tt == "case":
            lexer.next()
            swe, _ = self.parse_a_expr(lexer, actions)
            lexer.match("of")
            lexer.match("{")
            cases = []
            while not lexer.test("}", "default", None):
                pos = lexer.token.position()
                stmt, is_label = self.parse_a_stmt(lexer, actions, True)
                if not cases and not is_label:
                    raise GlapSyntaxError(
                        self.context, "Label was expected", pos
                    )
                if is_label:
                    cases.append((stmt, []))
                else:
                    cases[-1][1].append(stmt)
            default = None
            if lexer.test("default"):
                lexer.next()
                lexer.match(":")
                default = []
                while not lexer.test("}", None):
                    stmt, _ = self.parse_a_stmt(lexer, actions)
                    default.append(stmt)
            lexer.match("}")
            return actions.run(
                "a_stmt(case)", self.context, t.position(), swe, cases, default
            ), False
        elif tt == "for":
            lexer.next()
            var = lexer.match(GLAP_ID)
            lexer.match(":")
            cond, _ = self.parse_a_expr(lexer, actions)
            body = self.parse_a_block(lexer, actions)
            return actions.run(
                "a_stmt(for)", self.context, t.position(), var, cond, body
            ), False
        elif tt == "while":
            lexer.next()
            cond, _ = self.parse_a_expr(lexer, actions)
            body = self.parse_a_block(lexer, actions)
            return actions.run(
                "a_stmt(while)", self.context, t.position(), cond, body
            ), False
        elif tt == "do":
            lexer.next()
            body = self.parse_a_block(lexer, actions)
            lexer.match("while")
            cond, _ = self.parse_a_expr(lexer, actions)
            lexer.match(";")
            return actions.run(
                "a_stmt(do-while)", self.context, t.position(), body, cond
            ), False
        elif tt == "break":
            lexer.next()
            lexer.match(";")
            return actions.run(
                "a_stmt(break)", self.context, t.position()
            ), False
        elif tt == "continue":
            lexer.next()
            lexer.match(";")
            return actions.run(
                "a_stmt(continue)", self.context, t.position()
            ), False
        elif tt == "return":
            lexer.next()
            if lexer.test(";"):
                lexer.next()
                return actions.run(
                    "a_stmt(return)", self.context, t.position()
                ), False
            expr, _ = self.parse_a_expr(lexer, actions)
            lexer.match(";")
            return actions.run(
                "a_stmt(return(expr))", self.context, t.position(), expr
            ), False
        raise GlapSyntaxError(self.context, "Statement was expected")
    #-def

    def parse_a_block(self, lexer, actions):
        """
        """

        # a_block -> "{" a_stmt* "}"
        loc = lexer.match("{").position()
        stmts = []
        while not lexer.test("}", None):
            stmt, _ = self.parse_a_stmt(lexer, actions)
            stmts.append(stmt)
        lexer.match("}")
        return actions.run("a_stmt(block)", self.context, loc, stmts)
    #-def

    @expression_parser(
      (0, 0, "||", 1),
      (1, 1, "&&", 2),
      (2, 3, "<", 3),
      (2, 3, ">", 3),
      (2, 3, "<=", 3),
      (2, 3, ">=", 3),
      (2, 3, "==", 3),
      (2, 3, "!=", 3),
      (3, 3, "|", 4),
      (4, 4, "&", 5),
      (5, 5, "^", 6),
      (6, 6, "<<", 7),
      (6, 6, ">>", 7),
      (7, 7, "+", 8),
      (7, 7, "-", 8),
      (8, 8, "*", 9),
      (8, 8, "/", 9),
      (8, 8, "%", 9),
      (9, -1, "-", 9),
      (9, -1, "~", 9),
      (9, -1, "!", 9),
      (10, 10, "(", -1),
      (10, 10, "[", -1),
      (10, 10, ".", -1),
      first = [ "-", "~", "!", GLAP_ID, GLAP_INT, GLAP_FLOAT, GLAP_STR, "(" ]
    )
    def parse_a_expr(self, lexer, actions, level = 0):
        """
        """

        # a_expr[0] -> a_expr[0] "||" a_expr[1] | a_expr[1]
        # a_expr[1] -> a_expr[1] "&&" a_expr[2] | a_expr[2]
        # a_expr[2] -> a_expr[3] a_relop a_expr[3] | a_expr[3]
        # a_relop -> "<" | ">" | "<=" | ">=" | "==" | "!="
        # a_expr[3] -> a_expr[3] "|" a_expr[4] | a_expr[4]
        # a_expr[4] -> a_expr[4] "&" a_expr[5] | a_expr[5]
        # a_expr[5] -> a_expr[5] "^" a_expr[6] | a_expr[6]
        # a_expr[6] -> a_expr[6] a_bitshiftop a_expr[7] | a_expr[7]
        # a_bitshiftop -> "<<" | ">>"
        # a_expr[7] -> a_expr[7] a_addop a_expr[8] | a_expr[8]
        # a_addop -> "+" | "-"
        # a_expr[8] -> a_expr[8] a_mulop a_expr[9] | a_expr[9]
        # a_mulop -> "*" | "/" | "%"
        # a_expr[9] -> a_uop a_expr[9] | a_expr[10]
        # a_uop -> "-" | "~" | "!"
        # a_expr[10] -> a_expr[10] a_postfixop | a_expr_atom
        # a_postfixop -> "(" ( a_expr[0] ( "," a_expr[0] )* )? ")"
        #                 | "[" a_expr[0] "]"
        #                 | "." ID
        optab = self.parse_a_expr.optab
        op = optab.peekprefix(lexer)
        if op and op.level >= level:
            pos = lexer.token.position()
            lexer.next()
            result, is_lexpr = self.parse_a_expr(lexer, actions, op.rbp)
            result = actions.run(
                "a_expr(%s)" % op.mask, self.context, pos, result
            )
            oplvl = op.level
        else:
            result, is_lexpr = self.parse_a_expr_atom(lexer, actions)
            oplvl = optab.atomlevel
        while True:
            op = optab.peekoperator(lexer)
            if not op or op.lbp > oplvl or op.level < level:
                break
            if op.name == "(":
                pos = lexer.token.position()
                lexer.next()
                args = []
                while not lexer.test(")", None):
                    if args:
                        lexer.match(",")
                    arg, _ = self.parse_a_expr(lexer, actions)
                    args.append(arg)
                lexer.match(")")
                result = actions.run(
                    "a_expr(_(_))", self.context, pos, result, args
                )
                is_lexpr = False
            elif op.name == "[":
                pos = lexer.token.position()
                lexer.next()
                iexpr, _ = self.parse_a_expr(lexer, actions)
                lexer.match("]")
                result = actions.run(
                    "a_expr(_[_])", self.context, pos, result, iexpr
                )
                is_lexpr = True
            elif op.name == ".":
                pos = lexer.token.position()
                lexer.next()
                t_ID = lexer.match(GLAP_ID)
                result = actions.run(
                    "a_expr(_.ID)", self.context, pos, result, t_ID
                )
                is_lexpr = True
            elif op.rbp < 0:
                pos = lexer.token.position()
                lexer.next()
                result = actions.run(
                    "a_expr(%s)" % op.mask, self.context, pos, result
                )
                is_lexpr = False
            else:
                pos = lexer.token.position()
                lexer.next()
                rhs, _ = self.parse_a_expr(lexer, actions, op.rbp)
                result = actions.run(
                    "a_expr(%s)" % op.mask, self.context, pos, result, rhs
                )
                is_lexpr = False
            oplvl = op.level
        return result, is_lexpr
    #-def

    def parse_a_expr_atom(self, lexer, actions):
        """
        """

        # a_expr_atom -> ID | INT | FLOAT | STR | "(" a_expr[0] ")"
        t = lexer.peek()
        if t is None:
            raise GlapSyntaxError(self.context, "Unexpected end of input")
        tt = t.ttype
        if tt == GLAP_ID:
            lexer.next()
            return actions.run(
                "a_expr_atom(ID)", self.context, t.position(), t.value()
            ), True
        elif tt == GLAP_INT:
            lexer.next()
            return actions.run(
                "a_expr_atom(INT)", self.context, t.position(), t.value(True)
            ), False
        elif tt == GLAP_FLOAT:
            lexer.next()
            return actions.run(
                "a_expr_atom(FLOAT)", self.context, t.position(), t.value(True)
            ), False
        elif tt == GLAP_STR:
            lexer.next()
            return actions.run(
                "a_expr_atom(STR)", self.context, t.position(), t.value()
            ), False
        elif tt == "(":
            lexer.next()
            r = self.parse_a_expr(lexer, actions)
            lexer.match(")")
            return r
        raise GlapSyntaxError(
            self.context, "Atom (primary expression) was expected"
        )
    #-def
#-class
