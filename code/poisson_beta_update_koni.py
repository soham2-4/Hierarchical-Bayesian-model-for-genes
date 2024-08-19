import numpy as np
from .poisson_beta_slice_sample import slice_sample_gamma
from scipy.special import gammaln
from math import lgamma

def poisson_beta_update_koni(a_param, c_param):
    num_gene = c_param["num_gene"]
    for i in range(num_gene):
        def logdist(x):
            return (
                -x / a_param["beta_koni"][i] +
                (a_param["alpha_koni"][i] - 1) * np.log(x) +
                np.sum(
                    lgamma(x + c_param["koffi"][i]) - lgamma(x) +
                    (x - 1) * np.log(1 - c_param["pij"][i])
                )
            )
        c_param["koni"][i] = slice_sample_gamma(logdist, c_param["koni"][i], c_param["koni"][i] / 2)
    return c_param["koni"]
