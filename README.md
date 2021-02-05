# NicePlots #
## A collection of small tweaks to improve Python / plotting ##

<img src="examples/bar_chart.png" width="57.5%" /> <img src="examples/niceplotsPulseResponse.png" width="39.9%" />
<img src="examples/ParulaContours.png" width="97.6%" />


### How do I install? ###

* Clone this repository, then enter the folder in the command line terminal.
* Enter `pip install -e .` within the `niceplots` folder.

### How do I get set up? ###

* Use `import niceplots` at the top of a file where you would like to use any function defined in this package.
* Use `niceplots.setRCParams()` to set some matplotlib defaults for nice looking plots.
* Use `niceplots.all()` after all the plot commands to apply the niceplot standards on the figure.
* To use the Matlab colormap "parula", execute `from niceplots import parula` then use `parula.parula_map` as your colormap within your plotting script. See the contour plot example code for an example of this.

### Contribution guidelines ###

* Make any changes you see fit. Please fork your own version and submit a pull request.

### Who do I talk to? ###

* Any MDO Lab member
* Alasdair Gray, alachris@umich.edu
