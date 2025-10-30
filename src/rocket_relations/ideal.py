"""
ideal.py — Ideal rocket relations (c* and CF) under standard assumptions.

Assumptions
-----------
- Stagnation (chamber) conditions from constant-pressure heating
- Working fluid is a non-reacting, calorically perfect gas
- Nozzle flow is isentropic, steady, quasi-1D, and choked at the throat
- Neglect thermal/viscous/body forces

Functions
---------
c_star(gamma, R, T0)
    Characteristic velocity c* (Eq. 1)
c_f(gamma, pr_e, pr_a, eps)
    Thrust coefficient CF (Eq. 2) using ratios only
"""

from math import sqrt
from numbers import Real

def _require_numeric(name, x):
    """Enforce numeric scalar input."""
    if not isinstance(x, Real):
        raise TypeError(f"{name} must be numeric (got {type(x).__name__}).")

def c_star(gamma: float, R: float, T0: float) -> float:
    """
    Characteristic velocity c* for an ideal rocket.

    Parameters
    ----------
    gamma : float
        Ratio of specific heats (> 1). Dimensionless.
    R : float
        Specific gas constant (> 0). J/(kg·K) if SI.
    T0 : float
        Stagnation (chamber) temperature (> 0 K).

    Returns
    -------
    float
        c* in m/s (with SI inputs).

    Raises
    ------
    TypeError
        On non-numeric inputs.
    ValueError
        If gamma <= 1, R <= 0, or T0 <= 0.

    Formula (Eq. 1)
    ---------------
    c* = sqrt( (1/gamma) * ((gamma + 1)/2)^((gamma + 1)/(gamma - 1)) * R * T0 )
    """
    _require_numeric("gamma", gamma)
    _require_numeric("R", R)
    _require_numeric("T0", T0)

    if gamma <= 1:
        raise ValueError("gamma must be > 1.")
    if R <= 0:
        raise ValueError("R must be > 0.")
    if T0 <= 0:
        raise ValueError("T0 must be > 0 K.")

    term = ((gamma + 1.0) / 2.0) ** ((gamma + 1.0) / (gamma - 1.0))
    return sqrt((1.0 / gamma) * term * R * T0)


def c_f(gamma: float, pr_e: float, pr_a: float, eps: float) -> float:
    """
    Thrust coefficient CF for an ideal rocket nozzle (ratios form).

    Parameters
    ----------
    gamma : float
        Ratio of specific heats (> 1).
    pr_e : float
        Exit-to-chamber pressure ratio pe/p0 in [0, 1).
    pr_a : float
        Ambient-to-chamber pressure ratio pa/p0 in [0, 1).
    eps : float
        Area ratio Ae/A* (>= 1).

    Returns
    -------
    float
        Thrust coefficient CF (dimensionless).

    Raises
    ------
    TypeError
        On non-numeric inputs.
    ValueError
        If gamma <= 1, pr_e/pr_a ∉ [0,1), or eps < 1.

    Formula (Eq. 2)
    ---------------
    CF = sqrt( 2*gamma^2/(gamma-1) * (2/(gamma+1))^((gamma+1)/(gamma-1))
               * (1 - (pe/p0)^((gamma-1)/gamma)) )
         + (pe/p0 - pa/p0) * (Ae/A*)
    """
    _require_numeric("gamma", gamma)
    _require_numeric("pr_e", pr_e)
    _require_numeric("pr_a", pr_a)
    _require_numeric("eps", eps)

    if gamma <= 1:
        raise ValueError("gamma must be > 1.")
    for name, val in (("pr_e", pr_e), ("pr_a", pr_a)):
        if not (0.0 <= val < 1.0):
            raise ValueError(f"{name} must be in [0, 1).")
    if eps < 1.0:
        raise ValueError("eps (Ae/A*) must be >= 1.")

    factor = (2.0 * gamma * gamma) / (gamma - 1.0)
    expo   = (gamma + 1.0) / (gamma - 1.0)
    core   = (2.0 / (gamma + 1.0)) ** expo
    bracket = 1.0 - (pr_e ** ((gamma - 1.0) / gamma))

    term1 = sqrt(factor * core * bracket)
    term2 = (pr_e - pr_a) * eps
    return term1 + term2
