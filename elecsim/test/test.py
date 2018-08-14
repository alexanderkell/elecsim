"""run.py: Module to run the model"""

from elecsim.src.model.model import Model

import elecsim.src.scenario.scenario_data as Scenario

model = Model(Scenario)

for i in range(2):
    model.step()

