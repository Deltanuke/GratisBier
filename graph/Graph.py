"""
This is a module for working with directed and undirected multigraphs.
"""
# version: 29-01-2015, Paul Bonsma
# version: 01-02-2017, Pieter Bos, Tariq Bontekoe

from typing import List, Union, Set
from . import Edge, GraphError, Vertex


class Graph(object):
    def __init__(self, directed: bool, n: int=0, simple: bool=False):
        """
        Creates a graph.
        :param directed: Whether the graph should behave as a directed graph.
        :param simple: Whether the graph should be a simple graph, that is, not have multi-edges or loops.
        :param n: Optional, the number of vertices the graph should create immediately
        """
        self._id = 0
        self._v = list()
        self._e = list()
        self._simple = simple
        self._directed = directed
        self._next_label_value = 0

        for i in range(n):
            self.add_vertex(Vertex(self))

    def __repr__(self):
        """
        A programmer-friendly representation of the Graph.
        :return: The string to approximate the constructor arguments of the `Graph'
        """
        return 'Graph(id={}, directed={}, simple={}, #edges={n_edges}, #vertices={n_vertices})'.format(
            self._id, self._directed, self._simple, n_edges=len(self._e), n_vertices=len(self._v))

    def __str__(self) -> str:
        """
        A user-friendly representation of this graph
        :return: A textual representation of the vertices and edges of this graph
        """
        return 'V=[' + ", ".join(map(str, self._v)) + ']\nE=[' + ", ".join(map(str, self._e)) + ']'

    def _next_label(self) -> int:
        """
        Generates unique labels for vertices within the graph
        :return: A unique label
        """
        result = self._next_label_value
        self._next_label_value += 1
        return result

    @property
    def simple(self) -> bool:
        """
        Whether the graph is a simple graph, that is, it does not have multi-edges or loops.
        :return: Whether the graph is simple
        """
        return self._simple

    @property
    def directed(self) -> bool:
        """
        Whether the graph behaves as a directed graph
        :return: Whether the graph is directed
        """
        return self._directed

    @property
    def vertices(self) -> List["Vertex"]:
        """
        :return: The `set` of vertices of the graph
        """
        return list(self._v)

    @property
    def edges(self) -> List["Edge"]:
        """
        :return: The `set` of edges of the graph
        """
        return list(self._e)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def __iter__(self):
        """
        :return: Returns an iterator for the vertices of the graph
        """
        return iter(self._v)

    def __len__(self) -> int:
        """
        :return: The number of vertices of the graph
        """
        return len(self._v)

    def add_vertex(self, vertex: "Vertex"):
        """
        Add a vertex to the graph.
        :param vertex: The vertex to be added.
        """
        if vertex.graph != self:
            raise GraphError("A vertex must belong to the graph it is added to")

        self._v.append(vertex)

    def add_edge(self, edge: "Edge"):
        """
        Add an edge to the graph. And if necessary also the vertices.
        Includes some checks in case the graph should stay simple.
        :param edge: The edge to be added
        """

        if self._simple:
            if edge.tail == edge.head:
                raise GraphError('No loops allowed in simple graphs')

            if self.is_adjacent(edge.tail, edge.head):
                raise GraphError('No multiedges allowed in simple graphs')

        if edge.tail not in self._v:
            self.add_vertex(edge.tail)
        if edge.head not in self._v:
            self.add_vertex(edge.head)

        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def __add__(self, other: "Graph") -> "Graph":
        """
        Make a disjoint union of two graphs.
        :param other: Graph to add to `self'.
        :return: New graph which is a disjoint union of `self' and `other'.
        """
        # TODO: implementation
        pass

    def __iadd__(self, other: Union[Edge, Vertex]) -> "Graph":
        """
        Add either an `Edge` or `Vertex` with the += syntax.
        :param other: The object to be added
        :return: The modified graph
        """
        if isinstance(other, Vertex):
            self.add_vertex(other)

        if isinstance(other, Edge):
            self.add_edge(other)

        return self

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        """
        Tries to find edges between two vertices.
        :param u: One vertex
        :param v: The other vertex
        :return: The set of edges incident with both `u` and `v`
        """
        result = u._incidence.get(v, set())

        if not self._directed:
            result |= v._incidence.get(u, set())

        return set(result)

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        """
        Returns True iff vertices `u` and `v` are adjacent. If the graph is directed, the direction of the edges is
        respected.
        :param u: One vertex
        :param v: The other vertex
        :return: Whether the vertices are adjacent
        """
        return v in u.neighbours and (not self.directed or any(e.head == v for e in u.incidence))

    def is_tree(self):
        first = self.vertices[0]
        frontier = [(first, first.neighbours.copy())]
        closed = [first]
        while len(frontier) > 0:
            newfrontier = []
            for t in frontier:
                for v in t[1]:
                    if len(v.neighbours) > 1:
                        children = v.children(t[0])
                        for c in children:
                            if c in closed:
                                return False
                        newfrontier.append((v, children))
                    closed.append(t[0])
            frontier = newfrontier
        return True
