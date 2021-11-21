# NicePlots
## A collection of small tweaks to improve Python / plotting

![Build Status](https://github.com/mdolab/niceplots/workflows/niceplots/badge.svg)

<img src="examples/bar_chart.png" width="58.5%" /> <img src="examples/niceplotsPulseResponse.png" width="38.82%" />
<img src="examples/ParulaContours_dark.png" width="62.22%" /> <img src="examples/optProb-shaded.png" width="35%" />


### How do I install?

* Clone this repository, then enter the folder in the command line terminal.
* Enter `pip install -e .` within the `niceplots` folder.

#### Font installation (optional)

Niceplots will try and use the [computer modern bright](https://tug.org/FontCatalogue/computermodernbright/) font for the best looking plots so be sure to install it as a system font if you want to recreate the style of the plots above.
Otherwise, niceplots will still work but revert back to the matplotlib default sans-serif font, DejaVu Sans.

### How do I get set up?

* Use `import niceplots` at the top of a file where you would like to use any function defined in this package.
* Use `niceplots.setRCParams()` to set some matplotlib defaults for nice looking plots. Set `dark_mode=True` and `set_background_color=True` to make plots with a dark background.
* Use `niceplots.all()` after all the plot commands to apply the niceplot standards on the figure.
* To use the Matlab colormap "parula", execute `from niceplots import parula` then use `parula.parula_map` as your colormap within your plotting script. See the contour plot example code for an example of this.

### Contribution guidelines

* Make any changes you see fit. Please fork your own version and submit a pull request.

### Who do I talk to?

* Alasdair Gray, alachris@umich.edu
* Eirikur Jonsson eirikurj@umich.edu
