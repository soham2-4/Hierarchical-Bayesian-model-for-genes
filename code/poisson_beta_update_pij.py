import numpy as np
from .poisson_beta_slice_sample import slice_sample_beta

def poisson_beta_update_pij(read_count, c_param, a_param):
    num_gene, num_cell = read_count.shape
    for i in range(num_gene):
        for j in range(num_cell):
            def logdist(x):
                return (
                    (c_param["koffi"][i] - 1) * np.log(x) +
                    (c_param["koni"][i] - 1) * np.log(1 - x) +
                    np.log(1 - x) * read_count[i, j] +
                    a_param["size_factor"][i, j] * (c_param["si"][i] * (x - 1))
                )
            c_param["pij"][i, j] = slice_sample_beta(logdist, c_param["pij"][i, j], c_param["pij"][i, j] / 2)
    return c_param["pij"]