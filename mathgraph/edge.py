from mathgraph.vertex import Vertex


class Edge:
    """ Edge class

        This class models an edge of the graph. It is formed by a start vertex, an end vertex and
        a weight, and a name.

        Attributes:
        -----------
        start : Vertex
            Start vertex of the edge
        end : Vertex
            End vertex of the edge
        direction : "LEFT" || "RIGHT", optional
            For directed graph
        cost : float, optional
            Cost of the edge
        name  : str, optional
            A name for the graph
        updaters : dict, optional
            A dictionary with all the stats an object to be updated in any change of the graph
    """
    kind = 'edge'
    def __init__(self, start:Vertex, end:Vertex, direction=None, cost=1, name=None, updaters=None):
        self.start=start
        self.end=end
        self.direction=direction
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
    
    def add_updater(self,key):
        if key not in self.updaters.keys():
            self.updaters[key]=0
    
    def delete_updater(self,key):
        if key in self.updaters.keys():
            del self.updaters[key]
    
    def get_name(self):
        return self.name
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    def get_vertexes(self):
        return [self.start,self.end]
    
    def get_cost(self):
        return self.cost
    
    def set_cost(self,cost):
        assert cost, "You must specify a cost"
        self.cost=cost
    
    def get_updaters(self):
        return self.updaters
    
    def get_updater_val(self,key):
        try:
            return self.updaters[key]
        except:
            self.add_updater(key)
            return self.updaters[key]
    
    def __repr__(self):
        return "Edge ("+self.start.get_name()+","+self.end.get_name()+",cost="+str(self.cost)+")"
    
    def update_val(self,key=None,val=None):
        try:
            if key and self.updaters:
                self.updaters.update({key:val})
            else:
                raise Exception
        except Exception as inst:
            print("The key {0} is'nt a updater valid updater value in edge {1}".format(key,self.name))
