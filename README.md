# README #

### What is this repository for? ###

* A collection of small tweaks to improve Python / plotting

### How do I get set up? ###

* Add the matplotlibrc file to your ~/.config/matplotlib/ folder.
* Use 'import niceplots' at the top of a file where you would like to use any function defined in this package.
* Use 'niceplots.all()' after all the plot commands to apply the niceplot standards on the figure
* To use the Matlab colormap "parula", execute `from niceplots import parula` then use `parula.parula_map` as your colormap within your plotting script. For example, ` plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto', cmap=parula.parula_map)`

### Contribution guidelines ###

* Make any changes you see fit; please submit a pull request if you'd think they'd be useful.

### Who do I talk to? ###

* John Jasa, johnjasa@umich.edu
