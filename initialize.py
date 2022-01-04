import networkx as nx
import numpy as np


def graph_degree(graph):
    return [d for i, d in graph.degree]


class ClusterControl:
    def __init__(self, graph, t=100):
        self.G = graph
        self.iter = t
        prob_matrix = nx.adjacency_matrix(graph).todense()
        trans_matrix = np.apply_along_axis(lambda x: x / graph_degree(graph), 0, prob_matrix)
        self.trans_matrix = np.linalg.matrix_power(trans_matrix, t)


class Cluster:
    def __init__(self, node, clust_control):
        self.nodes = {node}
        self.probs = clust_control.trans_matrix[node, ]
        self.neighbors = {
            other: np.sqrt(np.sum(np.square(clust_control.trans_matrix[node] - clust_control.trans_matrix[other]) / graph_degree(clust_control.G)))
            for other in clust_control.G.neighbors(node)
        }

    def merge(self, other):
        pass
