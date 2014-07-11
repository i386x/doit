#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/objects.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-07-11 15:26:12 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! objects.\
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

def method(name):
    """
    """

    def f(cf):
        cf.doit_method = name
        return cf
    return f
#-def

class Method(object):
    """Method wrapper for deferred method invocation.
    """
    __slots__ = []

    def __init__(self, name, *args):
        """
        """

        self.__name = name
        self.__args = args
    #-def

    def invoke(self, obj, ctx):
        """
        """

        args = [arg.eval(ctx) for arg in self.__args)]
        method = obj.get_method(name)
        
    #-def
#-class

class Object(object):
    """
    """
    __slots__ = [ 'content', '__methods' ]

    def __init__(self, content):
        """
        """

        self.content = content
        self.make_methods()
    #-def

    def make_methods(self):
        """
        """

        self.__methods = {}
        for sattr in dir(self):
            attr = getattr(self, sattr)
            if type(attr) is not types.FunctionType
            or 'doit_method' not in dir(attr):
                continue
            self.__methods[attr.doit_method] = attr
    #-def

    def attached_to(self, ctx, owner):
        """
        """

        return self
    #-def

    def detached_from(self, ctx, owner):
        """
        """

        pass
    #-def

    @method("prefix operator ++")
    def dispose(self, ctx):
        """
        """

        pass
    #-def
#-class

class ReferableObject(Object):
    """
    """
    __slots__ = [ 'owners' ]

    def __init__(self, content):
        """
        """

        Object.__init__(self, content)
        self.owners = []
    #-def

    def attached_to(self, ctx, owner):
        """
        """

        if not owner in self.owners:
            self.owners.append(owner)
        return self
    #-def

    def detached_from(self, ctx, owner):
        """
        """

        check(ctx, owner in self.owners,
            "%s: variable %s is not owner of this object"
            % (self.__class__.__name__, owner.name)
        )
        self.owners.remove(owner)
        if not self.owners:
            self.dispose(ctx)
    #-def
#-class

class CopyableObject(Object):
    """
    """
    __slots__ = []

    def __init__(self, content):
        """
        """

        Object.__init__(self, content)
    #-def

    def attached_to(self, ctx, owner):
        """
        """

        return self.clone(ctx)
    #-def

    def detached_from(self, ctx, owner):
        """
        """

        self.dispose(ctx)
    #-def

    def clone(self, ctx):
        """
        """

        raise NotImplementedError
    #-def
#-class

class IntObject(CopyableObject):
    """
    """

    def __init__(self, value):
        """
        """

        CopyableObject.__init__(self, value)
    #-def

    def clone(self, ctx):
        """
        """

        return self.__class__(self.content)
    #-def

    @method("prefix operator -")
    def m_neg(self, ctx):
        """
        """

        return self.__class__(-self.content)
    #-def

    @method("operator +")
    def m_add(self, ctx, rhs):
        """
        """

        if isinstance(rhs, FloatObject):
            return FloatObject(self.content + rhs.content)
        elif isinstance(rhs, self.__class__):
            return self.__class__(self.content + rhs.content)
        ...
    #-def
#-class
