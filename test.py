from graph.graph import *
from graph.graph_io import *
#, save_graph, write_dot

with open('colorref_smallexample_4_7.grl') as f:
    G = load_graph(f)

def coloring(G):
    for v in G.vertices:
        v.color = 1
        maxcolor = 1
    i = 0
    for v in G.vertices:
        for u in G.vertices:
            if u != v and u.color == v.color:
                nu = len(u.neighbours)
                lu = u.neighbours
                nv = len(v.neighbours)
                if nu == nv:
                    for i in range(nv):
                        h = v.neighbours[i]
                        if h in lu:
                            lu.remove(h)
                        else:
                            u.color = maxcolor + 1
                            maxcolor = maxcolor + 1
                elif nu != nv:
                    u.color = maxcolor + 1
                    maxcolor = maxcolor + 1
    return G.vertices
print(coloring(G))