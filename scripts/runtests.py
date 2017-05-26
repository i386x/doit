#                                                         -*- coding: utf-8 -*-
#! \file    ./runtests.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-04-09 22:37:26 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Run all DoIt! tests.\
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

import sys
import os
import unittest

here = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(here, os.pardir)
sys.path.insert(0, root)

import tests

# Based on unittest/runner.py _WritelnDecorator and on sys.dysplayhook
# pseudocode from the standard Python documentation. One does not simply
# `sys.stdout.errors = 'backslashreplace'` .
class _WriteDecorator(object):
    __slots__ = [ 'stream' ]

    def __init__(self, stream):
        self.stream = stream
    #-def

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            return AttributeError(attr)
        return getattr(self.stream, attr)
    #-def

    def write(self, text):
        try:
            self.stream.write(text)
        except UnicodeEncodeError:
            bytes = text.encode(self.stream.encoding, 'backslashreplace')
            if hasattr(self.stream, 'buffer'):
                self.stream.buffer.write(bytes)
            else:
                text = bytes.decode(self.stream.encoding, 'strict')
                self.stream.write(text)
    #-def
#-class

if __name__ == '__main__':
    stream = _WriteDecorator(sys.stdout)
    unittest.TextTestRunner(stream, True, 2).run(tests.suite())
#-if
