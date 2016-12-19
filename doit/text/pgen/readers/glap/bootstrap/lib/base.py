#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/lib/base.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-07-12 22:35:19 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Glap common and auxiliary functions and modules.\
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

from doit.text.pgen.models.cfgram import \
    Grammar as CFGrammar

class GlapCodeStorageUnit(object):
    """
    """
    __slots__ = [ '__name', '__code' ]

    def __init__(self):
        """
        """

        self.__name = self.__class__.__name__
        self.__code = []
    #-def

    def set_name(self, name):
        """
        """

        self.__name = name
    #-def

    def name(self):
        """
        """

        return self.__name
    #-def

    def set_code(self, code):
        """
        """

        self.__code = code
    #-def

    def code(self):
        """
        """

        return self.__code
    #-def
#-class

class Module(GlapCodeStorageUnit):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        GlapCodeStorageUnit.__init__(self)
    #-def

    def constructor(self):
        """
        """

        return [DefModule(self.name(), self.code())]
    #-def
#-class

class Grammar(Module, CFGrammar):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Module.__init__(self)
        CFGrammar.__init__(self)
    #-def

    def constructor(self):
        """
        """

        return [
            DefModule(
                self.name(),
                [SetMember(GetLocal("this"), "grammar", self.clone())] \
                + self.code()
            )
        ]
    #-def
#-class

class Lexer(Grammar):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Grammar.__init__(self)

        self.set_code([
            SetProp("matched_symbol_variable_name", "c"),
            SetProp("matched_result_variable_name", "s"),
            SetProp("other_action", None),

            # defmacro str2tok ({|x| return (call $x:parser:GatherTokens)}
            #   $this
            # )
            DefMacro("str2tok", [], [
                _n(Call,
                    _n(Lambda, _a(['x']), _a(False), _s(
                        _n(Return, _n(Call,
                            _n(GetMember,
                                _n(GetMember,
                                    _n(GetLocal, _a('x')), _a('parser')
                                ),
                                _a('GatherTokens')
                            )
                        ))
                    ), _a([])),
                    _n(GetLocal, _a('this'))
                )
            ]),

            # defmacro other (lexother OTHER)
            DefMacro("other", [], [
                _n(Call, _a('lexother'), _a('OTHER'))
            ]),

            # define tokens ...toks {
            #   foreach t $toks {
            #     if (type t === List) {
            #       apply tokens $t
            #       continue
            #     }
            #     install_actions $t
            #   }
            # }
            Define("tokens", ['toks'], ['t'], True, [
                Foreach('t', GetLocal('toks'), [
                    If(Is(Type(GetLocal('t')), GetLocal('List')), [
                        Apply(GetLocal('tokens'), GetLocal('t')),
                        Continue()
                    ], []),
                    Call(GetLocal('install_actions'), GetLocal('t'))
                ])
            ]),

            # define install_actions t {
            #   if (type $t === String) {
            #     addtoken $t
            #     add_emit_action $t (mknode '{}'
            #       (build_emit_action $t)
            #     )
            #   }
            #   else if (type $t === Pair) {
            #     attr = first $t
            #     tname = second $t
            #
            #     assert (type $tname === String)
            #
            #     if ($attr == LEX_SKIP) {
            #       add_emit_action $tname (mknode '{}'
            #         (call build_skip_action)
            #       )
            #     }
            #     else if ($attr == LEX_OTHER) {
            #       addtoken $tname
            #       set_other_action (mknode '{}'
            #         (build_other_action $tname)
            #       )
            #     }
            #     else {
            #       throw ValueError "Unknown attribute"
            #     }
            #   }
            #   else {
            #     throw TypeError "'t' must be String or Pair"
            #   }
            # }
            Define("install_actions", ['t'], ['attr', 'tname'], False, [
                If(Is(Type(GetLocal('t')), GetLocal('String')), [
                    AddToken(GetLocal('t')),
                    Call('add_emit_action', GetLocal('t'), MkNode('{}',
                        Call('build_emit_action', GetLocal('t'))
                    ))
                ], [If(Is(Type(GetLocal('t')), GetLocal('Pair')), [
                    SetLocal('attr', First(GetLocal('t'))),
                    SetLocal('tname', Second(GetLocal('t'))),

                    Assert(Is(Type(GetLocal('tname')), GetLocal('String'))),

                    If(Eq(GetLocal('attr'), GetLocal('LEX_SKIP')), [
                        Call('add_emit_action', GetLocal('tname'), MkNode('{}',
                            Call('build_skip_action')
                        )
                    ], [If(Eq(GetLocal('attr'), GetLocal('LEX_OTHER')), [
                        AddToken(GetLocal('tname')),
                        Call('set_other_action', MkNode('{}',
                            Call('build_other_action', GetLocal('tname'))
                        )
                    ], [
                        Throw(GetLocal('ValueError'), "Unknown attribute")
                    ])])
                ], [
                    Throw(GetLocal('TypeError'), "'t' must be String or Pair")
                ])])
            ]),

            # define add_emit_action rname anode {
            #   rule = getrule $this:grammar $rname
            #   rule = mknode '.' $rule $anode
            #   addrule $this:grammar $rname $rule
            # }
            Define("add_emit_action", ['rname', 'anode'], ['rule'], False, [
                SetLocal('rule', GetRule(
                    GetMember(GetLocal('this'), 'grammar'), GetLocal('rname')
                )),
                SetLocal('rule', MkNode('.',
                    GetLocal('rule'), GetLocal('anode')
                )),
                AddRule(GetMember(GetLocal('this'), 'grammar'),
                    GetLocal('rname'), GetLocal('rule')
                ))
            ]),

            # define set_other_action anode {
            #   setprop 'other_action' $anode
            # }
            Define("set_other_action", ['anode'], [], False, [
                SetProp("other_action", GetLocal('anode'))
            ]),

            # define build_emit_action tname {
            #   Id_emit
            # }
            # build_skip_action
            # build_other_action

        ])
    #-def
#-class

class Base(Module):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Module.__init__(self)

        self.set_code([
            SetLocal('symbol2name', NewHashMap(
                NewPair("!", "XM"),
                NewPair("\"", "DQ"),
                NewPair("#", "HASH"),
                NewPair("$", "DOLLAR"),
                NewPair("%", "PERC"),
                NewPair("&", "AMP"),
                NewPair("'", "SQ"),
                NewPair("(", "LPAREN"),
                NewPair(")", "RPAREN"),
                NewPair("*", "AST"),
                NewPair("+", "PLUS"),
                NewPair(",", "COMMA"),
                NewPair("-", "DASH"),
                NewPair(".", "DOT"),
                NewPair("/", "SLASH"),
                NewPair(":", "COLON"),
                NewPair(";", "SEMI"),
                NewPair("<", "LT"),
                NewPair("=", "EQ"),
                NewPair(">", "GT"),
                NewPair("?", "QM"),
                NewPair("@", "AT"),
                NewPair("[", "LBRACK"),
                NewPair("\\", "BSLASH"),
                NewPair("]", "RBRACK"),
                NewPair("^", "CIRC"),
                NewPair("_", "USCORE"),
                NewPair("`", "BQ"),
                NewPair("{", "LBRACE"),
                NewPair("|", "VBAR"),
                NewPair("}", "RBRACE"),
                NewPair("~", "TILDE")
            ),

            # define qsyms x {
            #   result = ""
            #
            #   foreach c $x {
            #     if (isalnum $c) {
            #       result .= $c
            #     }
            #     else {
            #       result .= "_" . $this:symbol2name[$c]
            #     }
            #   }
            #   if ($result && $result[0] == "_") {
            #     result = (tail $result)
            #   }
            #   return $result
            # }
            Comm("""
            Translates symbols in `x` to their alphanumeric short names
            """,
            Define("qsyms", ["x"], ["result", "c"], False, [
                SetLocal("result", ""),

                Foreach("c", GetLocal("x"), [
                    If(IsAlnum(GetLocal("c")), [
                        SetLocal("result",
                            Concat(GetLocal("result"), GetLocal("c"))
                        )
                    ], [
                        SetLocal("result", Concat(
                            GetLocal("result"),
                            Concat("_", GetItem(
                                GetMember(GetLocal("this"), "symbol2name"),
                                GetLocal("c")
                            )
                        )
                    ])
                ]),
                If(And(
                    GetLocal("result"), Eq(GetItem(GetLocal("result"), 0), "_")
                ), [
                    SetLocal("result", Tail(GetLocal("result")))
                ], []),
                Return(GetLocal("result"))
            ])),

            DefGrammar(Lexer()),
            DefGrammar(Parser())
        ])
    #-def
#-class
