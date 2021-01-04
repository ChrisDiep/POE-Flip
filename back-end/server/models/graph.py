import networkx as nx
import matplotlib.pyplot as plt
from server.models.sat_solver import SearchForAllSolutions


class Graph:
    """ Class for creating and analyzing a graph of currencies """

    def __init__(self, data):
        self.MIN_TRADES = 2
        self.data = data
        self.data_dict = self.create_dict(data)
        self.currencies = self._parse_currencies(data)
        self.graph = nx.DiGraph()
        self.create_graph()

    def _parse_currencies(self, data):
        """ Maps the currencies from the database information to an array """
        currencies = []
        for entry in data:
            currencies.append(entry["currency_name"])
        return currencies

    def create_dict(self, data):
        currency_dict = {}
        for entry in data:
            currency_dict[entry["currency_name"]] = entry
        return currency_dict

    def create_graph(self):
        """ Adds edges and nodes to the graph from information in the database """
        self.graph.add_nodes_from(self.currencies)
        for entry in self.data:
            currency_name = entry["currency_name"]
            for currency_receiving in entry["prices"]:
                self._add_edges(
                    currency_name,
                    currency_receiving,
                    entry["prices"][currency_receiving],
                )

    def _add_edges(self, start, end, listings):
        """
        Adds edges to the nodes in the graph going from have to want
        """
        self.graph.add_edge(start, end, trades=listings)

    def print(self):
        """ Returns a string representation of the nodes """
        return " ".join(list(self.graph.nodes))

    def visualize(self):
        """ Creates a static visualization of the graph """
        nx.draw(self.graph, with_labels=True, font_weight="bold")
        plt.show()

    def simple_paths(self, start):
        """ Get paths in the graph and adds on the starting currency"""
        paths = []
        for currency in self.currencies:
            if start != currency:
                no_self_paths = list(
                    nx.all_simple_paths(
                        self.graph,
                        source=start,
                        target=currency,
                        cutoff=self.MIN_TRADES - 1,
                    )
                )
                for path in no_self_paths:
                    path.append(start)
                    paths.append(path)
                # paths[currency] = no_self_paths
        return paths

    def _get_path_solutions(self, path):
        """ Calls CP-Sat Solver to Get Solutions to whispers """
        listings_info = []
        for index in range(len(path) - 1):
            start_currency = path[index]
            end_currency = path[index + 1]
            listing_info = self.graph[start_currency][end_currency]
            listings_info.append(listing_info["trades"])
        solutions = SearchForAllSolutions(*listings_info)
        return solutions

    def _get_trade_profit(self, path_info):
        """ Calculates the profit of the path and creates response object """
        solutions = path_info["solutions"]
        uuid_ref = path_info["uuid_ref"]
        objs = []
        for solution in solutions:
            obj = {}
            obj["trades"] = path_info["trades"].split(",")
            count = 0
            obj["listings"] = {}
            for uuid in solution:
                if solution[uuid] != 0:
                    listing_info = uuid_ref[uuid]["listing"]
                    new_listing = {
                        "order_size": solution[uuid],
                        "info": {
                            "name": listing_info["name"],
                            "last_char": listing_info["last_char"],
                            "posted": listing_info["posted"]["$date"],
                            "status": listing_info["status"],
                            "league": listing_info["league"],
                            "whisper": listing_info["whisper"],
                            "language": listing_info["language"],
                            "has": {
                                "min_amount": listing_info["has_rate"],
                                "max_amount": listing_info["has_stock"],
                            },
                            "want": {"min_amount": listing_info["want_rate"]},
                        },
                    }
                    if listing_info["has_curr"] in obj["listings"]:
                        obj["listings"][listing_info["has_curr"]].append(new_listing)
                    else:
                        obj["listings"][listing_info["has_curr"]] = [new_listing]
                    count += 1
            obj["trades_num"] = count
            start_curr_info = []
            end_curr_info = []
            if obj["trades"][0] in obj["listings"]:
                start_curr_info = obj["listings"][obj["trades"][0]]
                end_curr_info = obj["listings"][obj["trades"][-1]]
            start_amt = 0
            end_amt = 0
            for listing in start_curr_info:
                start_amt += (
                    listing["order_size"] * listing["info"]["want"]["min_amount"]
                )
            for listing in end_curr_info:
                solution = listing["order_size"]
                has_rate = listing["info"]["has"]["min_amount"]
                end_amt += solution * has_rate
            obj["total_profit"] = end_amt - start_amt
            obj["profit_per_trade"] = obj["total_profit"] / obj["trades_num"] if obj["trades_num"] != 0 else None
            objs.append(obj)
        return objs

    def remove_dupes(self, entries):
        """ Removes duplicate whispers """
        new_entries = []
        for entry in entries:
            if entry not in new_entries:
                new_entries.append(entry)
        return new_entries

    def get_trades_profit(self, starting_currency):
        """ Gets profits for all paths """
        # Iterate through each edge
        # Create possible trade combinations for each edge
        # Sort trade combinations by net profit

        paths = self.simple_paths(starting_currency)
        profits = []
        for path in paths:
            # profits.append(self._get_path_solutions(path))
            path_solutions = self._get_path_solutions(path)
            profits += self._get_trade_profit(path_solutions)
        for entry in profits:
            if not entry["listings"]:
                profits.remove(entry)
        profits.sort(key=lambda x: x["total_profit"], reverse=True)
        print(len(profits))
        new_profits = self.remove_dupes(profits)
        print(len(new_profits))
        return new_profits
