from math_graph.graph import *
from math_graph.tree import *
from math_graph.tree_vertex import *
from numpy import *

im1=np.zeros([12,12])
im1[0,0]=1
im1[1,0]=1
#
im1[0,1]=1
im1[2,1]=1
#
im1[1,2]=1
im1[3,2]=1
#
im1[1,3]=1
im1[4,3]=1
#
im1[2,4]=1
im1[5,4]=1
#
im1[2,5]=1
im1[6,5]=1
#
im1[2,6]=1
im1[7,6]=1
#
im1[4,7]=1
im1[8,7]=1
#
im1[5,8]=1
im1[9,8]=1
#
im1[6,9]=1
im1[10,9]=1
#
im1[6,10]=1
im1[11,10]=1
#
im1[0,11]=1
im1[5,11]=1
#

print(im1)
g1=Graph(incidence_matrix=im1)
#print(g1)
g1.draw()
# v1=TreeVertex("v1")
# v2=TreeVertex("v2")
# v3=TreeVertex("v3")
# e1=Edge(v1,v2)
# e2=Edge(v2,v3)
# g2=Tree(edges=[e1,e2])
# print(g2)
# g2.draw()