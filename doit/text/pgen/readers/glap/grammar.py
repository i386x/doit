#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/grammar.py
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

GAC = GrammarAdjustmentCommand
GAP = GrammarAdjustmentParam
GAA = GrammarActionCommand
GAM = GrammarActionMacro

class GlapLexer(Grammar):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Grammar.__init__(self)
        self.set_name(self.__class__.__name__)

        self['COMMENT']    = S('-') + S('-') + V('COMMENTCHAR')['*']
        self['ID']         = V('LETTER_') + V('ALNUM_')['*']
        self['INT']        = V('INT_PART')
                           | (S('0') + V('ODIGIT')['*']) % "odigs"
                           | S('0') + (S('x') | S('X'))
                             + V('XDIGIT')['+'] % "xdigs"
        self['FLOAT']      = V('INT_PART') % "idigs" + V('FLOAT_PART')
        self['INT_PART']   = V('NZ_DIGIT') + V('DIGIT')['*']
        self['FLOAT_PART'] = V('FRAC_PART') + V('EXP_PART')['?']
                           | V('EXP_PART')
        self['FRAC_PART']  = S('.') + V('DIGIT')['+'] % "fdigs"
        self['EXP_PART']   = (S('E') | S('e'))
                             + (S('+') | S('-'))['?'] % "sign"
                             + V('DIGIT')['+'] % "expdigs"

        self['ALNUM_']      = A(  V('LETTER_') | V('DIGIT')           )
        self['LETTER_']     = A(  R('A', 'Z') | R('a', 'z') | S('_')  )
        self['DIGIT']       = A(  S('0') | V('NZDIGIT')               )
        self['NZ_DIGIT']    = A(  R('1', '9')                         )
        self['WHITESPACE']  = A(  S(' ') | S('\n')                    )
        self['COMMENTCHAR'] = A(  V('SOURCECHAR') - S('\n')           )
        self['SOURCECHAR']  = A(  ~(R('\0', '\37') | S('\177'))       )

        self.set_grammar_adjustment_program("Lexer", [
            (GAC.Import, (".", "GlapParser", "GetOperators"), "GetOperators"),

            (GAC.SetMatchedContentVariableName, "s"),
            (GAC.SetMatchedSymbolVariableName, "c"),
            (GAC.SetGenericInitialAction, [
                (GAA.SetVar, GAM.MatchedContentVariableName, String(""))
            ]),
            (GAC.SetGenericFinalAction, [
                (GAA.Emit, GAM.CurrentRuleName, GAM.MatchedContentVariableName)
            ]),
            (GAC.SetErrorAction, [
                (GAA.Emit, 'OTHER', GAM.MatcheSymbolVariableName)
            ]),

            (GAC.AddToken, 'WHITESPACE', GAP.Skip),
            (GAC.AddToken, 'COMMENT', GAP.Skip),
            (GAC.AddToken, 'ID', GAP.Emit),
            (GAC.AddToken, 'INT', GAP.Emit),
            (GAC.AddToken, 'FLOAT', GAP.Emit),
            (GAC.Invoke, "GetOperators", GAM.This),
            (GAC.SetInitialAction, 'INT', [
                (GAA.SetVar, "s", String("")),
                (GAA.SetVar, "base", Id('DEC'))
            ]),
            (GAC.SetActionByLabel, 'INT', "odigs", [
                (GAA.SetVar, "base", Id('OCT'))
            ]),
            (GAC.SetActionByLabel, 'INT', "xdigs", [
                (GAA.SetVar, "base", Id('HEX'))
            ]),
            (GAC.SetFinalAction, 'INT', [
                (GAA.Emit, 'INT', "s", "base")
            ]),
            (GAC.SetFinalAction, 'FLOAT', [
                (GAA.Emit, 'FLOAT', "idigs", "fdigs", "sign", "expdigs")
            ])
        ])
    #-def
#-class

class GlapParser(Grammar):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Grammar.__init__(self)
        self.set_name(self.__class__.__name__)

        self['start'] = (
            V('module')
        )
        self['module'] = (
            T("module") + T('ID') % "name"
              + start_module()
              + V('module_unit')['*']
              + end_module()
            + T("end")
        )
        self['module_unit'] = (
            V('grammar')
        )
        self['grammar'] = (
            T("grammar") + T('ID') % "name"
            + V('grammar_type_spec')['?']
              + start_grammar()
              + V('rule')['*']
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
          start_rule()
          + T('ID')
            + (T("->") | T(":") + set_alias_flag())
            + V('rule_rhs_expr')
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
            + V('GlapActionParser', 'start')
          + end_action()
          + T("}")
        )

        def is_str_ge(s, sz):
            return (GAO.And,
                (GAO.Type, s, GLT.String),
                (GAO.GtEq, (GAO.Strlen, s), sz),
            )
        #-def

        def trans

        self.set_grammar_adjustment_program("Parser", [
            (GAC.Define, "GetOperators", "lexer", [
                (GAC.ForEach, "r", GAM.Rules, [
                    (GAC.Visit, "r", "n", [
                        (GAC.If, (GAC.Expr, is_str_ge("n", 2)), [
                            (GAC.With, "lexer", [
                                (GAC.AddRule, trans("n"), makerhs("n")),
                                (GAC.AddToken, trans("n"), GAP.Emit)
                            ])
                        ])
                    ])
                ])
            ])
        ])
    #-def
#-class

def module():
    """
    """

    return None
#-def
