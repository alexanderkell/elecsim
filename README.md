## ElecSIM

This prepository contains the functionality for the ElecSIM package. ElecSIM is an agent-based model of an electricity market. ElecSIM can be generalised to any country, with starting parameters set in a scenario file.

Through the manipulation of a scenario file, one can build a custom environment of electricity producers with their respective power plants, and an electricity market which matches demand with supply.

ElecSIM allows users to explore the effect of different policy options and starting conditions on electricity markets. 

## Installation

If you're on MacOS, you can install the virtual environment and package manager for python "pipenv" using brew. If you are on linux, you can use Linuxbrew on linux using the same command:

```
$ brew install pipenv
```

if you're using Fedora 28:

```
$ sudo dnf install pipenv
```
or, if you're using windows, run the following in Power Shell:
```
pip install pipenv
```

Once pipenv is installed run the following commands in the folder of your choice to create a new virtual environment and install the dependencies required for this project:

```
pipenv install 
```
