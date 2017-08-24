#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/utils.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-02-27 18:26:58 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! utilities.\
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

import time

from doit.support.errors import doit_assert

_assert = doit_assert

def ordinal_suffix(n):
    """Returns a suffix (`st`, `nd`, ...) of the given ordinal number (1, 2,
    ...).

    :param int n: Ordinal number.

    :returns: Suffix (:class:`str`) that corresponds to `n`.
    """

    n = abs(n)
    return (
        "st" if (n % 10) == 1 and (n % 100) != 11 else \
        "nd" if (n % 10) == 2 and (n % 100) != 12 else \
        "rd" if (n % 10) == 3 and (n % 100) != 13 else \
        "th"
    )
#-def

def deep_eq(x, y):
    """Deeply compares `x` and `y` for equality.

    :param object x: First object.
    :param object y: Second object.

    :returns: :obj:`True` if `x` is equal to `y`, :obj:`False` otherwise \
        (:class:`bool`).
    """

    if x is y:
        return True
    if isinstance(x, (tuple, list)) and isinstance(y, (tuple, list)):
        if len(x) != len(y):
            return False
        i = 0
        while i < len(x):
            if not deep_eq(x[i], y[i]):
                return False
            i += 1
        return True
    if isinstance(x, dict) and isinstance(y, dict):
        if len(x) != len(y):
            return False
        for k in x:
            if k not in y:
                return False
            if not deep_eq(x[k], y[k]):
                return False
        return True
    return x == y
#-def

def timestamp():
    """Returns a dictionary filled with local time items.

    :returns: Local time items (:class:`dict`).

    When called, it records the actual value of local time and fills a
    :class:`dict` with these items:

    * `year` -- year (:class:`int`)
    * `month` -- month (1 to 12, :class:`int`)
    * `day` -- day (1 to 31, :class:`int`)
    * `hour` -- hour (0 to 23, :class:`int`)
    * `min` -- minute (0 to 59, :class:`int`)
    * `sec` -- second (0 to 59, :class:`int`)
    * `utcsign` -- `+` means east from Greenwich, `-` means west form Greenwich
                   (:class:`str`)
    * `utchour` -- absolute value of UTC offset (hour part, :class:`int`)
    * `utcmin` -- absolute value of UTC offset (minute part, :class:`int`)
    * `utcsec` -- absolute value of UTC offset (second part, :class:`int`)
    * `dsthour` -- DST shift value (hour part, :class:`int`)
    * `dstmin` -- DST shift value (minute part, :class:`int`)
    * `dstsec` -- DST shift value (second part, :class:`int`)
    """

    hour = (lambda x: x // 3600)
    minute = (lambda x: x // 60 - hour(x) * 60)
    second = (lambda x: x - hour(x) * 3600 - minute(x) * 60)

    ts = time.localtime()
    stamp = {}
    stamp['year'] = ts.tm_year
    stamp['month'] = ts.tm_mon
    stamp['day'] = ts.tm_mday
    stamp['hour'] = ts.tm_hour
    stamp['min'] = ts.tm_min
    stamp['sec'] = ts.tm_sec
    utcoffs = -time.timezone
    dstoffs = 3600 if ts.tm_isdst > 0 else 0
    stamp['utcsign'] = '-' if utcoffs < 0 else '+'
    utcoffs = abs(utcoffs)
    stamp['utchour'] = hour(utcoffs)
    stamp['utcmin'] = minute(utcoffs)
    stamp['utcsec'] = second(utcoffs)
    stamp['dsthour'] = hour(dstoffs)
    stamp['dstmin'] = minute(dstoffs)
    stamp['dstsec'] = second(dstoffs)
    return stamp
#-def

class Functor(object):
    """Base class for implementing function objects.

    :ivar args: List of arguments.
    :vartype args: tuple
    :ivar kwargs: Key-value arguments.
    :vartype kwargs: dict
    """
    __slots__ = [ 'args', 'kwargs' ]

    def __init__(self, *args, **kwargs):
        """Initialize the function object.

        :param tuple args: List of arguments.
        :param dict kwargs: Key-value arguments.
        """

        self.args = args
        self.kwargs = kwargs
    #-def

    def __eq__(self, other):
        """Implements ``self == other``.

        :param object other: Right-hand side argument of ``==``.

        :returns: :obj:`True` if this instance is equal to `other` \
            (:class:`bool`).
        """

        if not isinstance(other, self.__class__):
            return False
        if not deep_eq(self.args, other.args):
            return False
        if not deep_eq(self.kwargs, other.kwargs):
            return False
        return True
    #-def

    def __ne__(self, other):
        """Implements ``self != other``.

        :param object other: Right-hand side argument of ``!=``.

        :returns: :obj:`True` if this instance is not equal to `other` \
            (:class:`bool`).
        """

        return not self.__eq__(other)
    #-def

    def __call__(self):
        """Implements ``self()``. To be redefined by user.
        """

        pass
    #-def
#-class

class WithStatementExceptionHandler(object):
    """Implements exception handler which catch any exception raised inside
    with-statement.

    :ivar etype: Exception type.
    :vartype etype: type
    :ivar evalue: Exception value.
    :vartype evalue: Exception
    :ivar etraceback: Traceback object.
    :vartype etraceback: :class:`traceback`
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

        :param type etype: An exception type.
        :param Exception evalue: An exception value.
        :param etraceback: A traceback object.
        :type etraceback: :class:`traceback`

        :returns: :obj:`True` to suppress the caught exception.
        """

        self.etype = etype
        self.evalue = evalue
        self.etraceback = etraceback
        return True
    #-def
#-class

#
# Based on Pygments _TokenType from pygments-main/pygments/token.py
# (http://pygments.org/)
# 
class Collection(object):
    """A factory for making unique objects. Each object has attribute `name`
    with its name and `qname` with its qualified name (complete path).

    :ivar str name: Unique object name.
    :ivar str qname: Unique object full name.
    """
    __collections = {}
    __locked = False
    __slots__ = [ 'name', 'qname', 'siblings_', '__x' ]

    def __new__(cls, *args):
        """Creates a new or returns existing unique object (instance of
        :class:`Collection <doit.support.utils.Collection>`).

        :param tuple args: See below.

        :returns: The unique object (:class:`Collection \
            <doit.support.utils.Collection>`).

        :raises ~doit.support.errors.DoItAssertionError: When \
            :class:`Collection <doit.support.utils.Collection>` is locked \
            (see :meth:`lock() <doit.support.utils.Collection.lock>`).

        Called with no argument, creates an anonymous instance of
        :class:`Collection <doit.support.utils.Collection>`. Otherwise, the
        first argument is the name of the new instance, and the rest of
        arguments are names of instances to be inherited. Note that the
        existing object is returned instead of creating a new one with the same
        name.
        """

        _assert(not cls.__locked, "Collection is locked")
        if len(args) == 0:
            inst = object.__new__(cls)
            setattr(inst, 'name', repr(inst))
            setattr(inst, 'qname', repr(inst))
            setattr(inst, 'siblings_', {})
            return inst
        name = args[0]
        inst = cls.__collections.get(name, None)
        if inst is not None:
            return inst
        cls.__collections[name] = inst = object.__new__(cls)
        setattr(inst, 'name', name)
        setattr(inst, 'qname', name)
        setattr(inst, 'siblings_', {})
        for p in args[1:]:
            cls.__link(inst, p)
        return inst
    #-def

    @classmethod
    def __link(cls, destobj, srcpath):
        """Helper class method for inheriting subobjects from `srcpath`.

        :param destobj: A destination object.
        :type destobj: :class:`Collection <doit.support.utils.Collection>`
        :param str srcpath: A path to source object.
        """

        parts = srcpath.split('.')
        root = cls.__collections.get(parts[0], None)
        for sibname in parts[1:]:
            if root is None:
                break
            root = root.siblings_.get(sibname, None)
        if root is None:
            return
        for k in root.siblings_.keys():
            destobj.siblings_[k] = root.siblings_[k]
    #-def

    def __init__(self, *args):
        """Initializes the unique object.

        :param tuple args: See :meth:`__new__(*args) \
            <doit.support.utils.Collection.__new__>`.
        """

        pass
    #-def

    def __getattr__(self, value):
        """Returns the unique object with name `value` and qualified name
        ``self.qname + '.' + value``.

        :param str value: The unique object name.

        :returns: The unique object (:class:`Collection \
            <doit.support.utils.Collection>`).
        """

        if not value[0].isupper():
            return object.__getattribute__(self, value)
        inst = self.siblings_.get(value, None)
        if inst is not None:
            return inst
        self.siblings_[value] = inst = Collection()
        setattr(inst, 'name', value)
        setattr(inst, 'qname', "%s.%s" % (self.qname, value))
        return inst
    #-def

    def __contains__(self, item):
        """Tests the `item` ownership.

        :param item: An item to be tested.
        :type item: :class:`Collection <doit.support.utils.Collection>`

        :returns: :obj:`True` if `item` is in this object scope \
            (:class:`bool`).
        """

        return self is item or repr(item).startswith("%s." % repr(self))
    #-def

    def __repr__(self):
        """Implements the ``repr`` operator.

        :returns: The qualified name of this unique object or, if this object \
            was created as anonymous, its default representation \
            (:class:`str`).
        """

        if hasattr(self, 'qname'):
            return self.qname
        return object.__repr__(self)
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
