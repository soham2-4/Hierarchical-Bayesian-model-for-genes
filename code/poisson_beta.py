import numpy as np
import pandas as pd
from .poisson_beta_init import poisson_beta_init
from .poisson_beta_size_factor import poisson_beta_size_factor
from .poisson_beta_update_pij import poisson_beta_update_pij
from .poisson_beta_update_si import poisson_beta_update_si
from .poisson_beta_update_koni import poisson_beta_update_koni
from .poisson_beta_update_koffi import poisson_beta_update_koffi
from .poisson_beta_log_posterior import poisson_beta_log_posterior

class PoissonBeta:
    def __init__(self, input_file, output_file, num_iterations):
        self.input_file = input_file
        self.output_file = output_file
        self.num_iterations = num_iterations

    def run(self):
        # Read input data
        data = np.genfromtxt(self.input_file, delimiter="\t", skip_header=1, dtype=None, encoding=None, unpack=True)
        # convert to dataframe (handle last column which has true and false)
        gene_names = data[0].astype(str)
        transcript_length = data[1].astype(float)
        read_count = data[2:]
        print("read_count", read_count)
        array_2d = np.array(read_count)
        transposed_array = array_2d.T
        read_count = transposed_array
        #only take those rows where atleast one value is non zero
        expressed_index = np.sum(read_count, axis=1) != 0 
        read_count_expressed = read_count[expressed_index]
        print("read_count_expressed", read_count_expressed)

        # Initialize model parameters
        size_factor = poisson_beta_size_factor(read_count_expressed)
        num_gene, num_cell = read_count_expressed.shape
        c_param, a_param = poisson_beta_init(read_count_expressed, size_factor, transcript_length[expressed_index], num_gene, num_cell)

        # Run Gibbs sampling
        burn_in = self.num_iterations // 2
        samples_pij = np.zeros((num_gene, num_cell))
        samples_si = np.zeros((num_gene, self.num_iterations - burn_in))
        samples_koni = np.zeros((num_gene, self.num_iterations - burn_in))
        samples_koffi = np.zeros((num_gene, self.num_iterations - burn_in))
        log_posterior = np.zeros(self.num_iterations)

        for t in range(self.num_iterations):
            c_param["pij"] = poisson_beta_update_pij(read_count_expressed, c_param, a_param)
            c_param["si"] = poisson_beta_update_si(read_count_expressed.sum(axis=1), a_param, c_param)
            c_param["koni"] = poisson_beta_update_koni(a_param, c_param)
            c_param["koffi"] = poisson_beta_update_koffi(a_param, c_param)
            log_posterior[t] = poisson_beta_log_posterior(read_count_expressed, a_param, c_param)
            print(f"Poisson Beta Gibbs Sampling Iteration\t {t+1}/{self.num_iterations}\t {log_posterior[t]}")

            if t >= burn_in:
                samples_pij += c_param["pij"]
                samples_si[:, t - burn_in] = c_param["si"]
                samples_koni[:, t - burn_in] = c_param["koni"]
                samples_koffi[:, t - burn_in] = c_param["koffi"]

        samples_pij /= (self.num_iterations - burn_in)

        # Write output
        with open(self.output_file, "w") as f:
            f.write("Gene\tLength\tSi\tKoni\tKoffi\tSKoffi\tExi\t")
            f.write("\t".join(f"Pij(Cell{j+1})" for j in range(num_cell)))
            f.write("\n")

            for i in range(num_gene):
                f.write(f"{gene_names[i]}\t{transcript_length[i]}\t{samples_si[i].mean()}\t{samples_koni[i].mean()}\t{samples_koffi[i].mean()}\t")
                f.write(f"{samples_si[i].mean() / samples_koffi[i].mean()}\t")
                f.write(f"{samples_si[i].mean() * (samples_koni[i].mean() / (samples_koffi[i].mean() + samples_koni[i].mean()))}\t")
                f.write("\t".join(str(samples_pij[i, j]) for j in range(num_cell)))
                f.write("\n")