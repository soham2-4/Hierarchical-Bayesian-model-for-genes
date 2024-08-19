import numpy as np
from scipy.special import gammaln

def poisson_beta_init(read_count, size_factor, transcript_length, num_gene, num_cell):
    a_param = {
        "size_factor": np.outer(transcript_length, size_factor),
        "alpha_si": np.ones(num_gene),
        "beta_si": np.max(read_count / np.outer(transcript_length, size_factor), axis=1),
        "alpha_koni": np.ones(num_gene),
        "beta_koni": 100 * np.ones(num_gene),
        "alpha_koffi": np.ones(num_gene),
        "beta_koffi": 100 * np.ones(num_gene),
        "count_data_gammaln": gammaln(read_count + 1).sum(),
        "count_data_row_gammaln": gammaln(read_count + 1).sum(axis=1),
        "ln_size_factor": np.log(np.outer(transcript_length, size_factor)),
        "ln_size_factor_sum": (read_count * np.log(np.outer(transcript_length, size_factor))).sum(),
        "count_ln_size_factor": (read_count * np.log(np.outer(transcript_length, size_factor))).sum(axis=1)
    }

    c_param = {
        "num_gene": num_gene,
        "num_cell": num_cell,
        "si": np.mean(read_count / a_param["size_factor"]) * np.ones(num_gene),
        "koni": np.random.rand(num_gene),
        "koffi": np.random.rand(num_gene),
        "pij": 0.5 * np.ones((num_gene, num_cell))
    }

    for i in range(num_gene):
        x = read_count[i]
        e1 = np.mean(x)
        e2 = np.sum(x * (x - 1)) / x.size
        e3 = np.sum(x * (x - 1) * (x - 2)) / x.size
        print("The value of x is:", x)
        print("The value of e1, e2, e3 is:", e1, e2, e3)
        try:
            r1, r2, r3 = e1, e2 / e1, e3 / e2
        except:
            print("ZeroDivisionError encountered. The value of x is:", x)
            print("The value of e1, e2, e3 is:", e1, e2, e3)
            print("The value of read count is", read_count)
        kon_hat = 2 * r1 * (r3 - r2) / (r1 * r2 - 2 * r1 * r3 + r2 * r3)
        koff_hat = 2 * (r2 - r1) * (r1 - r3) * (r3 - r2) / ((r1 * r2 - 2 * r1 * r3 + r2 * r3) * (r1 - 2 * r2 + r3))
        s_hat = (-r1 * r2 + 2 * r1 * r3 - r2 * r3) / (r1 - 2 * r2 + r3)
        s_hat /= (transcript_length[i] * np.mean(size_factor))
        print("the value of konhat, koffhat, and shat is", kon_hat, koff_hat, s_hat)
        if s_hat > 0 and kon_hat > 0 and koff_hat > 0:
            print("entering if condition")
            c_param["si"][i] = s_hat
            c_param["koni"][i] = kon_hat
            c_param["koffi"][i] = koff_hat
    return c_param, a_param