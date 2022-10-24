import networkx as nx
import numpy as np
import itertools as it


def get_p1_and_p2(k1, k2, N):
    p2 = (2. * k2) / ((N - 1.) * (N - 2.))
    p1 = (k1 - 2. * k2) / ((N - 1.) - 2. * k2)
    if (p1 >= 0) and (p2 >= 0):
        return p1, p2
    else:
        raise ValueError('Negative probability!')


def generate_sc(N, p1, p2):
    G = nx.fast_gnp_random_graph(N, p1)
    while not nx.is_connected(G):
        G = nx.fast_gnp_random_graph(N, p1)

    triangles_list = []

    for tri in it.combinations(list(G.nodes()), 3):
        if np.random.uniform(0, 1) <= p2:
            triangles_list.append(tri)

            G.add_edge(tri[0], tri[1])
            G.add_edge(tri[1], tri[2])
            G.add_edge(tri[0], tri[2])

    node_neighbors_dict = {}
    for n in list(G.nodes()):
        node_neighbors_dict[n] = G[n].keys()

    node_triangles_dict = {}
    for tri in triangles_list:
        for n in tri:
            if n in node_triangles_dict.keys():
                node_triangles_dict[n].append(tri)
            else:
                node_triangles_dict[n] = [tri]

    return G, node_neighbors_dict, node_triangles_dict, triangles_list



