#                                                         -*- coding: utf-8 -*-
#! \file    ./doit/support/observer.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-10 23:00:07 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Observer.\
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

class Observable(object):
    """
    """
    __slots__ = [ '__listeners' ]

    def __init__(self):
        """
        """

        self.__listeners = []
    #-def

    def attach(self, listener):
        """
        """

        if listener not in self.__listeners:
            self.__listeners.append(listener)
    #-def

    def detach(self, listener):
        """
        """

        while listener in self.__listeners:
            self.__listeners.remove(listener)
    #-def

    def notify(self):
        """
        """

        for listener in self.__listeners:
            listener.update(self)
    #-def

    def get_state(self):
        """
        """

        not_implemented()
    #-def
#-class

class Observer(object):
    """
    """
    __slots__ = []

    def __init__(self):
        """
        """

        pass
    #-def

    def update(self, notifier):
        """
        """

        not_implemented()
    #-def

    def __eq__(self, rhs):
        """
        """

        return id(self) == id(rhs)
    #-def
#-class
