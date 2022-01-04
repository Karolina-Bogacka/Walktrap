import matplotlib.pyplot as plt
import networkx as nx
from distinctipy import distinctipy

from initialize import ClusterControl, ClusterArray, find_merge

k = 2
n, m = 10, 15
G = nx.barbell_graph(n, m)

colors = distinctipy.get_colors(n * 2 + m)

# display the colours
distinctipy.color_swatch(colors)


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


plt.figure(num=None, figsize=(30, 30), dpi=80)
plt.axis('off')
fig = plt.figure(1)
nx.draw(G, with_labels=True, node_size=1000)
plt.title("Barbell Graph")
plt.show()

cc = ClusterControl(G)
clusters = ClusterArray(G, cc)
for _ in range(2*n+m-k):
    i, j, _ = find_merge(clusters)
    clusters.merge(i, j)
plot_colored(clusters, G, colors)
