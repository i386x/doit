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
  $(error Sphinx is not installed)
endif

PYTHON_ = python3
ifeq ($(shell which $(PYTHON_) >/dev/null 2>&1; echo $$?), 1)
  PYTHON_ = python
  ifeq ($(shell which $(PYTHON_) >/dev/null 2>&1; echo $$?), 1)
    $(error Python interpreter is not installed (version 3 is needed))
  endif
endif

ifeq ($(shell $(PYTHON_) ../pyversion.py >/dev/null 2>&1; echo $$?), 3)
else
  $(error Python interpreter of version 3 is needed)
endif

LATEX_ = latex
ifeq ($(shell which $(LATEX_) >/dev/null 2>&1; echo $$?), 1)
  $(error LaTeX is not installed)
endif

DVI2PS_ = dvi2ps
ifeq ($(shell which $(DVI2PS_) >/dev/null 2>&1; echo $$?), 1)
  DVI2PS_ = dvitops
  ifeq ($(shell which $(DVI2PS_) >/dev/null 2>&1; echo $$?), 1)
    DVI2PS_ = dvips
    ifeq ($(shell which $(DVI2PS_) >/dev/null 2>&1; echo $$?), 1)
      $(error $(DVI2PS_) utility is not installed)
    endif
  endif
endif

GS_ = gs
ifeq ($(shell which $(GS_) >/dev/null 2>&1; echo $$?), 1)
  GS_ = gsexe
  ifeq ($(shell which $(GS_) >/dev/null 2>&1; echo $$?), 1)
    GS_ = ghostscript
    ifeq ($(shell which $(GS_) >/dev/null 2>&1; echo $$?), 1)
      GS_ = gswin32c
      ifeq ($(shell which $(GS_) >/dev/null 2>&1; echo $$?), 1)
        GS_ = gswin64c
        ifeq ($(shell which $(GS_) >/dev/null 2>&1; echo $$?), 1)
          $(error GhostScript interpreter is not installed)
        endif
      endif
    endif
  endif
endif

RM_ = rm
ifeq ($(shell which $(RM_) >/dev/null 2>&1; echo $$?), 1)
  $(error $(RM_) utility is not installed)
endif

BUILDDIR = build
MEDIADIR = static

SPHINXBUILD = $(SPHINXBUILD_)
SPHINXBUILDFLAGS = -d $(BUILDDIR)/doctrees .
PYTHON = $(PYTHON_)
PYTHONFLAGS =
LATEX = $(LATEX_)
LATEXFLAGS =
DVI2PS = $(DVI2PS_)
DVI2PSFLAGS =
GS = $(GS_)
GSFLAGS =
PS2PNG = $(GS) $(GSFLAGS) -r300 -dTextAlphaBits=4 -sDEVICE=png16m
PS2PNGFLAGS = -dBATCH -dNOPAUSE
RM = $(RM_)
RMFLAGS = -rf

HTML_SUFFIX := $(shell $(PYTHON) conf.py 2>/dev/null)

INDEX_HTML = $(BUILDDIR)/html/index$(HTML_SUFFIX)

API_DOC_IMG01_BASE = stackframe
API_DOC_IMG01 = $(MEDIADIR)/$(API_DOC_IMG01_BASE).png
API_DOC_MEDIA = $(API_DOC_IMG01)

SOURCES = index.rst lang.rst \
          dev/index.rst dev/basics.rst \
          dev/api/index.rst \
          dev/api/support/index.rst \
          dev/api/support/errors.rst

.PHONY: all help html clean

all: help

help:
	@echo "Usage: $(MAKE) <target>"
	@echo "where <target> is one of"
	@echo "    help  - print this help"
	@echo "    html  - generate HTML files"
	@echo "    clean - remove all generated files"

html: $(INDEX_HTML)

$(INDEX_HTML): $(SOURCES)
	$(SPHINXBUILD) -b html $(SPHINXBUILDFLAGS) $(BUILDDIR)/html

$(API_DOC_IMG01): $(MEDIADIR)/$(API_DOC_IMG01_BASE).ps
	$(PS2PNG) $(PS2PNGFLAGS) -sOutputFile=$@ \
            $(MEDIADIR)/$(API_DOC_IMG01_BASE).ps

$(MEDIADIR)/$(API_DOC_IMG01_BASE).ps: $(MEDIADIR)/$(API_DOC_IMG01_BASE).dvi
	$(DVI2PS) $(DVI2PSFLAGS) -o $@ $(MEDIADIR)/$(API_DOC_IMG01_BASE).dvi

$(MEDIADIR)/$(API_DOC_IMG01_BASE).dvi: $(MEDIADIR)/$(API_DOC_IMG01_BASE).tex
	$(LATEX) $(LATEXFLAGS) -output-directory=$(MEDIADIR) \
            $(MEDIADIR)/$(API_DOC_IMG01_BASE).tex

clean:
	$(RM) $(RMFLAGS) $(BUILDDIR)/*
	$(RM) $(RMFLAGS) $(MEDIADIR)/*.aux $(MEDIADIR)/*.log \
            $(MEDIADIR)/*.dvi $(MEDIADIR)/*.ps $(MEDIADIR)/*.png \
            $(MEDIADIR)/*.pdf
