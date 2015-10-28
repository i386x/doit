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

BUILDDIR = build
MEDIADIR = static

SPHINXBUILD = $(SPHINXBUILD_)
SPHINXBUILDFLAGS = -d $(BUILDDIR)/doctrees .
LATEX = latex
LATEXFLAGS =
DVI2PS = dvips
DVI2PSFLAGS =
GS = $(GS_)
GSFLAGS =
PS2PNG = $(GS) $(GSFLAGS) -r300 -dTextAlphaBits=4 -sDEVICE=png16m
PS2PNGFLAGS = -dBATCH -dNOPAUSE
RM = rm
RMFLAGS = -rf
TOUCH = touch
TOUCHFLAGS =

API_DOC_IMG01_BASE = stackframe
API_DOC_IMG01 = $(MEDIADIR)/$(API_DOC_IMG01_BASE).png
API_DOC_MEDIA = $(API_DOC_IMG01)

SOURCES = index.rst lang.rst api.rst

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
	$(RM) $(RMFLAGS) $(MEDIADIR)/*.aux $(MEDIADIR)/*.log \
            $(MEDIADIR)/*.dvi $(MEDIADIR)/*.ps $(MEDIADIR)/*.png \
            $(MEDIADIR)/*.pdf

html: $(SOURCES)
	$(SPHINXBUILD) -b html $(SPHINXBUILDFLAGS) $(BUILDDIR)/html

api.rst: $(API_DOC_MEDIA)

$(API_DOC_IMG01): $(MEDIADIR)/$(API_DOC_IMG01_BASE).ps
	$(PS2PNG) $(PS2PNGFLAGS) -sOutputFile=$@ \
            $(MEDIADIR)/$(API_DOC_IMG01_BASE).ps

$(MEDIADIR)/$(API_DOC_IMG01_BASE).ps: $(MEDIADIR)/$(API_DOC_IMG01_BASE).dvi
	$(DVI2PS) $(DVI2PSFLAGS) -o $@ $(MEDIADIR)/$(API_DOC_IMG01_BASE).dvi

$(MEDIADIR)/$(API_DOC_IMG01_BASE).dvi: $(MEDIADIR)/$(API_DOC_IMG01_BASE).tex
	$(LATEX) $(LATEXFLAGS) -output-directory=$(MEDIADIR) \
            $(MEDIADIR)/$(API_DOC_IMG01_BASE).tex
