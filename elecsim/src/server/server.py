"""server.py: Server which allows simulation to be displayed in browser"""

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from elecsim.src.model.Model_1 import World
from mesa.visualization.modules import ChartModule
from elecsim.src.data.uk_gencos_and_plants import read_smart_meter_data

COLOURS = {True: "#00AA00",
           False: "#880000"}

def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "h": 0.5,
                 "w":0.5,
                 "Color": COLOURS[agent.storage]}
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)


chart = ChartModule([{"Label": "AggregatedElectricity",
                      "Color": "Black"}],
                    data_collector_name="datacollector")


data = read_smart_meter_data('/Users/b1017579/Documents/PhD/Projects/6. Agent Based Models/elecsim/elecsim/Data/one_hour_30.csv')


server = ModularServer(World,
                       [grid, chart],
                       "House Model",
                       {"width":10,"height":10})
