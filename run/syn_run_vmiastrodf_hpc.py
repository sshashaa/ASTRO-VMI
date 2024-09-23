"""
Generate .pickle fils in /experiments/outputs (figure 10 (communication costs=0) and 11 (communication costs=1000))
"""
import sys
import os.path as o
import os
sys.path.append(o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), ".."))) # type:ignore


from simopt.experiment_base import ProblemSolver, plot_area_scatterplots, post_normalize, plot_progress_curves, plot_solvability_cdfs, read_experiment_results, plot_solvability_profiles, plot_terminal_scatterplots, plot_terminal_progress

def main():
    communication_costs = 1000

    if communication_costs == 0: # figure 10
        solvers = ["VMI3-0-cv10", "ASTRODF-0", "NELDMDQ-0", "SPSAQ-0"]
        budget = 2500
    elif communication_costs == 1000: # figure 11
        solvers = ["VMI3-1000-cv10", "ASTRODF-1000", "NELDMDQ-1000", "SPSAQ-1000"]
        budget = 300000 

    all_sigma_version = [1,2,3,4]
    d = 2
    num_problems = len(all_sigma_version)

    initial_solution = (0, 0)

    # RUNNING AND POST-PROCESSING EXPERIMENTS
    M = 20
    L = 200

    for i in range(num_problems):
        model_fixed_factors = {"sigma_version": all_sigma_version[i], "dim": d}
        problem_fixed_factors = {"budget": budget, "initial_solution": initial_solution}
        problem_rename = f"SYN-1_sigma_version={all_sigma_version[i]}_dim={d}"

        experiments_same_problem = []
        for solver in solvers:
            solver_name = solver

            if solver == "VMI3-0-cv10":
                solver_name = "VMIASTRODF"
                solver_fixed_factors = {"overhead_burden": 0, "sampling_version": 3, "cv": 10}
            elif solver == "NELDMDQ-0":
                solver_name = "NELDMDQ"
                solver_fixed_factors = {"overhead_burden": 0}
            elif solver == "SPSAQ-0":
                solver_name = "SPSAQ"
                solver_fixed_factors = {"overhead_burden": 0}
            elif solver == "ASTRODF-0":
                solver_name = "VMIASTRODF"
                solver_fixed_factors = {"overhead_burden": 0, "sampling_version": 0}

            if solver == "VMI3-1000-cv10":
                solver_name = "VMIASTRODF"
                solver_fixed_factors = {"overhead_burden": 1000, "sampling_version": 3, "cv": 10}
            elif solver == "NELDMDQ-1000":
                solver_name = "NELDMDQ"
                solver_fixed_factors = {"overhead_burden": 1000}
            elif solver == "SPSAQ-1000":
                solver_name = "SPSAQ"
                solver_fixed_factors = {"overhead_burden": 1000}
            elif solver == "ASTRODF-1000":
                solver_name = "VMIASTRODF"
                solver_fixed_factors = {"overhead_burden": 1000, "sampling_version": 0}

            # Temporarily store experiments on the same problem for post-normalization.
            print(f"Testing solver {solver} on problem {problem_rename}.")

            # Specify file path name for storing experiment outputs in .pickle file.
            file_name_path = "experiments/outputs/" + solver + "_on_" + problem_rename + ".pickle"
            print(f"Results will be stored as {file_name_path}.")

            # Initialize an instance of the experiment class.
            myexperiment = ProblemSolver(solver_name=solver_name,
                                    solver_rename=solver,
                                    solver_fixed_factors=solver_fixed_factors,
                                    problem_name="SYN-1",
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