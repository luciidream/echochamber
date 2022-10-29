import matplotlib.pyplot

import polarization_model2 as pm2
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
# import other_plots as op


if __name__ == '__main__':
    nodes = 500
    delta = 0.3

    mark = 'c'
    # -------------------------------ER RANDOM GRAPH------------------------------- #
    average_degree = 0.95
    G = nx.fast_gnp_random_graph(nodes, average_degree)
    while not(nx.is_connected(G)):
        G = nx.fast_gnp_random_graph(nodes, average_degree)
    # -------------------------------ER RANDOM GRAPH------------------------------- #
    # ----------------------------BARABASI ALBERT GRAPH---------------------------- #
    # new_edges_rate = 0.95
    # new_edges = int(new_edges_rate * nodes)
    # G = nx.barabasi_albert_graph(nodes, new_edges)
    # while not(nx.is_connected(G)):
    #     G = nx.barabasi_albert_graph(nodes, new_edges)
    # ----------------------------BARABASI ALBERT GRAPH---------------------------- #
    largest_cc = max(nx.connected_components(G), key=len)
    lcc = np.array(list(largest_cc))
    largest_connected_subgraph = nx.subgraph(G, largest_cc)
    params = {'T': 10., 'N': len(largest_cc), 'dt': 0.01, 'beta': 1, 'K': 1, 'alpha': 3, 'a_val': 0.1}
    # x0 = np.linspace(-1 - delta, 1 - delta, params['N'])
    x0 = np.linspace(-1, 1, params['N'])
    # np.random.shuffle(x0)
    centrality_dict = pm2.calculate_centrality(largest_connected_subgraph, mark)
    params['centrality'] = []
    for val in centrality_dict.values():
        params['centrality'].append(val)

    results = pm2.simulating_model(params, largest_connected_subgraph, x0, lcc)
    x_t = results['x_t']
    t_arr = results['t_arr']

    pro_x = x_t.copy()
    con_x = x_t.copy()
    pro_x[pro_x <= 0] = np.NaN
    con_x[con_x > 0] = np.NaN

    sns.set_theme()
    plt.figure(dpi=400, figsize=(16, 12))
    plt.plot(t_arr, pro_x.T, color='#20afdf', lw=0.2)
    plt.plot(t_arr, con_x.T, color='#ff80b3', lw=0.2)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel(" $t$ ", fontsize=20)
    plt.ylabel(" $x_{i}(t)$ ", fontsize=20)
    # -------------------------------ER RANDOM GRAPH------------------------------- #
    # str1 = 'beta=' + str(params['beta'])
    # str2 = 'alpha=' + str(params['alpha'])
    # str3 = 'N=' + str(nodes)
    # str4 = 'prob=' + str(average_degree)
    # -------------------------------ER RANDOM GRAPH------------------------------- #
    # ----------------------------BARABASI ALBERT GRAPH---------------------------- #
    # str1 = 'beta=' + str(params['beta'])
    # str2 = 'alpha=' + str(params['alpha'])
    # str3 = 'N=' + str(nodes)
    # str4 = 'prob=' + str(new_edges_rate)
    # ----------------------------BARABASI ALBERT GRAPH---------------------------- #
    # plt.legend([str1, str2, str3, str4])

    plt.title('Random Initial State ' + 'ER Random Graph ' + ' ' + 'N' + '=' + str(nodes) + ' '
              + r'$\alpha $' + '=' + str(params['alpha']) + ' ' + '$p$' + '=' + str(average_degree),
              fontsize=20)
    plt.show()
    # op.colored_network(G, np.array(x_t[:, int(params['T'] / params['dt'])]))

