#                                                         -*- coding: utf-8 -*-
#! \file    ./ndash.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-11-22 22:54:35 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Replace `--` by `&#8211;`.\
"""

__license__ = """\
Copyright (c) 2014 - 2015 Jiří Kučera.

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

from doit.support.utils import WithStatementExceptionHandler

def main(argv):
    wseh = WithStatementExceptionHandler()

    if len(argv) < 2:
        sys.stderr.write("%s: Not enough arguments.\n" % argv[0])
        return 1

    with wseh, open(argv[1], "rb") as fd:
        fcontent = fd.read()
    if wseh.etype is not None:
        sys.stderr.write("%s: Can't read from %s.\n" % tuple(argv[:2]))
        return 1

    fcontent = fcontent.replace(b"--", b"&#8211;")

    with wseh, open(argv[1], "wb") as fd:
        fd.write(fcontent)
    if wseh.etype is not None:
        sys.stderr.write("%s: Can't write to %s.\n" % tuple(argv[:2]))
        return 1

    return 0
#-def

if __name__ == '__main__':
    exit(main(sys.argv))
#-if
