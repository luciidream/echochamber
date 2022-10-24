import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns


def sigmoidal_func(x):
    return 2 * (1 / (1 + np.exp(-x))) - 1


def f_activity(sigma, x):
    # calculate equation(1)
    return sigma - x


def rkc_activity(f, dt, sigma, x):
    # Runge-Kutta integration
    k1 = dt * f(sigma, x)
    k2 = dt * f(sigma, x + k1 / 2.)
    k3 = dt * f(sigma, x + k2 / 2.)
    k4 = dt * f(sigma, x + k3)

    return k1, k2, k3, k4


def integration_step(f, dt, sigma, x):
    k1, k2, k3, k4 = rkc_activity(f, dt, sigma, x)

    return x + (1. / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def whos_active(a, N, largest_cc):
    # sample which agents are activated
    return largest_cc[np.where(np.random.uniform(0, 1, size=N) < a)[0]]


def calculate_centrality(G, mark):
    # conviction - edge weight
    # return a dictionary
    if mark == 'c':
        return nx.information_centrality(G)
    if mark == 'b':
        return nx.betweenness_centrality(G, k=nx.number_of_nodes(G))


def sigma_inputs_ad2(A, x, K, alpha, centrality):
    # centrality is array
    Ax = A * x
    # summation = np.sum(centrality * np.tanh(alpha * Ax), axis=1)
    summation = np.sum(centrality * sigmoidal_func(alpha * Ax), axis=1)
    # summation = np.dot(centrality, np.tanh(alpha * Ax))
    return K * summation


def homophily_sampling_connected(i, x, beta, G):
    neighbours = [n for n in G.neighbors(i)]
    degree = len(neighbours)
    dist_i = np.abs(x[neighbours] - x[i])
    p = (dist_i ** -beta)
    p /= np.sum(p)
    return np.unique(np.random.choice(range(degree), size=degree, replace=True, p=p))


def modify_matrix(x, a, beta, N, G, largest_cc):
    A = np.zeros((N, N))
    active_nodes = whos_active(a, N, largest_cc)
    for node in active_nodes:
        targets = homophily_sampling_connected(node, x, beta, G)
        for t in targets:
            A[node, t] = 1
            A[t, node] = 1
    return A


def simulating_model(params, G, x0, largest_cc):
    # cou = 0
    # sns.set_theme()
    N = params['N']
    dt = params['dt']
    T = params['T']
    K = params['K']
    alpha = params['alpha']
    a_val = params['a_val']
    beta = params['beta']
    centrality = params['centrality']

    timesteps = int(T / dt) + 1
    t_arr = np.linspace(0, T, timesteps)

    x_t = np.zeros((N, int(timesteps)))
    x = x0

    a = np.ones(N) * a_val

    for t in range(timesteps):
        x_t[:, t] = x
        A = modify_matrix(x, a, beta, N, G, largest_cc)
        sigma = sigma_inputs_ad2(A, x, K, alpha, centrality)
        x = integration_step(f_activity, dt, sigma, x)
        # plt.hist(x, bins=50)
        # plt.show()
        # cou += 1
        # print(cou)
    results = {'t_arr': t_arr, 'x_t': x_t}
    return results









