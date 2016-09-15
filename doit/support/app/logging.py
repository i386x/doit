#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/app/logging.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-09-11 21:50:10 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Logging.\
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

import os

from doit.support.utils import timestamp

from doit.support.app.errors import ApplicationError
from doit.support.app.io import CharBuffer

class StreamWrapper(object):
    """
    """
    __slots__ = [ '__log', '__stream', '__logging_on' ]

    def __init__(self, log, stream):
        """
        """

        self.__log = log
        self.__stream = stream
        self.__logging_on = True
    #-def

    def logging_on(self, logging_on = True):
        """
        """

        self.__logging_on = logging_on
    #-def

    def write(self, s):
        """
        """

        if self.__logging_on:
            self.__log.write(s)
        self.__stream.write(s)
    #-def
#-class

class Log(CharBuffer):
    """
    """
    __slots__ = [
        '__streams',
        '__log_dir',
        '__fmode', '__fencoding', '__fnewline', '__fd',
        '__error_class'
    ]

    def __init__(self, app, **kwargs):
        """
        """

        CharBuffer.__init__(self, app, **kwargs)
        self.__streams = {}
        self.__log_dir = kwargs.get('log_dir', "log")
        self.__log_dir = os.path.join(app.get_dir(), self.__log_dir)
        self.__fmode = kwargs.get('logfile_mode', "a")
        if self.__fmode not in ["w", "a"]:
            self.__fmode = "a"
        self.__fencoding = kwargs.get('logfile_enc', 'utf-8')
        self.__fnewline = kwargs.get('logfile_nl', "\n")
        self.__fd = None
        self.__error_class = kwargs.get('error_class', ApplicationError)
    #-def

    def wrap(self, **streams):
        """
        """

        for stream in streams:
            self.__streams[stream] = StreamWrapper(self, streams[stream])
        return self
    #-def

    def __getattribute__(self, attr):
        """
        """

        clsname = CharBuffer.__getattribute__(self, '__class__').__name__
        _ = lambda x: x.startswith('__') and '_%s%s' % (clsname, x) or x
        streams = CharBuffer.__getattribute__(self, _('__streams'))
        if attr in streams:
            return streams[attr]
        return CharBuffer.__getattribute__(self, attr)
    #-def

    def __enter__(self):
        """
        """

        self.on_enter()
        return self
    #-def

    def __exit__(self, et, ev, etb):
        """
        """

        if self.__fd:
            self.__fd.close()
            self.__fd = None
        return False
    #-def

    def on_enter(self):
        """
        """

        self.mkdir(self.log_dir())
        self.mkdir(os.path.join(self.log_dir(), self.app_name()))
        self.fopen(
            os.path.join(self.log_dir(), self.app_name(), self.log_name()),
            mode = self.fmode(),
            encoding = self.fencoding(),
            newline = self.fnewline()
        )
    #-def

    def header(self):
        """
        """

        ts = timestamp()
        return "[Logged at %s]\n" % (
            "%s %s (UTC%s, DST%s)" % (
                "%(year)04d-%(month)02d-%(day)02d" % ts,
                "%(hour)02d:%(min)02d:%(sec)02d" % ts,
                "%(utcsign)s%(utchour)02d:%(utcmin)02d" % ts,
                "+%(dsthour)02d:%(dstmin)02d" % ts
            )
        )
    #-def

    def footer(self):
        """
        """

        return "[End of log record]\n\n"
    #-def

    def flush(self):
        """
        """

        fd = self.logfile()
        if not fd or fd.closed:
            return
        fd.write(self.header())
        s = str(self)
        fd.write(s)
        if not s or s[-1] != '\n':
            fd.write('\n')
        fd.write(self.footer())
    #-def

    def mkdir(self, dirname):
        """
        """

        try:
            dirname = os.path.realpath(dirname)
            if not os.path.exists(dirname):
                os.mkdir(dirname)
            elif os.path.isfile(dirname):
                raise OSError("Can't create directory '%s'" % dirname)
        except Exception as e:
            raise self.__error_class(str(e))
    #-def

    def fopen(self, path, mode = "a", encoding = 'utf-8', newline = '\n'):
        """
        """

        if self.__fd and not self.__fd.closed:
            self.__fd.close()
        try:
            self.__fd = open(
                os.path.realpath(path),
                mode = mode,
                encoding = encoding,
                newline = newline
            )
        except Exception as e:
            self.__fd = None
            raise self.__error_class(str(e))
    #-def

    def log_dir(self):
        """
        """

        return self.__log_dir
    #-def

    def app_name(self):
        """
        """

        return os.path.splitext(os.path.basename(self.get_app().get_path()))[0]
    #-def

    def log_name(self):
        """
        """

        d = dict(appname = self.app_name())
        d.update(timestamp())
        return "%(appname)s-%(year)04d%(month)02d%(day)02d.log" % d
    #-def

    def fmode(self):
        """
        """

        return self.__fmode
    #-def

    def fencoding(self):
        """
        """

        return self.__fencoding
    #-def

    def fnewline(self):
        """
        """

        return self.__fnewline
    #-def

    def logfile(self):
        """
        """

        return self.__fd
    #-def
#-class
