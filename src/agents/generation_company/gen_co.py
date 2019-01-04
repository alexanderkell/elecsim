import logging

from mesa import Agent

from src.plants.plant_type.fuel_plant import FuelPlant
from src.market.electricity.bid import Bid
from src.plants.fuel.capacity_factor.capacity_factor_calculations import get_capacity_factor
from src.role.investment.calculate_npv import CalculateNPV
from src.role.investment.expected_load_duration_prices import LoadDurationPrices
from src.role.market.latest_market_data import LatestMarketData
from src.role.plants.costs.fuel_plant_cost_calculations import FuelPlantCostCalculations
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant

logger = logging.getLogger(__name__)

"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class GenCo(Agent):
    def __init__(self, unique_id, model, name, discount_rate, plants=None, money=5000000):
        """
        Agent which defines a generating company
        :param unique_id: Unique ID for the generating company
        :param model:  Model which defines the world that the agent lives in
        :param name: Name of generating company
        :param plants: Plants which the generating company is initialised with
        :param money: Money which the agent is initialised with
        """
        super().__init__(unique_id, model)
        if plants is None:
            plants = []

        self.name = name
        self.plants = plants
        self.money = money

        self.discount_rate = discount_rate

    def step(self):
        logger.debug("Stepping generation company: {}".format(self.name))
        # self.dismantle_old_plants()
        self.operate_constructed_plants()
        self.invest()
        self.reset_contracts()

    # def calculate_non_fuel_bids(self, segment_hour):
    #     bids = []
    #     renewable_plants = [renewable_plant for renewable_plant in self.plants if isinstance(renewable_plant, NonFuelPlant)]
    #     for plant in renewable_plants:
    #         marked_up_price = plant.short_run_marginal_cost(self.model)*1.1
    #         bids.append(Bid(self, plant, segment_hour, plant.capacity_mw, marked_up_price))
    #     return bids


    def calculate_bids(self, segment_hour, segment_demand):
        """
        Function to generate the bids for each of the power plants owned by the generating company.
        The bids submitted are the fixed costs divided by lifetime of plant plus yearly variable costs plus a 10% margin
        :param segment_hour: Number of hours in which the current segment is required
        :param segment_demand: Electricity consumption required for the specified number of hours
        :return: Bids returned for the available plants at the specified segment hour
        """

        bids = []

        for plant in self.plants:
            price = plant.short_run_marginal_cost(self.model)
            marked_up_price = price * 1.1
            if isinstance(plant, FuelPlant):
                if plant.capacity_fulfilled[segment_hour] < plant.capacity_mw:
                # if plant.min_running <= segment_hour and plant.capacity_fulfilled[segment_hour] < plant.capacity_mw:
                    bids.append(
                        Bid(self, plant, segment_hour, plant.capacity_mw - plant.capacity_fulfilled[segment_hour], marked_up_price)
                    )
            elif plant.plant_type in ['Offshore', 'Onshore', 'PV']:
                capacity_factor = get_capacity_factor(plant.plant_type, segment_hour)
                bids.append(
                    Bid(self, plant, segment_hour, capacity_factor * (plant.capacity_mw - plant.capacity_fulfilled[segment_hour]), marked_up_price)
                )

        return bids

    def invest(self):
        LOOK_BACK_YEARS = 4

        # Forecast segment prices
        load_duration_prices = LoadDurationPrices(model=self.model)
        forecasted_segment_prices = load_duration_prices.get_load_curve_price_predictions(reference_year=self.model.year_number+1, look_back_years=LOOK_BACK_YEARS)

        logger.debug("Load duration prices: {}".format(forecasted_segment_prices))


        # Forecast marginal costs
        market_data = LatestMarketData(model=self.model)

        power_plant = create_power_plant("estimate_variable", self.model.year_number, "CCGT", 1200)


        short_run_marginal_cost = market_data.get_predicted_marginal_cost(power_plant, LOOK_BACK_YEARS)
        logger.debug("short run marginal cost: {}".format(short_run_marginal_cost))

        forecasted_segment_prices = forecasted_segment_prices.to_frame().reset_index()
        forecasted_segment_prices['num_of_hours'] = abs(forecasted_segment_prices.segment_hour.diff())
        forecasted_segment_prices = forecasted_segment_prices.dropna()
        logger.debug("forecasted_segment_prices: \n {}".format(forecasted_segment_prices))

        forecasted_segment_prices['predicted_profit_per_mwh'] = forecasted_segment_prices['accepted_price'] - short_run_marginal_cost

        def total_profit_per_segment(row, capacity):
            if row['predicted_profit_per_mwh'] > 0:
                total_profit = row['num_of_hours']*row['predicted_profit_per_mwh']*capacity
            else:
                total_profit = 0
            return total_profit

        def total_running_hours(row):
            if row['predicted_profit_per_mwh'] > 0:
                running_hours = row['num_of_hours']
            else:
                running_hours = 0
            return running_hours

        def income(row, capacity):
            if row['predicted_profit_per_mwh'] > 0:
                running_hours = row['num_of_hours']*row['accepted_price']*capacity
            else:
                running_hours = 0
            return running_hours

        forecasted_segment_prices['total_profit_per_segment'] = forecasted_segment_prices.apply(lambda x: total_profit_per_segment(x, power_plant.capacity_mw), axis=1)
        forecasted_segment_prices['total_running_hours'] = forecasted_segment_prices.apply(lambda x: total_running_hours(x), axis=1)
        forecasted_segment_prices['total_income'] = forecasted_segment_prices.apply(lambda x: income(x, power_plant.capacity_mw), axis=1)

        logger.debug("total_hours_predicted_to_run: \n {}".format(forecasted_segment_prices))

        total_profit_for_year = sum(forecasted_segment_prices['total_profit_per_segment'])
        total_running_hours = sum(forecasted_segment_prices['total_running_hours'])
        total_yearly_income = sum(forecasted_segment_prices['total_income'])



        power_plant_vars = vars(power_plant)
        logger.debug("power_plant_vars: {}".format(power_plant_vars))
        vars_required = ['plant_type', 'capacity_mw', 'construction_year', 'average_load_factor', 'efficiency',
                         'pre_dev_period',
                         'construction_period', 'operating_period', 'pre_dev_spend_years', 'construction_spend_years',
                         'pre_dev_cost_per_mw', 'construction_cost_per_mw', 'infrastructure', 'fixed_o_and_m_per_mw',
                         'variable_o_and_m_per_mwh', 'insurance_cost_per_mw', 'connection_cost_per_mw']
        logger.debug("vars_required: {}".format(vars_required))

        power_plant_vars = {key:value for key, value in power_plant_vars.items() if key in vars_required}

        yearly_capital_cost = FuelPlantCostCalculations(**power_plant_vars).calculate_yearly_capital_costs()



        logger.debug("total_profit_for_year: {}, total running hours: {}".format(total_profit_for_year, total_running_hours))

        total_costs = yearly_capital_cost + short_run_marginal_cost*total_running_hours*power_plant.capacity_mw
        logger.debug("yearly_capital_cost: {}".format(yearly_capital_cost))

        logger.debug("total yearly cost: {}, total yearly income: {}".format(total_costs, total_yearly_income))

        result = total_yearly_income - total_costs

        logger.debug("result: {}".format(result))

        # CalculateNPV(self.model, self.discount_rate, self.model.year_number, 5, 70).get_expected_load_factor(load_duration_prices)


    def dismantle_old_plants(self):
        """
        Remove plants that are past their lifetime agent from plant list
        """

        def get_running_plants(plants):
            for plant in plants:
                if plant.construction_year + plant.operating_period + plant.construction_period + plant.pre_dev_period >= self.model.year_number:
                    yield plant
                else:
                    logger.info("Taking the plant '{}' out of service, year of construction: {}".format(plant.name,
                                                                                                        plant.construction_year))
                    continue

        plants_filtered = list(get_running_plants(self.plants))
        self.plants = plants_filtered

    def operate_constructed_plants(self):
        for plant in self.plants:
            if plant.is_operating is False and self.model.year_number >= plant.construction_year + plant.construction_period + plant.pre_dev_period:
                plant.is_operating = True

    def pay_money(self):
        # self.money -=
        # fixed_costs = sum(plant for plant in self.plants)
        # expenditure = sum(bid for plant in self.plants for bid in plant.bids)

        for plant in self.plants:
            pass

    def collect_money(self):
        income = sum((bid.price_per_mwh * bid.segment_hours) for plant in self.plants for bid in plant.bids if
                     bid.partly_accepted or bid.bid_accepted)
        self.money += income

    def reset_contracts(self):
        """
        Function to reset the contracts of all plants
        :return: None
        """
        for plant in self.plants:
            plant.reset_plant_contract()

