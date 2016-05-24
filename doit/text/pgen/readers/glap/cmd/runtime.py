#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/cmd/runtime.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-04-01 13:05:11 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor runtime.\
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

from doit.text.pgen.readers.glap.cmd.errors import \
    CmdExceptionError, \
    CmdTypeError

class BaseIterator(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def

    def reset(self):
        """
        """

        pass
    #-def

    def next(self):
        """
        """

        return self
    #-def
#-class

class FiniteIterator(BaseIterator):
    """
    """
    __slots__ = [ '__items', '__nitems', '__idx' ]

    def __init__(self, items):
        """
        """

        if not (hasattr(items, '__len__') and hasattr(items, '__getitem__')):
            raise CmdTypeError(
                "Iterator is initialized with non-iterable object"
            )
        BaseIterator.__init__(self)
        self.__items = items
        self.__nitems = len(items)
        self.__idx = 0
    #-def

    def reset(self):
        """
        """

        self.__idx = 0
    #-def

    def next(self):
        """
        """

        if self.__idx < self.__nitems:
            x = self.__items[self.__idx]
            self.__idx += 1
            return x
        return self
    #-def
#-class

class ExceptionClass(object):
    """
    """
    __slots__ = [ '__container', '__name', '__base' ]

    def __init__(self, container, name, base):
        """
        """

        self.__container = container
        self.__name = name
        self.__base = base
    #-def

    def name(self):
        """
        """

        return self.__name
    #-def

    def base(self):
        """
        """

        return self.__base
    #-def

    def is_superclass_of(self, cls):
        """
        """

        if not isinstance(cls, ExceptionClass):
            return False
        if cls.name() not in self.__container:
            return False
        if self.__container[cls.name()] is not cls:
            return False
        if self is cls:
            return True
        return self.is_superclass_of(cls.base())
    #-def
#-class

class BaseExceptionClass(ExceptionClass):
    """
    """
    __slots__ = []

    def __init__(self, container):
        """
        """

        ExceptionClass.__init__(self, container, 'BaseException', None)
    #-def
#-class

class Exceptions(dict):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        dict.__init__(self)
        base = BaseExceptionClass(self)
        self[base.name()] = base
    #-def

    def register_exception(self, name, basename):
        """
        """

        if name in self:
            raise CmdExceptionError(
                "Exception %s is already registered" % name
            )
        if basename not in self:
            raise CmdExceptionError("Unknown exception base %s" % basename)
        self[name] = ExceptionClass(self, name, self[basename])
    #-def

    def register_exceptions(self, *specs):
        """
        """

        for name, basename in specs:
            self.register_exception(name, basename)
    #-def
#-class

class Traceback(list):
    """
    """
    __slots__ = [ '__punctator' ]

    def __init__(self, stack):
        """
        """

        list.__init__(self, [cmd for cmd in stack if cmd.isfunc()])
        self.__punctator = ">"
        if stack:
            f, l, c = stack[-1].location
            if f is not None and l >= 0 and c >= 0:
                self.__punctator += " At [\"%s\":%d:%d]:" % (f, l, c)
    #-def

    def __str__(self):
        """
        """

        if len(self) == 0:
            return "In <main>:\n"
        s = "In %s" % self[0]
        i = 1
        while i < len(self):
            s += "\n| from %s" % self[i]
            i += 1
        return "%s:\n%s" % (s, self.__punctator)
    #-def
#-class

class ProcedureTemplate(tuple):
    """
    """
    __slots__ = []

    def __new__(cls, bvars, params, body, outer):
        """
        """

        return super(ProcedureTemplate, cls).__new__(
            cls, (bvars, params, body, outer)
        )
    #-def

    def __init__(self, bvars, params, body, outer):
        """
        """

        tuple.__init__(self)
    #-def
#-class
