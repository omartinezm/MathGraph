class Edge:
    """ Edge class
    
        This class models an edge of the graph. It is formed by a start vertex, an end vertex and
        a weight, and a name.
        
        Attributes:
        -----------
        vin : Vertex
            start vertex of the edge
        vend : Vertex
            end vertex of the edge
        cost : float
            Cost of the edge
        name  : str
            A name for the graph
        updaters : dict
            A dictionary with all the stats an object to be updated in any change of the graph
    """
    kind = 'edge'
    def __init__(self,vin,vend,cost=None,name=None, updaters=None):
        self.start=vin
        self.end=vend
        self.cost=cost
        self.name=name
        if updaters:
            self.updaters={}
            self.__create_updaters__(updaters)
        else:
            self.updaters=None
    def __create_updaters__(self,updaters):
        for up in updaters:
            self.updaters[up]=0
    def get_name(self):
        return self.name
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
    def get_cost(self):
        return self.cost
    def get_updaters(self):
        return self.updaters
    def __repr__(self):
        return "Edge ("+self.start.get_name()+","+self.end.get_name()+")"
    def update_val(self,key=None,val=None):
        if key and self.updaters:
            self.updaters.update({key:val})
        else:
            self.updaters[key]=val