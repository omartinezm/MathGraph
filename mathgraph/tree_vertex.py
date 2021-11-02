from mathgraph.vertex import Vertex

class TreeVertex(Vertex):
    """ Tree vertex class
    
        This class models the elements of the tree. It is a subclass of the Vertex class.
        It also have the parent and the leafs ot he node of the tree.
        
        Attribute:
        ----------
        parent : TreeVertex, optional
            Parent of the vertex
    """
    def __init__(self,name,weight=0,parent=None,updaters=None,height=None):
        """ We set the parent and the updaters.
        """
        super().__init__(name,weight,updaters)
        self.parent=parent
        self.leafs=[]
        self.height=height
        
    def get_parent(self):
        """ Returns the parent of the vertex
        """
        return self.parent
    def get_leafs(self):
        """ Returns the leafs of the vertex
        """
        return self.leafs
    def get_height(self):
        """ Returns the height of the vertex
        """
        return self.height
    def set_parent(self,parent):
        """ Set the parent of the vertex
        """
        self.parent=parent
    def set_height(self,h):
        """ Set the height of the vertex
        """
        self.height=h
    def add_leafs(self,leaf):
        """ Add leafs to the vertex
        """
        self.leafs.append(leaf)
    def delete_parent(self):
        """ Delete the parent
        """
        self.parent=None
    def delete_leaf(self,leaf):
        """ Delete a leaf
        """
        self.leafs.remove(leaf)
    def __repr__(self):
        rep="TreeVertex (name='"+self.name+"',weight="+str(self.weight)
        if self.parent:
            rep+=", parent="+self.parent.get_name()
        rep+=")"
        return rep
