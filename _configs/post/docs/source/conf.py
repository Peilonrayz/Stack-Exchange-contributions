# -*- coding: utf-8 -*-
# -- Path setup --

# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
# sys.path.append(os.path.abspath("./_ext"))

# -- Project information --

project = 'Post'
copyright = '2019, Peilonrayz'
author = 'Peilonrayz'

# -- Project Layout --

master_doc = 'post'
templates_path = ['_templates']
exclude_patterns = []

# -- Extensions --

extensions = [
    'sphinx_markdown_builder',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
]
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}


# -- Options for HTML output --
html_theme = 'alabaster'
html_static_path = ['_static']
