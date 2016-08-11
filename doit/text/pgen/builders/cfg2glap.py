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

class Cfg2Glap(Builder):
    """
    """
    __slots__ = []

    def __init__(self, owner):
        """
        """

        Builder.__init__(self, owner)
        self.set_name(self.__class__.__name__.lower())
    #-def

    def define_options(self):
        """
        """

        self.define_option(
            "help", ['h', '?'],
            about = "print this screen and exit",
            cb = self.on_help_option
        )
        self.define_kwoption(
            "input", ['i'],
            about = "directory representing Python package from which the\n" \
            "module containing context-free grammar is imported; this\n" \
            "option is required",
            flags = Option.MANDATORY
        )
        self.define_kwoption(
            "output", ['o'],
            about = "directory to which the result should be dumped; this\n" \
            "option is required",
            flags = Option.MANDATORY
        )
        self.define_kwoption(
            "format", ['f'],
            about = "directory containing a formatting rules for output;\n" \
            "a directory is viewed as Python package; the default\n" \
            "directory is given by config value"
        )
    #-def

    def short_help(self):
        """
        """

        return "dumps module with context-free grammar to GLAP source file"
    #-def

    def print_help(self):
        """
        """

        self.werr(self.strip_block("""\
        %(cmdname)s [options]

        Dumps module with context-free grammar to GLAP source file. The module
        that contains one or more context-free grammars and submodules is
        loaded as a regular Python package and it contains also informations
        about how it should be dumped, which files and directories should be
        created etc. The final structure containing generated source files in
        GLAP language and directories is dumped to the prespecified source
        directory.

        Options:
        %(options)s
        """)
    #-def

    def build(self, **opts):
        """
        """

        output_dir = opts.get('output_dir')
        if not output_dir:
            raise PgenError(
                "Cfg2Glap.build: Output directory is not specified"
            )
        self.check_opts(opts)
        self.dump_files(opts)
    #-def

    def check_opts(self, opts):
        """
        """

        with OptionChecker(self, opts) as oc:
            oc.mandatory('input', "Input is not specified")
            oc.mandatory('target_dir', "Target directory is not specified")
            oc.optional('log_dir')
    #-def

    def dump_files(self, opts):
        """
        """

        for m in opts.get('modules'):
            self.dump_module(m, opts)
    #-def

    def dump_module(self, m, opts):
        """
        """

        with GlapWriter(self, m.fname, opts) as writer:
            writer.write(m)
    #-def
#-class

def load():
    """
    """

    return Cfg2Glap
#-def
