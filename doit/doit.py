#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/doit.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-02-27 11:14:10 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! interpreter.\
"""

__license__ = """\
Copyright (c) 2014 Jiří Kučera.

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
import utils
import commands

from errors import perror, DoItError

try:
    __script_file = __file__
except NameError:
    __script_file = sys.argv[0]
if __script_file == "":
    __script_dir = "."
else:
    __script_dir = os.path.dirname(os.path.abspath(__script_file))

CFG_PATH = "./doit.cfg;" \
           "./cfg/doit.cfg;" \
           "./cfg/dev/doit.cfg;" \
           "%s/cfg/doit.cfg" % utils.sys2path(__script_dir)

def main(args):
    """main(args) -> integer

    Script entry point. Return the exit code.
    """

    try:
        context = Context()
        context.newgvar('CFG_PATH', String(CFG_PATH))
        context.parser = DoItParser(DoItLexer(context))
        sh = ShellCommand(None, ('', -1))
        sh.add_param('--config=$CFG_PATH')
        sh.run(context)
        return context.result.exitcode
    except DoItError as e:
        perror(e.detail)
        return e.errcode
    return 0
#-def

if __name__ == '__main__':
    exit(main(sys.argv))
#-if
