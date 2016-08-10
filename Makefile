#                                                         -*- coding: utf-8 -*-
#! \file    ./Makefile
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-05-26 18:54:31 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.0.0
#! \fdesc   Makefile for building DoIt!.
#

PYTHON_ = python3
ifeq ($(shell which $(PYTHON_) >/dev/null 2>&1; echo $$?), 1)
  PYTHON_ = python
  ifeq ($(shell which $(PYTHON_) >/dev/null 2>&1; echo $$?), 1)
    $(error Python interpreter is not installed (version 3 is needed))
  endif
endif

SCRIPTSDIR = scripts
PYVERSION = $(SCRIPTSDIR)/pyversion.py

ifeq ($(shell $(PYTHON_) $(PYVERSION) >/dev/null 2>&1; echo $$?), 3)
else
  $(error Python interpreter of version 3 is needed)
endif

PYTHON = $(PYTHON_)
PYTHONFLAGS =
RUNTESTS = $(PYTHON) $(PYTHONFLAGS) $(SCRIPTSDIR)/runtests.py
NDASH = $(PYTHON) $(PYTHONFLAGS) $(SCRIPTSDIR)/ndash.py

.PHONY: all help test markdown docs clean

all: markdown docs

help:
	@echo "Usage: $(MAKE) <target>"
	@echo "where <target> is one of"
	@echo "    help     - print this help"
	@echo "    test     - run all tests"
	@echo "    markdown - make .md files (for GitHub)"
	@echo "    docs     - generate the documentation"
	@echo "    clean    - remove all generated files"

test:
	$(RUNTESTS)

markdown: README.md HACKING.md TODO.md

docs:
	$(MAKE) -C docs html

clean:
	$(MAKE) -C docs clean

README.md: README
	$(NDASH) README $@

HACKING.md: HACKING
	$(NDASH) HACKING $@

TODO.md: TODO
	$(NDASH) TODO $@
