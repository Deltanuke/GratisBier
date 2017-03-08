from graph.graph import *
from graph.graph_io import *
#, save_graph, write_dot


def coloring(G):
    for v in G.vertices:
        v.color = G.apply_color()
    prev_coloring = G.get_coloring()

    i = 0

    while True:
        refine(G)
        new_coloring = G.get_coloring()
        if identical_coloring(prev_coloring, new_coloring):
            break
        prev_coloring = new_coloring

        i += 1
        output_process(G, i)
        if i > 10:
            return G
    return G


def refine(G: Graph):
    prev_coloring = G.get_coloring()
    print(prev_coloring)
    i = 0
    while i < len(G.vertices):
        v = G.vertices[i]
        G.advance_color()
        j = i + 1
        while j < len(G.vertices):
            u = G.vertices[j]
            if prev_coloring[v] == prev_coloring[u]:
                if identical_neighbours(v.get_neighbour_colors(), u.get_neighbour_colors()):
                    v.color = G.apply_color()
                    u.color = G.apply_color()
                    print("applied color %s to %s and %s" % (G.apply_color(), v, u))
            j += 1
        i += 1


def identical_neighbours(first: list, second: list):
    if len(first) != len(second):
        return False
    for c in first:
        if c in second:
            second.remove(c)
        else:
            return False
    if len(second) > 0:
        return False
    return True


def identical_coloring(prev: dict, new: dict) -> bool:
    if len(prev.keys()) != len(new.keys()):
        return False
    for k in prev.keys():
        if new.get(k) != prev.get(k):
            return False
    return True


def color_to_label(g: Graph):
    for v in g.vertices:
        v.label = v.color


def output_process(g: Graph, i: int):
    color_to_label(g)
    with open('output/output_%s.dot' % i, 'w') as f:
        write_dot(g, f)


with open('colorref_smallexample_4_7.grl') as f:
    G = load_graph(f)

colored_graph = coloring(G)
color_to_label(colored_graph)
