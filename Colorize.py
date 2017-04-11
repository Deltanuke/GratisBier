from graph_io import *

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


mode = 2  # 0 = count automorphisms between graphs, 1 = count automorphisms in a singel graph, 2 = detect isomorphism
input_file = "input/basic/basicGI1.grl"


def colorize_graph(gr: Graph):
    d = dict()
    index = 0

    # do the initial coloring based on indices
    for v in gr.vertices:
        v.color = v.degree
        v.color_next = v.degree
        #print(d.keys())
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


def colorize_list(graphs : list, auto: bool = False, single: bool = False):
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
    index = 0
    for vertices in d.values():
        for vertex in vertices:
            vertex.color = index
            vertex.color_next = index
        q.append(vertices)
        index += 1

    # set the index correctly
    index += 1

    q, index = colorize(q, index)
    main_iso = is_iso(q, graphs)
    filtered_isos = main_iso
    if len(filtered_isos) > 0:
        tuples = create_tuples_from_isos(filtered_isos)
        if single:
            tuples = list()
            for i in range(int(len(graphs) / 2)):
                tuples.append([graphs[i], graphs[(i + int(len(graphs)/2))]])
        for list_vertices in q:
            for vertex in list_vertices:
                if vertex.color >= index:
                    index = vertex.color + 1
        triples = list()
        for graph1, graph2 in tuples:
            # print("Testing graph " + str(graph1.id) + " against graph " + str(graph2.id))
            plist = purify_list(q, graph1, graph2)
            count = count_isomorphisms(plist, graph1, graph2, index, list(), list(), auto)
            if count > 0:
                if graph1.id <= graph2.id:
                    triples.append([graph1, graph2, count])
                else:
                    triples.append([graph2, graph1, count])

        if auto and single:
            print("Graph: Number of automorphisms:")
            for graph1, graph2, count in triples:
                print("{}:    {}".format(graph1.id, count))
        elif auto:
            print("Sets of isomorphic graphs: Number of automorphisms:")
            for graph1, graph2, count in triples:
                print("[{},{}]                {}".format(graph1.id, graph2.id, count))
        else:
            print("Sets of isomorphic graphs:")
            isomorphs = list()
            for graph1, graph2, count in triples:
                if len(isomorphs) == 0:
                    isomorphs.append([graph1, graph2])
                else:
                    for l in isomorphs:
                        if graph1 in l and graph2 not in l:
                            l.append(graph2)
                            break
                        elif graph2 in l and graph1 not in l:
                            l.append(graph1)
                            break
                        elif graph2 not in l and graph1 not in l:
                            isomorphs.append([graph1, graph2])
                            break
            for l in isomorphs:
                sys.stdout.write("[")
                for graph in l:
                    sys.stdout.write("{}, ".format(graph.id))
                print("]")


def sort_triples(triples):
    ret = list()
    for graph1, graph2, count in triples:
        id = 0
        if len(ret) == 0:
            ret.append([graph1, graph2, count])
            continue
        for graph11, graph22, countt in ret:
            if graph11.id > graph1.id:
                id = ret.index([graph11, graph22, countt])
                break
        ret.insert(id, [graph1, graph2, count])

def create_tuples_from_isos(dict_isos: dict) -> list:
    tuples = list()
    for graph in dict_isos.keys():
        for graph1 in dict_isos[graph]:
            if graph == graph1:
                continue
            entry = (graph1, graph)
            if not tuple_in_list(tuples, entry):
                tuples.append(entry)
            for graph2 in dict_isos[graph]:
                if graph1 == graph2:
                    continue
                entry = (graph2, graph1)
                if not tuple_in_list(tuples, entry):
                    tuples.append(entry)
    return tuples


def tuple_in_list(tuples: list, tuple: Tuple) -> bool:
    for tuple1 in tuples:
        if (tuple1[0] == tuple[0] and tuple1[1] == tuple[1]) or (tuple1[0] == tuple[1] and tuple1[1] == tuple[0]):
            return True
    return False



def check_isos(dict1: dict, dict2: dict):
    for graph1 in dict1.keys():
        for graph1_1 in dict1[graph1]:
            if graph1_1 not in dict2[graph1] and graph1 not in dict2[graph1_1]:
                return False
    return True


def is_unbalanced(main_list: list):
    for listVert in main_list:
        if len(listVert) % 2 == 1:
            return True
    return False


def purify_list(main_list: list, graph1: Graph, graph2: Graph) -> list:
    return_list = list()
    for vertices in main_list:
        tlist = list()
        for vertex in vertices:
            if vertex.graph == graph1 or vertex.graph == graph2:
                tlist.append(vertex)
        if len(tlist) > 0:
            return_list.append(tlist)
    return return_list


def count_isomorphisms(list_vertices: list, graph1: Graph, graph2: Graph, index: int,
                       servicable_vertices: list = list(), automorphisms: list = list(), auto: bool = False):
    if is_unbalanced(list_vertices):
        return 0
    if is_bijection(list_vertices, graph1, graph2):
        res = dict()
        for vertices in servicable_vertices:
            for v2 in vertices:
                if v2.graph == graph2:
                    res[v2.label] = v2.color_next
        # print("found bijection: {}".format(check_dict_in_list(automorphisms, res)))
        if not check_dict_in_list(automorphisms, res):
            automorphisms.append(res)
            return 1
        return 0
    num = 0
    color_classes = get_color_classes(list_vertices)
    if len(servicable_vertices) == 0:
        servicable_vertices = color_classes.copy()
    color_class = color_classes[0]
    vertex = get_first_vertex(color_class, graph1)
    vertex.color = index
    vertex.color_next = index
    # print("vertex {}: {}".format(vertex.graph.id, vertex.label))
    color_class.remove(vertex)
    inc_col = dict()
    for vertices in list_vertices:
        for v2 in vertices:
            inc_col[v2] = v2.color
    for change_vertex in color_class.copy():
        if change_vertex.graph == graph2:
            # print("vertex {}: {}".format(change_vertex.graph.id, change_vertex.label))
            change_vertex.color = index
            change_vertex.color_next = index
            color_class.remove(change_vertex)
            llist = list()
            llist.append(vertex)
            llist.append(change_vertex)
            list_vertices.append(llist)
            q, indext = colorize(list_vertices.copy(), index + 1)
            list_vertices.remove(llist)
            color_class.append(change_vertex)
            # print("down vvvvvvvvvvvvvvv")
            num += count_isomorphisms(q.copy(), graph1, graph2, indext + 1, servicable_vertices, automorphisms, auto)
            # print("up ^^^^^^^^^^^^^")
            if not auto and num > 0:
                return num
            for v2 in inc_col.keys():
                v2.color = inc_col[v2]
                v2.color_next = inc_col[v2]
            if not auto and num > 0:
                vertex.color = color_class[0].color
                vertex.color_next = color_class[0].color
                color_class.append(vertex)
                return num
    vertex.color = color_class[0].color
    vertex.color_next = color_class[0].color
    color_class.append(vertex)
    # print(len(automorphisms))
    return num


def check_dict_in_list(l: list, d: dict):
    if len(l) == 0:
        return False
    for dt in l:
        found = True
        for key in d.keys():
            if key not in dt.keys():
                found = False
                break
            if dt[key] != d[key]:
                found = False
                break
        if found:
            return True
    return False


def merge_lists(l1: list, l2: list) -> list():
    res = list()
    l1_deeper = None
    l2_deeper = None
    for l1_item in l1:
        if type(l1_item) is int:
            if l1_item not in res:
                res.append(l1_item)
        else:
            l1_deeper = l1_item
    for l2_item in l2:
        if type(l2_item) is int:
            if l2_item not in res:
                res.append(l2_item)
        else :
            l2_deeper = l2_item
    if l2_deeper and l1_deeper:
        res.append(merge_lists(l2_deeper, l1_deeper))
    elif l1_deeper:
        res.append(l1_deeper)
    else:
        res.append(l2_deeper)
    return res


def get_color_class(main_list: list) -> list:
    for vertices in main_list:
        if len(vertices) > 3:
            return vertices


def get_color_classes(main_list: list) -> list:
    classes = list()
    for vertices in main_list:
        if len(vertices) > 3:
            classes.append(vertices)
    return classes


def get_first_vertex(vertices: list, graph: Graph) -> Vertex:
    for vertex in vertices:
        if vertex.graph == graph:
            return vertex


def filter_bijections(isos: dict, vertices: list) -> dict:
    filtered_iso = dict()
    for graph in isos.keys():
        for graph_1 in isos[graph]:
            if not is_bijection(vertices, graph, graph_1):
                if graph not in filtered_iso.keys():
                    filtered_iso[graph] = list()
                filtered_iso[graph].append(graph_1)
            else:
                pass
                #print(
                #    "Graph " + str(graph.id) + " is ismorphic with graph " + str(graph_1.id) + ", with 1 isomorphism")
    return filtered_iso


def is_iso(list_of_list_verticecs : list, graph_list: list) -> dict:
    main_graphs = dict()
    for graph1 in graph_list:
        main_graphs[graph1] = graph_list.copy()
        main_graphs[graph1].remove(graph1)
    for list_vertices in list_of_list_verticecs:
        graphs = dict()
        for graph1 in graph_list:
            graphs[graph1] = list()
        for vertex in list_vertices:
            if vertex.graph not in graphs:
                continue
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
    remove_duplicate_isos(main_graphs)
    # for graph in main_graphs.keys():
    #     sys.stdout.write("Graph: " + str(graph.id) + " is iso with: ")
    #     sys.stdout.flush()
    #     for gr in main_graphs[graph]:
    #         sys.stdout.write(str(gr.id) + ", ")
    #     sys.stdout.write("\n")
    #     sys.stdout.flush()
    return main_graphs


def remove_duplicate_isos(list_graphs: dict):
    cleaned_graphs = list()
    empty_graphs = list()
    for graph in list_graphs.keys():
        cleaned_graphs.append(graph)
        for graph2 in list_graphs[graph]:
            if graph2 not in cleaned_graphs and len(list_graphs[graph2]) > 0 and graph in list_graphs[graph2]:
                list_graphs[graph2].remove(graph)
                if len(list_graphs[graph2]) == 0:
                    empty_graphs.append(graph2)
    for graph in empty_graphs:
        list_graphs.pop(graph)


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
                            # print("newcolor: {}".format(index))
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
    return main_list, index


def is_bijection(main_list: list, graph1: Graph, graph2: Graph):
    for listVert in main_list:
        found_graphs = list()
        for vertice in listVert:
            if vertice.graph != graph1 and vertice.graph != graph2:
                continue
            if vertice.graph in found_graphs:
                return False
            found_graphs.append(vertice.graph)
        if len(found_graphs) == 1:
            return False
    return True


def colorize_faster(main_list: "list", index: int) -> Tuple[list, int]:
    # start loop empty copy of the list and set changed back to False
    changed = True
    final_list = list()
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
                final_list.append(listVert)
                continue
            # the current list we were trying to split isn't empty so copy all entries from qtt (current working list0
            # to the outer working list qt
            if len(listVert) != 0:
                for vertices in copy_to_split:
                    for v in vertices:
                        v.update()
                    copy_list.append(vertices)
        # update the final list
        main_list = copy_list
    if len(main_list) > 0:
        for listVert in main_list:
            final_list.append(listVert)
    return final_list, index


def is_done(lists: "list"):
    return True

# with open('input/products72.grl') as _file:
#     g, o = read_graph_list(Graph, _file)
# with open('output/cubes.dot', 'w') as _file:
#     write_dot(g[0], _file)
# timeStart = time.time()
# colorize_list(g, False)
# # print(time.time() - timeStart)
with open(input_file) as _file:
    g, o = read_graph_list(Graph, _file)



#
# i = 0
# for graph in g:
#     graph.id = i
#     i += 1
# if mode == 0:
#     colorize_list(g, True)
# elif mode == 1:
#     with open(input_file) as _file:
#         g2, o = read_graph_list(Graph, _file)
#     for graph in g2:
#         g.append(graph)
#     i = 0
#     for graph in g:
#         graph.id = i
#         i += 1
#     colorize_list(g, True, True)
# elif mode == 2:
#     colorize_list(g, False)

