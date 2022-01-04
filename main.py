import csv
import time
from collections import OrderedDict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from initialize import ClusterControl, ClusterArray, find_merge, Partition, q_metric

start = time.time()
PATH = "D3-UNC.csv"

with open(f"datasets/{PATH}", newline='\n') as csvfile:
    data = np.loadtxt(csvfile, delimiter=",")

set_k = False
k = 1
n, m = 12, 6
# G = nx.barbell_graph(n, m)
G = nx.from_numpy_matrix(data)

#colors = distinctipy.get_colors(G.number_of_nodes())

# display the colours
#distinctipy.color_swatch(colors)


def plot_colored(clusters, G, colors):
    plt.figure(num=None, figsize=(30, 30), dpi=80)
    plt.axis('off')
    node_colors = [None] * G.number_of_nodes()
    for i, (key, cluster) in enumerate(clusters.clusters.items()):
        for n in cluster.nodes:
            node_colors[n] = colors[i]
    fig = plt.figure(1)
    nx.draw(G, node_color=node_colors, with_labels=True, node_size=1000)
    plt.title(f"Barbell Graph with {len(clusters.clusters)} clusters")
    plt.show()


def save_results(partition, G):
    dic = OrderedDict.fromkeys(sorted([n+1 for n in G.nodes]), 0)
    for i, cluster in enumerate(partition.split):
        for n in cluster:
            dic[n+1] = i+1
    with open(f'results/{PATH}', 'w') as csvfile:
        for key in dic.keys():
            csvfile.write("%s, %s\n" % (key, dic[key]))
    return dic


#plt.figure(num=None, figsize=(30, 30), dpi=80)
#plt.axis('off')
#fig = plt.figure(1)
#nx.draw(G, with_labels=True, node_size=1000)
#plt.title("Barbell Graph")
#plt.show()

cc = ClusterControl(G, t=500)
clusters = ClusterArray(G, cc)
partitions = {}
num = G.number_of_nodes()
best_num = num
max_q = q_metric(G, clusters)
for num in range(G.number_of_nodes() - k):
    i, j, distance = find_merge(clusters)
    clusters.merge(i, j)
    num -= 1
    q = q_metric(G, clusters)
    #print(f"There are {len(clusters.clusters)} partitions with Q {q}")
    if q > max_q:
        max_q = q
        best_num = len(clusters.clusters)
    partitions[len(clusters.clusters)] = Partition([x.nodes for x in clusters.clusters.values()], distance)
#print(max_q, best_num)

if set_k:
    save_results(partitions[k], G)
else:
    save_results(partitions[best_num], G)
end = time.time()
print(end - start)
#plot_colored(clusters, G, colors)
