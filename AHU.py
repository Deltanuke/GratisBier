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
        v.canonical_name = "10"
    else:
        for u in children:
            assign_canonical_names(u, v)
        children_names = []
        for u in children:
            children_names.append(u.canonical_name)
        children_names = sorted(children_names)
        temp = "1"
        for i in range(0, len(children_names)):
            temp += children_names[i]
        temp += "0"
        v.canonical_name = temp


def ahu_tree_isomorhpism(G1: Graph, G2: Graph):
    r11, r12 = root(G1)
    r21, r22 = root(G2)

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


def ahu_tree_authomorphisms(G: Graph):
    r11, r12 = root(G)
    assign_canonical_names(r11)
    return recursive_auth_calc(r11, r11.children())


def recursive_auth_calc(v: Vertex, children: List["Vertex"]):
    result = 1
    if len(children) < 1:
        return 1
    for c in children:
        result = result * recursive_auth_calc(c, c.children(v))
    return result * calculate_no_auth(children)


def calculate_no_auth(children: List["Vertex"]):
    count = 1
    groups = []
    for c1 in children:
        if already_in_group(c1, groups):
            continue
        group = equal_subtrees(c1, children)
        if len(group) > 1:
            groups.append(group)
    for group in groups:
        count = count * fact(len(group))
    return count


def fact(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * fact(n - 1)


def already_in_group(v: Vertex, groups):
    for group in groups:
        if v in group:
            return True
    return False


def equal_subtrees(v: Vertex, others: List["Vertex"]):
    equals = [v]
    for sibling in others:
        if v != sibling and v.canonical_name == sibling.canonical_name:
            equals.append(sibling)
    return equals


with open('input/Competition/c1/comp1.gr') as _file:
    gr,o = read_graph_list(Graph, _file)

number_of_graphs = len(gr)

isos = []

for x in range(number_of_graphs):
    if gr[x].is_tree():
        print("%s is a tree" % x)
        print("Number of aut: %s" % ahu_tree_authomorphisms(gr[x]))
    else:
        print("%s is no tree" % x)