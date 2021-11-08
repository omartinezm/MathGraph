# This class provides miscelania algorithms to apply over graphs
from mathgraph import graph
import numpy as np


class DepthFirstSearch():
    '''
        Depth First Search algoritm

        Given a vertex find all the connected vertex to the given one
    '''
    def __init__(self, graph,source=None) -> None:
        self.graph=graph
        self.source=source
        self.labels=[]
        self.edges=[]
        if self.source:
            if self.__validate__(source):
                self.apply(source)
            else:
                print("Source vertex "+str(source)+" does not exist in the graph.")

    def __validate__(self,vertex):
        if vertex not in self.graph.get_vertexes():
            return False
        else:
            return True

    def apply(self,v):
        '''
            Apply the class over the graph.

            It starts over the given vertex and iteratively find the connected vertexes.
        '''
        self.labels.append(v)
        edges=self.graph.get_edges(ver=v,starting=True,ending=False)
        for edge in edges:
            if edge.end not in self.labels:
                self.edges.append(edge)
                self.apply(edge.end)
    
    def to_draw(self):
        '''
            Returns the edges of the tree
        '''
        return self.edges

class ConnectedComponents():
    '''
        Connedted Components

        This classs applied over a graph find the connected components of the graph. It uses
        the DepthFirstSearch to construct the forest.
    '''
    def __init__(self,graph) -> None:
        self.graph=graph
        self.cc=[]
        self.__to_draw__=[]
        self.apply()
        self.__edges_to_draw__()

    def apply(self):
        '''
            Apply the class over the graph.

            It starts over the first listed vertex with no connected component and then
            follows with the next vertex with no connected component
        '''
        missing=self.graph.get_vertexes()
        while len(missing)>0:
            comp=DepthFirstSearch(self.graph,source=missing[0])
            self.cc.append(comp.edges)
            missing=list(set(missing)-set(comp.labels))
    def __edges_to_draw__(self):
        '''
            Once the connected components are constructed it put all the edges on a single
            list.
        '''
        self.__to_draw__= [edge for path in self.cc for edge in path]
    
    def to_draw(self):
        '''
            Returns the edges of the forest
        '''
        return self.__to_draw__

    def get_cc(self):
        '''
            Returns the connected components
        '''
        return self.cc

class PageRank:
    '''
        A page rank implementation
    '''
    def __init__(self,graph,iterations=100,dumf=0.85,aspercentage=False) -> None:
        self.graph=graph
        self.iterarions=iterations
        self.dumf=dumf
        self.rank=[]
        self.aspercentage=aspercentage
        self.apply()
        self.__save_rank__()
    
    def apply(self):
        '''
            Apply the pagerank algorithm over the graph
        '''
        M=self.graph.create_adjacency_matrix()
        n=M.shape[1]
        rank=np.random.rand(n,1)
        rank/=np.linalg.norm(rank,1)
        Mh=(self.dumf*M+(1-self.dumf)/n)
        for i in range(self.iterarions):
            rank = Mh@rank
        self.rank=rank/np.linalg.norm(rank,1)

    def __save_rank__(self):
        i=0
        for ver in self.graph.get_vertexes():
            ver.add_updater("pagerank")
            if self.aspercentage:
                ver.update_val(key="pagerank",val=round(100*self.rank[i][0],2))
            else:
                ver.update_val(key="pagerank",val=self.rank[i][0])
            i+=1
    
    def get_ranks(self):
        return self.rank