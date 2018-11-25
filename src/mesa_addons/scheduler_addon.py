from mesa.time import BaseScheduler

class OrderedActivation(BaseScheduler):
    """ A scheduler which activates each agent in the order that they are added to the scheduler

    Assumes that all agents have a step(model) method.

    """
    def step(self):
        """ Executes the step of all agents, one at a time.

        """
        for agent in self.agents[:]:
            agent.step()
        self.steps += 1
        self.time += 1
