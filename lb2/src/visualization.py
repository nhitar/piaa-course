import matplotlib.pyplot as plt
import networkx as nx


def visualize_mst(weight_matrix, path):
    G = nx.Graph()

    num_nodes = len(weight_matrix)
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = weight_matrix[i][j]
            if weight != 0:
                G.add_edge(i, j, weight=weight)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')

    path_edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if G.has_edge(u, v):
            path_edges.append((u, v))

    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2, edge_color='red')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.title("Визуализация графа с выделенным путём обхода")
    plt.axis('off')
    plt.show()
