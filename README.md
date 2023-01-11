# NicePlots
## A collection of small tweaks to improve Python / plotting

![Build Status](https://github.com/mdolab/niceplots/workflows/niceplots/badge.svg)
[![Documentation Status](https://readthedocs.com/projects/mdolab-niceplots/badge/?version=latest)](https://mdolab-niceplots.readthedocs-hosted.com/en/latest)
[![PyPI](https://img.shields.io/pypi/v/niceplots)](https://pypi.org/project/niceplots/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/niceplots)](https://pypi.org/project/niceplots/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<img src="https://raw.githubusercontent.com/mdolab/niceplots/main/examples/ParulaContours.png" width="62.22%" /> <img src="https://raw.githubusercontent.com/mdolab/niceplots/main/examples/optProb-shaded.png" width="35%" />
<img src="https://raw.githubusercontent.com/mdolab/niceplots/main/examples/bar_chart.png" width="47.65%" /> <img src="https://raw.githubusercontent.com/mdolab/niceplots/main/examples/james-darkPulseResponse.png" width="49.5%" />


## How do I install?

Niceplots can be pip installed directly from PyPI

```shell
pip install niceplots
```

### If you want to make changes

* Clone this repository, then enter the folder in the command line terminal.
* Enter `pip install -e .` within the `niceplots` folder.

### Font installation (optional)

Niceplots styles use fonts that do not ship with most operating systems, so you'll need to install them separately.
If they are not installed, matplotlib will revert back to its default sans-serif font, DejaVu Sans.

The font used by each style is as follows:
- doumount-light (default niceplots): CMU Bright
- doumount-dark: CMU Bright
- james-dark: Prompt
- james-light: Prompt

Install the fonts on your system and then delete Matplotlib's font cache, which is located in `~/.cache/matplotlib` by default on most operating systems.
Matplotlib will rebuild the font cache next time it is run and (hopefully) find the new fonts.

#### CMU Bright (doumont-light and doumont-dark)

The computer modern bright font can be downloaded from [this link](https://tug.org/FontCatalogue/computermodernbright/).
Alternatively, on Ubuntu, the font can be installed with the following commands:

```
sudo apt-get update
sudo apt-get install fonts-cmu
```
Arch linux users can get the font by installing the `otf-cm-unicode` package from AUR.

#### Prompt (james-dark and james-light)

The Prompt font can be download from [Google Fonts](https://fonts.google.com/specimen/Prompt).

## How do I get set up?

* Use `import niceplots` at the top of a file where you would like to use any function defined in this package.
* Use `niceplots.setStyle()` to set some matplotlib defaults for nice looking plots.
* Plot your beautiful data.
* Use `niceplots.All()` after all the plot commands to apply the niceplot standards on the figure.
* To use the Matlab colormap "parula", execute `from niceplots import parula` then use `parula.parula_map` as your colormap within your plotting script. See the contour plot example code for an example of this.

## Do you have docs?

Sort of, you can find our examples gallery and api documentation [here](https://mdolab-niceplots.readthedocs-hosted.com/en/latest)

## Contribution guidelines

* Make any changes you see fit. Please fork your own version and submit a pull request.

## Who do I talk to?

* Alasdair Gray, alachris@umich.edu
* Eytan Adler, eytana@umich.edu
* Eirikur Jonsson eirikurj@umich.edu
