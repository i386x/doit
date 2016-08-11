#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/app/application.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-03 23:19:27 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Classes for creating applications.\
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

import sys

ERROR_APPLICATION = DoItError.alloc_codes(1)

class ApplicationError(DoItError):
    """
    """
    __slots__ = []

    def __init__(self, emsg):
        """
        """

        DoItError.__init__(self, ERROR_APPLICATION, emsg)
    #-def
#-class

class ApplicationExit(ApplicationError):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        ApplicationError.__init__(self,
            "I am a signal rather then error. Please, handle me properly"
        )
    #-def
#-class

class OptionSharedData(object):
    """
    """
    SHRT_PREFIX = "-"
    LONG_PREFIX = "--"
    KW_DELIM = "="
    NAME_METAVAR = "name"
    VALUE_METAVAR = "value"

    OPTIONAL = 0
    MANDATORY = 1
    TYPE = 1
    __slots__ = []

    def __init__(self):
        """
        """

        self.SHRT_TEMPLATE = "%s%%(%s)s" % (
            self.SHRT_PREFIX, self.NAME_METAVAR
        )
        self.LONG_TEMPLATE = "%s%%(%s)s" % (
            self.LONG_PREFIX, self.NAME_METAVAR
        )
        self.KW_SHRT_TEMPLATE = "%s%%(%s)s<%%(%s)s>" % (
            self.SHRT_PREFIX, self.NAME_METAVAR, self.VALUE_METAVAR
        )
        self.KW_LONG_TEMPLATE = "%s%%(%s)s%s<%%(%s)s>" % (
            self.LONG_PREFIX, self.NAME_METAVAR, self.KW_DELIM,
            self.VALUE_METAVAR
        )
    #-def
#-class

class Option(OptionSharedData):
    """
    """
    __slots__ = []

    def __init__(self, name, **kwargs):
        """
        """

        OptionSharedData.__init__(self)
        self.name = name
        self.short_aliases = kwargs.get('short_aliases', [])
        self.when_defined = kwargs.get('when_defined', -1)
        self.when_given = kwargs.get('when_given', -1)
        self.about = kwargs.get('about', "")
        self.action_callback = kwargs.get('action_callback', (lambda o: None))
        self.flags = kwargs.get('flags', 0)
        self.default = kwargs.get('default')
    #-def

    def gen_help_lines(self, margin = 2, optcolsz = 24, fill = 2, limit = 79):
        """
        """

        # Check arguments validity:
        tab = margin + optcolsz + fill
        if margin < 1 or optcolsz < 1 or fill < 1 or tab >= limit:
            raise ApplicationError("Bad help line geometry")

        # Setup template arguments and templates:
        is_kwopt = isinstance(self, KwOption)
        tplargs = { self.NAME_METAVAR: self.name }
        if is_kwopt:
            tplargs[self.VALUE_METAVAR] = self.about_value
        ltpl = self.KW_LONG_TEMPLATE if is_kwopt else self.LONG_TEMPLATE
        stpl = self.KW_SHRT_TEMPLATE if is_kwopt else self.SHRT_TEMPLATE

        # Format and check arguments help:
        about = self.about % tplargs
        about_limit = limit - tab
        about_parts = [s.strip() for s in about.split('\n')]
        for s in about_parts:
            if len(s) > about_limit:
                raise ApplicationError("Help line is too long")

        # Generate arguments text forms:
        sopts = [ltpl % tplargs]
        for shopt in self.short_aliases:
            tplargs[self.NAME_METAVAR] = shopt
            sopts.append(stpl % tplargs)

        # Generate lines:
        smargin = " " * margin
        lines = []
        line = []
        i, n = 0, len(sopts)
        while i < n:
            sopt = sopts[i]
            line.append(sopt)
            r = self.__test_line_length(
                line, i < n - 1, margin, optcolsz, limit
            )
            if r == TOO_LONG:
                del line[-1]
                if not line:
                    raise ApplicationError("Help line is too long")
                self.__make_line(lines, line, smargin, ",")
                line = []
                continue
            elif r == FITS_TO_ROW:
                del line[-1]
                if not line:
                    i += 1
                    self.__make_line(
                        lines, [sopt], smargin, "" if i >= n else ","
                    )
                    # Last line - add about text:
                    if i >= n:
                        lines.append("")
                        self.__append_about(lines, about_parts, tab)
                    continue
                self.__make_line(lines, line, smargin, ",")
                line = []
                continue
            elif r == FITS_TO_COL:
                i += 1
                # Commit the last line and add about text:
                if i >= n:
                    self.__make_line(lines, line, smargin, "")
                    line = []
                    self.__append_about(lines, about_parts, tab)
                continue
            else:
                raise ApplicationError("Internal error")
        if lines and not lines[-1]:
            del lines[-1]
        return lines
    #-def

    def __test_line_length(line, is_last, indent, collimit, limit):
        """
        """

        sz = 0
        for s in line:
            sz += len(s)
        if sz > 0:
            sz += indent
        else:
            return EMPTY_LINE
        if len(line) >= 2:
            sz += (len(line) - 1) * 2 # separators
        if not is_last:
            sz += 1 # comma
        if sz <= collimit:
            return FITS_TO_COL
        elif sz <= limit:
            return FITS_TO_ROW
        return TOO_LONG
    #-def

    def __make_line(lines, line, sbeg, send):
        """
        """

        lines.append("%s%s%s" % (sbeg, ", ".join(line), send))
    #-def

    def __append_about(lines, about, tab):
        """
        """

        if not lines:
            lines.append("")
        i, n = 0, len(about)
        while i < n:
            if i == 0:
                pad = " " * (tab - len(lines[-1]))
                lines[-1] = ("%s%s%s" % (lines[-1], pad, about[i])).rstrip()
            else:
                pad = " " * tab
                lines.append(("%s%s" % (pad, about[i])).rstrip())
            i += 1
    #-def
#-class

class KwOption(Option):
    """
    """
    __slots__ = []

    def __init__(self, name, **kwargs):
        """
        """

        Option.__init__(self, name, **kwargs)
        self.value = self.default
        self.about_value = kwargs.get('about_value', "<value>")
    #-def
#-class

class OptionDispatcher(OptionSharedData):
    """
    """
    __slots__ = []

    def __init__(self, processor):
        """
        """

        OptionSharedData.__init__(self)
        self.__processor = processor
        self.__options = self.__processor.get_options()
        self.__halt = False
    #-def

    def get_processor(self):
        """
        """

        return self.__processor
    #-def

    def dispatch(self, opt):
        """
        """

        if self.halted():
            self.unhalt()
            return False
        if opt.startswith(self.LONG_PREFIX):
            return self.dispatch_long(opt[len(self.LONG_PREFIX):])
        elif opt.startswith(self.SHRT_PREFIX):
            return self.dispatch_short(opt[len(self.SHRT_PREFIX):])
        return False
    #-def

    def dispatch_long(self, opt):
        """
        """

        if not opt:
            return False
        opts = self.__options
        d = opt.find(self.KW_DELIM)
        if d < 0:
            opts.set_option(opt)
        else:
            key = opt[0:d]
            value = opt[d + len(self.KW_DELIM):]
            if not key:
                self.__processor.on_missing_key(opt, prefix = self.LONG_PREFIX)
            if not value:
                self.__processor.on_missing_value(
                    opt, prefix = self.LONG_PREFIX
                )
            opts.set_kwoption(key, value)
        return True
    #-def

    def dispatch_short(self, opt):
        """
        """

        if not opt:
            return False
        opts = self.__options
        i = 0
        while i < len(opt):
            optname = opts.fullname(opt[i])
            if not optname:
                self.__processor.on_missing_alias(
                    opt[i], prefix = self.SHRT_PREFIX
                )
                optname = opt[i]
            if opts.is_kwoption(optname):
                v = opt[i + 1:]
                if not v:
                    self.__processor.on_missing_value(
                        opt[i], prefix = self.SHRT_PREFIX
                    )
                opts.set_kwoption(optname, v)
                return True
            opts.set_option(optname)
            i += 1
        return True
    #-def

    def halt(self):
        """
        """

        self.__halt = True
    #-def

    def unhalt(self):
        """
        """

        self.__halt = False
    #-def

    def halted(self):
        """
        """

        return self.__halt
    #-def
#-class

class Options(dict):
    """
    """
    __slots__ = []

    def __init__(self, processor):
        """
        """

        dict.__init__(self)
        self.__processor = processor
        self.__defined = []
        self.__alias2name = {}
        self.__given = []
        self.__check_enabled = True
    #-def

    def get_processor(self):
        """
        """

        return self.__processor
    #-def

    def fullname(self, shopt):
        """
        """

        return self.__alias2name.get(shopt)
    #-def

    def is_option(self, optname):
        """
        """

        return (
            isinstance(self.get(optname), Option) \
            and not self.is_kwoption(optname)
        )
    #-def

    def is_kwoption(self, optname):
        """
        """

        return isinstance(self.get(optname), KwOption)
    #-def

    def set_option(self, opt):
        """
        """

        if not opt in self:
            self.__processor.on_invalid_option(opt)
            return
        opt_object = self[opt]
        if not self.is_option(opt):
            self.__processor.on_expected_option(opt)
        if opt in self.__given:
            self.__given.remove(opt)
        self.__given.append(opt)
        self.adjust_given()
        opt_object.action_callback(opt_object)
    #-def

    def set_kwoption(self, key, value):
        """
        """

        if not key in self:
            self.__processor.on_invalid_option(key)
            return
        opt_object = self[key]
        if not self.is_kwoption(opt):
            self.__processor.on_expected_kwoption(opt)
        if opt in self.__given:
            self.__given.remove(opt)
        self.__given.append(opt)
        self.adjust_given()
        opt_object.value = value
        opt_object.action_callback(opt_object)
    #-def

    def __setitem__(self, optname, opt):
        """
        """

        opt.name = optname
        dict.__setitem__(self, optname, opt)
        if not optname in self.__defined:
            self.__defined.append(optname)
            opt.when_defined = len(self.__defined) - 1
        else:
            self.__processor.on_option_conflict(optname)
        for a in opt.short_aliases:
            if a in self.__alias2name:
                self.__processor.on_alias_conflict(a)
            self.__alias2name[a] = optname
    #-def

    def __delitem__(self, optname):
        """
        """

        if optname not in self:
            return
        if optname in self.__given:
            self.__given.remove(optname)
        for a in self[optname].short_aliases:
            if a in self.__alias2name:
                del self.__alias2name[a]
        if optname in self.__defined:
            self.__defined.remove(optname)
        self[optname].when_defined = -1
        self[optname].when_given = -1
        dict.__delitem__(self, optname)
        self.adjust()
    #-def

    def adjust(self):
        """
        """

        self.adjust_defined()
        self.adjust_given()
    #-def

    def adjust_defined(self):
        """
        """

        i = 0
        while i < len(self.__defined):
            self[self.__defined[i]].when_defined = i
            i += 1
    #-def

    def adjust_given(self):
        """
        """

        i = 0
        while i < len(self.__given):
            self[self.__given[i]].when_given = i
            i += 1
    #-def

    def enable_check(self):
        """
        """

        self.__check_enabled = True
    #-def

    def disable_check(self):
        """
        """

        self.__check_enabled = False
    #-def

    def check_enabled(self):
        """
        """

        return self.__check_enabled
    #-def

    def check(self):
        """
        """

        if not self.check_enabled():
            self.enable_check()
            return
        errcls = self.__processor.get_error_class()
        for opt in self:
            if self[opt].when_given < 0 \
            and (self[opt].flags & Option.TYPE == Option.MANDATORY):
                raise errcls(
                    "%s: Mandatory option `%s' is missing" % (
                        self.__processor.get_app().get_name(), opt
                    )
                )
    #-def

    def get_defined_options(self):
        """
        """

        l = []
        for opt in self.__defined:
            l.append(self[opt])
        return l
    #-def
#-class

class OptionProcessor(object):
    """
    """
    __slots__ = []

    def __init__(self, app):
        """
        """

        self.__app = app
        self.__options = Options(self)
        self.__option_dispatcher = OptionDispatcher(self)
        self.__errcls = ApplicationError
    #-def

    def get_app(self):
        """
        """

        return self.__app
    #-def

    def set_options(self, options):
        """
        """

        self.__options = options
    #-def

    def get_options(self):
        """
        """

        return self.__options
    #-def

    def set_dispatcher(self, dispatcher):
        """
        """

        self.__option_dispatcher = dispatcher
    #-def

    def get_dispatcher(self):
        """
        """

        return self.__option_dispatcher
    #-def

    def set_error_class(self, errcls):
        """
        """

        self.__errcls = errcls
    #-def

    def get_error_class(self):
        """
        """

        return self.__errcls
    #-def

    def process(self, argv):
        """
        """

        i = 0
        while i < len(argv) and self.__option_dispatcher.dispatch(argv[i]):
            i += 1
        self.__options.check()
        return i
    #-def

    def on_option_conflict(self, opt, **params):
        """
        """

        raise self.__errcls(
            "%s: Long option `%s' is already specified" % (
                self.__app.get_name(), opt
            )
        )
    #-def

    def on_alias_conflict(self, opt, **params):
        """
        """

        raise self.__errcls(
            "%s: Short option `%s' is already specified" % (
                self.__app.get_name(), opt
            )
        )
    #-def

    def on_invalid_option(self, opt, **params):
        """
        """

        raise self.__errcls(
            "%s: Invalid option `%s'" % (self.__app.get_name(), opt)
        )
    #-def

    def on_expected_option(self, opt, **params):
        """
        """

        raise self.__errcls(
            "%s: `%s' must be simple (not key-value) option" % (
                self.__app.get_name(), opt
            )
        )
    #-def

    def on_expected_kwoption(self, opt, **params):
        """
        """

        raise self.__errcls(
            "%s: `%s' must be key-value option" % (self.__app.get_name(), opt)
        )
    #-def

    def on_missing_alias(self, opt, **params):
        """
        """

        prefix = params.get('prefix', "")
        raise self.__errcls(
            "%s: Invalid option `%s%s'" % (self.__app.get_name(), prefix, opt)
        )
    #-def

    def on_missing_key(self, opt, **params):
        """
        """

        prefix = params.get('prefix', "")
        raise self.__errcls(
            "%s: `%s%s' - missing key" % (self.__app.get_name(), prefix, opt)
        )
    #-def

    def on_missing_value(self, opt, **params):
        """
        """

        pass
    #-def
#-class

class Application(object):
    """
    """
    __slots__ = []

    def __init__(self, owner = None):
        """
        """

        self.__owner = None
        self.__name = None
        self.__option_processor = None
        self.__pending_args = []
        self.__exitcode = 0
    #-def

    def get_owner(self):
        """
        """

        return self.__owner
    #-def

    def set_name(self, name):
        """
        """

        self.__name = name
    #-def

    def get_name(self):
        """
        """

        return self.__name
    #-def

    def set_option_processor(self, op):
        """
        """

        self.__option_processor = op
    #-def

    def get_option_processor(self):
        """
        """

        return self.__option_processor
    #-def

    def get_pending_args(self):
        """
        """

        return self.__pending_args
    #-def

    def set_exitcode(self, ec):
        """
        """

        self.__exitcode = ec
    #-def

    def get_exitcode(self):
        """
        """

        return self.__exitcode
    #-def

    def set_output(self, output):
        """
        """

        self.__output = output
    #-def

    def set_error_log(self, error_log):
        """
        """

        self.__error_log = error_log
    #-def

    def set_log(self, log):
        """
        """

        self.__log = log
    #-def

    def run(self, argv = None):
        """
        """

        if argv is None:
            argv = sys.argv
        if not self.__name:
            if argv and argv[0]:
                self.__name = argv[0]
                argv = argv[1:]
            else:
                self.__name = "<app-name>"
        try:
            self.__option_processor = OptionProcessor(self)
            self.at_start()
            i = self.__option_processor.process(argv)
            self.__pending_args = argv[i:]
            self.__exitcode = self.main()
        except ApplicationExit:
            pass
        except ApplicationError as e:
            self.handle_error(e)
        finally:
            self.at_end()
        return self.__exitcode
    #-def

    def main(self):
        """
        """

        return 0
    #-def

    def define_option(self, name,
        shorts = [], about = "", cb = (lambda opt: None), flags = 0,
        default = None
    ):
        """
        """

        self.get_option_processor().get_options()[name] = Option(name,
            short_aliases = shorts, about = about, action_callback = cb,
            flags = flags, default = default
        )
    #-def

    def define_kwoption(self, name,
        shorts = [], about = "", cb = (lambda opt: None), flags = 0,
        default = None
    ):
        """
        """

        self.get_option_processor().get_options()[name] = KwOption(name,
            short_aliases = shorts, about = about, action_callback = cb,
            flags = flags, default = default
        )
    #-def

    def make_options_help(self):
        """
        """

        options = self.__option_processor.get_options().get_defined_options()
        hl = ["\n"]
        for o in options:
            hl.extend(["%s\n" % s for s in o.gen_help_lines()])
        hl.append("\n")
        return "".join(hl)
    #-def

    def at_start(self):
        """
        """

        pass
    #-def

    def at_end(self):
        """
        """

        pass
    #-def

    def handle_error(self, e):
        """
        """

        pass
    #-def

    def strip_block(self, s):
        """
        """

        lines = s.split('\n')
        if not lines:
            return ""
        i = 0
        for line in lines:
            if line and line[0] == ' ':
                while i < len(line) and line[i] == ' ':
                    i += 1
                break
        if i > 0:
            ws = " " * i
            j = 0
            while j < len(lines):
                if lines[j].startswith(ws):
                    lines[j] = lines[j][i:]
                j += 1
        return '\n'.join(lines)
    #-def

    def wout(self, s):
        """
        """

        self.__output.write(s)
    #-def

    def werr(self, s):
        """
        """

        self.__error_log.write(s)
    #-def

    def wlog(self, s):
        """
        """

        self.__log.write(s)
    #-def

    def exit(self, ec = 0):
        """
        """

        self.set_exitcode(ec)
        raise ApplicationExit()
    #-def
#-class
