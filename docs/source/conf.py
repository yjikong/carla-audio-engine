import os
import sys
from unittest.mock import MagicMock

# Geht zwei Ebenen nach oben von /docs/source/ zu deinem /Code/ Ordner
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../Code/CARLA'))

# Erweitertes Mocking für verschachtelte Module
MOCK_MODULES = [
    'carla', 'numpy', 'pygame', 'pygame.locals', 
    'pygame.display', 'pygame.draw', 'pygame.event'
]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = MagicMock()

# -- Project information -----------------------------------------------------
project = 'SoundCARLA'
copyright = '2026, Kai Braun, Ozan Miguel Gündogdu, Yeri Jikong'
author = 'Kai Braun, Ozan Miguel Gündogdu, Yeri Jikong'
release = '0.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Liest deine Docstrings
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',     # Versteht den Google-Style
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
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
add_module_names = False

# -- Custom Setup Hook -------------------------------------------------------
def setup(app):
    def skip(app, what, name, obj, skip, options):
        # Definiere die Module, die "leer" sein sollen (nur Docstrings)
        clean_modules = [
            "Code.CARLA.generate_traffic",
            "Code.CARLA.manual_control_sw" # Prüfe, ob der Name exakt stimmt
        ]
        
        # Hole das Modul, zu dem das aktuelle Objekt gehört
        module_name = getattr(obj, "__module__", None)

        if module_name in clean_modules:
            # Wenn wir uns in einem der Zielmodule befinden, 
            # überspringen wir alles (Funktionen, Klassen, etc.)
            return True 
            
        return skip

    app.connect("autodoc-skip-member", skip)