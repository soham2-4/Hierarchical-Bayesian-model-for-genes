import numpy as np
from .poisson_beta_slice_sample import slice_sample_gamma
from math import lgamma
from scipy.special import gammaln

def poisson_beta_update_koffi(a_param, c_param):
    num_gene = c_param["num_gene"]
    for i in range(num_gene):
        def logdist(x):
            return (
                -x / a_param["beta_koffi"][i] +
                (a_param["alpha_koffi"][i] - 1) * np.log(x) +
                np.sum(
                    lgamma(x + c_param["koni"][i]) -
                    lgamma(x) +
                    (x - 1) * np.log(c_param["pij"][i])
                )
            )
        c_param["koffi"][i] = slice_sample_gamma(logdist, c_param["koffi"][i], c_param["koffi"][i] / 2)
    return c_param["koffi"]