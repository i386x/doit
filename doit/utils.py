#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/utils.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-02-27 18:26:58 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! utilities.\
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

import os

def sys2path(p):
    """sys2path(p) -> str

    Return a system path p converted to DoIt! universal path.
    """

    d = os.path.dirname(p)
    b = os.path.basename(p)
    if d == '':
        return b
    d = d.replace(os.sep, '/').replace(os.pardir, '..').replace(os.curdir, '.')
    return "%s/%s" % (d, b)
#-def

def path2sys(p):
    """path2sys(p) -> str

    Return a universal DoIt! path p converted to system path. Universal DoIt!
    path can be only relative.
    """

    if p.startswith("./"):
        p = p[2:]
    def f(x):
        if x == '.':
            return os.curdir
        elif x == '..':
            return os.pardir
        return x
    return os.path.join(*[f(x) for x in p.split('/')])
#-def

class WithStatementExceptionHandler(object):
    """Implements exception handler which catch any exception raised inside
       with-statement.
    """
    __slots__ = [ 'etype', 'evalue', 'etraceback' ]

    def __init__(self):
        """WithStatementExceptionHandler()
             -> instance of WithStatementExceptionHandler

        Constructor.
        """

        self.etype = None
        self.evalue = None
        self.etraceback = None
    #-def

    def __enter__(self):
        """__enter__() -> instance of WithStatementExceptionHandler

        Called when entering to with-statement.
        """

        return self
    #-def

    def __exit__(self, etype, evalue, etraceback):
        """__exit__(etype, evalue, etraceback) -> instance of bool

        Called when exiting from with-statement.
        """

        self.etype = etype
        self.evalue = evalue
        self.etraceback = etraceback
        return True
    #-def
#-class

def doit_read(fpath):
    """doit_read(fpath) -> str or None

    Read the text file encoded in UTF-8 at fpath location and return its
    content or None in case of error.
    """

    s = ""
    wseh = WithStatementExceptionHandler()
    with wseh, open(path2sys(fpath), 'r', encoding = 'utf-8') as f:
        s = f.read()
    if wseh.evalue is not None:
        return None
    return s
#-def

#
# Based on Pygments _TokenType from pygments-main/pygments/token.py
# (http://pygments.org/)
# 
class Collection(object):
    """A factory for making unique objects. Each object has attribute `name'
    with its name and `qname' with its qualified name (complete path).

    Example of use:
        # Create an anonymous object:
        a = Collection()
        # Create new object named 'ItemA':
        ItemA = Collection("ItemA")
        # Create a subobject named 'SubItem1':
        SubItem1 = ItemA.SubItem1
        # Create new object 'ItemB' and inherits subobjects from 'ItemA':
        ItemB = Collection("ItemB", "ItemA")
    """
    __slots__ = [ 'name', 'qname', 'siblings' ]
    collections = {}
    __locked = False

    def __new__(cls, *args):
        """__new__(...) -> instance of Collection

        Preconstructor. Called with no argument, creates an anonymous instance
        of Collection. Otherwise, the first argument is the name of the new
        instance, and the rest of arguments are names of instances to be
        inherited. Note that the existing object is returned instead of
        creating a new one with the same name.
        """

        assert not cls.__locked, "Collection is locked."
        if len(args) == 0:
            inst = object.__new__(cls)
            setattr(inst, 'name', repr(inst))
            setattr(inst, 'qname', repr(inst))
            setattr(inst, 'siblings', {})
            return inst
        name = args[0]
        inst = cls.collections.get(name, None)
        if inst is not None:
            return inst
        cls.collections[name] = inst = object.__new__(cls)
        setattr(inst, 'name', name)
        setattr(inst, 'qname', name)
        setattr(inst, 'siblings', {})
        for p in args[1:]:
            cls.__link(inst, p)
        return inst
    #-def

    @classmethod
    def __link(cls, destobj, srcpath):
        """__link(destobj, srcpath)

        Helper static method for inheriting subobjects from srcpath.
        """

        parts = srcpath.split('.')
        root = cls.collections.get(parts[0], None)
        for sibname in parts[1:]:
            if root is None:
                break
            root = root.siblings.get(sibname, None)
        if root is None:
            return
        for k in root.siblings.keys():
            destobj.siblings[k] = root.siblings[k]
    #-def

    def __init__(self, *args):
        """Collection(...) -> instance of Collection

        Constructor.
        """

        pass
    #-def

    def __getattr__(self, value):
        """__getattr__(value) -> object

        Overloaded getter to satisfy the behaviour in the example of use of the
        Collection class.
        """

        if not value[0].isupper():
            return object.__getattribute__(self, value)
        inst = self.siblings.get(value, None)
        if inst is not None:
            return inst
        self.siblings[value] = inst = Collection()
        setattr(inst, 'name', value)
        setattr(inst, 'qname', "%s.%s" % (self.qname, value))
        return inst
    #-def

    def __contains__(self, item):
        """__contains__(item) -> bool

        x.__contains__(y) <==> y in x

        Return True if x is y or if y is subitem of x.
        Examples:
        >>> A in A
        True
        >>> A.B in A.B
        True
        >>> A.C in A.B
        False
        >>> A in A.B
        False
        >>> A.B in A
        True
        >>> A.B.C.D in A.B
        True
        """

        return self is item or item.qname.startswith("%s." % self.qname)
    #-def

    @classmethod
    def lock(cls):
        """lock()

        Forbids adding new elements.
        """

        cls.__locked = True
    #-def

    @classmethod
    def unlock(cls):
        """unlock()

        Permits adding new elements.
        """

        cls.__locked = False
    #-def
#-class
