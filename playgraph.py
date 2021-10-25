from sys import path

import numpy
from math_graph.graph import *
from math_graph.tree import *
from math_graph.tree_vertex import *
from numpy import *

from math_graph.search_algorithms import *

# im1=np.zeros([18,18])
# im1[0,0]=1
# im1[1,0]=1
# #
# im1[0,1]=1
# im1[2,1]=1
# #
# im1[0,13]=1
# im1[13,13]=1
#
# im1[0,13]=1
# im1[13,13]=1
# #
# im1[0,14]=1
# im1[14,14]=1
# #
# im1[0,15]=1
# im1[15,15]=1
# #
# im1[0,16]=1
# im1[16,16]=1
# #
# im1[0,17]=1
# im1[17,17]=1
#
# im1[1,2]=1
# im1[3,2]=1
# #
# im1[1,3]=1
# im1[4,3]=1
# #
# im1[2,4]=1
# im1[5,4]=1
# #
# im1[2,5]=1
# im1[6,5]=1
# #
# im1[2,6]=1
# im1[7,6]=1
# #
# im1[4,7]=1
# im1[8,7]=1
# #
# im1[5,8]=1
# im1[9,8]=1
# #
# im1[6,9]=1
# im1[10,9]=1
# #
# im1[6,10]=1
# im1[11,10]=1
# #
# im1[0,11]=1
# im1[5,11]=1
#
# n=20
# im1=np.zeros([n+1,n])
# for i in range(n):
#     im1[i][i]=1
#     im1[i+1][i]=1
#print(im1)
file=open("D:\graph_package\im1.csv")
im1=numpy.loadtxt(file, delimiter=";")
g1=Graph(incidence_matrix=im1)
#print(g1)

vertexes=g1.get_vertexes()
# print(vertexes)
source=vertexes[0]
target=vertexes[3]
# print(source)
# print(target)
dj=Dijkstra(g1,source=source)#,target=target)
# print("DIST")
# print(dj.dist)
# print("FDIST")
# print(dj.fdist)
# print("PREV")
# print(dj.prev)
# print("PATH")
# print(dj.path)
print(dj.get_gime())
ar=AStar(g1,source=source)#,target=target)
print(ar.get_gime())
g1.draw(path=dj.path)