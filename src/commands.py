#                                                         -*- coding: utf-8 -*-
#! \file    ./src/commands.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2014-02-27 20:35:32 (UTC+01:00, DST+00:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   @pyfile.docstr
#
"""\
DoIt! commands.\
"""

__license__ = """\
Copyright (c) 2014 Jiří Kučera.

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

from utils import Token, Lexer

# =============================================================================
# == Lexical analysis                                                        ==
# =============================================================================

# !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
__FLAGCHARS = "!#$%&*+?@^~"
__SYMBOLS = "!%&()*+,/:<=>?@[]^`{|}~"

__I_DONT_KNOW = 0
__ID_NAME = 1
__DASHED_NAME = 2
__VAR_NAME = 3

class DoItLexer(Lexer):
    """Lexical analyzer for DoIt! interpreter.
    """
    __slots__ = []

    def __init__(self, input):
        """DoItLexer(input) -> instance of Lexer

        Constructor.
        """

        Lexer.__init__(self, input)
    #-def

    def scan(self):
        """
        """

        getc = self.input.getc
        ungets = self.input.ungets
        while True:
            c = getc()
            # EOF
            if c == '':
                return None
            # Delimiter #1
            elif c == '\n':
                t = Delimiter(self)
                self.line += 1
                return t
            # Space
            elif c.isspace():
                continue
            # Delimiter #2
            elif c == ';':
                return Delimiter(self)
            # Multiline handling
            elif c == '\\':
                c = getc()
                if c != '\n':
                    ungets(c)
                    raise
                self.line += 1
                continue
            # Comment
            elif c == '#':
                while True:
                    c = getc()
                    if c == '':
                        break
                    elif c == '\n':
                        self.line += 1
                        break
                continue
            # Path or Selector
            elif c == '.':
                ln = self.line
                c = getc()
                if c == '/':
                    return Path(self.__scan_path('', getc, ungets), ln)
                elif c == '.':
                    return Path(self.__scan_path('..', getc, ungets), ln)
                elif c.isalpha():
                    return Selector(self.__scan_word(c, getc, ungets), ln)
                else:
                    ungets(c)
                    return Path('.', ln)
                continue
            # Label or CommandName or Variable or Identifier
            elif c.isalpha() or c in ['_', '$']:
                peeked = ''
                l = [self.__scan_cmdpart(c, getc, ungets)]
                # { DASHED, ID, VAR }
                while True:
                    t_old, _ = l[-1]
                    t, v = tv = self.__scan_cmdpart(getc(), getc, ungets)
                    # t in { DASHED, ID, VAR, DIRSEP, ? }
                    # t is ? => stop
                    if t == __I_DONT_KNOW:
                        peeked = v
                        break
                    # Handle '//'
                    if t == __DIRSEP_NAME and t_old == __DIRSEP_NAME:
                        ungets('/')
                        break
                    l.append(tv)
                if l[-1][0] == __DIRSEP_NAME:
                    raise
                if peeked == ':':
                    getc()
                    return Label(l)
                if len(l) > 1:
                    return CommandName(l)
                t, v = l[0]
                if t == __VAR_NAME:
                    return Variable(v)
                elif t == __ID_NAME:
                    return Identifier(v)
                return CommandName(v)
            # Word
            elif c.isdigit():
                v = c
                return Word(v)
            # HardString or SoftString
            elif c == '\'' or c == '"':
                v = self.__scan_string(c, getc, ungets)
                if c == '"':
                    return SoftString(v)
                return HardString(v)
            # ShortArg or LongArg or KwArg
            elif c == '-':
                c = getc()
                if c == '':
                    raise
                elif c == '-':
                    return self.__scan_long_or_kw_arg(getc, ungets)
                elif c.isalnum() or c in __FLAGCHARS:
                    cc = getc()
                    if cc.isalnum() or cc in __FLAGCHARS:
                        ungets('-' + cc)
                        return ShortArg(c)
                    elif c == '' or cc.isspace() or cc == ';' or cc == '\\':
                        ungets(cc)
                        return ShortArg(c)
                    ungets(cc)
                    raise
                ungets(c)
                raise
            # Symbols - must be last
            elif c in __SYMBOLS:
                return Symbol(self, c)
            raise LexerError(self, "Unexpected character %s" % repr(c))
        raise LexerError(self, "Hidden DoIt lexer bug")
    #-def

    def __scan_cmdpart(self, c, getc, ungets):
        """
        """

        s = c
        if c.isalpha() or c == ['-', '_']:
            while True:
                c = getc()
                if c.isalnum() or c in ['-', '_']:
                    s += c
                    continue
                ungets(c)
                break
            if '-' in s:
                return (__DASHED_NAME, s)
            return (__ID_NAME, s)
        elif c == '$':
            s = getc()
            if not s.isalpha() and not s == '_':
                ungets(s)
                raise LexerError(self, "Expected letter or '_' after '$'")
            while True:
                c = getc()
                if c.isalnum() or c == '_':
                    s += c
                    continue
                ungets(c)
                break
            return (__VAR_NAME, s)
        elif c == '/':
            return (__DIRSEP_NAME, '/')
        else:
            ungets(c)
        return (__I_DONT_KNOW, c)
    #-def
#-class

class CmdLineLexer(Lexer):
#-class

__buildin_commands = {}

def command(*parsers):
    """
    """

    def wrap_command(cmd):
        def command_wraper(args, ctx):
            opts = Parser.pxalt(*parsers).parse(args, ctx)
            return cmd(opts, ctx)
        return command_wraper
    return wrap_command
#-def

@command(
    _longarg('help', "Print %(command)s usage."),
    _posarg('command_name', str, """
        Search for command `command_name' and return it; otherwise raise a
        CommandNotFound exception. The command searching strategy is:
          + first search in prespecified directories,
          + after that, search in builtin commands.
    """)
)
def getcmd(opts, ctx):
    """getcmd(opts, ctx) -> instance of Command

    Return command which name is in opts using informations from ctx where to
    search. Raise CommandNotFoundError if command does not exists.
    """

    if opts.get('--help', False):
        return HelpScreen(cmd_getcmd)
    cmd_name = opts[1]
    cmd = ctx.environment.get('#CMDLIST', {}).get(\
        cmd_name, __buildin_commands.get('%s' % cmd_name, None)\
    )
    if cmd is not None:
        return Command(cmd)
    raise CommandNotFoundError(opts[1])
#-def

@command(
    _cmd('if') + COMMANDS + _separg(';')
    + _separg('then') + COMMANDS
    + _optargs(
        _separg('elif') + COMMANDS + _separg(';')
        + _separg('then') + COMMANDS
    )
    + _optarg(
        _separg('else') + COMMANDS
    )
    + _separg('end')
)
