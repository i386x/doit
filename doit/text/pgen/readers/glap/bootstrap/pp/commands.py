#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/pp/commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-07-14 22:14:03 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Glap grammar preprocessor commands.\
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

from doit.support.utils import deep_eq
from doit.support.cmd.commands import Trackable, DefModule

RULESVARNAME = '@rules'

class DefRule(Trackable):
    """
    """
    __slots__ = [ 'label', 'rhs', 'is_short' ]

    def __init__(self, label, rhs, is_short):
        """
        """

        Trackable.__init__(self)
        self.label = label
        self.rhs = rhs
        self.is_short = is_short
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Trackable.__eq__(self, other) \
        and deep_eq(self.label, other.label) \
        and deep_eq(self.rhs, other.rhs) \
        and self.is_short == other.is_short
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def

    def expand(self, processor):
        """
        """

        ctx = CommandContext(self)
        processor.insertcode(
            Initializer(ctx),
            GetMember(GetLocal(Module.THISVARNAME), RULESVARNAME),
            self.do_defrule,
            Finalizer(ctx)
        )
    #-def

    def do_defrule(self, processor):
        """
        """

        rules = processor.acc()

        ctx = processor.cmdctx(self)
        if not isinstance(rules, Grammar):
            raise CommandError(processor.TypeError,
                "%s: Run me inside grammar module" % self.name,
                processor.traceback()
            )
        self.rhs.location = self.location
        self.rhs.properties['label'] = self.label
        self.rhs.properties['is_short'] = self.is_short
        rules[self.label] = self.rhs
    #-def
#-class

class DefGrammar(DefModule):
    """
    """
    __slots__ = [ 'gspecs' ]

    def __init__(self, gname, gspecs, gbody):
        """
        """

        DefModule.__init__(self, gname, gbody)
        self.gspecs = gspecs
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and DefModule.__eq__(self, other) \
        and deep_eq(self.gspecs, other.gspecs)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def

    def create_module(self, processor):
        """
        """

        ctx = processor.cmdctx(self)
        body = []
        for gspecid, gspecloc in self.gspecs:
            gspec = ctx.env.getvar(gspecid)
            if not isinstance(gspec, Module):
                raise CommandError(processor.TypeError,
                    "%r %s is not module" % (gspecid, gspecloc),
                    processor.traceback()
                )
            body.extend(gspec.body)
        body.append(
            SetMember(GetLocal(Module.THISVARNAME), RULESVARNAME, Grammar())
        )
        body.extend(self.body)
        g = Module(self.mname, processor.mkqname(self.mname), body, ctx.env)
        processor.insertcode(g, self.pushacc, g)
    #-def
#-class
