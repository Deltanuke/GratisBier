from graph.graph import *
from graph.graph_io import *

def coloring(G):
    for v in G.vertices:
        v.color = 1
        maxcolor = 1
    for v in G.vertices:
        for u in G.vertices:
            if u != v and u.color == v.color:
                nu = u.neighbours
                nv = v.neighbours
                cnu = []
                cnv = []
                for i in nu:
                    cnu.append(i.color)
                for i in nv:
                    cnv.append(i.color)
                scnu = sorted(cnu)
                scnv = sorted(cnv)
                if scnu != scnv:
                    u.color = maxcolor + 1
        maxcolor = maxcolor + 1
    return G


def color_to_label(G):
    for v in G.vertices:
        v.label = v.color
    return G

with open('colorref_smallexample_4_7.grl') as f:
    G = load_graph(f)

print(coloring(G))
print(color_to_label(coloring(G)))


# colored_graph = coloring(G)
# color_to_label(colored_graph)

# with open('output.dot', 'w') as f:
#     write_dot(colored_graph, f)
