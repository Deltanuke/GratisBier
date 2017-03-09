from graph import *


class Colorize(object):

    def colorize_graph(self, G : "Graph"):
        q = dict()
        index = 0
        for g in G.vertices:
            g.color = g.degree
            if g.color not in q:
                q[g.color] = list()
            q[g.color].append(g)
            if g.degree > index:
                index = g.degree

        while not self.is_done(q):
            qt = dict()
            index = 0;
            for g in q.items():
                i = 0;
                qtt = dict()
                if len(g) > 1:
                    for v in g:


                else:
                    qt[index] = g
                    index += 1


    def is_done(self, G : "dict"):
        for g in G.items():
            if len(g) > 1:
                return False
        return True

g = Graph(False, 4)
