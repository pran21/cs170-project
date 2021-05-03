import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import itertools as it


def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    cities = []
    edges = []
    k = 15
    c = 1
    endNode = len(G.nodes) - 1
    newG = G.copy()
    print(G.nodes)

    bestNode = (None, -1)
    for node in list(G.nodes):
        if node == 0 or node == endNode:
            continue
        Gprime = newG.copy()
        Gprime.remove_node(node)
        dists, paths = nx.single_source_dijkstra(Gprime, 0)
        if dists[endNode] > bestNode[1]:
            bestNode = (node, dists[endNode])        
    cities.append(bestNode[0])

    for _ in range(k):
        assert nx.is_connected(newG)
        dists, paths = nx.single_source_dijkstra(newG, 0)
        shortestPath = paths[endNode]
        shortestEdge = (None, float('inf'))
        for i in range(len(shortestPath) - 1):
            edge = G.edges[shortestPath[i], shortestPath[i+1]]
            if edge['weight'] < shortestEdge[1]:
                testG = newG.copy()
                testG.remove_edge(shortestPath[i], shortestPath[i+1])
                if not nx.is_connected(testG):
                    continue
                shortestEdge = ((shortestPath[i], shortestPath[i+1]), edge['weight'])
        # print(shortestPath)
        # print(shortestEdge)
        edges.append(shortestEdge[0])
        newG.remove_edge(shortestEdge[0][0], shortestEdge[0][1])

    return cities, edges


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    # assert len(sys.argv) == 2
    # path = sys.argv[1]
    for i in range(1, 100):
        print("INPUT: ", i)
        path = 'inputs/small/small-' + str(i) + '.in'
        G = read_input_file(path)
        c, k = solve(G)
        assert is_valid_solution(G, c, k)
        print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
        output_path = 'outputs/small-' + str(i) + '.out'
        write_output_file(G, c, k, output_path)
    # write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
