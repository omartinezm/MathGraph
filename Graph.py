import Vertex, Edge
class Graph:
    """ Graph class
    
        This class models a graph. It is formed by a list of vertext and a loist of edges, a name
        and a boolean which indicates if it's directed or not
        
        Attributes:
        -----------
        vertex: list
            A list of Vertexes.
        edges : list
            A list of Edges.
        name  : str, optional
            A name for the graph
        isdirected: boolean, optional
            A boolean which indicates if the graph is directed or not
        autoupdate: boolean, optional
            A boolean which indicates fi the stats of each element of the graph must be updates
            everytime a new element is included.
        updaters: dict, optional
            A list of functions by which the graph information is updated
    """
    kind = 'graph'
    def __init__(self,vertex,edges,name=None,isdirected=False,
                 autoupdate=False,updaters={},propagation=False):
        self.autoupdate=False # We first create the graph, then update it
        self.propagation=propagation
        self.isdirected=isdirected
        self.name=name
        self.__in_degrees__={}
        self.__out_degrees__={}
        self.vertex=[]
        self.add_vertex(vertex)
        self.edges=[]
        self.add_edge(edges)
        self.autoupdate=autoupdate
        self.updaters=updaters
        if autoupdate:
            self.update_all()
    def add_vertex(self,vertex):
        """ Add vertexes to the graph and update the graph stats, if any.
            
            Parameters:
            ===========
            vertex: list
                A list of vertexes to add        
        """
        for ver in vertex:
            if not (ver in self.vertex):
                # Vertex does not exist, must add
                self.vertex.append(ver)
                self.__in_degrees__[ver]=0
                self.__out_degrees__[ver]=0
        # If you add a vertex, no correlated information between vertex is
        # added to the graph
        #if self.autoupdate:
        #    for ver in self.find_neighborhood_vertexes(vertex):
        #        self.update(vertex=ver)
    def add_edge(self,edges):
        """ Add an edge to the graph and update the graph stats, if any.
        
            If the vertex does not exist in the graph, it is added
            
            Parameters:
            ===========
            edges: list
                A list of edges to add        
        """
        for edge in edges:
            exist=False
            for ed in self.get_edges(edge.start):
                if ed.start==edge.start and ed.end==edge.end:
                    # The edge already exist!
                    exist=True
                    break
            if(not exist):
                if not (edge.start in self.vertex):
                    # Start vertex does not exist, must add
                    self.vertex.append(edge.start)
                    self.__in_degrees__[edge.start]=0
                    self.__out_degrees__[edge.start]=1
                else:
                    # End vertex exist, must increase the out_degree of start vertex
                    self.__out_degrees__.update({edge.start:self.__out_degrees__[edge.start]+1})
                if not (edge.end in self.vertex):
                    # End vertex does not exist, must add
                    self.vertex.append(edge.end)
                    self.__in_degrees__[edge.end]=1
                    self.__out_degrees__[edge.end]=0
                else:
                    # End vertex exist, must increase the in_degree of end vertex
                    self.__in_degrees__.update({edge.end:self.__in_degrees__[edge.end]+1})
                #self.__degrees__.update({edge.start:self.__degrees__[edge.start]+1})
                #self.__degrees__.update({edge.end:self.__degrees__[edge.end]+1})
                #WORDS_INDEX.update({word:WORDS_INDEX[word]+ 1})
                self.edges.append(edge)
        if self.autoupdate:
            for ed in edges:
                self.update(vertex=[ed.start],propagate=False)
                self.update(vertex=[ed.end],propagate=False)
            # Update the graph stats if case
    def delete_vertex(self, vertex):
        """ Delete a vertex of the graph
        
            This function deletes the vertex of the graph, and also the edges connected
            to the vertex.
            
            Parameters:
            ===========
            vertex : Vertex
                A vertex to remove.
        """
        if vertex in self.vertex:
            for edge in self.get_edges(vertex):
                self.delete_edge(edge)
            self.vertex.remove(vertex)
        else:
            print("Vertex does not exist.")
    def delete_edge(self, edge):
        try:
            self.edges.remove(edge)
            self.__in_degrees__.update({edge.end:self.__in_degrees__[edge.end]-1})
            self.__out_degrees__.update({edge.start:self.__out_degrees__[edge.start]-1})
        except:
            print("Edge does not exist.")
            
    def get_name(self):
        """ Returns the name of the graph
        
        """
        return self.name
    def get_vertexes(self):
        """ Returns the vertexes of the graph
        
        """
        return self.vertex
    def get_edges(self,ver=None,starting=True, ending=True):
        """ Returns the edges of the graph.
        
            This method returns all the edges of the graph, or also the edged connected to
            a given vertex. Also can restrict the edges to the out edges of in edges of the
            given vertex.
            
            Parameters:
            ===========
            ver : Vertex, optional
                A vertex we want the edges connected to.
            starting : Boolean, optional
                A boolean that indicates if we want the edges starting form the vertex
            ending : Boolean, optional
                A boolean that indicates if we want the edges ending form the vertex        
        """
        if not ver:
            return self.edges
        else:
            res=[]
            for edge in self.edges:
                if edge.start == ver and starting:
                    res.append(edge)
                elif edge.end == ver and ending:
                    res.append(edge)
            return res
    def get_degree(self,vertex,exiting=False,entering=False):
        """ Find the degree of the vertex
            
            Given the vertex it calculates the in-degree, out-degree and the total
            degree
            
            Parameters:
            ===========
            vertex : Vertex,
                The vertex we are studying
            exiting : Boolean, optional
                A boolean that indicates if we want the edges starting form the vertex
            entering : Boolean, optional
                A boolean that indicates if we want the edges ending form the vertex   
        """
        #ext=len(self.find_neighborhood_vertexes(vertex,exiting=True))
        #ent=len(self.find_neighborhood_vertexes(vertex,entering=True))
        if not vertex in self.vertex:
            return "Vertex does not exist"
        if not exiting and not entering:
            # Total degree
            return self.__out_degrees__[vertex]-self.__in_degrees__[vertex]
        elif not entering:
            # In degree
            return self.__in_degrees__[vertex]
        else:
            # Out degree
            return self.__out_degrees__[vertex]
        
    def find_neighborhood_vertexes(self,vertex,starting=True,ending=True):
        """ Function that find all the neighborhood vertexes
        
            Given a vertex if returns all those vertexes which are connected to this
            by an edge. It can be exiting o entering from the vertex.
            
            Parameters:
            ===========
            vertex : Vertex,
                The vertex we are studying
            exiting : Boolean, optional
                A boolean that indicates if we want the edges starting form the vertex
            entering : Boolean, optional
                A boolean that indicates if we want the edges ending form the vertex        
        """
        res=[]
        for edge in self.get_edges(vertex,starting=starting,ending=ending):#,ending=entering):
            if not starting:
                res.append(edge.start)
            elif not ending:
                res.append(edge.end)
        #for edge in self.get_edges(vertex):
        #    res.append(edge.end)
        return res
    
    def find_vertex_by_name(self,name):
        """ Find the vertex on the graph given the str name of the vertex
        
            Parameters:
            ===========
            name : str,
                The vertex name
        """
        for ver in self.vertex:
            if ver.get_name()==name:
                return ver
        # If there, vertex does not exist
        return None
    
    def update(self,vertex=[],edge=[],propagate=False,exclude=[]):
        """ Update funcion of the graph
        
            In some implementations it is needed to update the stats and data of
            the graph in real time. This function does this each time a change is introduced
            to the graph
            
            Parameters:
            ===========
            vertex : list, optional
                A list of vertexes to propagate
            edge : list, optional
                A list of edges to propagate
            propagate : boolean, optional
                An indicator of propagation
            exclude : list, optional
                A list of vertexes to omit
        """
        for updater in self.updaters:
            #ex=exclude
            for ver in vertex:
                if ver not in exclude:
                    updater(self,self.updaters[updater],[ver],ver,edge)
                    if propagate or self.propagation:
                        self.__propagate__(updater,[ver],ver,edge,exclude)
            """
            if vertex not in exclude:
                updater(self,self.updaters[updater],[vertex],vertex,edge,exclude)
                if propagate:
                    self.__propagate__(updater,[vertex],vertex,edge,exclude=[])
            """
    def __propagate__(self,updater,start_vertex,vertex=None,edge=None,exclude=[]):
        """ Progragates the updater by all those vertex connected to the given one
        
            Parameters:
            ===========
            updater :  function
                The function of the updater
            start_vertex : Vertex
                The first vertex propagated
            vertex : Vertex
                The vertex we want to propagate
            edge : Edge
                The edge we want to propagate
            exclude : list, optional
                A list of vertex to be excluded
        """
        for ver in self.find_neighborhood_vertexes(vertex,ending=False):
            if ver not in exclude:
                updater(self,self.updaters[updater],start_vertex,ver,edge=None)
                exclude.append(ver)
                self.__propagate__(updater,ver,start_vertex,exclude=exclude)
    def update_all(self,vertex=None):
        """ Update all the graph        
        """
        if self.propagation:
            if vertex:
                self.update([vertex])
            else:
                print("Your graph have propagation, you need to specify the start vertex")
        for up in self.updaters:
            for (ver,edge) in zip(self.vertex,self.edges):
                if ver.get_updaters():
                    up(self,self.updaters[up],ver,None,True)
    def get_updaters_values(self,key=None):
        """ Returns a dictionary with the value of the updater for each vertex
        
            Parameter:
            ==========
            key : string
                The name of the updater
        """
        if not key:
            return "An updater key is needed!"
        
        res={}        
        for ver in self.vertex:
            if ver.get_updaters():
                if key in ver.get_updaters():
                    res[ver]=ver.get_updaters()[key]
                else:
                    res[ver]=None
            else:
                res[ver]=None
        return res
    def add_updater(self,key,vertex=None):
        """ Add an updater to a vertex or all the vertex
        
            Parameters:
            ===========
            key : string
                Name of the updater
            vertex : Vertex
                Vertex in the graph to add an updater. If vertex is None
                then it is added to all the vertex of the graph
        """
        if vertex:
            if vertex in self.get_vertexes():
                vertex.add_updater(key)
            else:
                print("Vertex does not exist")
        else:
            for ver in self.vertex:
                ver.add_updater(key)
    def __repr__(self):
        return "Graph (\n vertex="+str(self.get_vertexes())+",\n edges="+str(self.get_edges())+")"