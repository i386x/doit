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

from doit.config.version import Version, UNUSED_VERSION

from doit.config.config import PYTHON_CPYTHON, \
                               PYTHON_IRON, \
                               PYTHON_JYTHON, \
                               PYTHON_PYPY, \
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
                               PLATFORM_POSIX, \
                               PLATFORM_SUNOS, \
                               PLATFORM_WINDOWS, \
                               PLATFORM_WINCE, \
                               Configuration

fargs = lambda *args, **kwargs: (args, kwargs)

def _version_or_unused(vt, vi):
    if not vt and (not vi or isinstance(vi, Raises)):
        return UNUSED_VERSION
    if not vt:
        vt = (0, 0, 0)
    return Version(*(vt + (-1, vi)))
#-def

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
        if isinstance(d['platform.architecture.bits'], Raises):
            arch = d['platform.architecture.bits']
        else:
            arch = (
                "%dbit" % d['platform.architecture.bits'],
                d['platform.architecture.linkage']
            )
        if d['platform.python.version.major'] < 0:
            pyvt = None
            pyvs = ""
        else:
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
        if not d['platform.python.compiler.name']:
            pycomp = ""
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
                _version_or_unused(d['host.version'], t[0][0]),
                d['host.machine'],
                d['host.arch'],
                d['host.python.implementation'],
                _version_or_unused(
                    d['host.python.version'], d['host.python.compiler']
                ),
                d['host.posix'],
                d['jitable']
            )
        ))
    return cases
#-def

class Raises(object):
    __slots__ = [ 'what' ]

    def __init__(self, what):
        self.what = what
    #-def
#-class

_platform_cases_spec_base = {
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
    'sys.platform': "",
    'os.name': "",
    'configured': True,
    'is.ok': True,
    'what.is.wrong': "",
    'target.platform': PLATFORM_ANY,
    'target.machine': MACHINE_DOIT,
    'host.platform': "",
    'host.version': (0, 0, 0),
    'host.machine': MACHINE_x86_64,
    'host.arch': ARCH_64,
    'host.python.implementation': PYTHON_CPYTHON,
    'host.python.version': (3, 3, 3),
    'host.python.compiler': "GCC 4.8.3",
    'host.posix': False,
    'jitable': False
}

_platform_cases_template = [
    # `platform.platform()` works:
    fargs("Darwin-10.4.0-i386-64bit",
        platform_machine = "i386",
        sys_platform = "darwin10",
        os_name = "posix",
        host_platform = PLATFORM_DARWIN,
        host_version = (10, 4, 0),
        host_posix = True,
        jitable = True
    ),
    fargs("FreeBSD-8.1-x64-64bit",
        platform_machine = "x64",
        sys_platform = "freebsd8",
        host_platform = PLATFORM_FREEBSD,
        host_version = (8, 1, 0)
    ),
    fargs("NetBSD-5.0.2-amd64-64bit",
        platform_machine = "amd64",
        sys_platform = "netbsd5",
        host_platform = PLATFORM_NETBSD,
        host_version = (5, 0, 2)
    ),
    fargs("OpenBSD-4.6-x86_64-64bit",
        platform_machine = "x86_64",
        sys_platform = "openbsd4",
        host_platform = PLATFORM_OPENBSD,
        host_version = (4, 6, 0)
    ),
    fargs("Linux-2.6.32-x86_64-64bit",
        sys_platform = "linux2",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 32)
    ),
    fargs("SunOS-5.11-x64-64bit",
        platform_machine = "x64",
        sys_platform = "sunos5",
        host_platform = PLATFORM_SUNOS,
        host_version = (5, 11, 0)
    ),
    fargs("Windows-8-6.2.9200",
        platform_machine = "amd64",
        sys_platform = "win32",
        os_name = "nt",
        host_platform = PLATFORM_WINDOWS,
        host_version = (6, 2, 9200),
        host_posix = False
    ),
    fargs("CYGWIN_NT-6.3-WOW64-1.7.32-0.274-5-3-x86_64-64bit",
        platform_machine = "x86_64",
        sys_platform = "cygwin",
        os_name = "posix",
        host_platform = PLATFORM_WINDOWS,
        host_version = (6, 3, 0),
        host_posix = True
    ),
    fargs("MSYS_NT-6.2-x86_64-64bit",
        sys_platform = "msys",
        host_version = (6, 2, 0)
    ),
    fargs("MINGW32_NT-6.1-x86_64-64bit",
        sys_platform = "mingw",
        host_version = (6, 1, 0)
    ),
    # `platform.platform()` does not work -> use `sys.platform`:
    fargs("",
        platform_machine = "i386",
        sys_platform = "darwin10",
        os_name = "posix",
        host_platform = PLATFORM_DARWIN,
        host_version = UNUSED_VERSION,
        host_posix = True
    ),
    fargs("",
        platform_machine = "x64",
        sys_platform = "freebsd8",
        host_platform = PLATFORM_FREEBSD
    ),
    fargs("",
        platform_machine = "amd64",
        sys_platform = "netbsd5",
        host_platform = PLATFORM_NETBSD
    ),
    fargs("",
        platform_machine = "x86_64",
        sys_platform = "openbsd4",
        host_platform = PLATFORM_OPENBSD
    ),
    fargs("",
        sys_platform = "linux2",
        host_platform = PLATFORM_LINUX
    ),
    fargs("",
        platform_machine = "x64",
        sys_platform = "sunos5",
        host_platform = PLATFORM_SUNOS
    ),
    fargs("",
        platform_machine = "amd64",
        sys_platform = "win32",
        os_name = "nt",
        host_platform = PLATFORM_WINDOWS,
        host_posix = False
    ),
    fargs("",
        platform_machine = "x86_64",
        sys_platform = "cygwin",
        os_name = "posix",
        host_platform = PLATFORM_WINDOWS,
        host_posix = True
    ),
    fargs("",
        sys_platform = "msys"
    ),
    fargs("",
        sys_platform = "mingw"
    ),
    # `sys.platform()` does not work -> use `os.name`:
    fargs("",
        platform_machine = "i386",
        sys_platform = "",
        os_name = "posix",
        host_platform = PLATFORM_POSIX,
        host_version = UNUSED_VERSION,
        host_posix = True
    ),
    fargs("",
        platform_machine = "amd64",
        os_name = "nt",
        host_platform = PLATFORM_WINDOWS,
        host_posix = False
    ),
    fargs("",
        os_name = "ce",
        host_platform = PLATFORM_WINCE
    ),
    # Unknown platform:
    fargs("Unknown-1.2.3-amd64-64bit",
        sys_platform = "unknown",
        os_name = "",
        host_platform = "",
        host_version = (0, 0, 0),
        jitable = False
    ),
    # post_probe test:
    fargs("Windows-CE-2.3.2600-power6-32bit",
        platform_machine = "power6",
        platform_architecture_bits = 32,
        sys_maxsize = 2**32 - 1,
        sys_platform = "wince",
        os_name = "ce",
        host_platform = PLATFORM_WINCE,
        host_version = (2, 3, 2600),
        host_machine = "",
        host_arch = ARCH_32
    )
]

_platform_cases = make_cases(
    _platform_cases_spec_base, _platform_cases_template
)

_machine_cases_spec_base = {
    'platform.platform': "",
    'platform.machine': "",
    'platform.architecture.bits': 0,
    'platform.architecture.linkage': "",
    'platform.python.implementation': "CPython",
    'platform.python.version.major': 3,
    'platform.python.version.minor': 3,
    'platform.python.version.patchlevel': 3,
    'platform.python.compiler.name': "GCC",
    'platform.python.compiler.version.major': 4,
    'platform.python.compiler.version.minor': 8,
    'platform.python.compiler.version.patchlevel': 3,
    'sys.maxsize': 0,
    'sys.platform': "",
    'os.name': "",
    'configured': True,
    'is.ok': True,
    'what.is.wrong': "",
    'target.platform': PLATFORM_ANY,
    'target.machine': MACHINE_DOIT,
    'host.platform': "",
    'host.version': UNUSED_VERSION,
    'host.machine': "",
    'host.arch': "",
    'host.python.implementation': PYTHON_CPYTHON,
    'host.python.version': (3, 3, 3),
    'host.python.compiler': "GCC 4.8.3",
    'host.posix': False,
    'jitable': False
}

_machine_cases_template = [
    fargs("Linux-2.6.26-i386-32bit",
        platform_machine = "i386",
        platform_architecture_bits = 32,
        sys_maxsize = 2**32 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86,
        host_arch = ARCH_32,
        host_posix = True,
        jitable = True
    ),
    fargs("Linux-2.6.26-i486-32bit",
        platform_machine = "i486"
    ),
    fargs("Linux-2.6.26-i686-32bit",
        platform_machine = "i686"
    ),
    fargs("Linux-2.6.26-i786-32bit",
        platform_machine = "i786"
    ),
    fargs("Linux-2.6.26-x86-32bit",
        platform_machine = "x86"
    ),
    fargs("Linux-2.6.26-x86_64-64bit",
        platform_machine = "x86_64",
        platform_architecture_bits = 64,
        sys_maxsize = 2**64 - 1,
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64
    ),
    fargs("Linux-2.6.26-x86_64-64bit",
        platform_machine = "x86-64"
    ),
    fargs("Linux-2.6.26-x64-64bit",
        platform_machine = "x64"
    ),
    fargs("Linux-2.6.26-AMD64-64bit",
        platform_machine = "AMD64"
    ),
    fargs("Linux-2.6.26-ARM5-32bit",
        platform_machine = "ARM5",
        platform_architecture_bits = 32,
        sys_maxsize = 2**32 - 1,
        host_machine = "",
        host_arch = ARCH_32,
        jitable = False
    )
]

_machine_cases = make_cases(_machine_cases_spec_base, _machine_cases_template)

_architecture_cases_spec_base = patch(_machine_cases_spec_base, {})

_architecture_cases_template = [
    fargs("Linux-2.6.26-i386-32bit",
        platform_machine = "i386",
        platform_architecture_bits = 32,
        sys_maxsize = 2**32 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86,
        host_arch = ARCH_32,
        host_posix = True,
        jitable = True
    ),
    fargs("Linux-2.6.26-x86_64-64bit",
        platform_machine = "x86_64",
        platform_architecture_bits = 64,
        sys_maxsize = 2**64 - 1,
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64
    ),
    fargs("Linux-2.6.26-x86_64",
        platform_architecture_bits = 0
    ),
    fargs("Linux-2.6.26-i386",
        platform_machine = "i386",
        sys_maxsize = 2**32 - 1,
        host_machine = MACHINE_x86,
        host_arch = ARCH_32
    ),
    fargs("Linux-2.6.26-unknown",
        platform_machine = "unknown",
        sys_maxsize = 0,
        host_machine = "",
        host_arch = "",
        jitable = False
    )
]

_architecture_cases = make_cases(
    _architecture_cases_spec_base, _architecture_cases_template
)

_fixes_cases_spec_base = patch(_machine_cases_spec_base, {})

_fixes_cases_expected_0 = [
    ("", ""), ("", ARCH_32), ("", ARCH_64),
    ("", ARCH_32), ("", ARCH_32), ("", ARCH_64),
    ("", ARCH_64), ("", ARCH_32), ("", ARCH_64)
]
_fixes_cases_expected_1 = [
    (MACHINE_x86, ARCH_32), (MACHINE_x86, ARCH_32), (MACHINE_x86_64, ARCH_64),
    (MACHINE_x86, ARCH_32), (MACHINE_x86, ARCH_32), (MACHINE_x86_64, ARCH_64),
    (MACHINE_x86_64, ARCH_64), (MACHINE_x86, ARCH_32),
      (MACHINE_x86_64, ARCH_64)
]
_fixes_cases_expected_2 = [
    (MACHINE_x86_64, ARCH_64), (MACHINE_x86, ARCH_32),
      (MACHINE_x86_64, ARCH_64),
    (MACHINE_x86, ARCH_32), (MACHINE_x86, ARCH_32), (MACHINE_x86_64, ARCH_64),
    (MACHINE_x86_64, ARCH_64), (MACHINE_x86, ARCH_32),
      (MACHINE_x86_64, ARCH_64)
]
_fixes_cases_expected = (
    _fixes_cases_expected_0, _fixes_cases_expected_1, _fixes_cases_expected_2
)

_fixes_cases_template = []

_xs = ["", MACHINE_x86, MACHINE_x86_64]
_ys = [0, 32, 64]
_zs = [0, 2**32 - 1, 2**64 - 1]
for x in _xs:
    for y in _ys:
        for z in _zs:
            p = '-'.join(
                ["Linux", "2.6.26"] \
                + [x for x in [x] if x] \
                + ["%dbit" % y for y in [y] if y]
            )
            i = _xs.index(x)
            j =  _ys.index(y)*3 + _zs.index(z)
            m, a = _fixes_cases_expected[i][j]
            _fixes_cases_template.append(
                fargs(p,
                    platform_machine = x,
                    platform_architecture_bits = y,
                    sys_maxsize = z,
                    sys_platform = "linux2",
                    os_name = "posix",
                    host_platform = PLATFORM_LINUX,
                    host_version = (2, 6, 26),
                    host_machine = m,
                    host_arch = a,
                    host_posix = True,
                    jitable = True if m and a else False
                )
            )
        #-for
    #-for
#-for

_fixes_cases = make_cases(_fixes_cases_spec_base, _fixes_cases_template)

_python_cases_spec_base = patch(_machine_cases_spec_base, {})

_python_cases_template = [
    fargs("Linux-2.6.26-i386-32bit",
        platform_machine = "i386",
        platform_architecture_bits = 32,
        platform_python_implementation = "CPython",
        platform_python_version_major = 3,
        platform_python_version_minor = 4,
        platform_python_version_patchlevel = 3,
        platform_python_compiler_name = "GCC",
        platform_python_compiler_version_major = 4,
        platform_python_compiler_version_minor = 7,
        platform_python_compiler_version_patchlevel = 2,
        sys_maxsize = 2**32 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86,
        host_arch = ARCH_32,
        host_python_implementation = PYTHON_CPYTHON,
        host_python_version = (3, 4, 3),
        host_python_compiler = "GCC 4.7.2",
        host_posix = True,
        jitable = True
    ),
    fargs("Linux-2.6.26-i386-32bit",
        platform_python_implementation = "IronPython",
        platform_python_version_major = 3,
        platform_python_version_minor = 3,
        platform_python_version_patchlevel = 2,
        platform_python_compiler_name = ".NET",
        platform_python_compiler_version_major = 2,
        platform_python_compiler_version_minor = 2,
        platform_python_compiler_version_patchlevel = 0,
        host_python_implementation = PYTHON_IRON,
        host_python_version = (3, 3, 2),
        host_python_compiler = ".NET 2.2.0",
        jitable = False
    ),
    fargs("Linux-2.6.26-i386-32bit",
        platform_python_implementation = "Jython",
        platform_python_version_major = 3,
        platform_python_version_minor = 3,
        platform_python_version_patchlevel = 3,
        platform_python_compiler_name = "java_se",
        platform_python_compiler_version_major = 6,
        platform_python_compiler_version_minor = 2,
        platform_python_compiler_version_patchlevel = 6,
        sys_platform = "java_se",
        host_python_implementation = PYTHON_JYTHON,
        host_python_version = (3, 3, 3),
        host_python_compiler = "java_se 6.2.6"
    ),
    fargs("Linux-2.6.26-i386-32bit",
        platform_python_implementation = "PyPy",
        platform_python_version_major = 3,
        platform_python_version_minor = 2,
        platform_python_version_patchlevel = 1,
        platform_python_compiler_name = "",
        platform_python_compiler_version_major = 0,
        platform_python_compiler_version_minor = 0,
        platform_python_compiler_version_patchlevel = 0,
        sys_platform = "linux2",
        host_python_implementation = PYTHON_PYPY,
        host_python_version = (3, 2, 1),
        host_python_compiler = ""
    ),
    fargs("Linux-2.6.26-i386-32bit",
        platform_python_implementation = "Unknown",
        platform_python_version_major = 1,
        platform_python_version_minor = 2,
        platform_python_version_patchlevel = 1,
        platform_python_compiler_name = "Clang",
        platform_python_compiler_version_major = 2,
        platform_python_compiler_version_minor = 0,
        platform_python_compiler_version_patchlevel = 1,
        host_python_implementation = "",
        host_python_version = (1, 2, 1),
        host_python_compiler = "Clang 2.0.1"
    ),
    fargs("Linux-2.6.26-i386-32bit",
        platform_python_implementation = "CPython",
        platform_python_version_major = -1,
        platform_python_version_minor = 3,
        platform_python_version_patchlevel = 4,
        platform_python_compiler_name = "Clang",
        platform_python_compiler_version_major = 2,
        platform_python_compiler_version_minor = 1,
        platform_python_compiler_version_patchlevel = 1,
        host_python_implementation = PYTHON_CPYTHON,
        host_python_version = (0, 0, 0),
        host_python_compiler = "Clang 2.1.1",
        jitable = True
    ),
    fargs("Linux-2.6.26-i386-32bit",
        platform_python_implementation = "CPython",
        platform_python_version_major = -1,
        platform_python_version_minor = 3,
        platform_python_version_patchlevel = 4,
        platform_python_compiler_name = "",
        platform_python_compiler_version_major = 2,
        platform_python_compiler_version_minor = 2,
        platform_python_compiler_version_patchlevel = 1,
        host_python_implementation = PYTHON_CPYTHON,
        host_python_version = UNUSED_VERSION,
        host_python_compiler = ""
    ),
    fargs("Linux-2.6.26-i386-32bit",
        platform_python_implementation = "Unknown",
        platform_python_version_major = -1,
        platform_python_version_minor = 3,
        platform_python_version_patchlevel = 4,
        platform_python_compiler_name = "",
        platform_python_compiler_version_major = 2,
        platform_python_compiler_version_minor = 0,
        platform_python_compiler_version_patchlevel = 0,
        host_python_implementation = "",
        host_python_version = UNUSED_VERSION,
        host_python_compiler = "",
        jitable = False
    )
]

_python_cases = make_cases(_python_cases_spec_base, _python_cases_template)

_error_cases_spec_base = {
    'platform.platform': "",
    'platform.machine': "",
    'platform.architecture.bits': 0,
    'platform.architecture.linkage': "",
    'platform.python.implementation': "CPython",
    'platform.python.version.major': 3,
    'platform.python.version.minor': 3,
    'platform.python.version.patchlevel': 3,
    'platform.python.compiler.name': "GCC",
    'platform.python.compiler.version.major': 4,
    'platform.python.compiler.version.minor': 8,
    'platform.python.compiler.version.patchlevel': 3,
    'sys.maxsize': 0,
    'sys.platform': "",
    'os.name': "",
    'configured': True,
    'is.ok': True,
    'what.is.wrong': "",
    'target.platform': PLATFORM_ANY,
    'target.machine': MACHINE_DOIT,
    'host.platform': "",
    'host.version': UNUSED_VERSION,
    'host.machine': "",
    'host.arch': "",
    'host.python.implementation': PYTHON_CPYTHON,
    'host.python.version': (3, 3, 3),
    'host.python.compiler': "GCC 4.8.3",
    'host.posix': False,
    'jitable': False
}

_error_cases_template = [
    # platform.platform():
    fargs(Raises(Exception("platform.platform() failed")),
        platform_machine = "amd64",
        platform_architecture_bits = 64,
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.platform() failed',)",
        host_platform = "",
        host_version = UNUSED_VERSION,
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64,
        host_posix = False
    ),
    fargs(Raises(BaseException("platform.platform() failed")),
        platform_machine = "amd64",
        platform_architecture_bits = 64,
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "",
        host_platform = "",
        host_version = UNUSED_VERSION,
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64,
        host_posix = False
    ),
    # platform.machine():
    fargs(Raises(Exception("platform.platform() failed")),
        platform_machine = Raises(Exception("platform.machine() failed")),
        platform_architecture_bits = 64,
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.platform() failed',)",
        host_platform = "",
        host_version = UNUSED_VERSION,
        host_machine = "",
        host_arch = ARCH_64,
        host_posix = False
    ),
    fargs(Raises(BaseException("platform.platform() failed")),
        platform_machine = Raises(Exception("platform.machine() failed")),
        platform_architecture_bits = 64,
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.machine() failed',)",
        host_platform = "",
        host_version = UNUSED_VERSION,
        host_machine = "",
        host_arch = ARCH_64,
        host_posix = False
    ),
    fargs("Linux-2.6.26-64bit",
        platform_machine = Raises(Exception("platform.machine() failed")),
        platform_architecture_bits = 64,
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.machine() failed',)",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = "",
        host_arch = ARCH_64,
        host_posix = True
    ),
    fargs("Linux-2.6.26-64bit",
        platform_machine = Raises(BaseException("platform.machine() failed")),
        platform_architecture_bits = 64,
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = "",
        host_arch = ARCH_64,
        host_posix = True
    ),
    # platform.architecture():
    fargs("Linux-2.6.26",
        platform_machine = Raises(Exception("platform.machine() failed")),
        platform_architecture_bits = Raises(Exception(
            "platform.architecture() failed"
        )),
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.machine() failed',)",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = "",
        host_arch = "",
        host_posix = True
    ),
    fargs("Linux-2.6.26",
        platform_machine = Raises(BaseException("platform.machine() failed")),
        platform_architecture_bits = Raises(Exception(
            "platform.architecture() failed"
        )),
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.architecture() failed',)",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = "",
        host_arch = "",
        host_posix = True
    ),
    fargs("Linux-2.6.26-x86_64",
        platform_machine = "x86_64",
        platform_architecture_bits = Raises(Exception(
            "platform.architecture() failed"
        )),
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.architecture() failed',)",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86_64,
        host_arch = "",
        host_posix = True
    ),
    fargs("Linux-2.6.26-x86_64",
        platform_machine = "x86_64",
        platform_architecture_bits = Raises(BaseException(
            "platform.architecture() failed"
        )),
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86_64,
        host_arch = "",
        host_posix = True
    ),
    # platform.python_implementation():
    fargs("Linux-2.6.26-x86_64",
        platform_machine = "x86_64",
        platform_architecture_bits = Raises(Exception(
            "platform.architecture() failed"
        )),
        platform_python_implementation = Raises(Exception(
            "platform.implementation() failed"
        )),
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.architecture() failed',)",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86_64,
        host_arch = "",
        host_python_implementation = "",
        host_python_version = UNUSED_VERSION,
        host_python_compiler = "",
        host_posix = True
    ),
    fargs("Linux-2.6.26-x86_64",
        platform_machine = "x86_64",
        platform_architecture_bits = Raises(BaseException(
            "platform.architecture() failed"
        )),
        platform_python_implementation = Raises(Exception(
            "platform.implementation() failed"
        )),
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.implementation() failed',)",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86_64,
        host_arch = "",
        host_python_implementation = "",
        host_python_version = UNUSED_VERSION,
        host_python_compiler = "",
        host_posix = True
    ),
    fargs("Linux-2.6.26-x86_64-64bit",
        platform_machine = "x86_64",
        platform_architecture_bits = 64,
        platform_python_implementation = Raises(Exception(
            "platform.implementation() failed"
        )),
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "Exception('platform.implementation() failed',)",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64,
        host_python_implementation = "",
        host_python_version = UNUSED_VERSION,
        host_python_compiler = "",
        host_posix = True
    ),
    fargs("Linux-2.6.26-x86_64-64bit",
        platform_machine = "x86_64",
        platform_architecture_bits = 64,
        platform_python_implementation = Raises(BaseException(
            "platform.implementation() failed"
        )),
        sys_maxsize = 2**64 - 1,
        sys_platform = "linux2",
        os_name = "posix",
        is_ok = False,
        what_is_wrong = "",
        host_platform = PLATFORM_LINUX,
        host_version = (2, 6, 26),
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64,
        host_python_implementation = "",
        host_python_version = UNUSED_VERSION,
        host_python_compiler = "",
        host_posix = True
    )
]

_error_cases = make_cases(_error_cases_spec_base, _error_cases_template)

_set_target_platform_cases_spec_base = {
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
    'host.python.implementation': PYTHON_CPYTHON,
    'host.python.version': (3, 3, 3),
    'host.python.compiler': "GCC 4.8.3",
    'host.posix': True,
    'jitable': True
}

_set_target_platform_cases_template = [
    fargs("Linux-2.6.26-amd64-64bit",
        target_platform = PLATFORM_LINUX,
        target_machine = MACHINE_x86_64
    ),
    fargs("Linux-2.6.26-arm5-32bit",
        platform_machine = "arm5",
        platform_architecture_bits = 32,
        sys_maxsize = 2**32 - 1,
        target_platform = PLATFORM_ANY,
        target_machine = MACHINE_DOIT,
        host_machine = "",
        host_arch = ARCH_32,
        jitable = False
    )
]

_set_target_platform_cases = make_cases(
    _set_target_platform_cases_spec_base, _set_target_platform_cases_template
)

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
    'host.python.implementation': PYTHON_CPYTHON,
    'host.python.version': (3, 3, 3),
    'host.python.compiler': "GCC 4.8.3",
    'host.posix': True,
    'jitable': True
}

# From <https://bugs.python.org/issue3937>:
_normal_cases_template = [
    fargs("Linux-2.6.26-1-vserver-amd64-x86_64-with-debian-5.0.5"),
    fargs("Linux-debian_5.0.5-x86_64-64bit",
        platform_machine = "x86_64",
        platform_python_version_minor = 4, # 3.4.3
        platform_python_compiler_version_patchlevel = 6, # 4.8.6
        sys_platform = "linux",
        host_version = (5, 0, 5),
        host_python_version = (3, 4, 3),
        host_python_compiler = "GCC 4.8.6"
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
        host_version = (10, 4, 0),
        host_python_version = (3, 4, 1),
        host_python_compiler = "GCC 4.8.5"
    ),
    fargs("Linux-2.6.32-24-generic-x86_64-with-Ubuntu-10.04-lucid",
        platform_architecture_linkage = "",
        platform_python_version_patchlevel = 2, # 3.4.2
        platform_python_compiler_version_patchlevel = 6, # 4.8.6
        sys_platform = "linux2",
        host_version = (2, 6, 32),
        host_python_version = (3, 4, 2),
        host_python_compiler = "GCC 4.8.6"
    ),
    fargs("Linux-Ubuntu_10.04-x86_64-64bit_ELF",
        platform_architecture_linkage = "ELF",
        platform_python_version_patchlevel = 0, # 3.4.0
        platform_python_compiler_version_minor = 7,
        platform_python_compiler_version_patchlevel = 1, # 4.7.1
        sys_platform = "linux",
        host_version = (10, 4, 0),
        host_python_version = (3, 4, 0),
        host_python_compiler = "GCC 4.7.1"
    ),
    fargs("Linux-2.6.32.8yukyuk36-x86_64-with-Ubuntu-10.04-lucid",
        platform_architecture_linkage = "",
        platform_python_version_patchlevel = 1, # 3.4.1
        platform_python_compiler_version_minor = 5, # 4.5.1
        sys_platform = "linux2",
        host_version = (2, 6, 32),
        host_python_version = (3, 4, 1),
        host_python_compiler = "GCC 4.5.1"
    ),
    fargs("Linux-Ubuntu_10.04-x86_64-64bit_ELF",
        platform_architecture_linkage = "ELF",
        platform_python_version_patchlevel = 2, # 3.4.2
        platform_python_compiler_version_patchlevel = 2, # 4.5.2
        sys_platform = "linux",
        host_version = (10, 4, 0),
        host_python_version = (3, 4, 2),
        host_python_compiler = "GCC 4.5.2"
    ),
    fargs("Linux-2.6.33.5-rscloud-x86_64-with-fedora-15-Rawhide",
        platform_architecture_linkage = "",
        platform_python_version_minor = 3,
        platform_python_version_patchlevel = 3, # 3.3.3
        platform_python_compiler_version_minor = 6,
        platform_python_compiler_version_patchlevel = 1, # 4.6.1
        sys_platform = "linux2",
        host_version = (2, 6, 33),
        host_python_version = (3, 3, 3),
        host_python_compiler = "GCC 4.6.1"
    ),
    fargs("Linux-fedora_15-x86_64-64bit_ELF",
        platform_architecture_linkage = "ELF",
        platform_python_version_minor = 4, # 3.4.3
        platform_python_compiler_version_minor = 7,
        platform_python_compiler_version_patchlevel = 2, # 4.7.2
        sys_platform = "linux",
        host_version = (15, 0, 0),
        host_python_version = (3, 4, 3),
        host_python_compiler = "GCC 4.7.2"
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
        host_arch = ARCH_32,
        host_python_version = (3, 2, 1),
        host_python_compiler = "GCC 4.3.4"
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
        host_version = (5, 11, 0),
        host_python_version = (3, 2, 3),
        host_python_compiler = "Clang 3.2.4"
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
        host_arch = ARCH_64,
        host_python_version = (3, 4, 3)
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
        host_version = (2, 6, 32),
        host_python_compiler = "GCC 4.8.7"
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
        host_arch = ARCH_32,
        host_python_version = (3, 2, 2),
        host_python_compiler = "Clang 3.4.5"
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
        host_machine = "",
        host_python_version = (3, 2, 1),
        host_python_compiler = "GCC 4.3.3",
        jitable = False
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
        host_machine = MACHINE_x86,
        host_python_version = (3, 3, 3),
        host_python_compiler = "GCC 4.5.6",
        jitable = True
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
        host_version = (8, 11, 1),
        host_python_compiler = "Clang 3.4.5"
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
        host_arch = ARCH_64,
        host_python_version = (3, 4, 3),
        host_python_compiler = "Clang 3.5.2"
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
        host_python_version = (3, 3, 3),
        host_python_compiler = "MSC 1200.0.0",
        host_posix = False
    ),
    fargs("Windows-post2008Server-6.1.7600",
        platform_machine = "AMD64",
        platform_architecture_bits = 64,
        platform_python_compiler_version_major = 1600, # 1600.0.0
        sys_maxsize = 2**64 - 1,
        host_version = (6, 1, 7600),
        host_machine = MACHINE_x86_64,
        host_arch = ARCH_64,
        host_python_compiler = "MSC 1600.0.0"
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
            if isinstance(env[0], Raises):
                raise env[0].what
            return env[0]
        def _machine():
            if isinstance(env[1], Raises):
                raise env[1].what
            return env[1]
        def _architecture():
            if isinstance(env[2], Raises):
                raise env[2].what
            return env[2]
        def _python_implementation():
            if isinstance(env[3], Raises):
                raise env[3].what
            return env[3]
        def _python_version():
            if isinstance(env[4], Raises):
                raise env[4].what
            return env[4]
        def _python_compiler():
            if isinstance(env[5], Raises):
                raise env[5].what
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

    def test_caching(self):
        with PlatformSysOsModules(_normal_cases[0]):
            Configuration.reset()
            cfg1 = Configuration()
            cfg2 = Configuration()
        self.assertIsNotNone(cfg1)
        self.assertIs(cfg1, cfg2)
    #-def

    def test_platform_cases(self):
        for t in _platform_cases:
            self.do_test(t)
    #-def

    def test_machine_cases(self):
        for t in _machine_cases:
            self.do_test(t)
    #-def

    def test_architecture_cases(self):
        for t in _architecture_cases:
            self.do_test(t)
    #-def

    def test_fixes_cases(self):
        for t in _fixes_cases:
            self.do_test(t)
    #-def

    def test_python_cases(self):
        for t in _python_cases:
            self.do_test(t)
    #-def

    def test_error_cases(self):
        for t in _error_cases:
            self.do_test(t)
    #-def

    def test_set_target_platform_cases(self):
        for t in _set_target_platform_cases:
            self.do_test(t, "jit")
    #-def

    def test_normal_cases(self):
        for t in _normal_cases:
            self.do_test(t)
    #-def

    def do_test(self, env, *args, **kwargs):
        with PlatformSysOsModules(env):
            Configuration.reset()
            cfg = Configuration(*args, **kwargs)
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
        if r[6] is None:
            self.assertIsNone(cfg.host_version())
        else:
            self.assertEqual(cfg.host_version(), r[6])
            self.assertEqual(cfg.host_version().info, r[6].info)
        self.assertEqual(cfg.host_machine(), r[7])
        self.assertEqual(cfg.host_arch(), r[8])
        hpi, hpv = cfg.host_interpreter()
        self.assertEqual(hpi, r[9])
        if r[10] is None:
            self.assertIsNone(hpv, r[10])
        else:
            self.assertEqual(hpv, r[10])
            self.assertEqual(hpv.info, r[10].info)
        self.assertIs(cfg.have_posix(), r[11])
        self.assertIs(cfg.jitable(), r[12])
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConfigurationCase))
    return suite
#-def
