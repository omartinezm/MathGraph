import math as mt
import random as rd
import numpy as np
from timeit import default_timer as timer

###
# This file provides search algorithms to apply over graphs.


class SearchAlgorithm:
    kind="Search Algorithm"
    def __init__(self,graph,source=None,target=None) -> None:
        self.graph=graph
        self.dist={}
        self.prev={}
        self.path={}
        self.run_time=0
        self.source=source
        self.target=target
        self.fsource=False
        if source:
            if not self.__validate__(source):
                print("Source vertex "+str(source)+" does not exist in the graph")
            else:
                self.fsource=True
        if target:
            if not self.__validate__(target):
                print("Target vertex "+str(target)+" does not exist in the graph")
                

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

    def find_path(self):
        path={}
        act=self.target
        end=False
        while(not end):
            if act not in self.prev.keys():
                end=True
                path=[]
                break
            path[act]=self.prev[act]
            act=self.prev[act]
            if act==self.source:
                end=True
        self.path=path
    
    '''
        Returns the time needed to run the algorithm
    '''
    def get_gime(self):
        fortime=float("{:.20f}".format(self.run_time))
        return self.kind,self.run_time

    '''
        Set the source of the algorithm
    '''
    def set_source(self, vertex):
        if self.__validate__(vertex):
            if self.source == vertex:
                pass
            else:
                self.source=vertex
                print("Source changed. You must run the 'apply' method  to refresh the paths.")

    '''
        Set the target of the algorithm
    '''
    def set_target(self, vertex):
        if self.__validate__(vertex):
            if self.target == vertex:
                pass
            else:
                self.target=vertex
                print("Target changed. You must run the 'find_path' method to refresh the path.")
    
    '''
        Returns the source
    '''
    def get_source(self):
        return self.source
    
    '''
        Returns the target
    '''
    def get_target(self):
        return self.target
    
class Dijkstra(SearchAlgorithm):
    '''
        Implementation of Dijkstra's algorithm over a graph.
    '''
    kind="Dijkstra"
    def __init__(self,graph,source=None,target=None) -> None:
        super().__init__(graph,source,target)
        if self.fsource:
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
            edges=self.graph.get_edges(u)
            for edge in edges:
                alt=self.dist[u]+edge.get_cost()
                neig = edge.start if edge.start != u else edge.end
                if alt<self.dist[neig]:
                    self.prev[neig]=u
                    self.dist[neig]=alt
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
    
    
class AStar(SearchAlgorithm):
    kind="AStar"
    def __init__(self,graph,source=None,target=None):
        super().__init__(graph,source,target)
        self.fdist={}
        if self.fsource:
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

class Greddy(SearchAlgorithm):
    kind="Greedy"
    def __init__(self, graph, source=None, target=None) -> None:
        super().__init__(graph, source=source, target=target)
        if self.fsource:
            self.apply()

    def apply(self):
        stime=timer()
        Q=[]
        for v in self.graph.get_vertexes():
            self.dist[v]=-mt.inf
            self.prev[v]=None
            Q.append(v)
        self.dist[self.source]=0
        while(len(Q)>0):
            u=self.__find_max__(Q)
            if u==self.target:
                break
            Q.remove(u)
            neig=self.graph.find_neighborhood_vertexes(u,starting=True,ending=True)
            for vertex in neig:
                alt=vertex.get_weight()
                if alt>self.dist[vertex]:
                    self.dist[vertex]=alt
                    self.prev[vertex]=u
        etime=timer()
        self.run_time=etime-stime
        self.find_path()
    
    def __find_max__(self,Q):
        max=Q[0]
        for vertex in Q:
            if self.dist[vertex]>self.dist[max]:
                max=vertex
        return max

class BellmanFord(SearchAlgorithm):
    kind="Bellman Ford"
    def __init__(self, graph, source=None, target=None) -> None:
        super().__init__(graph, source=source, target=target)
        if self.fsource:
            self.apply()

    def apply(self):
        stime=timer()
        for v in self.graph.get_vertexes():
            self.dist[v]=mt.inf
            self.prev[v]=None
        self.dist[self.source]=0
        edges=self.graph.get_edges()
        for _ in range(len(self.graph.get_vertexes())-1):
            for edge in edges:
                alt=self.dist[edge.start]+edge.get_cost()
                if alt<self.dist[edge.end]:
                    self.dist[edge.end]=alt
                    self.prev[edge.end]=edge.start

        for edge in edges:
            if self.dist[edge.start]+edge.get_cost()<self.dist[edge.end]:
                print("The graph contains a cycle with negative weight")
        etime=timer()
        self.run_time=etime-stime
        self.find_path()
    
class FloydWarshall(SearchAlgorithm):
    kind="FloydWarshall"
    def __init__(self, graph, source=None, target=None) -> None:
        super().__init__(graph, source=source, target=target)
        if self.fsource:
            self.apply()

    def apply(self):
        stime=timer()
        for v in self.graph.get_vertexes():
            self.dist[v]={}
            self.prev[v]={}
            for w in self.graph.get_vertexes():
                if v==w:
                    self.dist[v][w]=0
                    self.prev[v][w]=v
                else:
                    self.dist[v][w]=mt.inf
                    self.prev[v][w]=None

        edges=self.graph.get_edges()
        for edge in edges:
            self.dist[edge.start][edge.end]=edge.get_cost()
            self.prev[edge.start][edge.end]=edge.end
        for v1 in self.graph.get_vertexes():
            for v2 in self.graph.get_vertexes():
                for v3 in self.graph.get_vertexes():
                    alt=self.dist[v2][v1]+self.dist[v1][v3]
                    if alt<self.dist[v2][v3]:
                        self.dist[v2][v3]=alt
                        self.prev[v2][v3]=self.prev[v2][v1]

        etime=timer()
        self.run_time=etime-stime
        self.find_path()
    
    def find_path(self):
        exist=True
        path=[self.source]
        if self.target==None:
            exist=False
            path=[]
        elif self.prev[self.source][self.target]==None:
            exist=False
            path=[]
        if exist:
            s=self.source
            t=self.target
            while(s!=t):
                s=self.prev[s][t]
                path.insert(0,s)
                self.path[path[1]]=path[0]
        self.path
