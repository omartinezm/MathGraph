from tree_vertex import TreeVertex

class BinTreeVertex(TreeVertex):
    """ Binary tree vertex class

        This class models the elements of a binary tree. It is a subclass of the TreeVertex class.

        Attribute:
        ----------
        parent : TreeVertex, optional
            Parent of the vertex
    """
    def __init__(self,name,parent=None,left=None,right=None,updaters=None):
        """ We set the parent and the updaters.
        """
        super().__init__(name,updaters)
        self.parent=parent
        self.leafs={}

    def set_left(self,left):
        self.leafs["LEFT"]=left
        self.left=left

    def set_right(self,right):
        self.leafs["RIGHT"]=right

    def add_leafs(self,leaf,direction):
        """ Add a leaf to the vertex
        """
        if direction=="LEFT":
            self.set_left(leaf)
        elif direction=="RIGHT":
            self.set_right(leaf)

    def __repr__(self):
        rep="BinTreeVertex (name="+self.name
        if self.parent:
            rep+=", parent="+self.parent.get_name()
        rep+=")"
        return rep
