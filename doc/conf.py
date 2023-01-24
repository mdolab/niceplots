from sphinx_mdolab_theme.config import *
from glob import glob
import shutil
import os
from sphinx_gallery.scrapers import figure_rst
from pathlib import PurePosixPath

class svgScraper(object):
    """This is a custom scraper for sphinx-gallery that allows us to use svg files in our examples. It is almost
    entirely copied from the PNGScraper shown at:
    https://sphinx-gallery.github.io/dev/advanced.html#example-2-detecting-image-files-on-disk
    """
    def __init__(self):
        self.seen = set()

    def __repr__(self):
        return 'svgScraper'

    def __call__(self, block, block_vars, gallery_conf):
        # Find all svg files in the directory of this example.
        path_current_example = os.path.dirname(block_vars['src_file'])
        svgs = sorted(glob(os.path.join(path_current_example, '*.svg')))

        # Get the name of the current example, e.g if the file is called "plot_nested_pie_chart.py",
        # then example_name = "nested_pie_chart"
        example_name = os.path.splitext(os.path.basename(block_vars['src_file']))[0].split("plot_")[0]

        # Iterate through svgs, copy them to the sphinx-gallery output directory
        image_names = list()
        image_path_iterator = block_vars['image_path_iterator']
        for svg in svgs:
            if svg not in self.seen and example_name.lower() in svg.lower():
                self.seen |= set(svg)
                this_image_path = image_path_iterator.next()
                image_path = PurePosixPath(this_image_path)
                image_path = image_path.with_suffix('.svg')
                image_names.append(image_path)
                shutil.move(svg, image_path)
        # Use the `figure_rst` helper function to generate rST for image files
        return figure_rst(image_names, gallery_conf['src_dir'])

# -- Project information -----------------------------------------------------
project = "niceplots"

# sphinx-gallery
extensions.extend(["sphinx_gallery.gen_gallery"])
sphinx_gallery_conf = {
    "examples_dirs": "../examples",  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
    'image_scrapers': (svgScraper(),),
}
