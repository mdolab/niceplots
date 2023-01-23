from sphinx_mdolab_theme.config import *
from sphinx_gallery.scrapers import matplotlib_scraper

class matplotlib_svg_scraper(object):

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return matplotlib_scraper(*args, format='svg', **kwargs)

# -- Project information -----------------------------------------------------
project = "niceplots"

# sphinx-gallery
extensions.extend(["sphinx_gallery.gen_gallery"])
sphinx_gallery_conf = {
    "examples_dirs": "../examples",  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
    'image_scrapers': (matplotlib_svg_scraper(),),
}
