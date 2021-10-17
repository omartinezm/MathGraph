from math_graph.graph import Graph
import warnings

class Tree(Graph):
    kind = 'Tree'
    """ Tree class

        This class models a tree graph. It is a subclass of the graph class.
    """
    def __init__(self,vertex=[],edges=[],binary=False,name=None,updaters=None):
        super().__init__(name=name,updaters=updaters,isdirected=True)
        self.binary=binary
        self.add_edge(edges)
        self.height=self.get_height()
    def add_edge(self,edgs):
        """ Add an edge to the graph and update the graph stats, if any.

            If the vertex does not exist in the graph, it is added

            Parameters:
            ===========
            edges: list
                A list of edges to add
        """
        for edge in edgs:
            exist=self.__exist_edge__(edge)
            if(not exist):
                if edge.end.parent:
                    return "This edge is not admisible on a tree. The vertex "+edge.end.get_name()+" already have a parent"
                # If we are in this part of code then the edge is admisible.
                self.__add_new_edge__(edge)
                # If is a binary graph we set the left and right leaf
                if edge.direction:
                    edge.start.add_leafs(edge.end,edge.direction)
                else:
                    edge.start.add_leafs(edge.end)
                # New part on the graph, it set the parent and leafs
                edge.end.set_parent(edge.start)
                self.edges.append(edge)
        """ if self.autoupdate:
            # Update the graph stats if case
            for ed in edges:
                self.update(vertex=[ed.end],propagate=False) """
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
    def find_root(self):
        """ Find the root of the tree
        """
        v=self.get_vertexes()[0]
        while(True):
            if v.get_parent():
                v=v.get_parent()
            else:
                break
        return v

    def get_height(self):
        """ Find the height of the tree
        """
        start=self.find_root()
        if self.binary:
            leafs=start.get_leafs().values()
        else:
            leafs=start.get_leafs()
        h=0
        while(leafs):
            h+=1
            new=[]
            for leaf in leafs:
                if self.binary:
                    new.extend(leaf.leafs.values())
                else:
                    new.extend(leaf.get_leafs())
            leafs=new
        return h

    def draw_console(self,v=None,deep=0):
        """ Draw a representation of the tree on the console

            Parameters:
            ===========
            v : vertex
                The vertex from which we start the graph. You can
                draw all he graph or from an specific vertex.
            deep : int >0
                The deep of the vertex. Works a as tabulation.
        """
        if not v:
            v=self.find_root()
        if(deep==0):
            text=v.get_name()
        elif(deep>1):
            text="  "*(deep)+"\-"+v.get_name()+"    [deep="+str(deep)+"]"
        else:
            text="\\"*(deep)+"-"+v.get_name()+"    [deep="+str(deep)+"]"
        print(text)
        if self.binary:
            for f in v.get_leafs().values():
                deep+=1
                self.draw_console(f,deep)
                deep-=1
        else:
            for f in v.get_leafs():
                deep+=1
                self.draw_console(f,deep)
                deep-=1

