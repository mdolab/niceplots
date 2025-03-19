from sphinx_mdolab_theme.config import *
from glob import glob
import shutil
import os
import sys
from sphinx_gallery.scrapers import figure_rst
from pathlib import PurePosixPath

# This is necessary for sphinx_gallery to be able to import sphinxext.matplotlib_svg_scraper
# (see https://sphinx-gallery.github.io/stable/configuration.html#importing-callables)
sys.path.insert(0, os.path.dirname(__file__))

# -- Project information -----------------------------------------------------
project = "niceplots"

# sphinx-gallery
extensions.extend(["sphinx_gallery.gen_gallery"])
sphinx_gallery_conf = {
    "examples_dirs": "../examples",  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
    "image_scrapers": ("sphinxext.matplotlib_svg_scraper",),
}
