import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from netgraph import Graph


def what_edge(node_lists, edge_list):
    pp_edges = []
    cc_edges = []
    pc_edges = []
    for pair in edge_list:
        if (pair[0] in node_lists[0]) and (pair[1] in node_lists[0]):
            pp_edges.append(pair)
        if (pair[0] in node_lists[1]) and (pair[1] in node_lists[1]):
            cc_edges.append(pair)
        if ((pair[0] in node_lists[1]) and (pair[1] in node_lists[0])) or ((pair[0] in node_lists[0]) and (pair[1] in node_lists[1])):
            pc_edges.append(pair)

    return pp_edges, cc_edges, pc_edges


def colored_network(G, x):
    plt.figure(dpi=400, figsize=(16, 16))
    # pos = nx.spring_layout(G)
    node_list = np.array([node for node in G.nodes()])
    # edge_list = [edge for edge in G.edges()]

    pro_node = list(node_list[np.where(x > 0)[0]])
    con_node = list(node_list[np.where(x < 0)[0]])
    neu_node = list(node_list[np.where(x == 0)[0]])

    # nx.draw_networkx_nodes(G, pos, pro_node, node_color='tab:blue', node_size=80, alpha=0.5)
    # nx.draw_networkx_nodes(G, pos, con_node, node_color='tab:red', node_size=80, alpha=0.5)
    # nx.draw_networkx_nodes(G, pos, neu_node, node_color='tab:black', node_size=80, alpha=0.3)
    #
    # pp_edges, cc_edges, pc_edges = what_edge([pro_node, con_node, neu_node], edge_list)
    # other_edges = list(set(edge_list) - set(pp_edges) - set(cc_edges) - set(pc_edges))

    # nx.draw_networkx_edges(G, pos, width=0.05, alpha=0.3)
    # nx.draw_networkx_edges(G, pos, edgelist=pp_edges, width=0.1, alpha=0.3, edge_color='tab:blue')
    # nx.draw_networkx_edges(G, pos, edgelist=cc_edges, width=0.1, alpha=0.3, edge_color='tab:red')
    # nx.draw_networkx_edges(G, pos, edgelist=pc_edges, width=0.1, alpha=1, edge_color='tab:purple')
    # nx.draw_networkx_edges(G, pos, edgelist=other_edges, width=0.1, alpha=0.5, edge_color='tab:black')

    node_to_community = {}
    for node in pro_node:
        node_to_community[node] = 0
    for node in con_node:
        node_to_community[node] = 1
    for node in neu_node:
        node_to_community[node] = 2
    community_map = {
        0: 'tab:blue',
        1: 'tab:red',
        2: 'tab:purple'
    }
    node_color = {node: community_map[community_id] for node, community_id in node_to_community.items()}
    Graph(G,
          node_color=node_color,
          node_edge_width=0,
          node_alpha=0.5,
          node_size=2.0,
          edge_alpha=0.1,
          node_layout='community',
          node_layout_kwargs=dict(node_to_community=node_to_community),
          edge_layout='bundled',
          edge_layout_kwargs=dict(k=2000),)

    plt.axis('off')
    plt.show()
