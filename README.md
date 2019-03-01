## ElecSIM 
[![Build Status](https://travis-ci.org/alexanderkell/elecsim.svg?branch=master)](https://travis-ci.org/alexanderkell/elecsim)

This prepository contains the functionality for the ElecSIM package. ElecSIM is an agent-based model of an electricity market. ElecSIM can be generalised to any country, with starting parameters set in a scenario file.

Through the manipulation of a scenario file, one can build a custom environment of electricity producers with their respective power plants, and an electricity market which matches demand with supply.

ElecSIM allows users to explore the effect of different policy options and starting conditions on electricity markets. 

## Installation

Install elecsim through the python repository pip with the following command
```
pip install elecsim
```

Or for the latest release:
```
pip install git+https://github.com/alexanderkell/elecsim
```

## Getting started

To get started create a python file once elecsim is installed through pip and fill it with the following code:

```
from elecsim.model.world import World
import logging
logging.basicConfig(level=logging.INFO) # Displays information of run

if __name__ == "__main__":
    world = World(2018) # Initiates world in the year 2018
    for i in range(20): # Runs the simulation for 20 years
        world.step() # Step for another year
```
