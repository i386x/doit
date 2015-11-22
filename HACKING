Source file format
==================

* encoding: UTF-8, no BOM
* line endings: UNIX style (0x0A)
* max. line length: 80 characters (including LF)
* allowed white spaces: 0x20 (SPACE), 0x0A (LF)
* header comment format::

#                                                         -*- coding: utf-8 -*-
#! \file    ./path/to/file.py
#! \author  Name Surname, <email@server.com>
#! \stamp   yyyy-mm-dd HH:MM:SS (UTC+HH:MM, DST+HH:MM)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   @pyfile.docstr
#

* \file must reflect the real position of source file
* version (for now) must be 0.0.0

* doc string
* license::

__license__ = """\
Copyright (c) 2014 - 2015 Name Surname.

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

* license must be MIT with 2014 - 2015

* standard Python library imports
* 3rd party libraries imports
* DoIt! modules imports:

  - in the order of their definitions in imported module

* constants

* classes:

  - class must be derived from object or Exception
  - doc string:

    * brief info about class

    * class variables (visible to user)::

          :cvar type name: Description.

          or

          :cvar name: Description.
          :vartype name: :class:`type`

    * member variables (visible to user)::

          :ivar type name: Description.

          or

          :ivar name: Description.
          :vartype name: :class:`type`

  - class variables definitions
  - __slots__

  - methods:

    * doc string:

      - brief info
      - params (use backslash and indentation if the line limit was exceeded)::

            :param type name: Description.

            or

            :param name: Description.
            :type name: :class:`type`

      - returns (use backslash and indentation if the line limit was
        exceeded)::

            :returns: Description (:class:`type`).

      - raises (use backslash and indentation if the line limit was exceeded)::

            :raises exception: Reason.

            or

            :raises ~DoItException: Reason.

      - notes

    * ``#-def``

  - ``#-class``

* routines (see methods)

Test directory format
=====================

* test directory must reflects the source directory

  - ``test_`` prefix must appears at the begining of the each file and
    directory name

* test files have the structure very similar to source files, except:

  - no doc strings are used (except file doc string)
  - auxiliary subroutines and classes must appear before tests
  - classes derived from ``unittest.TestCase`` do not have ``__slots__``

Documentation
=============

* links between objects must work

  - there are some exceptions:

    * :class:`traceback` -- not documented in the official Python documentation

* the order of documented stuff must reflects the order in source file
