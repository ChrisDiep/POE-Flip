import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    """ Class for creating and analyzing a graph of currencies """
    def __init__(self, data):
        self.data = data
        self.currencies = self._parse_currencies(data)
        self.graph = nx.DiGraph()
        self.create_graph()

    def _parse_currencies(self, data):
        """ Maps the currencies from the database information to an array """
        currencies = []
        for entry in data:
            currencies.append(entry["currency_name"])
        return currencies

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
