from multiprocessing import Pool
import numpy as np
import carry_out_erGraph as coer
import carry_out_SC as cosc

if __name__ == '__main__':
    n_processes = 10
    n_simulations = 10

    iter_rounds = range(0, n_simulations)
    pool = Pool(n_processes)

    # ER
    # results = pool.map(coer.one_sim_er, iter_rounds)
    # np.save('er_heatmap.npy', results)

    # SC one time
    # results = pool.map(cosc.one_sim_sc, iter_rounds)
    # np.save('one_sc.npy', results)

    # SC heatmap
    # results = pool.map(cosc.one_heatmap_sc, iter_rounds)
    # np.save('sc_heatmap.npy', results)
    # pool.close()

    for i in range(n_simulations):
        results = cosc.carry_out_sc(cosc.k1_arr, cosc.k2_arr, cosc.alpha_arr, cosc.params,
                                    cosc.G_list, cosc.triangle_lists, cosc.x_0)
        fn = 'sc_heatmap' + str(i) + '.npy'
        np.save(fn, results)
