import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allCountries = DAO.getAllCountries()
        self._retailers = []

        self._grafo = nx.Graph()

    def buildGraph(self, country, year):

        self._grafo.clear()
        self._retailers = DAO.getRetailers(country)
        self._grafo.add_nodes_from(self._retailers)

        self.addEdge(year, country)

    def addEdge(self, year, country):
        for r1 in self._retailers:
            for r2 in self._retailers:
                if r1.Retailer_code != r2.Retailer_code:
                    peso = DAO.getPeso(r1, r2, year, country)
                    if peso > 0:
                        self._grafo.add_edge(r1, r2, weight=peso)

    def getVolumeRetailer(self):
        listTuple = []
        for n in self._grafo.nodes:
            vicini = nx.neighbors(self._grafo, n)
            volume = 0
            for v in vicini:
                volume += self._grafo[n][v]["weight"]
            listTuple.append((n, volume))
        listTupleSorted = sorted(listTuple, key=lambda x: x[1], reverse=True)
        return listTupleSorted
