# ElecSim

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
pip install -e git+https://github.com/alexanderkell/elecsim
```

## Getting started

Once ElecSim is installed, create a python file and fill it with the following code:

```
from elecsim.model.world import World 

if __name__ == "__main__":
    world = World(initialization_year = 2018, log_level="info")
    for i in range(20):
        world.step()
```
This code imports the `World` class. We use logging to display useful information of the run. This can be turned to 'warning' or changed to 'debug' for further information.

We instantiate the model to start in the year 2018. The for loop steps the model 20 times, which is equivalent to 20 years in the model.

## Custom Scenario

Whilst elecsim comes with a fully parametrised case study of the UK in 2018, you can update the scenario data however you wish. Here we show you how to edit a scenario file for a model run.

Open the scenario file found [here](https://github.com/alexanderkell/elecsim/blob/master/elecsim/scenario/scenario_data.py) and make the required changes. 

For a scenario of the Scottish electricity market we make the following changes:
```
segment_demand_diff = [17568, 21964, 23127, 24327, 25520, 26760, 27888, 28935, 29865, 30721, 31567, 32315, 33188, 34182, 35505, 37480, 39585, 42206, 45209, 52152]
# Peak demand in Scotland is 9.5 times smaller than that of the UK as a whole
segment_demand_diff = [x/9.5 for x in segment_demand_diff]
...
historical_hourly_demand = pd.read_csv('{}/data/processed/electricity_demand/uk_all_year_demand.csv'.format(ROOT_DIR))
historical_hourly_demand.demand = historical_hourly_demand.demand/9.5
...
# We read a new file containing power plants of Scotland
power_plants = pd.read_csv('/path/to/power_plants/scotland_plants.csv', dtype={'Start_date': int})
```
We then pass this new scenario file into the World class as shown below:

```
from elecsim.model.world import World 

if __name__ == "__main__":
    world = World(initialization_year = 2018, scenario_file='/path/to/scenario.py', log_level="warning")
    for i in range(20):
        world.step()
```

This will now run the Scottish scenario for 20 years.


## Docker

ElecSim is hosted on docker hub, so that anybody on any machine can quickly get running. 

Run the following command to pull ElecSim from docker hub
```
docker pull alexkell/elecsim:latest
```
Once you have an ElecSim container run a particular file using the following command
```
docker run elecsim <path/to/file>
```

## Contributing back to ElecSim

If you run into an issue, please submit a ticket [here](https://github.com/alexanderkell/elecsim/issues). If possible, please follow up with a pull request.

To add a feature, submit a ticket [here](https://github.com/alexanderkell/elecsim/issues).
