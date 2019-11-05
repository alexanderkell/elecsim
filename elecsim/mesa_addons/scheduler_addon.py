import logging
from itertools import chain
from random import shuffle

from mesa.time import BaseScheduler

logging.getLogger(__name__)

from elecsim.agents.generation_company.gen_co import GenCo
from elecsim.agents.demand.demand import Demand
from elecsim.market.electricity.market.power_exchange import PowerExchange
import elecsim.scenario.scenario_data
from elecsim.role.market.latest_market_data import LatestMarketData

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

        if elecsim.scenario.scenario_data.investment_mechanism == "RL" and self.model.step_number % self.model.market_time_splices == 0:
            obs = LatestMarketData(self.model).get_RL_investment_observations()
            actions = self.model.client.get_action(self.model.eid, obs)
            # logger.info("actions: {}".format(actions))

            reward = {}
            for gen_co_name, action in actions.items():
                gen_co_to_invest = [gen_co for gen_co in gen_cos if gen_co.name == gen_co_name][0]

                gen_co_to_invest.invest_RL(action)

                reward[gen_co_name] = gen_co_to_invest.money

        for agent in chain(gen_cos, demand_agents):
            agent.step()

        reward = {}
        for genco in self.model.get_gencos():
            reward[genco.name] = genco.money

        if elecsim.scenario.scenario_data.investment_mechanism == "RL":
            self.model.client.log_returns(self.model.eid, reward=reward)

        self.steps += 1
        self.time += 1

