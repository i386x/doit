#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/config/config.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-09-05 22:23:14 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! configuration.\
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

import sys
import os
import platform
import re

from doit.config.version import Version, UNUSED_VERSION

# General constants:
ANY = '<any>'

# Environment specific constants:
PYTHON_CPYTHON = 'CPython'
PYTHON_IRON = 'IronPython'
PYTHON_JYTHON = 'Jython'
PYTHON_PYPY = 'PyPy'
ARCH_32 = '32bit'
ARCH_64 = '64bit'
MACHINE_x86 = 'x86'
MACHINE_x86_64 = 'x86_64'
MACHINE_DOIT = 'DoIt!'
PLATFORM_ANY = ANY
PLATFORM_DARWIN = 'Darwin'
PLATFORM_FREEBSD = 'FreeBSD'
PLATFORM_NETBSD = 'NetBSD'
PLATFORM_OPENBSD = 'OpenBSD'
PLATFORM_LINUX = 'Linux'
PLATFORM_POSIX = 'POSIX'
PLATFORM_SUNOS = 'SunOS'
PLATFORM_WINDOWS = 'Windows'
PLATFORM_WINCE = 'WinCE'

class Configuration(object):
    """`DoIt!` configuration.
    """
    OPT_JIT = 'jit'
    __configuration = None
    __re_invdigs = re.compile("[^0-9]+")
    __slots__ = [
        '__configured', '__is_ok', '__what_is_wrong',
        '__target_platform', '__target_machine',
        '__host_platform', '__host_version', '__host_machine', '__host_arch',
          '__host_interpreter', '__host_interpreter_version',
        '__is_posix', '__jitable'
    ]

    def __new__(cls, *args, **kwargs):
        """Creates a new or returns an existing configuration.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.

        :returns: The instance of :class:`Configuration \
            <doit.config.config.Configuration>`.
        """

        if not cls.__configuration:
            _ = lambda x: (
                x.startswith('__') and '_%s%s' % (cls.__name__, x) or x
            )
            inst = object.__new__(cls)
            setattr(inst, _('__configured'), False)
            setattr(inst, _('__is_ok'), True)
            setattr(inst, _('__what_is_wrong'), "")
            setattr(inst, _('__target_platform'), PLATFORM_ANY)
            setattr(inst, _('__target_machine'), MACHINE_DOIT)
            setattr(inst, _('__host_platform'), "")
            setattr(inst, _('__host_version'), UNUSED_VERSION)
            setattr(inst, _('__host_machine'), "")
            setattr(inst, _('__host_arch'), "")
            setattr(inst, _('__host_interpreter'), "")
            setattr(inst, _('__host_interpreter_version'), UNUSED_VERSION)
            setattr(inst, _('__is_posix'), False)
            setattr(inst, _('__jitable'), False)
            cls.__configuration = inst
        return cls.__configuration
    #-def

    def __init__(self, *args, **kwargs):
        """Initializes the configuration.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        if not self.__configured:
            self.configure(*args, **kwargs)
    #-def

    def configure(self, *args, **kwargs):
        """Gathers the informations about host environment and sets the target
        platform.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        # We suppose that configuring DoIt! will be successful:
        self.__is_ok = True
        self.__what_is_wrong = ""

        # Environment probing:
        self.__probe_host_platform(*args, **kwargs)
        self.__probe_host_machine(*args, **kwargs)
        self.__probe_host_architecture(*args, **kwargs)
        self.__fix_host_architecture(*args, **kwargs)
        self.__fix_host_machine(*args, **kwargs)
        self.__probe_host_interpreter(*args, **kwargs)
        self.__test_if_jitable(*args, **kwargs)

        # Set target platform:
        self.__set_target_platform(*args, **kwargs)

        # Done:
        self.__configured = True
    #-def

    def configured(self):
        """Test whether the configuration data was gathered and the
        configuration variables was set.

        :returns: :obj:`True` if the configuration process has been finished \
            (:class:`bool`).
        """

        return self.__configured
    #-def

    def is_ok(self):
        """Test whether the configuration process has been successful.

        :returns: :obj:`True` if the configuration process has been \
            successful (:class:`bool`).
        """

        return self.__is_ok
    #-def

    def what_is_wrong(self):
        """Gets the details about what is wrong if the configuration process
        failed.

        :returns: The failure reason (:class:`str`).
        """

        return self.__what_is_wrong
    #-def

    def target_platform(self):
        """Gets the target platform (mostly the operating system name).

        :returns: The target platform name (:class:`str`).
        """

        return self.__target_platform
    #-def

    def target_machine(self):
        """Gets the target machine (mostly the CPU type).

        :returns: The target machine name (:class:`str`).
        """

        return self.__target_machine
    #-def

    def host_platform(self):
        """Gets the host system platform name.

        :returns: The host system platform name (:class:`str`).
        """

        return self.__host_platform
    #-def

    def host_version(self):
        """Gets the host system version.

        :returns: The host system version (:class:`Version \
            <doit.config.version.Version>` or :obj:`None`).
        """

        return self.__host_version
    #-def

    def host_machine(self):
        """Gets the host machine name.

        :returns: The host machine name (:class:`str`).
        """

        return self.__host_machine
    #-def

    def host_arch(self):
        """Gets the host architecture name.

        :returns: The host architecture name (:class:`str`).
        """

        return self.__host_arch
    #-def

    def host_interpreter(self):
        """Gets the host interpreter name and version.

        :retunrs: The :class:`tuple` containing the host interpreter name \
            (:class:`str`) and the host interpreter version (:class:`Version \
            <doit.config.version.Version>` or :obj:`None`).
        """

        return self.__host_interpreter, self.__host_interpreter_version
    #-def

    def have_posix(self):
        """Test whether the host system is POSIX compatible.

        :returns: :obj:`True` if the host system is POSIX compatible \
            (:class:`bool`).
        """

        return self.__is_posix
    #-def

    def jitable(self):
        """Test whether the `DoIt!` virtual machine byte code can be compiled
        into the machine code using the just-in-time compiler.

        :returns: :obj:`True` if the `DoIt!` virtual machine code can be \
            just-in-time compiled (:class:`bool`).
        """

        return self.__jitable
    #-def

    def __probe_host_platform(self, *args, **kwargs):
        """Detects the host platform.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        self.__host_platform = ""
        self.__host_version = UNUSED_VERSION
        self.__is_posix = False
        try:
            platform_id = platform.platform()
            if not platform_id:
                self.__probe_host_platform2(*args, **kwargs)
                return
            platform_parts = platform_id.split('-')
            self.__host_platform = self.__decode_os(platform_parts[0])
            if not self.__host_platform:
                self.__probe_host_platform2(*args, **kwargs)
                return
            platform_parts[0] = self.__host_platform
            self.__host_version = self.__decode_os_version(platform_parts)
            if not self.__host_version:
                self.__host_version = Version(0, 0, 0, -1, "")
            self.__host_version.info = platform_id
            self.__post_probe_host_platform(*args, **kwargs)
        except Exception as e:
            self.__host_platform = ""
            self.__host_version = UNUSED_VERSION
            self.__is_posix = False
            if not self.__what_is_wrong:
                self.__what_is_wrong = repr(e)
            self.__is_ok = False
        except:
            self.__host_platform = ""
            self.__host_version = UNUSED_VERSION
            self.__is_posix = False
            self.__is_ok = False
        #-try
    #-def

    def __probe_host_machine(self, *args, **kwargs):
        """Detects the host machine.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        self.__host_machine = ""
        try:
            machine = platform.machine().lower()
            if machine in [ 'i386', 'i486', 'i686', 'i786', 'x86' ]:
                self.__host_machine = MACHINE_x86
            elif machine in [ 'x86_64', 'x86-64', 'x64', 'amd64' ]:
                self.__host_machine = MACHINE_x86_64
        except Exception as e:
            self.__host_machine = ""
            if not self.__what_is_wrong:
                self.__what_is_wrong = repr(e)
            self.__is_ok = False
        except:
            self.__host_machine = ""
            self.__is_ok = False
        #-try
    #-def

    def __probe_host_architecture(self, *args, **kwargs):
        """Detects the host architecture.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        self.__host_arch = ""
        try:
            bits, _ = platform.architecture()
            bits = bits.lower()
            if bits in [ ARCH_32, ARCH_64 ]:
                self.__host_arch = bits
            elif sys.maxsize > 2**32:
                self.__host_arch = ARCH_64
            elif sys.maxsize > 2**16:
                self.__host_arch = ARCH_32
        except Exception as e:
            self.__host_arch = ""
            if not self.__what_is_wrong:
                self.__what_is_wrong = repr(e)
            self.__is_ok = False
        except:
            self.__host_arch = ""
            self.__is_ok = False
        #-try
    #-def

    def __fix_host_architecture(self, *args, **kwargs):
        """Resolves the ambiguity of architecture detection on some systems.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        if self.__host_platform == PLATFORM_DARWIN \
        and self.__host_arch == ARCH_32 \
        and sys.maxsize > 2**32:
            self.__host_arch = ARCH_64
    #-def

    def __fix_host_machine(self, *args, **kwargs):
        """
        """

        if self.__host_machine == MACHINE_x86 and self.__host_arch == ARCH_64:
            self.__host_machine = MACHINE_x86_64
    #-def

    def __probe_host_interpreter(self, *args, **kwargs):
        """Detects host interpreter.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        self.__host_interpreter = ""
        self.__host_interpreter_version = UNUSED_VERSION
        try:
            self.__host_interpreter = {
                'cpython': PYTHON_CPYTHON,
                'ironpython': PYTHON_IRON,
                'jython': PYTHON_JYTHON,
                'pypy': PYTHON_PYPY
            }.get(platform.python_implementation().lower(), '')
            self.__host_interpreter_version = self.__to_version(
                platform.python_version()
            )
            python_compiler = platform.python_compiler()
            if python_compiler:
                if not self.__host_interpreter_version:
                    self.__host_interpreter_version = Version(0, 0, 0, -1, "")
                self.__host_interpreter_version.info = python_compiler
        except Exception as e:
            self.__host_interpreter = ""
            self.__host_interpreter_version = UNUSED_VERSION
            if not self.__what_is_wrong:
                self.__what_is_wrong = repr(e)
            self.__is_ok = False
        except:
            self.__host_interpreter = ""
            self.__host_interpreter_version = UNUSED_VERSION
            self.__is_ok = False
        #-try
    #-def

    def __test_if_jitable(self, *args, **kwargs):
        """Detects the support for just-in-time compiler.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        _ = lambda x: False
        self.__jitable = False
        if self.__host_interpreter != PYTHON_CPYTHON \
        or not self.__host_arch \
        or not self.__host_machine \
        or not self.__host_platform \
        or _("64bit interpreter on 32bit machine? We are doomed.") \
        or self.__host_machine == MACHINE_x86 and self.__host_arch == ARCH_64:
            return
        self.__jitable = True
    #-def

    def __set_target_platform(self, *args, **kwargs):
        """Sets the target platform.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        self.__target_machine = MACHINE_DOIT
        self.__target_platform = PLATFORM_ANY
        self.__jitable = False
        allow_JIT = self.__class__.OPT_JIT in args
        if self.__jitable and allow_JIT:
            self.__target_platform = self.__host_platform
            self.__target_machine = self.__host_machine
        if self.__target_machine == MACHINE_x86_64 \
        and self.__host_arch == ARCH_32:
            self.__target_machine = MACHINE_x86
    #-def

    def __probe_host_platform2(self, *args, **kwargs):
        """First alternative detection of the host platform.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        self.__host_platform = self.__decode_os(sys.platform)
        if not self.__host_platform:
            self.__probe_host_platform3(*args, **kwargs)
            return
        self.__post_probe_host_platform(*args, **kwargs)
    #-def

    def __probe_host_platform3(self, *args, **kwargs):
        """Second alternative detection of the host platform.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        self.__host_platform = {
            'nt': PLATFORM_WINDOWS,
            'ce': PLATFORM_WINCE,
            'posix': PLATFORM_POSIX
        }.get(os.name, '')
        self.__post_probe_host_platform(*args, **kwargs)
    #-def

    def __post_probe_host_platform(self, *args, **kwargs):
        """Fix the names of some platforms and test whether the platform is
        POSIX compatible.

        :param tuple args: A positinal arguments.
        :param dict kwargs: A keyword arguments.
        """

        if self.__host_platform == PLATFORM_WINDOWS and os.name == 'ce':
            self.__host_platform = PLATFORM_WINCE
        if os.name == 'posix':
            self.__is_posix = True
    #-def

    @staticmethod
    def __decode_os(os_name):
        """Extracts the platform name from `os_name`.

        :param str os_name: A string containing the name of operating system.

        :returns: The platform name (:class:`str`).
        """

        os_name = os_name.lower()
        if os_name.startswith('darwin'):
            return PLATFORM_DARWIN
        if os_name.startswith('freebsd'):
            return PLATFORM_FREEBSD
        if os_name.startswith('netbsd'):
            return PLATFORM_NETBSD
        if os_name.startswith('openbsd'):
            return PLATFORM_OPENBSD
        if os_name.startswith('linux'):
            return PLATFORM_LINUX
        if os_name.startswith('sunos'):
            return PLATFORM_SUNOS
        if os_name.startswith('windows'):
            return PLATFORM_WINDOWS
        if os_name.startswith('win32'):
            return PLATFORM_WINDOWS
        if os_name.startswith('cygwin'):
            return PLATFORM_WINDOWS
        if os_name.startswith('mingw'):
            return PLATFORM_WINDOWS
        if os_name.startswith('msys'):
            return PLATFORM_WINDOWS
        return ''
    #-def

    @staticmethod
    def __decode_os_version(platform_parts):
        """From `platform_parts`, extract the version.

        :param list platform_parts: A splitted platform identification string.

        :returns: The extracted version (:class:`Version \
            <doit.config.version.Version>` or :obj:`None`).
        """

        if platform_parts[0] in [
            PLATFORM_DARWIN,
            PLATFORM_FREEBSD, PLATFORM_NETBSD, PLATFORM_OPENBSD,
            PLATFORM_LINUX,
            PLATFORM_SUNOS
        ] and len(platform_parts) >= 2:
            return Configuration.__to_version(platform_parts[1])
        if platform_parts[0] == PLATFORM_WINDOWS and len(platform_parts) >= 3:
            return Configuration.__to_version(platform_parts[2])
        return UNUSED_VERSION
    #-def

    @staticmethod
    def __to_version(version_id):
        """Converts `version_id` to :class:`Version \
        <doit.config.version.Version>` object.

        :param list version_id: A version string.

        :returns: The version string converted to :class:`Version \
            <doit.config.version.Version>` object or :obj:`None`.
        """

        version_parts = version_id.split('.')
        n = len(version_parts)
        major = Configuration.__to_int(version_parts[0], -1) if n >= 1 else -1
        if major < 0:
            return UNUSED_VERSION
        minor = Configuration.__to_int(version_parts[1]) if n >= 2 else 0
        patchlevel = Configuration.__to_int(version_parts[2]) if n >= 3 else 0
        return Version(major, minor, patchlevel, -1, "")
    #-def

    @staticmethod
    def __to_int(s, default = 0):
        """Converts string `s` to integer.

        :param str s: A string to be converted.
        :param int default: A default value to return if `s` cannot be \
            converted.

        :returns: The string `s` converted to integer (:class:`int`).

        If `s` has form ``12abcd...``, ``12`` is returned. If `s` has form
        ``abcde...xyz1234``, ``1234`` is returned. Otherwise, `default` is
        returned.
        """

        numlist = Configuration.__re_invdigs.split(s)
        if numlist and numlist[0]:
            return int(numlist[0])
        if numlist and numlist[-1]:
            return int(numlist[-1])
        return default
    #-def

    @classmethod
    def reset(cls):
        """Resets the configuration cache so the new instance of
        :class:`Configuration <doit.config.config.Configuration>` is created
        when :meth:`__new__(*args, **kwargs) \
        <doit.config.config.Configuration.__new__>` is called instead of
        returning the current.
        """

        cls.__configuration = None
    #-def
#-class
