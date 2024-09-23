"""
Generate .pickle fils in /experiments/outputs (figure 12 (p=1,10 and communication costs=0,1000))
"""
import sys
import os.path as o
import os
sys.path.append(o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), ".."))) # type:ignore

from simopt.experiment_base import ProblemSolver, plot_area_scatterplots, post_normalize, plot_progress_curves, plot_solvability_cdfs, read_experiment_results, plot_solvability_profiles, plot_terminal_scatterplots, plot_terminal_progress

def main():
    p = 1 # circuit depths
    communication_costs = 1000 # communication costs

    if communication_costs == 0:
        solvers = ["VMI3-0-cv10", "ASTRODF-0", "NELDMDQ-0", "SPSAQ-0"]
    elif communication_costs == 1000:
        solvers = ["VMI3-1000-cv10", "ASTRODF-1000", "NELDMDQ-1000", "SPSAQ-1000"]


    if p == 1:
        theta = (1.6, 1.6)
        if communication_costs == 0:
            budget = 3000
        elif communication_costs == 1000:
            budget = 200000
        
    else:
        theta = (1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6, 1.6)
        if communication_costs == 0:
            budget = 10000
        elif communication_costs == 1000:
            budget = 1500000
            
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

    
    num_problems = len(all_edges)

    # RUNNING AND POST-PROCESSING EXPERIMENTS
    M = 20
    L = 200

    for i in range(num_problems):
        model_fixed_factors = {"edges": all_edges[i], "p": p, "theta": theta}
        problem_fixed_factors = {"budget": budget, "initial_solution": theta}
        problem_rename = f"MAXCUT-1_edges={all_edges[i]}_p={p}"

        # Temporarily store experiments on the same problem for post-normalization.
        experiments_same_problem = []
        solver_fixed_factors = {}

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