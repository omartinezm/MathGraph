import math as mt
import copy

from mathgraph.graph import Graph

class MinSpanningTreeAlgorithm:
    '''
        Minimal Spanning Tree algorithm

        This class apply an algorithm over the graph. The result is a minimal spanning tree.
    '''
    kind="Minimal Spanning Tree"
    def __init__(self,graph) -> None:
        self.mst=Graph(name="mnt")
        self.prev=[]
        if isinstance(graph,Graph):
            self.apply(graph)
        else:
            print("A graph is needed. "+str(graph))

    def get_mst(self):
        return self.mst

    def get_graph(self):
        return self.graph

    def apply(self,graph):
        pass

    def to_draw(self):
        return self.prev

    def get_mst(self):
        self.mst.add_edge(self.prev)
        return self.mst

class Boruvka(MinSpanningTreeAlgorithm):
    kind="Boruvka"
    def __init__(self, graph) -> None:
        super().__init__(graph)

    def apply(self, graph):
        return super().apply(graph)

class Kruskal(MinSpanningTreeAlgorithm):
    '''
        Kruskal algorithm.
    '''
    kind="Kruskal"
    def __init__(self, graph) -> None:
        super().__init__(graph)

    def apply(self, graph):
        sortEdges=sorted(graph.get_edges(), key=lambda edge: edge.get_cost())
        F=[]
        vset={}
        vertexes=graph.get_vertexes()
        for vertex in vertexes:
            vset[vertex]=[vertex]
        for edge in sortEdges:
            l1=self.__find_tree__(vset,edge.start)
            l2=self.__find_tree__(vset,edge.end)
            if l1!=l2:
                F.append(edge)
                self.__join__(vset,l1,l2)
        self.prev=F
    
    def __join__(self,vset,v1,v2):
        if v1!=v2:
            for ver in vset[v2]:
                vset[v1].append(ver)
            del vset[v2]
    def __find_tree__(self,vset,vertex):
        keys=vset.keys()
        if vertex in keys:
            return vertex
        else:
            for key in keys:
                if vertex in vset[key]:
                    return key
        return None

class Prim(MinSpanningTreeAlgorithm):
    '''
        Prim's algorimth for min. spanning tree
    '''
    def __init__(self, graph) -> None:
        super().__init__(graph)

    def apply(self, graph):
        F,R,V=[],[], graph.get_vertexes() # Edges in the tree, Reached vertexes
        av=graph.get_vertexes()[0] # Actual vertex
        V.remove(av)
        while(len(V)>0):
            R.append(av)
            edges=set()
            for v in R:
                edges.update(graph.get_edges(ver=v))
            edges=sorted(edges, key=lambda edge: edge.get_cost())
            found=False
            while(not found):
                edge=edges[0]
                startend=[edge.start,edge.end]
                for v in startend:
                    if v not in R and v in V:
                        F.append(edge)
                        av=v
                        found=True
                        V.remove(av)
                        break
                edges=edges[1:]
        self.prev=F


