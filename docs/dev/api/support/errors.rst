.. _doit-dev-api-support-errors:

.. admonition:: TODO
   :class: warning

   Update this doc after first version of |doit| will be released.

.. module:: support.errors
   :synopsis: DoIt! errors and exceptions.

:mod:`doit.support.errors` -- |doit| Errors and Exceptions 
==========================================================

During its bootstrap phase, |doit| uses for error reporting exceptions derived
from :exc:`DoItError <doit.support.errors.DoItError>`. Every |doit| exception
object keeps an error code and error message, where error codes are divided to
the following categories:

* 0 -- no error
* 1 to 254 -- reserved for |doit| internal errors
* 255 -- unknown error
* 256 and greater -- reserved for user defined errors and for further use

The actual list of error codes used internally by |doit| is:

=========================  =====  =============================================
Error code                 Value  Meaning
=========================  =====  =============================================
``ERROR_OK``               0      No error.
``ERROR_ASSERT``           1      Assertion failed.
``ERROR_NOT_IMPLEMENTED``  2      Feature, method, or subroutine is not
                                  implemented.
``ERROR_MEMORY_ACCESS``    3      Access to virtual machine memory failed.
``ERROR_RUNTIME``          4      Runtime error inside virtual machine occured.
``ERROR_ASSEMBLER``        5      Assembling phase failed.
``ERROR_LINKER``           6      Linking phase failed.
``ERROR_UNKNOWN``          255    Unknown error.
=========================  =====  =============================================

These error codes are common for both |doit| bootstrap and |doit| core modules,
which are JITable.

|doit| Errors and Exceptions API
--------------------------------

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
