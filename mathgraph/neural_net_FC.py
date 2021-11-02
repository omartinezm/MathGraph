from tqdm import tqdm,tqdm_gui
from random import random
from .graph import Graph
from .edge import Edge
from .neuron import Neuron

class NeuralNetFC(Graph):
    
    kind = "NeuralNetFC"
    def __init__(self,name=None,npl=[2,2],updaters={},random=True):
        super().__init__(vertex=[],edges=[],name=name,isdirected=False,autoupdate=False,
                updaters=updaters,propagation=True)
       
        self.nlayers=len(npl)
        self.npl=npl
        self.vertex={}
        self.random=random
        self.edges=self.__make_edges__(self.nlayers,npl)
        self.add_edge(self.edges)
        
    def __make_edges__(self,nlayers,npl):
        """ Make and add the edges of the network
        
            This is a fully connected network.
            
            Parameters:
            ===========
            nlayers : int
                Number of layers of the network
            npl : list
                List with the number of neurons per layer       
        """
        edges=[]
        layers=[self.__make_layer__(npl[i],i) for i in range(nlayers)]
        for n in tqdm(range(nlayers-1), desc="Connecting network"):
            for i in range(npl[n]):
                for j in range(npl[n+1]):
                    edges.append(Edge(layers[n][i],layers[n+1][j],cost=random() if self.random else -1))
        return edges
    def __make_layer__(self,nneurons,iden):
        """ Creates the neurons of the layer and add it to the list of neurons
        
            By default the neurons are named as "l(iden)_v(number)" where iden is a identifier of
            the layer and number is the number of the neuron. By default, 'iden' and 'number' are
            numbered from zero.
            
            Parameters:
            ===========
            nneurons : int
                number of neurons of the layer
            iden : str
                a string that identifies the neuron.        
        """
        layer=[]
        for i in tqdm(range(nneurons),desc="Layer "+str(iden)):
            tv=Neuron(name="L"+str(iden)+"_v"+str(i),bias=0)
            layer.append(tv)
            self.vertex[tv.get_name()]=tv
            self.__in_degrees__[tv.get_name()]=0
            self.__out_degrees__[tv.get_name()]=0
        return layer
    
    def update_neuron(self,name,key,value):
        """ Update the value of the neuron on a given key
        
            Parameters:
            ===========
            name : str
                name of the neuron to change the value
            key : str
                name of the uptader to change
            value : float
                new value of the neuron at the updater
        """
        for k in key:
            self.find_vertex_by_name(name).update_val(k,value)
        
    def propagate(self,sLayer=0,edge=None,back=False,key=None):
        """ Propagates the values back or forward
        
            Parameters:
            ===========
            layer : int, optional
                A starting layer to propagate
            edge : Edge, optional
                An edge to go on propagation
            back : boolean, optional
                True if you want to go backward, False if you want to go forward
            sLayer : int, optional (not implemented)
                Indicates the layer from which you want to propagate back or forward
        """
        assert -1<sLayer<self.nlayers , "Incorrect start layer"
        for i in range(self.npl[-1]):
            for k in key:
                self.vertex["L"+str(len(self.npl)-1)+"_v"+str(i)].update_val(k,0)
        s=sum(self.npl)
        if back:
            # We go from the last layer to the first layer
            for neu in tqdm(list(reversed(sorted(self.vertex))),desc="Prop. on "+str(self.nlayers)+" layers"):
                self.update([self.vertex[neu]],back=True,key=key)
        else:
            # From the first to last.
            for neu in tqdm(self.vertex,desc="Prop. on "+str(self.nlayers)+" layers"):
                self.update([self.vertex[neu]],key=key)
                if not ("L"+str(len(self.npl)-1) in neu):
                    for k in key:
                        self.vertex[neu].update_val(k,0)
    def train(self,train_batch=[],epoch=1):
        """ Train the neural network
        
        """
        return "TODO"
    def get_bias_values(self):
        """ Return the biases of the network
        
        """
        res=[self.vertex[neu].get_bias() for neu in self.vertex]
        return res
    def get_error(self,X=[],y=[],key=None):
        predicted=self.predict(X,key=key)
        print(predicted)
        res=[]
        for (pred,expec) in zip(predicted,y):
            rt=[]
            for (p1,e1) in zip(pred,expec):
                rt.append(p1-e1)
            res.append(rt)
        return res
    def predict(self,data=[],key=None):
        """ Show the prediction given a initial data
        
            Parameter:
            ==========
            data : list[list]
                A list containing lists of input data
            key : str, optiona
                The name of the key we want to train, if key is None we train all the keys
        """
        res=[]
        for vec in data:
            if len(vec)==self.npl[0]:
                for i in range(self.npl[0]):
                    self.update_neuron("L0_v"+str(i),key,vec[i])
                self.propagate(key=key)
                r1=[]
                for i in range(self.npl[-1]):
                    for k in key:
                        r1.append(self.vertex["L"+str(len(self.npl)-1)+"_v"+str(i)].get_updater_val(k))
                res.append(r1)
        return res
    def __repr__(self):
        return "NeuralNet_FC (\n   \033[1m config \033[0;0m="+str(self.npl)+"\n   \033[1m vertex \033[0;0m="+str(self.get_vertexes())+",\n   \033[1m edges \033[0;0m="+str(self.get_edges())+")"
   
    
