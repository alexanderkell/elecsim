# ElecSim

[![Build Status](https://travis-ci.org/alexanderkell/elecsim.svg?branch=master)](https://travis-ci.org/alexanderkell/elecsim) [![Coverage Status](https://coveralls.io/repos/github/alexanderkell/elecsim-paper/badge.svg?branch=master)](https://coveralls.io/github/alexanderkell/elecsim-paper?branch=master)

ElecSim is an agent-based model of an electricity market written in python. ElecSim can be generalised to any country, with the starting parameters set in a scenario file.

Through the manipulation of a scenario file, one can build a custom environment of electricity producers with their respective power plants, and an electricity market which matches demand with supply.

ElecSim allows practitioners to explore the effect of different policy options and starting conditions on electricity markets. 


# Features

* Generalisable to any country
* Integration of major power plant types
* Default parameter data included
* Example model library


## Installation

Install ElecSim through the python repository pip with the following command
```
pip install elecsim
```

Or for the latest release:
```
pip install git+https://github.com/alexanderkell/elecsim
```

## Getting started

Once ElecSim is installed, create a python file and fill it with the following code:

```
from elecsim.model.world import World 
import logging
logging.basicConfig(level=logging.INFO) 

if __name__ == "__main__":
    world = World(2018)
    for i in range(20):
        world.step()
```
This code imports the `World` class. We use logging to display useful information of the run. This can be turned off or changed to debug for further information.

We then instantiate the model to include information for the year 2018. Here, the for loop steps the model 20 times, which is equivalent to 20 years in the model.
