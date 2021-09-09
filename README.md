# ElecSim

ElecSim is an agent-based model of an electricity market written in python. ElecSim can be generalised to any country, with the starting parameters set in a scenario file. However, ElecSim comes setup with data for the UK electricity market.

Through the manipulation of a scenario file, one can build a custom environment of electricity producers with their respective power plants, and an electricity market which matches demand with supply.

ElecSim allows practitioners to explore the effect of different policy options and starting conditions on electricity markets. 

For the full papers which detail ElecSim, see publications [[1]](https://dl.acm.org/doi/10.1145/3307772.3335321) and [[2]](https://dl.acm.org/doi/10.1145/3396851.3397682).


# Features

* Integration of major power plant types
* Default parameter data included for the UK
* Example model library

## Anaconda Environment

It is recommended that the user uses a (conda environment)[https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html] to isolate the packages when running ElecSim.

Create a conda environment on the command line, with the following command:

```
conda create -n elecsim python=3.7
```

Activate the environment with:

```bash
> conda activate elecsim
```

Later, to recover the system-wide "normal" python, deactivate the environment with:

```bash
> conda elecsim
```

## Installation

It is recommended to install elecsim by first downloading the latest repository from github:
```
git clone https://github.com/alexanderkell/elecsim.git
```

Then, you can install elecsim as a python package with the following command from the directory where the `elecsim` folder has been saved:

```
python -m pip install -e "elecsim[dev]"
```

This allows you to make changes to the elecsim code, and for the changes to be immediately updated in your environment for the elecsim package.

Next, install the requirement packages for elecsim to run, from inside the `elecsim` folder:

```
python -m pip install -r requirements.txt
```


## Getting started

Once ElecSim is installed, create a python file and fill it with the following code:

```
from elecsim.model.world import World 

number_of_years = 20
number_of_time_steps = 8

if __name__ == "__main__":
    world = World(2018, log_level="info", market_time_splices=8, number_of_steps=number_of_years*number_of_time_steps)
    for years in range(number_of_years):
        for time_steps in range(number_of_time_steps):
            world.step()
```
This code imports the `World` class. We use logging to display useful information of the run. This can be turned to 'warning' or changed to 'debug' for further information.

We instantiate the model to start in the year 2018. The first for loop steps the model 20 times, which is equivalent to 20 years in the model. The second for loop iterates through the 8 representative days. If you would like to run the model for a single year, just remove the `for years in range(20):` line and the `number_of_years` variable from the World instantiation.

To see the output data check the directory where you ran the code, which should contain a folder called `ElecSim_Output` with CSVs. You can visualise this data in a visualisation proram of your choice. For instance `seaborn`, `excel` or `ggplot`.

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
    for years in range(20):
        for time_steps in range(8):
            world.step()
```

This will now run the Scottish scenario for 20 years, with 8 representative days per year.



## Questions

If you run into an issue, please submit a ticket [here](https://github.com/alexanderkell/elecsim/issues) and we'll be happy to help you get started.
