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
from doit.asm.doit_asm import SECTION_INFO, SECTION_TEXT, SECTION_DATA, \
                                SECTION_SYMBOLS, \
                              InfoSection, DoItAssembler
from doit.bdist.linker import AssembledObject, LinkableObject

_assert = lambda cond, emsg: doit_assert(cond, emsg, DoItLinkerError)

class SectionInfo(Section):
    """
    """
    required_fields = sARCH, sARCH_VERSION, sASM, sASM_VERSION
    __slots__ = []

    def __init__(self, sections):
        """
        """

        Section.__init__(self, sINFO)
        _assert(isinstance(sections, DoItSections),
            "Not a DoIt! assembler sections"
        )
        _assert(sINFO in sections, "\"%s\" section is required" % sINFO)
        info = sections[sINFO]
        _assert(isinstance(info, InfoSection),
            "Not a DoIt! assembler \"%s\" section" % sINFO
        )
        _assert(sARCH in info, "Architecture information is missing")
        _assert(info[sARCH] == MACHINE_DOIT, "Architecture must be DoIt! VM")
        _assert(sARCH_VERSION in info, "Architecture version is missing")
        _assert(
            info[sARCH_VERSION] is UNUSED_VERSION \
            or isinstance(info[sARCH_VERSION], Version),
            "Not a version"
        )
        _assert(sASM in info, "Assembler name is missing")
        _assert(info[sASM] == DoItAssembler.__name__,
            "Assembler must be DoIt! assembler"
        )
        _assert(sASM_VERSION in info, "Assembler version is missing")
        _assert(
            info[sASM_VERSION] is UNUSED_VERSION \
            or isinstance(info[sASM_VERSION], Version),
            "Not a version"
        )
        for f in self.__class__.required_fields:
            self[f] = info[f]
    #-def
#-class

class SectionTextData(Section):
    """
    """
    required_fields = sORG, sALIGN
    __slots__ = [ 'data' ]

    def __init__(self, sections, name):
        """
        """

        Section.__init__(self, name)
        self.data = []
        _assert(isinstance(sections, DoItSections),
            "Not a DoIt! assembler sections"
        )
        _assert(name in (sTEXT, sDATA), "Invalid section name")
        _assert(name in sections, "\"%s\" section is required" % name)
        s = sections[name]
        _assert(isinstance(s, TextOrDataSection),
            "Not a DoIt! assembler \"%s\" or \"%s\" section" % (sTEXT, sDATA)
        )
        p = s.properties()
        _assert(sORG in p, "Origin information expected")
        _assert(isinstance(p[sORG], int) and p[sORG] >= 0,
            "Origin must be a non-negative integer"
        )
        _assert(sALIGN in p, "Section alignment information expected")
        _assert(
            isinstance(p[sALIGN], int) and p[sALIGN] > 0 \
            and (p[sALIGN] - 1) & p[sALIGN] == 0,
            "Section alignment must be positive power of two integer"
        )
        for f in self.__class__.required_fields:
            self[f] = p[f]
        for i in s.data():
            _assert(isinstance(i, DoItInstruction), "No a DoIt! instruction")
            self.data.append(i)
    #-def
#-class

class SectionSymbols(Section):
    """
    """
    __slots__ = []

    def __init__(self, sections):
        """
        """

        Section.__init__(self, sSYMBOLS)
        _assert(isinstance(sections, DoItSections),
            "Not a DoIt! assembler sections"
        )
        _assert(sSYMBOLS in sections, "\"%s\" section is required" % sSYMBOLS)
        symbols = sections[sSYMBOLS]
        _assert(isinstance(symbols, SymbolsSection),
            "Not a DoIt! assembler \"%s\" section" % sSYMBOLS
        )
        for s in symbols.properties():
            self[s] = symbols[s]
    #-def
#-class

class DoItAssembledObject(AssembledObject):
    """
    """
    version = Version(0, 0, 0, 0, "")
    __slots__ = []

    def __init__(self, name, asm):
        """
        """

        AssembledObject.__init__(self, name, asm)
    #-def

    def make_sections(self, sections, asm):
        """
        """

        _assert(isinstance(asm, DoItAssembler), "Not a DoIt! assembler")

        asm_sections = asm.sections().sections()
        _assert(isinstance(asm_sections, DoItSections),
            "Not a DoIt! assembler sections"
        )

        if len(asm_sections) == 0:
            self.timestamp()
            return
        self[sINFO] = SectionInfo(asm_sections)
        if sTEXT in asm_sections:
            self[sTEXT] = SectionTextData(asm_sections, sTEXT)
        if sDATA in asm_sections:
            self[sDATA] = SectionTextData(asm_sections, sDATA)
        if sSYMBOLS in asm_sections:
            self[sSYMBOLS] = SectionSymbols(asm_sections)

        self.timestamp(asm_sections[sINFO].get(sTIMEDATE, -1))
    #-def
#-class

class FromAssembledObject(object):
    """
    """
    __slots__ = []

    def __init__(self, lobj, lobjsecs):
        """
        """

        self.__lobject = lobject
        self.__lsections = lsections
        self.__relocs = collections.OrderedDict()
    #-def

    def __call__(self, name, section):
        """
        """

        if name in (sINFO, sTEXT, sDATA):
            self.__lsections[name] = section.clone()
        if name == sSYMBOLS:
            self.__relocs = section.clone()
    #-def

    def postprocess(self):
        """
        """

        if not self.__relocs:
            self.__relocs = 
            self.__finalize()
            return
        on_undefined_symbol = OnUndefinedSymbol(self)
        for sec in self.__lsections:
            if sec in (sTEXT, sDATA):
                for ins in self.__lsection[name].data:
                    ins.update(self.__relocs, on_undefined_symbol)
        self.__finalize(on_undefined_symbol.undefined_symbols)
    #-def
#-class

class DoItLinkableObject(LinkableObject):
    """
    """

    def __init__(self, object):
        """
        """

        LinkableObject.__init__(self, object)
    #-def

    def make_sections(self, sections, object):
        """
        """

        if isinstance(object, DoItAssembledObject):
            f = FromAssembledObject(self, sections)
            object.each_section(f)
            f.postprocess()
    #-def

    def __from_assembled_object(self, sections, object):
        """
        """

        # .info, .text, .data, .relocs, .extern
        object.each_section(SectionVisitor(self, sections))
#-class

# -----------------------------------------------------------------------------
# -- Cut off:

class DoItLinkable(LinkableObject):
    """`DoIt!` linkable object.
    """
    version = DOIT_VERSION
    __slots__ = []

    def __init__(self, name, assembler):
        """Initializes the `DoIt!` linkable object from the `DoIt!` assembler.

        :param assembler: A `DoIt!` assembler.
        :type assembler: :class:`DoItAssembler \
            <doit.asm.doit_asm.DoItAssembler>`

        :raises ~doit.support.errors.DoItLinkerError: If the extraction of \
            informations from `assembler` fails.
        """

        LinkableObject.__init__(self)
        self.name = name
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
        self.arch = info[InfoSection.ARCH_FIELD]
        self.arch_version = info[InfoSection.ARCH_VERSION_FIELD]
        self.machine = info[InfoSection.MACHINE_FIELD]
        self.machine_version = info[InfoSection.MACHINE_VERSION_FIELD]
        self.platform = info[InfoSection.PLATFORM_FIELD]
        self.platform_version = info[InfoSection.PLATFORM_VERSION_FIELD]
        self.flags = ASSEMBLED_OBJECT
        self.timedate = info[InfoSection.TIMEDATE_FIELD]
        self.linkable_version = self.__class__.version
        self.linker_name = info[InfoSection.ASSEMBLER_FIELD]
        self.linker_version = info[InfoSection.VERSION_FIELD]

        self.sections = {}
        for sec in sections:
            name = sec.name()
            _assert(
                name in DoItAssembler.supported_sections,
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
    TASK_OPTION = 'task'
    TASK_PREPROCESS = 'preprocess'
    STACK_SIZE_OPTION = 'stack_size'
    __slots__ = []

    def __init__(self):
        """Initializes the linker.
        """

        Linker.__init__(self)
        self.__opts = {}
    #-def

    def link(self, *objects, **arguments):
        """
        """

        C = self.__class__
        O = self.__opts

        self.__setopts(arguments)
        if O[C.TASK_OPTION] == C.TASK_PREPROCESS:
            result = []
            for obj in objects:
                result.append(self.__preprocess(object))
            return result
        return executable
    #-def

    def __merge_sections(self):
        """
        """

        sections = {
          SECTION_TEXT: [],
          SECTION_DATA: [],
          SECTION_SYMBOLS: {}
        }
        bases = {
          SECTION_TEXT: 0,
          SECTION_DATA: 0
        }
        for obj in objects:
            self.__verify_object(obj)
            if SECTION_TEXT in object.sections:
                text.extend(object.sections[SECTION_TEXT].data())
            if SECTION_DATA in object.sections:
                data.extend(object.sections[SECTION_DATA].data())
            if SECTION_SYMBOLS in object.sections:
                symbols_section = object.sections[SECTION_SYMBOLS].data()
                for symbol in symbols_section:
                    section_name, location = symbols_section[symbol]
                    if section_name == SECTION_TEXT:
                        location += text_base
                    elif section_name == SECTION_DATA:
                        location += data_base
                    else:
                        _fail()
                    symbols[symbol] = ()

            for sec in object.sections:
                if sec.name() not in sections:
                    sections[sec.name()] = []
    #-def

    def __setopts(self, arguments):
        """
        """

        self.__opts.clear()
        self.__opts[TASK_OPTION] = arguments.get(TASK_OPTION, TASK_PREPROCESS)
        self.__opts[STACK_SIZE_OPTION] = arguments.get(STACK_SIZE_OPTION, 512)
    #-def
#-class
