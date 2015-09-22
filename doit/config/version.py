#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/config/version.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-08-27 19:03:32 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! version constants.\
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

from doit.support.errors import doit_assert

_assert = doit_assert

class Version(object):
    """Implements the version holder.

    Member variables:

    * `major` (:class:`int`) -- major version number
    * `minor` (:class:`int`) -- minor version number
    * `patchlevel` (:class:`int`) -- patch level
    * `date` (:class:`int`) -- date as ``10000*year + 100*month + day``
    * `info` (:class:`str`) -- additional informations
    """
    __slots__ = [ 'major', 'minor', 'patchlevel', 'date', 'info' ]

    def __init__(
        self, major = 0, minor = 0, patchlevel = 0, date = 0, info = ""
    ):
        """Initializes the version.

        :param int major: A major version number.
        :param int minor: A minor version number.
        :param int patchlevel: A patch level.
        :param int date: A date (``10000*year + 100*month + day``).
        :param str info: An additional informations.
        """

        self.major = major
        self.minor = minor
        self.patchlevel = patchlevel
        self.date = date
        self.info = info
    #-def

    def __eq__(self, rhs):
        """Implements the ``self == rhs`` test.

        :param rhs: A right-hand side.
        :type rhs: :class:`Version <doit.config.version.Version>`

        :returns: :obj:`True` if ``self == rhs`` (:class:`bool`).

        :raises ~doit.support.errors.DoItAssertionError: If the `rhs` is not \
            consistent with this version.
        """

        return self.__compare(rhs) == 0
    #-def

    def __ne__(self, rhs):
        """Implements the ``self != rhs`` test.

        :param rhs: A right-hand side.
        :type rhs: :class:`Version <doit.config.version.Version>`

        :returns: :obj:`True` if ``self != rhs`` (:class:`bool`).

        :raises ~doit.support.errors.DoItAssertionError: If the `rhs` is not \
            consistent with this version.
        """

        return self.__compare(rhs) != 0
    #-def

    def __lt__(self, rhs):
        """Implements the ``self < rhs`` test.

        :param rhs: A right-hand side.
        :type rhs: :class:`Version <doit.config.version.Version>`

        :returns: :obj:`True` if ``self < rhs`` (:class:`bool`).

        :raises ~doit.support.errors.DoItAssertionError: If the `rhs` is not \
            consistent with this version.
        """

        return self.__compare(rhs) < 0
    #-def

    def __gt__(self, rhs):
        """Implements the ``self > rhs`` test.

        :param rhs: A right-hand side.
        :type rhs: :class:`Version <doit.config.version.Version>`

        :returns: :obj:`True` if ``self > rhs`` (:class:`bool`).

        :raises ~doit.support.errors.DoItAssertionError: If the `rhs` is not \
            consistent with this version.
        """

        return self.__compare(rhs) > 0
    #-def

    def __le__(self, rhs):
        """Implements the ``self <= rhs`` test.

        :param rhs: A right-hand side.
        :type rhs: :class:`Version <doit.config.version.Version>`

        :returns: :obj:`True` if ``self <= rhs`` (:class:`bool`).

        :raises ~doit.support.errors.DoItAssertionError: If the `rhs` is not \
            consistent with this version.
        """

        return self.__compare(rhs) <= 0
    #-def

    def __ge__(self, rhs):
        """Implements the ``self >= rhs`` test.

        :param rhs: A right-hand side.
        :type rhs: :class:`Version <doit.config.version.Version>`

        :returns: :obj:`True` if ``self >= rhs`` (:class:`bool`).

        :raises ~doit.support.errors.DoItAssertionError: If the `rhs` is not \
            consistent with this version.
        """

        return self.__compare(rhs) >= 0
    #-def

    def __compare(self, rhs):
        """Compares this version with `rhs`.

        :param rhs: A right-hand side.
        :type rhs: :class:`Version <doit.config.version.Version>`

        :returns: The result of comparison (:class:`int`).

        :raises ~doit.support.errors.DoItAssertionError: If the `rhs` is not \
            consistent with this version.
        """

        if rhs is self:
            return 0
        d = self.date - rhs.date
        ignore_date = self.date < 0 or rhs.date < 0
        x = self.major - rhs.major
        if x == 0:
            x = self.minor - rhs.minor
        if x == 0:
            x = self.patchlevel - rhs.patchlevel
        _assert(ignore_date or x == d or x*d > 0, "Inconsistent version")
        return x
    #-def

    def __str__(self):
        """Implements the conversion to :class:`str`.

        :returns: The ``"{major}.{minor}.{patchlevel}"`` string (:class:`str`).
        """

        return "%d.%d.%d" % (self.major, self.minor, self.patchlevel)
    #-def

    def __repr__(self):
        """Gets the representation of :class:`Version \
        <doit.config.version.Version>` object.

        :returns: This object text representation (:class:`str`).
        """

        return "Version(" \
            "major = %d, minor = %d, patchlevel = %d, date = %d, info = %s" \
        ")" % (
            self.major, self.minor, self.patchlevel, self.date, repr(self.info)
        )
    #-def
#-class

UNUSED_VERSION = None
NULL_VERSION = Version(0, 0, 0, 0, "")

DOIT_VERSION = Version(0, 0, 0, 20140101, "Development")
