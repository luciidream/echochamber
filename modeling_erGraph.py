import polarization_model2 as pm2
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns


def models(params, alpha, prob, mark):
    params['alpha'] = alpha
    # -------------------------------ER RANDOM GRAPH------------------------------- #
    G = nx.fast_gnp_random_graph(params['N'], prob)
    while not(nx.is_connected(G)):
        G = nx.fast_gnp_random_graph(params['N'], prob)
    # -------------------------------ER RANDOM GRAPH------------------------------- #
    # ----------------------------BARABASI ALBERT GRAPH---------------------------- #
    # new_edges = int(prob * params['N'])
    # G = nx.barabasi_albert_graph(params['N'], new_edges)
    # while not (nx.is_connected(G)):
    #     G = nx.barabasi_albert_graph(params['N'], new_edges)
    # ----------------------------BARABASI ALBERT GRAPH---------------------------- #
    largest_cc = max(nx.connected_components(G), key=len)
    lcc = np.array(list(largest_cc))
    x0 = np.linspace(-1, 1, params['N'])
    centrality_dict = pm2.calculate_centrality(G, mark)

    params['centrality'] = []
    for val in centrality_dict.values():
        params['centrality'].append(val)

    results = pm2.simulating_model(params, G, x0, lcc)
    return results


def plotting(results, params, prob, alpha):

    params['alpha'] = alpha
    x_t = results['x_t']
    t_arr = results['t_arr']
    pro_x = x_t.copy()
    con_x = x_t.copy()
    pro_x[pro_x <= 0] = np.NaN
    con_x[con_x > 0] = np.NaN

    sns.set_theme()
    plt.figure()
    plt.plot(t_arr, pro_x.T, color='blue', lw=0.5)
    plt.plot(t_arr, con_x.T, color='red', lw=0.5)
    plt.xlabel("Time")
    plt.ylabel("Opinions xi(t)")
    str1 = 'beta=' + str(params['beta'])
    str2 = 'alpha=' + str(params['alpha'])
    str3 = 'N=' + str(500)
    str4 = '<k>=' + str(prob * params['N'])
    plt.legend([str1, str2, str3, str4])
    plt.show()


def calculate_final_x(results, params):
    """

    :return: abs first
    """
    final_ind = int(params['T'] / params['dt'])
    x_final = results['x_t'][:, final_ind]
    return np.average(np.abs(x_final))


def calculate_final_x2(results, params):
    """

    :return: average first
    """
    final_ind = int(params['T'] / params['dt'])
    x_final = results['x_t'][:, final_ind]
    return np.abs(np.average(x_final))

# def heatmap_plotting(avg_final_xi):

