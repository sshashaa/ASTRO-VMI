import sys
import os.path as o

sys.path.append(o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), "..")))

# Import the Experiment class and other useful functions
from simopt.experiment_base import read_experiment_results, post_normalize, plot_solvability_profiles

m = 20 # Macro-replication
L = 200 # Post-replication

solvers = ["VMI3-0-cv10", "ASTRODFPF-1", "ASTRODFPF-10"] 

problem_name = "MAXCUT-1"

p = 1

all_edges = [[[0,1],[1,2],[0,2]],
            [[0,3],[0,4],[1,3],[2,4]],
            [[0,1],[1,2],[0,2],[0,3]],
            [[0,1],[0,2],[0,3],[0,4]],
            [[0,3],[1,3],[1,2],[0,2]],
            [[0,3],[0,4],[1,3],[1,4],[1,2],[2,4]],
            [[0,3],[0,4],[1,3],[1,4],[1,2],[0,2]], 
            [[2,4],[2,1],[3,4],[3,1],[0,2]],
            [[2,4],[2,3],[3,4],[3,1],[0,2]],
            [[0,1],[1,3],[1,4],[1,5],[2,4],[2,5]],
            [[0,3],[1,5],[2,3],[2,4],[2,5],[3,4]],
            [[0,1],[0,2],[1,4],[2,3],[2,5],[3,5]]]


experiments_same_problem = []


num_problems = len(all_edges)

for i in range(num_problems):
    problem_rename = f"MAXCUT-1_edges={all_edges[i]}_p={p}"

    # Temporarily store experiments on the same problem for post-normalization.
    experiments_same_problem = []
    solver_fixed_factors = {}

    for solver in solvers:
        solver_name = solver
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
    if solver == "VMI3-0-cv10":
        solver_name = "ASTRO-DF-VM3"
    elif solver == "ASTRODFPF-1":
        solver_name = "ASTRO-DF with regularized function (c_p = 1)"
    elif solver == "ASTRODFPF-10":
        solver_name = "ASTRO-DF with regularized function (c_p = 10)"

    for i in range(num_problems):
        problem_rename = f"MAXCUT-1_edges={all_edges[i]}_p={p}"
        file_name = f"{solver}_on_{problem_rename}"
        # Load experiment.
        new_experiment = read_experiment_results(f"experiments/outputs/{file_name}.pickle")
        # Rename problem to produce nicer plot labels.
        new_experiment.problem.name = f"MAXCUT-1 with edges={all_edges[i]}"
        new_experiment.solver.name = solver_name
        experiments_same_solver.append(new_experiment)

    myexperiment.append(experiments_same_solver)

n_solvers = len(myexperiment)
n_problems = len(myexperiment[0])

print("Plotting results.")

plot_solvability_profiles(myexperiment, plot_type="cdf_solvability", solve_tol=0.1, all_in_one=True, plot_CIs=True, print_max_hw=False)

# Plots will be saved in the folder experiments/plots.
print("Finished. Plots can be found in experiments/plots folder.")