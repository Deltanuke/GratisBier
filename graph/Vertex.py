from typing import List
from . import *


class Vertex(object):
    """
    `Vertex` objects have a property `graph` pointing to the graph they are part of,
    and an attribute `label` which can be anything: it is not used for any methods,
    except for `__str__`.
    """

    def __init__(self, graph: "Graph", label=None):
        """
        Creates a vertex, part of `graph`, with optional label `label`.
        (Labels of different vertices may be chosen the same; this does
        not influence correctness of the methods, but will make the string
        representation of the graph ambiguous.)
        :param graph: The graph that this `Vertex` is a part of
        :param label: Optional parameter to specify a label for the
        """
        if label is None:
            label = graph._next_label()
        self.colornum = 0
        self._color_next = 0
        self._color = 0
        self._graph = graph
        self.label = label
        self._incidence = {}

    def __repr__(self):
        """
        A programmer-friendly representation of the vertex.
        :return: The string to approximate the constructor arguments of the `Vertex'
        """
        return 'Vertex(label={}, #incident={} ,color={})'.format(self.label, len(self._incidence), self._color)

    def __str__(self) -> str:
        """
        A user-friendly representation of the vertex, that is, its label.
        :return: The string representation of the label.
        """
        return str(self.__repr__())

    def is_adjacent(self, other: "Vertex") -> bool:
        """
        Returns True iff `self` is adjacent to `other` vertex.
        :param other: The other vertex
        """
        return other in self._incidence

    def _add_incidence(self, edge: "Edge"):
        """
        For internal use only; adds an edge to the incidence map
        :param edge: The edge that is used to add the incidence
        """
        other = edge.other_end(self)

        if other not in self._incidence:
            self._incidence[other] = set()

        self._incidence[other].add(edge)

    @property
    def graph(self) -> "Graph":
        """
        The graph of this vertex
        :return: The graph of this vertex
        """
        return self._graph

    @property
    def incidence(self) -> List["Edge"]:
        """
        Returns the list of edges incident with the vertex.
        :return: The list of edges incident with the vertex
        """
        result = set()

        for edge_set in self._incidence.values():
            result |= edge_set

        return list(result)

    @property
    def neighbours(self) -> List["Vertex"]:
        """
        Returns the list of neighbors of the vertex.
        """
        return list(self._incidence.keys())

    @property
    def color(self) -> int:
        return self._color

    @color.setter
    def color(self, color):
        self.colornum = color
        self._color = color

    @property
    def color_next(self) -> int:
        return self._color_next

    @color_next.setter
    def color_next(self, color_next):
        self._color_next = color_next

    @property
    def degree(self) -> int:
        """
        Returns the degree of the vertex
        """
        return sum(map(len, self._incidence.values()))

    def update(self):
        self._color = self._color_next

    def same_vertices(self, other: "Vertex"):
        oNeighbours = other.neighbours
        for n in self.neighbours:
            for oN in oNeighbours:
                if n.color == oN.color:
                    oNeighbours.remove(oN)
                    break
            else:
                return False
        return len(oNeighbours) == 0

    def farthest(self, sender: "Vertex" = None):
        length = 0
        vertices_path = []
        for v in self.neighbours:
            if v != sender:
                length_temp, vertices_temp = v.farthest(self)
                if length_temp + 1 > length:
                    length = length_temp + 1
                    vertices_path = vertices_temp
        vertices_path.append(self)
        return length, vertices_path

    def children(self, head=None):
        n = self.neighbours.copy()
        if head is not None:
            n.remove(head)
        return n
