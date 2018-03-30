"""power_exchange.py: Functionality to run power exchange"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


from elecsim.src.agents.generation_company.gen_co import GenCo


def tender_bids(agents, ldc):
    generator_companies = [x for x in agents if isinstance(x, GenCo)]
    for i in range(len(generator_companies)):
        print("Generator company number: "+str(i))
        bids = generator_companies[i].make_bid()
        for j in range(len(bids)):
            print(bids[j])
    # print(generator_companies)

    def sort_bid_price(obj):
        return obj.bid_price

    # print(generator_companies.sort(key=sort_bid_price))


