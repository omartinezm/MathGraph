from .vertex import Vertex

class Neuron(Vertex):
    def __init__(self,name,updaters=None,bias=0):
        super().__init__(name=name,weight=0,updaters=updaters)
        self.bias=bias
        if updaters:
            self.__create_updaters__(updaters)
    def __create_updaters__(self,updaters):
        for up in updaters:
            self.updaters[up]=0
    def get_bias(self):
        """ Return the bias of the neuron
        """
        return self.bias
    def __repr__(self):
        return "Neuron (name='"+self.name+"', bias="+str(self.bias)+")"
