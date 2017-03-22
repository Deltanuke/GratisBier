from typing import List
from graph import Graph, Vertex
from graph_io import *


def areIsomorph(graph1: Graph, graph2: Graph):
    head1 = graph1.vertices[0]
    for head2 in graph2.vertices:
        if isomorph(head1, head2):
                return True, head1, head2
    return False, None, None


def isomorph(head1: Vertex, head2: Vertex):
    return isIsomorph(head1, head1.neighbours, head2, head2.neighbours)


def isIsomorph(head1: Vertex, children1: List["Vertex"],
               head2: Vertex, children2: List["Vertex"]):
    if len(children1) != len(children2):
        return False
    if len(children1) == 0:
        return True
    return childrenAreIsomorph(head1, children1, head2, children2)


# Requires that children1 and children2 are of equal length and > 0
def childrenAreIsomorph(head1: Vertex, children1: List["Vertex"], head2: Vertex, children2: List["Vertex"]):
        a = children1.pop(0)
        for b in children2:
            children2.remove(b)
            if isIsomorph(a, extractChildren(head1, a), b, extractChildren(head2, b)):
                return True
        return False


def extractChildren(head: Vertex, v: Vertex):
    n = v.neighbours.copy()
    n.remove(head)
    return n


with open('input/bigtrees1.grl') as _file:
    gr,o = read_graph_list(Graph, _file)

first = gr[0]
second = gr[1]

iso, head1, head2 = areIsomorph(first, first)
print("The trees were %s with the heads %s and %s" % (iso, head1, head2))

with open('outputfirst.dot', 'w') as f:
    write_dot(first, f)

with open('outputsecond.dot', 'w') as f:
    write_dot(second, f)

