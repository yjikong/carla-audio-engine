import os
import sys
from unittest.mock import MagicMock

# Geht zwei Ebenen nach oben von /docs/source/ zu deinem /Code/ Ordner
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../Code/CARLA'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Erweitertes Mocking für verschachtelte Module
MOCK_MODULES = [
    'carla', 'numpy', 'pygame', 'pygame.locals', 
    'pygame.display', 'pygame.draw', 'pygame.event'
]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = MagicMock()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SoundCARLA'
copyright = '2026, Kai Braun, Ozan Miguel Gündogdu, Yeri Jikong'
author = 'Kai Braun, Ozan Miguel Gündogdu, Yeri Jikong'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Liest deine Docstrings
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',     # Versteht den Google-Style, den wir gerade geschrieben haben
    'sphinx.ext.viewcode',     # Fügt Links zum Quellcode hinzu
    'sphinx_rtd_theme',        # Das schicke Read-the-Docs Design
    'sphinx.ext.extlinks'
    ]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pygame': ('https://www.pygame.org/docs/', None),
}

extlinks = {
    'carla_docs': ('https://carla.readthedocs.io/en/0.9.15/%s', '%s')
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True  # Dokumentiert auch die __init__ Methoden
napoleon_use_param = True
napoleon_use_rtype = True
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

add_module_names = False