.. _doit-dev-basics:

.. admonition:: TODO
   :class: warning

   Update this doc after first version of |doit| will be released.

Basic Concepts
==============

|doit| consists of these following parts:

* |doit| `Bootstrap` -- depending on the host system configuration, initializes
  the |doit| `Core`
* |doit| `Virtual Machine` -- interprets |doit| instructions
* |doit| `Just-In-Time Compiler` (`JIT`) -- compiles |doit| core and |doit|
  applications to the native code
* |doit| `Core` -- a set of core modules for scanning, parsing, type checking,
  compiling, optimizing, managing resources, runtime support etc.
