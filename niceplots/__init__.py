import os
from matplotlib import font_manager

__version__ = "2.6.0"


def addFonts():
    font_dirs = [os.path.join(os.path.dirname(__file__), "fonts")]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)


addFonts()

from .utils import *
from .parula import *
