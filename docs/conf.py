#!/usr/bin/env python3
#
# sentidict documentation build configuration file
#
# This file is execfile()d with the current directory set to its
# containing dir.

import os
import sys
import importlib.metadata

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "sentidict"
copyright = "2017-2025, Andy Reagan"
author = "Andy Reagan"

# Get version from package metadata
try:
    version = importlib.metadata.version("sentidict")
    release = version
except importlib.metadata.PackageNotFoundError:
    version = "0.0.0"
    release = "0.0.0"

# -- General configuration ---------------------------------------------------

# Minimum Sphinx version
needs_sphinx = "4.0"

# Add any Sphinx extension module names here
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

# Add mappings for intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
}

# Add any paths that contain templates here
templates_path = ["_templates"]

# Support for markdown files
source_suffix = [".rst", ".md"]

# The master toctree document
master_doc = "index"
root_doc = "index"

# List of patterns for files to exclude
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Syntax highlighting style
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages
html_theme = "sphinx_rtd_theme"

# Theme options
html_theme_options = {
    "navigation_depth": 4,
    "titles_only": False,
    "sticky_navigation": True,
}

# Add any paths that contain custom static files
html_static_path = ["_static"]

# -- MyST Parser Configuration ------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

myst_heading_anchors = 3


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "sentidictdoc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "sentidict.tex", "sentidict Documentation", "Andy Reagan", "manual"),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "sentidict", "sentidict Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "sentidict",
        "sentidict Documentation",
        author,
        "sentidict",
        "One line description of project.",
        "Miscellaneous",
    ),
]
