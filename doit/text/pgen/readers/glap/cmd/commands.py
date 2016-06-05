#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/text/pgen/readers/glap/cmd/commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-14 15:36:02 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Possible commands to be processed by command processor.\
"""

__license__ = """\
Copyright (c) 2014 - 2016 Jiří Kučera.

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

from doit.text.pgen.readers.glap.cmd.errors import \
    CommandError

from doit.text.pgen.readers.glap.cmd.runtime import \
    Pair, \
    List, \
    HashMap

NumericTypes = (int, float)
SequenceTypes = (str, Pair, list)
FixedLengthSequenceTypes = (Pair,)
VariableLengthSequenceTypes = (str, list)
CollectionTypes = (str, Pair, list, dict)

class Location(tuple):
    """
    """
    __slots__ = []

    def __new__(cls, file = None, line = -1, column = -1):
        """
        """

        return super(Location, cls).__new__(cls, (file, line, column))
    #-def

    def __init__(self, file = None, line = -1, column = -1):
        """
        """

        tuple.__init__(self)
    #-def

    def file(self):
        """
        """

        return self[0]
    #-def

    def line(self):
        """
        """

        return self[1]
    #-def

    def column(self):
        """
        """

        return self[2]
    #-def

    def __str__(self):
        """
        """

        f, l, c = self
        if f is None or l < 0 or c < 0:
            return "(internal)"
        return "at [\"%s\":%d:%d]" % self
    #-def
#-class

class Finalizer(object):
    """
    """
    __slots__ = [ 'cmd' ]

    def __init__(self, cmd):
        """
        """

        self.cmd = cmd
    #-def

    def __call__(self, processor):
        """
        """

        self.cmd.leave(processor)
    #-def
#-class

class Command(object):
    """
    """
    __slots__ = [ 'name', 'location', 'env' ]

    def __init__(self):
        """
        """

        self.name = self.__class__.__name__.lower()
        self.location = Location()
        self.env = None
    #-def

    def isfunc(self):
        """
        """

        return False
    #-def

    def set_location(self, file = None, line = -1, column = -1):
        """
        """

        self.location = Location(file, line, column)
    #-def

    def __str__(self):
        """
        """

        return "\"%s\" %s" % (self.name, self.location)
    #-def

    def help(self, processor):
        """
        """

        pass
    #-def

    def enter(self, processor):
        """
        """

        pass
    #-def

    def expand(self, processor):
        """
        """

        pass
    #-def

    def leave(self, processor):
        """
        """

        pass
    #-def

    def pushacc(self, processor):
        """
        """

        processor.pushacc()
    #-def

    def find_exception_handler(self, e):
        """
        """

        return None
    #-def
#-class

class Trackable(Command):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Command.__init__(self)
    #-def

    def enter(self, processor):
        """
        """

        self.env = processor.getenv()
        processor.pushcmd(self)
    #-def

    def leave(self, processor):
        """
        """

        processor.popcmd(self)
        self.env = None
    #-def
#-class

class SetLocal(Trackable):
    """
    """
    __slots__ = [ 'varname', 'value' ]

    def __init__(self, name, value):
        """
        """

        Trackable.__init__(self)
        self.varname = name
        self.value = value
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            self.enter, self.value, self.do_setlocal, Finalizer(self)
        )
    #-def

    def do_setlocal(self, processor):
        """
        """

        self.env.setvar(self.varname, processor.acc())
    #-def
#-class

class GetLocal(Trackable):
    """
    """
    __slots__ = [ 'varname' ]

    def __init__(self, name):
        """
        """

        Trackable.__init__(self)
        self.varname = name
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            self.enter, self.do_getlocal, Finalizer(self)
        )
    #-def

    def do_getlocal(self, processor):
        """
        """

        processor.setacc(self.env.getvar(self.varname))
    #-def
#-class

class Operation(Trackable):
    """
    """
    OP_TAB = {
        # Arithmetic operations:
        'add': dict(
            types = [(NumericTypes, NumericTypes)],
            operation = (lambda a, b: a + b)
        ),
        'sub': dict(
            types = [(NumericTypes, NumericTypes)],
            operation = (lambda a, b: a - b)
        ),
        'mul': dict(
            types = [(NumericTypes, NumericTypes)],
            operation = (lambda a, b: a * b)
        ),
        'div': dict(
            types = [(NumericTypes, NumericTypes)],
            constraints = (lambda p, a, b: \
                (True, None, "") if b != 0 else \
                (False, p.ValueError, "Second operand must be non-zero")
            ),
            operation = (lambda a, b: a / b)
        ),
        'mod': dict(
            types = [(NumericTypes, NumericTypes)],
            constraints = (lambda p, a, b: \
                (True, None, "") if b != 0 else \
                (False, p.ValueError, "Second operand must be non-zero")
            ),
            operation = (lambda a, b: a % b)
        ),
        'neg': dict(
            types = [(NumericTypes,)],
            operation = (lambda a: -a)
        ),
        # Bitwise operations:
        'bitand': dict(
            types = [(int, int)],
            operation = (lambda a, b: a & b)
        ),
        'bitor': dict(
            types = [(int, int)],
            operation = (lambda a, b: a | b)
        ),
        'bitxor': dict(
            types = [(int, int)],
            operation = (lambda a, b: a ^ b)
        ),
        'shiftl': dict(
            types = [(int, int)],
            constraints = (lambda p, a, b: \
                (True, None, "") if b >= 0 else \
                (False, p.ValueError,
                    "Second operand must be a non-negative integer"
                )
            ),
            operation = (lambda a, b: a << b)
        ),
        'shiftr': dict(
            types = [(int, int)],
            constraints = (lambda p, a, b: \
                (True, None, "") if b >= 0 else \
                (False, p.ValueError,
                    "Second operand must be a non-negative integer"
                )
            ),
            operation = (lambda a, b: a >> b)
        ),
        'inv': dict(
            types = [(int,)],
            operation = (lambda a: ~a)
        ),
        # Comparison operations:
        'lt': dict(
            types = [(NumericTypes, NumericTypes), (str, str)],
            operation = (lambda a, b: a < b)
        ),
        'gt': dict(
            types = [(NumericTypes, NumericTypes), (str, str)],
            operation = (lambda a, b: a > b)
        ),
        'le': dict(
            types = [(NumericTypes, NumericTypes), (str, str)],
            operation = (lambda a, b: a <= b)
        ),
        'ge': dict(
            types = [(NumericTypes, NumericTypes), (str, str)],
            operation = (lambda a, b: a >= b)
        ),
        'eq': dict(
            types = [(object, object)],
            operation = (lambda a, b: a == b)
        ),
        'ne': dict(
            types = [(object, object)],
            operation = (lambda a, b: a != b)
        ),
        'is': dict(
            types = [(object, object)],
            operation = (lambda a, b: a is b)
        ),
        # Logic operations:
        'and': dict(
            types = [(bool, bool)],
            conversions = (lambda p, a: \
                False if a is p.Null else a
            ),
            operation = (lambda a, b: a and b)
        ),
        'or': dict(
            types = [(bool, bool)],
            conversions = (lambda p, a: \
                False if a is p.Null else a
            ),
            operation = (lambda a, b: a or b)
        ),
        'not': dict(
            types = [(bool,)],
            conversions = (lambda p, a: \
                False if a is p.Null else a
            ),
            operation = (lambda a: not a)
        ),
        # Collection operations:
        # - constructive:
        'copy': dict(
            types = [(CollectionTypes,)],
            operation = (lambda a: \
                a.__class__(*(a if isinstance(a, Pair) else [a]))
            )
        ),
        'slice': dict(
            types = [(VariableLengthSequenceTypes, int, int)],
            operation = (lambda a, b, c: a.__class__(a[b:c]))
        ),
        'concat': dict(
            types = [(str, str)],
            operation = (lambda a, b: "%s%s" % (a, b))
        ),
        'join': dict(
            types = [(list, list)],
            operation = (lambda a, b: List(a + b))
        ),
        'merge': dict(
            types = [(dict, dict)],
            operation = (lambda a, b: HashMap.merge(a, b))
        ),
        # - informative:
        'strlen': dict(
            types = [(str,)],
            operation = (lambda a: len(a))
        ),
        'size': dict(
            types = [(CollectionTypes,)],
            operation = (lambda a: len(a))
        ),
        'empty': dict(
            types = [(CollectionTypes,)],
            operation = (lambda a: len(a) == 0)
        ),
        'contains': dict(
            types = [(CollectionTypes, object)],
            constraints = (lambda p, a, b: \
                (True, None, "") \
                if (isinstance(a, str) and isinstance(b, str)) \
                or not isinstance(a, str) \
                else (False, p.TypeError,
                    "Bad type of second operand (string was expected)"
                )
            ),
            operation = (lambda a, b: b in a)
        ),
        'count': dict(
            types = [(SequenceTypes, object)],
            constraints = (lambda p, a, b: \
                (True, None, "") \
                if (isinstance(a, str) and isinstance(b, str)) \
                or not isinstance(a, str) \
                else (False, p.TypeError,
                    "Bad type of second operand (string was expected)"
                )
            ),
            operation = (lambda a, b: a.count(b))
        ),
        'isdigit': dict(
            types = [(str,)],
            operation = (lambda a: a[0].isdigit() if a != "" else False)
        ),
        'isupper': dict(
            types = [(str,)],
            operation = (lambda a: a[0].isupper() if a != "" else False)
        ),
        'islower': dict(
            types = [(str,)],
            operation = (lambda a: a[0].islower() if a != "" else False)
        ),
        'isalpha': dict(
            types = [(str,)],
            operation = (lambda a: a[0].isalpha() if a != "" else False)
        ),
        'isletter': dict(
            types = [(str,)],
            operation = (lambda a: \
                a[0].isalpha() or a[0] == "_" if a != "" else False
            )
        ),
        'isalnum': dict(
            types = [(str,)],
            operation = (lambda a: a[0].isalnum() if a != "" else False)
        ),
        'isword': dict(
            types = [(str,)],
            operation = (lambda a: \
                a[0].isalnum() or a[0] == "_" if a != "" else False
            )
        ),
        'keys': dict(
            types = [(dict,)],
            operation = (lambda a: List(a.keys()))
        ),
        'values': dict(
            types = [(dict,)],
            operation = (lambda a: List(a.values()))
        ),
        # - elementwise:
        'first': dict(
            types = [(Pair,)],
            operation = (lambda a: a[0])
        ),
        'second': dict(
            types = [(Pair,)],
            operation = (lambda a: a[1])
        ),
        'getitem': dict(
            types = [(CollectionTypes, object)],
            constraints = (lambda p, a, b: \
                (True, None, "") if isinstance(a, dict) and b in a else \
                (True, None, "") if isinstance(a, SequenceTypes) \
                                 and isinstance(b, int) \
                                 and 0 <= b and b < len(a) else \
                (False, p.KeyError if isinstance(a, dict) else p.IndexError, \
                    "%r is not a valid key into the hashmap" % b \
                        if isinstance(a, dict) else \
                    "%r is not a valid index into the sequence" % b
                )
            ),
            operation = (lambda a, b: a[b])
        ),
        # - searching:
        'substr': dict(
            types = [(str, str)],
            operation = (lambda a, b: a.find(b))
        ),
        'find': dict(
            types = [(str, str, int, int)],
            operation = (lambda a, b, c, d: a.find(b, c, d))
        ),
        'rfind': dict(
            types = [(str, str, int, int)],
            operation = (lambda a, b, c, d: a.rfind(b, c, d))
        ),
        # - adjustments:
        'lstrip': dict(
            types = [(str,)],
            operation = (lambda a: a.lstrip())
        ),
        'rstrip': dict(
            types = [(str,)],
            operation = (lambda a: a.rstrip())
        ),
        'strip': dict(
            types = [(str,)],
            operation = (lambda a: a.strip())
        ),
        'toupper': dict(
            types = [(str,)],
            operation = (lambda a: a.upper())
        ),
        'tolower': dict(
            types = [(str,)],
            operation = (lambda a: a.lower())
        ),
        'subst': dict(
            types = [(str, str, str)],
            operation = (lambda a, b, c: a.replace(b, c))
        ),
        'trans': dict(
            types = [(str, dict)],
            operation = (lambda a, b: ''.join([b.get(x, x) for x in a]))
        ),
        'sort': dict(
            types = [(list,)],
            operation = (lambda a: (lambda l: l.sort() or l)(List(a)))
        ),
        'reverse': dict(
            types = [(list,)],
            operation = (lambda a: (lambda l: l.reverse() or l)(List(a)))
        ),
        'unique': dict(
            types = [(list,)],
            operation = (lambda a: List.unique(a))
        ),
        'split': dict(
            types = [(str, str)],
            operation = (lambda a, b: List(a.split(b)))
        )
    }
    __slots__ = [ 'operands' ]

    def __init__(self, *operands):
        """
        """

        Trackable.__init__(self)
        self.operands = operands
    #-def

    def expand(self, processor):
        """
        """

        code = [self.enter]
        for o in self.operands:
            code.extend([o, self.pushacc])
        code.extend([self.do_op, Finalizer(self)])
        processor.insertcode(*code)
    #-def

    def do_op(self, processor):
        """
        """

        # 1) Test whether the operation is defined:
        op_tab = self.__class__.OP_TAB
        if self.name not in op_tab:
            raise CommandError(processor.NameError,
                "Undefined operation '%s'" % self.name
            )

        # 2) Load operands:
        args = []
        for _ in self.operands:
            args.append(processor.popval())
        args.reverse()
        nargs = len(args)

        # 3) Load operation specification:
        op_spec = op_tab[self.name]

        # 4) Check if the number of operands coincides with the arity of the
        #    operator:
        types = op_spec['types']
        arity = len(types[0])
        if arity != nargs:
            raise CommandError(processor.TypeError,
                "%s: Exactly %d operand%s %s needed (%d %s given)" \
                % (
                    self.name,
                    arity,
                    "s" if arity != 1 else "",
                    "are" if arity != 1 else "is",
                    nargs,
                    "were" if nargs != 1 else "was"
                )
            )

        # 5) Do the occasional conversions:
        if 'conversions' in op_spec:
            conversions = op_spec['conversions']
            for i in range(arity):
                args[i] = conversions(processor, args[i])

        # 6) Check the types of operands:
        type_error = False
        i = 0
        for typespec in types:
            type_error = False
            for j in range(arity):
                if not isinstance(args[j], typespec[j]):
                    type_error = True
                    i = j
                    break
            if not type_error:
                break
        if type_error:
            raise CommandError(processor.TypeError,
                "%s: Bad type of the %d%s operand" \
                % (
                    self.name,
                    i + 1,
                    "st" if (i % 10) == 0 and (i % 100) != 10 else \
                    "nd" if (i % 10) == 1 and (i % 100) != 11 else \
                    "rd" if (i % 10) == 2 and (i % 100) != 12 else \
                    "th"
                )
            )

        # 7) Test the occasional constraints:
        r, e, m = op_spec.get('constraints', (lambda p, *x: (True, None, "")))(
            processor, *args
        )
        if not r:
            raise CommandError(e, "%s: %s" % (self.name, m))

        # 8) Do the operation:
        processor.setacc(op_spec['operation'](*args))
    #-def
#-class

class Add(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Sub(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Mul(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Div(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Mod(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Neg(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class BitAnd(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class BitOr(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class BitXor(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class ShiftL(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class ShiftR(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Inv(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Lt(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Gt(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Le(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Ge(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Eq(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Ne(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Is(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class And(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Or(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Not(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Copy(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Slice(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c):
        """
        """

        Operation.__init__(self, a, b, c)
    #-def
#-class

class Concat(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Join(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Merge(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Strlen(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Size(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Empty(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Contains(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Count(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class IsDigit(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsUpper(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsLower(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsAlpha(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsLetter(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsAlnum(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class IsWord(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Keys(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Values(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class First(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Second(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class GetItem(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Substr(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Find(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c, d):
        """
        """

        Operation.__init__(self, a, b, c, d)
    #-def
#-class

class RFind(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c, d):
        """
        """

        Operation.__init__(self, a, b, c, d)
    #-def
#-class

class LStrip(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class RStrip(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Strip(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class ToUpper(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class ToLower(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Subst(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b, c):
        """
        """

        Operation.__init__(self, a, b, c)
    #-def
#-class

class Trans(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class Sort(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Reverse(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Unique(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a):
        """
        """

        Operation.__init__(self, a)
    #-def
#-class

class Split(Operation):
    """
    """
    __slots__ = []

    def __init__(self, a, b):
        """
        """

        Operation.__init__(self, a, b)
    #-def
#-class

class ToBool(Operation):
    pass

class ToInt(Operation):
    pass

class ToFlt(Operation):
    pass

class ToStr(Operation):
    pass

class ToPair(Operation):
    pass

class ToList(Operation):
    pass

class ToHash(Operation):
    pass

class All(Operation):
    pass

class Any(Operation):
    pass

class Map(Operation):
    pass

class Filter(Operation):
    pass

class Block(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, *commands):
        """
        """

        Trackable.__init__(self)
        self.commands = commands
    #-def

    def enter(self, processor):
        """
        """

        self.env = processor.newenv()
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            *((self.enter,) + self.commands + (Finalizer(self),))
        )
    #-def
#-class

class If(Trackable):
    """
    """
    __slots__ = [ 'c', 't', 'e' ]

    def __init__(self, c, t, e):
        """
        """

        Trackable.__init__(self)
        self.c = c
        self.t = t
        self.e = e
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            self.enter, self.c, self.pushacc, self.do_if, Finalizer(self)
        )
    #-def

    def do_if(self, processor):
        """
        """

        processor.insertcode(
            *(self.t if processor.popval() else self.e)
        )
    #-def
#-class
 
class Foreach(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, var, itexp, body):
        """
        """

        Trackable.__init__(self)
        self.var = var
        self.itexp = itexp
        self.body = body
        self.iterator = None
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            self.enter, self.itexp, self.do_for, Finalizer(self)
        )
    #-def

    def do_for(self, processor):
        """
        """

        if not isinstance(processor.acc(), Iterable):
            raise CmdTypeError("Object must be iterable")
        self.iterator = processor.acc().iterator()
        self.iterator.reset()
        processor.insertcode(self.do_loop)
    #-def

    def do_loop(self, processor):
        """
        """

        x = self.iterator.next()
        if x is self.iterator:
            return
        processor.pushval(x)
        processor.insertcode(
            *((self.do_setvar,) + self.body + (self.do_loop,))
        )
    #-def

    def do_setvar(self, processor):
        """
        """

        self.env.setvar(self.var, processor.popval())
    #-def

    def leave(self, processor):
        """
        """

        self.iterator.reset()
        self.iterator = None
        Trackable.leave(self, processor)
    #-def
#-class

class Closure(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, name, bvars, args, body, outer):
        """
        """

        Trackable.__init__(self)
        self.name = name
        self.bvars = bvars
        self.args = args
        self.body = body
        self.outer = outer
    #-def

    def isfunc(self):
        """
        """

        return True
    #-def

    def enter(self, processor):
        """
        """

        self.env = Environment(self.outer)
        for bvar in self.bvars:
            self.env.setvar(bvar, Null())
        for argname in self.args:
            self.env.setvar(argname, self.args[argname])
        processor.pushcmd(self)
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(
            *((self.enter,) + self.body + (Finalizer(self),))
        )
    #-def
#-class

class Call(Command):
    """
    """
    __slots__ = []

    def __init__(self, name, *args):
        """
        """

        Command.__init__(self)
        self.name = value(name)
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        proc = processor.getenv().getvar(self.name)
        if not isinstance(proc, ProcedureTemplate):
            procedure.insertcode(CmdTypeError(
                "%s must be callable" % self.name
            ))
            return
        _, params, _, _ = proc
        nparams = len(params)
        nargs = len(self.args)
        if nargs != nparams:
            processor.insertcode(CmdTypeError(
                "%s takes %d argument%s but %d w%s given" \
                % (
                    self.name,
                    nparams,
                    "" if nparams == 1 else "s",
                    nargs,
                    "as" if nargs == 1 else "ere"
                )
            ))
            return
        processor.pushval(Value({}))
        i = 0
        for arg in self.args:
            processor.insertcode(
                arg, self.pushacc, Value(params[i]), self.pushacc, self.do_arg
            )
            i += 1
        processor.insertcode(
            Value((self.name, proc)), self.pushacc, self.do_call
        )
    #-def

    def do_arg(self, processor):
        """
        """

        name = processor.popval().value
        value = processor.popval()
        processor.topval().value[name] = value
    #-def

    def do_call(self, processor):
        """
        """

        name, proc = processor.popval().value
        args = processor.popval().value
        bvars, _, body, outer = proc
        processor.insertcode(Closure(name, bvars, args, body, outer))
    #-def
#-class

class SetItem(Trackable):
    pass

class DelItem(Trackable):
    pass

class Remove(Trackable):
    pass

class RemoveAll(Trackable):
    pass

class Each(Trackable):
    pass

class Visit(Trackable):
    pass

class Print(Trackable):
    """
    """
    __slots__ = []

    def __init__(self, *args):
        """
        """

        Trackable.__init__(self)
        self.args = args
    #-def

    def expand(self, processor):
        """
        """

        processor.insertcode(self.enter)
        for arg in self.args:
            processor.insertcode(arg, self.do_print_arg)
        processor.insertcode(Finalizer(self))
    #-def

    def do_print_arg(self, processor):
        """
        """

        processor.write(self.__class__.__name__.upper(),
            "%s" % processor.acc()
        )
    #-def
#-class
