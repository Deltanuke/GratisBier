from typing import List, Set
from . import Graph


class UnsafeGraph(Graph):
    @property
    def vertices(self) -> List["Vertex"]:
        return self._v

    @property
    def edges(self) -> List["Edge"]:
        return self._e

    def add_vertex(self, vertex: "Vertex"):
        self._v.append(vertex)

    def add_edge(self, edge: "Edge"):
        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        left = u._incidence.get(v, None)
        right = None

        if not self._directed:
            right = v._incidence.get(u, None)

        if left is None and right is None:
            return set()

        if left is None:
            return right

        if right is None:
            return left

        return left | right

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        return v in u._incidence or (not self._directed and u in v._incidence)