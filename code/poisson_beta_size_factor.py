import numpy as np
from scipy.stats import gmean


def poisson_beta_size_factor(read_count):
    nonzero_gene = np.sum(np.log(read_count), axis=1) != -np.inf
    print(nonzero_gene)
    # normalized_read_count = read_count[nonzero_gene] / gmean(read_count[nonzero_gene], axis=0)
    normalized_read_count = read_count[nonzero_gene]
    row_gmean = gmean(normalized_read_count, axis=1)
    row_gmean_reshaped = row_gmean.reshape(-1, 1)
    print(row_gmean_reshaped)
    # divide each entry by the geometric mean of it's row
    normalized_read_count = normalized_read_count / row_gmean_reshaped
    print(normalized_read_count)
    size_factor = np.zeros(read_count.shape[1])
    print("size factor", size_factor.shape)
    for j in range(read_count.shape[1]):
        size_factor[j] = np.median(normalized_read_count[normalized_read_count[:, j] != 0, j])
    print(size_factor)
    return size_factor
