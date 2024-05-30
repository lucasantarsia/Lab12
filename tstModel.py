from datetime import datetime

import networkx as nx

from model.model import Model

model = Model()

model.buildGraph("Germany", 2016)
print(len(model._grafo.nodes))
print(len(model._grafo.edges))
print(*model._grafo.nodes, sep='\n')
print(*model._grafo.edges, sep='\n')

listaRetailerVolume = model.getVolumeRetailer()
for ret, vol in listaRetailerVolume:
    print(ret, vol)

tic = datetime.now()
camminoOttimo, pesoOttimo = model.getBestPath(5)
print(f"tempo: {(datetime.now() - tic)}")
print(f"peso = {pesoOttimo}")
print(*camminoOttimo, sep='\n')
