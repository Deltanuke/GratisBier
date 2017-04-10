from typing import List
from graph import Graph, Vertex
from graph_io import *
import time


def root(G: Graph):
    r = G.vertices[0]
    length, vertices_path = r.farthest()
    v1 = vertices_path[0]
    length, vertices_path = v1.farthest()
    if length % 2 == 1:
        return vertices_path[length // 2], vertices_path[length // 2 + 1]
    else:
        return vertices_path[length // 2], None


def assign_canonical_names(v: Vertex, super: Vertex = None):
    children = v.neighbours.copy()
    if super is not None:
        children.remove(super)
    if len(children) <= 0:
        #print("Leaf: %s. Ch'10', '10']ildren: %s. #children: %s" % (v, children, len(children)))
        v.canonical_name = "10"
    else:
        for u in children:
            assign_canonical_names(u, v)
        children_names = []
        for u in children:
            children_names.append(u.canonical_name)
        children_names = sorted(children_names)
        #print("Children names: %s" % children_names)
        temp = "1"
        for i in range(0, len(children_names)):
            temp += children_names[i]
        temp += "0"
        #print("The newly assigned name is %s" % temp)
        v.canonical_name = temp


def ahu_tree_isomorhpism(G1: Graph, G2: Graph):
    r11, r12 = root(G1)
    r21, r22 = root(G2)

    #print("The roots are %s and %s for graph 1" % (r11, r12))
    #print("The roots are %s and %s for graph 1" % (r21, r22))

    if r12 is None and r22 is None:
        return ahu_root_isomorphism(r11, r21)
    if r12 is not None and r22 is not None:
        return ahu_root_isomorphism(r12, r21) or ahu_root_isomorphism(r12, r22)
    else:
        return False


def ahu_root_isomorphism(r1: Vertex, r2: Vertex):
    assign_canonical_names(r1)
    assign_canonical_names(r2)
    if r1.canonical_name == r2.canonical_name:
        return True
    else:
        return False

with open('input/bigtrees1.grl') as _file:
    gr,o = read_graph_list(Graph, _file)

first = gr[0]
second = gr[1]

# start = time.time()
# for i in range(0, 1000):
#     is_iso = ahu_tree_isomorhpism(first, second)
# diff = time.time() - start
#
# print(": %s. %s" % (diff, is_iso))


#isomorph = ahu_tree_isomorhpism(first, second)
#print(isomorph)

with open('outputfirst.dot', 'w') as f:
    write_dot(first, f)

with open('outputsecond.dot', 'w') as f:
    write_dot(second, f)

