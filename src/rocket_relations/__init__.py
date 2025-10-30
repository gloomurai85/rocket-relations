"""
rocket_relations — Basic ideal rocket relations (educational)

Public API
----------
c_star(gamma, R, T0) -> float
c_f(gamma, pr_e, pr_a, eps) -> float
"""
from .ideal import c_star, c_f
__all__ = ["c_star", "c_f"]
