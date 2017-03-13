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
GLAP lexers and parsers definitions.\
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

class GlapLexer(TagProgram):
    """
    """
    __slots__ = []

    def __init__(self, envclass):
        """
        """

        icc = TagICCompiler()

        M = icc.symbol_table().macro_factory()
        L = icc.symbol_table().label_factory()

        NOTEOF = lambda c: c is not None
        ASCIICHAR = lambda c: ord(' ') <= ord(c) and ord(c) <= ord('~')
        COMMENTCHAR = lambda c: NOTEOF(c) and (ASCIICHAR(c) or ord(c) >= 128)
        SOURCECHAR = lambda c: c == '\n' or COMMENTCHAR(c)
        icc.define('ODIGIT', ('1', '7'))
        icc.define('NZ_DIGIT', ('1', '9'))
        icc.define('DIGIT', '0', M.NZ_DIGIT)
        icc.define('XDIGIT', M.DIGIT, ('a', 'f'), ('A', 'F'))
        icc.define('LETTER_', ('A', 'Z'), ('a', 'z'), '_')
        icc.define('ALNUM_', M.DIGIT, M.LETTER_)
        CHARCHAR = lambda c: COMMENTCHAR(c) and c not in ("'", "\\")
        STRCHAR = lambda c: COMMENTCHAR(c) and c not in ('"', '\\')
        icc.define('ESCAPECHAR', "abtnvfr\"'\\")

        TagProgram.__init__(self, 'glap_lexer', envclass, icc.compile([
          # Start state:
          L._start,
            BRANCH       (L._switch_table),
          L._eof,
            HALT,
          L._switch_table,
            SYMBOL       ('-',        L._comment_or_minus),
            SYMBOL       (' ',        L._whitespace),
            SYMBOL       ('\n',       L._newline),
            SET          (M.LETTER_,  L._id),
            SET          (M.NZ_DIGIT, L._int_part),
            SYMBOL       ('0',        L._oct_or_hex_int),
            SYMBOL       ("'",        L._char),
            SYMBOL       ('"',        L._str),
            DEFAULT      (L._other),
            EOF          (L._eof),
            NULL,
          L._restart,
            PAUSE,
            JUMP         (L._start),
          # COMMENT -> "--" COMMENTCHAR*
          L._comment_or_minus,
            SKIP         ('-'),
            TEST         ('-'),
            JFALSE       (L._minus),
            SKIP         ('-'),
            SKIP_MANY    (COMMENTCHAR),
            JUMP         (L._start),
          L._minus,
            CALL         (self.emit_minus),
            JUMP         (L._restart),
          # WS -> (' ' | '\n')*
          L._whitespace,
            SKIP_MANY    (' '),
            JUMP         (L._start),
          L._newline,
            SKIP         ('\n'),
            CALL         (self.advance_lineno),
            JUMP         (L._start),
          # ID -> LETTER_ ALNUM_*
          L._id,
            MATCH        (M.LETTER_),
            PUSH_MATCH,
            MATCH_MANY   (M.ALNUM_),
            CONCAT       (STK, ACC),
            CALL         (self.emit_id),
            JUMP         (L._restart),
          # INT -> INT_PART
          # INT -> "0" ODIGIT*
          # INT -> "0" [Xx] XDIGIT+
          # FLOAT -> INT_PART FLOAT_PART
          #
          # INT -> "0" (ODIGIT* | [Xx] XDIGIT+)
          L._oct_or_hex_int,
            MATCH        ('0'),
            TEST         (['X', 'x']),
            JTRUE        (L._hex_int),
            PUSH_MATCH,
            MATCH_MANY   (M.ODIGIT),
            CONCAT       (STK, ACC),
            CALL         (self.emit_oct_int),
            JUMP         (L._restart),
          L._hex_int,
            SKIP         (['X', 'x']),
            MATCH_PLUS   (M.XDIGIT),
            CALL         (self.emit_hex_int),
            JUMP         (L._restart),
          # INT_PART -> NZ_DIGIT DIGIT*
          L._int_part,
            MATCH        (M.NZ_DIGIT),
            PUSH_MATCH,
            MATCH_MANY   (M.DIGIT),
            CONCAT       (STK, ACC),
            TEST         ('.'),
            JTRUE        (L._float_part),
            CALL         (self.emit_int),
            JUMP         (L._restart),
          # FLOAT_PART -> FRAC_PART EXP_PART?
          # FLOAR_PART -> EXP_PART
          #
          # FRAC_PART -> "." DIGIT+
          L._float_part,
            SKIP         ('.'),
            MATCH_PLUS   (M.DIGIT),
            PUSH_MATCH,
            TEST         (['e', 'E']),
            JTRUE        (L._exp_part),
            PUSH         ([]), # no sign
            PUSH         ([]), # no exp
            CALL         (self.emit_float),
            JUMP         (L._restart),
          # EXP_PART -> [Ee] [+-]? DIGIT+
          L._exp_part,
            SKIP         (['e', 'E']),
            MATCH_OPT    (['+', '-']),
            PUSH_MATCH,
            MATCH_PLUS   (M.DIGIT),
            PUSH_MATCH,
            CALL         (self.emit_float),
            JUMP         (L._restart),
          # CHAR -> "'" ("\\" ESCAPE_SEQUENCE | CHARCHAR) "'"
          L._char,
            SKIP         ("'"),
            TEST         ('\\'),
            JFALSE       (L._charchar),
            SKIP         ('\\'),
            CALL         (L._escape_sequence),
            JUMP         (L._char_finish),
          L._charchar,
            MATCH        (CHARCHAR),
            PUSH_MATCH,
          L._char_finish,
            SKIP         ("'"),
            CALL         (self.emit_char),
            JUMP         (L._restart),
          # STR -> '"' ('\\' ESCAPE_SEQUENCE | STRCHAR)* '"'
          L._str,
            SKIP         ('"'),
            PUSH         (""),
          L._str_loop,
            TEST         ('"'),
            JTRUE        (L._str_finish),
            TEST         ('\\'),
            JFALSE       (L._strchar),
            SKIP         ('\\'),
            CALL         (L._escape_sequence),
            JUMP         (L._str_addchar),
          L._strchar,
            MATCH        (STRCHAR),
            PUSH_MATCH,
          L._str_addchar,
            CONCAT       (STK, STK),
            JUMP         (L._str_loop),
          L._str_finish,
            SKIP         ('"'),
            CALL         (self.emit_str),
            JUMP         (L._restart),
          # ESCAPE_SEQUENCE -> ESCAPE_CHAR
          # ESCAPE_SEQUENCE -> ODIGIT+
          # ESCAPE_SEQUENCE -> "x" XDIGIT+
          # ESCAPE_SEQUENCE -> "u" XDIGIT XDIGIT XDIGIT XDIGIT
          L._escape_sequence,
            BRANCH       (L._escape_swt),
            FAIL         ("One of [abtnvfr'\"\\0-7xu] was expected"),
          L._escape_swt,
            SET          (M.ESCAPECHAR, L._escape_char),
            SET          (M.ODIGIT, L._oct_escape),
            SYMBOL       ('x', L._hex_escape),
            SYMBOL       ('u', L._unicode_escape),
            NULL,
          L._escape_char,
            MATCH        (M.ESCAPECHAR),
            CALL         (self.contribute_escapechar),
            RETURN,
          L._oct_escape,
            MATCH_PLUS   (M.ODIGIT),
            CALL         (self.contribute_oct_char),
            RETURN,
          L._hex_escape,
            SKIP         ('x'),
            MATCH_PLUS   (M.XDIGIT),
            CALL         (self.contribute_hex_char),
            RETURN,
          L._unicode_escape,
            SKIP         ('u'),
            MATCH        (M.XDIGIT),
            PUSH_MATCH,
            MATCH        (M.XDIGIT),
            PUSH_MATCH,
            MATCH        (M.XDIGIT),
            PUSH_MATCH,
            MATCH        (M.XDIGIT),
            PUSH_MATCH,
            CALL         (self.contribute_unicode_char),
            RETURN,
          # OTHER -> SOURCECHAR
          L._other,
            MATCH        (SOURCECHAR),
            CALL         (self.emit_other),
            JUMP         (L._restart)
        ]))
    #-def

    def advance_lineno(self, te):
        """
        """
    #-def
#-class


class GlapParser(TagProgram):
    """
    """
    __slots__ = []

    def __init__(self, envclass):
        """
        """

        TagProgram.__init__(self, 'glap_parser', envclass)
        self.compile([
          # start -> module
          L._start,
            PARSE (L._module),
            HALT,
          # module -> "module" ID module_unit* "end"
          L._module,
            SKIP  (GLAP_KW_MODULE),
            MATCH (GLAP_ID),
            PUSH_MATCH,
            PUSH  ([]),
          L._module_1,
            TEST  (GLAP_KW_END),
            JTRUE (L._module_2),
            PARSE_MANY  (L._module_unit),
            JOIN  (STK, STK),
            JUMP  (L._module_1),
          L._module_2,
            SKIP  (GLAP_KW_END),
            CALL  (self.make_module),
            RETURN

    def parse(self):
        """
        """

        self.parse_module()
    #-def

    def parse_module(self):
        """
        """

        t = self.__input.peek()
        if t.ttype != "module":

class __GlapParser(Parser):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Grammar.__init__(self)

        self['start'] = (
            V('module')
        )
        def start_module():
            m, NewModule, name = str2id("m NewModule name")
            return Assign(m, NewModule(name))
        def add_to_module():
            AddToModule, m, munit = str2id("AddToModule m munit")
            return AddToModule(m, munit)
        def end_module():
            FinishModule, m = str2id("FinishModule m")
            return Block(
                FinishModule(m),
                Return(m)
            )
        self['module'] = (
            T("module") + T('ID') % "name"
              + start_module()
              + (
                V('module_unit') % "munit"
                + add_to_module()
              )['*']
              + end_module()
            + T("end")
        )
        self['module_unit'] = (
            V('command')
            | V('module')
            | V('grammar')
        )
        def start_grammar():
            g, NewGrammar, name, gtspec = str2id("g NewGrammar name gtspec")
            return Assign(g, NewGrammar(name, gtspec))
        def add_r_to_g():
            AddToGrammar, g, r = str2id("AddToGrammar g r")
            return AddToGrammar(g, r)
        def add_cmd_to_g():
            AddToGrammar, g, cmd = str2id("AddToGrammar g cmd")
            return AddToGrammar(g, cmd)
        def end_grammar():
            FinishGrammar, g = str2id("FinishGrammar g")
            return Block(
                FinishGrammar(g),
                Return(g)
            )
        self['grammar'] = (
            T("grammar") + T('ID') % "name"
            + V('grammar_type_spec')['?'] % "gtspec"
              + start_grammar()
              + (
                V('rule') % "r" + add_r_to_g()
                | T(".") + V('command') % "cmd" + add_cmd_to_g()
              )['*']
              + end_grammar()
            + T("end")
        )
        def start_gts_list():
            gts_list, NewGTSList = str2id("gts_list NewGTSList")
            return Assign(gts_list, NewGTSList())
        def add_gts_to_gts_list():
            AddToGTSList, gts_list, name = str2id("AddToGTSList gts_list name")
            return AddToGTSList(gts_list, name)
        def end_gts_list():
            FinishGTSList, gts_list = str2id("FinishGTSList gts_list")
            return Block(
                FinishGTSList(gts_list),
                Return(gts_list)
            )
        self['grammar_type_spec'] = (
            T("(")
              + start_gts_list()
              + (
                V('ID') % "name"
                + add_gts_to_gts_list()
                + (
                  T(",") + V('ID') % "name"
                  + add_gts_to_gts_list()
                )['*']
              )['?']
              + end_gts_list()
            + T(")")
        )
        def start_rule():
            r, NewRule, lhs = str2id("r NewRule lhs")
            return Assign(r, NewRule(lhs))
        def set_alias_flag():
            SetAliasFlag, r = str2id("SetAliasFlag r")
            return SetAliasFlag(r, BoolLiteral(True))
        def end_rule():
            FinishRule, SetRhs, r, rhs = str2id("FinishRule SetRhs r rhs")
            return Block(
                SetRhs(r, rhs),
                FinishRule(r),
                Return(r)
            )
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
