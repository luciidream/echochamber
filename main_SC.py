import ho_polarization as hop
import numpy as np
import carry_out_SC as co
import sc_gen as scg
import polarization_model2 as pm2

if __name__ == '__main__':
    # N = 180
    # k1 = 100
    # k2 = 25

    sigma_mark = ['1', '2', '3']
    params = {'T': 5., 'N': 180, 'dt': 0.01, 'beta': 1, 'alpha1': 3, 'alpha2': 3, 'a_val1': 0.1,
              'a_val2': 0.05, 'k1': 175, 'k2': 25, 'mark': 'c'}
    p1, p2 = scg.get_p1_and_p2(params['k1'], params['k2'], params['N'])
    params['x0'] = np.linspace(-1, 1, params['N'])
    G, node_neighbors_dict, node_triangles_dict, triangles_list = scg.generate_sc(params['N'], p1, p2)
    centrality_dict = pm2.calculate_centrality(G, params['mark'])
    params['centrality1'] = []
    for val in centrality_dict.values():
        params['centrality1'].append(val)
    params['centrality2'] = hop.calculate_triangle_centrality(triangles_list, params['centrality1'])
    results = co.run_one_sc(params, G, triangles_list)

    hop.plotting(results[0], params)
    hop.plotting(results[1], params)
    hop.plotting(results[2], params)
