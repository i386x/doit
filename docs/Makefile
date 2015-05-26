#                                                         -*- coding: utf-8 -*-
#! \file    ./docs/Makefile
#! \author  Jiří Kučera, <sanczes@gmail.com>
#! \stamp   2015-05-01 13:47:56 (UTC+01:00, DST+01:00)
#! \project DoIt!: A Simple Extendable Command Language
#! \license MIT
#! \version 0.1.0
#! \fdesc   Makefile for building the documentation.
#

SPHINXBUILD_ = sphinx-build
ifeq ($(shell which $(SPHINXBUILD_) >/dev/null 2>&1; echo $$?), 1)
  $(error Sphinx is not installed.)
endif

BUILDDIR = build

SPHINXBUILD = $(SPHINXBUILD_)
SPHINXBUILDFLAGS = -d $(BUILDDIR)/doctrees .
RM = rm
RMFLAGS = -rf

.PHONY: all html help clean

all: help

help:
	@echo "Usage: $(MAKE) <target>"
	@echo "where <target> is one of"
	@echo "    help  - print this help"
	@echo "    clean - remove all generated files"
	@echo "    html  - generate HTML files"

clean:
	$(RM) $(RMFLAGS) $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(SPHINXBUILDFLAGS) $(BUILDDIR)/html
