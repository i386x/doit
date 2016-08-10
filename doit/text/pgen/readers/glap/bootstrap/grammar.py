#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/bootstrap/grammar.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-11 10:19:52 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
GLAP lexers and parsers definitions.\
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

class GlapLexer(Lexer):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Lexer.__init__(self)

        self['COMMENT']    = S('-') + S('-') + V('COMMENTCHAR')['*']
        self['WS']         = V('WHITESPACE')['+']
        self['ID']         = V('LETTER_') + V('ALNUM_')['*']
        self['INT']        = V('INT_PART')
                           | (S('0') + V('ODIGIT')['*'])
                           | S('0') + (S('x') | S('X'))
                             + V('XDIGIT')['+']
        self['FLOAT']      = V('INT_PART') + V('FLOAT_PART')
        self['INT_PART']   = V('NZ_DIGIT') + V('DIGIT')['*']
        self['FLOAT_PART'] = V('FRAC_PART') + V('EXP_PART')['?']
                           | V('EXP_PART')
        self['FRAC_PART']  = S('.') + V('DIGIT')['+']
        self['EXP_PART']   = (S('E') | S('e'))
                             + (S('+') | S('-'))['?']
                             + V('DIGIT')['+']

        self['ALNUM_']      = A(  V('LETTER_') | V('DIGIT')           )
        self['LETTER_']     = A(  R('A', 'Z') | R('a', 'z') | S('_')  )
        self['DIGIT']       = A(  S('0') | V('NZDIGIT')               )
        self['NZ_DIGIT']    = A(  R('1', '9')                         )
        self['WHITESPACE']  = A(  S(' ') | S('\n')                    )
        self['COMMENTCHAR'] = A(  V('SOURCECHAR') - S('\n')           )
        self['SOURCECHAR']  = A(  ~(R('\0', '\37') | S('\177'))       )

        self.set_code([
            Call(GetLocal('tokens'),
                Call(GetLocal('lexskip'), 'COMMENT'),
                Call(GetLocal('lexskip'), 'WS'),
                'ID',
                'INT',
                'FLOAT',
                Expand(GetLocal('str2tok')),
                Expand(GetLocal('other'))
            )
        ])
    #-def
#-class

class GlapParser(Parser):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Grammar.__init__(self)

        def start_module():
            m, factory, name = str2id("m factory name")
            return Assign(m, factory._NewModule(name))

        def add_to_module():
            m, munit = str2id("m munit")
            return m._add(munit)

        def end_module():
            m = str2id("m")
            return Block(
                m._commit(),
                Return(m)
            )

        def start_grammar():
            g, factory, name, gtspec = str2id("g factory name gtspec")
            return Assign(g, factory._NewGrammar(name, gtspec))

        def add_r_to_g():
            g, r = str2id("g r")
            return g._add(r)

        def add_cmd_to_g():
            g, cmd = str2id("g cmd")
            return g._add(cmd)

        def end_grammar():
            g = str2id("g")
            return Block(
                g._commit(),
                Return(g)
            )

        def start_gts_list():
            gts_list, factory = str2id("gts_list factory")
            return Assign(gts_list, factory._NewGTSList())

        def add_gts_to_gts_list():
            gts_list, name = str2id("gts_list name")
            return gts_list._add(name)

        def end_gts_list():
            gts_list = str2id("gts_list")
            return Block(
                gts_list._commit(),
                Return(gts_list)
            )

        def start_rule():
            r, factory, lhs = str2id("r factory lhs")
            return Assign(r, factory._NewRule(lhs))

        def set_alias_flag():
            r = str2id("r")
            true = BoolLiteral(True)
            return r._set_alias_flag(true)

        def end_rule():
            r, rhs = str2id("r rhs")
            return Block(
                r._add(rhs),
                r._commit(),
                Return(r)
            )

        self['start'] = (
            V('module')
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
        self['rule'] = (
          T('ID') % "lhs"
          + start_rule()
            + (T("->") | T(":") + set_alias_flag())
            + V('rule_rhs_expr') % "rhs"
          + end_rule()
          + T(";")
        )
        self['rule_rhs_expr'] = PrecedenceGraph(
          (0, (0, "|", 1), 1),
          (1, (1, "-", 2), 2),
          (2, (2, "", 3),  3),
          (3, (3, "*"),    4),
          (3, (3, "+"),    4),
          (3, (3, "?"),    4),
          (4, ("-", 4),    5),
          (4, ("~", 4),    5),
          (5, (6, "'", 6), 6),
          (6, (T('ID'),),   -1),
          (6, (T('STRING'),), -1),
          (6, (V('char_or_range'),), -1),
          (6, (T("eps"),), -1),
          (6, (V('action'),), -1),
          (6, ("(", 0, ")"), -1)
        )
        self['char_or_range'] = (
            T('ID')
            + push_token()
            + (
              T("..") + T('ID')
              + push_token_and_range_mark()
            )['?']
            + make_range_literal()
        )
        self['action'] = (
          T("{")
          + start_action()
            + V('act_start')
          + end_action()
          + T("}")
        )
        self['command'] = (
          V('c_expr') + T('DELIM')
        )
        self['c_expr'] = PrecedenceGraph(
          (0, (0, "=", 1), 1),
          (0, (0, "+=", 1), 1),
          (0, (0, "-=", 1), 1),
          (0, (0, "*=", 1), 1),
          (0, (0, "/=", 1), 1),
          (0, (0, "%=", 1), 1),
          (0, (0, "&=", 1), 1),
          (0, (0, "|=", 1), 1),
          (0, (0, "^=", 1), 1),
          (0, (0, "<<=", 1), 1),
          (0, (0, ">>=", 1), 1),
          (0, (0, "&&=", 1), 1),
          (0, (0, "||=", 1), 1),
          (0, (0, ".=", 1), 1),
          (0, (0, "++=", 1), 1),
          (0, (0, "~~=", 1), 1),
        )
    #-def
#-class
