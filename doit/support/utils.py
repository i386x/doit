#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/utils.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-02-27 18:26:58 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
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
    """Convert a system path to DoIt! universal path.

    :param str p: System path.

    :returns: DoIt! universal path (:class:`str`).

    DoIt! universal path is a UNIX-like relative path. It is recomended the
    system path `p` to be also relative.
    """

    d = os.path.dirname(p)
    b = os.path.basename(p)
    if d == '':
        return b
    d = d.replace(os.sep, '/').replace(os.pardir, '..').replace(os.curdir, '.')
    return "%s/%s" % (d, b)
#-def

def path2sys(p):
    """Convert a DoIt! universal path to system path.

    :param str p: DoIt! universal path.

    :returns: System path (:class:`str`).

    DoIt! universal path is a UNIX-like relative path.
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
        """Initializes the handler.
        """

        self.etype = None
        self.evalue = None
        self.etraceback = None
    #-def

    def __enter__(self):
        """Called when entering to with-statement.

        :returns: This object (:class:`WithStatementExceptionHandler \
            <doit.support.utils.WithStatementExceptionHandler>`).
        """

        return self
    #-def

    def __exit__(self, etype, evalue, etraceback):
        """Called when exiting from with-statement.

        :param type etype: Exception type.
        :param Exception evalue: Exception value.
        :param traceback etraceback: Traceback.

        :returns: :obj:`True` to suppress the caught exception.
        """

        self.etype = etype
        self.evalue = evalue
        self.etraceback = etraceback
        return True
    #-def
#-class

def doit_read(fpath):
    """Read the text file encoded in UTF-8.

    :param str fpath: DoIt! path to the location of file.

    :returns: Content of file at `fpath` (:class:`str`).

    In case of error, :obj:`None` is returned.
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
    """A factory for making unique objects. Each object has attribute `name`
    with its name and `qname` with its qualified name (complete path).

    Example of use::

        # Create an anonymous object:
        a = Collection()

        # Create new object named 'ItemA':
        ItemA = Collection("ItemA")

        # Create a subobject named 'SubItem1':
        SubItem1 = ItemA.SubItem1

        # This is true now:
        SubItem1.name == "SubItem1"
        SubItem1.qname == "ItemA.SubItem1"

        # Create new object 'ItemB' and inherits subobjects from 'ItemA':
        ItemB = Collection("ItemB", "ItemA")

        # This is now also true:
        SubItem1 is ItemB.SubItem1
    """
    __slots__ = [ 'name', 'qname', 'siblings' ]
    collections = {}
    __locked = False

    def __new__(cls, *args):
        """Creates a new or return existing unique object (instance of
        :class:`Collection <doit.support.utils.Collection>`).

        :returns: Unique object (:class:`Collection \
            <doit.support.utils.Collection>`).

        :raises AssertionError: When :class:`Collection \
            <doit.support.utils.Collection>` is locked (see :meth:`lock() \
            <doit.support.utils.Collection.lock>`).

        Called with no argument, creates an anonymous instance of
        :class:`Collection <doit.support.utils.Collection>`. Otherwise, the
        first argument is the name of the new instance, and the rest of
        arguments are names of instances to be inherited. Note that the
        existing object is returned instead of creating a new one with the same
        name.
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
        """Helper class method for inheriting subobjects from `srcpath`.
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
        """Initializes the unique object.
        """

        pass
    #-def

    def __getattr__(self, value):
        """Return a unique object with name `value` and qualified name
        ``self.qname + '.' + value``.

        :param str value: Unique object name.

        :returns: Unique object (:class:`Collection \
            <doit.support.utils.Collection>`).
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
        """Tests the `item` ownership.

        :param item: Item to be tested.
        :type item: :class:`Collection <doit.support.utils.Collection>`

        :returns: :obj:`True` if `item` is in this object scope \
            (:class:`bool`).

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
        """Forbids the adding of new elements.
        """

        cls.__locked = True
    #-def

    @classmethod
    def unlock(cls):
        """Permits the adding of new elements.
        """

        cls.__locked = False
    #-def
#-class
