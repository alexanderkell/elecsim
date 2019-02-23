import logging
from itertools import chain
from random import shuffle

from mesa.time import BaseScheduler

logging.getLogger(__name__)

from elecsim.agents.generation_company.gen_co import GenCo
from elecsim.agents.demand.demand import Demand
from elecsim.market.electricity.power_exchange import PowerExchange

class OrderedActivation(BaseScheduler):
    """ A scheduler which activates each agent in the order that they are added to the scheduler

    Assumes that all agents have a step(model) method.

    """
    def step(self):
        """ Executes the step of all agents, one at a time.
        """

        gen_cos = [agent for agent in self.agents if isinstance(agent, GenCo)]
        shuffle(gen_cos)

        demand_agents = [agent for agent in self.agents if isinstance(agent, Demand)]
        power_exchange = [agent for agent in self.agents if isinstance(agent, PowerExchange)]

        logging.info("Stepping agents")
        for agent in chain(power_exchange, gen_cos, demand_agents):
            agent.step()
        self.steps += 1
        self.time += 1
