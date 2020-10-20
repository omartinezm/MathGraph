from tqdm import tqdm,tqdm_gui

class NeuralNet_FC(Graph):
    def __init__(self,name=None,vertex=[],npl=[2,2],updaters={}):
        self.autoupdate=False # We first create the graph, then update it
        self.propagation=True
        self.isdirected=False
        self.name=name
        self.__in_degrees__={}
        self.__out_degrees__={}
        self.updaters=updaters
        
        self.nlayers=len(npl)
        self.npl=npl
        self.vertex=[]
        self.edges=[]
        self.add_edge(self.__make_edges__(self.nlayers,npl))
        
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
        for n in range(nlayers-1):
            for i in range(npl[n]):
                for j in range(npl[n+1]):
                    edges.append(Edge(layers[n][i],layers[n+1][j],cost=-1))
        return edges
    def __make_layer__(self,nneurons,iden):
        """ Creates the neuron and add it to the list of neurons
        
            The neurons are named as "c(iden)-v(number)" where iden is a identifier of the layer
            and number is the number of the neuron. By default, 'iden' and 'number' are numbered
            from zero.
            
            Parameters:
            ===========
            nneurons : int
                number of neurons of the layer
            iden : str
                a string that identifies the neuron.        
        """
        layer=[]
        for i in range(nneurons):
            tv=Vertex(name="c"+str(iden)+"-v"+str(i),weight=0)
            layer.append(tv)
            self.vertex.append(tv)
            self.__in_degrees__[tv]=0
            self.__out_degrees__[tv]=0
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
        self.find_vertex_by_name(name).update_val(key,value)
        
    def propagate(self,sLayer=0,edge=None,back=False):
        """ Propagates the values back or forward
        
            Parameters:
            ===========
            layer : int, optional
                A starting layer to propagate
            edge : Edge, optional
                An edge to go on propagation
            back : boolean, optional
                True if you want to go backward, False if you want to go forward
        """
        assert -1<sLayer<self.nlayers , "Incorrect start layer"
        s=sum(self.npl)
        if back:
            # We go from the last layer to the first layer
            for i in tqdm(range(s-sLayer),desc="Prop. on "+str(self.nlayers-sLayer)+" layers"):
                self.update([self.vertex[s-i-sLayer]],back=back)
        else:
            # From the first to last.
            for i in tqdm(range(s-sLayer),desc="Prop. on "+str(self.nlayers-sLayer)+" layers"):
                self.update([self.vertex[i+sLayer]])
    def train(self,train_batch=[],epoch=1):
        """ Train the neural network
        
        """
        return "TODO"
    def __repr__(self):
        return "NeuralNet_FC (\n   \033[1m config \033[0;0m="+str(self.npl)+"\n   \033[1m vertex \033[0;0m="+str(self.get_vertexes())+",\n   \033[1m edges \033[0;0m="+str(self.get_edges())+")"