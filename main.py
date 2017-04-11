from graph import Graph
import AHU


def isomorph(g1: Graph, g2: Graph):
    if g1.is_tree():
        if not g2.is_tree():
            return False
        return AHU.ahu_tree_isomorhpism(g1, g2)
