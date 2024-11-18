# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

sys.path.insert(0, os.path.abspath(r"C:\Users\Дима\Desktop\ДИПЛОМ\Pip\8.3\исправленные доработанные методы и тесты"))

project = '8.3 Attestation'
copyright = '2024, Student BAS'
author = 'Student BAS'
release = '-'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',        # Поддержка docstring в стиле Google/NumPy
    'sphinx_autodoc_typehints',   # Автоматическое добавление аннотаций типов
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_dir = r"C:\Users\Дима\Desktop\ДИПЛОМ\Pip\8.3\исправленные доработанные методы и тесты\docs"


language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
