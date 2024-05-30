import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allCountries = DAO.getAllCountries()
        self._retailers = []
        self._idMap = {}

        self._grafo = nx.Graph()

        self._solBest = []
        self._pesoBest = 0

    def buildGraph(self, country, year):

        self._grafo.clear()
        self._retailers = DAO.getRetailers(country)
        for r in self._retailers:
            self._idMap[r.Retailer_code] = r
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

    def getBestPath(self, N):
        self._solBest = []
        self._pesoBest = 0
        for n in self._grafo.nodes:  # per ogni nodo
            if len(list(nx.neighbors(self._grafo, n))) != 0:  # controllo che abbia dei vicini
                source = n  # il nodo n è il nodo sorgente da cui parte il cammino
                parziale = [source]  # quindi posso già aggiungerlo in parziale
                self.ricorsione(parziale, N)
        return self._solBest, self._pesoBest  # ritorno il cammino migliore e il peso migliore

    def ricorsione(self, parziale, N):
        # Verifico che parziale possa essere una soluzione sia una soluzione ottima
        if len(parziale) == N+1 and parziale[-1] == parziale[0]:  # e cioè se i nodi sono esattamente N+1 (archi devono essere N) e se l'ultimo nodo del percorso è lo stesso del nodo iniziale
            if self.pesoTot(parziale) > self._pesoBest:  # se il peso del nuovo cammino è maggiore rispetto a quello trovato fino ad ora allora diventa quello ottimo
                self._pesoBest = self.pesoTot(parziale)  # mi salvo il peso tot e il cammino
                self._solBest = copy.deepcopy(parziale)
            return  # Se non è un cammino ottimo non posso più continuare perchè ho raggiunto il num massimo di nodi e quindi esco
        # Se invece non è una soluzione devo continuare ad aggiungere nodi in parziale per trovarla
        for n in nx.neighbors(self._grafo, parziale[-1]):  # per ogni vicino n dell'ultimo nodo in parziale
            if (n not in parziale and len(parziale) < N) or (n in parziale and len(parziale) == N):
            # Posso aggiungerlo in parziale solo se è un nodo che non è stato attraversato oppure che è stato già attraversato
            # ma essendo l'ultimo del percorso deve essere uguale al nodo sorgente
                parziale.append(n)
                self.ricorsione(parziale, N)
                parziale.pop()

    def pesoTot(self, listOfNodes):
        peso = 0
        for i in range(0, len(listOfNodes)-1):
            peso += self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return peso

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
