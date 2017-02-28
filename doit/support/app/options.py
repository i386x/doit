#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/app/options.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-28 18:54:24 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Options processing.\
"""

__license__ = """\
Copyright (c) 2014 - 2017 Jiří Kučera.

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

from doit.support.app.printer import \
    Word, PageBuilder

from doit.support.app.errors import \
    ApplicationError

class Option(object):
    """
    """
    SHRT_PREFIX = "-"
    LONG_PREFIX = "--"
    KW_DELIM = "="
    NAME_METAVAR = "name"
    VALUE_METAVAR = "value"
    OPTREQ_BIT_MASK = 1
    OPTIONAL = 0
    REQUIRED = 1
    __slots__ = [
        'name', 'short_aliases',
        'when_defined', 'when_given',
        'about', 'about_value',
        'action_callback', 'flags',
        'default', 'has_value', 'value'
    ]

    def __init__(self, name, **kwargs):
        """
        """

        self.name = name
        self.short_aliases = kwargs.get('short_aliases', [])
        self.when_defined = kwargs.get('when_defined', -1)
        self.when_given = kwargs.get('when_given', -1)
        self.about = kwargs.get('about', "")
        self.about_value = kwargs.get('about_value', "value")
        self.action_callback = kwargs.get('action_callback', (lambda o: None))
        self.flags = kwargs.get('flags', 0)
        self.default = kwargs.get('default')
        self.has_value = kwargs.get('has_value', False)
        self.value = self.default
    #-def

    def short_template(self):
        """
        """

        if self.has_value:
            return "%s%%(%s)s<%%(%s)s>" % (
                self.SHRT_PREFIX, self.NAME_METAVAR, self.VALUE_METAVAR
            )
        return "%s%%(%s)s" % (self.SHRT_PREFIX, self.NAME_METAVAR)
    #-def

    def long_template(self):
        """
        """

        if self.has_value:
            return "%s%%(%s)s%s<%%(%s)s>" % (
                self.LONG_PREFIX, self.NAME_METAVAR, self.KW_DELIM,
                self.VALUE_METAVAR
            )
        return "%s%%(%s)s" % (self.LONG_PREFIX, self.NAME_METAVAR)
    #-def

    def helprow(self):
        """
        """

        d = {
            self.NAME_METAVAR: self.name,
            self.VALUE_METAVAR: self.about_value
        }
        wopts = [Word(self.long_template() % d)]
        for a in self.short_aliases:
            wopts[-1].data = "%s," % wopts[-1].data
            wopts.append(Word(
                self.short_template() % {
                    self.NAME_METAVAR: a, self.VALUE_METAVAR: self.about_value
                }
            ))
        return wopts, PageBuilder.to_words(self.about % d)
    #-def

    def is_required(self):
        """
        """

        return (self.flags & self.OPTREQ_BIT_MASK) == self.REQUIRED
    #-def

    @classmethod
    def repr_short(cls, optname):
        """
        """

        return "%s%s" % (cls.SHRT_PREFIX, optname)
    #-def

    @classmethod
    def repr_long(cls, optname):
        """
        """

        return "%s%s" % (cls.LONG_PREFIX, optname)
    #-def

    def __str__(self):
        """
        """

        return self.repr_long(self.name)
    #-def
#-class

class OptionDispatcher(object):
    """
    """
    __slots__ = [
        'LONG_PREFIX', 'SHRT_PREFIX', 'KW_DELIM',
        '__repr_short_func', '__repr_long_func',
        '__processor', '__options',
        '__halt'
    ]

    def __init__(self, processor):
        """
        """

        oc = processor.get_option_class()
        self.LONG_PREFIX = oc.LONG_PREFIX
        self.SHRT_PREFIX = oc.SHRT_PREFIX
        self.KW_DELIM = oc.KW_DELIM
        self.__repr_short_func = oc.repr_short
        self.__repr_long_func = oc.repr_long
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
                self.__processor.on_missing_key(self.__repr_long_func(opt))
            if not value:
                self.__processor.on_missing_value(self.__repr_long_func(opt))
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
                    self.__repr_short_func(opt[i])
                )
                optname = opt[i]
            if opts.is_kwoption(optname):
                v = opt[i + 1:]
                if not v:
                    self.__processor.on_missing_value(
                        self.__repr_short_func(opt[i])
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
    __slots__ = [
        '__processor',
        '__defined', '__alias2name', '__given',
        '__check_enabled'
    ]

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

        o = self.get(optname)
        return isinstance(o, Option) and not o.has_value
    #-def

    def is_kwoption(self, optname):
        """
        """

        o = self.get(optname)
        return isinstance(o, Option) and o.has_value
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
        if not self.is_kwoption(key):
            self.__processor.on_expected_kwoption(key)
        if key in self.__given:
            self.__given.remove(key)
        self.__given.append(key)
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
            if self[opt].when_given < 0 and self[opt].is_required():
                raise errcls(
                    "%s: Required option `%s' is missing" % (
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

    def get_given_options(self):
        """
        """

        l = []
        for opt in self.__given:
            l.append(self[opt])
        return l
    #-def
#-class

class OptionProcessor(object):
    """
    """
    __slots__ = [
        '__app',
        '__option_class', '__options_class', '__dispatcher_class',
            '__error_class',
        '__options', '__dispatcher'
    ]

    def __init__(self, app, **kwargs):
        """
        """

        self.__app = app
        self.__option_class = kwargs.get('option_class', Option)
        self.__options_class = kwargs.get('options_class', Options)
        self.__dispatcher_class = kwargs.get(
            'dispatcher_class', OptionDispatcher
        )
        self.__error_class = kwargs.get('error_class', ApplicationError)
        self.__options = self.__options_class(self)
        self.__dispatcher = self.__dispatcher_class(self)
    #-def

    def get_app(self):
        """
        """

        return self.__app
    #-def

    def get_option_class(self):
        """
        """

        return self.__option_class
    #-def

    def get_options_class(self):
        """
        """

        return self.__options_class
    #-def

    def get_dispatcher_class(self):
        """
        """

        return self.__dispatcher_class
    #-def

    def get_error_class(self):
        """
        """

        return self.__error_class
    #-def

    def get_options(self):
        """
        """

        return self.__options
    #-def

    def get_dispatcher(self):
        """
        """

        return self.__dispatcher
    #-def

    def process(self, argv):
        """
        """

        i = 0
        while i < len(argv) and self.__dispatcher.dispatch(argv[i]):
            i += 1
        self.__options.check()
        return i
    #-def

    def on_option_conflict(self, opt, **params):
        """
        """

        raise self.__error_class(
            "%s: Long option `%s' is already specified" % (
                self.__app.get_name(), opt
            )
        )
    #-def

    def on_alias_conflict(self, opt, **params):
        """
        """

        raise self.__error_class(
            "%s: Short option `%s' is already specified" % (
                self.__app.get_name(), opt
            )
        )
    #-def

    def on_invalid_option(self, opt, **params):
        """
        """

        raise self.__error_class(
            "%s: Invalid option `%s'" % (self.__app.get_name(), opt)
        )
    #-def

    def on_expected_option(self, opt, **params):
        """
        """

        raise self.__error_class(
            "%s: `%s' must be simple (not key-value) option" % (
                self.__app.get_name(), opt
            )
        )
    #-def

    def on_expected_kwoption(self, opt, **params):
        """
        """

        raise self.__error_class(
            "%s: `%s' must be key-value option" % (self.__app.get_name(), opt)
        )
    #-def

    def on_missing_alias(self, opt, **params):
        """
        """

        raise self.__error_class(
            "%s: Invalid option `%s'" % (self.__app.get_name(), opt)
        )
    #-def

    def on_missing_key(self, opt, **params):
        """
        """

        raise self.__error_class(
            "%s: `%s' - missing key" % (self.__app.get_name(), opt)
        )
    #-def

    def on_missing_value(self, opt, **params):
        """
        """

        pass
    #-def
#-class
