import time

import networkx as nx

from initialize import ClusterControl, ClusterArray, find_merge, Partition, q_metric, save_results, open_data


def run_unset(PATH):
    data = open_data(PATH)
    start = time.time()
    G = nx.from_numpy_matrix(data)
    cc = ClusterControl(G, t=500)
    clusters = ClusterArray(G, cc)
    num = G.number_of_nodes()
    best_num = num
    max_q = q_metric(G, clusters)
    partition = Partition([x.nodes for x in clusters.clusters.values()])
    for _ in range(num-1):
        i, j, distance = find_merge(clusters)
        clusters.merge(i, j)
        q = q_metric(G, clusters)
        if q > max_q:
            max_q = q
            best_num = len(clusters.clusters)
            partition = Partition([x.nodes for x in clusters.clusters.values()])
    end = time.time()
    save_results(partition, G, PATH)
    return max_q, best_num, end - start


def run_set(PATH, k):
    data = open_data(PATH)
    start = time.time()
    G = nx.from_numpy_matrix(data)
    cc = ClusterControl(G, t=500)
    clusters = ClusterArray(G, cc)
    for n in range(G.number_of_nodes() - k):
        i, j, distance = find_merge(clusters)
        clusters.merge(i, j)
    partition = Partition([x.nodes for x in clusters.clusters.values()])
    end = time.time()
    save_results(partition, G, PATH)
    return end - start


print(run_set("D1-K=2.csv", 2))
print(run_unset("D1-UNC.csv"))
print(run_set("D2-K=7.csv", 7))
print(run_unset("D2-UNC.csv"))
print(run_set("D3-K=12.csv", 12))
print(run_unset("D3-UNC.csv"))
