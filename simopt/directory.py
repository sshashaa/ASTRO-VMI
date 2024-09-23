#!/usr/bin/env python
"""
Summary
-------
Provide dictionary directories listing solvers, problems, and models.
"""
from __future__ import annotations

# import solvers
from simopt.solvers.astrodfonemodel import ASTRODF1M
from simopt.solvers.astrodftwomodel import ASTRODF2M
from simopt.solvers.vmiastrodf import VMIASTRODF
from simopt.solvers.neldmdq import NelderMeadQ
from simopt.solvers.spsaq import SPSAQ

# import models and problems
from simopt.models.maxcut import MaxCutMinEnergy, MAXCUT
from simopt.models.synthetic import SYNTHETIC, SYNTHETIC_MIN

# Import base
from simopt.base import Model, Problem, Solver

# directory dictionaries
solver_directory: dict[str, "Solver"] = {
    "VMIASTRODF": VMIASTRODF,
    "ASTRODF1M": ASTRODF1M,
    "ASTRODF2M": ASTRODF2M,
    "NELDMDQ": NelderMeadQ,
    "SPSAQ": SPSAQ
}

solver_unabbreviated_directory: dict[str, "Solver"] = {
}

problem_directory: dict[str, "Problem"] = {
    "MAXCUT-1": MaxCutMinEnergy,
    "SYN-1": SYNTHETIC_MIN
}

problem_unabbreviated_directory: dict[str, "Problem"] = {
}
model_directory: dict[str, "Model"] = {
    "MAXCUT": MAXCUT,
    "SYN": SYNTHETIC
}
model_unabbreviated_directory: dict[str, "Model"] = {
}
model_problem_unabbreviated_directory: dict[str, str] = {
    "Min Deterministic Function + Noise (SUCG)": "EXAMPLE",
    "Max Profit for Continuous Newsvendor (SBCG)": "CNTNEWS",
    "Min Mean Sojourn Time for MM1 Queue (SBCG)": "MM1",
    "Min Total Cost for Facility Sizing (SSCG)": "FACSIZE",
    "Max Service for Facility Sizing (SDCN)": "FACSIZE",
    "Max Revenue for Revenue Management Temporal Demand (SDDN)": "RMITD",
    "Min Total Cost for (s, S) Inventory (SBCN)": "SSCONT",
    "Max Revenue for Iron Ore (SBDN)": "IRONORE",
    "Max Revenue for Continuous Iron Ore (SBCN)": "IRONORE",
    "Max Profit for Dynamic Newsvendor (SBDN)": "DYNAMNEWS",
    "Min Cost for Dual Sourcing (SBDN)": "DUALSOURCING",
    "Min Total Cost for Discrete Contamination (SSDN)": "CONTAM",
    "Min Total Cost for Continuous Contamination (SSCN)": "CONTAM",
    "Min Avg Difference for Chess Matchmaking (SSCN)": "CHESS",
    "Min Mean Longest Path for Stochastic Activity Network (SBCG)": "SAN",
    "Max Revenue for Hotel Booking (SBDN)": "HOTEL",
    "Max Revenue for Restaurant Table Allocation (SDDN)": "TABLEALLOCATION",
    "Max Log Likelihood for Gamma Parameter Estimation (SBCN)": "PARAMESTI",
    "Min Mean Longest Path for Fixed Stochastic Activity Network (SBCG)": "FIXEDSAN",
    "Min Total Cost for Communication Networks System (SDCN)": "NETWORK",
    "Min Total Departed Visitors for Amusement Park (SDDN)": "AMUSEMENTPARK",
}
model_problem_class_directory: dict[str, "Model"] = {
}
