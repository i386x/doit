#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/annotation/types.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-05-28 09:43:05 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
C-like data types for annotating functions.\
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

from doit.support.errors import DoItOverflowError, \
                                DoItUnderflowError, \
                                DoItZeroDivisionError, \
                                DoItTypeError, \
                                doit_assert

from doit.config.config import ARCH_64, Configuration

_is_64bit = Configuration().host_arch() == ARCH_64

_overflow = lambda x: doit_assert(False, x, DoItOverflowError, 2)
_zerodiv = lambda x = "Division by zero": doit_assert(
               False, x, DoItZeroDivisionError, 2
           )
_badtype = lambda x: doit_assert(False, x, DoItTypeError, 2)

class fptr(object):
    """
    """
    __slots__ = []
#-def

class FunPtrCreator(object):
    """
    """
    __slots__ = [ '__rt' ]

    def __init__(self, rt):
        """
        """

        self.__rt = rt
    #-def

    def __call__(self, *ats):
        """
        """

        for at in ats:
            _tassert(isinstance(at, Type), "Argument must be Type instance")
        typemap = self.__rt.typemap
        rt_name = self.__rt.typename()
        ats_name = ", ".join([at.typename() for at in ats])
        funspec = "(%s)(*)(%s)" % (rt_name, ats_name)
        if funcspec in typemap:
            return typemap[funcspec]
        return type(fptr.__name__, (FunPtr, ), dict(
            sfuncspec = funcspec,
            return_t = self.__rt,
            args_t = ats,
            __slots__ = []
        ))
    #-def
#-class

class Type(type):
    """
    """
    typemap = {}
    __slots__ = []

    def __init__(cls, name, bases, attrs, **opts):
        """
        """

        typename = cls.typename()
        if not opts.get('base', False) and typename not in Type.typemap:
            Type.typemap[typename] = cls
    #-def

    def __call__(cls, *args, **kwargs):
        """
        """

        if len(args) == 1 and args[0] is fptr:
            # cls is a return type:
            #   cls(fptr)(t1, t2) creates new function signature
            return FunPtrCreator(cls)
        return super().__call__(*args, **kwargs)
    #-def

    def typename(cls):
        """
        """

        return "<%s id=%d>" % (cls.__name__, id(cls))
    #-def
#-class

class Integral(metaclass = Type, base = True):
    __slots__ = [ '__v' ]

    def __new__(cls, v):
        if cls is Integral:
            _badtype("Integral should not be instantiated")
        return super(Integral, cls).__new__(cls)
    #-def

    def __init__(self, v):
        if not isinstance(v, (int, float, str, bytes, Integral, Real)):
            _badtype("Bad type of value")
        if isinstance(v, (str, bytes)):
            if len(v) != 1:
                _badval("Single character string was expected")
            v = ord(v)
        v = int(v) & self.__class__.BITMASK
        if self.__class__.MIN_VALUE < 0 and v & self.__class__.MSB_MASK:
            v = v - self.__class__.BITMASK - 1
        if v < self.__class__.MIN_VALUE or v > self.__class__.MAX_VALUE:
            _overflow("Value is too large")
        self.__v = v
    #-def

    def __int__(self):
        return self.__v
    #-def

    def __float__(self):
        return float(self.__v)
    #-def

    # Binary ops support:

    def __add__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(self.__add_impl(a, b))
    #-def

    __radd__ = __add__

    def __sub__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(self.__sub_impl(a, b))
    #-def

    def __rsub__(self, other):
        b = self.__v
        a = int(type(self)(other))

        return type(self)(self.__sub_impl(a, b))
    #-def

    def __mul__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(self.__mul_impl(a, b))
    #-def

    __rmul__ = __mul__

    def __truediv__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(self.__div_impl(a, b))
    #-def

    def __rtruediv__(self, other):
        b = self.__v
        a = int(type(self)(other))

        return type(self)(self.__div_impl(a, b))
    #-def

    def __floordiv__(self, other):
        return NotImplemented
    #-def

    __rfloordiv__ = __floordiv__

    def __mod__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(self.__mod_impl(a, b))
    #-def

    def __rmod__(self, other):
        b = self.__v
        a = int(type(self)(other))

        return type(self)(self.__mod_impl(a, b))
    #-def

    def __divmod__(self, other):
        return NotImplemented
    #-def

    __rdivmod__ = __divmod__

    def __pow__(self, other):
        return NotImplemented
    #-def

    __rpow__ = __pow__

    def __lshift__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(self.__lshift_impl(a, b))
    #-def

    def __rlshift__(self, other):
        b = self.__v
        a = int(type(self)(other))

        return type(self)(self.__lshift_impl(a, b))
    #-def

    def __rshift__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(self.__rshift_impl(a, b))
    #-def

    def __rrshift__(self, other):
        b = self.__v
        a = int(type(self)(other))

        return type(self)(self.__rshift_impl(a, b))
    #-def

    def __and__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(a & b)
    #-def

    __rand__ = __and__

    def __or__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(a | b)
    #-def

    __ror__ = __or__

    def __xor__(self, other):
        a = self.__v
        b = int(type(self)(other))

        return type(self)(a ^ b)
    #-def

    __rxor__ = __xor__

    # In-place ops:

    def __iadd__(self, other):
        self.__v = self.__add_impl(self.__v, int(type(self)(other)))
        return self
    #-def

    def __isub__(self, other):
        self.__v = self.__sub_impl(self.__v, int(type(self)(other)))
        return self
    #-def

    def __imul__(self, other):
        self.__v = self.__mul_impl(self.__v, int(type(self)(other)))
        return self
    #-def

    def __itruediv__(self, other):
        self.__v = self.__div_impl(self.__v, int(type(self)(other)))
        return self
    #-def

    def __imod__(self, other):
        self.__v = self.__mod_impl(self.__v, int(type(self)(other)))
        return self
    #-def

    def __ilshift__(self, other):
        self.__v = self.__lshift_impl(self.__v, int(type(self)(other)))
        return self
    #-def

    def __irshift__(self, other):
        self.__v = self.__rshift_impl(self.__v, int(type(self)(other)))
        return self
    #-def

    def __iand__(self, other):
        self.__v &= int(type(self)(other))
        return self
    #-def

    def __ixor__(self, other):
        self.__v ^= int(type(self)(other))
        return self
    #-def

    def __ior__(self, other):
        self.__v |= int(type(self)(other))
        return self
    #-def

    # Unary ops:

    def __neg__(self):
        return type(self)(-self.__v)
    #-def

    def __pos__(self):
        return type(self)(self.__v)
    #-def

    def __invert__(self):
        return type(self)(~self.__v)
    #-def

    # Private part:

    @staticmethod
    def __add_impl(a, b):
        if a > 0 and b > 0 and a > self.__class__.MAX_VALUE - b \
        or a < 0 and b < 0 and a < self.__class__.MIN_VALUE - b:
            _overflow("%d + %d overflowed" % (a, b))
        return a + b
    #-def

    @staticmethod
    def __sub_impl(a, b):
        if a > 0 and b < 0 and a > self.__class__.MAX_VALUE + b \
        or a < 0 and b > 0 and a < self.__class__.MIN_VALUE + b:
            _overflow("%d - %d overflowed" % (a, b))
        return a - b
    #-def

    @staticmethod
    def __mul_impl(a, b):
        if a == 0 or b == 0:
            return 0
        elif a < 0 and b > 0 and a < self.__class__.MIN_VALUE / b \
        or a > 0 and b < 0 and a > self.__class__.MIN_VALUE / b \
        or a < 0 and b < 0 and a < self.__class__.MAX_VALUE / b \
        or a > 0 and b > 0 and a > self.__class__.MAX_VALUE / b:
            _overflow("%d * %d overflowed" % (a, b))
        return a*b
    #-def

    @staticmethod
    def __div_impl(a, b):
        if b == 0:
            _zerodiv()
        return a // b
    #-def

    @staticmethod
    def __mod_impl(a, b):
        if b == 0:
            _zerodiv()
        return a % b
    #-def

    @staticmethod
    def __lshift_impl(a, b):
        if b < 0:
            _badval("Negative shift count")
        return (a << b) & self.__class__.BITMASK
    #-def

    @staticmethod
    def __rshift_impl(a, b):
        if b < 0:
            _badval("Negative shift count")
        return a >> b
    #-def
#-class

class Real(metaclass = Type, base = True):
    __slots__ = [ '__v' ]

    def __new__(cls, v):
        if cls is Real:
            _badtype("Real should not be instantiated")
        return super(Real, cls).__new__(cls)
    #-def

    def __init__(self, v):
        self.__v = self.pack(v)
    #-def
#-class

class Ptr(metaclass = Type, base = True):
    __slots__ = [ '__p' ]

    def __init__(self, p):
        """
        """

        _tassert(type(p) is self.__class__.underlying_t,
            "type(p) is not %s" % self.__class__.underlying_t.typename()
        )
        self.__p = p
    #-def
#-class

class FunPtr(metaclass = Type, base = True):
    __slots__ = [ '__f' ]

    def __init__(self, f):
        """
        """

        if not hasattr(f, '__call__') or not hasattr(f, '__annotations__') \
        or not hasattr(f, '__code__'):
            _badtype("Function or method was expected")
        _assert(f.__code__.co_argcount == len(f.__code__.co_varnames),
            "co_argcount != len(co_varnames)"
        )
        _tassert('return' in f.__annotations__,
            "Function or method has no return type"
        )
        _tassert(f.__annotations__['return'] is self.__class__.return_t,
            "%s has different signature" % f.__name__
        )
        _tassert(f.__code__.co_argcount == len(self.__class__.args_t),
            "%s has different signature" % f.__name__
        )
        for i, v in enumerate(f.__code__.co_varnames):
            _tassert(v in f.__annotations__, "%s has no type" % v)
            _tassert(f.__annotations__[v] is self.__class__.args_t[i],
                "%s has different signature" % f.__name__
            )
        self.__f = f
    #-def

    @classmethod
    def typename(cls):
        """
        """

        return cls.sfuncspec
    #-def
#-class

def make_integral_type(name, bits, signed):
    """
    """

    return type(name, (Integral, ), dict(
        MIN_VALUE = -(1 << (bits - 1)) if signed else 0,
        MAX_VALUE = (1 << (bits - 1)) - 1 if signed else (1 << bits) - 1,
        BITS = bits,
        BITMASK = (1 << bits) - 1,
        LSB_MASK = 1,
        MSB_MASK = 1 << (bits - 1),
        SIZE = (bits >> 3) + 1 if bits & 7 else bits >> 3,
        __slots__ = []
    ))
#-def

def make_real_type(name, bits):
    """
    """

    _tassert(bits in [32, 64],
        "Only sigle- and double-precision floating point types are supported"
    )
    return type(name, (Real, ), dict(
        BITS = bits,
        SIZE = (bits >> 3) + 1 if bits & 7 else bits >> 3,
        __slots__ = []
    ))
#-def

def ptr(t):
    """
    """

    _tassert(isinstance(t, Type), "t is not a Type instance")
    typename = "*%s" % t.typename()
    if typename in Type.typemap:
        return Type.typemap[typename]
    return type('ptr', (Ptr, ), dict(
        underlying_t = t,
        __slots__ = []
    ))
#-def

char_t = make_integral_type('char_t', 8, True)
short_t = make_integral_type('short_t', 16, True)
int_t = make_integral_type('int_t', 32, True)
long_t = make_integral_type('long_t', 64 if _is_64bit else 32, True)
longlong_t = make_integral_type('longlong_t', 64, True)
wchar_t = make_integral_type('wchar_t', 32, True)

int8_t = make_integral_type('int8_t', 8, True)
int16_t = make_integral_type('int16_t', 16, True)
int32_t = make_integral_type('int32_t', 32, True)
int64_t = make_integral_type('int64_t', 64, True)

uchar_t = make_integral_type('uchar_t', 8, False)
ushort_t = make_integral_type('ushort_t', 16, False)
uint_t = make_integral_type('uint_t', 32, False)
ulong_t = make_integral_type('ulong_t', 64 if _is_64bit else 32, False)
ulonglong_t = make_integral_type('ulonglong_t', 64, False)
uwchar_t = make_integral_type('uwchar_t', 32, False)

uint8_t = make_integral_type('uint8_t', 8, False)
uint16_t = make_integral_type('uint16_t', 16, False)
uint32_t = make_integral_type('uint32_t', 32, False)
uint64_t = make_integral_type('uint64_t', 64, False)

size_t = make_integral_type('size_t', 64 if _is_64bit else 32, False)

float_t = make_real_type('float_t', 32)
double_t = make_real_type('double_t', 64)

class Scanner(Class):
    __slots__ = [ ]

    def __init__(self):
        self.pin = Stream(char_t)(null)

    def skip(self, s: stream):
        while self.space(s) or self.comment(s):
            pass

    def space(self, s):
        # TEST_SET
        if not s.test(SPACE):
            return False
        # NEXT_CHAR
        s.next()
        return True

    def comment(self, s):
        # TRYMATCH
        if not s.trymatch("/*"):
            return False
        # TEST
        while not s.test("*/") and s.peek:
            s.next()
        # MATCH
        s.match("*/")
        return True

    def scan(self, s: Stream(char_t)):
        self.skip(s)
        cat = s.testcat()
        if cat == EOF:
            return Null
        if cat == LETTER:
            return self.scan_word(s)
        elif cat == DIGIT:
            return self.scan_number(s)
        else:
            return INVALID
