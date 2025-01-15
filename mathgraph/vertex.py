class Vertex(object):
    """ Vertex class
        
        This class models a vertex on a graph. It is formed by a name, a weight and a object to contain.
        
        Attributes:
        -----------
        name  : str
            A name for the graph
        weight : float
            A number which indicates the weight of the vertex
        content : object
            An object
        updaters : dict
            A dictionary with all the stats an object to be updated in any change of the graph
    """
    kind = 'vertex'
    def __init__(self,name,weight=0,content=None,updaters=None):
        self.weight=weight
        self.name=name
        self.container=content
        self.updaters={}
        if updaters:
            self.__create_updaters__(updaters)
    
    def __create_updaters__(self,updaters):
        """ Create all the updaters of the vertex
        """
        for up in updaters:
            self.updaters[up]=0
    
    def add_updater(self,key):
        """ Add an updater
        """
        if key not in self.updaters.keys():
            self.updaters[key]=0
    
    def delete_updater(self,key):
        """ Delete an updater
        """
        if key in self.updaters.keys():
            del self.updaters[key]
    
    def get_weight(self):
        """ Return the weight of the vertex
        """
        return self.weight
    
    def set_weight(self,n_weight):
        """ Set the weight of the vertex
        """
        self.weight=n_weight
    
    def set_name(self,n_name):
        """ Set the name of the vertex
        """
        self.name=n_name
    
    def get_updaters(self):
        """ Return the updaters
        """
        return self.updaters
    
    def get_updater_val(self,key):
        """ Return the value of the updater
        """
        try:
            return self.updaters[key]
        except:
            print("Updater does not exist.")
    
    def get_name(self):
        """ Return the name of the vertex
        """
        return self.name
    
    def get_content(self):
        """ Return the container of the vertex
        """
        return self.content
    
    def set_contain(self, contain):
        """ Set the container of the vertex
        """
        self.contain=contain
    
    def update_val(self,key=None,val=None):
        """ Update the value of the updater
        """
        if key and self.updaters:
            self.updaters.update({key:val})
        else:
            self.updaters[key]=val

    def __repr__(self):
        return "Vertex (name='"+self.name+"',weight="+str(self.weight)+")"
