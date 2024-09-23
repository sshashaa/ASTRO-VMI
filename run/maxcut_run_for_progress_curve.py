"""
Generate .pickle fils in /experiments/outputs (figure 13a)
"""
import sys
import os.path as o
import os
sys.path.append(o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), ".."))) # type:ignore

from simopt.experiment_base import ProblemSolver, plot_area_scatterplots, post_normalize, plot_progress_curves, plot_solvability_cdfs, read_experiment_results, plot_solvability_profiles, plot_terminal_scatterplots, plot_terminal_progress

def main():
    solvers = ["VMI3IT-cv10", "ASTRODFIT"]
    budget = 7000
    theta = (1.6, 1.6)

    # RUNNING AND POST-PROCESSING EXPERIMENTS
    M = 20
    L = 200
    model_fixed_factors = {"theta": theta}
    problem_fixed_factors = {"budget": budget, "initial_solution": theta}
    problem_rename = f"MAXCUT-1"

    # Temporarily store experiments on the same problem for post-normalization.
    experiments_same_problem = []
    solver_fixed_factors = {}

    for solver in solvers:
        solver_name = solver

        if solver == "VMI3IT-cv10":
            solver_name = "VMIASTRODF"
            solver_fixed_factors = {"overhead_burden": 0, "sampling_version": 3, "cv": 10}
        elif solver == "ASTRODFIT":
            solver_name = "VMIASTRODF"
            solver_fixed_factors = {"overhead_burden": 0, "sampling_version": 0}

        # Temporarily store experiments on the same problem for post-normalization.
        print(f"Testing solver {solver} on problem {problem_rename}.")

        # Specify file path name for storing experiment outputs in .pickle file.
        file_name_path = "experiments/outputs/" + solver + "_on_" + problem_rename + ".pickle"
        print(f"Results will be stored as {file_name_path}.")

        # Initialize an instance of the experiment class.
        myexperiment = ProblemSolver(solver_name=solver_name,
                                solver_rename=solver,
                                solver_fixed_factors=solver_fixed_factors,
                                problem_name="MAXCUT-1",
                                problem_rename=problem_rename,
                                problem_fixed_factors=problem_fixed_factors,
                                model_fixed_factors=model_fixed_factors)

        # Run a fixed number of macroreplications of the solver on the problem.
        myexperiment.run(n_macroreps=M)

        print("Post-processing results.")

        # Run a fixed number of postreplications at all recommended solutions.
        myexperiment.post_replicate(n_postreps=L)
        experiments_same_problem.append(myexperiment)

    # Find an optimal solution x* for normalization.
    post_normalize(experiments=experiments_same_problem, n_postreps_init_opt=L)

if (__name__ == "__main__"):
    main()