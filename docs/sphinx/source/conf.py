# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("../../.."))

# -- Project information -----------------------------------------------------
project = "GoNetwork AI"
copyright = "2025, GoNetwork"
author = "GoNetwork Team"
release = "1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "pt_BR"

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Extension configuration -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pyside6": ("https://doc.qt.io/qtforpython/6.2/objects.inv", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/20/", None),
}

# -- Napoleon settings ------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True

# -- MyST settings ---------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
    "attrs_block",
]

# -- Add logo and favicon --------------------------------------------------
html_logo = "_static/images/logo.png"
html_favicon = "_static/images/favicon.ico"
