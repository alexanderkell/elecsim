"""run.py: Module to run the model"""

from elecsim.src.model.model import Model

model = Model()

for i in range(10):
    model.step()

