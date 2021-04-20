from parse import write_input_file, read_input_file, write_output_file
from random import randrange
import networkx as nx
import matplotlib.pyplot as plt

V = 100
G = nx.Graph()
edges = []
for i in range(V):
    for j in range(i + 1, V):
        length = randrange(100000) / 1000
        edge = (i, j, length)
        edges.append(edge)

G.add_weighted_edges_from(edges)
fileName = str(V) + '.in'
write_input_file(G, fileName)

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

