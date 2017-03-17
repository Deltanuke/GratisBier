from graph import *
import time
from graph_io import *
import time

""""
the idea:
color all the vertices initially based on their number of neighbour, put them all in a list and put those lists in a
list which we can iterate.
every iteration a check is done, if the outer list contains only lists with size of 1 or smaller it cannot be
improved upon so stop iterating. if the changed flag has not been set by the previous iteration the new list is the
same as the old list so it will not be improved by any next iterations so stop iterating

in the iteration:
loop over every list as these lists contain a number of vertices which can possibly be split in multiple lists
because the vertices now have different neighbours.
put the first vertice in a new list, now check for every other vertice if it has the same neighbours as the first.
if so append it to the list, if not create a new list and check every next vertice on the new number of lists.
after this list has been split all vertices in the same list have the same neighbours. they also have update colors
however the other vertices cannot see this new color yet as this would influence the algorithm.
now all these new lists are put into the full list.
after we tried splitting all old lists update the color of the vertices, update the old list to be the new list and
create a new 'new list' and start the process over again
"""


def colorize_graph(gr: Graph):
    d = dict()
    index = 0

    # do the initial coloring based on indices
    for v in gr.vertices:
        v.color = v.degree
        v.color_next = v.degree
        print(d.keys())
        if v.color not in d.keys():
            d[v.color] = list()
        d[v.color].append(v)
        if v.degree > index:
            index = v.degree

    # prepare for loop
    q = list()
    # change dict to list to be iterated updon
    for vertices in d.values():
        q.append(vertices)

    # set the index correctly
    index += 1

    colorize(q, index)


def colorize_list(graphs : list):
    d = dict()
    index = 0

    # do the initial coloring based on indices
    for gr in graphs:
        for v in gr.vertices:
            v.color = v.degree
            v.color_next = v.degree
            if v.color not in d.keys():
                d[v.color] = list()
            d[v.color].append(v)
            if v.degree > index:
                index = v.degree

    # prepare for loop
    q = list()
    # change dict to list to be iterated updon
    for vertices in d.values():
        q.append(vertices)

    # set the index correctly
    index += 1

    q = colorize(q, index)
    check_iso(q, graphs)


def check_iso(list_of_list_verticecs : list, graph_list: list):
    main_graphs = dict()
    for graph1 in graph_list:
        main_graphs[graph1] = graph_list.copy()
        main_graphs[graph1].remove(graph1)
    for list_vertices in list_of_list_verticecs:
        graphs = dict()
        for graph1 in graph_list:
            graphs[graph1] = list()
        for vertex in list_vertices:
            graphs[vertex.graph].append(vertex)
        for k1 in graphs:
            l1 = graphs[k1]
            for k2 in graphs:
                l2 = graphs[k2]
                if len(l1) != len(l2):
                    try:
                        main_graphs[k1].remove(k2)
                    except ValueError:
                        pass
                    try:
                        main_graphs[k2].remove(k1)
                    except ValueError:
                        pass
    for graph in main_graphs.keys():
        sys.stdout.write("Graph: " + graph.__repr__() + " is iso with: ")
        sys.stdout.flush()
        for gr in main_graphs[graph]:
            sys.stdout.write(gr.__repr__() + ", ")
        sys.stdout.write("\n")
        sys.stdout.flush()


def colorize(main_list: "list", index: int):
    # start loop empty copy of the list and set changed back to False
    changed = True
    while changed:
        # empty copy of the list and set changed back to False
        copy_list = list()
        changed = False
        for listVert in main_list:
            # create empty list for possibly splitting the current list
            copy_to_split = list()
            if len(listVert) > 1:
                # more than 1 entry in this list, eligible for splitting
                for v in listVert:
                    if len(copy_to_split) > 0:
                        # if an entry has already been posted to qtt check if the current vertice has the same neighbour
                        appended = False
                        for f in copy_to_split:
                            # if the current vertice has the same neighbours as the first item in the current list
                            # append this vertice to the list
                            if f[0].same_vertices(v):
                                f.append(v)
                                v.color_next = f[0].color_next
                                appended = True
                                break
                        # the current vertice has not been appended to a list, it must have different neighbours than
                        # any previous vertices, create a new entry in qtt and set changed to True and set a new color
                        if not appended:
                            l = list()
                            v.color_next = index
                            index += 1
                            l.append(v)
                            copy_to_split.append(l)
                            changed = True
                    # there is not a single entry in qtt, create a new entry and append the current vertice
                    else:
                        l = list()
                        l.append(v)
                        copy_to_split.append(l)
            # the current list has the size of 1 so is unable to be split. keep it this way
            elif len(listVert) == 1:
                copy_list.append(listVert)
                continue
            # the current list we were trying to split isn't empty so copy all entries from qtt (current working list0
            # to the outer working list qt
            if len(listVert) != 0:
                for vertices in copy_to_split:
                    copy_list.append(vertices)
        # update every color in the list to prepare for the next iteration
        for vertices in copy_list:
            for v in vertices:
                v.update()
        # update the final list
        main_list = copy_list
    return main_list


def is_done(lists: "list"):
    return True


with open('input/colorref_smallexample_6_15.grl') as _file:
    g, o = read_graph_list(Graph, _file)
print(g)
i = 0
for graph in g:
    graph.id = i
    i += 1
timeStart = time.time()
colorize_list(g)
print(time.time() - timeStart)


