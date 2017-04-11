from typing import List
from graph import Graph, Vertex
from graph_io import *
import time
import AHU


class Counter():
    def __init__(self):
        self.i = 0

    def increment(self):
        self.i += 1

    def get(self):
        return self.i
comparisons = Counter()


# Use this method when you are sure that both graphs are trees but unsure wether they are isomorph
def areIsomorph(graph1: Graph, graph2: Graph):
    head11, head12 = AHU.root(graph1)
    head21, head22 = AHU.root(graph2)
    # print("Heads 1: %s, %s. Heads 2: %s, %s" % (head11, head12, head21, head22))
    if head12 is None and head22 is None:
        return isomorph(head11, head21)
    if head12 is not None and head22 is not None:
        return isomorph(head12, head21) or isomorph(head12, head22)
    else:
        return False


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
                if len(children1) == 0 or childrenAreIsomorph(head1, children1.copy(), head2, copyc2):
                    return True
        return False


def extractChildren(head: Vertex, v: Vertex):
    n = v.neighbours.copy()
    n.remove(head)
    return n


with open('input/bigtrees1.grl') as _file:
    gr,o = read_graph_list(Graph, _file)

start = time.time()
for i in range(100):
    for x in range(0, 3):
        for y in range(0, 3):
            iso = areIsomorph(gr[x], gr[y])
diff = (time.time() - start) / 1600

print("The trees were %s, solved in %s. #VERTICES = %s" % (iso, diff, len(gr[0].vertices)))
# print("# %s comparisons were made" % comparisons.get())

# with open('outputfirst.dot', 'w') as f:
#     write_dot(first, f)
#
# with open('outputsecond.dot', 'w') as f:
#     write_dot(second, f)

