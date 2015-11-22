#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/bdist/linker.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-08-25 12:52:28 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! general linker interfaces.\
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

import time
import collections

from doit.config.version import UNUSED_VERSION

class Section(collections.OrderedDict):
    """
    """
    __slots__ = [ 'name' ]

    def __init__(self, name):
        """
        """

        collections.OrderedDict.__init__(self)
        self.name = name
    #-def
#-class

class LinkableBase(object):
    """Linkable base class.
    """
    version = UNUSED_VERSION
    __slots__ = [ '__name', '__timedate', '__sections' ]

    def __init__(self, name, content_source, timedate = -1):
        """Initializes the linkable base.
        """

        self.__name = name
        self.__timedate = timedate
        self.__sections = collections.OrderedDict()
        self.make_sections(self.__sections, content_source)
    #-def

    def make_sections(self, dest, src):
        """
        """

        pass
    #-def

    def timestamp(self, now = -1):
        """
        """

        if self.__timedate < 0:
            self.__timedate = \
                int(time.mktime(time.gmtime())) if now < 0 else now
    #-def

    def name(self):
        """
        """

        return self.__name
    #-def

    def timedate(self):
        """
        """

        return self.__timedate
    #-def

    def get_section(self, name):
        """
        """

        return self.__sections[name]
    #-def

    def each_section(self, f):
        """
        """

        for k in self.__sections:
            f(k, self.__sections[k])
    #-def
#-class

class AssembledObject(LinkableBase):
    """
    """
    __slots__ = []

    def __init__(self, name, asm):
        """
        """

        LinkableBase.__init__(self, name, asm)
    #-def
#-class

class LinkableObject(LinkableBase):
    """Base class for linkable objects.
    """
    __slots__ = []

    def __init__(self, object):
        """Initializes the linkable object.
        """

        LinkableBase.__init__(self, object.name(), object)
    #-def
#-class

class Executable(LinkableObject):
    """Base class for executable objects.
    """
    __slots__ = []

    def __init__(self, name, objects, options, version):
        """Initializes the executable object.
        """

        LinkableObject.__init__(self, name, (objects, options), version)
    #-def
#-class
