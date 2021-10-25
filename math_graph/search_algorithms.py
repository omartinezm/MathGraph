import math as mt
import random as rd
import numpy as np
from timeit import default_timer as timer
from pyglet.libs.win32.constants import FROM_LEFT_1ST_BUTTON_PRESSED

###
# This file provides search algorithms to apply over graphs.

class SearhAlgorithm:
    kind="Search Algorithm"
    def __init__(self,graph,source=None,target=None) -> None:
        self.graph=graph
        self.source=source
        self.target=target
        self.path=[]
        self.run_time=0

    '''
        Returns True if the vertex is in the graph, False if not.
    '''
    def __validate__(self,vertex):
        if vertex not in self.graph.get_vertexes():
            return False
        else:
            return True

    """
        Apply the algorithm
    """
    def apply(self):
        pass

    '''
        Returns the time needed to run the algorithm
    '''
    def get_gime(self):
        return self.kind,self.run_time
    
class Dijkstra(SearhAlgorithm):
    '''
        Implementation of Dijkstra's algorithm over a graph.
    '''
    kind="Dijkstra"
    def __init__(self,graph,source=None,target=None) -> None:
        super().__init__(graph,source,target)
        self.dist={}
        self.prev={}
        self.path=[]
        fsource=False
        if self.source:
            if not self.__validate__(self.source):
                print("Source vertex "+str(self.source)+" does not exist in the graph")
            else:
                fsource=True
        if self.target:
            if not self.__validate__(self.target):
                print("Target vertex "+str(self.target)+" does not exist in the graph")
        if fsource:
            self.apply()
        
    
    """
        Apply the Dijkstra algorithm
    """
    def apply(self):
        stime=timer()
        Q=[]
        for v in self.graph.get_vertexes():
            self.dist[v]=mt.inf
            self.prev[v]=None
            Q.append(v)
        self.dist[self.source]=0
        while(len(Q)>0):
            u=self.__find_min__(Q)
            if u==self.target:
                break
            Q.remove(u)
            neig=self.graph.find_neighborhood_vertexes(u,starting=True,ending=True)
            for vertex in neig:
                alt=self.dist[u]+1
                if alt<self.dist[vertex]:
                    self.dist[vertex]=alt
                    self.prev[vertex]=u
        etime=timer()
        self.run_time=etime-stime
        self.find_path()
    
    """
        Find the element with the minimun distance on the set Q
        Q = list o vertexes
        dist = dictionary of distances
    """
    def __find_min__(self,Q):
        min=Q[0]
        for vertex in Q:
            if self.dist[vertex]<self.dist[min]:
                min=vertex
        return min
    
    """
        Find the path between the source and target
    """
    def find_path(self):
        path=[self.target]
        act=self.target
        end=False
        while(not end):
            if act not in self.prev.keys():
                end=True
                path=[]
                break
            path.append(self.prev[act])
            act=self.prev[act]
            if act==self.source:
                end=True
        self.path=path
    """
        Set the source of the algorithm
    """
    def set_source(self, vertex):
        if self.__validate__(vertex):
            self.source=vertex

    """
        Set the target of the algorithm
    """
    def set_target(self, vertex):
        if self.__validate__(vertex):
            self.target=vertex
    
    """
        Returns the source
    """
    def get_source(self):
        return self.source
    
    """
        Returns the target
    """
    def get_target(self):
        return self.target
    
class AStar(SearhAlgorithm):
    kind="AStar"
    def __init__(self,graph,source=None,target=None):
        super().__init__(graph,source,target)
        self.prev={}
        self.dist={}
        self.fdist={}
        if self.source:
            if not super().__validate__(self.source):
                print("Source vertex "+str(self.source)+" does not exist in the graph")
            else:
                fsource=True
        if self.target:
            if not super().__validate__(self.target):
                print("Target vertex "+str(self.target)+" does not exist in the graph")
        if fsource:
            self.apply()
    
    def apply(self):
        stime=timer()
        dset=[self.source]
        for v in self.graph.get_vertexes():
            self.dist[v]=mt.inf
            self.fdist[v]=mt.inf
            self.prev[v]=None
        self.dist[self.source]=0
        self.fdist[self.source]=self.source.get_weight()
        while(len(dset)>0):
            u=self.__find_min__(dset)
            if u==self.target:
                break
            dset.remove(u)
            edges=self.graph.get_edges(u)
            
            for edge in edges:
                alt=self.dist[u]+edge.get_cost()
                neig = edge.start if edge.start != u else edge.end
                if alt<self.dist[neig]:
                    self.prev[neig]=u
                    self.dist[neig]=alt
                    self.fdist[neig]=self.dist[neig]+neig.get_weight()
                    if neig not in dset:
                        dset.append(neig)
        etime=timer()
        self.run_time=etime-stime
        self.find_path()

    def __find_min__(self,Q):
        min=Q[0]
        for vertex in Q:
            if self.fdist[vertex]<self.fdist[min]:
                min=vertex
        return min

    def find_path(self):
        path=[self.target]
        act=self.target
        end=False
        while(not end):
            if act not in self.prev.keys():
                end=True
                path=[]
                break
            path.append(self.prev[act])
            act=self.prev[act]
            if act==self.source:
                end=True
        self.path=path