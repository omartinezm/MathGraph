from sys import path

import numpy
from math_graph.graph import *
from algorithms.search_algorithms import *
from algorithms.min_spanning_tree import *
from numpy import *
import random as rd

from math_graph.tree import Tree




file=open("D:\graph_package\im1.csv")
im1=numpy.loadtxt(file, delimiter=";")
g1=Graph(incidence_matrix=im1)
edges=g1.get_edges()
for edge in edges:
    edge.set_cost(rd.randint(1,5))
edges[1].set_cost(19)
g1=Graph(edges=edges)
vertexes=g1.get_vertexes()
# print(edges)
source=vertexes[0]
target=vertexes[2]
dj=Dijkstra(g1,source=source,target=target)
# print(dj.get_gime())
# print(dj.path)
ar=AStar(g1,source=source,target=target)
# print(ar.get_gime())
gr=Greddy(g1,source=source,target=target)
# print(gr.get_gime())
bf=BellmanFord(g1,source=source,target=target)
# print(bf.get_gime())
fw=FloydWarshall(g1,source=source,target=target)
print(fw.get_gime())
# g1.draw(path=dj.path)
# g1.draw(path=ar.path)
# g1.draw(path=gr.path)
# g1.draw(path=bf.path)
# print(fw.path)
# g1.draw(path=fw.path)
kr=Kruskal(g1)
# print(kr.prev)
g1.draw(mst=kr.prev,path=gr.path)