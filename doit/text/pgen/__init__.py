#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/__init__.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-03 21:57:10 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Tools for parser generators distribution and maintaining.\
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

class ParserGenerator(Application):
    """
    """
    __slots__ = []

    def __init__(self, owner = None):
        """
        """

        Application.__init__(self, owner)
        self.__commands = {}
    #-def

    def define_options(self):
        """
        """

        self.define_option(
            "quite", ['q'],
            about = "suppress all messages"
        )
        self.define_option(
            "help", ['h', '?'],
            about = "print this screen and exit"
            cb = self.on_help_option
        )
    #-def

    def load_commands(self):
        """
        """

    #-def

    def at_start(self):
        """
        """

        self.define_options()
    #-def

    def print_help(self):
        """
        """

        self.werr(self.strip_block("""\
        usage: %(appname)s [program options] <command> [command options]

        where program options are
        %(options)s
        The available commands are
        %(commands)s
        To see more detailed informations about specific command, type
        `%(appname)s help <command>` or `%(appname)s <command> %(helpopt)s`
        """) % dict(
            appname = self.get_name(),
            options = self.make_options_help(),
            commands = self.make_commands_help(),
            helpopt = self.get_help_option_name()
        ))
    #-def

    def on_help_option(self, opt):
        """
        """

        self.print_help()
        self.exit(1)
    #-def
#-class
