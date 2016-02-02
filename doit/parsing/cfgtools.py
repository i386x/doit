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

def find_blocking_variables_visitor(node, *args):
    """
    """

    if isinstance(node, (Sym, Range, Action)):
        return (True, [])
    elif isinstance(node, Var):
        var, root = args
        return (False, [args[0]])
    elif isinstance(node, ):

def extract_variables_visitor(node, *args):
    """
    """

    if isinstance(node, Var):
        value, container = args
        container.add(value)
    return None
#-def

def get_variables_stats(cfg):
    """
    """

    if get_variables not in cfg.cache:
        lhs_variables = set()
        rhs_variables = set()
        variable_deps = {}
        undefined_variables = set()
        unreacheable_variables = set()
        is_cycle_free = True

        # Get variable dependencies:
        rules = cfg.get_rules()
        for lhs in rules:
            variable_deps[lhs] = set()
            lhs_variables.add(lhs)
            rules[lhs].visit(extract_variables_visitor, variable_deps[lhs])
            rhs_variables |= variable_deps[lhs]
        variables = lhs_variables | rhs_variables

        # Build inverse variable dependencies:
        inv_variable_deps = {}

        # BFS the grammar:
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

        cfg.cache[get_variables_stats] = dict(
            lhs_variables = lhs_variables,
            rhs_variables = rhs_variables,
            variables = variables,
            undefined_variables = rhs_variables - lhs_variables,
            unreachable_variables = variables - visited,
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
