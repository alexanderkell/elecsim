"""run.py: Module to run the world of electricity consuming households"""

from elecsim.src.Model.Model import World

print("Running")
elec = World(50,50)
elec.run_model()
