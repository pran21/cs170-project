import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import matplotlib.pyplot as plt
import itertools as it


def getEdgesInClique(clique, G):
    edges = []
    possibleEdges = list(it.combinations(clique, 2))
    for edge in possibleEdges:
        if edge in G.edges:
            edges.append(edge)
    return edges

def getMostImpactfulNode(G):
    endNode = max(G.nodes)
    bestNode = (None, -1)
    for node in G.nodes:
        if node == 0 or node == endNode:
            continue
        newG = G.copy()
        newG.remove_node(node)
        if not nx.is_connected(newG):
            continue
        dists, paths = nx.single_source_dijkstra(newG, 0)
        if dists[endNode] > bestNode[1]:
            bestNode = (node, dists[endNode])
    return bestNode[0]

def getMostImpactfulEdge(combos, G):
    endNode = max(G.nodes)
    bestEdge = (None, -1)
    for edges in combos:
        newG = G.copy()
        for edge in edges:
            if newG.has_edge(*edge):
                newG.remove_edge(edge[0], edge[1])
            if not nx.is_connected(newG):
                newG.add_edge(edge[0], edge[1])
                continue
        
        dists, paths = nx.single_source_dijkstra(newG, 0)
        if dists[endNode] > bestEdge[1]:
            bestEdge = (edges, dists[endNode])
    return bestEdge[0]

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
    endNode = max(G.nodes)
    newG = G.copy()
    edgeToKeep = []

    for _ in range(c):
        bestNode = getMostImpactfulNode(newG)     
        cities.append(bestNode)
        newG.remove_node(bestNode)

    while k > 0:
        assert nx.is_connected(newG)
        dists, paths = nx.single_source_dijkstra(newG, 0)
        shortestPath = paths[endNode]
        edgeList = []
        # for i in range(len(shortestPath) - 1):
        #     edgeList.append((shortestPath[i], shortestPath[i+1]))
        for node in shortestPath:
            for edge in newG.edges:
                if edge[0] == node or edge[1] == node:
                    edgeList.append(edge)
        edgeList = list(set([i for i in edgeList]))
        for edge in edgeToKeep:
            if edge in edgeList:
                edgeList.remove(edge)
        print(edgeList)
        edgeCombinations = list(it.combinations(edgeList, 2))
        print("Number of combos: ", len(edgeCombinations))

        bestCombination = getMostImpactfulEdge(edgeCombinations, newG)
        print('best: ', bestCombination)
        if bestCombination:
            for edge in bestCombination:
                if k == 0:
                    break
                if newG.has_edge(*edge):
                    k -=1
                    edges.append(edge)
                    newG.remove_edge(edge[0], edge[1])
                if not nx.is_connected(newG):
                    # k += 1
                    edges.remove(edge)
                    newG.add_edge(edge[0], edge[1])
                    edgeToKeep.append(edge)


    print('Cities: ', cities)
    print('Edges: ', edges)
    return cities, edges

def solve2(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    cities = []
    edges = []
    k = 50
    c = 3
    endNode = max(G.nodes)
    newG = G.copy()

    for _ in range(c):
        bestNode = getMostImpactfulNode(newG)
        if bestNode:
            cities.append(bestNode)
            newG.remove_node(bestNode)

    for _ in range(k):
        assert nx.is_connected(newG)
        dists, paths = nx.single_source_dijkstra(newG, 0)
        shortestPath = paths[endNode]
        edgeList = []
        for i in range(len(shortestPath) - 1):
            edgeList.append((shortestPath[i], shortestPath[i+1]))
        edgeCombinations = list(it.combinations(edgeList, 1))
        # if len(edgeList) > 1:
        #     edgeCombinations = list(it.combinations(edgeList, 2))
        # else:
        #     edgeCombinations = list(it.combinations(edgeList, 1))
        # print("Number of combos: ", len(edgeCombinations))

        bestCombination = getMostImpactfulEdge(edgeCombinations, newG)
        # print('best: ', bestCombination)
        if bestCombination:
            for edge in bestCombination:
                if newG.has_edge(*edge):
                    edges.append(edge)
                    newG.remove_edge(edge[0], edge[1])
                if not nx.is_connected(newG):
                    edges.remove(edge)
                    newG.add_edge(edge[0], edge[1])
    print('Cities: ', cities)
    print('Edges: ', edges)
    return cities, edges


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

def single_file(lol):
    path = 'inputs/small/small-' + str(lol) +  '.in'
    # path = 'test.in'
    # path = 'inputs/medium/medium-' + str(lol) +  '.in'
    # path = 'inputs/large/large-' + str(lol) +  '.in'
    G = read_input_file(path)
    print(G.nodes)
    # c, k = solve2(G)
    c, k = solve2(G)
    assert is_valid_solution(G, c, k)
    print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
    write_output_file(G, c, k, 'small-test.out')

if __name__ == '__main__':
    # single_file(62)
    for i in range(1, 301):
        print("INPUT: ", i)
        path = 'inputs/medium/medium-' + str(i) + '.in'
        G = read_input_file(path)
        c, k = solve2(G)
        assert is_valid_solution(G, c, k)
        print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
        output_path = 'outputs/medium-' + str(i) + '.out'
        write_output_file(G, c, k, output_path)

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
