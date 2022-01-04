import networkx as nx
import numpy as np


def q_metric(G, clusters):
    q = 0
    total_edges = len(G.edges)
    for key, cluster in clusters.clusters.items():
        ei, ai = 0.0, 0.0
        for n in cluster.nodes:
            edges = G.edges(n)
            for (i, j) in edges:
                if i in cluster.nodes and j in cluster.nodes:
                    ei += 1
                ai += 1
        q += (ei - (ai ** 2)/total_edges)/total_edges
    return q


def graph_degree(graph):
    return [d for i, d in graph.degree]


def distance_squared(var_1, var_2, graph):
    return np.sum(np.square(var_1 - var_2) / graph_degree(graph))


def initial_variance(node, other, cluster_control):
    return distance_squared(cluster_control.trans_matrix[node, ],
                            cluster_control.trans_matrix[other, ],
                            cluster_control.G) / (2 * cluster_control.G.number_of_nodes())


def initialize_cluster(node, cluster_control):
    return Cluster(
        node,
        {node},
        cluster_control.trans_matrix[node, ],
        {other: initial_variance(node, other, cluster_control) for other in cluster_control.G.neighbors(node)}
    )


def recompute_variance(node_1, node_2, new_node, target, graph):
    if target.index in node_1.neighbors.keys() and target.index in node_2.neighbors.keys():
        variance_1 = (node_1.size + new_node.size) * node_1.neighbors[target.index]
        variance_2 = (node_2.size + new_node.size) * node_2.neighbors[target.index]
        # Could also access node_1.index from node_2.neighbors
        self_variance = new_node.size * node_1.neighbors[node_2.index]
        return (variance_1 + variance_2 - self_variance) / (node_1.size + node_2.size + new_node.size)
    else:
        factor = (node_1.size + node_2.size) * new_node.size / (node_1.size + node_2.size + new_node.size)
        return factor * distance_squared(new_node.probs, target.probs, graph) / graph.number_of_nodes()


class ClusterControl:
    def __init__(self, graph, t=100):
        self.G = graph
        self.iter = t
        prob_matrix = nx.adjacency_matrix(graph).todense()
        trans_matrix = np.apply_along_axis(lambda x: x / graph_degree(graph), 0, prob_matrix)
        self.trans_matrix = np.linalg.matrix_power(trans_matrix, t)


class ClusterArray:
    def __init__(self, graph, cluster_control):
        self.index = graph.number_of_nodes()
        self.clusters = {i: initialize_cluster(i, cluster_control) for i in range(graph.number_of_nodes())}
        self.control = cluster_control

    def next_index(self):
        self.index += 1
        return self.index

    def merge(self, i, j):
        c = self.clusters[i].merge(self.clusters[j], self)
        self.clusters[c.index] = c
        self.clusters.pop(i)
        self.clusters.pop(j)
        return self


class Cluster:
    def __init__(self, index, nodes, probs, neighbors):
        self.index = index
        self.nodes = nodes
        self.size = len(self.nodes)
        self.probs = probs
        self.neighbors = neighbors

    def merge_neighbors(self, i, j, new_index, score):
        self.neighbors.pop(i, None)
        self.neighbors.pop(j, None)
        self.neighbors[new_index] = score
        return self

    def merge(self, other, clusters):
        c = Cluster(
            clusters.next_index(),
            self.nodes.union(other.nodes),
            # Weighted average
            (self.size * self.probs + other.size * other.probs) / (self.size + other.size),
            dict()
        )

        neighbors = set(self.neighbors.keys()).union(set(other.neighbors.keys()))
        neighbors.remove(self.index)
        neighbors.remove(other.index)

        c.neighbors = {
            target: recompute_variance(self, other, c, clusters.clusters[target], clusters.control.G) for target in neighbors
        }

        for target, score in c.neighbors.items():
            clusters.clusters[target].merge_neighbors(self.index, other.index, c.index, score)

        return c


def find_merge(clusters):
    # We need to find 2 clusters with the least distance to merge
    # in the next step
    min_d, to_merge = None, None
    for i, cluster in clusters.clusters.items():
        for j, dist in cluster.neighbors.items():
            if min_d is None or dist < min_d:
                min_d = dist
                to_merge = (i, j)
    return to_merge[0], to_merge[1], min_d


class Partition:
    def __init__(self, split, score):
        self.split = split
        self.score = score
