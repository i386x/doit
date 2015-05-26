#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/runtime/atoms.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-05-28 09:43:05 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! atomic data types.\
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

class Pointer(object):
    """
    """
    __slots__ = [ '__segment', '__offset' ]

    def __init__(self, segment, offset):
        """
        """

        self.__segment = segment
        self.__offset = offset
    #-def

    def read(self):
        """
        """

        return self.__segment[self.__offset]
    #-def

    def write(self, data):
        """
        """

        self.__segment[self.__offset] = data
    #-def

    def __add__(self, i):
        """
        """

        return self.__class__(self.__segment, self.__offset + i)
    #-def

    def __iadd__(self, i):
        """
        """

        self.__offset += i
        return self
    #-def

    def __sub__(self, i):
        """
        """

        return self.__class__(self.__segment, self.__offset - i)
    #-def

    def __isub__(self, i):
        """
        """

        self.__offset -= i
        return self
    #-def

    def __setitem__(self, i, v):
        """
        """

        self.__segment[self.__offset + i] = v
    #-def

    def __getitem__(self, i):
        """
        """

        return self.__segment[self.__offset + i]
    #-def
#-class

class Closure(Code):
    """
    """

    def __init__(self, obj, f):
        """
        """

        Code.__init__(self)
        sp = self.rsp
        self.\
          push([sp - 1]).\
          move([sp - 2], obj).\
          jump(f).\
        assemble()
    #-def
#-class

class Object(object):
    """
    """
    __slots__ = [ '__vars', '__varlist' ]

    def __init__(self):
        """
        """

        self.__vars = {}
        self.__varlist = []
    #-def

    def defvar(self, name, value = DoIt.Null):
        """
        """

        if name not in self.__varlist:
            self.__varlist.append(name)
        self.__vars[name] = value
    #-def

    def undefvar(self, name):
        """
        """

        if name not in self.__varlist:
            return False
        self.__varlist.remove(name)
        del self.__vars[name]
        return True
    #-def

    def setvar(self, name, value):
        """
        """

        if name not in self.__varlist:
            return False
        self.__vars[name] = value
        return True
    #-def

    def getvar(self, name):
        """
        """

        return self.__vars.get(name, DoIt.Undefined)
    #-def

    def hasvar(self, name):
        """
        """

        return self.getvar(name).__class__ is not DoIt.Undefined
    #-def

    def bind(self, name, f):
        """
        """

        self.defvar(name, make_closure(self, f))
    #-def

    def clear(self):
        """
        """

        while self.__varlist:
            self.undefvar(self.__varlist[-1])
    #-def
#-class

is_bool = lambda t: isinstance(t, bool)
is_int = lambda t: isinstance(t, int)
is_float = lambda t: isinstance(t, float)
is_str = lambda t: isinstance(t, str)
is_list = lambda t: isinstance(t, list)
is_dict = lambda t: isinstance(t, dict)
is_undefined = lambda t: t is DoIt.Undefined
is_null = lambda t: t is DoIt.Null
is_pointer = lambda t: isinstance(t, Pointer)
is_object = lambda t: isinstance(t, Object)
is_atom = lambda t: is_bool(t) or is_int(t) or is_float(t) or is_str(t)       \
                 or is_list(t) or is_dict(t)                                  \
                 or is_undefined(t) or is_null(t)                             \
                 or is_pointer(t) or is_object(t)
