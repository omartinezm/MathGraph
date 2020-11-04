from graph import Graph
import warnings

class Tree(Graph):
    kind = 'Tree'
    def __init__(self,vertex=[],edges=[],name=None,updaters=None):
        super().__init__(name=name,updaters=updaters)
        self.vertex={}
        self.edges=[]
        self.add_edge(edges)
    def add_edge(self,edges):
        """ Add an edge to the graph and update the graph stats, if any.
        
            If the vertex does not exist in the graph, it is added
            
            Parameters:
            ===========
            edges: list
                A list of edges to add        
        """
        for edge in edges:
            exist=self.__exist_edge__(edge)
            if(not exist):
                if edge.end.parent:
                    return "This edge is not admisible on a tree. The vertex "+edge.end.get_name()+" already have a parent"
                # If we are in this part of code then the edge is admisible.
                self.__add_new_edge__(edge)
                self.edges.append(edge)
                # New part on the graph, it set the parent and leafs
                edge.end.set_parent(edge.start)
                edge.start.add_leafs([edge.end])
        if self.autoupdate:
            # Update the graph stats if case
            for ed in edges:
                self.update(vertex=[ed.end],propagate=False)
    def delete_edge(self, edge):
        """ Deletes an edge
            
            The in_degree and out_degree is updated.
            
            Parameters:
            ===========
            edge : Edge
                The edge we want to delete.
        """
        if super().delete_edge(edge):
            edge.end.delete_parent()
            edge.start.delete_leaf(edge.end)
            return True
        else:
            return False