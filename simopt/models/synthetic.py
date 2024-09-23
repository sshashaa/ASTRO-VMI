import numpy as np
import math
from numpy.linalg import norm

from simopt.base import Model, Problem

class SYNTHETIC(Model):
    def __init__(self, fixed_factors={}):
        self.name = "SYNTHETIC"
        self.n_rngs = 1
        self.n_responses = 1
        self.specifications = {
            "dim": {
                "description": "Problem Dimension",
                "datatype": int,
                "default": 2
            },
            "sigma_version":{
                "description": "sigma version",
                "datatype": int,
                "default": 1
            }
        }
        # Set factors of the simulation model.
        super().__init__(fixed_factors)
        self.specifications = {
            "X": {
                "description": "Decision Variables (vector)",
                "datatype": tuple,
                "default": (-1,) * self.factors["dim"]
            }
        }
        super().__init__(fixed_factors)

    def replicate(self, rng_list):
        rng = rng_list[0]
        d = self.factors["dim"]
        x = self.factors["X"]
        sigma_version = self.factors["sigma_version"]
        stochastic_noise = np.zeros(d)

        for i in range(d-1):
            if sigma_version == 1:
                sigma = math.sqrt(abs((x[i] - 3) * (x[i+1] - 2)))
            elif sigma_version == 2:
                sigma = math.sqrt(abs((x[i]**2 + x[i+1]-11)**2 + (x[i]+x[i+1]**2-7)**2))
            elif sigma_version == 3:
                sigma = math.sqrt(abs((x[i]**2 + x[i+1]-11)**2 + (x[i]+x[i+1]**2-7)**2 + 10*(x[i]-x[i+1])**2))
            else:
                sigma = math.sqrt(abs((x[i]**2 + x[i+1]-11)**2 + (x[i]+x[i+1]**2-7)**2 + (x[i]-x[i+1])**2 + abs(x[i]-3)))

            stochastic_noise[i] = rng.normalvariate(mu=0, sigma=sigma)

        # modified version of the Himmelblau's function
        
        objective_value = 0 
        for i in range(d-1):
            if i%2 == 0:
                objective_value += (x[i]**2 + x[i+1]-11)**2 + (x[i]+x[i+1]**2-7)**2 + (x[i]-x[i+1])**2 + abs(x[i]-3) + stochastic_noise[i]

        
        #objective_value = (x[0]**2 + x[1]-11)**2 + (x[0]+x[1]**2-7)**2 + (x[0]-x[1])**2 + abs(x[0]-3) + stochastic_noise[0]

        # Compose responses and gradients.
        responses = {"objective_value": objective_value}
        gradients = {}
        return responses, gradients


"""
Summary
-------
Minimize the objective function value (Synthetic problem)
"""


class SYNTHETIC_MIN(Problem):
    def __init__(self, name="SYN-1", fixed_factors={}, model_fixed_factors={}):
        self.name = name
        self.n_objectives = 1
        self.n_stochastic_constraints = 0
        self.minmax = (-1,)
        self.constraint_type = "unconstrained"
        self.variable_type = "continuous"
        self.gradient_available = False
        self.optimal_value = None
        self.optimal_solution = None  # (90, 50, 0)
        self.model_default_factors = {}
        self.model_decision_factors = {"X"}
        self.factors = fixed_factors
        self.specifications = {
            "budget": {
                "description": "Max # of replications for a solver to take.",
                "datatype": int,
                "default": 50000
            }
        }
        super().__init__(fixed_factors, model_fixed_factors)

        self.model = SYNTHETIC(self.model_fixed_factors)
        self.dim = self.model.factors["dim"]
        self.lower_bounds = (-np.inf,) * self.dim
        self.upper_bounds = (np.inf,) * self.dim
        self.specifications = {
            "initial_solution": {
                "description": "Initial solution from which solvers start.",
                "datatype": tuple,
                #"default": (-5,) * self.dim
                "default": (0, 0)
            }
        }
        super().__init__(fixed_factors, model_fixed_factors)
        # Instantiate model with fixed factors and over-riden defaults.

    def vector_to_factor_dict(self, vector):
        factor_dict = {
            "X": vector[:]
        }
        return factor_dict

    def factor_dict_to_vector(self, factor_dict):
        vector = tuple(factor_dict["X"])
        return vector

    def response_dict_to_objectives(self, response_dict):
        objectives = (response_dict["objective_value"],)
        return objectives

    def get_random_solution(self, rand_sol_rng):
        temp = [rand_sol_rng.random() for _ in range(self.dim)]
        x = tuple([x * 150 for x in temp])
        return x
