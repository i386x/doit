#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/parsing/cfgtools.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-01-12 21:31:16 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Context-free grammar tools.\
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

def extract_variables_visitor(node, *args):
    """
    """

    if isinstance(node, Var):
        value, container = args
        container.add(value)
    return None
#-def

def termination_checker_visitor(node, *args):
    """
    """

    if isinstance(node, (Sym, Range, Action)):
        return True
    elif isinstance(node, Var):
        var, tv, _ = args
        return var in tv
    elif isinstance(node, (Alias, DoNotRecord, Complement, PositiveIteration)):
         # args[0] == node.visit(...)
        return args[0]
    elif isinstance(node, (Iteration, Optional)):
        # X* and X? sets always contain an empty string
        return True
    elif isinstance(node, Label):
        # args[0] == left_node.visit(...)
        return args[0]
    elif isinstance(node, Catenation):
        # args[0] == left_node.visit(...)
        # args[1] == right_node.visit(...)
        return args[0] and args[1]
    elif isinstance(node, Alternation):
        # args[0] == left_node.visit(...)
        # args[1] == right_node.visit(...)
        return args[0] or args[1]
    else:
        _badnode()
#-def

def get_variables_stats(cfg):
    """
    """

    if get_variables not in cfg.cache:
        lhs_variables = set()
        rhs_variables = set()
        variable_deps = {}
        is_cycle_free = True

        # Get variable dependencies:
        rules = cfg.get_rules()
        for lhs in rules:
            variable_deps[lhs] = set()
            lhs_variables.add(lhs)
            rules[lhs].visit(extract_variables_visitor, variable_deps[lhs])
            rhs_variables |= variable_deps[lhs]
        variables = lhs_variables | rhs_variables

        # BFS the grammar for reachable variables:
        visited = set()
        to_visit = [cfg.get_start()]
        while to_visit:
            var = to_visit.pop(0)
            if var in variable_deps:
                visited.add(var)
                for x in variable_deps[var]:
                    if x not in visited:
                        to_visit.append(x)
                    else:
                        is_cycle_free = False
                    #-if
                #-for
            #-if
        #-while

        # Compute the set of nonterminating variables:
        nonterminating_variables = variables.copy()
        terminating_variables = set()
        while True:
            old_tv_card = len(terminating_variables)
            for lhs in rules:
                if lhs in terminating_variables:
                    continue
                if rules[lhs].visit(
                    termination_checker_visitor,
                    terminating_variables,
                    nonterminating_variables
                ):
                    terminating_variables.add(lhs)
                    nonterminating_variables.discard(lhs)
                #-if
            #-for
            if old_tv_card == len(terminating_variables):
                break
            #-if
        #-while

        cfg.cache[get_variables_stats] = dict(
            lhs_variables = lhs_variables,
            rhs_variables = rhs_variables,
            variables = variables,
            undefined_variables = rhs_variables - lhs_variables,
            unreachable_variables = variables - visited,
            nonterminating_variables = nonterminating_variables,
            is_cycle_free = is_cycle_free,
            variable_deps = variable_deps,
            has_start = cfg.get_start() in visited
        )
    return cfg.cache[get_variables_stats]
#-def

def get_lhs_variables(cfg):
    """
    """

    if get_lhs_variables not in cfg.cache:
        cfg.cache[get_lhs_variables] = get_variables_stats(cfg)[
            'lhs_variables'
        ]
    return cfg.cache[get_lhs_variables]
#-def

def get_rhs_variables(cfg):
    """
    """

    if get_rhs_variables not in cfg.cache:
        cfg.cache[get_rhs_variables] = get_variables_stats(cfg)[
            'rhs_variables'
        ]
    return cfg.cache[get_rhs_variables]
#-def

def get_variables(cfg):
    """
    """

    if get_variables not in cfg.cache:
        cfg.cache[get_variables] = get_variables_stats(cfg)[
            'variables'
        ]
    return cfg.cache[get_variables]
#-def

def get_undefined_variables(cfg):
    """
    """

    if get_undefined_variables not in cfg.cache:
        cfg.cache[get_undefined_variables] = get_variables_stats(cfg)[
            'undefined_variables'
        ]
    return cfg.cache[get_undefined_variables]
#-def

def get_unreachable_variables(cfg):
    """
    """

    if get_unreachable_variables not in cfg.cache:
        cfg.cache[get_unreachable_variables] = get_variables_stats(cfg)[
            'unreachable_variables'
        ]
    return cfg.cache[get_unreachable_variables]
#-def

def get_nonterminating_variables(cfg):
    """
    """

    if get_nonterminating_variables not in cfg.cache:
        cfg.cache[get_nonterminating_variables] = get_variables_stats(cfg)[
            'nonterminating_variables'
        ]
    return cfg.cache[get_nonterminating_variables]
#-def

def is_cycle_free(cfg):
    """
    """

    if is_cycle_free not in cfg.cache:
        cfg.cache[is_cycle_free] = get_variables_stats(cfg)[
            'is_cycle_free'
        ]
    return cfg.cache[is_cycle_free]
#-def

def get_variable_deps(cfg):
    """
    """

    if get_variable_deps not in cfg.cache:
        cfg.cache[get_variable_deps] = get_variables_stats(cfg)[
            'variable_deps'
        ]
    return cfg.cache[get_variable_deps]
#-def

def has_start(cfg):
    """
    """

    if has_start not in cfg.cache:
        cfg.cache[has_start] = get_variables_stats(cfg)[
            'has_start'
        ]
    return cfg.cache[has_start]
#-def

def is_well_defined(cfg):
    """
    """

    if is_well_defined not in cfg.cache:
        cfg.cache[is_well_defined] = (
            not get_undefined_variables(cfg) \
            and not get_unreachable_variables(cfg) \
            and not get_nonterminating_variables(cfg) \
            and has_start(cfg)
        )
    return cfg.cache[is_well_defined]
#-def

def is_classic_rhs_visitor(node, *args):
    """
    """

    if isinstance(node, (Sym, Var, Action)):
        return True
    elif isinstance(node, (Alias, DoNotRecord, Label)):
        return args[0]
    elif isinstance(node, (Catenation, Alternation)):
        return args[0] and args[1]
    else:
        return False
#-def

def is_classic(cfg):
    """
    """

    # Every right-hand side of every rule in a "classic" grammar consists of a
    # string over set of terminal symbols and variables:
    if is_classic not in cfg.cache:
        cfg.cache[is_classic] = True

        rules = cfg.get_rules()
        for lhs in rules:
            if not rules[lhs].visit(is_classic_rhs_visitor):
                cfg.cache[is_classic] = False
                break
            #-if
        #-for
    return cfg.cache[is_classic]
#-def
