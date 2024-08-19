import numpy as np
from .poisson_beta_slice_sample import slice_sample_gamma

def poisson_beta_update_si(sum_count, a_param, c_param):
    num_gene = c_param["num_gene"]
    for i in range(num_gene):
        def logdist(x):
            sum_pij = np.sum(a_param["size_factor"][i] * (c_param["pij"][i] - 1))
            sum_x = sum_count[i]
            return (
                -x / a_param["beta_si"][i] +
                (a_param["alpha_si"][i] - 1) * np.log(x) +
                sum_x * np.log(x) +
                x * sum_pij
            )
        c_param["si"][i] = slice_sample_gamma(logdist, c_param["si"][i], c_param["si"][i] / 2)
    return c_param["si"]