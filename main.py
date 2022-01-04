import matplotlib.pyplot as plt
import networkx as nx

from initialize import ClusterControl, ClusterArray, find_merge

G = nx.windmill_graph(10, 3)

plt.figure(num=None, figsize=(30, 30), dpi=80)
plt.axis('off')
fig = plt.figure(1)
nx.draw(G, with_labels=True,node_size=1000)
plt.title("Regular Layout")
plt.show()

cc = ClusterControl(G)
clusters = ClusterArray(G, cc)
i, j, _ = find_merge(clusters)
clusters.merge(i, j)
