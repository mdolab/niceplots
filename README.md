# NicePlots
## A collection of nice styles and helper functions for matplotlib

![Build Status](https://github.com/mdolab/niceplots/workflows/niceplots/badge.svg)
[![Documentation Status](https://readthedocs.com/projects/mdolab-niceplots/badge/?version=latest)](https://mdolab-niceplots.readthedocs-hosted.com/en/latest)
[![PyPI](https://img.shields.io/pypi/v/niceplots)](https://pypi.org/project/niceplots/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/niceplots)](https://pypi.org/project/niceplots/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<img src="https://mdolab-niceplots.readthedocs-hosted.com/en/latest/_images/sphx_glr_plot_parula_contours_001.svg" width="61%" /> <img src="https://mdolab-niceplots.readthedocs-hosted.com/en/latest/_images/sphx_glr_plot_opt_prob_002.svg" width="38.2%" />
<img src="https://mdolab-niceplots.readthedocs-hosted.com/en/latest/_images/sphx_glr_plot_bar_chart_001.svg" width="61%" /> <img src="https://mdolab-niceplots.readthedocs-hosted.com/en/latest/_images/sphx_glr_plot_style_demo_004.svg" width="38.2%" />

<!-- https://mdolab-niceplots.readthedocs-hosted.com/en/latest/_images/ -->

## How do I install?

NicePlots can be pip installed directly from PyPI

```shell
pip install niceplots
```

### If you want to make changes

* Clone this repository, then enter the folder in the command line terminal.
* Enter `pip install -e .` within the `niceplots` folder.

### Font installation

As of v2.6.0, NicePlots now comes packaged with the fonts required for its custom styles, so you don't need to install them yourself.

## How do I get set up?

* `import matplotlib.pyplot as plt` and `import niceplots` at the top of a file where you would like to use any function defined in this package.
* Use `plt.style.use(niceplots.get_style())` to set some defaults for nice-looking plots. You can also try passing different styles to `get_style()`, such as NicePlots' `"james-dark"` or any of matplotlib's styles (see the function's documentation for a full list of available NicePlots styles).
* Take advantage of NicePlots' helper functions, including (but not limited to) `adjust_spines`, `horiz_bar`, and `plot_nested_pie`, which are all documented in the [examples gallery](https://mdolab-niceplots.readthedocs-hosted.com/en/latest/auto_examples/index.html).
* Admire your beautiful data.

## Do you have docs?

Sort of, you can find our examples gallery and API documentation [here](https://mdolab-niceplots.readthedocs-hosted.com/en/latest)

## Help, my old NicePlots code doesn't work anymore!

We made a couple of changes to the API in version 2.0.0, most of them can be fixed with a simple find and replace.
Check the [release notes](https://github.com/mdolab/niceplots/releases/tag/v2.0.0) for more details.

## Contribution guidelines

Make any changes you see fit. Please fork your own version and submit a pull request.

## Who do I talk to?

Please post questions and suggestions to either the [issues](https://github.com/mdolab/niceplots/issues) (if it's concerning a bug) or [discussions](https://github.com/mdolab/niceplots/discussions) tab on the NicePlots GitHub repo.
