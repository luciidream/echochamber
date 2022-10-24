import numpy as np
import polarization_model2 as pm2
import networkx as nx
import itertools as it
import matplotlib.pyplot as plt
import seaborn as sns


def active_triangles(triangles_list, a2):
    tri_count = len(triangles_list)
    return np.where(np.random.uniform(0, 1, size=tri_count) < a2)[0]


def calculate_triangle_centrality(triangle_list, centrality1):
    centrality2 = []
    for tri in triangle_list:
        tmp = 0
        for t in tri:
            tmp += centrality1[t]
        centrality2.append(tmp / 3)
    return centrality2


def modify_triangle_matrix(triangle_list, A, a2, N):
    A_t = np.zeros((len(triangle_list), N))
    active_tris = active_triangles(triangle_list, a2)
    for i in active_tris:
        for t in triangle_list[i]:
            A_t[i, t] = 1
        # for c in it.permutations(list(triangle_list[i]), 2):
        #     A[np.array(c, dtype=int)] = 1
    return A_t, A


def sigma_inputs_with_triangles(A, A_t, x, alpha1, alpha2, centrality1, centrality2, triangle_list):
    Ax = A * x
    t, n = A_t.shape
    # A_tx = A_t * x
    # x_tri = []
    # for t in range(0, len(triangle_list)):
    #     temp = 0
    #     for ind in triangle_list[t]:
    #         temp += x[ind]
    #     x_tri.append(temp / 3)
    # A_tx = np.transpose(A_t) * x_tri
    X_T = np.zeros((t, n))
    for i in range(0, t):
        for ind in triangle_list[i]:
            temp = list(triangle_list[i])
            temp.remove(ind)
            temp = np.array(temp, dtype=int)
            if x[temp[0]] * x[temp[1]] > 0:
                X_T[i, ind] = np.average([x[temp[0]], x[temp[1]]])
            else:
                X_T[i, ind] = 0
    A_tx = np.transpose(A_t * X_T)
    pairwise_summation = np.sum(centrality1 * pm2.sigmoidal_func(alpha1 * Ax), axis=1)
    triangle_summation = np.sum(np.transpose(centrality2 * pm2.sigmoidal_func(alpha2 * A_tx)), axis=0)

    return pairwise_summation, triangle_summation


def simulating_models_with_sc(params, G, x0, triangles_list, mark):

    N = params['N']
    dt = params['dt']
    T = params['T']
    alpha1 = params['alpha1']
    alpha2 = params['alpha2']
    a_val1 = params['a_val1']
    a_val2 = params['a_val2']
    beta = params['beta']
    centrality1 = params['centrality1']
    centrality2 = params['centrality2']

    largest_cc = max(nx.connected_components(G), key=len)
    lcc = np.array(list(largest_cc))

    timestep = int(T / dt) + 1
    t_arr = np.linspace(0, T, timestep)

    x_t = np.zeros((N, int(timestep)))
    x = x0

    a1 = np.ones(N) * a_val1
    a2 = np.ones(len(triangles_list)) * a_val2

    # cou = 0
    for t in range(timestep):
        # cou += 1
        x_t[:, t] = x
        A = pm2.modify_matrix(x, a1, beta, N, G, lcc)
        A_t, A = modify_triangle_matrix(triangles_list, A, a2, N)
        # only pairwise interaction
        sigma1 = sigma_inputs_with_triangles(A, A_t, x, alpha1, alpha2, centrality1, centrality2, triangles_list)[0]
        sigma2 = sigma_inputs_with_triangles(A, A_t, x, alpha1, alpha2, centrality1, centrality2, triangles_list)[1]
        if mark == '1':
            sigma = sigma1
        # only triangle interaction
        if mark == '2':
            sigma = sigma2
        if mark == '3':
            sigma = sigma1 + sigma2
        x = pm2.integration_step(pm2.f_activity, dt, sigma, x)

        # print(cou)
    results = {'t_arr': t_arr, 'x_t': x_t}
    return results


def plotting(results, params):

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
    str2 = 'alpha1=' + str(params['alpha1'])
    str3 = 'alpha2=' + str(params['alpha2'])
    str4 = 'N=' + str(params['N'])
    str5 = 'p1=' + str(params['k1'])
    str6 = 'p2=' + str(params['k2'])

    plt.legend([str1, str2, str3, str4, str5, str6])
    plt.show()


