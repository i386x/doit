#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/app/config.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-12-13 11:50:26 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Commands for reading and maintaining configuration files.\
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

import os

from doit.support.app.io import read_all, write_items
from doit.support.app.printer import PageFormatter, PageBuilder
from doit.support.app.application import EXIT_SUCCESS, EXIT_FAILURE

COMM = 0
NL = 1
ITEM = 2

def load_config(path):
    """
    """

    def scan(l):
        if l == "":
            return (NL, l)
        elif l[0] == '#':
            return (COMM, l)
        b = l.find('=')
        if b < 0:
            return (COMM, l)
        key = l[:b].strip()
        if key == "":
            return (COMM, l)
        return (ITEM, key, l[b + 1:].strip())
    config_raw_data = read_all(path)
    if config_raw_data is None:
        return None, None
    config_data = config_raw_data.split('\n')
    config_data = [x.strip() for x in config_data]
    while config_data and config_data[-1] == "":
        config_data.pop()
    config_data = [scan(x) for x in config_data]
    return config_data, dict([
        (x[1], i) for i, x in enumerate(config_data) if x[0] == ITEM
    ])
#-def

def set_item(config_data, config_data_map, key, value):
    """
    """

    if key not in config_data_map:
        i = len(config_data)
        config_data.append((ITEM, key, value))
        config_data_map[key] = i
        return
    config_data[config_data_map[key]] = (ITEM, key, value)
#-def

def get_item(config_data, config_data_map, key):
    """
    """

    if key not in config_data_map:
        return None
    return config_data[config_data_map[key]][2]
#-def

def del_item(config_data, config_data_map, key):
    """
    """

    for i, x in enumerate(config_data):
        if x[0] == ITEM and x[1] == key:
            config_data[i] = (COMM, "#%s = %s" % (x[1], x[2]))
    if key in config_data_map:
        del config_data_map[key]
#-def

def merge_items(config_data_A, config_data_B):
    """
    """

    config_data = config_data_A + config_data_B
    return config_data, dict([
        (x[1], i) for i, x in enumerate(config_data) if x[0] == ITEM
    ])
#-def

def config_to_kvmap(config_data, config_data_map):
    """
    """

    return dict([
        (k, config_data[config_data_map[k]][2]) for k in config_data_map
    ])
#-def

def save_config(path, config_data):
    """
    """

    def p(x):
        v = "%s = %s" % (x[1], x[2]) if x[0] == ITEM else x[1]
        return "%s\n" % v.strip()
    if not write_items(path, config_data, p):
        return False, "Can't write to <%s>" % path
    return True, ""
#-def

def set_config_option(cmd, path, key, value, verbose):
    """
    """

    cfg_data, cfg_map = load_config(path)
    if cfg_data is None and os.path.exists(path) and os.path.isfile(path):
        cmd.werr("%s: File <%s> cannot be opened.\n" % (cmd.get_name(), path))
        return EXIT_FAILURE
    if cfg_data is None:
        cfg_data, cfg_map = [], {}
    set_item(cfg_data, cfg_map, key, value)
    r, m = save_config(path, cfg_data)
    if not r:
        cmd.werr("%s: %s.\n" % (cmd.get_name(), m))
        return EXIT_FAILURE
    verbose and cmd.wout(
        "%s: Option '%s' in <%s> has been updated.\n" % (
            cmd.get_name(), key, path
        )
    )
    return EXIT_SUCCESS
#-def

def unset_config_option(cmd, path, key, verbose):
    """
    """

    cfg_data, cfg_map = load_config(path)
    if cfg_data is None and os.path.exists(path) and os.path.isfile(path):
        cmd.werr("%s: File <%s> cannot be opened.\n" % (cmd.get_name(), path))
        return EXIT_FAILURE
    if cfg_data is None:
        return EXIT_SUCCESS
    del_item(cfg_data, cfg_map, key)
    r, m = save_config(path, cfg_data)
    if not r:
        cmd.werr("%s: %s.\n" % (cmd.get_name(), m))
        return EXIT_FAILURE
    verbose and cmd.wout(
        "%s: Option '%s' in <%s> has been unset.\n" % (
            cmd.get_name(), key, path
        )
    )
    return EXIT_SUCCESS
#-def

# Note: tested manualy
def make_config_helppage(cmd, hp):
    """
    """

    helppage = PageBuilder()
    helppage.paragraph("""
    %s\\ [options]\\ <action>
    """ % cmd.get_name())
    helppage.paragraph("""
    Maintains configuration files.
    """)
    helppage.paragraph("""
    Every configuration file is a list of key-value options (items), one
    key-value option per line. A key-value option is a sequence of characters
    containing '=' with at least one nonblank character on the left-hand side
    of '='. The characters on the left of '=' are treated as a key and the
    characters on the right of '=' are treated as a value. The possible blank
    characters around key and value are omitted. If line starts with '#', it is
    treated as a comment. As a comments are treated also lines that do not
    contain '=' or a key-value options with empty keys. Empty lines are
    ignored. Available options for this command are:
    """)
    helppage.table(cmd.list_options())
    helppage.paragraph("""
    Available actions are:
    """)
    helppage.table(cmd.list_commands(cmd.actions()))
    helppage.paragraph("""
    To see more detailed informations about specific action, type
    `%shelp` after action's name.
    """ % cmd.get_option_processor().get_option_class().LONG_PREFIX)
    PageFormatter().format(helppage.page, hp)
#-def
