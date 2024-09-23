"""
Summary
-------
Max-Cut Problem using QAOA

"""
from __future__ import annotations

import numpy as np
import networkx as nx
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from mrg32k3a.mrg32k3a import MRG32k3a

from simopt.base import Model, Problem


class MAXCUT(Model):
    """
    A model that simulates QAOA to solve Max-Cut problem
    Returns the expected energy of current quantum state

    Attributes
    ----------
    name : string
        name of model
    n_rngs : int
        number of random-number generators used to run a simulation replication
    n_responses : int
        number of responses (performance measures)
    factors : dict
        changeable factors of the simulation model
    specifications : dict
        details of each factor (for GUI and data validation)
    check_factor_list : dict
        switch case for checking factor simulatability

    Arguments
    ---------
    fixed_factors : nested dict
        fixed factors of the simulation model

    See also
    --------
    base.Model
    """

    def __init__(self, fixed_factors=None):
        if fixed_factors is None:
            fixed_factors = {}
        self.name = "MAXCUT"
        self.n_rngs = 1
        self.n_responses = 1
        self.specifications = {
            "p": {
                "description": "problem dimension",
                "datatype": int,
                "default":1
            },
            "theta": {
                "description": "decision variable",
                "datatype": tuple,
                "default": (1.6, 1.6)
            },
            "edges":{
                "description": "edges",
                "datatype": list,
                "default": [[0,1],[0,2],[1,4],[2,3],[2,5],[3,5]]
            }
        }
        self.check_factor_list = {
            "theta": self.check_theta,
            "p": self.check_p
        }
        # Set factors of the simulation model.
        super().__init__(fixed_factors)

    def check_theta(self):
        return True

    def check_p(self):
        return self.factors["p"] > 0

    def replicate(self, rng_list: list["MRG32k3a"]) -> tuple[dict, dict]:
        """
        Simulate a single replication for the current model factors.

        Arguments
        ---------
        rng_list : list of mrg32k3a.mrg32k3a.MRG32k3a objects
            rngs for model to use when simulating a replication

        Returns
        -------
        responses : dict
            performance measures of interest
            "energy" = energy
        """
        # Designate separate random number generators.
        # Outputs will be coupled when generating demand.
        X_rng = rng_list[0]

        p = self.factors["p"]
        edges =self.factors["edges"]

        G = nx.Graph()
        G.add_edges_from(edges) 
        

        def append_zz_term(qc, q1, q2, gamma):
            qc.cx(q1, q2)
            qc.rz(2 * gamma, q2)
            qc.cx(q1, q2)

        def get_cost_operator_circuit(G, gamma):
            N = G.number_of_nodes()
            qc = QuantumCircuit(N, N)
            for i, j in G.edges():
                append_zz_term(qc, i, j, gamma)
            return qc

        def append_x_term(qc, q1, beta):
            qc.rx(2 * beta, q1)

        def get_mixer_operator_circuit(G, beta):
            N = G.number_of_nodes()
            qc = QuantumCircuit(N, N)
            for n in G.nodes():
                append_x_term(qc, n, beta)
            return qc

        def get_qaoa_circuit(G, beta, gamma):
            assert (len(beta) == len(gamma))
            p = len(beta)  # infering number of QAOA steps from the parameters passed
            N = G.number_of_nodes()
            qc = QuantumCircuit(N, N)
            # apply a layer of Hadamards
            qc.h(range(N))
            # apply p alternating operators
            for i in range(p):
                qc = qc.compose(get_cost_operator_circuit(G, gamma[i]))
                qc = qc.compose(get_mixer_operator_circuit(G, beta[i]))

            # measure the result
            qc.barrier(range(N))
            qc.measure(range(N), range(N))
            return qc

        def maxcut_obj(x, G):
            cut = 0
            for i, j in G.edges():
                if x[i] != x[j]:
                    # the edge is cut
                    cut -= 1
            return cut

        theta = np.array(self.factors["theta"])

        backend = Aer.get_backend('qasm_simulator')
        beta = theta[:p]
        gamma = theta[p:]
        qc = get_qaoa_circuit(G, beta, gamma)

        counts = execute(qc, backend, seed_simulator=X_rng.poissonvariate(200), shots = 5).result().get_counts()

        def compute_maxcut_energy(counts, G):
            energy = 0
            total_counts = 0
            for meas, meas_count in counts.items():
                obj_for_meas = maxcut_obj(meas, G)
                energy += obj_for_meas * meas_count
                total_counts += meas_count
            return energy / total_counts

        def invert_counts(counts):
            return {k[::-1]: v for k, v in counts.items()}

        energy = compute_maxcut_energy(invert_counts(counts), G)

        responses = {"energy": energy}
        gradients = {}
        return responses, gradients


"""
Summary
-------
Maximize the energy
"""


class MaxCutMinEnergy(Problem):
    """
    Base class to implement simulation-optimization problems.

    Attributes
    ----------
    name : string
        name of problem
    dim : int
        number of decision variables
    n_objectives : int
        number of objectives
    n_stochastic_constraints : int
        number of stochastic constraints
    minmax : tuple of int (+/- 1)
        indicator of maximization (+1) or minimization (-1) for each objective
    constraint_type : string
        description of constraints types:
            "unconstrained", "box", "deterministic", "stochastic"
    variable_type : string
        description of variable types:
            "discrete", "continuous", "mixed"
    lower_bounds : tuple
        lower bound for each decision variable
    upper_bounds : tuple
        upper bound for each decision variable
    gradient_available : bool
        indicates if gradient of objective function is available
    optimal_value : tuple
        optimal objective function value
    optimal_solution : tuple
        optimal solution
    model : Model object
        associated simulation model that generates replications
    model_default_factors : dict
        default values for overriding model-level default factors
    model_fixed_factors : dict
        combination of overriden model-level factors and defaults
    model_decision_factors : set of str
        set of keys for factors that are decision variables
    rng_list : list of mrg32k3a.mrg32k3a.MRG32k3a objects
        list of RNGs used to generate a random initial solution
        or a random problem instance
    factors : dict
        changeable factors of the problem
            initial_solution : tuple
                default initial solution from which solvers start
            budget : int > 0
                max number of replications (fn evals) for a solver to take
    specifications : dict
        details of each factor (for GUI, data validation, and defaults)

    Arguments
    ---------
    name : str
        user-specified name for problem
    fixed_factors : dict
        dictionary of user-specified problem factors
    model_fixed_factors : dict
        subset of user-specified non-decision factors to pass through to the model

    See also
    --------
    base.Problem
    """

    def __init__(self, name="MAXCUT-1", fixed_factors=None, model_fixed_factors=None):
        if fixed_factors is None:
            fixed_factors = {}
        if model_fixed_factors is None:
            model_fixed_factors = {}
        self.name = name
        self.n_objectives = 1
        self.n_stochastic_constraints = 0
        self.minmax = (-1,)
        self.constraint_type = "unconstrained"
        self.variable_type = "continuous"
        self.gradient_available = False
        self.optimal_value = None
        self.optimal_solution = None
        self.model_default_factors = {}
        self.model_decision_factors = {"theta"}
        self.factors = fixed_factors
        self.specifications = {
            "initial_solution": {
                "description": "initial solution",
                "datatype": tuple,
                "default":(1.6, 1.6)
            },
            "budget": {
                "description": "max # of replications for a solver to take",
                "datatype": int,
                "default": 5000
            }
        }
        self.check_factor_list = {
            "initial_solution": self.check_initial_solution,
            "budget": self.check_budget
        }
        super().__init__(fixed_factors, model_fixed_factors)
        # Instantiate model with fixed factors and over-riden defaults.
        self.model = MAXCUT(self.model_fixed_factors)
        self.dim = len(self.factors["initial_solution"])
        self.lower_bounds = (-np.inf,) * self.dim
        self.upper_bounds = (np.inf,) * self.dim

    def vector_to_factor_dict(self, vector):
        """
        Convert a vector of variables to a dictionary with factor keys

        Arguments
        ---------
        vector : tuple
            vector of values associated with decision variables

        Returns
        -------
        factor_dict : dictionary
            dictionary with factor keys and associated values
        """
        factor_dict = {
            "theta": vector[:]
        }
        return factor_dict

    def factor_dict_to_vector(self, factor_dict):
        """
        Convert a dictionary with factor keys to a vector
        of variables.

        Arguments
        ---------
        factor_dict : dictionary
            dictionary with factor keys and associated values

        Returns
        -------
        vector : tuple
            vector of values associated with decision variables
        """
        vector = tuple(factor_dict["theta"])
        return vector

    def response_dict_to_objectives(self, response_dict):
        """
        Convert a dictionary with response keys to a vector
        of objectives.

        Arguments
        ---------
        response_dict : dictionary
            dictionary with response keys and associated values

        Returns
        -------
        objectives : tuple
            vector of objectives
        """
        objectives = (response_dict["energy"],)
        return objectives

    def get_random_solution(self, rand_sol_rng):
        """
        Generate a random solution for starting or restarting solvers.

        Arguments
        ---------
        rand_sol_rng : mrg32k3a.mrg32k3a.MRG32k3a object
            random-number generator used to sample a new random solution

        Returns
        -------
        x : tuple
            vector of decision variables
        """
        # Generate random solution using acceptable/rejection.
        x = tuple(rand_sol_rng.mvnormalvariate(mean_vec=np.zeros(self.dim), cov=np.eye(self.dim), factorized=False))
        x = tuple(i * 1.5 for i in x)
        
        return x
