import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, data):
        self.data = data
        self.currencies = self._parse_currencies(data)
        self.graph = nx.DiGraph()
        self.create_graph()

    def _parse_currencies(self, data):
        currencies = []
        for entry in data:
            currencies.append(entry["currency_name"])
        return currencies

    def create_graph(self):
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
        self.graph.add_edge(start, end, trades=listings)

    def print(self):
        return " ".join(list(self.graph.nodes))

    def visualize(self):
        nx.draw(self.graph, with_labels=True, font_weight="bold")
        plt.show()
