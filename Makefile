#                                                         -*- coding: utf-8 -*-
#! \file    ./Makefile
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-05-26 18:54:31 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   Makefile for building DoIt!.
#

PYTHON_ = python3
ifeq ($(shell which $(PYTHON_) >/dev/null 2>&1; echo $$?), 1)
  PYTHON_ = python
  ifeq ($(shell which $(PYTHON_) >/dev/null 2>&1; echo $$?), 1)
    $(error Python interpreter is not installed (version 3 is needed))
  endif
endif

ifeq ($(shell $(PYTHON_) pyversion.py >/dev/null 2>&1; echo $$?), 3)
else
  $(error Python interpreter of version 3 is needed)
endif

SED_ = sed
ifeq ($(shell which $(SED_) >/dev/null 2>&1; echo $$?), 1)
  $(error $(SED_) utility is not installed)
endif

COPY_ = cp
ifeq ($(shell which $(COPY_) >/dev/null 2>&1; echo $$?), 1)
  $(error $(COPY_) utility is not installed)
endif

PYTHON = $(PYTHON_)
PYTHONFLAGS =
SED = $(SED_)
SEDFLAGS =
COPY = $(COPY_)
COPYFLAGS =

.PHONY: all help test markdown docs clean

all: markdown docs

help:
	@echo "Usage: $(MAKE) <target>"
	@echo "where <target> is one of"
	@echo "    help  - print this help"
	@echo "    test  - run all tests"
	@echo "    docs  - generate the documentation"
	@echo "    clean - remove all generated files"

test:
	$(PYTHON) $(PYTHONFLAGS) runtests.py

markdown: README.md HACKING.md TODO.md

docs:
	$(MAKE) -C docs html

clean:
	$(MAKE) -C docs clean

README.md: README
	$(COPY) $(COPYFLAGS) README $@

HACKING.md: HACKING
	$(COPY) $(COPYFLAGS) HACKING $@
	$(PYTHON) $(PYTHONFLAGS) ndash.py $@

TODO.md: TODO
	$(COPY) $(COPYFLAGS) TODO $@
