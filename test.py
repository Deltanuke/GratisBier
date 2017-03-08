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


def output(g: Graph, name: str):
    color_to_label(g)
    with open(name, 'w') as f:
        write_dot(g, f)


def output_colorless(g: Graph, name: str):
    with open(name, 'w') as f:
        write_dot(g, f)


def color(g: Graph):
    changed = True
    i = 0
    while changed:
        i += 1
        # output_process(g, i)
        print("New iteration")

        g.apply_color();g.advance_color()
        changed = False
        copy_vertices = g.vertices.copy()

        neighbour_colors = get_all_neighbour_colors(g)
        print("The neighbour colors are ")
        print(neighbour_colors)

        while len(copy_vertices) > 0 and not changed:
            print(copy_vertices)
            v = copy_vertices.pop(0)
            color_class = g.get_color_class(v.color)
            updated_color = False

            j = 0
            while j < len(copy_vertices):
                u = copy_vertices[j]
                if v.color == u.color and identical_neighbours(neighbour_colors[v], neighbour_colors[u]):
                    print("Vertex %s was equal to vertex %s, with respective colors %s and %s, neighbour colors %s and %s"% (v, u, v.color, u.color, neighbour_colors[v], neighbour_colors[u]))
                    u.color = g.apply_color()
                    copy_vertices.pop(j)
                    updated_color = True
                else:
                    j += 1
                    print("Vertex %s was not equal to vertex %s, with respective colors %s and %s, neighbour colors %s and %s"% (v, u, v.color, u.color, neighbour_colors[v], neighbour_colors[u]))
            if updated_color:
                v.color = g.apply_color()
                print("Created a new color %s, with %s vertices" % (g.apply_color(), len(g.get_color_class(g.apply_color()))))
                g.advance_color()
            if len(color_class) != len(set(color_class) & set(g.get_color_class(v.color))):
                changed = True


def get_all_neighbour_colors(g: Graph):
    res = {}
    for v in g.vertices:
        res[v] = v.get_neighbour_colors()
    return res

with open('colorref_smallexample_2_49.grl') as f:
    G = load_graph(f)

color(G)
output(G, "output/result.dot")