import sys
import os.path as o

sys.path.append(o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), "..")))

# Import the Experiment class and other useful functions
from simopt.experiment_base import read_experiment_results, post_normalize, plot_progress_curves, plot_solvability_cdfs, plot_solvability_profiles

m = 20 # Macro-replication
L = 200 # Post-replication

solvers = ["VMI1-1000", "VMI2-1000", "VMI3-1000-cv10"] 

problem_name = "SYNVMI-1"

all_sigma_version = [1,2,3,4]
d = 2
num_problems = len(all_sigma_version)


for i in range(num_problems):
    model_fixed_factors = {"sigma_version": all_sigma_version[i], "dim": d}
    problem_rename = f"SYNVMI-1_sigma_version={all_sigma_version[i]}_dim={d}"

    experiments_same_problem = []
    for solver in solvers:
        solver_name = solver

        # Temporarily store experiments on the same problem for post-normalization.
        file_name = f"{solver}_on_{problem_rename}"
        myexperiment = read_experiment_results(f"experiments/outputs/{file_name}.pickle")
        experiments_same_problem.append(myexperiment)

    # Find an optimal solution x* for normalization.
    post_normalize(experiments=experiments_same_problem, n_postreps_init_opt=L)

myexperiment = []
ind_experiment = []
n = len(solvers)

for solver in solvers:
    experiments_same_solver = []
    solver_name = solver
    if solver == "VMI3-1000-cv10":
        solver_name = "ASTRO-DF-VM3"
    elif solver == "VMI2-1000":
        solver_name = "ASTRO-DF-VM2"
    elif solver == "VMI1-1000":
        solver_name = "ASTRO-DF-VM1"

    
    for i in range(num_problems):
        problem_rename = f"SYNVMI-1_sigma_version={all_sigma_version[i]}_dim={d}"
        file_name = f"{solver}_on_{problem_rename}"
        # Load experiment.
        new_experiment = read_experiment_results(f"experiments/outputs/{file_name}.pickle")
        # Rename problem to produce nicer plot labels.
        new_experiment.problem.name = f"SYN-1_sigma_version={all_sigma_version[i]}_dim={d}"
        new_experiment.solver.name = solver_name
        experiments_same_solver.append(new_experiment)

    myexperiment.append(experiments_same_solver)


n_solvers = len(myexperiment)
n_problems = len(myexperiment[0])
print("Plotting results.")

plot_solvability_profiles(myexperiment, plot_type="cdf_solvability", solve_tol=0.001, all_in_one=True, plot_CIs=True, print_max_hw=False)
    
# Plots will be saved in the folder experiments/plots.
print("Finished. Plots can be found in experiments/plots folder.")
