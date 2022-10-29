import numpy as np
import carry_out_SC as cosc
import ho_polarization as hop


def get_dict(data_co, ind, rounds):
    result = {}
    for dic in data_co[:, ind]:
        if 't_arr' not in result.keys():
            result['t_arr'] = dic['t_arr']
        if 'x_t' not in result.keys():
            result['x_t'] = dic['x_t']
        else:
            temp = result['x_t']
            result['x_t'] = dic['x_t'] + temp
    result['x_t'] = result['x_t'] / rounds
    return result


if __name__ == '__main__':
    data_collection = np.load('one_sc.npy', allow_pickle=True)
    params = cosc.params
    result1 = get_dict(data_collection, 0, 10)
    result2 = get_dict(data_collection, 1, 10)
    result3 = get_dict(data_collection, 2, 10)
    result4 = {'t_arr': result1['t_arr'], 'x_t': result1['x_t'] - result3['x_t']}
    result5 = {'t_arr': result1['t_arr'], 'x_t': result3['x_t'] - result1['x_t']}

    # hop.plotting(result1, params, '1')
    # hop.plotting(result2, params, '2')
    # hop.plotting(result3, params, '3')
    # hop.plotting(result4, params, '4')
    hop.plotting(result5, params, '5')




