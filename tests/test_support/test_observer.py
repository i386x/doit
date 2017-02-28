#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_support/test_observer.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-02-26 21:00:17 (UTC+01:00, DST+00:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Observer module tests.\
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

import unittest

from doit.support.errors import DoItNotImplementedError

from doit.support.observer import Observable, Observer

class Client(Observable):
    __slots__ = [ '__name', '__message' ]

    def __init__(self, name):
        Observable.__init__(self)
        self.__name = name
        self.__message = ""
    #-def

    def send_message(self, msg):
        self.__message = msg
        self.notify()
    #-def

    def get_state(self):
        return "%s(%s)" % (self.__name, self.__message)
    #-def
#-class

class Server(Observer):
    __slots__ = [ 'result' ]

    def __init__(self):
        Observer.__init__(self)
        self.result = []
    #-def

    def update(self, notifier):
        self.result.append(notifier.get_state())
    #-def
#-class

class NamedServer(Server):
    __slots__ = [ '__name' ]

    def __init__(self, name):
        Server.__init__(self)
        self.__name = name
    #-def

    def __eq__(self, rhs):
        return self.__name == rhs.__name
    #-def
#-class

class TestObserverCase(unittest.TestCase):

    def test_observable_get_state_is_not_implemented(self):
        with self.assertRaises(DoItNotImplementedError):
            Observable().get_state()
    #-def

    def test_observer_update_is_not_implemented(self):
        with self.assertRaises(DoItNotImplementedError):
            Observer().update(Observable())
    #-def

    def test_observer_observable_basic_communication(self):
        s1 = Server()
        s2 = Server()
        s3 = Server()
        c1 = Client("a")
        c2 = Client("b")
        c3 = Client("c")

        c1.attach(s1)
        c1.attach(s2)
        c2.attach(s2)
        c2.attach(s3)
        c3.attach(s1)
        c3.attach(s3)

        self.assertEqual(s1.result, [])
        self.assertEqual(s2.result, [])
        self.assertEqual(s3.result, [])
        c1.send_message("m1")
        self.assertEqual(s1.result, ["a(m1)"])
        self.assertEqual(s2.result, ["a(m1)"])
        self.assertEqual(s3.result, [])
        c2.send_message("m2")
        self.assertEqual(s1.result, ["a(m1)"])
        self.assertEqual(s2.result, ["a(m1)", "b(m2)"])
        self.assertEqual(s3.result, ["b(m2)"])
        c3.send_message("m3")
        self.assertEqual(s1.result, ["a(m1)", "c(m3)"])
        self.assertEqual(s2.result, ["a(m1)", "b(m2)"])
        self.assertEqual(s3.result, ["b(m2)", "c(m3)"])
        c1.detach(s2)
        c1.send_message("m4")
        self.assertEqual(s1.result, ["a(m1)", "c(m3)", "a(m4)"])
        self.assertEqual(s2.result, ["a(m1)", "b(m2)"])
        self.assertEqual(s3.result, ["b(m2)", "c(m3)"])
        c1.detach(s2)
    #-def

    def test_observer_equality(self):
        c1 = Client("x")
        s1 = NamedServer("A1")
        s2 = NamedServer("A1")
        s3 = NamedServer("B1")

        c1.attach(s1)
        c1.attach(s3)
        c1.attach(s2)

        self.assertEqual(s1.result, [])
        self.assertEqual(s2.result, [])
        self.assertEqual(s3.result, [])
        c1.send_message("m5")
        self.assertEqual(s1.result, ["x(m5)"])
        self.assertEqual(s2.result, [])
        self.assertEqual(s3.result, ["x(m5)"])
        c1.detach(s2)
        c1.send_message("m6")
        self.assertEqual(s1.result, ["x(m5)"])
        self.assertEqual(s2.result, [])
        self.assertEqual(s3.result, ["x(m5)", "x(m6)"])
        c1.detach(s1)
        c1.detach(s2)
        c1.detach(s3)
        c1.send_message("m7")
        self.assertEqual(s1.result, ["x(m5)"])
        self.assertEqual(s2.result, [])
        self.assertEqual(s3.result, ["x(m5)", "x(m6)"])
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestObserverCase))
    return suite
#-def
