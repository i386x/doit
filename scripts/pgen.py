#                                                         -*- coding: utf-8 -*-
#! \file    ./pgen.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-09-06 13:49:00 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Parser generator.\
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

here = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(here, os.pardir)

sys.path.insert(0, root)

from doit.support.app.logging import Log
from doit.text.pgen import ParserGenerator

class PGen(ParserGenerator):
    __slots__ = []

    def __init__(self, path):
        ParserGenerator.__init__(self)
        self.set_path(path)
        log = Log(self).wrap(stdout = sys.stdout, stderr = sys.stderr)
        self.set_output(log.stdout)
        self.set_log(log)
        self.set_error_log(log.stderr)
    #-def
#-class

if __name__ == '__main__':
    exit(PGen(__file__).run(sys.argv[1:]))
#-if
