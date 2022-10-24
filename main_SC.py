import ho_polarization as hop
import numpy as np
import carry_out_SC as co
if __name__ == '__main__':
    # N = 180
    # k1 = 100
    # k2 = 25

    sigma_mark = ['1', '2', '3']
    params = {'T': 5., 'N': 180, 'dt': 0.01, 'beta': 1, 'alpha1': 3, 'alpha2': 3, 'a_val1': 0.1,
              'a_val2': 0.05, 'k1': 100, 'k2': 25, 'mark': 'c'}
    params['x0'] = np.linspace(-1, 1, params['N'])
    results = co.run_one_sc(params)

    hop.plotting(results[0], params)
    hop.plotting(results[1], params)
    hop.plotting(results[2], params)
