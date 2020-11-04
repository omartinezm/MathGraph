from vertex import Vertex

class TreeVertex(Vertex):
    """ Tree vertex class
    
        This class models the elements of the tree. It is a subclass of the Vertex class.
        It also have the parent and the leafs ot he node of the tree.
        
        Attribute:
        ----------
        parent : TreeVertex, optional
            Parent of the vertex
        leafs : list, optional
            Leafs of the tree from this vertex
    """
    def __init__(self,name,parent=None, leafs=[],updaters=None):
        """ We set the parent, the leafs and the updaters.
        """
        super().__init__(name,updaters)
        self.parent=parent
        self.leafs=leafs
        
    def get_parent(self):
        """ Returns the parent of the vertex
        """
        return self.parent
    def get_leafs(self):
        """ Returns the leafs of the vertex
        """
        return self.leafs
    def set_parent(self,parent):
        """ Set the parent of the vertex
        """
        self.parent=parent
    def add_leafs(self,leafs):
        """ Add leafs to the vertex
        """
        self.leafs.extend(leafs)
    def delete_parent(self):
        """ Delete the parent
        """
        self.parent=None
    def delete_leaf(self,leaf):
        """ Delete a leaf
        """
        self.leafs.remove(leaf)
    def __repr__(self):
        rep="TreeVertex (name="+self.name
        if self.parent:
            rep+=", parent="+self.parent.get_name()
        #if self.leafs:
        #    rep+=", leafs="+str(self.leafs)
        rep+=")"
        return rep