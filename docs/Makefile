# Simplified makefile for Sphinx documentation

# Variables
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Main targets
.PHONY: help clean html

# Default target is html
all: html

# Help command
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)"

# Clean the build directory
clean:
	rm -rf $(BUILDDIR)/*

# Build HTML documentation
html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html"
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Catch-all for other formats
%:
	$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)/$@"
	@echo
	@echo "Build finished. The $@ pages are in $(BUILDDIR)/$@."
