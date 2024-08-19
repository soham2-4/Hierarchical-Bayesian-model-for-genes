from poisson_beta.poisson_beta import PoissonBeta

if __name__ == "__main__":
    input_file = "data/data.txt"
    output_file = "result.txt"
    num_iterations = 1000

    pb = PoissonBeta(input_file, output_file, num_iterations)
    pb.run()