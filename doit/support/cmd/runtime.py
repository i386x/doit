#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/cmd/runtime.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-04-01 13:05:11 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Command processor's runtime utilities.\
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

from doit.support.utils import deep_eq

from doit.support.cmd.errors import \
    CommandError

def isderived(exc, base):
    """
    """

    if not isinstance(exc, ExceptionClass):
        return False
    while exc:
        if exc is base:
            return True
        exc = exc.base()
    return False
#-def

class Location(tuple):
    """
    """
    __slots__ = []

    def __new__(cls, file = None, line = -1, column = -1):
        """
        """

        return super(Location, cls).__new__(cls, (file, line, column))
    #-def

    def __init__(self, file = None, line = -1, column = -1):
        """
        """

        tuple.__init__(self)
    #-def

    def file(self):
        """
        """

        return self[0]
    #-def

    def line(self):
        """
        """

        return self[1]
    #-def

    def column(self):
        """
        """

        return self[2]
    #-def

    def __str__(self):
        """
        """

        f, l, c = self
        if f is None or l < 0 or c < 0:
            return "(internal)"
        return "at [\"%s\":%d:%d]" % self
    #-def
#-class

class Evaluable(object):
    """
    """

    def __init__(self):
        """
        """

        self.location = Location()
        self.properties = {}
    #-def

    def set_location(self, file = None, line = -1, column = -1):
        """
        """

        self.location = Location(file, line, column)
        return self
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and self.location == other.location \
        and deep_eq(self.properties, other.properties)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def
#-class

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

class Iterable(Evaluable):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Evaluable.__init__(self)
    #-def

    def iterator(self):
        """
        """

        return BaseIterator()
    #-def
#-class

class Pair(tuple, Iterable):
    """
    """
    __slots__ = []

    def __new__(cls, a, b):
        """
        """

        return super(Pair, cls).__new__(cls, (a, b))
    #-def

    def __init__(self, a, b):
        """
        """

        tuple.__init__(self)
        Iterable.__init__(self)
    #-def

    def iterator(self):
        """
        """

        return FiniteIterator(self)
    #-def
#-class

class List(list, Iterable):
    """
    """
    __slots__ = []

    def __init__(self, data = []):
        """
        """

        list.__init__(self, data)
        Iterable.__init__(self)
    #-def

    def iterator(self):
        """
        """

        return FiniteIterator(self)
    #-def

    @staticmethod
    def unique(l):
        """
        """

        r = List([])
        for x in l:
            if x not in r:
                r.append(x)
        return r
    #-def
#-class

class HashMap(dict, Iterable):
    """
    """
    __slots__ = []

    def __init__(self, data = {}):
        """
        """

        dict.__init__(self, data)
        Iterable.__init__(self)
    #-def

    def iterator(self):
        """
        """

        return FiniteIterator(list(self.keys()))
    #-def

    @staticmethod
    def merge(d1, d2):
        """
        """

        r = HashMap(d1)
        r.update(d2)
        return r
    #-def
#-class

class UserType(Evaluable):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Evaluable.__init__(self)
    #-def

    def __eq__(self, other):
        """
        """

        return isinstance(other, self.__class__) \
        and Evaluable.__eq__(self, other)
    #-def

    def __ne__(self, other):
        """
        """

        return not self.__eq__(other)
    #-def

    def to_bool(self, processor):
        """
        """

        return True
    #-def

    def to_int(self, processor):
        """
        """

        raise CommandError(processor.TypeError,
            "%s is not convertible to integer" % self.__class__.__name__,
            processor.traceback()
        )
    #-def

    def to_float(self, processor):
        """
        """

        raise CommandError(processor.TypeError,
            "%s is not convertible to float" % self.__class__.__name__,
            processor.traceback()
        )
    #-def

    def to_str(self, processor):
        """
        """

        raise CommandError(processor.TypeError,
            "%s is not convertible to string" % self.__class__.__name__,
            processor.traceback()
        )
    #-def

    def to_pair(self, processor):
        """
        """

        raise CommandError(processor.TypeError,
            "%s is not convertible to pair" % self.__class__.__name__,
            processor.traceback()
        )
    #-def

    def to_list(self, processor):
        """
        """

        raise CommandError(processor.TypeError,
            "%s is not convertible to list" % self.__class__.__name__,
            processor.traceback()
        )
    #-def

    def to_hash(self, processor):
        """
        """

        raise CommandError(processor.TypeError,
            "%s is not convertible to hash" % self.__class__.__name__,
            processor.traceback()
        )
    #-def

    def do_visit(self, processor, f, *args):
        """
        """

        raise CommandError(processor.TypeError,
            "%s is not visitable" % self.__class__.__name__,
            processor.traceback()
        )
    #-def
#-class

class ExceptionClass(object):
    """
    """
    __slots__ = [ '__name', 'qname', '__base' ]

    def __init__(self, name, qname, base):
        """
        """

        self.__name = name
        self.qname = qname
        self.__base = base
    #-def

    def __str__(self):
        """
        """

        return self.__name
    #-def

    def base(self):
        """
        """

        return self.__base
    #-def
#-class

class Traceback(list):
    """
    """
    __slots__ = [ '__punctator' ]

    def __init__(self, stack):
        """
        """

        list.__init__(self, [ctx.cmd for ctx in stack if ctx.cmd.isfunc()])
        self.__punctator = ">"
        if stack:
            f, l, c = stack[-1].cmd.location
            if f is not None and l >= 0 and c >= 0:
                self.__punctator += " At [\"%s\":%d:%d]:" % (f, l, c)
    #-def

    def __str__(self):
        """
        """

        if len(self) == 0:
            self.append("<main>")
        s = "In %s" % self[0]
        i = 1
        while i < len(self):
            s += "\n| from %s" % self[i]
            i += 1
        return "%s:\n%s" % (s, self.__punctator)
    #-def
#-class

class Procedure(tuple):
    """
    """
    __slots__ = []

    def __new__(cls, name, qname, bvars, params, vararg, body, outer):
        """
        """

        return super(Procedure, cls).__new__(
            cls, (name, qname, bvars, params, vararg, body, outer)
        )
    #-def

    def __init__(self, name, qname, bvars, params, vararg, body, outer):
        """
        """

        tuple.__init__(self)
    #-def
#-class
