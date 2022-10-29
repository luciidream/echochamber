import numpy as np
import matplotlib.pyplot as plt
import modeling_SC as md2
import modeling_erGraph as md1
# from matplotlib import cm
import seaborn as sns

if __name__ == '__main__':

    N = 150
    k1_arr = np.linspace(30, 140, 12)
    k2_arr = np.linspace(2, 12, 6)
    alpha_arr = np.linspace(0, 4, 11)
    mark = 'c'
    sigma_mark = '3'
    res_cube = np.zeros((len(k1_arr), len(k2_arr), len(alpha_arr)))

    params = {'T': 1., 'N': N, 'dt': 0.01, 'beta': 0.5, 'a_val1': 0.1,
              'a_val2': 0.05}

    rounds = 0

    for i in range(0, len(k1_arr)):
        for j in range(0, len(k2_arr)):
            for k in range(0, len(alpha_arr)):
                rounds += 1
                res_cube[(i, j, k)] = \
                    md1.calculate_final_x(md2.models_sc(params, k1_arr[i], k2_arr[j],
                                                        alpha_arr[k], alpha_arr[k], mark, sigma_mark='3'), params)
                print(rounds, res_cube[(i, j, k)])

    np.save('res_cube.npy', res_cube)
    # trial = np.random.randint(0, 10, size=(10, 10, 9))
    K1, K2, alphas = np.meshgrid(k1_arr, k2_arr, alpha_arr)
    sns.set_theme()
    fig = plt.figure(dpi=400, figsize=(16, 9))
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Pairwise <k1>')
    ax.set_ylabel('2-simplex <k2>')
    ax.set_zlabel('Alpha')
    hm = ax.scatter3D(K1, K2, alphas, c=res_cube, alpha=0.5, marker='.', s=100)
    fig.colorbar(hm)
    plt.show()
