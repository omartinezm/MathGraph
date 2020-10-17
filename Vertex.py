class Vertex(object):
    """ Vertex class
        
        This class models a vertex on a graph. It is formed by a name, a weight and a object to contain.
        
        Attributes:
        -----------
        name  : str
            A name for the graph
        weight : float
            A number which indicates the weight of the vertex
        contain : object
            An object
        updaters : dict
            A dictionary with all the stats an object to be updated in any change of the graph
    """
    kind = 'vertex'
    def __init__(self,name,weight=0,contain=None,updaters=None):
        self.weight=weight
        self.name=name
        self.edges=[]
        self.contain=contain
        self.updaters={}
        if updaters:
            self.__create_updaters__(updaters)
    def __create_updaters__(self,updaters):
        for up in updaters:
            self.updaters[up]=0
    def add_updater(self,key):
        if key not in self.updaters.keys():
            self.updaters[key]=0
    def delete_updater(self,key):
        if key in self.updaters.keys():
            del self.updaters[key]
    def get_weight(self):
        return self.weight
    def set_weight(self,n_weight):
        self.weight=n_weight
    def set_name(self,n_name):
        self.name=n_name
    def get_updaters(self):
        return self.updaters
    def get_updater_val(self,key):
        try:
            return self.updaters[key]
        except:
            self.add_updater(key)
            return self.updaters[key]
    def add_edge(self,edge):
        self.edges.append(edge)
    def get_name(self):
        return self.name
    def get_contain(self):
        return self.contain
    def set_contain(self, contain):
        self.contain=contain
    def __repr__(self):
        return "Vertex (name='"+self.name+"',weight="+str(self.weight)+")"
    def set_update_val(self,key=None,val=None):
        if key and self.updaters:
            self.updaters.update({key:val})
        else:
            self.updaters[key]=val