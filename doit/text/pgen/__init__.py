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

import sys
import os

from doit.support.utils import WithStatementExceptionHandler

from doit.support.app.io import CharBuffer
from doit.support.app.printer import \
    escape, PageFormatter, TableBuilder, PageBuilder
from doit.support.app.application import \
    EXIT_SUCCESS, EXIT_FAILURE, INTERNAL_ERROR, \
    Application

from doit.text.pgen.cache import COMMANDS_DIR, get_commands, add_command
from doit.text.pgen.builders.builder import Builder

class Help(Builder):
    """
    """
    __slots__ = [ '__helppage', '__commands' ]

    def __init__(self, owner, **kwargs):
        """
        """

        Builder.__init__(self, owner, **kwargs)
        self.set_name(self.name())
        self.set_output(owner.get_output())
        self.set_log(owner.get_log())
        self.set_error_log(owner.get_error_log())

        self.__helppage = CharBuffer(self)
        self.__commands = kwargs.get('commands', {})
    #-def

    def at_start(self):
        """
        """

        self.define_option(
            "help", ['h', '?'],
            about = "print this screen and exit",
            cb = self.on_help_option
        )

        helppage = PageBuilder()
        helppage.paragraph("""
        %s\\ [options] <command\\ name>
        """ % self.get_name())
        helppage.paragraph("""
        Provides the detailed help information about selected command.
        """)
        helppage.paragraph("""
        Options:
        """)
        helppage.table(self.list_options())
        PageFormatter().format(helppage.page, self.__helppage)
    #-def

    def main(self):
        """
        """

        options = self.get_option_processor().get_options()
        if options['help'].when_given >= 0:
            self.werr_nolog(self.__helppage)
            return EXIT_FAILURE
        pending_args = self.get_pending_args()
        if not pending_args:
            self.werr_nolog(
                "%s: Command name was expected.\n\n" % self.get_name()
            )
            return EXIT_FAILURE
        command = pending_args.pop(0)
        if command not in self.__commands:
            self.werr_nolog(
                "%s: Unknown command '%s'.\n\n" % (self.get_name(), command)
            )
            return EXIT_FAILURE
        command = self.__commands[command](
            owner = self,
            commands = self.__commands
        )
        return command.run([str(options['help'])])
    #-def

    @staticmethod
    def description():
        """
        """

        return "prints the detailed help information about selected command"
    #-def
#-class

class Add(Builder):
    """
    """
    NONE = 0
    BUILDER = 1
    __slots__ = [ '__helppage', '__element_type', '__v' ]

    def __init__(self, owner, **kwargs):
        """
        """

        Builder.__init__(self, owner, **kwargs)
        self.set_name(self.name())
        self.set_output(owner.get_output())
        self.set_log(owner.get_log())
        self.set_error_log(owner.get_error_log())

        self.__helppage = CharBuffer(self)
        self.__element_type = self.NONE
        self.__v = not kwargs.get('quite', False)
    #-def

    def at_start(self):
        """
        """

        oc = self.get_option_processor().get_option_class()

        self.define_option(
            "help", ['h', '?'],
            about = "print this screen and exit",
            cb = self.on_help_option
        )
        self.define_option(
            "builder", ['b'],
            about = "add builder to the parser generator",
            cb = self.on_builder_option
        )
        self.define_option(
            "command", ['c'],
            about = "add command to the parser generator (" \
                "actually alias for %s" \
            ")" % oc.repr_long("builder"),
            cb = self.on_builder_option
        )
        self.define_kwoption(
            "name", ['n'],
            about = "the name of the new element"
        )

        helppage = PageBuilder()
        helppage.paragraph("""
        %s\\ [options]
        """ % self.get_name())
        helppage.paragraph("""
        Adds new element (command, builder, etc.) to the parser generator
        system.
        """)
        helppage.paragraph("""
        If this command is executed with %(builder)s parameter, the parameter
        %(name)s with the new command's name is also required. If the new
        command's name is 'mycmd', then the command-adding machinery searches
        <%(cmddir)s> directory for the file 'mycmd.py'. For the structure of
        'mycmd.py', see any file in <%(cmddir)s>.
        """ % dict(
            builder = oc.repr_long('builder'),
            name = oc.repr_long('name'),
            cmddir = escape(os.path.relpath(COMMANDS_DIR))
        ))
        helppage.paragraph("""
        Options:
        """)
        helppage.table(self.list_options())
        PageFormatter().format(helppage.page, self.__helppage)
    #-def

    def main(self):
        """
        """

        options = self.get_option_processor().get_options()
        if options['help'].when_given >= 0:
            self.werr_nolog(self.__helppage)
            return EXIT_FAILURE
        if self.__element_type == self.NONE:
            self.werr_nolog(
                "%s: I don't know what to add.\n\n" % self.get_name()
            )
            return EXIT_FAILURE
        elif self.__element_type == self.BUILDER:
            if not options['name'].value:
                self.werr_nolog(
                    "%s: The name of command/builder must be specified.\n\n" \
                    % self.get_name()
                )
                return EXIT_FAILURE
            r, m = add_command(options['name'].value)
            if not r:
                self.__v and self.werr("%s: %s.\n" % (self.get_name(), m))
                return EXIT_FAILURE
            self.__v and self.wout(
                "%s: Adding new command `%s` has been successful.\n" \
                % (self.get_name(), options['name'].value)
            )
        else:
            self.werr_nolog(
                "%s: Unknown action (internal error).\n\n" % self.get_name()
            )
            return INTERNAL_ERROR
        return EXIT_SUCCESS
    #-def

    @staticmethod
    def description():
        """
        """

        return "adds new command/builder/etc. to parser generator"
    #-def

    def on_builder_option(self, opt):
        """
        """

        self.__element_type = self.BUILDER
    #-def
#-class

class ParserGenerator(Application):
    """
    """
    __slots__ = [ '__helppage', '__noargs', '__commands', '__quite_mode' ]

    def __init__(self, owner = None, **kwargs):
        """
        """

        Application.__init__(self, owner, **kwargs)
        self.__helppage = CharBuffer(self)
        self.__noargs = CharBuffer(self)
        self.__commands = dict([(x.name(), x) for x in [Help, Add]])
        self.__quite_mode = False
    #-def

    def at_start(self):
        """
        """

        self.load_commands()

        oc = self.get_option_processor().get_option_class()

        self.define_option(
            "quite", ['q'],
            about = "suppress all messages"
        )
        self.define_option(
            "help", ['h', '?'],
            about = "print this screen and exit",
            cb = self.on_help_option
        )

        helppage = PageBuilder()
        helppage.paragraph("""
        Usage:\\ %s\\ [program\\ options]\\ <command>\\ [command\\ options]
        """ % escape(self.get_name()))
        helppage.paragraph("""
        where "program\\ options" are:
        """)
        helppage.table(self.list_options())
        helppage.paragraph("""
        The available commands are:
        """)
        helppage.table(self.list_commands())
        helppage.paragraph("""
        To see more detailed informations about specific command, type
        `%(appname)s\\ help\\ <command>` or
        `%(appname)s\\ <command>\\ %(longprefix)shelp`.
        """ % dict(
            appname = escape(self.get_name()),
            longprefix = oc.LONG_PREFIX
        ))
        PageFormatter().format(helppage.page, self.__helppage)

        noargs = PageBuilder()
        noargs.paragraph("""
        %(appname)s: No arguments were specified. Type
        `%(appname)s\\ %(longprefix)shelp` to see how to use me.
        """ % dict(
            appname = escape(self.get_name()),
            longprefix = oc.LONG_PREFIX
        ))
        PageFormatter().format(noargs.page, self.__noargs)
    #-def

    def list_commands(self):
        """
        """

        table = TableBuilder(col0 = 10, sep0 = 8, col1 = 60)
        cs = list(self.__commands.keys())
        cs.sort()
        for c in cs:
            table.row(
                PageBuilder.to_words(c),
                PageBuilder.to_words(self.__commands[c].description())
            )
        return table
    #-def

    def load_commands(self):
        """
        """

        commands = get_commands()
        if commands is None:
            raise ApplicationError(
                "Reading commands from cache was unsuccessful"
            )
        for cmd in commands:
            if cmd.name() in self.__commands:
                raise ApplicationError(
                    "Command '%s' is already loaded" % cmd.name()
                )
            self.__commands[cmd.name()] = cmd
    #-def

    def main(self):
        """
        """

        options = self.get_option_processor().get_options()
        if options['help'].when_given >= 0:
            self.werr_nolog(self.__helppage)
            return EXIT_FAILURE
        self.__quite_mode = options['quite'].when_given >= 0
        pending_args = self.get_pending_args()
        if not pending_args and not options.get_given_options():
            self.werr_nolog(self.__noargs)
            return EXIT_FAILURE
        if not pending_args:
            return EXIT_SUCCESS
        command = pending_args.pop(0)
        if command not in self.__commands:
            self.werr_nolog(
                "%s: Unknown command '%s'.\n\n" % (self.get_name(), command)
            )
            return EXIT_FAILURE
        command = self.__commands[command](
            owner = self,
            commands = self.__commands,
            quite = self.__quite_mode
        )
        return command.run(pending_args)
    #-def

    def at_end(self):
        """
        """

        log = self.get_log()
        if not str(log):
            return
        eh = WithStatementExceptionHandler()
        with eh, log as l:
            l.flush()
        if eh.etype:
            sys.__stderr__.write("Writing to the log file has failed.\n")
    #-def
#-class
