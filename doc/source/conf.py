# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# 指定项目路径
import os
import sys
import sphinx_markdown_builder
sys.path.insert(0, os.path.abspath('../../appbuilder'))

project = 'Appbuilder-SDK'
copyright = '2024, baidubce'
author = 'baidubce'
release = '0.9.4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_markdown_builder'
    ]

templates_path = ['_templates']

# 排除tests目录及其子文件
exclude_patterns = ['appbuilder/tests/**/*']

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
