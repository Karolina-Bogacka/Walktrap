import networkx as nx
import numpy as np


class ClusterControl:
    def __init__(self, graph, iter=100):
        self.G = graph
        self.iter = iter
        self.prob_matrix = np.linalg.matrix_power(nx.linalg.adjacency_matrix(graph), iter)


class Cluster:
    def __init__(self, node, clust_control):
        self.nodes = {node}
        self.probs = clust_control.prob_matrix[node, ].toarray()
        self.neighbors = clust_control.G.neighbors(node)

    def merge(self, other):
        pass
