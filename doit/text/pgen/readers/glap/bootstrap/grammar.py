#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/bootstrap/grammar.py
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

GLAP_ID    = 1
GLAP_INT   = 2
GLAP_FLOAT = 3
GLAP_CHAR  = 4
GLAP_STR   = 5

class GlapStream(object):
    """
    """
    __slots__ = [ 'name', 'data', 'pos', 'size' ]

    def __init__(self, name, s):
        """
        """

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

class GlapToken(Token):
    """
    """
    NAMES = {
      GLAP_ID: "identifier",
      GLAP_INT: "int literal",
      GLAP_FLOAT: "float literal",
      GLAP_CHAR: "char literal",
      GLAP_STR: "string literal"
    }
    __slots__ = []

    def __init__(self, ttype, location, *data):
        """
        """

        Token.__init__(self, ttype, location, data)
    #-def

    def location(self):
        """
        """

        return self.data[0]
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

class GlapLexer(object):
    """
    """
    crange = lambda a, b: [ chr(c) for c in range(ord(a), ord(b) + 1) ]
    WS = "\n "
    ASCIICHAR = lambda c: ord(' ') <= ord(c) and ord(c) <= ord('~')
    COMMENTCHAR = lambda c: GlapLexer.ASCIICHAR(c) or ord(c) >= 128
    SOURCECHAR = lambda c: c == '\n' or GlapLexer.COMMENTCHAR(c)
    ODIGIT = "01234567"
    DIGIT = "0123456789"
    XDIGIT = "%sABCDEFabcdef" % DIGIT
    IDCHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
    IDCHARNUM = "%s%s" % (DIGIT, IDCHAR)
    KEYWORDS = [ "module", "grammar", "end" ]
    CHARCHAR = lambda c: GlapLexer.COMMENTCHAR(c) and c not in ("'", "\\")
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
    __slots__ = [ 'istream', 'token' ]

    def __init__(self, istream):
        """
        """

        self.istream = istream
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
            raise GlapSyntaxError(self, "Expected end of input")
    #-def

    def test(self, *ts):
        """
        """

        if self.peek():
            return self.token.ttype in ts
        return None in ts
    #-def

    def match(self, t):
        """
        """

        if not self.peek() or self.token.ttype != t:
            raise GlapSyntaxError(self, "Expected %s" % GlapToken.tokname(t))
        t = self.token
        self.next()
        return t
    #-def

    def next(self):
        """
        """

        istream = self.istream
        self.skip_spaces(istream)
        c = istream.peek(1)
        if c == "":
            self.token = None
        elif c in self.IDCHAR:
            self.token = self.scan_ID(c, istream)
        elif c in self.DIGIT:
            self.token = self.scan_NUMBER(c, istream)
        elif c == '\'':
            self.token = self.scan_CHAR(c, istream)
        elif c == '"':
            self.token = self.scan_STR(c, istream)
        else:
            raise GlapLexError(istream, "Unexpected symbol %r" % c)
    #-def

    def skip_spaces(self, istream):
        """
        """

        # ( [ ' ', '\n' ]* | "--" COMMENTCHAR* )*
        while True:
            p = istream.pos
            istream.matchset(self.WS)
            self.skip_comment(istream)
            if p < istream.pos:
                continue
            break
    #-def

    def skip_comment(self, istream):
        """
        """

        if istream.peek(2) != "--":
            return
        istream.next(2)
        istream.matchmanyif(GlapLexer.COMMENTCHAR)
    #-def

    def scan_ID(self, c, istream):
        """
        """

        # IDCHAR IDCHARNUM*
        p = istream.pos
        m = istream.matchmany(self.IDCHARNUM)
        if m in self.KEYWORDS:
            return GlapToken(m, p)
        return GlapToken(GLAP_ID, p, m)
    #-def

    def scan_NUMBER(self, c, istream):
        """
        """

        # (DIGIT - '0') DIGIT*
        #   ( '.' DIGIT+ )?
        #   ( ( 'E' | 'e' ) ( '+' | '-' )? DIGIT+ )?
        # '0' ODIGIT*
        # '0' ( 'X' | 'x' ) XDIGIT+
        p = istream.pos
        if c != '0':
            # Non-zero digit case - match integral part:
            ipart = istream.matchmany(self.DIGIT)
            c = istream.peek(1)
            if c not in [ '.', 'E', 'e' ]:
                return GlapToken(GLAP_INT, p, GLAP_INT_DEC, ipart)
            # Floating-point number - try match fraction part:
            fpart, epart = "", ""
            if c == '.':
                istream.next()
                fpart = istream.matchplus(self.DIGIT)
                # Repeek:
                c = istream.peek(1)
            # Try match exponent part:
            if c in [ 'E', 'e' ]:
                istream.next()
                epart = istream.matchopt(['+', '-'], '+')
                epart += istream.matchplus(self.DIGIT)
            return GlapToken(GLAP_FLOAT, p, ipart, fpart, epart)
        # '0' - octal or hexadecimal number:
        istream.next()
        if istream.peek(1) in [ 'X', 'x' ]:
            istream.next()
            return GlapToken(
                GLAP_INT, p, GLAP_INT_HEX, istream.matchplus(self.XDIGIT)
            )
        return GlapToken(
            GLAP_INT, p, GLAP_INT_OCT, "0" + istream.matchmany(self.ODIGIT)
        )
    #-def

    def scan_CHAR(self, c, istream):
        """
        """

        # '\'' ( '\\' ESCAPE_SEQUENCE | CHARCHAR ) '\''
        p = istream.pos
        istream.next()
        c = istream.peek(1)
        if c == "":
            raise GlapLexError(istream, "Unexpected end of input")
        elif c == '\\':
            istream.next()
            ch = self.scan_ESCAPE_SEQUENCE(istream.peek(), istream)
        elif GlapLexer.CHARCHAR(c):
            ch = c
            istream.next()
        else:
            raise GlapLexError(istream, "Unexpected symbol %r" % c)
        istream.match('\'')
        return GlapToken(GLAP_CHAR, p, ch)
    #-def

    def scan_STR(self, c, istream):
        """
        """

        # '"' ( '\\' ESCAPE_SEQUENCE | STRCHAR )* '"'
        p = istream.pos
        istream.next()
        s = ""
        while True:
            c = istream.peek(1)
            if c in ("", '"'):
                break
            elif c == '\\':
                istream.next()
                s += self.scan_ESCAPE_SEQUENCE(istream.peek(), istream)
            elif GlapLexer.STRCHAR(c):
                s += c
                istream.next()
            else:
                raise GlapLexError(istream, "Unexpected symbol %r" % c)
        istream.match('"')
        return GlapToken(GLAP_STR, p, s)
    #-def

    def scan_ESCAPE_SEQUENCE(self, c, istream):
        """
        """

        # ESCAPECHAR
        # ODIGIT ODIGIT? ODIGIT?
        # 'x' XDIGIT{2}
        # 'u' XDIGIT{4}
        if c == "":
            raise GlapLexError(istream, "Unexpected end of input")
        elif c in self.ESCAPECHAR2CHAR:
            istream.next()
            return self.ESCAPECHAR2CHAR[c]
        elif c in self.ODIGIT:
            x = self.matchset(self.ODIGIT)
            x += self.matchopt(self.ODIGIT, "")
            x += self.matchopt(self.ODIGIT, "")
            return chr(int(x, 8))
        elif c == 'x':
            istream.next()
            return chr(int(self.matchn(self.XDIGIT, 2), 16))
        elif c == 'u':
            istream.next()
            return chr(int(self.matchn(self.XDIGIT, 4), 16))
        raise GlapLexError(istream, "Invalid symbol (%r) after '\\'" % c)
    #-def
#-class

class GlapParser(TagProgram):
    """
    """
    __slots__ = [ 'context' ]

    def __init__(self, context):
        """
        """

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
        lexer.match("module")
        t_ID = lexer.match(GLAP_ID)
        module_units = []
        while lexer.peek() and not lexer.test("end"):
            module_units.append(self.parse_module_unit(self, lexer, actions))
        lexer.match("end")
        return actions.run("module", self.context, t_ID, module_units)
    #-def

    def parse_module_unit(self, lexer, actions):
        """
        """

        # module_unit -> module | grammar | command
        t = lexer.peek()
        if not t:
            raise GlapSyntaxError(lexer, "Unexpected end of input")
        t = t.ttype
        if t == "module":
            return self.parse_module(lexer, actions)
        elif t == "grammar":
            return self.parse_grammar(lexer, actions)
        return self.parse_command(lexer, actions)
    #-def

    def parse_grammar(self, lexer, actions):
        """
        """

        # grammar -> "grammar" ID grammar_type_spec?
        #              ( rule | "." command )*
        #            "end"
        lexer.match("grammar")
        t_ID = lexer.match(GLAP_ID)
        grammar_type_spec = []
        if lexer.test("("):
            grammar_type_spec = self.parse_grammar_type_spec(lexer, actions)
        rules_and_commands = []
        while lexer.peek() and not lexer.test("end"):
            if lexer.test("."):
                lexer.next()
                rules_and_commands.append(self.parse_command(lexer, actions))
                continue
            rules_and_commands.append(self.parse_rule(lexer, actions))
        lexer.match("end")
        return actions.run("grammar",
            self.context, t_ID, grammar_type_spec, rules_and_commands
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
#-class

class __GlapParser(Parser):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Grammar.__init__(self)

        self['rule'] = (
          T('ID') % "lhs"
          + start_rule()
            + (T("->") | T(":") + set_alias_flag())
            + V('rule_rhs_expr') % "rhs"
          + end_rule()
          + T(";")
        )
        _ = lambda v: Return(str2id(v))
        _un = lambda x: Return(str2id("%s" % x)(str2id("lhs")))
        _bin = lambda x: Return(str2id("%s" % x)(*str2id("lhs rhs")))
        self['rule_rhs_expr'] = PrecedenceGraph(
          (0, (0, "|", 1), 1, _bin("RuleAltExpression")),
          (1, (1, "-", 2), 2, _bin("RuleExcludeExpression")),
          (2, (2, "", 3),  3, _bin("RuleConcatExpression")),
          (3, (3, "*", -1), 4, _un("RuleStarExpression")),
          (3, (3, "+", -1), 4, _un("RulePlusExpression")),
          (3, (3, "?", -1), 4, _un("RuleOptExpression")),
          (4, (-1, "-", 4), 5, _un("RuleDiscardExpression")),
          (4, (-1, "~", 4), 5, _un("RuleInvExpression")),
          (5, (6, "'", 6), 6, _bin("RuleLabelExpression")),
          (6, (-1, V('rule_rhs_expr_atom'), -1) -1, _("lhs"))
        )
        Epsilon = Return(str2id("Epsilon")())
        self['rule_rhs_expr_atom'] = (
          T('ID') % "i" + _("i")
          | T('STRING') % "s" + _("s")
          | V('char_or_range') % "cr" + _("cr")
          | T("eps") + Epsilon
          | V('action') % "a" + _("a")
          | T("(") + V('rule_rhs_expr_0') % "e" + T(")") + _("e")
        )
        def rule_range_literal():
            RuleRangeLiteral, a, b = str2id("RuleRangeLiteral a b")
            return Return(RangeLiteral(a, b))
        def rule_char_literal():
            CharLiteral, a = str2id("CharLiteral a")
            return Return(CharLiteral(a))
        self['char_or_range'] = (
            T('ID') % "a"
            + (
              T("..") + T('ID') % "b"
              + rule_range_literal()
            )['?']
            + rule_char_literal()
        )
        self['action'] = (
          T("{")
            + V('a_start') % "a"
          + T("}")
          + _("a")
        )
        # Command grammar:
        self['command'] = (
          V('c_expr') % "expr" + T('DELIM') + _("expr")
          | V('c_stmt') % "stmt" + T('DELIM') + _("stmt")
        )
        c_expr = PrecedenceGraph()
        self['c_expr'] = c_expr
        for op, act in [
            ("=", _bin("CmdAssignExpression")),
            ("+=", _bin("CmdInplaceAddExpression")),
            ("-=", _bin("CmdInplaceSubExpression")),
            ("*=", _bin("CmdInplaceMulExpression")),
            ("/=", _bin("CmdInplaceDivExpression")),
            ("%=", _bin("CmdInplaceModExpression")),
            ("&=", _bin("CmdInplaceBitAndExpression")),
            ("|=", _bin("CmdInplaceBitOrExpression")),
            ("^=", _bin("CmdInplaceBitXorExpression")),
            ("<<=", _bin("CmdInplaceBitShiftLeftExpression")),
            (">>=", _bin("CmdInplaceBitShiftRightExpression")),
            ("&&=", _bin("CmdInplaceAndExpression")),
            ("||=", _bin("CmdInplaceOrExpression")),
            (".=", _bin("CmdInplaceConcatExpression")),
            ("++=", _bin("CmdInplaceJoinExpression")),
            ("~~=" _bin("CmdInplaceMergeExpression"))
        ]:
            c_expr.add(0, (12, op, 0), 1, act)
        c_expr.add_more([
          (1, (1, "||", 2), 2, _bin("CmdOrExpression")),
          (2, (2, "&&", 3), 3, _bin("CmdAndExpression"))
        ])
        for op, act in [
            ("<", _bin("CmdLtExpression")),
            (">", _bin("CmdGtExpression")),
            ("<=", _bin("CmdLeExpression")),
            (">=", _bin("CmdGeExpression")),
            ("==", _bin("CmdEqExpression")),
            ("!=", _bin("CmdNeExpression")),
            ("===", _bin("CmdIsExpression")),
            ("in", _bin("CmdContainsExpression"))
        ]:
            c_expr.add(3, (4, op, 4), 4, act)
        c_expr.add_more([
          (4, (4, "|", 5), 5, _bin("CmdBitOrExpression")),
          (5, (5, "&", 6), 6, _bin("CmdBitAndExpression")),
          (6, (6, "^", 7), 7, _bin("CmdBitXorExpression"))
        ])
        for op, act in [
            ("<<", _bin("CmdBitShiftLeftExpression")),
            (">>", _bin("CmdBitShiftRightExpression"))
        ]:
            c_expr.add(7, (7, op, 8), 8, act)
        for op, act in [
            ("+", _bin("CmdAddExpression")),
            ("-", _bin("CmdSubExpression")),
            (".", _bin("CmdConcatExpression")),
            ("++", _bin("CmdJoinExpression")),
            ("~~", _bin("CmdMergeExpression"))
        ]:
            c_expr.add(8, (8, op, 9), 9, act)
        for op, act in [
            ("*", _bin("CmdMulExpression")),
            ("/", _bin("CmdDivExpression")),
            ("%", _bin("CmdModExpression"))
        ]:
            c_expr.add(9, (9, op, 10), 10, act)
        for op, act in [
            ("-", _un("CmdNegExpression")),
            ("!", _un("CmdNotExpression")),
            ("~", _un("CmdInvExpression"))
        ]:
            c_expr.add(10, (-1, op, 10), 11, act)
        def c_call_expr():
            CmdCallExpression, lhs, args = str2id("CmdCallExpression lhs args")
            return Return(CmdCallExpression(lhs, args))
        c_expr.add(11, (12, V('c_call_args') % "args", -1), 12, c_call_expr())
        for op in [ V('c_index_op'), V('c_access_op') ]:
            c_expr.add(12, (12, op, -1), 13)
        c_expr.add(13, (-1, V('c_expr_atom'), -1), -1)
        self['c_call_args'] = (
          V('c_expr_4')['+']
        )
        self['c_index_op'] = (
          T("[") + V('c_expr_0') + T("]")
        )
        self['c_access_op'] = (
          T(".") + T('ID')
        )
        self['c_expr_atom'] = (
          (T("$") | T("#"))['?'] + T('ID')
          | T("$(") + V('c_expr_1')['+'] + T(")")
          | T('INT')
          | T('FLOAT')
          | T('STRING')
          | V('c_pair')
          | V('c_list')
          | V('c_hash')
          | V('c_lambda')
          | T("(") + V('c_expr_0') + T(")")
        )
        self['c_pair'] = (
          T("(") + V('c_expr_1') + T(",") + V('c_expr_1') + T(")")
        )
        self['c_list'] = (
          T("[") + V('c_list_items')['?'] + T("]")
        )
        self['c_list_items'] = (
          V('c_expr_1') + (
            T(",") + V('c_expr_1')
          )['*']
        )
        self['c_hash'] = (
          T("[")
          + V('c_hash_item') + (
            T(",") + V('c_hash_item')
          )['*']
          + T("]")
        )
        self['c_hash_item'] = (
          V('c_expr_1') + T("=>") + V('c_expr_1')
        )
        self['c_lambda'] = (
          T("{") + T("|") + V('c_fargs') + T("|")
            + V('command')['*']
          + T("}")
        )
        self['c_fargs'] = (
          T('ID')['*'] + (T("...") + T('ID'))['?']
        )
        self['c_stmt'] = (
          V('c_defmacro')
          | V('c_define')
          | V('c_if')
          | V('c_foreach')
          | V('c_while')
          | V('c_dowhile')
          | T("break")
          | T("continue")
          | T("return") + V('c_expr_1')['?']
          | V('c_try')
          | T("throw") + V('c_expr_1') + V('c_expr_1')
          | T("rethrow") + V('c_expr_1')
        )
        self['c_block'] = (
          T("{") + V('command')['*'] + T("}")
        )
        self['c_defmacro'] = (
          T("defmacro") + T('ID') + T('ID')['*'] + T("(")
            + V('command')['*']
          + T(")")
        )
        self['c_define'] = (
          T("define") + T('ID') + V('c_fargs')
            + V('c_block')
        )
        self['c_if'] = (
          T("if") + V('c_expr_1')
            + V('c_block')
          + V('c_if_elif')['*']
          + V('c_if_else')['?']
        )
        self['c_if_elif'] = (
          T("elif") + V('c_expr_1') + V('c_block')
        )
        self['c_if_else'] = (
          T("else") + V('c_block')
        )
        self['c_foreach'] = (
          T("foreach") + T('ID') + V('c_expr_1')
            + V('c_block')
        )
        self['c_while'] = (
          T("while") + V('c_expr_1')
            + V('c_block')
        )
        self['c_dowhile'] = (
          T("do")
            + V('c_block')
          T("while") + V('c_expr_1')
        )
        self['c_try'] = (
          T("try")
            + V('c_block')
          + V('c_try_catch')['*']
          + V('c_try_finally')['?']
        )
        self['c_try_catch'] = (
          T("catch") + T('ID') + T('ID')['?']
            + V('c_block')
        )
        self['c_try_finally'] = (
          T("finally")
            + V('c_block')
        )
        # Action grammar:
        self['a_start'] = (
          V('a_stmt')['*']
        )
        self['a_stmt'] = (
          V('a_block')
          | V('a_assign')
          | V('a_if')
          | V('a_case')
          | V('a_for')
          | V('a_while')
          | V('a_dowhile')
          | T("break") + T(";")
          | T("continue") + T(";")
          | T("return") + V('a_expr')['?'] + T(";")
        )
        self['a_block'] = (
          T("{") + V('a_stmt')['*'] + T("}")
        )
        self['a_assign_op'] = (
          T("=")
          | T("+=")
          | T("-=")
          | T("*=")
          | T("/=")
          | T("%=")
          | T("&=")
          | T("|=")
          | T("^=")
          | T("<<=")
          | T(">>=")
        )
        self['a_assign'] = (
          V('a_lexpr') + V('a_assign_op') + V('a_expr') + T(";")
        )
        self['a_if'] = (
          T("if") + V('a_expr')
            + V('a_block')
          + V('a_elif')['*']
          + V('a_else')['?']
        )
        self['a_elif'] = (
          T("elif") + V('a_expr')
            + V('a_block')
        )
        self['a_else'] = (
          T("else")
            + V('a_block')
        )
        self['a_case'] = (
          T("case") + V('a_expr') + T("of") + T("{")
            + V("a_cases")['*']
            + V("a_default")['?']
          + T("}")
        )
        self['a_cases'] = (
          V('a_expr') + T(":")
            + V('a_stmt')['*']
        )
        self['a_default'] = (
          T("default") + T(":")
            + V('a_stmt')['*']
        )
        self['a_for'] = (
          T("for") + T('ID') + T(":") + V('a_expr')
            + V('a_block')
        )
        self['a_while'] = (
          T("while") + V('a_expr')
            + V('a_block')
        )
        self['a_dowhile'] = (
          T("do")
            + V('a_block')
          + T("while")
        )
        a_lexpr = PrecedenceGraph()
        self['a_lexpr'] = a_lexpr
        for op in [ V('a_index_op'), V('a_access_op') ]:
            a_lexpr.add(0, (0, op, -1), 1)
        a_lexpr.add(1, (-1, V('a_lexpr_atom'), -1), -1)
        self['a_lexpr_atom'] = (
          T('ID')
          | T("(") + V('a_expr_0') + T(")") + (
              V('a_index_op') | V('a_access_op')
            )
        )
        a_expr = PrecedenceGraph()
        self['a_expr'] = a_expr
        a_expr.add_more([
          (0, (0, "||", 1), 1),
          (1, (1, "&&", 2), 2)
        ])
        for op in [ "<", ">", "<=", ">=", "==", "!=" ]:
            a_expr.add(2, (3, op, 3), 3)
        a_expr.add_more([
          (3, (3, "|", 4), 4),
          (4, (4, "&", 5), 5),
          (5, (5, "^", 6), 6)
        ])
        for op in [ "<<", ">>" ]:
            a_expr.add(6, (6, op, 7), 7)
        for op in [ "+", "-" ]:
            a_expr.add(7, (7, op, 8), 8)
        for op in [ "*", "/", "%" ]:
            a_expr.add(8, (8, op, 9), 9)
        for op in [ "-", "~", "!" ]:
            a_expr.add(9, (-1, op, 9), 10)
        for op in [ V('a_call_op'), V('a_index_op'), V('a_access_op') ]:
            a_expr.add(10, (10, op, -1), 11)
        a_expr.add(11, (-1, V('a_expr_atom'), -1), -1)
        self['a_call_op'] = (
          T("(") + V('a_call_args')['?'] + T(")")
        )
        self['a_call_args'] = (
          V('a_expr_0') + (T(",") + V('a_expr_0'))['*']
        )
        self['a_index_op'] = (
          T("[") + V('a_expr_0') + T("]")
        )
        self['a_access_op'] = (
          T(".") + T('ID')
        )
        self['a_expr_atom'] = (
          T('ID')
          | T('INT')
          | T('FLOAT')
          | T('STRING')
          | T("(") + V('a_expr_0') + T(")")
        )
    #-def
#-class
