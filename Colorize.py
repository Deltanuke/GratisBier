from graph.graph import *
from graph.graph_io import *
import collections

# Settings
use_color = True


# Globals
class Counter():
    def __init__(self):
        self.count = 0

    def next(self):
        self.count += 1
        return self.count - 1


counter = Counter()
available_color_names = [
    "cyan",
    "darkgreen",
    "darkorange",
    "deeppink",
    "lawngreen",
    "magenta",
    "yellow",
    "maroon",
    "red",
    "saddlebrown",
    "purple",
    "blue",
    "navy",
    "pink",
    "black",
    "darkred",
    "slategrey",
    "greenyellow",
    "firebrick1",
    "gold3",
    "deeppink3",
    "deeppink",
    "azure4",
    "aquamarine",
    "blueviolet"
]
available_fill_color_names = available_color_names.copy()

# Explanation: For every item in the first list, make sure there are as many of them in the other
compare_neighbour_colors = lambda x, y: collections.Counter(x) == collections.Counter(y)


class Color():
    def __init__(self, vertices: List["Vertex"]):
        self._vertices = vertices

        if use_color:
            # Select and apply the actual color for this color group
            self.color = available_color_names.pop(0)
            self._apply_color_to_vertices()
        else:
            # Select a number to label the vertices
            self.number = counter.next()
            self._apply_number_to_vertices()

    def _apply_color_to_vertices(self):
        for v in self._vertices:
            v.colortext = self.color

    def _apply_number_to_vertices(self):
        for v in self._vertices:
            v.label = self.number

    def branch_color(self, vertices: List["Vertex"]):
        # Split off the vertices that are no longer part of this color
        for v in vertices:
            self._vertices.remove(v)

        return Color(vertices)

    def get_vertices(self):
        return self._vertices.copy()

    def no_vertices(self):
        return len(self._vertices)


def colorize(g: Graph):
    # Place all the vertices in a initial color
    colors = [Color(g.vertices)]

    previous_number_of_colors = 0
    while not previous_number_of_colors == len(colors):
        # Update remember amount of colors
        previous_number_of_colors = len(colors)

        # Remember the current color configuration
        history = color_history(g)

        # Process all colors
        for c in colors:
            new = refine(c, history)

            # Continue refining while we can branch the color into more
            while new is not None:
                colors.append(new)
                new = refine(c, history)


def refine(c: Color, history: dict):
    # Get a single vertice from a copied list
    vertices = c.get_vertices()
    first = vertices.pop(0)

    # Make a list that will hold all the vertices that should be in the same color
    equals = [first]
    for v in vertices:
        if should_be_same_color(first, v, history):
            equals.append(v)

    # Decide whether to create a new color or to keep the current one
    if not len(equals) == c.no_vertices():
        return c.branch_color(equals)
    else:
        return None


def should_be_same_color(u: Vertex, v: Vertex, history: dict):
    if history[u] == history[v]:
        # List all the neighbour colors for u and v
        un = [history[w] for w in u.neighbours]
        vn = [history[w] for w in v.neighbours]

        # Check whether un and vn are identical
        if compare_neighbour_colors(un, vn):
            return True
    return False


def color_history(g: Graph):
    history = {}
    for v in g.vertices:
        # Determine whether we are using the labels or the colors
        if use_color:
            history[v] = v.colortext
        else:
            history[v] = v.label
    return history


with open('colorref_smallexample_2_49.grl') as f:
    G = load_graph(f)

colorize(G)

with open('output/result.dot', 'w') as f:
    write_dot(G, f)
