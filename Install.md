Installation of PyBilliards is as simple as any other python package. Just follow the following instructions.


# Install using binaries #

Since PyBilliards is written in pure python, the binaries are themselves the sources. However depending on your wish you can choose to install specific binary package for you platform.
Currently we do not yet provide specific packaged binaries, but expect them soon after a release.
We expect to provide at least a windows installer, and maybe an rpm too.

# Install using sources #

Using source install in python is also pretty easy. Just download the source tarball (wait for a release :) ) and extract it to a convenient directory.

## Requirements ##

On your platform you need to install the latest [python](http://www.python.org) version. In addition you also need the [pygame](http://www.pygame.org) and [numpy](http://numpy.scipy.org) libraries.
On linux you can easily install them using your favourite package manager.
On windows you may need to download the installers from their website. Another option for windows users is to download the pybilliards-full installer, which includes these dependencies.

## Installation ##

For just playing the game you can simply run the file billiards.py from the src directory where you have extracted the sources.
You can install in on your system once you have python, pygame and numpy installed. Run the following command from a terminal with administrative privileges
```
python setup.py install
```
If you want a developer installation so that you can also try changing the code yourself and help with the development, then do
```
python setup.py develop
```

# Install from trunk #

This is for those who want the current source (with all the new features and bugs :) ).
The project uses [mercurial](http://mercurial.selenic.com/) DVCS for version control.
You need to install mercurial and then clone the repo using the following command
```
hg clone https://pybilliards.googlecode.com/hg/ pybilliards 
```

Then you may proceed using for normal or development installation using the procedure given in the [Install#Installation](Install#Installation.md) section