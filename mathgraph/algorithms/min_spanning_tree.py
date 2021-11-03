import math as mt

from mathgraph.graph import Graph

class MinSpanningTreeAlgorithm:
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

class Boruvka(MinSpanningTreeAlgorithm):
    kind="Boruvka"
    def __init__(self, graph) -> None:
        super().__init__(graph)

    def apply(self, graph):
        return super().apply(graph)

class Kruskal(MinSpanningTreeAlgorithm):
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