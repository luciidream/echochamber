import numpy as np
import carry_out_SC as cosc
import ho_polarization as hop

if __name__ == '__main__':
    data_collection = np.load('one_sc.npy', allow_pickle=True)
    params = cosc.params


