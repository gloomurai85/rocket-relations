# Configuration for Sphinx
import os, sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../src'))

project = 'rocket_relations'
author = 'Giovanni Suarez'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',      # adds [source] links
    'sphinx.ext.intersphinx',   # links to external docs (Python stdlib)
]

autosummary_generate = True

# Napoleon tweaks for cleaner Returns/Types sections
napoleon_google_docstring = True
napoleon_numpy_docstring  = True
napoleon_use_rtype        = True

# Let :class:`float` etc. link to python docs
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
