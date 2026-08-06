# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from datetime import datetime as dt

project = 'TRX'
copyright = f'2021-{dt.now().year}, The TRX developers'
author = 'The TRX developers'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinxcontrib.bibtex",
    "sphinx_design",
    ]

bibtex_bibfiles = ['references.bib']
bibtex_default_style = 'plain'
bibtex_reference_style = 'author_year'


myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_image",
    "tasklist",
]
myst_heading_anchors = 3

templates_path = ['_templates']
exclude_patterns = ['.DS_Store']
source_suffix = ['.rst', '.md']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

# Added theme configuration. See: https://pydata-sphinx-theme.readthedocs.io/

html_logo = "_static/logo.png"

html_theme_options = {
    "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
    "use_edit_page_button": True,
    "icon_links": [
        {
            "name": "Home",
            "url": "index.html",
            "icon": "fa-solid fa-home",
            "attributes": {"target": "_self"},
        },
        {
            "name": "GitHub",
            "url": "https://github.com/tee-ar-ex/",
            "icon": "fab fa-github-square",
        }]

}

html_context = {
    "github_url": "https://github.com",
    "github_user": "tee-ar-ex",
    "github_repo": "tee-ar-ex.github.io",
    "github_version": "main",
    "doc_path": "source",
}

html_sidebars = {
    "**": ["sidebar-nav-bs.html", "implementation-links.html"],
}