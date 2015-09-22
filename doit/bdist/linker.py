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

class LinkableBase(object):
    """Linkable base class.
    """
    __slots__ = [
        'arch', 'arch_version',
        'platform', 'platform_version',
        'flags', 'timedate',
        'sections'
    ]

    def __init__(self):
        """Initializes the linkable base.

        Member variables:

        * `arch` (:class:`str`) -- architecture identifier
        * `arch_version` (:class:`tuple`) -- architecture version
        * `platform` (:class:`str`) -- platform identifier
        * `platform_version` (:class:`tuple`) -- platform version
        * `flags` (:class:`int`) -- additional informations
        * `timedate` (:class:`int`) -- time date stamp (in seconds)
        * `sections` (:class:`dict`) -- sections with data
        """

        self.arch = ''
        self.arch_version = ()
        self.platform = ''
        self.platform_version = ()
        self.flags = 0
        self.timedate = -1
        self.sections = {}
    #-def
#-class

class LinkableObject(LinkableBase):
    """Base class for linkable objects.

    Member variables:

    * `linkable_version` (:class:`tuple`) -- the version of linkable object
    * `linker_name` (:class:`str`) -- the name of the linker or assembler
    * `linker_version` (:class:`tuple`) -- the version of the linker or \
        assembler
    """
    __slots__ = [ 'linkable_version', 'linker_name', 'linker_version' ]

    def __init__(self):
        """Initializes the linkable object.
        """

        LinkableBase.__init__(self)
        self.linkable_version = ()
        self.linker_name = ''
        self.linker_version = ()
    #-def
#-class

class Executable(LinkableBase):
    """Base class for executable objects.

    Member variables:

    * `executable_version` (:class:`tuple`) -- the version of executable \
        object (not the executable code)
    * `entry_point` (:class:`int`) -- where the executable code begins
    * `code_section_idx` (:class:`str`) -- where the section with executable \
        code is located (in `sections`)
    """
    __slots__ = [ 'executable_version', 'entry_point', 'code_section_idx' ]

    def __init__(self):
        """Initializes the executable object.
        """

        LinkableBase.__init__(self)
        self.executable_version = ()
        self.entry_point = -1
        self.code_section_idx = ''
    #-def
#-class

class Linker(object):
    """Base class for linkers.
    """
    __slots__ = []

    def __init__(self):
        """Initializes the linker.
        """

        pass
    #-def
#-class
