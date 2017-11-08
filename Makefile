#                                                         -*- coding: utf-8 -*-
#! \file    ./Makefile
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-05-26 18:54:31 (UTC+01:00, DST+01:00)
#! \project DoIt!: Tools and Libraries for Building DSLs
#! \license MIT
#! \version 0.0.0
#! \fdesc   Makefile for building DoIt!.
#

WC = wc
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
STATS = $(WC) -lc

SOURCES = doit/config/config.py \
          doit/config/version.py \
          doit/support/app/application.py \
          doit/support/app/config.py \
          doit/support/app/errors.py \
          doit/support/app/io.py \
          doit/support/app/logging.py \
          doit/support/app/options.py \
          doit/support/app/printer.py \
          doit/support/cmd/commands.py \
          doit/support/cmd/errors.py \
          doit/support/cmd/eval.py \
          doit/support/cmd/runtime.py \
          doit/support/errors.py \
          doit/support/observer.py \
          doit/support/utils.py \
          doit/support/visitnode.py \
          doit/text/fmt/format.py \
          doit/text/pgen/builders/builder.py \
          doit/text/pgen/builders/cfg2glap.py \
          doit/text/pgen/cache/fmt/__init__.py \
          doit/text/pgen/cache/__init__.py \
          doit/text/pgen/models/action.py \
          doit/text/pgen/models/ast.py \
          doit/text/pgen/models/cfgram.py \
          doit/text/pgen/models/precedence.py \
          doit/text/pgen/models/token.py \
          doit/text/pgen/readers/glap/bootstrap/lib/base.py \
          doit/text/pgen/readers/glap/bootstrap/pp/commands.py \
          doit/text/pgen/readers/glap/bootstrap/pp/eval.py \
          doit/text/pgen/readers/glap/bootstrap/__init__.py \
          doit/text/pgen/readers/glap/bootstrap/parser.py \
          doit/text/pgen/readers/reader.py \
          doit/text/pgen/utils/cfgtools.py \
          doit/text/pgen/utils/tagengine.py \
          doit/text/pgen/writers/writer.py \
          doit/text/pgen/__init__.py \
          doit/text/pgen/errors.py \
          scripts/pgen.py \
          scripts/pyversion.py \
          scripts/runtests.py

TESTS_GLAP_DIR = tests/test_text/test_pgen/test_readers/test_glap

TESTS =   tests/test_config/__init__.py \
          tests/test_config/test_config.py \
          tests/test_config/test_version.py \
          tests/test_support/test_app/__init__.py \
          tests/test_support/test_app/test_application.py \
          tests/test_support/test_app/test_config.py \
          tests/test_support/test_app/test_errors.py \
          tests/test_support/test_app/test_io.py \
          tests/test_support/test_app/test_logging.py \
          tests/test_support/test_app/test_options.py \
          tests/test_support/test_app/test_printer.py \
          tests/test_support/test_cmd/__init__.py \
          tests/test_support/test_cmd/test_commands.py \
          tests/test_support/test_cmd/test_errors.py \
          tests/test_support/test_cmd/test_eval.py \
          tests/test_support/test_cmd/test_runtime.py \
          tests/test_support/__init__.py \
          tests/test_support/test_errors.py \
          tests/test_support/test_observer.py \
          tests/test_support/test_utils.py \
          tests/test_support/test_visitnode.py \
          tests/test_text/test_fmt/__init__.py \
          tests/test_text/test_fmt/test_format.py \
          tests/test_text/test_pgen/test_models/__init__.py \
          tests/test_text/test_pgen/test_models/test_action.py \
          tests/test_text/test_pgen/test_models/test_ast.py \
          tests/test_text/test_pgen/test_models/test_cfgram.py \
          tests/test_text/test_pgen/test_models/test_precedence.py \
          tests/test_text/test_pgen/test_models/test_token.py \
          $(TESTS_GLAP_DIR)/test_bootstrap/__init__.py \
          $(TESTS_GLAP_DIR)/test_bootstrap/test_parser.py \
          $(TESTS_GLAP_DIR)/__init__.py \
          tests/test_text/test_pgen/test_readers/__init__.py \
          tests/test_text/test_pgen/test_utils/__init__.py \
          tests/test_text/test_pgen/test_utils/test_tagengine.py \
          tests/test_text/test_pgen/__init__.py \
          tests/test_text/test_pgen/test_errors.py \
          tests/test_text/__init__.py \
          tests/__init__.py \
          tests/common.py

AUXES =   .gitignore \
          HACKING.md \
          LICENSE \
          Makefile \
          README.md \
          TODO.md

FILES =   $(SOURCES) $(TESTS) $(AUXES)

.PHONY: all help test docs clean stats stats-s stats-t stats-st

all: docs

help:
	@echo "Usage: $(MAKE) <target>"
	@echo "where <target> is one of"
	@echo "    help     - print this help"
	@echo "    test     - run all tests"
	@echo "    docs     - generate the documentation"
	@echo "    clean    - remove all generated files"
	@echo "    stats    - print project statistics (number of lines"
	@echo "               and number of bytes)"
	@echo "    stats-s  - print project statistics (only sources)"
	@echo "    stats-t  - print project statistics (only tests)"
	@echo "    stats-st - print project statistics (sources and tests)"

test:
	$(RUNTESTS)

docs:
	$(MAKE) -C docs html

clean:
	$(MAKE) -C docs clean

stats:
	$(STATS) $(FILES)

stats-s:
	$(STATS) $(SOURCES)

stats-t:
	$(STATS) $(TESTS)

stats-st:
	$(STATS) $(SOURCES) $(TESTS)
