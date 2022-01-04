import matplotlib.pyplot as plt
import networkx as nx

from initialize import ClusterControl, ClusterArray, find_merge, Partition

# G = nx.windmill_graph(10, 3)
G = nx.generators.barbell_graph(10, 2)

plt.figure(num=None, figsize=(30, 30), dpi=80)
plt.axis('off')
fig = plt.figure(1)
nx.draw(G, with_labels=True,node_size=1000)
plt.title("Regular Layout")
plt.show()

cc = ClusterControl(G, t=500)
clusters = ClusterArray(G, cc)
partitions = []
for k in range(G.number_of_nodes() - 1):
    i, j, distance = find_merge(clusters)
    clusters.merge(i, j)
    partitions.append(Partition([x.nodes for x in clusters.clusters.values()], distance))
