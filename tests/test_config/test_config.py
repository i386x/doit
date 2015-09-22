#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_config/test_config.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-09-12 00:26:49 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! config module tests.\
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
import unittest

from ..common import ModuleContext

from doit.config.version import Version

from doit.config.config import PYTHON_CPYTHON, \
                               ARCH_32, \
                               ARCH_64, \
                               MACHINE_x86, \
                               MACHINE_x86_64, \
                               MACHINE_DOIT, \
                               PLATFORM_ANY, \
                               PLATFORM_DARWIN, \
                               PLATFORM_FREEBSD, \
                               PLATFORM_NETBSD, \
                               PLATFORM_OPENBSD, \
                               PLATFORM_LINUX, \
                               PLATFORM_SUNOS, \
                               PLATFORM_WINDOWS, \
                               Configuration

fargs = lambda *args, **kwargs: (args, kwargs)

def patch(base, d):
    r = {}
    for k in base:
        k_ = k.replace('.', '_')
        if k_ in d:
            r[k] = d[k_]
        else:
            r[k] = base[k]
    return r
#-def

def make_cases(spec, templates):
    cases = []
    d = patch(spec, {})
    for t in templates:
        d = patch(d, t[1])
        arch = (
            "%dbit" % d['platform.architecture.bits'],
            d['platform.architecture.linkage']
        )
        pyvt = (
            d['platform.python.version.major'],
            d['platform.python.version.minor'],
            d['platform.python.version.patchlevel']
        )
        pyvs = "%d.%d.%d" % pyvt
        pycomp = "%s %d.%d.%d" % (
            d['platform.python.compiler.name'],
            d['platform.python.compiler.version.major'],
            d['platform.python.compiler.version.minor'],
            d['platform.python.compiler.version.patchlevel']
        )
        cases.append((
            # platform.platform():
            t[0][0],
            # platform.machine():
            d['platform.machine'],
            # platform.architecture():
            arch,
            # platform.python_implementation():
            d['platform.python.implementation'],
            # platform.python_version():
            pyvs,
            # platform.python_compiler():
            pycomp,
            # sys.maxsize:
            d['sys.maxsize'],
            # sys.platform:
            d['sys.platform'],
            # os.name:
            d['os.name'], (
                d['configured'],
                d['is.ok'],
                d['what.is.wrong'],
                d['target.platform'],
                d['target.machine'],
                d['host.platform'],
                Version(*(d['host.version'] + (-1, t[0][0]))),
                d['host.machine'],
                d['host.arch'],
                d['host.interpreter'],
                Version(*(pyvt + (-1, pycomp))),
                d['host.posix'],
                d['jitable']
            )
        ))
    return cases
#-def

_normal_cases_spec_base = {
    'platform.platform': "",
    'platform.machine': "amd64",
    'platform.architecture.bits': 64,
    'platform.architecture.linkage': "",
    'platform.python.implementation': "CPython",
    'platform.python.version.major': 3,
    'platform.python.version.minor': 3,
    'platform.python.version.patchlevel': 3,
    'platform.python.compiler.name': "GCC",
    'platform.python.compiler.version.major': 4,
    'platform.python.compiler.version.minor': 8,
    'platform.python.compiler.version.patchlevel': 3,
    'sys.maxsize': 2**64 - 1,
    'sys.platform': "linux2",
    'os.name': "posix",
    'configured': True,
    'is.ok': True,
    'what.is.wrong': "",
    'target.platform': PLATFORM_ANY,
    'target.machine': MACHINE_DOIT,
    'host.platform': PLATFORM_LINUX,
    'host.version': (2, 6, 26),
    'host.machine': MACHINE_x86_64,
    'host.arch': ARCH_64,
    'host.interpreter': PYTHON_CPYTHON,
    'host.posix': True,
    'jitable': False
}

# From <https://bugs.python.org/issue3937>:
_normal_cases_template = [
    fargs("Linux-2.6.26-1-vserver-amd64-x86_64-with-debian-5.0.5"),
    fargs("Linux-debian_5.0.5-x86_64-64bit",
        platform_machine = "x86_64",
        platform_python_version_minor = 4, # 3.4.3
        platform_python_compiler_version_patchlevel = 6, # 4.8.6
        sys_platform = "linux",
        host_version = (5, 0, 5)
    ),
    fargs("Linux-2.6.32-24-server-x86_64-with-Ubuntu-10.04-lucid",
        sys_platform = "linux2",
        host_version = (2, 6, 32)
    ),
    fargs("Linux-Ubuntu_10.04-x86_64-64bit_ELF",
        platform_architecture_linkage = "ELF",
        platform_python_version_patchlevel = 1, # 3.4.1
        platform_python_compiler_version_patchlevel = 5, # 4.8.5
        sys_platform = "linux",
        host_version = (10, 4, 0)
    ),
    fargs("Linux-2.6.32-24-generic-x86_64-with-Ubuntu-10.04-lucid",
        platform_architecture_linkage = "",
        platform_python_version_patchlevel = 2, # 3.4.2
        platform_python_compiler_version_patchlevel = 6, # 4.8.6
        sys_platform = "linux2",
        host_version = (2, 6, 32)
    ),
    fargs("Linux-Ubuntu_10.04-x86_64-64bit_ELF",
        platform_architecture_linkage = "ELF",
        platform_python_version_patchlevel = 0, # 3.4.0
        platform_python_compiler_version_minor = 7,
        platform_python_compiler_version_patchlevel = 1, # 4.7.1
        sys_platform = "linux",
        host_version = (10, 4, 0)
    ),
    fargs("Linux-2.6.32.8yukyuk36-x86_64-with-Ubuntu-10.04-lucid",
        platform_architecture_linkage = "",
        platform_python_version_patchlevel = 1, # 3.4.1
        platform_python_compiler_version_minor = 5, # 4.5.1
        sys_platform = "linux2",
        host_version = (2, 6, 32)
    ),
    fargs("Linux-Ubuntu_10.04-x86_64-64bit_ELF",
        platform_architecture_linkage = "ELF",
        platform_python_version_patchlevel = 2, # 3.4.2
        platform_python_compiler_version_patchlevel = 2, # 4.5.2
        sys_platform = "linux",
        host_version = (10, 4, 0)
    ),
    fargs("Linux-2.6.33.5-rscloud-x86_64-with-fedora-15-Rawhide",
        platform_architecture_linkage = "",
        platform_python_version_minor = 3,
        platform_python_version_patchlevel = 3, # 3.3.3
        platform_python_compiler_version_minor = 6,
        platform_python_compiler_version_patchlevel = 1, # 4.6.1
        sys_platform = "linux2",
        host_version = (2, 6, 33)
    ),
    fargs("Linux-fedora_15-x86_64-64bit_ELF",
        platform_architecture_linkage = "ELF",
        platform_python_version_minor = 4, # 3.4.3
        platform_python_compiler_version_minor = 7,
        platform_python_compiler_version_patchlevel = 2, # 4.7.2
        sys_platform = "linux",
        host_version = (15, 0, 0)
    ),
    fargs("Linux-2.6.24dedibox-r8-c7-i686-with-debian-5.0.5",
        platform_machine = "i686",
        platform_architecture_bits = 32,
        platform_architecture_linkage = "",
        platform_python_version_minor = 2,
        platform_python_version_patchlevel = 1, # 3.2.1
        platform_python_compiler_version_minor = 3,
        platform_python_compiler_version_patchlevel = 4, # 4.3.4
        sys_maxsize = 2**32 - 1,
        sys_platform = "linux2",
        host_version = (2, 6, 24),
        host_machine = MACHINE_x86,
        host_arch = ARCH_32
    ),
    fargs("Linux-debian_5.0.5-i686-32bit",
        sys_platform = "linux2",
        host_version = (5, 0, 5)
    ),
    fargs("SunOS-5.11-i86pc-i386-32bit",
        platform_machine = "i386",
        platform_python_version_patchlevel = 3, # 3.2.3
        platform_python_compiler_name = "Clang",
        platform_python_compiler_version_major = 3,
        platform_python_compiler_version_minor = 2,
        platform_python_compiler_version_patchlevel = 4, # 3.2.4
        sys_platform = "sunos5",
        host_platform = PLATFORM_SUNOS,
        host_version = (5, 11, 0)
    ),
    fargs("FreeBSD-8.1-STABLE-amd64-64bit-ELF",
        platform_machine = "amd64",
        platform_architecture_bits = 64,
        platform_architecture_linkage = "ELF",
        platform_python_version_minor = 4, # 3.4.3
        sys_maxsize = 2**64 - 1,
        sys_platform = "freebsd8",
        host_platform = PLATFORM_FREEBSD,
        host_version = (8, 1, 0),
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64
    ),
    fargs("OpenBSD-4.6-amd64-Genuine_Intel-R-_CPU_000_@_2.93GHz-64bit-ELF",
        sys_platform = "openbsd4",
        host_platform = PLATFORM_OPENBSD,
        host_version = (4, 6, 0)
    ),
    fargs("Linux-2.6.32.13-x86_64-with-glibc2.2.5",
        platform_machine = "x86_64",
        platform_architecture_linkage = "",
        platform_python_compiler_name = "GCC",
        platform_python_compiler_version_major = 4,
        platform_python_compiler_version_minor = 8,
        platform_python_compiler_version_patchlevel = 7, # 4.8.7
        sys_platform = "linux2",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 32)
    ),
    fargs("NetBSD-5.0.2-i386-32bit-ELF",
        platform_machine = "i386",
        platform_architecture_bits = 32,
        platform_architecture_linkage = "ELF",
        platform_python_version_minor = 2,
        platform_python_version_patchlevel = 2, # 3.2.2
        platform_python_compiler_name = "Clang",
        platform_python_compiler_version_major = 3,
        platform_python_compiler_version_minor = 4,
        platform_python_compiler_version_patchlevel = 5, # 3.4.5
        sys_maxsize = 2**32 - 1,
        sys_platform = "netbsd5",
        host_platform = PLATFORM_NETBSD,
        host_version = (5, 0, 2),
        host_machine = MACHINE_x86,
        host_arch = ARCH_32
    ),
    fargs("Linux-2.6.32-trunk-iop32x-armv5tel-with-debian-squeeze-sid",
        platform_machine = "armv5tel",
        platform_architecture_linkage = "",
        platform_python_version_patchlevel = 1, # 3.2.1
        platform_python_compiler_name = "GCC",
        platform_python_compiler_version_major = 4,
        platform_python_compiler_version_minor = 3,
        platform_python_compiler_version_patchlevel = 3, # 4.3.3
        sys_platform = "linux2",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 32),
        host_machine = ""
    ),
    fargs("Linux-debian_squeeze/sid-armv5tel-32bit_ELF",
        platform_architecture_linkage = "ELF",
        sys_platform = "linux",
        host_version = (0, 0, 0)
    ),
    fargs("Linux-2.6.18-194.8.1.el5-i686-athlon-with-redhat-5.5-Final",
        platform_machine = "i686",
        platform_architecture_linkage = "",
        platform_python_version_minor = 3,
        platform_python_version_patchlevel = 3, # 3.3.3
        platform_python_compiler_version_minor = 5,
        platform_python_compiler_version_patchlevel = 6, # 4.5.6
        sys_platform = "linux2",
        host_version = (2, 6, 18),
        host_machine = MACHINE_x86
    ),
    fargs("Linux-redhat_5.5-i686-32bit_ELF",
        platform_architecture_linkage = "ELF",
        sys_platform = "linux",
        host_version = (5, 5, 0)
    ),
    fargs("Darwin-8.11.1-i386-32bit",
        platform_machine = "i386",
        platform_architecture_linkage = "",
        platform_python_compiler_name = "Clang",
        platform_python_compiler_version_major = 3,
        platform_python_compiler_version_minor = 4,
        platform_python_compiler_version_patchlevel = 5, # 3.4.5
        sys_platform = "darwin8",
        host_platform = PLATFORM_DARWIN,
        host_version = (8, 11, 1)
    ),
    fargs("Darwin-10.4.0-i386-64bit",
        platform_architecture_bits = 64,
        platform_python_version_minor = 4, # 3.4.3
        platform_python_compiler_version_minor = 5,
        platform_python_compiler_version_patchlevel = 2, # 3.5.2
        sys_maxsize = 2**64 - 1,
        sys_platform = "darwin10",
        host_platform = PLATFORM_DARWIN,
        host_version = (10, 4, 0),
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64
    ),
    fargs("Windows-XP-5.1.2600-SP3",
        platform_machine = "x86",
        platform_architecture_bits = 32,
        platform_architecture_linkage = "WindowsPE",
        platform_python_version_minor = 3, # 3.3.3
        platform_python_compiler_name = "MSC",
        platform_python_compiler_version_major = 1200,
        platform_python_compiler_version_minor = 0,
        platform_python_compiler_version_patchlevel = 0, # 1200.0.0
        sys_maxsize = 2**32 - 1,
        sys_platform = "windows",
        os_name = "nt",
        host_platform = PLATFORM_WINDOWS,
        host_version = (5, 1, 2600),
        host_machine = MACHINE_x86,
        host_arch = ARCH_32,
        host_posix = False
    ),
    fargs("Windows-post2008Server-6.1.7600",
        platform_machine = "AMD64",
        platform_architecture_bits = 64,
        platform_python_compiler_version_major = 1600, # 1600.0.0
        sys_maxsize = 2**64 - 1,
        host_version = (6, 1, 7600),
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64
    )
]

_normal_cases = make_cases(_normal_cases_spec_base, _normal_cases_template)

class PlatformSysOsModules(ModuleContext):
    __slots__ = [
        '__old_platform_platform',
        '__old_platform_machine',
        '__old_platform_architecture',
        '__old_platform_python_implementation',
        '__old_platform_python_version',
        '__old_platform_python_compiler',
        '__old_sys_maxsize',
        '__old_sys_platform',
        '__old_os_name'
    ]

    def __init__(self, env):
        ModuleContext.__init__(self, env)
        self.__old_platform_platform = platform.platform
        self.__old_platform_machine = platform.machine
        self.__old_platform_architecture = platform.architecture
        self.__old_platform_python_implementation = \
            platform.python_implementation
        self.__old_platform_python_version = platform.python_version
        self.__old_platform_python_compiler = platform.python_compiler
        self.__old_sys_maxsize = sys.maxsize
        self.__old_sys_platform = sys.platform
        self.__old_os_name = os.name
    #-def

    def replace(self, env):
        def _platform():
            return env[0]
        def _machine():
            return env[1]
        def _architecture():
            return env[2]
        def _python_implementation():
            return env[3]
        def _python_version():
            return env[4]
        def _python_compiler():
            return env[5]

        platform.platform = _platform
        platform.machine = _machine
        platform.architecture = _architecture
        platform.python_implementation = _python_implementation
        platform.python_version = _python_version
        platform.python_compiler = _python_compiler
        sys.maxsize = env[6]
        sys.platform = env[7]
        os.name = env[8]
    #-def

    def restore(self):
        platform.platform = self.__old_platform_platform
        platform.machine = self.__old_platform_machine
        platform.architecture = self.__old_platform_architecture
        platform.python_implementation = \
            self.__old_platform_python_implementation
        platform.python_version = self.__old_platform_python_version
        platform.python_compiler = self.__old_platform_python_compiler
        sys.maxsize = self.__old_sys_maxsize
        sys.platform = self.__old_sys_platform
        os.name = self.__old_os_name
    #-def
#-class

class TestConfigurationCase(unittest.TestCase):

    def test_normal_cases(self):
        for t in _normal_cases:
            self.do_test(t)
    #-def

    def do_test(self, env):
        with PlatformSysOsModules(env):
            Configuration.reset()
            cfg = Configuration()
        self.check(cfg, env)
    #-def

    def check(self, cfg, env):
        r = env[9]
        self.assertIs(cfg.configured(), r[0])
        self.assertIs(cfg.is_ok(), r[1])
        self.assertEqual(cfg.what_is_wrong(), r[2])
        self.assertEqual(cfg.target_platform(), r[3])
        self.assertEqual(cfg.target_machine(), r[4])
        self.assertEqual(cfg.host_platform(), r[5])
        self.assertEqual(cfg.host_version(), r[6])
        self.assertEqual(cfg.host_version().info, r[6].info)
        self.assertEqual(cfg.host_machine(), r[7])
        self.assertEqual(cfg.host_arch(), r[8])
        self.assertEqual(cfg.host_interpreter()[0], r[9])
        self.assertEqual(cfg.host_interpreter()[1], r[10])
        self.assertEqual(cfg.host_interpreter()[1].info, r[10].info)
        self.assertIs(cfg.have_posix(), r[11])
        self.assertIs(cfg.jitable(), r[12])
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConfigurationCase))
    return suite
#-def
