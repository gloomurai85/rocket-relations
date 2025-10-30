"""
ideal.py — Ideal rocket relations (c* and CF) under standard assumptions.

Assumptions
-----------
- Stagnation (chamber) conditions from constant-pressure heating.
- Working fluid is a non-reacting, calorically perfect gas.
- Nozzle flow is isentropic, steady, quasi-1D, and choked at the throat.
- Neglect thermal/viscous/body forces.

Functions
---------
c_star(gamma, R, T0)
    Characteristic velocity c* (Eq. 1).
c_f(gamma, pr_e, pr_a, eps)
    Thrust coefficient CF (Eq. 2) using pressure/area ratios only.

Notes
-----
Formulas used (ratios form)::

    c* = sqrt( (1/gamma) * ((gamma + 1)/2)^((gamma + 1)/(gamma - 1)) * R * T0 )

    CF = sqrt( 2*gamma^2/(gamma-1) * (2/(gamma+1))^((gamma+1)/(gamma-1))
               * (1 - (pr_e)^((gamma-1)/gamma)) ) + (pr_e - pr_a) * eps
"""

from math import sqrt
from numbers import Real


def _require_numeric(name, x):
    """Enforce numeric scalar input (accepts Python Real numbers)."""
    if not isinstance(x, Real):
        raise TypeError(f"{name} must be numeric (got {type(x).__name__}).")


def c_star(gamma: float, R: float, T0: float) -> float:
    r"""
    Characteristic velocity c* for an ideal rocket.

    Parameters
    ----------
    gamma : float
        Ratio of specific heats (> 1). Dimensionless.
    R : float
        Specific gas constant (> 0). Units: J/(kg·K) if SI.
    T0 : float
        Stagnation (chamber) temperature (> 0). Absolute units (K).

    Returns
    -------
    float
        Characteristic velocity c* [m/s if SI inputs].

    Raises
    ------
    TypeError
        If any input is not numeric.
    ValueError
        If `gamma <= 1`, `R <= 0`, or `T0 <= 0`.

    Notes
    -----
    Implements Eq. (1) from the HW handout:

        c* = sqrt( (1/gamma) * ((gamma + 1)/2)^((gamma + 1)/(gamma - 1)) * R * T0 )

    Examples
    --------
    >>> from rocket_relations import c_star
    >>> round(c_star(1.2, 350.0, 3500.0), 4)
    1706.6214
    """
    # ---- type checks ----
    _require_numeric("gamma", gamma)
    _require_numeric("R", R)
    _require_numeric("T0", T0)

    # ---- domain checks ----
    if gamma <= 1:
        raise ValueError("gamma must be > 1 for a physical calorically perfect gas.")
    if R <= 0:
        raise ValueError("R must be > 0.")
    if T0 <= 0:
        raise ValueError("T0 must be > 0 (absolute temperature).")

    # ---- computation (Eq. 1) ----
    term = ((gamma + 1.0) / 2.0) ** ((gamma + 1.0) / (gamma - 1.0))
    value = sqrt((1.0 / gamma) * term * R * T0)
    return value


def c_f(gamma: float, pr_e: float, pr_a: float, eps: float) -> float:
    r"""
    Thrust coefficient **CF** for an ideal rocket nozzle (ratios form).
    
    :param float gamma: Ratio of specific heats (> 1).
    :param float pr_e: Exit-to-chamber pressure ratio ``p_e/p_0`` in ``[0, 1)``.
    :param float pr_a: Ambient-to-chamber pressure ratio ``p_a/p_0`` in ``[0, 1)``.
    :param float eps: Area ratio ``A_e/A^*`` (``>= 1``).
    :returns: Thrust coefficient ``CF`` (dimensionless).
    :rtype: float
    :raises TypeError: If any input is not numeric.
    :raises ValueError: If ``gamma <= 1``, or ``pr_e``/``pr_a`` not in ``[0, 1)``, or ``eps < 1``.
    
    **Formula (ratios form)**
    
    .. math::
    
       CF = \sqrt{\frac{2\gamma^2}{\gamma-1}
                  \left(\frac{2}{\gamma+1}\right)^{\frac{\gamma+1}{\gamma-1}}
                  \left(1 - (pr_e)^{\frac{\gamma-1}{\gamma}}\right)}
            + (pr_e - pr_a)\,\epsilon
    
    **Example**
    
    .. code-block:: python
    
       >>> from rocket_relations import c_f
       >>> round(c_f(1.2, pr_e=0.0125, pr_a=0.02, eps=10.0), 7)
       1.5423079
    """

    # ---- type checks ----
    _require_numeric("gamma", gamma)
    _require_numeric("pr_e", pr_e)
    _require_numeric("pr_a", pr_a)
    _require_numeric("eps", eps)

    # ---- domain checks ----
    if gamma <= 1:
        raise ValueError("gamma must be > 1.")
    for name, val in (("pr_e", pr_e), ("pr_a", pr_a)):
        if not (0.0 <= val < 1.0):
            raise ValueError(f"{name} must be in [0, 1).")
    if eps < 1.0:
        raise ValueError("eps (Ae/A*) must be >= 1.")

    # ---- computation (Eq. 2) ----
    factor = (2.0 * gamma * gamma) / (gamma - 1.0)
    expo = (gamma + 1.0) / (gamma - 1.0)
    core = (2.0 / (gamma + 1.0)) ** expo
    bracket = 1.0 - (pr_e ** ((gamma - 1.0) / gamma))

    term1 = sqrt(factor * core * bracket)
    term2 = (pr_e - pr_a) * eps
    return term1 + term2
