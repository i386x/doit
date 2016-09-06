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

from doit.support.app.errors import \
    ApplicationError, ApplicationExit

from doit.support.app.printer import \
    TableBuilder

from doit.support.app.options import \
    OptionProcessor

class Application(object):
    """
    """
    __slots__ = [
        '__owner', '__name',
        '__option_processor_class', '__table_class',
        '__option_processor', '__pending_args',
        '__exitcode',
        '__output', '__log', '__error_log'
    ]

    def __init__(self, owner = None, **kwargs):
        """
        """

        self.__owner = owner
        self.__name = None
        self.__option_processor_class = kwargs.get(
            'option_processor_class', OptionProcessor
        )
        self.__table_class = kwargs.get('table_class', TableBuilder)
        self.__option_processor = self.__option_processor_class(self, **kwargs)
        self.__pending_args = []
        self.__exitcode = 0
        self.__output = None
        self.__log = None
        self.__error_log = None
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

    def get_option_processor_class(self):
        """
        """

        return self.__option_processor_class
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

    def get_output(self):
        """
        """

        return self.__output
    #-def

    def set_log(self, log):
        """
        """

        self.__log = log
    #-def

    def get_log(self):
        """
        """

        return self.__log
    #-def

    def set_error_log(self, error_log):
        """
        """

        self.__error_log = error_log
    #-def

    def get_error_log(self):
        """
        """

        return self.__error_log
    #-def

    def run(self, argv = sys.argv[:]):
        """
        """

        if not self.__name:
            if argv and argv[0]:
                self.__name = argv[0]
                argv = argv[1:]
            else:
                self.__name = "<app-name>"
        try:
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

        oc = self.__option_processor.get_option_class()
        self.__option_processor.get_options()[name] = oc(name,
            short_aliases = shorts, about = about, action_callback = cb,
            flags = flags, default = default
        )
    #-def

    def define_kwoption(self, name,
        shorts = [], about = "", cb = (lambda opt: None), flags = 0,
        default = None, value_meta = "value"
    ):
        """
        """

        oc = self.__option_processor.get_option_class()
        self.__option_processor.get_options()[name] = oc(name,
            short_aliases = shorts, about = about, about_value = value_meta,
            action_callback = cb, flags = flags, default = default,
            has_value = True
        )
    #-def

    def list_options(self, **tspec):
        """
        """

        options = self.__option_processor.get_options().get_defined_options()
        if not tspec:
            tspec['col0'] = 24
            tspec['sep0'] = 2
            tspec['col1'] = 50
        table = self.__table_class(**tspec)
        for opt in options:
            table.row(*(opt.helprow()))
        return table
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

    def wout(self, s):
        """
        """

        if self.__output:
            self.__output.write(str(s))
    #-def

    def wlog(self, s):
        """
        """

        if self.__log:
            self.__log.write(str(s))
    #-def

    def werr(self, s):
        """
        """

        if self.__error_log:
            self.__error_log.write(str(s))
    #-def

    def exit(self, ec = 0):
        """
        """

        self.set_exitcode(ec)
        raise ApplicationExit()
    #-def
#-class
