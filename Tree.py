from typing import List
from graph import Graph, Vertex
from graph_io import *
import time

# Use this method when you are sure that both graphs are trees but unsure wether they are isomorph
def areIsomorph(graph1: Graph, graph2: Graph):
    head1 = graph1.vertices[0]
    for head2 in graph2.vertices:
        if isomorph(head1, head2):
                return True, head1, head2
    return False, None, None


# Use this method when you are sure that both graphs are trees and for sure that if they are isomorph the given heads must be equal
# It is not recommended to use this method
def isomorph(head1: Vertex, head2: Vertex):
    # because we are dealing with heads we handle all neighbours as children
    return isIsomorph(head1, head1.neighbours, head2, head2.neighbours)


def isIsomorph(head1: Vertex, children1: List["Vertex"],
               head2: Vertex, children2: List["Vertex"]):
    # if the number of children for both comparing head are not equal then they cannot be isomorph
    if len(children1) != len(children2):
        return False
    # if the head have no children left then no more recursion is needed and it can be concluded that these subtrees are isomorph
    if len(children1) == 0:
        return True
    # whether the current subtrees are isomorph depends on their children
    return childrenAreIsomorph(head1, children1, head2, children2)


# Requires that children1 and children2 are of equal length and > 0
def childrenAreIsomorph(head1: Vertex, children1: List["Vertex"], head2: Vertex, children2: List["Vertex"]):
        # Because the heads can have an arbitrary amount of children we need to try every combination of children
        # If there exists a combination for which all the subtrees are isomorph than the current heads are isomorph
        a = children1.pop(0)
        for b in children2:
            if isIsomorph(a, extractChildren(head1, a), b, extractChildren(head2, b)):
                copyc2 = children2.copy()
                copyc2.remove(b)
                if len(children1) == 0 or childrenAreIsomorph(head1, children1, head2, copyc2):
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

iso, head1, head2 = areIsomorph(first, second)
print("The trees were %s with the heads %s and %s" % (iso, head1, head2))

with open('outputfirst.dot', 'w') as f:
    write_dot(first, f)

with open('outputsecond.dot', 'w') as f:
    write_dot(second, f)

