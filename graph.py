from vertex import Vertex
from edge import Edge
from draw_graph import DrawGraph
import warnings

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
            A list of functions by which the graph information is updated. The function must follow
            the followint format
                def f(graph,key,start_vertex,vertex,edge,back):
                    # Your code
            where
                graph : a Graph object
                key : the key of the updater
                start_vertex : a vertex, represent the vertes from which you start to propagate
                vertex : a vertex in which you are working
                edge : an edge
                back : a boolean representing if you are working back or forward.
    """
    kind = 'graph'
    def __init__(self,vertex=[],edges=[],name=None,isdirected=False,
                 autoupdate=False,updaters={},propagation=False):
        self.autoupdate=False # We first create the graph, then update it
        self.propagation=propagation
        self.isdirected=isdirected
        self.name=name
        self.__in_degrees__={}
        self.__out_degrees__={}

        self.vertex={}
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
                if self.find_vertex_by_name(ver.get_name()):
                    warnings.warn("Already exist a vertex with the name '"+str(ver.get_name())+"'")
                self.vertex[ver]=ver.get_name()
                self.__in_degrees__[ver]=0
                self.__out_degrees__[ver]=0
        # If you add a vertex, no correlated information between vertex is
        # added to the graph
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
                    self.add_vertex([edge.start])
                    self.__out_degrees__[edge.start]=1
                else:
                    # Start vertex exist, must increase the out_degree of start vertex
                    self.__out_degrees__.update({edge.start:self.__out_degrees__[edge.start]+1})
                if not (edge.end in self.vertex):
                    # End vertex does not exist, must add
                    self.add_vertex([edge.end])
                    self.__in_degrees__[edge.end]=1
                else:
                    # End vertex exist, must increase the in_degree of end vertex
                    self.__in_degrees__.update({edge.end:self.__in_degrees__[edge.end]+1})
                self.edges.append(edge)
        if self.autoupdate:
            # Update the graph stats if case
            for ed in edges:
                #self.update(vertex=[ed.start],propagate=False)
                self.update(vertex=[ed.end],propagate=False)
    def set_vertex_updater_val(self, vertex, key, val):
        vertex.update_val(key,val)
        if self.autoupdate:
            for ver in self.find_neighborhood_vertexes(vertex,ending=False):
                self.update([ver],propagate=self.propagation)

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
            del self.vertex[vertex]
            del self.__in_degrees__[vertex]
            del self.__out_degrees__[vertex]
        else:
            print("Vertex does not exist.")
    def delete_edge(self, edge):
        """ Deletes an edge
            
            The in_degree and out_degree is updated.
            
            Parameters:
            ===========
            edge : Edge
                The edge we want to delete.
        """
        #try:
        self.__in_degrees__.update({edge.end.name:self.__in_degrees__[edge.end.name]-1})
        self.__out_degrees__.update({edge.start.name:self.__out_degrees__[edge.start.name]-1})
        self.edges.remove(edge)
        #except:
        #print("Edge does not exist.")
            
    def get_name(self):
        """ Returns the name of the graph
        
        """
        return self.name
    def get_vertexes(self):
        """ Returns the vertexes of the graph
        
        """
        return list(self.vertex)
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
                A boolean that indicates if we want the edges ending in the vertex      
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
            vertex : str,
                The name of the vertex we are studying
            exiting : Boolean, optional
                A boolean that indicates if we want the edges starting form the vertex
            entering : Boolean, optional
                A boolean that indicates if we want the edges ending form the vertex   
        """
        #if not vertex in self.vertex.keys():
        ver=self.find_vertex_by_name(vertex)
        if not ver:
            return "Vertex does not exist"
        if not exiting and not entering:
            # Total degree
            return self.__out_degrees__[ver]-self.__in_degrees__[ver]
        elif not entering:
            # In degree
            return self.__in_degrees__[ver]
        else:
            # Out degree
            return self.__out_degrees__[ver]
        
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
        for edge in self.get_edges(vertex,starting=starting,ending=ending):
            if starting:
                res.append(edge.start)
            elif ending:
                res.append(edge.end)
        return res
    
    def find_vertex_by_name(self,name):
        """ Find the vertex on the graph given the str name of the vertex
        
            Parameters:
            ===========
            name : str,
                The vertex name
        """
        for key,val in self.vertex.items():
            if val==name:
                return key
        #return "Vertex does not exist"

    def update(self,vertex=[],edge=[],propagate=False,exclude=[],back=False,key=None):
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
            back : boolean, optional
                True if you want to propagate back
        """
        if key:
            keys=key
        else:
            keys=self.updaters
        for updater in keys:
            for ver in vertex:
                if ver not in exclude:
                    self.updaters[updater](self,updater,[ver],ver,edge,back)
                    # To evade loops and propagation on the start vertex
                    if propagate:
                        #print("acá")
                        exclude=[ver]
                        self.__propagate__(updater,[ver],ver,edge,exclude,back)
    def __propagate__(self,updater,start_vertex,vertex=None,edge=None,exclude=[],back=False):
        """ Progragates the updater by all those vertex connected to the given one
        
            Parameters:
            ===========
            updater :  key
                The function of the updater
            start_vertex : Vertex
                The first vertex propagated
            vertex : Vertex
                The vertex we want to propagate
            edge : Edge
                The edge we want to propagate
            exclude : list, optional
                A list of vertex to be excluded
            back : boolean, optional
                True if you want to propagate back
        """
        for ver in self.find_neighborhood_vertexes(vertex,ending=False):
            if ver not in exclude:
                self.updaters[updater](self,updater,start_vertex,ver,edge=None,back=back)
                exclude.append(ver)
                self.__propagate__(updater,start_vertex,ver,exclude=exclude,back=back)    
    def update_all(self,vertex=None):
        """ Update all the graph        
        """
        if self.propagation:
            if vertex:
                self.update([vertex])
            else:
                print("Your graph have propagation, you need to specify the start vertex")
        for up in self.updaters:
            for ver in self.vertex:
                if ver.get_updaters():
                    self.updaters[up](self,up,None,ver,None,False)
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
        #print(self.vertex.values())
        for ver in self.vertex:
            if ver.get_updaters():
                if key in ver.get_updaters():
                    res[ver]=ver.get_updaters()[key]
                else:
                    res[ver]=None
            else:
                res[ver]=None
        return res
    def add_key_updater(self,key,vertex=None):
        """ Add a kee updater to a vertex or all the vertex. This just add the
            indicator of the updater, not the updater function.
        
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
    def add_func_updater(self, key, func):
        """ Add a function updater for a key
        
            Parameters:
            ===========
            key : string
                Name of the updater
            func : function
                Function linked to the key. The function must follow the followint format
                    def f(graph,key,start_vertex,vertex,edge,back):
                        # Your code
                where
                    graph : a Graph object you are working at.
                    key : the key of the updater
                    start_vertex : a vertex, represent the vertes from which you start to propagate
                    vertex : a vertex in which you are working
                    edge : an edge
                    back : a boolean representing if you are working back or forward.
                Your function must satisfy your implementation, all this is your responsability.
                Also, must take care of loops, thats the objective of knowing the starting vertex.
                An example:
                
                def p_back(graph,key,start_vertex,vertex=None,edge=None,back=False):
                    if back:
                        for v in graph.get_edges(vertex,starting=False):
                            v.start.update_val(key,v.start.get_updater_val(key)+v.get_cost()*vertex.get_updater_val(key))
                    else:
                        for v in graph.get_edges(vertex,ending=False):
                            v.end.update_val(key,v.end.get_updater_val(key)+v.get_cost()*vertex.get_updater_val(key))
                
                The function p_back is the back and forward propagation on a neuronal net.
        """
        self.updaters[key]=func
    def draw(self,*arg,**kwargs):
        """ Draw a graph using the DrawGraph class
            
        """
        dg=DrawGraph(self,*arg,**kwargs)
        dg.run()
        
    def __repr__(self):
        return "Graph (\n vertex="+str(self.get_vertexes())+",\n edges="+str(self.get_edges())+")"
