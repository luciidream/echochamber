import polarization_model2 as pm2
import numpy as np
import sc_gen as scg
import ho_polarization as hop


def models_sc(params, k1, k2, alpha1, alpha2, mark, sigma_mark, graph=None, triangle_list=None, x_0=None):
    params['p1'], params['p2'] = scg.get_p1_and_p2(k1, k2, params['N'])
    params['alpha1'], params['alpha2'] = alpha1, alpha2
    if (graph is None) and (triangle_list is None):
        G, node_neighbors_dict, node_triangles_dict, triangles_list = \
            scg.generate_sc(params['N'], params['p1'], params['p2'])
    else:
        G = graph
        triangles_list = triangle_list
    centrality_dict = pm2.calculate_centrality(G, mark)
    params['centrality1'] = []
    for val in centrality_dict.values():
        params['centrality1'].append(val)
    params['centrality2'] = hop.calculate_triangle_centrality(triangles_list, params['centrality1'])
    if x_0 is None:
        x0 = np.linspace(-1, 1, params['N'])
    else:
        x0 = x_0
    results = hop.simulating_models_with_sc(params, G, x0, triangles_list, sigma_mark)
    return results
