import modeling_erGraph as md
import numpy as np
import networkx as nx
# import matplotlib.pyplot as plt
# import seaborn as sns

# if __name__ == '__main__':
#     # prob_arr = np.linspace(1, 0.01, 81)
#     prob_arr = np.linspace(0.99, 0.01, 81)
#     alpha_arr = np.linspace(0, 4, 81)
#     params = {'T': 2., 'N': 500, 'dt': 0.01, 'beta': 0.5, 'K': 1, 'a_val': 0.1}
#
#     avg_final_xi = np.zeros((len(alpha_arr), len(prob_arr)))
#     rounds = 0
#     for i in range(0, len(prob_arr)):
#         for j in range(0, len(alpha_arr)):
#             rounds += 1
#             avg_final_xi[i, j] = \
#                 md.calculate_final_x(md.models(params, alpha_arr[j], prob_arr[i], 'c'), params)
#             print(rounds)
#
#     abs_ver = avg_final_xi
#     np.save('avg_final_xi2.npy', avg_final_xi)
#     np.save('abs_ver2.npy', abs_ver)
#
#     plt.figure(dpi=400, figsize=(16, 9))
#     plt.xticks(fontsize=8, rotation=45)
#     plt.yticks(fontsize=8, rotation=45)
#     ax = sns.heatmap(avg_final_xi, yticklabels=prob_arr, xticklabels=alpha_arr)
#     ax.set_xticks(ax.get_xticks()[::5])
#     ax.set_xticklabels(alpha_arr[::5])
#     ax.set_yticks(ax.get_yticks()[::5])
#     ax.set_yticklabels(prob_arr[::5])
#     plt.ylabel("Connecting probability", fontsize=12)
#     plt.xlabel("Alpha", fontsize=12)
#     plt.show()

prob_arr = np.linspace(1, 0.01, 5)
alpha_arr = np.linspace(0, 4, 5)
params = {'T': 2., 'N': 500, 'dt': 0.01, 'beta': 0.5, 'K': 1, 'a_val': 0.1}
G_list = []
for pro in prob_arr:
    G = nx.fast_gnp_random_graph(params['N'], pro)
    while not (nx.is_connected(G)):
        G = nx.fast_gnp_random_graph(params['N'], pro)
    G_list.append(G)
# x0_list = []
# for pro in prob_arr:
#     temp = np.linspace(-1, 1, params['N'])
#     x0_list.append(temp)
x0 = np.linspace(-1, 1, params['N'])


def carry_out_er(prob_arr, alpha_arr, G_list, x0, params):
    abs_first = np.zeros((len(alpha_arr), len(prob_arr)))
    ave_first = np.zeros((len(alpha_arr), len(prob_arr)))
    for i in range(0, len(prob_arr)):
        for j in range(0, len(alpha_arr)):
            res = md.models(params, alpha_arr[j], prob_arr[i], 'c', G_list[i], x0)
            abs_first[i, j] = \
                md.calculate_final_x(res, params)
            ave_first[i, j] = \
                md.calculate_final_x2(res, params)
    results = [abs_first, ave_first]
    return results


def one_sim_er(it):
    print("IT ROUND %i" % it)

    results = carry_out_er(prob_arr, alpha_arr, G_list, x0, params)
    return results
