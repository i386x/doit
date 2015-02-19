#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/lang.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-05-28 09:43:05 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! language support.\
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

class Value(object):
    """
    """
    __slots__ = [ '__type', '__data' ]

    def __init__(self, type, data):
        """
        """

        self.__type = type
        self.__data = data
    #-def

    def type(self):
        """
        """

        return self.__type
    #-def

    def data(self):
        """
        """

        return self.__data
    #-def

    def copy(self):
        """
        """

        return Value(self.__type, self.__data)
    #-def
#-class

class Undefined(Value):
    """
    """

    def __init__(self):
        """
        """

        Value.__init__(self, self.__class__.__name__, None)
    #-def
#-class

class Null(Value):
    """
    """

    def __init__(self):
        """
        """

        Value.__init__(self, self.__class__.__name__, None)
    #-def
#-class

class HostString(Value):
    """
    """

    def __init__(self, data = ""):
        """
        """

        Value.__init__(self, self.__class__.__name__, data)
    #-def

    def copy(self):
        """
        """

        return Value(self.type, "%s" % self.data())
    #-def
#-class

class HostList(Value):
    """
    """

    def __init__(self, data = []):
        """
        """

        Value.__init__(self, self.__class__.__name__, data)
    #-def
#-class

class HostFunction(Value):
    """
    """

    def __init__(self, data = lambda state: pass):
        """
        """

        Value.__init__(self, self.__class__.__name__, data)
    #-def
#-class

class Item(object):
    """
    """
    __slots__ = [ 'value', 'is_const' ]

    def __init__(self, value, is_const):
        """
        """

        self.value = value
        self.is_const = is_const
    #-def
#-class

class Member(Item):
    """
    """
    __slots__ = [ 'privacy' ]

    def __init__(self, value, is_const, privacy):
        """
        """

        Item.__init__(self, value, is_const)
        self.privacy = privacy
    #-def
#-class

class Object(Value):
    """
    """

    def __init__(self):
        """
        """

        Value.__init__(self, self.__class__.__name__, {})
    #-def

    def __setitem__(self, key, value):
        """
        """

        self.data()[key] = value
    #-def

    def __getitem__(self, key):
        """
        """

        return self.data()[key]
    #-def

    def __delitem__(self, key):
        """
        """

        if not key in self:
            return
        del self.data()[key]
    #-def

    def __contains__(self, item):
        """
        """

        return self.get(item) is not None
    #-def

    def get(self, key, default = None):
        """
        """

        return self.data().get(key, default)
    #-def

    def set_member(self, name, value, is_const, privacy):
        """
        """

        self[name] = Member(value, is_const, privacy)
    #-def
#-class

class Environment(object):
    """
    """
    __slots__ = [ '__prev', '__vars', '__varlist' ]

    def __init__(self, env = None):
        """
        """

        self.__prev = env
        self.__vars = {}
        self.__varlist = []
    #-def

    def __setitem__(self, key, value):
        """
        """

        if key not in self.__varlist:
            self.__varlist.append(key)
        self.__vars[key] = value
    #-def

    def __getitem__(self, key):
        """
        """

        value = self.__vars.get(key, None)
        if value is None and self.__prev is not None:
            value = self.__prev[key]
        return value
    #-def

    def __delitem__(self, key):
        """
        """

        if not key in self.__varlist:
            return
        del self.__vars[key]
        self.__varlist.remove(key)
    #-def

    def set_item(self, name, value, is_const):
        """
        """

        self[name] = Item(value, is_const)
    #-def

    def clear(self):
        """
        """

        while self.__varlist:
            del self.__vars[self.__varlist.pop()]
    #-def
#-class
