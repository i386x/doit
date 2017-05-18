#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/bootstrap/__init__.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-12-19 02:04:45 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
GLAP bootstrap.\
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

class GlapLexError(ParsingError):
    """
    """
    __slots__ = []

    def __init__(self, istream, detail):
        """
        """

        s = istream.data[0 : istream.pos]
        lineno = s.count('\n') + 1
        if lineno > 1:
            s = s.split('\n')[-1]
        colno = len(s) + 1
        ParsingError.__init__(self, "In <%s> at [%d:%d]: %s" % (
            istream.name, lineno, colno, detail
        ))
    #-def
#-class

class GlapSyntaxError(ParsingError):
    """
    """
    __slots__ = []

    def __init__(self, lexer, detail):
        """
        """

        p = lexer.istream.pos
        if lexer.token:
            p = lexer.token.location()
        s = lexer.istream.data[0 : p]
        lineno = s.count('\n') + 1
        if lineno > 1:
            s = s.split('\n')[-1]
        colno = len(s) + 1
        ParsingError.__init__(self, "In <%s> at [%d:%d]: %s" % (
            lexer.istream.name, lineno, colno, detail
        ))
    #-def
#-class

class GlapParserActions(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        self.actions = {
          'start': self.on_start,
          'module': self.on_module
        }
    #-def

    def on_start(self, context, module):
        """
        """

        return module
    #-def

    def on_module(self, context, loc, name, module_units):
        """
        """

        node = DefModule(name.value(), module_units)
        node.set_location(*make_location(context, loc))
        return node
    #-def

    def run(self, action, context, *args):
        """
        """

        if action not in self.actions:
            raise ParsingError("Action %r does not exist" % action)
        return self.actions[action](context, *args)
    #-def
#-class

def get_source():
    """
    """

    return "foo"
#-def
