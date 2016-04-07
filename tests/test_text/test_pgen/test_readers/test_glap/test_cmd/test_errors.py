#                                                         -*- coding: utf-8 -*-
#! \file    ./tests/test_text/test_pgen/ \
#!              test_readers/test_glap/test_cmd/test_errors.py
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2016-04-06 20:37:59 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#
"""\
Glap reader command processor error module tests.\
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

import unittest

from doit.text.pgen.readers.glap.cmd.errors import \
    COMMAND_PROCESSOR_ERROR_BASE, \
    CommandProcessorError

class AuxTraceback(object):
    __slots__ = [ '__content' ]

    def __init__(self, content):
        self.__content = content
    #-def

    def __str__(self):
        return ".".join(self.__content)
    #-def
#-class

class AuxTracebackProvider(object):
    __slots__ = [ '__content' ]

    def __init__(self, *content):
        self.__content = list(content)
    #-def

    def traceback(self):
        return AuxTraceback(self.__content)
    #-def
#-class

class TestCommandProcessorErrorCase(unittest.TestCase):

    def test_CommandProcessorError(self):
        error_code = COMMAND_PROCESSOR_ERROR_BASE
        error_message = "Dummy error message"
        traceback_provider = AuxTracebackProvider("f1", "f2", "g3")

        with self.assertRaises(CommandProcessorError) as eh:
            raise CommandProcessorError(
                traceback_provider, error_code, error_message
            )

        self.assertEqual(str(eh.exception), "")
    #-def
#-class

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommandProcessorErrorCase))
    return suite
#-def
