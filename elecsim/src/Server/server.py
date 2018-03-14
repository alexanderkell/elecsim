"""server.py: Server which allows simulation to be displayed in browser"""

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from elecsim.src.Model.Model import World
from mesa.visualization.modules import ChartModule

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


chart = ChartModule([{"Label":"Electricity Consumption",
                      "Colour":"Black"}],
                    data_collector_name="datacollector")

server = ModularServer(World,
                       [grid, chart],
                       "House Model",
                       {"width":10,"height":10})
