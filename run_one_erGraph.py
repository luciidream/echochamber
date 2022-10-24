import modeling_erGraph as md
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
    prob_arr = np.linspace(1, 0.01, 51)
    # prob_arr = np.linspace(0.99, 0.01, 21)
    alpha_arr = np.linspace(0, 4, 51)
    params = {'T': 2., 'N': 500, 'dt': 0.01, 'beta': 0.5, 'K': 1, 'a_val': 0.1}

    abs_first = np.zeros((len(alpha_arr), len(prob_arr)))
    ave_first = np.zeros((len(alpha_arr), len(prob_arr)))
    rounds = 0
    for i in range(0, len(prob_arr)):
        for j in range(0, len(alpha_arr)):
            rounds += 1
            temp = md.models(params, alpha_arr[j], prob_arr[i], 'c')
            abs_first[i, j] = \
                md.calculate_final_x(temp, params)
            ave_first[i, j] = \
                md.calculate_final_x2(temp, params)
            print(rounds)

    final_ver = abs_first - ave_first
    # np.save('avg_final_xi2.npy', avg_final_xi)
    # np.save('abs_ver2.npy', abs_ver)

    plt.figure(dpi=400, figsize=(16, 9))
    plt.xticks(fontsize=8, rotation=45)
    plt.yticks(fontsize=8, rotation=45)
    ax = sns.heatmap(final_ver, yticklabels=prob_arr, xticklabels=alpha_arr)
    ax.set_xticks(ax.get_xticks()[::5])
    ax.set_xticklabels(alpha_arr[::5])
    ax.set_yticks(ax.get_yticks()[::5])
    ax.set_yticklabels(prob_arr[::5])
    plt.ylabel("Connecting probability", fontsize=12)
    plt.xlabel("Alpha", fontsize=12)
    plt.show()
