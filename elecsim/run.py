"""run.py: Module to run the world of electricity consuming households"""

from elecsim.src.server.server import server


server.port = 8521  # The default
server.launch()
