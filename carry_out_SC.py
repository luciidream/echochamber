import sc_gen as scg
import ho_polarization as hop
import polarization_model2 as pm2
import numpy as np
import modeling_SC as md2
import modeling_erGraph as md1

k1_arr = np.linspace(30, 140, 12)
k2_arr = np.linspace(2, 10, 5)
alpha_arr = np.linspace(0, 4, 11)
params = {'T': 5., 'N': 150, 'dt': 0.01, 'beta': 1, 'alpha1': 3, 'alpha2': 3,
          'a_val1': 0.1, 'a_val2': 0.05, 'k1': 100, 'k2': 25, 'mark': 'c'}
params['x0'] = np.linspace(-1, 1, params['N'])
x_0 = np.linspace(-1, 1, params['N'])
p1, p2 = scg.get_p1_and_p2(params['k1'], params['k2'], params['N'])
G, node_neighbors_dict, node_triangles_dict, triangles_list = scg.generate_sc(params['N'], p1, p2)
centrality_dict = pm2.calculate_centrality(G, params['mark'])
params['centrality1'] = []
for val in centrality_dict.values():
    params['centrality1'].append(val)
params['centrality2'] = hop.calculate_triangle_centrality(triangles_list, params['centrality1'])
G_list = []
triangle_lists = []
for p in range(len(k1_arr)):
    temp1 = []
    temp2 = []
    for q in range(len(k2_arr)):
        G, node_neighbors_dict, node_triangles_dict, triangles_list = scg.generate_sc(params['N'], k1_arr[p], k2_arr[q])
        temp1.append(G)
        temp2.append(triangles_list)

    G_list.append(temp1)
    triangle_lists.append(temp2)


def run_one_sc(params, G, triangles_list):
    sigma_mark = ['1', '2', '3']
    x0 = params['x0']
    result1 = hop.simulating_models_with_sc(params, G, x0, triangles_list, sigma_mark[0])
    result2 = hop.simulating_models_with_sc(params, G, x0, triangles_list, sigma_mark[1])
    result3 = hop.simulating_models_with_sc(params, G, x0, triangles_list, sigma_mark[2])
    return result1, result2, result3


def carry_out_sc(k1_arr, k2_arr, alpha_arr, params, G_list, triangle_lists, x0):
    abs_first_cube = np.zeros((len(k1_arr), len(k2_arr), len(alpha_arr)))
    ave_first_cube = np.zeros((len(k1_arr), len(k2_arr), len(alpha_arr)))
    for i in range(0, len(k1_arr)):
        for j in range(0, len(k2_arr)):
            for k in range(0, len(alpha_arr)):
                temp = md2.models_sc(params, k1_arr[i], k2_arr[j], alpha_arr[k], alpha_arr[k], params['mark'],
                                     G_list[i][j], triangle_lists[i][j], x0)

                abs_first_cube[(i, j, k)] = md1.calculate_final_x(temp, params)
                ave_first_cube[(i, j, k)] = md1.calculate_final_x2(temp, params)

    cubes = [abs_first_cube, ave_first_cube]
    return cubes


def one_heatmap_sc(it):
    print("IT ROUND %i" % it)

    results = carry_out_sc(k1_arr, k2_arr, alpha_arr, params, G_list, triangle_lists, x_0)
    return results


def one_sim_sc(it):
    print("IT ROUND %i" % it)

    results = run_one_sc(params, G, triangles_list)
    return results





