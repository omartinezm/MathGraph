from vertex import Vertex

class Neuron(Vertex):
    def __init__(self,name,updaters=None,bias=0):
        self.name=name
        self.weight=0
        self.bias=bias
        self.updaters={}
        if updaters:
            self.__create_updaters__(updaters)
    def __create_updaters__(self,updaters):
        for up in updaters:
            self.updaters[up]=0
    def get_bias(self):
        return self.bias