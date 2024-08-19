import numpy as np
from scipy.special import gammaln

def poisson_beta_log_posterior(read_count, a_param, c_param):
    log_posterior = (
        np.sum(read_count * (np.log(c_param["si"])[:, np.newaxis] + np.log(1 - c_param["pij"]))) +
        a_param["ln_size_factor_sum"] +
        np.sum(a_param["size_factor"] * (c_param["si"][:, np.newaxis] * (c_param["pij"] - 1))) -
        a_param["count_data_gammaln"]
    )

    log_posterior += np.sum(
        gammaln(c_param["koni"][:, np.newaxis] + c_param["koffi"][:, np.newaxis]) -
        gammaln(c_param["koni"][:, np.newaxis]) -
        gammaln(c_param["koffi"][:, np.newaxis]) +
        (c_param["koffi"][:, np.newaxis] - 1) * np.log(c_param["pij"]) +
        (c_param["koni"][:, np.newaxis] - 1) * np.log(1 - c_param["pij"])
    )

    log_posterior += np.sum(
        -c_param["si"] / a_param["beta_si"] +
        (a_param["alpha_si"] - 1) * np.log(c_param["si"]) -
        a_param["alpha_si"] * np.log(a_param["beta_si"]) -
        gammaln(a_param["alpha_si"])
    )

    log_posterior += np.sum(
        -c_param["koni"] / a_param["beta_koni"] +
        (a_param["alpha_koni"] - 1) * np.log(c_param["koni"]) -
        a_param["alpha_koni"] * np.log(a_param["beta_koni"]) -
        gammaln(a_param["alpha_koni"])
    )

    log_posterior += np.sum(
        -c_param["koffi"] / a_param["beta_koffi"] +
        (a_param["alpha_koffi"] - 1) * np.log(c_param["koffi"]) -
        a_param["alpha_koffi"] * np.log(a_param["beta_koffi"]) -
        gammaln(a_param["alpha_koffi"])
    )

    return log_posterior