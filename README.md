# Math Graph

An implementation of [graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) on python

## Description

This package provides the vertex, edge and graph structure in python. Also includes a drawer for graphs.

## Usage

Import the package as

```python
import mathgraph
```

Create some vertexes

```python
v1=Vertex(name="Big node",weight=4)
v2=Vertex(name="Medium node",weight=3)
v3=Vertex(name="Medium node",weight=2)
v4=Vertex(name="Small node",weight=1)
v5=Vertex(name="Little node",weight=0.5)
v6=Vertex(name="Tiny node",weight=0.25)
```

Now some edges connecting the vertexes

```python
e1=Edge(vstart=v1,vend=v2,cost=1)
e2=Edge(vstart=v1,vend=v3,cost=1.5)
e3=Edge(vstart=v2,vend=v4,cost=1)
e4=Edge(vstart=v3,vend=v5,cost=2)
e5=Edge(vstart=v5,vend=v6,cost=0)
```

And finally the graph. The graph accepts vertexes and edges, if you only put the edges it automatically add the vertexes to the graph:

```python
g1=Graph(edges=[e1,e2,e3,e4,e5,e6])
```

You can see the graph with the command (don't work on Mac (yet)):

```python
g1.draw()
```

## Features

1. The structure is intented for a wide use, so the `Vertex` and `Edge` class include `updaters`. This updaters are a dictionary of stats that can change following some rules given by the updater function on the `Graph` class. The updaters on the graph is a dictionary with functions that takes some arguments and refresh the data of the updaters dictionary on `Vertex`es and `Edge`s.

2. Some particular graphs were included, like `Tree` and `NeuralNetFC`. The `Tree` class, as it's name say, create a tree. You can also create a neural net. At this moments only accepts fully connected nn's.

3. The pack `mathgraph.algorithms` have some methods to apply over the structure `Graph`. Like Dijkstra and Greddy path search, and Kruskal minimum spanning tree. This paths can be visualized on the `.draw()` if you give it as arguments.

```python
from algorithms.search_algorithms import Dijkstra
source=v1
target=v6
dj=Dijkstra(g1,source=source,target=target)
g1.draw(path=dj.get_path())
```
4. A graph can be created from an incidence matrix using a `numpy` matrix. Moreover, you can construct the incidence and adjacency matrix once you have a graph with the functions `create_incidence_matrix()`, `create_adjacency_matrix()`. The order of appearence of the vertex (rows) on the incidence matrix is given by the listing order of the vertex, same case for the columns and edges.


### Requirements
`pyglet`, `numpy`.
