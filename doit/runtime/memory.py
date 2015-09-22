#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/runtime/memory.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-04-14 20:16:23 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! VM memory.\
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

from doit.support.errors import DoItMemoryAccessError, doit_assert

_assert = doit_assert
_massert = lambda cond, emsg: doit_assert(cond, emsg, DoItMemoryAccessError, 2)

class Pointer(object):
    """Data structure which keeps the memory location as a pair of segment
    (:class:`Memory <doit.runtime.memory.Memory>`) and offset (:class:`int`).

    Example of use::

        # Obtaining a pointer:
        p = Pointer(mem)
        pp = mem + 0 # Same effect
        ppp = Pointer(p, 1)

        # Pointer arithmetic:
        j = p + 2
        i = j - 4
        p += 3
        i -= 2
        j - i  # j and i must be from the same segment

        # Access to kept location:
        x = p[0]
        y = j[-1]
        i[2] = j[3]
        p[1] = 2
    """
    __slots__ = [ '__segment', '__offset' ]

    def __init__(self, segment, offset = 0):
        """Initializes the pointer.

        :param segment: A segment or a pointer.
        :type segment: :class:`Memory <doit.runtime.memory.Memory>` or \
            :class:`Pointer <doit.runtime.memory.Pointer>`
        :param int offset: An offset (optional; the default value is 0).

        If `segment` is pointer, the segment part of new pointer will be
        ``segment.segment()`` and the offset part will be
        ``offset + segment.offset()``.
        """

        if isinstance(segment, self.__class__):
            # segment is pointer:
            offset += segment.offset()
            segment = segment.segment()
        # segment is memory:
        self.__segment = segment
        self.__offset = offset
    #-def

    def segment(self):
        """Returns the segment part of pointer.

        :returns: The segment (:class:`Memory <doit.runtime.memory.Memory>`).
        """

        return self.__segment
    #-def

    def offset(self):
        """Returns the offset part of pointer.

        :returns: The offset (:class:`int`).
        """

        return self.__offset
    #-def

    def read(self):
        """Reads the data the pointer refers to.

        :returns: The data stored at the referred location (:class:`object`).

        :raises ~doit.support.errors.DoItMemoryAccessError: If the location \
            is invalid.
        """

        return self.__segment[self.__offset]
    #-def

    def write(self, data):
        """Writes the `data` to the location the pointer refers to.

        :param object data: A data to be written.

        :raises ~doit.support.errors.DoItMemoryAccessError: If the location \
            is invalid.
        """

        self.__segment[self.__offset] = data
    #-def

    def __add__(self, i):
        """Implements the ``pointer + i``. This is equivalent to
        ``Pointer(pointer.segment(), pointer.offset() + i)``.

        :param int i: A pointer offset increment.

        :returns: The new instance of :class:`Pointer \
            <doit.runtime.memory.Pointer>`.
        """

        return self.__class__(self.__segment, self.__offset + i)
    #-def

    def __iadd__(self, i):
        """Implements the ``pointer += i`` (adds `i` to pointer's offset).

        :param int i: A pointer offset increment.

        :returns: This object (:class:`Pointer <doit.runtime.memory.Pointer>`).
        """

        self.__offset += i
        return self
    #-def

    def __sub__(self, i):
        """Implements the ``pointer - i``. If `i` is :class:`int`, this is
        equivalent to ``Pointer(pointer.segment(), pointer.offset() - i)``. If
        `i` is :class:`Pointer <doit.runtime.memory.Pointer>` and has the same
        segment as ``pointer``, the result is the distance between ``pointer``
        and `i`.

        :param i: A pointer or a pointer offset decrement.
        :type i: :class:`Pointer <doit.runtime.memory.Pointer>` or :class:`int`

        :returns: The new instance of :class:`Pointer \
            <doit.runtime.memory.Pointer>` or the distance between two \
            pointers  (:class:`int`).

        :raises ~doit.support.errors.DoItAssertionError: If ``pointer`` and \
            `i` have different segments (in the case the `i` is \
            :class:`Pointer <doit.runtime.memory.Pointer>`).
        """

        if isinstance(i, self.__class__):
            _assert(
                self.__segment is i.segment(),
                "Pointers have different segments"
            )
            return self.__offset - i.offset()
        return self.__class__(self.__segment, self.__offset - i)
    #-def

    def __isub__(self, i):
        """Implements the ``pointer -= i`` (adds `-i` to pointer's offset).

        :param int i: A pointer offset decrement.

        :returns: This object (:class:`Pointer <doit.runtime.memory.Pointer>`).
        """

        self.__offset -= i
        return self
    #-def

    def __setitem__(self, i, v):
        """Implements ``pointer[i] = v`` (writes `v` to the location referred
        by ``pointer`` and adjusted by `i`).

        :param int i: A relative position to the pointer's referred location.
        :param object v: A data to be written.

        :raises ~doit.support.errors.DoItMemoryAccessError: If the target \
            location is invalid.
        """

        self.__segment[self.__offset + i] = v
    #-def

    def __getitem__(self, i):
        """Implements ``pointer[i]`` (reads data from the location referred by
        ``pointer`` and adjusted by `i`).

        :param int i: A relative position to the pointer's referred location.

        :returns: The data stored at the requested location (:class:`object`).

        :raises ~doit.support.errors.DoItMemoryAccessError: If the target \
            location is invalid.
        """

        return self.__segment[self.__offset + i]
    #-def
#-class

class Memory(list):
    """The memory abstraction base class. Instances of this class or the class
    derived from this class are used by `DoIt!` virtual machine as a storage
    for code or data.
    """
    __slots__ = [ '__memused' ]

    def __init__(self):
        """Initializes the memory.
        """

        list.__init__(self, [])
        self.__memused = 0
    #-def

    def sbrk(self, brk):
        """Set the upper bound of used memory.

        :param int brk: A new upper bound value ("break").

        :raises ~doit.support.errors.DoItAssertionError: If `brk` value is \
            invalid.
        """

        _assert(brk >= 0, "Invalid memory break value (%d)" % brk)
        if brk > len(self):
            list.extend(self, [None]*(brk - len(self)))
        self.__memused = brk
    #-def

    def __add__(self, i):
        """Implements ``mem + i``.

        :param int i: An index to the memory.

        :returns: :class:`Pointer <doit.runtime.memory.Pointer>` with segment \
            as this object and offset as `i`.
        """

        return Pointer(self, i)
    #-def

    def __setitem__(self, i, v):
        """Implements ``mem[i] = v`` (writes `v` to position `i` in the
        memory).

        :param int i: An index to the memory.
        :param object v: A data to be written.

        :raises ~doit.support.errors.DoItMemoryAccessError: If the index `i` \
            to the memory is invalid.
        """

        _massert(i >= 0 and i < self.__memused, "Memory write error at %d" % i)
        list.__setitem__(self, i, v)
    #-def

    def __getitem__(self, i):
        """Implements ``mem[i]`` (reads data from the memory location at `i`).

        :param int i: An index to the memory.

        :returns: The data stored at the location `i` in the memory \
            (:class:`object`).

        :raises ~doit.support.errors.DoItMemoryAccessError: If the index `i` \
            to the memory is invalid.
        """

        _massert(i >= 0 and i < self.__memused, "Memory read error at %d" % i)
        return list.__getitem__(self, i)
    #-def

    def stats(self):
        """Get the memory statistic.

        :returns: The pair of :class:`int` values, where the first is the \
            size of used memory and the second is the total memory size.
        """

        return self.__memused, len(self)
    #-def
#-class
