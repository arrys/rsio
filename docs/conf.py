from pathlib import Path
import sys
sys.path.append(str(Path('..').resolve()))

project = "RoboSAPIENS IO Project"
copyright = "2025"
author = "Sahar Nasimi Nezhad, Bert Van Acker, Arkadiusz Ryś"
release = "0.4.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary"
]

templates_path = ["templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["static"]
