#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/app/io.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-08-30 10:58:45 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Input/Output services.\
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

from doit.support.errors import not_implemented
from doit.support.utils import WithStatementExceptionHandler

class AbstractStream(object):
    """
    """
    __slots__ = [ '__app' ]

    def __init__(self, app, **kwargs):
        """
        """

        self.__app = app
    #-def

    def get_app(self):
        """
        """

        return self.__app
    #-def

    def read(self, n = -1):
        """
        """

        not_implemented()
    #-def

    def write(self, data):
        """
        """

        not_implemented()
    #-def

    def seek(self, offset, from_what = 0):
        """
        """

        not_implemented()
    #-def

    def tell(self):
        """
        """

        not_implemented()
    #-def

    def size(self):
        """
        """

        not_implemented()
    #-def
#-class

class Buffer(AbstractStream):
    """
    """
    __slots__ = [ '__pos' ]

    def __init__(self, app, **kwargs):
        """
        """

        AbstractStream.__init__(self, app, **kwargs)
        self.__pos = 0
    #-def

    def seek(self, offset, from_what = 0):
        """
        """

        if from_what == 0:
            self.__pos = offset
        elif from_what == 1:
            self.__pos += offset
        elif from_what == 2:
            self.__pos = self.size() + offset
        if self.__pos < 0:
            self.__pos = 0
        if self.__pos > self.size():
            self.__pos = self.size()
    #-def

    def tell(self):
        """
        """

        return self.__pos
    #-def
#-class

class CharBuffer(Buffer):
    """
    """
    __slots__ = [ '__content' ]

    def __init__(self, app, **kwargs):
        """
        """

        Buffer.__init__(self, app, **kwargs)
        self.__content = []
    #-def

    def read(self, n = -1):
        """
        """

        if n < 0:
            s = ''.join(self.__content[self.tell():])
            self.seek(0, 2)
            return s
        i = self.tell()
        j = i + n
        s = ''.join(self.__content[i:j])
        self.seek(j)
        return s
    #-def

    def write(self, data):
        """
        """

        self.__content.extend(data)
    #-def

    def size(self):
        """
        """

        return len(self.__content)
    #-def

    def __str__(self):
        """
        """

        return ''.join(self.__content)
    #-def
#-class

class OutputProxy(AbstractStream):
    """
    """
    __slots__ = [ '__outfunc' ]

    def __init__(self, app, **kwargs):
        """
        """

        AbstractStream.__init__(self, app, **kwargs)
        self.__outfunc = kwargs.get('outfunc', app.wout)
    #-def

    def write(self, data):
        """
        """

        self.__outfunc(data)
    #-def
#-class

def read_all(path):
    """
    """

    wseh = WithStatementExceptionHandler()
    content = ""
    with wseh, open(path, 'r', encoding = None, newline = None) as f:
        content = f.read()
    if wseh.etype:
        return None
    return content
#-def

def write_items(path, items, p):
    """
    """

    wseh = WithStatementExceptionHandler()
    with wseh, open(path, 'w', encoding = 'utf-8', newline = '\n') as f:
        for x in items:
            f.write(p(x))
    return wseh.etype is None
#-def
