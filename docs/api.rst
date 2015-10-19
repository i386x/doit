.. _doit-api:

`DoIt!` Core API
================

In this documentation, you can find the description of `DoIt!` core modules
(those written in Python 3, not the `DoIt!` standard library), `DoIt!` design
concepts and a many tutorials and examples which can help you to understand how
all the mentioned stuff works together.

.. _introduction:

Gentle introduction to `DoIt!` architecture
-------------------------------------------

The `DoIt!` was designed as a framework for creating a programming (or
scripting) languages and their compilers (or interpreters). The core of `DoIt!`
was written in Python 3 and is distributed via several modules:

* :mod:`doit.support <support>` -- commonly used functions and classes

  - :mod:`doit.support.errors <support.errors>` -- error codes and exceptions
  - :mod:`doit.support.utils <support.utils>` -- utility functions and classes

.. SUGGESTION: split runtime to runtime and interpreter?

* :mod:`doit.runtime <runtime>` -- `DoIt!` virtual machine and its services

  - :mod:`doit.runtime.memory <runtime.memory>` -- a memory of `DoIt!` virtual
    machine
  - :mod:`doit.runtime.inst <runtime.inst>` -- the instruction set of `DoIt!`
    virtual machine
  - :mod:`doit.runtime.vm <runtime.vm>` -- `DoIt!` virtual machine

* :mod:`doit.asm <asm>` -- assembler interfaces

  - :mod:`doit.asm.asm <asm.asm>` -- common assembler interfaces
  - :mod:`doit.asm.doit_asm <asm.doit_asm>` -- `DoIt!` assembler

.. TODO: parsing
.. TODO: io
.. TODO: codegen
.. SUGGESTION: add a reflector which could compile these modules to
..             DoIt! intial language

The dependency diagram between all these modules is presented below (this is
not actually an import diagram):

.. raw:: html

     <center>

.. graphviz::
   :caption: The dependency diagram between `DoIt!` core modules.

     digraph DoIt_modules_dependencies {
       node [shape = record];

       errors [label = "<errors> doit.support.errors"];
       utils [label = "<utils> doit.support.utils"];
       memory [label = "<memory> doit.runtime.memory"];
       inst [label = "<inst> doit.runtime.inst"];
       vm [label = "<vm> doit.runtime.vm"];
       asm [label = "<asm> doit.asm.asm"];
       doit_asm [label = "<doit_asm> doit.asm.doit_asm"];

       doit_asm:doit_asm -> asm:asm;
       doit_asm:doit_asm -> inst:inst;
       doit_asm:doit_asm -> errors:errors;

       asm:asm -> errors:errors;

       vm:vm -> memory:memory;
       vm:vm -> inst:inst;
       vm:vm -> utils:utils;
       vm:vm -> errors:errors;

       memory:memory -> errors:errors;

       inst:inst -> asm:asm;
       inst:inst -> doit_asm:doit_asm;
       inst:inst -> vm:vm;
       inst:inst -> memory:memory;
       inst:inst -> errors:errors;

       utils:utils -> errors:errors;
     }

.. raw:: html

     </center>

Next, we describe a bit more the particular nodes of the diagram above and the
dependencies between them.

.. _error-system:

`DoIt!` error system
--------------------

As you can see, every module in `DoIt!` depends on :mod:`doit.support.errors
<support.errors>` module. In this module is defined the base exception for all
exceptions which may occur inside `DoIt!`: :exc:`DoItError
<doit.support.errors.DoItError>`. That is, all exceptions raised inside `DoIt!`
should be derived from :exc:`DoItError <doit.support.errors.DoItError>`.

:exc:`DoItError <doit.support.errors.DoItError>` :meth:`constructor
<doit.support.errors.DoItError>` takes 2 arguments: an `error code` and an
`error message`. The maximal number of error codes should be 256 and the
following conventions should be kept:

* 0 -- no error
* 1, 2, 3, ... -- `DoIt!` internal errors
* 254, 253, 252, ... -- user defined errors
* 255 -- unknown error

In `DoIt!`, errors are handled either by the user code, before the `DoIt!`
virtual machine starts, or by the `DoIt!` virtual machine itself.

.. admonition:: About error handling inside the `DoIt!` virtual machine
   :class: note

   When a :exc:`DoItError <doit.support.errors.DoItError>` based exception is
   caught inside the `DoIt!` virtual machine and error flag was not set before,
   the `DoIt!` virtual machine stores its current state onto the execution
   stack and calls an error handler stored in register ``eh``. Otherwise, the
   `DoIt!` virutal machine is abnormally aborted. See also :ref:`vm`.

The following example shows you what to do if you want to define your own error
that should be handled inside `DoIt!`. First, define your error code::

    MY_ERROR = 254

then define your error::

    from doit.support.errors import DoItError

    class MyError(DoItError):
        __slots__ = []

        def __init__(self, emsg):
            DoItError.__init__(self, MY_ERROR, emsg)

now, you can use ``MyError`` inside your `DoIt!` based project.

.. SUGGESTIONS: error code allocator, error subgroups

.. _utilities:

`DoIt!` utilities
-----------------

The :mod:`doit.support.utils <support.utils>` provides two classes:

* :class:`WithStatementExceptionHandler
  <doit.support.utils.WithStatementExceptionHandler>`
* :class:`Collection <doit.support.utils.Collection>`

The :class:`WithStatementExceptionHandler
<doit.support.utils.WithStatementExceptionHandler>` class, as its name say, can
catch an exception raised within the ``with`` statement. Example::

    def fread(name, encoding = 'utf-8'):
        content = ""
        wseh = WithStatementExceptionHandler()
        with wseh, open(name, 'r', encoding = encoding) as f:
            content = f.read()
        if wseh.evalue is not None:
            return None
        return content

In the example above, if the opening or reading the file `name` fails, the
raised exception is caught by ``wseh`` and stored in its member variables
``etype``, ``evalue`` and ``etraceback``.

The :class:`Collection <doit.support.utils.Collection>` class provides a
generator for unique objects. You can generate two type of unique objects:
`named` and `anonymous`. To generate anonymous objects, just type::

    anonymous_object = Collection()

and to generate named object, just type::

    TokenTypes = Collection("TokenTypes")

.. note::

   The name of named unique object must begin with upper case letter.

Each generated object has attributes ``name`` and ``qname``. The ``name``
attribute returns the name and the ``qname`` attribute returns the qualified
(full) name of the object.

Since the generated unique object is an instance of :class:`Collection
<doit.support.utils.Collection>`, it can be used as a generator for unique
objects too. Such object is generated under the scope of its generator so its
inherits its name::

    WhiteSpace = TokenTypes.WhiteSpace
    Idendifier = TokenTypes.Identifier
    String = TokenTypes.String

    Comment = WhiteSpace.Comment
    NewLine = WhiteSpace.NewLine

Observe that the name of the newly generated object (the part after the dot)
starts with upper case letter. On this example, we can demonstrate the
difference between ``name`` and ``qname``::

    >>> Comment.name
    'Comment'
    >>> Comment.qname
    'TokenTypes.WhiteSpace.Comment'

The ``name`` and ``qname`` of anonymous object is its Python representation
string::

    >>> anonymous_object.name
    '<Collection object at 0x0000000002637BE0>'
    >>> anonymous_object.qname
    '<Collection object at 0x0000000002637BE0>'

.. admonition:: Tips
   :class: note

   1) You can get the qualified name of the object also by using the
      :func:`repr` operator::

          >>> repr(anonymous_object)
          '<Collection object at 0x0000000002637BE0>'
          >>> repr(NewLine)
          'TokenTypes.WhiteSpace.NewLine'

   #) You can of course use as generators an anonymous objects, but this is not
      recomended::

          >>> repr(anonymous_object.SomeStuff)
          '<Collection object at 0x0000000002637BE0>.SomeStuff'

While generating new unique objects, they can inherit the subobjects from the
old ones. To do this, we first define some unique objects, most of them with
subobjects::

    Fruit = Collection('Fruit')
    Apple = Fruit.Apple

    Vegetable = Collection('Vegetable')
    Carrot = Vegetable.Carrot
    LittleCarrot = Carrot.LittleCarrot

    Empty = Collection('Empty')

    Apiaceae = Collection('Apiaceae')
    AnotherCarrot = Apiaceae.Carrot

then, we type::

    Food = Collection('Food', \
        'Fruit', 'Vegetable', 'Vegetable.Carrot', 'Empty', 'Apiaceae'
    )

Now, we look what subobjects are contained in ``Food``::

    >>> Food.Apple is Apple
    True
    >>> Food.Carrot is Carrot
    False
    >>> Food.LittleCarrot is LittleCarrot
    True
    >>> Food.Carrot is AnotherCarrot
    True

From ``Fruit`` was copied ``Apple``, from ``Vegetable`` was copied ``Carrot``,
from ``Vegetable.Carrot`` was copied ``LittleCarrot``, nothing was copied from
``Empty``, and from ``Apiaceae`` was copied ``Carrot`` which overwrites the
``Carrot`` copied from ``Vegetable``.

To test whether the one object is contained in another object as its subobject,
you can use the ``in`` operator::

    >>> A = Collection('A')
    >>> B = A.B
    >>> C = B.C
    >>> C in A
    True
    >>> A in C
    False

.. note::

   To resolve the object containment, the ``in`` operator use the qualified
   names of objects.

Last, it is time to say something about :meth:`Collection.lock()
<doit.support.utils.Collection.lock>` and :meth:`Collection.unlock()
<doit.support.utils.Collection.unlock>` class methods. These class methods are
used to disable/enable the capability of generating new unique objects.
Consider the following example::

    #
    # token.type can be:
    # -- TokenTypes.Identifier
    # -- TokenTypes.WhiteSpace
    # -- TokenTypes.String
    #
    if token.type is TokenTypes.Identifear:
        symbol_table.save(token)

If :class:`Collection <doit.support.utils.Collection>` is :meth:`unlocked
<doit.support.utils.Collection.unlock>`, the new unique object called
``Identifear`` is generated and since its uniqueness, the ``token`` is never
saved into the ``symbol_table``. On the other hand, if :class:`Collection
<doit.support.utils.Collection>` is :meth:`locked
<doit.support.utils.Collection.lock>`, the :exc:`DoItAssertionError
<doit.support.errors.DoItAssertionError>` exception is raised since
``Identifear`` does not exist (was never generated before), and the programmer
must find and correct this typo. Thus, if you want to generate your own unique
objects, use the following pattern::

    Collection.unlock()

    MyUniqueObject = Collection('MyUniqueObject')
    SymbolA = MyUniqueObject.SymbolA
    SymbolB = MyUniqueObject.SymbolB
    SymbolC = MyUniqueObject.SymbolC

    Collection.lock()

.. _vm:

`DoIt!` virtual machine
-----------------------

The `DoIt!` :class:`virtual machine <doit.runtime.vm.Interpreter>`, situated in
:mod:`doit.runtime.vm <runtime.vm>` module, is designed as a stack-based
virtual machine with a necessary number of registers. It relies on
:class:`Memory <doit.runtime.memory.Memory>` class that manages the three
separated memory areas inside `DoIt!` virtual machine, mapped to the three
corresponding `segment registers` (we assume that the instance of `DoIt!`
virtual machine is stored in ``vm``):

* ``vm.cs`` (code segment register) -- this register refers to :class:`Memory
  <doit.runtime.memory.Memory>` where the instructions are stored
* ``vm.ds`` (data segment register) -- this register refers to auxiliary
  :class:`Memory <doit.runtime.memory.Memory>` space
* ``vm.ss`` (stack segment register) -- this register refers to :class:`Memory
  <doit.runtime.memory.Memory>` used as execution stack

The `DoIt!` virtual machine has also two registers to support the subroutines
and stack manipulation:

* ``vm.sp`` (stack pointer) -- points to the top of the execution stack
* ``vm.fp`` (frame pointer) -- points to the frame of the most recently invoked
  subroutine on the execution stack

.. admonition:: The execution stack and stackframe
   :class: note

   The execution stack of the `DoIt!` virtual machine grows towards to higher
   addresses. That is, the ``vm.sp`` value is also the number of items pushed
   onto the execution stack.

   The structure of stackframe is a similar as in C programming language:

   .. raw:: html

        <center>

   .. graphviz::

        digraph StackFrame {
          rankdir = LR;

          pnode [shape = point, width = 0.01, height = 0.01, fixedsize = true];
          next_frame [shape = none, margin = 0, label = <next frame>];
          {rank = same; pnode; next_frame;}
          stackframe [shape = record, label = "\
            <a> Mth local variable\
            |\
            <b> ...\
            |\
            <c> 1st local variable\
            |\
            <d> 0th local variable\
            |\
            <e> old vm.fp\
            |\
            <f> return address\
            |\
            <g> 0th argument\
            |\
            <h> 1st argument\
            |\
            <i> ...\
            |\
            <j> Nth argument\
          "];
          fpreg [shape = none, margin = 0, label = <vm.fp>];

          pnode -> stackframe:e [arrowhead = none];
          next_frame -> stackframe:j [style = invis];
          stackframe:d -> fpreg [style = invis];
          fpreg -> stackframe:d;
          pnode -> next_frame [minlen = 5];
          stackframe:e -> next_frame [style = invis];
        }

   .. raw:: html

        </center>

   The `return address` is either `offset` (near call) or `segment:offset` (far
   call), where `segment` is pushed onto the stack earlier than `offset`.

Another important registers are:

* ``vm.ip`` (instruction pointer) -- points to the current instruction to be
  executed
* ``vm.flags`` -- the execution flags
* ``vm.status`` -- the `DoIt!` virtual machine state
* ``vm.eh`` (error handler pointer) -- points to the error handling subroutine

In ``vm.flags``, the combination of the following values can be considered
(defined in :mod:`doit.runtime.vm <runtime.vm>`)::

    ZF = 1 << 0  # zero flag
    SF = 1 << 1  # sign flag
    EF = 1 << 2  # error flag

The value of ``vm.flags`` can influence the result of execution of several
instructions. On the other hand, some instructions can change the ``vm.flags``
value (see the :ref:`vm-inst` below). The only possible values of ``vm.status``
are (also defined in :mod:`doit.runtime.vm <runtime.vm>`)::

    STOPPED = Collection('VM').Status.STOPPED
    RUNNING = Collection('VM').Status.RUNNING
    ABORTED = Collection('VM').Status.ABORTED

.. note::

   The initial values of the `DoIt!` virtual machine registers are::

       vm.cs = Memory()
       vm.ds = Memory()
       vm.ss = Memory()
       vm.sp = 0
       vm.fp = 0
       vm.ip = 0
       vm.flags = 0
       vm.status = STOPPED
       vm.eh = 0

The heart of `DoIt!` virtual machine is the :meth:`run()
<doit.runtime.vm.Interpreter.run>` method. When :meth:`run()
<doit.runtime.vm.Interpreter.run>` is called, the `DoIt!` virtual machine
enters to ``RUNNING`` state and executes the instruction from ``vm.cs[vm.ip]``
location. If this instruction raise an :exc:`DoItError` based exception, these
steps are performed:

1. First, the ``vm.flags`` is checked that error flag (``EF``) is not set. If
   the error flag was set before, the `DoIt!` virtual machine is aborted (i.e.
   it enters to ``ABORTED`` state and calls :meth:`on_abort(ecode, emsg)
   <doit.runtime.vm.Interpreter.on_abort>` callback).
#. The current state of the `DoIt!` virtual machine is stored onto the
   execution stack as a stackframe with the following structure:

   .. raw:: html

        <center>

   .. graphviz::

        digraph ErrorStackFrame {
          rankdir = LR;

          stackframe [shape = record, label = "\
            <a> old vm.fp\n\
            (next frame)
            |\
            <b> return address\
            |\
            <c> error code\
            |\
            <d> error message\
            |\
            <e> vm.cs\
            |\
            <f> vm.ds\
            |\
            <g> vm.ss\
            |\
            <h> old vm.sp\
            |\
            <i> old vm.fp\
            |\
            <j> old vm.ip\
            |\
            <k> old vm.flags\
          "];
        }

   .. raw:: html

        </center>

#. The error flag is set.
#. The instruction pointer is set to the address given by ``vm.eh`` (i.e. the
   jump to the error handling subroutine is performed).

.. note::

   The error flag must be cleared manually before the return from the error
   handling subroutine.

Whenever the other type of exception occurs, the `DoIt!` virtual machine is
aborted. After the instruction was executed, the instruction pointer is
advanced by one and whole process is repeated. The `DoIt!` virtual machine is
properly halted when it enters to ``STOPPED`` state.

.. _vm-inst:

Instruction set
```````````````

The list of instructions supported by the `DoIt!` virtual machine. The ``imm``
means immediate operand, the ``breg`` stands for base register (stack pointer
or frame pointer), the ``sreg`` stands for segment register (code segment, data
segment or stack segment), the ``reg`` stands for both base and segment
register and the ``mem`` means memory location (i.e. the operand is a memory
place).

===========================  ==================================================
Instruction                  Description
===========================  ==================================================
``MOVE breg, imm/breg/mem``  Moves the value of `imm` (from `breg`, from `mem`)
                             to `breg`.
``MOVE sreg, sreg/mem``      Moves the value from `sreg`/`mem` to `sreg`.
``MOVE mem, imm/reg/mem``    Moves the value of `imm` (from `reg`, from `mem`)
                             to `mem`.
``POP imm``                  Pops `imm` items from the execution stack.
``POP reg/mem``              Pops one item from the top of the execution stack
                             and stores its value to `reg`/`mem`.
``PUSH imm/reg/mem``         Push the value of `imm`/`reg`/`mem` onto the
                             execution stack.
===========================  ==================================================

.. _asm:

`DoIt!` assembler
-----------------

Before you run the `DoIt!` virtual machine, you must pass the instruction list
to it and set the instruction pointer to the entry point. The instruction list
can be obtained by two ways: either it is made by direct writing of
instructions to the code segment of `DoIt!` virtual machine or it can be
assembled by `DoIt!` assembler. The first approach requires that you put the
instructions to the code segment and set the offsets and many other things
manually::

    vm = Interpreter()

    # Alloc the space for instructions:
    vm.cs.sbrk(11)
    # Reserve the space on the stack:
    vm.ss.sbrk(256)

    # Fill the code segment with instructions:
    # 0: push fp
    vm.cs[0] = Push(RegisterFP())
    # 1: move fp, sp
    vm.cs[1] = Move(RegisterFP(), RegisterSP())
    # 2: add sp, 1
    vm.cs[2] = Add(RegisterSP(), Immediate(1))
    # 3: move [fp], 3
    vm.cs[3] = Move(
        MemoryLocation(
            RegisterSS(), BasePlusOffset(RegisterFP(), Immediate(0))
        ),
        Immediate(3)
    )
    # 4: dec
    vm.cs[4] = Dec()
    # 5: jnz 4
    vm.cs[5] = Jnz(Immediate(4))
    # 6: move sp, fp
    vm.cs[6] = Move(RegisterSP(), RegisterFP())
    # 7: pop fp
    vm.cs[7] = Pop(RegisterFP())
    # 8: retn 0
    vm.cs[8] = Retn(Immediate(0))
    # 9: call 0
    vm.cs[9] = Call(Immediate(0))
    # 10: halt
    vm.cs[10] = Halt()

    # Set the instruction pointer to entry point:
    vm.ip = 9

    # Start the execution:
    vm.run()

The second approach uses the `DoIt!` assembler and several friendly tools::

    assembler = DoItAssembler()
    # Get the registers:
    _, _, _, sp, fp = assembler.registers

    # Assemble the code (entry point is "main" by default):
    assembler.start()    \
      .section("text")   \
        .label("fun")    \
          .push(fp)      \
          .move(fp, sp)  \
          .add(sp, 1)    \
          .move([fp], 3) \
        .label(".loop")  \
          .dec()         \
          .jnz(".loop")  \
          .move(sp, fp)  \
          .pop(fp)       \
          .retn(0)       \
        .label("main")   \
          .call("fun")   \
          .halt()        \
      .end_section()     \
    .end()

    # Link the assembled code, load it, and run it:
    main_o = DoItLinkable(assembler)
    main = DoItLinker(main_o).link()
    app = Application()
    app.run(main)

.. For now, we left the explanation of the examples above to later.

.. the virtual machine
.. adding own errors
.. adding own instructions
.. handling the virtual machine errors
.. - on VM level
.. - on Python level
.. adding own assembler
.. comming soon

.. _refguide:

Complete `DoIt!` core modules reference guide
---------------------------------------------

Here you can find the reference manual of the every function and class provided
by `DoIt!` core modules.

.. module:: support
   :synopsis: `DoIt!` auxiliary routines and classes.

:mod:`doit.support` -- `DoIt!` auxiliary functions and classes
``````````````````````````````````````````````````````````````

Functions and classes commonly used by `DoIt!`.

.. module:: support.errors
   :synopsis: `DoIt!` errors and exceptions.

:mod:`doit.support.errors` -- `DoIt!` errors and exceptions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

This module provides the error codes and exceptions used inside `DoIt!`. The
predefined error codes are::

    ERROR_OK = 0
    ERROR_ASSERT = 1
    ERROR_NOT_IMPLEMENTED = 2
    ERROR_MEMORY_ACCESS = 3
    ERROR_RUNTIME = 4
    ERROR_ASSEMBLER = 5
    ERROR_LINKER = 6
    ERROR_UNKNOWN = 255

Supported exceptions and the auxiliary functions which are using them are:

.. autoexception:: doit.support.errors.DoItError
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoexception:: doit.support.errors.DoItAssertionError
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoexception:: doit.support.errors.DoItNotImplementedError
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoexception:: doit.support.errors.DoItMemoryAccessError
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoexception:: doit.support.errors.DoItRuntimeError
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoexception:: doit.support.errors.DoItAssemblerError
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoexception:: doit.support.errors.DoItLinkerError
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autofunction:: doit.support.errors.__get_caller_name

.. autofunction:: doit.support.errors.doit_assert

.. autofunction:: doit.support.errors.not_implemented

.. module:: support.utils
   :synopsis: `DoIt!` utilities.

:mod:`doit.support.utils` -- `DoIt!` utilities
''''''''''''''''''''''''''''''''''''''''''''''

General purpose utility functions and classes.

.. autoclass:: doit.support.utils.WithStatementExceptionHandler
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.support.utils.Collection
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. module:: config
   :synopsis: `DoIt!` version and configuration.

:mod:`doit.config` -- `DoIt!` version and configuration
```````````````````````````````````````````````````````

The `DoIt!` configuration and version.

.. module:: config.version
   :synopsis: `DoIt!` version.

:mod:`doit.config.version` -- `DoIt!` version
'''''''''''''''''''''''''''''''''''''''''''''

There are two variables defined in this module:

* ``UNUSED_VERSION = None`` -- for unused versions;
* ``DOIT_VERSION`` (:class:`Version <doit.config.version.Version>`) -- holds
  the recent version of `DoIt!`.

The version itself is represented by the
:class:`Version <doit.config.version.Version>` class.

.. autoclass:: doit.config.version.Version
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. module:: config.config
   :synopsis: `DoIt!` configuration.

:mod:`doit.config.config` -- `DoIt!` configuration
''''''''''''''''''''''''''''''''''''''''''''''''''

Classes and functions for configuring `DoIt!`, system probing etc.

.. autoclass:: doit.config.config.Configuration
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. module:: runtime
   :synopsis: `DoIt!` virtual machine (VM) and VM runtime services.

:mod:`doit.runtime` -- `DoIt!` virtual machine (VM) and VM runtime services
```````````````````````````````````````````````````````````````````````````

The `DoIt!` virtual machine and runtime services.

.. module:: runtime.memory
   :synopsis: `DoIt!` VM memory.

:mod:`doit.runtime.memory` -- `DoIt!` VM memory
'''''''''''''''''''''''''''''''''''''''''''''''

The support for `DoIt!` virtual machine memory.

.. autoclass:: doit.runtime.memory.Pointer
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.runtime.memory.Memory
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. module:: runtime.inst
   :synopsis: `DoIt!` VM instruction set.

:mod:`doit.runtime.inst` -- `DoIt!` VM instruction set
''''''''''''''''''''''''''''''''''''''''''''''''''''''

The definitions of instructions for the `DoIt!` virtual machine.

.. autoclass:: doit.runtime.inst.DoItInstruction
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.runtime.inst.Push
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.runtime.inst.Pop
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.runtime.inst.Move
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. module:: runtime.vm
   :synopsis: `DoIt!` virtual machine.

:mod:`doit.runtime.vm` -- `DoIt!` virtual machine
'''''''''''''''''''''''''''''''''''''''''''''''''

The `DoIt!` virtual machine implementation.

.. autoclass:: doit.runtime.vm.Interpreter
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. module:: asm
   :synopsis: Assembly language interfaces.

:mod:`doit.asm` -- Assembly language interfaces
```````````````````````````````````````````````

Interfaces for writing a machine code in the assembly language manner.

.. module:: asm.asm
   :synopsis: General assembler interfaces.

:mod:`doit.asm.asm` -- General assembler interfaces
'''''''''''''''''''''''''''''''''''''''''''''''''''

This module provides an interfaces for building custom assemblers. Predefined
section names::

    SECTION_INFO = ".info"
    SECTION_TEXT = ".text"
    SECTION_DATA = ".data"
    SECTION_SYMBOLS = ".symbols"

Interfaces for custom assemblers and their components:

.. autoclass:: doit.asm.asm.InstructionOperandExpression
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.ConstNode
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.RegisterNode
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.BinOpNode
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.AddNode
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.SubNode
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.MultNode
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.IndexNode
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.NodeVisitor
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.InstructionOperand
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.Instruction
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.AsmCommon
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.BufferMixinBase
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.DataWriterMixinBase
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.Section
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.Sections
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.asm.Assembler
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. module:: asm.doit_asm
   :synopsis: `DoIt!` assembler.

:mod:`doit.asm.doit_asm` -- `DoIt!` assembler
'''''''''''''''''''''''''''''''''''''''''''''

The implementation of `DoIt!` assembler.

.. autoclass:: doit.asm.doit_asm.DoItInstructionOperand
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.Register
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.BaseRegister
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.SegmentRegister
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.DetectSegmentRegister
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.RegisterCS
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.RegisterDS
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.RegisterSS
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.RegisterSP
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.RegisterFP
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.Immediate
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.BasePlusOffset
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.MemoryLocation
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.InsOpCompiler
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.ListLikeBufferMixin
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.DictLikeBufferMixin
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.InfoSection
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.TextOrDataSection
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.SymbolsSection
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.DoItSections
   :show-inheritance:
   :members:
   :special-members:
   :private-members:

.. autoclass:: doit.asm.doit_asm.DoItAssembler
   :show-inheritance:
   :members:
   :special-members:
   :private-members:
