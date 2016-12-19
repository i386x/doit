#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/builders/cfg2glap.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-11 09:08:57 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Converts context-free grammar to the GLAP definition file.\
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

import os

from doit.support.app.io import CharBuffer
from doit.support.app.printer import PageFormatter, PageBuilder
from doit.support.app.application import EXIT_SUCCESS, EXIT_FAILURE

from doit.text.pgen.builders.builder import Builder

class Cfg2Glap(Builder):
    """
    """
    __slots__ = [ '__helppage', '__v' ]

    def __init__(self, owner, **kwargs):
        """
        """

        Builder.__init__(self, owner, **kwargs)
        self.set_name(self.name())
        self.set_output(owner.get_output())
        self.set_log(owner.get_log())
        self.set_error_log(owner.get_error_log())
        self.set_cwd(owner.get_cwd())

        self.__helppage = CharBuffer(self)
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
        self.define_kwoption(
            "input", ['i'],
            about = """"
            path to or dotted name of a Python package with context-free
            grammar; this option is required
            """,
            flags = oc.REQUIRED
        )
        self.define_kwoption(
            "output", ['o'],
            about = """
            directory to which the result should be dumped; this option is
            required
            """,
            flags = oc.REQUIRED
        )
        self.define_kwoption(
            "format", ['f'],
            about = """
            path to or dottet name of a Python package with formatting rules;
            the default is given by config value
            """
        )

        helppage = PageBuilder()
        helppage.paragraph("""
        %s\\ [options]
        """ % self.get_name())
        helppage.paragraph("""
        Dumps module with context-free grammar to GLAP source file.
        """)
        helppage.paragraph("""
        The module that contains one or more context-free grammars and
        submodules is loaded as a regular Python package and it contains also
        informations about how it should be dumped, which files and directories
        should be created etc. The final structure containing generated source
        files in GLAP language and directories is dumped to the prespecified
        source directory.
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
        srcobj = self.load_source(options['input'].value)
        if not srcobj:
            return EXIT_FAILURE
        output_dir = os.path.realpath(options['output'].value)
        if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
            self.werr_nolog(
                "%s: Invalid output directory.\n" % self.get_name()
            )
            return EXIT_FAILURE
        fmtpath = options['format'].value
        if not fmtpath:
            fmtpath = self.get_owner().get_config_value('fmtdir')
        fmtmod = self.load_formatter(fmtpath)
        return EXIT_SUCCESS
    #-def

    def handle_error(self, e):
        """
        """

        self.werr_nolog("%s.\n" % e.detail)
        self.set_exitcode(EXIT_FAILURE)
    #-def

    @staticmethod
    def description():
        """
        """

        return "dumps module with context-free grammar to GLAP source file"
    #-def

    def load_source(self, path):
        """
        """

        nm = self.get_name()
        if not path:
            self.werr("%s: No path to source package specified.\n" % nm)
            return None
        srcmod = self.load_module(path, 'bootstrap', 'get_source')
        if not srcmod:
            self.werr("%s: No source package found at <%s>.\n" % (nm, path))
            return None
        return srcmod.get_source()
    #-def

    def load_formatter(self, path):
        """
        """

        if not path:
            self.nofmt("output files")
            return None
        fmtmod = self.load_module(path, 'fmt', 'get_formatter')
        if not fmtmod:
            self.werr(
                "%s: Formatter package not found at <%s>.\n" % (
                    self.get_name(), path
                )
            )
            self.nofmt("output files")
            return None
        return fmtmod
    #-def

    def nofmt(self, what):
        """
        """

        self.__v and self.wout(
            "%s: No formatting for %s will be used.\n" % (
                self.get_name(), what
            )
        )
    #-def
#-class

def get_command_class():
    """
    """

    return Cfg2Glap
#-def
