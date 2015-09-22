#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/bdist/doit_linker.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-08-25 19:46:22 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! linker.\
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

from doit.support.errors import DoItLinkerError, doit_assert
from doit.asm.doit_asm import SECTION_INFO, DoItAssembler
from doit.bdist.linker import LinkableObject

_assert = lambda cond, emsg: doit_assert(cond, emsg, DoItLinkerError)

class DoItLinkable(LinkableObject):
    """`DoIt!` linkable object.
    """
    __slots__ = []

    def __init__(self, assembler):
        """Initializes the `DoIt!` linkable object from the `DoIt!` assembler.

        :param assembler: A `DoIt!` assembler.
        :type assembler: :class:`DoItAssembler \
            <doit.asm.doit_asm.DoItAssembler>`

        :raises ~doit.support.errors.DoItLinkerError: If the extraction of \
            informations from `assembler` fails.
        """

        LinkableObject.__init__(self)
        _assert(
            isinstance(assembler, DoItAssembler),
            "The assembler must be the DoIt! assember"
        )
        sections, name2pos = assembler.sections()
        _assert(len(sections) > 0, "There are no sections")
        _assert(
            SECTION_INFO in name2pos,
            "`%s` section was expected" % SECTION_INFO
        )
        info = sections[name2pos[SECTION_INFO]]
        self.arch = info[ARCH_FIELD]
        self.arch_version = info[ARCH_VERSION_FIELD]
        self.platform = info[PLATFORM_FIELD]
        self.platform_version = info[PLATFORM_VERSION_FIELD]
        self.flags = ASSEMBLED_OBJECT
        self.timedate = info[TIMEDATE_FIELD]
        self.linkable_version = VERSION
        self.linker_name = info[ASSEMBLER_FIELD]
        self.linker_version = info[VERSION_FIELD]

        for sec in sections:
            name = sec[NAME_FIELD]
            _assert(
                name in DoItAssembler.sections,
                "Section `%s` is not supported" % name
            )
            if name != SECTION_INFO:
                _assert(
                    name not in self.sections, "Duplicit section `%s`" % name
                )
                self.sections[name] = sec
            #-if
        #-for
    #-def
#-class

class DoItExecutable(Executable):
    """`DoIt!` executable object.
    """
    sections = (SECTION_TEXT, SECTION_DATA, SECTION_STACK)
    __slots__ = []

    def __init__(self):
        """Initializes the `DoIt!` executable object.
        """

        Executable.__init__(self)
        self.entry_point = 0
        self.stack_size = 0
        self.code = []
        self.data = []
    #-def
#-class

class DoItLinker(Linker):
    """`DoIt!` linker.
    """
    __slots__ = []

    def __init__(self, *objects, **arguments):
        """Initializes the linker.
        """

        Linker.__init__(self)
        self.__objects = objects
        self.__setopts(arguments)
    #-def

    def run(self, *objects, **arguments):
        """
        """

        return executable
    #-def

    def __setopts(self, arguments):
        """
        """

        self.__opts[STACK_SIZE_OPTION] = arguments.get(STACK_SIZE_OPTION, 512)
    #-def
#-class
