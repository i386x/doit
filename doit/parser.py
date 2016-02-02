#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/parser.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-06-21 ‏‎12:24:47 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! parser and lexer.\
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

class DoItLexerGrammar(Grammar):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        Grammar.__init__(self)

        emit = self.__emit

        self['start']      = V('COMMENT')
                           | V('WHITESPACE')
                           | V('ID')
                           | V('INT')
                           | V('BINT')
                           | V('OINT')
                           | V('XINT')
                           | V('FLOAT')
                           | V('CHAR')
                           | V('STRING')

        self['COMMENT']    = S('#') + (~S('\n'))['*'] + S('\n')['?']

        self['ID']         = V('LETTER_') + V('ALNUM_')['*']
                             + emit('ID', '$0')

        self['INT']        = V('INT_PART') + emit('INT', '$1', DEC)
        self['BINT']       = -S('0') + -(S('B') | S('b'))
                             + V('BIT')['+']
                             + emit('INT', '$0', BIN)
        self['OINT']       = -S('0') + V('ODIGIT')['+']
                             + emit('INT', '$0', OCT)
        self['XINT']       = -S('0') + -(S('X') | S('x'))
                             + V('XDIGIT')['+']
                             + emit('INT', '$0', HEX)
        self['FLOAT']      = V('INT_PART') + V('FLOAT_PART')
                             + emit('FLOAT', '$1', 'frac', 'sign', 'exp')
        self['INT_PART']   = S('0')
                           | V('NZ_DIGIT') + V('DIGIT')['*']
        self['FLOAT_PART'] = V('EXP_PART')
                           | V('FRAC_PART') + V('EXP_PART')['?']
        self['FRAC_PART']  = -S('.') + V('DIGIT')['+'] % 'frac'
        self['EXP_PART']   = -(S('E') | S('e'))
                             + (S('+') | S('-'))['?'] % 'sign'
                             + V('DIGIT')['+'] % 'exp'

        self['CHAR']       = -S('\'') + V('SYMBOL') + -S('\'')
                             + emit('CHAR', '$1')

        self['ALNUM_']     = A(S('_') | V('ALNUM'))
        self['ALNUM']      = A(V('DIGIT') | V('LETTER'))
        self['LETTER_']    = A(S('_') | V('LETTER'))
        self['LETTER']     = A(V('UPPER') | V('LOWER'))
        self['UPPER']      = A(S('A') - S('Z'))
        self['LOWER']      = A(S('a') - S('z'))
        self['NZ_DIGIT']   = A(S('1') - S('9'))
        self['DIGIT']      = A(S('0') - S('9'))
        self['SYMBOL']     = V('ESCAPE')
    #-def

    def __emit(self, name, *values):
        """
        """

        name = Id(name)
        values = [ Id(v) for v in values ]
        Token = Id('Token')

        return Action(
            Return(Token(name, *values))
        )
    #-def
#-class

class DoItParser(Grammar):
    __slots__ = []

    def __init__(self):
        self['start'] = Var('')


#==============================================================================

class Lexer(object):
    """Base class for lexical analyzer.
    """
    __slots__ = [ 'context', 'current', 'last' ]

    def __init__(self, context):
        """Lexer(context) -> instance of Lexer

        Constructor. Initialize lexer with given context.
        """

        self.context = context
        self.current = None
        self.last = None
    #-def

    def peek(self):
        """peek() -> instance of Token

        Return the current token at input or None if end was reached.
        """

        if self.current is not None:
            return self.current
        self.current = self.scan()
        return self.current
    #-def

    def next(self):
        """next()

        Move to the next token keeping the last one. Recommendation: call
        next() after semantic action to ensure that next input will be read by
        updated lexer.
        """

        if self.current is not None:
            self.last = self.current
        self.current = self.scan()
    #-def

    def scan(self):
        """scan() -> instance of Token

        User defined scanning routine. Return the next token from input or None
        if end of input was reached.
        """

        raise NotImplementedError
    #-def
#-class

class Parser(object):
    """Recursive descent parser base class.
    """
    __slots__ = [ 'lexer' ]

    def __init__(self, lexer):
        """Parser(lexer) -> instance of Parser

        Constructor.
        """

        self.lexer = lexer
    #-def

    def start(self):
        """start() -> instance of Command

        Entry point of parsing.
        """

        raise NotImplementedError
    #-def
#-class

def update_word_lexer(word, words, reobj):
    """update_word_lexer(word, words, reobj) -> instance of SRE_Pattern

    If word is not in words, update words and regular expression object, which
    match word from words.
    """

    if word in words:
        return reobj
    words.append(word)
    words.sort(key = len, reverse = True)
    return re.compile(
        '|'.join([re.escape(x) for x in ws])
    )
#-def

@patch_class
class DoItLexer(Lexer):
    """DoIt lexical analyzer.
    """
    __slots__ = [
        '__upreops_list',
        '__upreops_re',
        '__upreops_parsers',
        '__upostops_list',
        '__upostops_re',
        '__upostops_parsers',
        '__bopgroups_list',
        '__bopgroups_assoc',
        '__bopgroups_prec',
        '__binops',
        '__binops_parsers',
        '__braces',
        '__statements'
    ]
    GRP_PREFIX_NAME = "prefix"
    GRP_POSTFIX_NAME = "postfix"
    PRIVATE_GRP_NAMES = [GRP_PREFIX_NAME, GRP_POSTFIX_NAME]

    def __init__(self, context):
        """DoItLexer(context) -> instance of Lexer

        Constructor.
        """

        Lexer.__init__(self, context)
        # Operators:
        # - unary prefix:
        self.__upreops_list = []
        self.__upreops_re = None
        self.__upreops_parsers = {}
        # - unary postfix:
        self.__upostops_list = []
        self.__upostops_re = None
        self.__upostops_parsers = {}
        # - binary:
        self.__bopgroups_list = []
        self.__bopgroups_assoc = {}
        self.__bopgroups_prec = {}
        self.__binops = {}
        self.__binops_parsers = {}
        # Braces:
        self.__braces = {}
        # Statements:
        self.__statements = []

        # Builtin operator groups:
        self.define_binary_operator_group(
          "comma", Operator.Left, Precedence.Highest
        )
        self.define_binary_operator_group(
          "assign", Operator.Right, Precedence.Highest
        )
        self.define_binary_operator_group(
          "logor", Operator.Left, Precedence.Highest
        )
        self.define_binary_operator_group(
          "logand", Operator.Left, Precedence.Highest
        )
        self.define_binary_operator_group(
          "bitor", Operator.Left, Precedence.Highest
        )
        self.define_binary_operator_group(
          "bitxor", Operator.Left, Precedence.Highest
        )
        self.define_binary_operator_group(
          "bitand", Operator.Left, Precedence.Highest
        )
        self.define_binary_operator_group(
          "rel", Operator.NoAssoc, Precedence.Highest
        )
        self.define_binary_operator_group(
          "bshift", Operator.Left, Precedence.Highest
        )
        self.define_binary_operator_group(
          "add", Operator.Left, Precedence.Highest
        )
        self.define_binary_operator_group(
          "mul", Operator.Left, Precedence.Highest
        )
        # Builtin operators:
        self.define_operator('++', "postfix")
        self.define_operator('--', "postfix")
        self.define_operator('.', "postfix", self.parse_specifier)
        self.define_operator('list', "postfix", self.parse_index)
        self.define_operator('!', "prefix")
        self.define_operator('~', "prefix")
        self.define_operator('+', "prefix")
        self.define_operator('-', "prefix")
        self.define_operator('++', "prefix")
        self.define_operator('--', "prefix")
        self.define_operator('*', "mul")
        self.define_operator('/', "mul")
        self.define_operator('%', "mul")
        self.define_operator('+', "add")
        self.define_operator('-', "add")
        self.define_operator('<<', "bshift")
        self.define_operator('>>', "bshift")
        self.define_operator('<', "rel")
        self.define_operator('<=', "rel")
        self.define_operator('>', "rel")
        self.define_operator('>=', "rel")
        self.define_operator('==', "rel")
        self.define_operator('!=', "rel")
        self.define_operator('&', "bitand")
        self.define_operator('^', "bitxor")
        self.define_operator('|', "bitor")
        self.define_operator('&&', "logand")
        self.define_operator('||', "logor")
        self.define_operator('=', "assign")
        self.define_operator('+=', "assign")
        self.define_operator('-=', "assign")
        self.define_operator('*=', "assign")
        self.define_operator('/=', "assign")
        self.define_operator('%=', "assign")
        self.define_operator('&=', "assign")
        self.define_operator('^=', "assign")
        self.define_operator('|=', "assign")
        self.define_operator('<<=', "assign")
        self.define_operator('>>=', "assign")
        self.define_operator(',', "comma")
        # Builtin braces:
        self.define_braces('[', ']', "list")
        self.define_braces('(', ')', "expr")
        self.define_braces('{', '}', "hash")
        self.define_braces("{{\n", "}}", "template")
        self.define_braces("{{", "}}", "template")
        # Builtin statements:
        self.define_statement("do")
        self.define_statement("if")
        self.define_statement("for")
        self.define_statement("while")
        self.define_statement("with")
        self.define_statement("when")
    #-def

    def define_binary_operator_group(self, name, assoc, ppos, refgrp = None):
        """define_binary_operator_group(name, assoc, ppos[, refgrp])

        Define new group for binary operators. The name parameter is the group
        name, assoc is the group associativity, ppos is the position in
        precedence table, and refgrp is the name of reference group. Allowed
        values for assoc are:
        - Operator.Left
        - Operator.Right
        - Operator.NoAssoc
        Allowed values for ppos are:
        - Precedence.Highest
        - Precedence.Lowest
        - Precedence.Before
        - Precedence.After
        In the case of last two values of ppos, refgrp is required.
        """

        # Check group name:
        check(self.context, name, "Group name is empty.")
        check(self.context,
            name not in self.GRP_PRIVATE_NAMES,
            "Group name %s is private." % repr(name)
        )
        check(self.context,
            name not in self.__bopgroups_list,
            "Group %s is already defined." % repr(name)
        )
        # Check associativity:
        check(self.context,
            assoc in [Operator.Left, Operator.Right, Operator.NoAssoc],
            "Bad value of associativity argument."
        )
        # Check position in precedence table:
        check(self.context,
            ppos in [
                Precedence.Highest, Precedence.Lowest,
                Precedence.Before, Precedence.After
            ],
            "Invalid type of position in precedence table."
        )
        check(self.context,
            ppos not in [Precedence.Before, Precedence.After] or refgrp,
            "Missing name of reference group."
        )
        # Check reference group name:
        check(self.context,
            refgrp not in self.GRP_PRIVATE_NAMES,
            "Name %s of reference group is private." % repr(refgrp)
        )
        check(self.context,
            (not refgrp) or refgrp in self.__bopgroups_list,
            "Group %s is not defined." % repr(refgrp)
        )
        # Add group name:
        if ppos == Precedence.Highest:
            self.__bopgroups_list.append(name)
        elif ppos == Precedence.Lowest:
            self.__bopgroups_list.insert(0, name)
        elif ppos == Precedence.Before:
            self.__bopgroups_list.insert(
                self.__bopgroups_list.index(refgrp), name
            )
        elif ppos == Precedence.After:
            self.__bopgroups_list.insert(
                self.__bopgroups_list.index(refgrp) + 1, name
            )
        else:
            internal_error(self.context, "Reached unreachable.")
        # Set group associativity:
        self.__bopgroups_assoc[name] = assoc
        # Update values in precedence table:
        for i, g in enumerate(self.__bopgroups_list):
            self.__bopgroups_prec[g] = i
    #-def

    def define_operator(self, name, group, parser = None):
        """define_operator(name, group[, parser])

        Add operator name into operator group group. If parser is defined, it
        is used to finish operator. If operator name starts with letter, digit,
        or '_', it is treated as a name of brace group and in this case parser
        must be defined and group must be postfix. Example:
          Let '[' and ']' be braces from 'list' group and let 'list' be an
          unary postfix operator with parser 'parse_expression'. Then

            $x[2]

          is parsed as $x with unary operator [2] applied.
        """

        # Check operator name:
        check(self.context, name, "Operator name is empty.")
        check(self.context,
            not (name[0].isalnum() or name[0] == '_')
            or (parser and group == self.GRP_POSTFIX_NAME),
            "Parser and 'postfix' group are required if operator name is "\
            "brace group."
        )
        check(self.context,
            name not in self.__braces.keys(),
            "Operator-brace conflict."
        )
        # Check group:
        check(self.context,
            group in self.GRP_PRIVATE_NAMES or group in self.__bopgroups_list,
            "Group name %s is not defined." % repr(group)
        )
        # Define operator:
        if group == self.GRP_PREFIX_NAME:
            self.__upreops_re = update_word_lexer(
                name, self.__upreops_list, self.__upreops_re
            )
            if parser:
                self.__upreops_parsers[name] = parser
        elif group == self.GRP_POSTFIX_NAME:
            self.__upostops_re = update_word_lexer(
                name, self.__upostops_list, self.__upostops_re
            )
            if parser:
                self.__upostops_parsers[name] = parser
        else:
            self.__binops[name] = group
            if parser:
                self.__binops_parsers[name] = parser
    #-def

    def define_braces(self, left, right, group):
        """define_braces(left, right, group)

        Define new pair of braces under group group.
        """

        # Check validity of braces:
        check(self.context, left and right, "Empty brace definition.")
        check(self.context,
            left != right,
            "Both braces have same definitions."
        )
        check(self.context,
            left not in self.__binops.keys() and
            right not in self.__binops.keys(),
            "Brace-operator conflict."
        )
        # Define braces:
        self.__upreops_re = update_word_lexer(
            left, self.__upreops_list, self.__upreops_re
        )
        self.__upreops_re = update_word_lexer(
            right, self.__upreops_list, self.__upreops_re
        )
        self.__upostops_re = update_word_lexer(
            left, self.__upostops_list, self.__upostops_re
        )
        self.__upostops_re = update_word_lexer(
            right, self.__upostops_list, self.__upostops_re
        )
        self.__braces[left] = self.__braces[right] = (left, right, group)
    #-def

    def define_statement(self, name):
        """define_statement(name)

        Define new statement keyword.
        """

        if name in self.__statements:
            return
        self.__statements.append(name)
    #-def

    def scan(self):
        """scan() -> instance of Token

        Scan for the token from FIRST(start) set. Candidates are:
          - left brace for expression
          - unary prefix operator
          - identifier, statement keyword
          - integer, multipart integer, floating point number
          - single quoted string
          - double quoted string
          - path
          - left brace for template
          - left brace for list
          - left brace for hash
        """

        ctx = self.context
        if not ctx.inputstack:
            return None
        input = ctx.inputstack[-1]
        data = input.data
        offset = input.offset
        dsize = input.size
        # Skip comments and spaces:
        offset = self.skip(data, offset)
        if offset >= dsize:
            input.offset = dsize
            return None
        # Scan for token:
        c = data[offset]
        #: TIdentifier
        if c.isalpha() or c in "$_":
            ws, input.offset = self.scan_identifier(data, offset, dsize)
            return TIdentifier(self, offset, [w for w in ws if w])
        #: TInt, TMultiInt, TFloat
        elif c.isdigit():
            snum, input.offset = self.scan_number(data, offset)
            if 'f' in snum:
                return TFloat(self, offset, snum[:-1])
            elif 'e' in snum or 'E' in snum:
                return TFloat(self, offset, snum)
            elif '.' in snum:
                return TMultiInt(self, offset, snum.split('.'))
            return TInt(self, offset, snum)
        #: TSqStr
        elif c == '\'':
            s, input.offset = self.scan_single_quoted_string(
                data, offset, dsize
            )
            return TSqStr(self, offset, s)
        #: TDqStr
        elif c == '"':
            s, vps, input.offset = self.scan_double_quoted_string(
                data, offset, dsize
            )
            return TDqStr(self, offset, s, vps)
        #: UNARY OPERATOR, LBRACE, PATH
        else:
            # Try scan path first:
            path, vs, input.offset = self.scan_path(data, offset, dsize)
            if path:
                return TPath(self, offset, path, vs)
            # Must be unary prefix operator or left brace:
            if not self.__upreops_re:
                stok = ""
                input.offset = offset
            else:
                stok, input.offset = self.omatch(
                    self.__upreops_re, data, offset
                )
            if not stok:
                parser_error(ctx, ctx.getipos(offset),
                    "Expected unary prefix operator or left brace."
                )
            # Assume that we have brace:
            brace_info = self.__braces.get(stok, None)
            if brace_info:
                if stok != brace_info[0]:
                    parse_error(ctx, ctx.getipos(offset),
                        "Expected left brace"
                    )
                return TLeftBrace(self, offset, brace_info)
            # We have unary prefix operator:
            # - finish parsing if it is necessary:
            finisher = self.__upreops_parsers.get(stok, None)
            if not finisher:
                invoker = MethodInvoker(PREFIX_OPERATOR % stok)
                return TOperator(self, offset, invoker, Operator.Prefix)
            invoker, input.offset = finisher(stok, data, input.offset)
            return TOperator(self, offset, invoker, Operator.Prefix)
        internal_error(ctx, "Reached unreachable in scan routine.")
    #-def

    def skip(self, data, offset):
        r"""skip(data, offset) -> integer

        Skip all blanks and comments.
        == cut ==
        <regexp>
          <name>SKIPPER</name>
          <code>
            # Regular expression for matching whitespaces and comments.
            (?:                   # Do not capture.
              \# [^\n]*           # Skip comment
            |                     # or
              [\a\b\t\n\v\f\r ]*  # whitespaces
            |                     # or
              \\ \r? \n           # escaped end of line
            |                     # or
              ;                   # ';' (null command).
            )*
          </code>
        </regexp>
        """

        return self.SKIPPER.match(data, offset).end()
    #-def

    def scan_identifier(self, data, offset, dsize):
        r"""scan_identifier(data, offset, dsize) -> (list, integer)

        Scan for identifier.
        == cut ==
        <regexp>
          <name>VARNAME_RE</name>
          <code>
            # Regular expression for matching variable names.
            [A-Za-z_] [0-9A-Za-z_]*
          </code>
          <message>letter or '_'</message>
        </regexp>
        <regexp>
          <name>VARUSE_RE</name>
          <code>
            # Regular expression for matching variable use.
            \$ [A-Za-z_] [0-9A-Za-z_]*
          </code>
          <message>'$' followed by letter or '_'</message>
        </regexp>
        """

        wordlist = []
        w, offset = self.omatch(self.VARNAME_RE, data, offset)
        wordlist.append(w)
        ws, offset = self.imatch(self.VARUSE_RE, data, offset)
        wordlist.extend(ws)
        while offset < dsize and data[offset] == '-':
            old_offset = offset + 1
            w, offset = self.omatch(self.VARNAME_RE, data, offset)
            ws, offset = self.imatch(self.VARUSE_RE, data, offset)
            if offset == old_offset:
                offset -= 1
                break
            wordlist.append('-')
            wordlist.append(w)
            wordlist.extend(ws)
        return wordlist, offset
    #-def

    def scan_number(self, data, offset):
        r"""scan_number(data, offset) -> (str, integer)

        Scan for floating point number, integer, or multipart integer.
        == cut ==
        <regexp>
          <name>NUMBER_RE</name>
          <code>
            # Regular expression for matching integer, multi-integer, or float.
            # After sequence of digits,
            [0-9]+
            (?:
              # match optional dot followed by sequence of digits.
              \. [0-9]+
              (?:
                # If the following is exponent part, we have float.
                [eE] [+-]? [0-9]+ f?
              |
                # Else, if we can match 'f', we have float.
                f
              |
                # Otherwise, try to match multi-integer fields.
                (?: \. [0-9]+ )+
              )?
              # Here, we have a multi-integer.
            )?
            # Here, we have an integer.
          </code>
          <message>digit</message>
        </regexp>
        """

        return self.match(self.NUMBER_RE, data, offset)
    #-def

    def scan_single_quoted_string(self, data, offset, dsize):
        """scan_single_quoted_string(data, offset, dsize) -> (str, integer)

        Scan for single quoted string.
        """

        s = ""
        if offset >= dsize or data[offset] != '\'':
            parse_error(self.context, self.context.getipos(offset),
                "Expected single quote (')."
            )
        offset += 1
        while offset < dsize:
            c = data[offset]
            if c == '\'':
                break
            elif c == '\\':
                esc, offset = self.scan_escape_char(data, offset, dsize)
                s += esc
            elif self.is_strchar(c):
                offset += 1
                s += c
            else:
                parse_error(self.context, self.context.getipos(offset),
                    "Invalid string character %s." % repr(c)
                )
        if offset >= dsize or data[offset] != '\'':
            parse_error(self.context, self.context.getipos(offset),
                "Expected single quote (')."
            )
        return s, offset + 1
    #-def

    def scan_double_quoted_string(self, data, offset, dsize):
        """scan_double_quoted_string(data, offset, dsize)
           -> (str, list, integer)

        Scan for double quoted string.
        """

        s = ""
        v = []
        if offset >= dsize or data[offset] != '"':
            parse_error(self.context, self.context.getipos(offset),
                "Expected double quote (\")."
            )
        offset += 1
        while offset < dsize:
            c = data[offset]
            if c == '"':
                break
            elif c == '$':
                varuse, offset = self.omatch(self.VARUSE_RE, data, offset)
                if not varuse:
                    offset += 1
                    s += c
                    continue
                v.append((len(s), len(varuse)))
                s += varuse
            elif c == '\\':
                esc, offset = self.scan_escape_char(data, offset, dsize)
                s += esc
            elif self.is_strchar(c):
                offset += 1
                s += c
            else:
                parse_error(self.context, self.context.getipos(offset),
                    "Invalid string character %s." % repr(c)
                )
        if offset >= dsize or data[offset] != '"':
            parse_error(self.context, self.context.getipos(offset),
                "Expected double quote (\")."
            )
        return s, v, offset + 1
    #-def

    def scan_escape(self, data, offset, dsize):
        r"""scan_escape(data, offset, dsize) -> (str, integer)

        Scan for escape sequence.
        == cut ==
        <regexp>
          <name>OCTNUM_RE</name>
          <code>
            # Match from 1 to 3 octal digits.
            [0-7]{1, 3}
          </code>
          <message>octal digit</message>
        </regexp>
        <regexp>
          <name>XNUM_RE</name>
          <code>
            # Match two hexadecimal digits.
            [0-9A-Fa-f]{2}
          </code>
          <message>two hexadecimal digits</message>
        </regexp>
        <regexp>
          <name>XQUAD_RE</name>
          <code>
            # Match four hexadecimal digits.
            [0-9A-Fa-f]{4}
          </code>
          <message>four hexadecimal digits</message>
        </regexp>
        <regexp>
          <name>XOCTET_RE</name>
          <code>
            # Match eight hexadecimal digits.
            [0-9A-Fa-f]{8}
          </code>
          <message>eight hexadecimal digits</message>
        </regexp>
        """

        if offset >= dsize or data[offset] != '\\':
            parse_error(self.context, self.context.getipos(offset),
                "Expected backslash (\\)."
            )
        if offset + 1 >= dsize:
            parse_error(self.context, self.context.getipos(offset),
                "Unexpected end of input."
            )
        offset += 1
        c = data[offset]
        if c not in "\n\r" or ord(c) < 32 or ord(c) > 126:
            parse_error(self.context, self.context.getipos(offset),
                "Escape sequence must contains only ASCII7 printable "\
                "characters, \\r followed by \\n, or \\n."
            )
        elif c in "abtnvfr":
            return eval(r"'\%s'" % c), offset + 1
        elif c == '\n':
            return "", offset + 1
        elif c == '\r':
            offset += 1
            if offset >= dsize or data[offset] != '\n':
                parse_error(self.context, self.context.getipos(offset),
                    "Expected line feed (\\n)."
                )
            return "", offset + 1
        elif c in "01234567":
            onum, offset = self.match(self.OCTNUM_RE, data, offset)
            return eval(r"'\%s'" % onum), offset
        elif c == 'x':
            xnum, offset = self.match(self.XNUM_RE, data, offset)
            return eval(r"'\x%s'" % xnum), offset
        elif c == 'u':
            xquad, offset = self.match(self.XQUAD_RE, data, offset)
            return eval(r"'\u%s'" % xquad), offset
        elif c == 'U':
            xoctet, offset = self.match(self.XOCTET_RE, data, offset)
            return eval(r"'\U%s'" % xoctet)
        return c, offset + 1
    #-def

    def is_strchar(self, c):
        """is_strchar(c) -> bool

        Return True is c is character allowed in string.
        """

        return c in "\t\n\r" or (ord(c) > 31 and c.isprintable())
    #-def

    def scan_path(self, data, offset, dsize):
        """scan_path(data, offset, dsize) -> (str, list, integer)

        Scan for path.
        """

        if data[offset:offset+2] != "./":
            return "", [], offset
        p = "./"
        vs = []
        s, offset = self.scan_path_part(data, offset + 2, dsize, p, vs)
        if not s:
            return ".", vs, offset
        p += s
        while offset < dsize:
            c = data[offset]
            if c != '/':
                break
            p += c
            s, offset = self.scan_path_part(data, offset + 1, dsize, p, vs)
            if not s:
                break
            p += s
        if p[-1] == '/':
            p = p[:-1]
        if p.startswith("./..")
            p = p[2:]
            vs = [(x - 2, y - 2) for x, y in vs]
        return p, vs, offset
    #-def

    def scan_path_part(self, data, offset, dsize, p, vs):
        """scan_path_part(data, offset, dsize, p, vs) -> (str, integer)

        Scan for part of path lying between '/'.
        """

        if data[offset:offset+2] == "..":
            return "..", offset + 2
        s = ""
        l = len(p)
        while offset < dsize:
            c = data[offset]
            if c == '$':
                varuse, offset = self.omatch(self.VARUSE_RE, data, offset)
                if not varuse:
                    offset += 1
                    s += c
                    continue
                vs.append((l + len(s), len(varuse)))
                s += varuse
            elif s and s[-1] == '.' and c == '.':
                return s[:-1], offset - 1
            elif s and s[-1] == '\\':
                if c not in " $()+-@_~":
                    return s[:-1], offset - 1
                offset += 1
                s = s[:-1] + c
            elif c in "!+-.@\\_~" or c.isalnum():
                offset += 1
                s += c
            else:
                break
        if s and s[-1] == '\\':
            return s[:-1], offset - 1
        return s, offset
    #-def

    def match(self, reobj, data, offset):
        """match(reobj, data, offset) -> (str, integer)

        Match string described by reobj from data starting at offset. Raise
        an exception if matching fails.
        """

        m = reobj.match(data, offset)
        if m is None:
            parse_error(self.context, self.context.getipos(offset),
                "Expected %s." % self.ERR_MESSAGES[reobj]
            )
        return m.group(), m.end()
    #-def

    def omatch(self, reobj, data, offset):
        """omatch(reobj, data, offset) -> (str, integer)

        Like match, but if matching fails, ("", offset) is returned.
        """

        m = reobj.match(data, offset)
        if m is None:
            return "", offset
        return m.group(), m.end()
    #-def

    def imatch(self, reobj, data, offset):
        """imatch(reobj, data, offset) -> (list, integer)

        Return the list of zero or more strings which satisfies reobj and the
        pointer to the first improper character in data.
        """

        l = []
        while True:
            m = reobj.match(data, offset)
            if m is None or m.end() == offset:
                break
            l.append(m.group())
            offset = m.end()
        return l, offset
    #-def
#-class

class DoItParser(Parser):
    """
    """

    def __init__(self, lexer):
        """
        """

        Parser.__init__(self, lexer)
    #-def

    def start(self):
        """start()

        Intitial rule.

        start -> statement*
        """

        lexer = self.lexer
        peek = lexer.peek
        next = lexer.next
        
    #-def

    def statement(self, lexer, peek, next):
        """statement()

        Rules for the statement parsing.

        statement -> STATEMENT_NAME ...
        statement -> expression
        """

        token = peek()
        if token == TokenType.Identifier and token.is_statement():
            return self.stmt_parse(lexer, peek, next)
        return self.expression(lexer, peek, next)
    #-def

    def expression(self, lexer, peek, next, level = 0):
        """expression([level = 0]) -> instance of Command

        expression -> uexpression (BINOP expression)*
        """

        left = uexpression()
        operator = peek()
        while operator == TokenType.Operator.Binary\
        and operator.priority >= level:
            next()
            right = self.expression(operator.level)
            left = InfixOperatorCommand(operator, left, right)
            if not operator.is_associative():
                break
            operator = peek()
        return left
    #-def

    def uexpression(self):
        """uexpression()

        uexpression -> atom params
        uexpression -> pexpression
        """

        token = peek()
        if token == TokenType.Operator and token.is_unary_prefix():
            return self.pexpression()
    #-def

    def pexpression(self):
        """pexpression()

        pexpression -> UOP pexpression
        pexpression -> ppexpression
        """

    def ppexpression(self):
        """ppexpression()

        ppexpression -> ppexpression UOP
        ppexpression -> atom
        """

    def atom(self):
        """atom()

        atom -> atom SPECIFIER
        atom -> IDENTIFIER
        atom -> NUMBER
        atom -> STRING
        atom -> PATH
        atom -> TEMPLATE
        atom -> hash
        atom -> LEXPRPAR expression REXPRPAR
        """
        if t == TokenType.CmdOrVarName:
            lexer.skip()
            
    #-def

    def hash(self):
        """hash()

        hash -> LHASHPAR
        """
    #-def

    def params(self):
        """params()

        params -> param params
        params -> param
        """
    #-def

    def param(self):
        """param()

        param -> atom
        param -> WORD
        """
    #-def
#-class
