import sys
import os.path as o

sys.path.append(o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), "..")))

# Import the Experiment class and other useful functions
from simopt.experiment_base_log_flat import ProblemSolver, plot_area_scatterplots, post_normalize, plot_progress_curves, plot_solvability_cdfs, read_experiment_results, plot_solvability_profiles, plot_terminal_scatterplots, plot_terminal_progress

def main():
    m = 20 # Macro-replication
    L = 200 # Post-replication

    solvers = ["ASTRODF2M", "ASTRODF1M", "NELDMDQ"]

    budget = 2000
    all_solutions = [(-5,-5), (0,0), (-2,-2), (3,-3), (-3,-3), (-2,3)]

    num_problems = len(all_solutions)

    for i in range(num_problems):
        model_fixed_factors = {"sigma_version": 1, "dim": 2}
        problem_fixed_factors = {"initial_solution": all_solutions[i], "budget": budget}
        problem_rename = f"SYNTWOMODEL-1_solution={all_solutions[i]}"

        # Temporarily store experiments on the same problem for post-normalization.
        experiments_same_problem = []
        solver_fixed_factors = {}

        for solver in solvers:
            solver_name = solver
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
            myexperiment.run(n_macroreps=m)

            print("Post-processing results.")

            # Run a fixed number of postreplications at all recommended solutions.
            myexperiment.post_replicate(n_postreps=L)
            experiments_same_problem.append(myexperiment)

        # Find an optimal solution x* for normalization.
        post_normalize(experiments=experiments_same_problem, n_postreps_init_opt=L)

    myexperiment = []
    n = len(solvers)

    for solver in solvers:
        experiments_same_solver = []
        solver_name = solver
        if solver == "ASTRODF2M":
            solver_name = "ASTRO-DF-1Model"
        elif solver == "ASTRODF1M":
            solver_name = "ASTRO-DF-2Model"
        elif solver == "NELDMDQ":
            solver_name = "Nelder-Mead"
        
        for i in range(num_problems):
            problem_rename = f"SYNTWOMODEL-1_solution={all_solutions[i]}"
            file_name = f"{solver}_on_{problem_rename}"
            # Load experiment.
            new_experiment = read_experiment_results(f"experiments/outputs/{file_name}.pickle")
            new_experiment.problem.name = f"SYN-1_initial_solution={all_solutions[i]}"
            new_experiment.solver.name = solver_name
            experiments_same_solver.append(new_experiment)

        myexperiment.append(experiments_same_solver)

    n_solvers = len(myexperiment)
    n_problems = len(myexperiment[0])
    print("Plotting results.")

    for i in range(n_problems):
        plot_progress_curves([myexperiment[solver_idx][i] for solver_idx in range(n_solvers)], plot_type="mean", normalize=False, print_max_hw=False)
        
    print("Finished. Plots can be found in experiments/plots folder.")


if (__name__ == "__main__"):
    main()
    
