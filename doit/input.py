#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/input.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-06-25 18:29:37 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! input handling.\
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

from . import errors
from .support.utils import doit_read

class Input(object):
    """Input holder class.
    """
    __slots__ = [ 'name', 'offset', 'size', 'data' ]

    def __init__(self, name, data):
        """Input(name, data) -> instance of Input

        Constructor.
        """

        self.name = name
        self.offset = 0
        self.size = len(data)
        self.data = data
    #-def

    def position(self, offset = -1):
        """position([offset]) -> (integer, integer)

        Return pair (line number, character position) in input stream at given
        offset. If offset is ommited, current offset in input stream is used.
        """

        lnum = cpos = i = 0
        if offset < 0:
            offset = self.offset
        while i < self.offset:
            cpos += 1
            if self.data[i] == '\n':
                cpos = 0
                lnum += 1
            i += 1
        return lnum, cpos
    #-def
#-class

class Inputs(object):
    """Implements input stack.
    """
    __slots__ = [ '__inputs' ]

    def __init__(self):
        """Inputs() -> instance of Inputs

        Constructor.
        """

        self.__inputs = []
    #-def

    def push_from_file(self, fpath):
        """push_from_file(fpath)

        Load the content of file at fpath location and push it onto the input
        stack. Raise an IOError exception if operation fails.
        """

        s = doit_read(fpath)
        if s is None:
            raise errors.IOError("Cannot read from file '%s'." % fpath)
        self.__inputs.append(Input(fpath, s))
    #-def

    def push_from_str(self, name, s):
        """push_from_str(name, s)

        Push s onto the input stack.
        """

        self.__inputs.append(Input(name, s))
    #-def

    def empty(self):
        """empty() -> bool

        Return True if input stack is empty.
        """

        return len(self.__inputs) == 0
    #-def

    def pop(self):
        """pop()

        Remove the topmost item from input stack.
        """

        if self.empty():
            return
        self.__inputs.pop()
    #-def

    def current(self):
        """current() -> instance of Input or None

        Return the topmost item from input stack or None.
        """

        if self.empty():
            return None
        return self.__inputs[-1]
    #-def
#-class
