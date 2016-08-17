#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_fmt/test_format.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-11 15:55:31 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Formatter tests.\
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

import unittest

from doit.text.fmt.format import \
    FormatError, \
    TextBlock as _b, TextTerminal as _t, \
    Var as _V, Term as _T, \
    Indent, Dedent, Space, LineBreak as _lb, SpaceOrLineBreak, \
    IncBreakCost, DecBreakCost, \
    Block, \
    Formatter

# start -> [ start ]
# start -> WORD
text_01 = _b('start', [
    _t('[', "["),
    _b('start', [
        _t('WORD', "_CXX_HAS_VARIADIC_TEMPLATES")
    ], 1),
    _t(']', "]")
])

# S -> a b c %lb(1000) d e f g %lb(0) h i j k %lb(1000) l m n o p q %lb(0)
text_02 = _b('S', [
    _t('a'), _t('b'), _t('c'), _t('d'), _t('e'), _t('f'), _t('g'), _t('h'),
    _t('i'), _t('j'), _t('k'), _t('l'), _t('m'), _t('n'), _t('o'), _t('p'),
    _t('q')
])
text_02_sbs = [
    [
        'a', 'b', 'c', '%linebreak(1000)', 'd', 'e', 'f', 'g', '%linebreak(0)'
    ], [
        'h', 'i', 'j', 'k', '%linebreak(1000)', 'l', 'm', 'n', 'o', 'p', 'q',
        '%linebreak(0)'
    ]
]
text_02_nobreak_sbs = [
    [
        'a', 'b', 'c', '%linebreak(1000)', 'd', 'e', 'f', 'g', '%linebreak(0)',
        'h', 'i', 'j', 'k', '%linebreak(1000)', 'l', 'm', 'n', 'o', 'p', 'q',
        '%linebreak(0)'
    ]
]

# S -> %space a %space b %space_or_linebreak(1000)
text_03 = _b('S', [
    _t('a'), _t('b')
])
text_03_sbs = [
    [
        '%space', 'a', '%space', 'b', '%space_or_linebreak(1000)',
        '%linebreak(0)'
    ]
]

# S -> a S
# S -> b
text_04 = _b('S', [
    _t('a'), _b('S', [ _t('b') ], 1)
])
text_04_sbs = [
    [
        'a', 'S([b], 1)', '%linebreak(0)'
    ]
]

# start -> [ start ]
# start -> a
# start -> [ start , %space start ] %linebreak(0) a start
text_05 = _b('start', [
    _t('['),
        _b('start', [ _t('a') ], 1), _t(','),
        _b('start', [ _t('a') ], 1),
    _t(']'),
    _t('a'),
    _b('start', [ _t('a') ], 1)
], 2)
text_05_too_much = _b('start', [
    _t('['),
        _b('start', [ _t('a') ], 1), _t(','),
        _b('start', [ _t('a') ], 1),
    _t(']'),
    _t('a'),
    _b('start', [ _t('a') ], 1), _t('a'), _t('a')
], 2)
text_05_sbs = [
    [
        '[', 'start([a], 1)', ',', '%space', 'start([a], 1)', ']',
        '%linebreak(0)'
    ], [
        'a', 'start([a], 1)', '%linebreak(0)'
    ]
]

# A -> %space_or_linebreak(0) a b %space_or_linebreak(0) a b
#      %space_or_linebreak(1000)
text_06_a = _b('A', [
    _t('a'), _t('b'), _t('a'), _t('b')
], 0)
text_06_a_sbs = [
    [
        '%space_or_linebreak(0)'
    ], [
        'a', 'b', '%space_or_linebreak(0)'
    ], [
        'a', 'b', '%space_or_linebreak(1000)', '%linebreak(0)'
    ]
]

# A -> a b %space_or_linebreak(0) a b
text_06_b = _b('A', [
    _t('a'), _t('b'), _t('a'), _t('b')
], 1)
text_06_b_sbs = [
    [
        'a', 'b', '%space_or_linebreak(0)'
    ], [
        'a', 'b', '%linebreak(0)'
    ]
]

# A -> a b %space_or_linebreak(0) a b %space_or_linebreak(0)
text_06_c = _b('A', [
    _t('a'), _t('b'), _t('a'), _t('b')
], 2)
text_06_c_sbs = [
    [
        'a', 'b', '%space_or_linebreak(0)'
    ], [
        'a', 'b', '%space_or_linebreak(0)'
    ]
]

# A -> a A b
# A -> x
text_07 = _b('A', [
    _t('a'),
    _b('A', [
        _t('a'),
        _b('A', [
            _t('a'),
            _b('A', [ _t('x') ], 1),
            _t('b')
        ]),
        _t('b')
    ]),
    _t('b')
])
text_07_sb = [
    'a', 'a', 'a', 'x', 'b', 'b', 'b', '%linebreak(0)'
]

def FDecl(tspec, fname, argspec):
    return _b('fdecl', [
        parse_tspec(tspec), _t('FNAME', fname), parse_fargs(argspec),
        _t(';', ';')
    ], 0)
#-def

def parse_tspec(tspec):
    if tspec[-1] == '*':
        tname, stars = tspec.split(' ')
        return _b('ftype', [
            _t('TNAME', tname), parse_stars(stars)
        ], 1)
    return _b('ftype', [
        _t('TNAME', tspec)
    ], 0)
#-def

def parse_stars(stars):
    if stars == '*':
        return _b('stars', [
            _t('*', '*')
        ], 1)
    return _b('stars', [
        _t('*', '*'), parse_stars(stars[1:])
    ], 0)
#-def

def parse_fargs(argspec):
    if not argspec:
        return _b('fargs', [
            _t('(', '('), _t(')', ')')
        ], 0)
    return _b('fargs', [
        _t('(', '('), parse__args(argspec), _t(')', ')')
    ], 1)
#-def

def parse__args(argspec):
    if len(argspec) > 1:
        return _b('_args', [
            parse_arg(argspec[0]), _t(',', ','), parse__args(argspec[1:])
        ], 0)
    return _b('_args', [
        parse_arg(argspec[0])
    ], 1)
#-def

def parse_arg(arg):
    tname, argname = arg.split(' ')
    return _b('arg', [
        _t('TNAME', tname), _t('ARGNAME', argname)
    ], 0)
#-def

class Output(object):
    __slots__ = [ 'data' ]

    def __init__(self):
        self.data = ""
    #-def

    def write(self, s):
        self.data += s
    #-def
#-class

class Formatter_A(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(2, 'start', [ _T('['), _V('start'), _T(']') ])
        r.add(3, 'start', [ _T('WORD') ])
    #-def
#-class

class Formatter_B(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'S', [
            _T('a'), _T('b'), _T('c'), _lb(1000),
            _T('d'), _T('e'), _T('f'), _T('g'), _lb(0),
            _T('h'), _T('i'), _T('j'), _T('k'), _lb(1000),
            _T('l'), _T('m'), _T('n'), _T('o'), _T('p'), _T('q'), _lb(0)
        ])
    #-def
#-class

class Formatter_C(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'S', [
            Space(), _T('a'), Space(), _T('b'), SpaceOrLineBreak(1000)
        ])
    #-def
#-class

class Formatter_D(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'S', [ _V('S'), _T('a') ])
    #-def
#-class

class Formatter_E(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'S', [ _T('a'), _V('T') ])
    #-def
#-class

class Formatter_F(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'S', [ _T('a'), _V('S') ])
        r.add(1, 'S', [ _T('b') ])
    #-def
#-class

class Formatter_G(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'start', [ _T('['), _V('start'), _T(']') ])
        r.add(1, 'start', [ _T('a') ])
        r.add(2, 'start', [
            _T('['), _V('start'), _T(','), Space(), _V('start'), _T(']'),
                _lb(0),
            _T('a'), _V('start')
        ])
    #-def
#-class

class Formatter_H(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'start', [ _T('['), _V('start'), _T(']') ])
        r.add(1, 'start', [ _T('a') ])
        r.add(2, 'start', [
            _T('['), _V('start'), _T(','), Space(), _V('start'), _T(']'), "",
                _lb(0),
            _T('a'), _V('start')
        ])
    #-def
#-class

class Formatter_I(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'A', [
            SpaceOrLineBreak(0), _T('a'), _T('b'), SpaceOrLineBreak(0),
            _T('a'), _T('b'), SpaceOrLineBreak(1000)
        ])
        r.add(1, 'A', [
            _T('a'), _T('b'), SpaceOrLineBreak(0),
            _T('a'), _T('b')
        ])
        r.add(2, 'A', [
            _T('a'), _T('b'), SpaceOrLineBreak(0),
            _T('a'), _T('b'), SpaceOrLineBreak(0)
        ])
        r.add(3, 'A', [])
    #-def
#-class

class Formatter_J(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.add(0, 'A', [ _T('a'), _V('A'), _T('b') ])
        r.add(1, 'A', [ _T('x') ])
    #-def
#-class

class Formatter_K(Formatter):
    __slots__ = []

    def __init__(self):
        Formatter.__init__(self)
        r = self.rules
        r.indentation = 4
        # fdecl -> %i(4) ftype %d(4) FNAME fargs ; %linebreak(0)
        r.add(0, 'fdecl', [
            IncBreakCost(4), _V('ftype'), DecBreakCost(4), _T('FNAME'),
            _V('fargs'), _T(';'), _lb(0)
        ])
        # ftype -> TNAME %space_or_linebreak(1000)
        r.add(0, 'ftype', [
            _T('TNAME'), SpaceOrLineBreak(1000)
        ])
        # ftype -> TNAME %space stars %linebreak(1000)
        r.add(1, 'ftype', [
            _T('TNAME'), Space(), _V('stars'), _lb(1000)
        ])
        # stars -> * stars
        r.add(0, 'stars', [
            _T('*'), _V('stars')
        ])
        # stars -> *
        r.add(1, 'stars', [
            _T('*')
        ])
        # fargs -> ( %i(1) %linebreak(1000) %d(1) )
        r.add(0, 'fargs', [
            _T('('), IncBreakCost(), _lb(1000), DecBreakCost(), _T(')')
        ])
        # fargs -> ( %i(1) %linebreak(1000)
        #          %indent %i(1) _args %d(1) %linebreak(1000)
        #          %dedent %d(1) )
        r.add(1, 'fargs', [
            _T('('), IncBreakCost(), _lb(1000),
            Indent(), IncBreakCost(), _V('_args'), DecBreakCost(), _lb(1000),
            Dedent(), DecBreakCost(), _T(')')
        ])
        # _args -> arg , %space_or_linebreak(1000) _args
        r.add(0, '_args', [
            _V('arg'), _T(','), SpaceOrLineBreak(1000), _V('_args')
        ])
        # _args -> arg
        r.add(1, '_args', [
            _V('arg')
        ])
        # arg   -> TNAME %space ARGNAME
        r.add(0, 'arg', [
            _T('TNAME'), Space(), _T('ARGNAME')
        ])
    #-def
#-class

class TestTextNodeCase(unittest.TestCase):

    def test_make_subblocks_no_rule_for_node(self):
        f = Formatter_A()

        with self.assertRaises(FormatError):
            text_01.make_subblocks(f)
    #-def

    def test_make_subblocks_rule_has_no_alternatives(self):
        f = Formatter_A()

        with self.assertRaises(FormatError):
            text_01.make_subblocks(f)
    #-def

    def test_make_subblocks_line_breaking(self):
        f = Formatter_B()

        bs = text_02.make_subblocks(f)
        self.assertEqual(len(bs), 2)
        for x in bs:
            self.assertIsInstance(x, Block)
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, text_02_sbs)
    #-def

    def test_make_subblocks_no_line_breaking(self):
        f = Formatter_B()

        bs = text_02.make_subblocks(f, True)
        self.assertEqual(len(bs), 1)
        for x in bs:
            self.assertIsInstance(x, Block)
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, text_02_nobreak_sbs)
    #-def

    def test_make_subblocks_text_operators(self):
        f = Formatter_C()

        bs = text_03.make_subblocks(f)
        self.assertEqual(len(bs), 1)
        for x in bs:
            self.assertIsInstance(x, Block)
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, text_03_sbs)
    #-def

    def test_make_subblocks_not_enough_elements(self):
        f = Formatter_B()

        with self.assertRaises(FormatError):
            text_03.make_subblocks(f)
    #-def

    def test_make_subblocks_var_term_mismatch(self):
        f = Formatter_D()

        with self.assertRaises(FormatError):
            text_04.make_subblocks(f)
    #-def

    def test_make_subblocks_var_term_name_mismatch(self):
        f = Formatter_E()

        with self.assertRaises(FormatError):
            text_04.make_subblocks(f)
    #-def

    def test_make_subblocks_var_term(self):
        f = Formatter_F()

        bs = text_04.make_subblocks(f)
        self.assertEqual(len(bs), 1)
        for x in bs:
            self.assertIsInstance(x, Block)
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, text_04_sbs)
    #-def

    def test_make_subblocks_all(self):
        f = Formatter_G()

        bs = text_05.make_subblocks(f)
        self.assertEqual(len(bs), 2)
        for x in bs:
            self.assertIsInstance(x, Block)
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, text_05_sbs)
    #-def

    def test_make_subblocks_invalid_element(self):
        f = Formatter_H()

        with self.assertRaises(FormatError):
            text_05.make_subblocks(f)
    #-def

    def test_make_subblocks_too_much_elements(self):
        f = Formatter_G()

        with self.assertRaises(FormatError):
            text_05_too_much.make_subblocks(f)
    #-def

    def test_make_subblocks_line_breaks_sanitizing(self):
        f = Formatter_I()

        bs = text_06_a.make_subblocks(f)
        self.assertEqual(len(bs), 3)
        for x in bs:
            self.assertIsInstance(x, Block)
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, text_06_a_sbs)

        bs = text_06_b.make_subblocks(f)
        self.assertEqual(len(bs), 2)
        for x in bs:
            self.assertIsInstance(x, Block)
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, text_06_b_sbs)

        bs = text_06_c.make_subblocks(f)
        self.assertEqual(len(bs), 2)
        for x in bs:
            self.assertIsInstance(x, Block)
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, text_06_c_sbs)
    #-def

    def test_make_subblocks_empty(self):
        f = Formatter_I()

        bs = _b('A', [], 3).make_subblocks(f)
        self.assertEqual(len(bs), 0)
    #-def
#-class

class TestBlockCase(unittest.TestCase):

    def test_expand_elements_empty(self):
        f = Formatter_I()
        b = Block([])

        b.expand_elements(f)
        self.assertTrue(b.empty())
    #-def

    def test_expand_elements(self):
        f = Formatter_J()

        bs = text_07.make_subblocks(f)
        self.assertEqual(len(bs), 1)
        for x in bs:
            self.assertIsInstance(x, Block)
        b = bs[0]
        b.expand_elements(f)
        sb = [repr(e) for e in b.elements]
        self.assertEqual(sb, text_07_sb)
    #-def

    def test_adjust_break_costs(self):
        b = Block([
            _lb(1000), IncBreakCost(), _t('a'), SpaceOrLineBreak(1000),
            IncBreakCost(), IncBreakCost(), _t('b'), SpaceOrLineBreak(1000),
            DecBreakCost(), _lb(1000), DecBreakCost(), SpaceOrLineBreak(1000),
            DecBreakCost(), _lb(1000), SpaceOrLineBreak(0)
        ])

        b.adjust_break_costs()
        sb = [repr(e) for e in b.elements]
        self.assertEqual(sb, [
            '%linebreak(0)', 'a', '%space_or_linebreak(1)', 'b',
            '%space_or_linebreak(3)', '%linebreak(2)',
            '%space_or_linebreak(1)', '%linebreak(0)',
            '%space_or_linebreak(0)'
        ])
    #-def

    def test_decrease_break_costs(self):
        b = Block([
            _t('a'), Space(), _lb(4), _t('a'), SpaceOrLineBreak(3)
        ])

        b.decrease_break_costs(2)
        sb = [repr(e) for e in b.elements]
        self.assertEqual(sb, [
            'a', '%space', '%linebreak(2)', 'a', '%space_or_linebreak(1)'
        ])
    #-def

    def test_compute_line_length(self):
        f = Formatter_I()

        b = Block([_lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (0, 1, 1))

        b = Block([Space(), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (1, 2, 1))

        b = Block([Space(), Space(), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (2, 3, 1))

        b = Block([Space(), Space(), Space(), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (3, 4, 1))

        b = Block([Space(), Space(), Space(), Space(), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (4, 5, 1))

        b = Block([_t('a', "xy"), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (0, 1, 3))

        b = Block([SpaceOrLineBreak(1), _t('a', "xy"), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (1, 2, 3))

        b = Block([Space(), _t('a', 'u'), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (1, 2, 2))

        b = Block([Space(), SpaceOrLineBreak(1), _t('a', "z"), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (2, 3, 2))

        b = Block([_t('c', "123"), SpaceOrLineBreak(1), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (0, 1, 4))

        b = Block([_t('c', "123"), Space(), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (0, 1, 4))

        b = Block([_t('c', "123"), Space(), SpaceOrLineBreak(1), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (0, 1, 4))

        b = Block([Space(), _t('c', "123"), SpaceOrLineBreak(1), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (1, 2, 4))

        b = Block([
            Space(), Space(), _t('c', "123"), SpaceOrLineBreak(1), Space(),
            _lb(0)
        ])
        r = b.compute_line_length(f)
        self.assertEqual(r, (2, 3, 4))

        b = Block([_t('c', "123"), _t('x', "gg"), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (0, 2, 6))

        b = Block([_t('c', "123"), Space(), _t('x', "gg"), _lb(0)])
        r = b.compute_line_length(f)
        self.assertEqual(r, (0, 3, 7))

        b = Block([
            Space(), _t('c', "123"), Space(), SpaceOrLineBreak(1),
            _t('1', '2'), Space(), _t('x', "gg"), SpaceOrLineBreak(1), _lb(0)
        ])
        r = b.compute_line_length(f)
        self.assertEqual(r, (1, 7, 10))

        b = Block([
            Space(), _t('c', "123"), Space(), SpaceOrLineBreak(1),
            _t('1', '2'), Space(), _t('x', "gg"), SpaceOrLineBreak(1), _lb(0)
        ])
        b.indentation_level = 3
        r = b.compute_line_length(f)
        self.assertEqual(r, (1, 7, 16))
    #-def

    def test_get_block(self):
        b = Block([])
        r = b.get_block(0)
        self.assertIsNone(r[0])
        self.assertEqual(r[1], 0)

        b = Block([_lb(0)])
        r = b.get_block(0)
        sb = [repr(e) for e in r[0].elements]
        self.assertEqual(sb, [ '%linebreak(0)' ])
        self.assertEqual(r[1], 1)

        b = Block([_t('a')])
        r = b.get_block(0)
        sb = [repr(e) for e in r[0].elements]
        self.assertEqual(sb, [ 'a', '%linebreak(0)' ])
        self.assertEqual(r[1], 1)

        b = Block([SpaceOrLineBreak(1000)])
        r = b.get_block(0)
        sb = [repr(e) for e in r[0].elements]
        self.assertEqual(sb, [ '%space_or_linebreak(1000)', '%linebreak(0)' ])
        self.assertEqual(r[1], 1)

        b = Block([
            _lb(0),
            SpaceOrLineBreak(0),
            _t('a'), Space(), _t('b'), _lb(0),
            _t('c'), SpaceOrLineBreak(0),
            _lb(1000), SpaceOrLineBreak(1000), _t('d')
        ])
        r = b.get_block(0)
        sb = [repr(e) for e in r[0].elements]
        self.assertEqual(sb, [ '%linebreak(0)' ])
        self.assertEqual(r[1], 1)

        r = b.get_block(1)
        sb = [repr(e) for e in r[0].elements]
        self.assertEqual(sb, [ '%space_or_linebreak(0)' ])
        self.assertEqual(r[1], 2)

        r = b.get_block(2)
        sb = [repr(e) for e in r[0].elements]
        self.assertEqual(sb, [ 'a', '%space', 'b', '%linebreak(0)' ])
        self.assertEqual(r[1], 6)

        r = b.get_block(6)
        sb = [repr(e) for e in r[0].elements]
        self.assertEqual(sb, [ 'c', '%space_or_linebreak(0)' ])
        self.assertEqual(r[1], 8)

        r = b.get_block(8)
        sb = [repr(e) for e in r[0].elements]
        self.assertEqual(sb, [
            '%linebreak(1000)', '%space_or_linebreak(1000)', 'd',
            '%linebreak(0)'
        ])
        self.assertEqual(r[1], 11)

        r = b.get_block(11)
        self.assertIsNone(r[0])
        self.assertEqual(r[1], 11)
    #-def

    def test_verify(self):
        with self.assertRaises(FormatError):
            Block([[]]).verify()
        with self.assertRaises(FormatError):
            Block([]).verify()
        with self.assertRaises(FormatError):
            Block([Space()]).verify()
        with self.assertRaises(FormatError):
            Block([SpaceOrLineBreak(1)]).verify()
        Block([SpaceOrLineBreak(0)]).verify()
        Block([_t('a'), SpaceOrLineBreak(0)]).verify()
        with self.assertRaises(FormatError):
            Block([_t('a'), _lb(0), _t('s'), SpaceOrLineBreak(0)]).verify()
        Block([Indent(), _t('a'), Dedent(), _lb(1), Space(), _lb(0)]).verify()
    #-def

    def test_do_break(self):
        bs = Block([]).do_break()
        self.assertEqual(bs, [])

        bs = Block([_t('a'), _lb(0)]).do_break()
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, [
            [
                'a', '%linebreak(0)'
            ]
        ])

        bs = Block([_t('a'), _lb(0), _t('b'), SpaceOrLineBreak(0)]).do_break()
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, [
            [
                'a', '%linebreak(0)'
            ], [
                'b', '%space_or_linebreak(0)'
            ]
        ])

        bs = Block([
            _t('a'), Indent(), _lb(0), _t('b'), Dedent(), _lb(0)
        ]).do_break()
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, [
            [
                'a', '%indent', '%linebreak(0)'
            ], [
                'b', '%dedent', '%linebreak(0)'
            ]
        ])
        self.assertEqual(bs[0].indentation_level, 0)
        self.assertEqual(bs[1].indentation_level, 0)

        bs = Block([
            Indent(), _t('a'), Indent(), _lb(0),
            _t('b'), Dedent(), _lb(0),
            Dedent(), _lb(0),
            _t('c'), Indent(), Dedent(), _t('d'), _lb(0)
        ]).do_break()
        sbs = [[repr(e) for e in b.elements] for b in bs]
        self.assertEqual(sbs, [
            [
                'a', '%indent', '%linebreak(0)'
            ], [
                'b', '%dedent', '%linebreak(0)'
            ], [
                '%linebreak(0)'
            ], [
                'c', '%indent', '%dedent', 'd', '%linebreak(0)'
            ]
        ])
        self.assertEqual(bs[0].indentation_level, 1)
        self.assertEqual(bs[1].indentation_level, 1)
        self.assertEqual(bs[2].indentation_level, 0)
        self.assertEqual(bs[3].indentation_level, 0)
    #-def
#-class

class TestFormatterCase(unittest.TestCase):

    def test_format_bad_input(self):
        f = Formatter_K()

        with self.assertRaises(FormatError):
            f.format(_t('TNAME', "my_type"), Output())
    #-def

    def test_format(self):
        text1 = FDecl(
            "int", "f", []
        )
        text2 = FDecl(
            "void **", "mem_probe", [
                "mem_chunk_ptr pchunk",
                "mem_chunk_size sz"
            ]
        )
        text3 = FDecl(
            "void", "test", [ "int a" ]
        )
        text4 = FDecl(
            "my_very_very_very_very_long_type *",
            "very_long_name_for_a_some_meaningless_function",
            [
                "pointer_to_char character",
                "coordinate_type coordinateX",
                "coordinate_type coordinateY",
                "mutable_buffer_pointer buffer"
            ]
        )
        text5 = FDecl(
            "void *", "zparse", [
                "zparser_context_ptr pctx",
                "zparser_flags_type flags",
                "zparser_diagnosis diag"
            ]
        )
        text6 = FDecl(
            "looooooooooooooooooooooooooooooong_int_is_loooooooooooooooooo" \
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong",
            "zababa", []
        )
        f = Formatter_K()

        o = Output()
        f.format(text1, o)
        self.assertEqual(o.data,
            "int f();\n"
        )

        o = Output()
        f.format(text2, o)
        self.assertEqual(o.data,
            "void **mem_probe(mem_chunk_ptr pchunk, mem_chunk_size sz);\n"
        )

        o = Output()
        f.format(text3, o)
        self.assertEqual(o.data,
            "void test(int a);\n"
        )

        o = Output()
        f.format(text4, o)
        self.assertEqual(o.data,
            "my_very_very_very_very_long_type *\n" \
            "very_long_name_for_a_some_meaningless_function(\n" \
            "    pointer_to_char character,\n" \
            "    coordinate_type coordinateX,\n" \
            "    coordinate_type coordinateY,\n" \
            "    mutable_buffer_pointer buffer\n" \
            ");\n"
        )

        o = Output()
        f.format(text5, o)
        self.assertEqual(o.data,
            "void *zparse(\n" \
            "    zparser_context_ptr pctx, zparser_flags_type flags, " \
                "zparser_diagnosis diag\n" \
            ");\n"
        )

        o = Output()
        with self.assertRaises(FormatError):
            f.format(text6, o)
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBlockCase))
    suite.addTest(unittest.makeSuite(TestTextNodeCase))
    suite.addTest(unittest.makeSuite(TestFormatterCase))
    return suite
#-def
