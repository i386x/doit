DoIt! Language Interpreter API
==============================

This document describes DoIt! interpreter from a programmer's point of view.
The whole DoIt! interpreter is written in Python 3 and divided into several
modules. The heart of DoIt! interpreter is situated in runtime module, which
contains the virtual machine implementation.

DoIt! Modules
-------------

This section contains a reference guide to all DoIt! modules and packages.

.. module:: support
   :synopsis: DoIt! auxiliary routines and classes.

:mod:`doit.support` -- DoIt! auxiliary routines and classes
```````````````````````````````````````````````````````````

This module contains various submodules commonly used by other parts of DoIt!
language interpreter.

.. module:: support.utils
   :synopsis: DoIt! utilities.

:mod:`doit.support.utils` -- DoIt! utilities
''''''''''''''''''''''''''''''''''''''''''''

General purpose utility functions and classes.

.. autofunction:: doit.support.utils.sys2path

.. autofunction:: doit.support.utils.path2sys

.. autoclass:: doit.support.utils.WithStatementExceptionHandler
   :members:
   :private-members:
   :special-members:

.. autofunction:: doit.support.utils.doit_read

.. autoclass:: doit.support.utils.Collection
   :members:
   :private-members:
   :special-members:

.. module:: asm
   :synopsis: Assembly language interfaces.

:mod:`doit.asm` -- Assembly language interfaces
```````````````````````````````````````````````

Since writing the binary code by hand may be tedious, this module provides an
interface for writing the code in assebly language way. This module contains an
abstract assembler class as a base interface class and several concrete
assembler implementations, one per concrete architecture. Asseblers are
designed as fluent interfaces. That is, for every assembly instruction there is
a corresponding method which, when invoked, writes the binary representation of
instruction to the buffer and returns its owner, which is of course an instance
of assembler, so the method invokations can be chained.

.. module:: asm.asm
   :synopsis: Abstract assembler.

:mod:`doit.asm.asm` -- Abstract assembler
'''''''''''''''''''''''''''''''''''''''''

Common interface for all concrete assembler implementations.

.. autoclass:: doit.asm.asm.AbstractOperand
   :members:
   :private-members:
   :special-members:
