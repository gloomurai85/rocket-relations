import math
import pytest
from rocket_relations import c_star, c_f

# Ground-truth scalar checks using provided reference values.
def test_scalar_ground_truth():
    # Given reference values from the specification.
    T0 = 3500.0
    gamma = 1.2
    R = 350.0
    pr_e = 0.0125
    pr_a = 0.02
    eps = 10.0

    expected_c_star = 1706.6214
    expected_cf = 1.5423079

    result_c_star = c_star(gamma, R, T0)
    result_cf = c_f(gamma, pr_e, pr_a, eps)

    assert math.isclose(result_c_star, expected_c_star, rel_tol=1e-8, abs_tol=1e-8)
    assert math.isclose(result_cf, expected_cf, rel_tol=1e-8, abs_tol=1e-8)

# Parametrized sanity sweep: several realistic (gamma, R, T0) tuples asserting positive c*.
@pytest.mark.parametrize(
    "gamma,R,T0",
    [
        (1.1, 287.0, 3000.0),   # low gamma, typical gas constant, high temperature
        (1.3, 350.0, 2500.0),   # moderate gamma and R
        (1.67, 4124.0, 1200.0), # monoatomic-like gamma with large R (artificial)
        (1.2, 295.0, 1800.0),   # near-propulsive conditions
    ],
)
def test_c_star_positive_sanity(gamma, R, T0):
    # c* should be strictly positive for valid physical inputs.
    value = c_star(gamma, R, T0)
    assert isinstance(value, float)
    assert value > 0.0

# Type validation: non-numeric inputs should raise TypeError for c_star.
@pytest.mark.parametrize(
    "args",
    [
        ("not-a-number", 350.0, 3500.0),
        (1.2, "R-as-string", 3500.0),
        (1.2, 350.0, None),
    ],
)
def test_c_star_type_errors(args):
    # Passing non-numeric types to c_star must raise TypeError.
    with pytest.raises(TypeError):
        c_star(*args)

# Type validation: non-numeric inputs should raise TypeError for c_f.
@pytest.mark.parametrize(
    "args",
    [
        ("gamma", 0.01, 0.0, 10.0),
        (1.2, "pr_e", 0.0, 10.0),
        (1.2, 0.01, 0.0, "eps"),
    ],
)
def test_c_f_type_errors(args):
    # Passing non-numeric types to c_f must raise TypeError.
    with pytest.raises(TypeError):
        c_f(*args)

# Domain validation for c_star: invalid numeric ranges should raise ValueError.
@pytest.mark.parametrize(
    "gamma,R,T0",
    [
        (1.0, 350.0, 3500.0),   # gamma <= 1
        (0.9, 350.0, 3500.0),   # gamma < 1
        (1.2, 0.0, 3500.0),     # R <= 0
        (1.2, -287.0, 3500.0),  # R < 0
        (1.2, 350.0, 0.0),      # T0 <= 0
        (1.2, 350.0, -100.0),   # T0 < 0
    ],
)
def test_c_star_value_errors(gamma, R, T0):
    # Domain violations for c_star must raise ValueError.
    with pytest.raises(ValueError):
        c_star(gamma, R, T0)

# Domain validation for c_f: invalid numeric ranges should raise ValueError.
@pytest.mark.parametrize(
    "gamma,pr_e,pr_a,eps",
    [
        (1.0, 0.01, 0.0, 2.0),     # gamma <= 1
        (1.2, -0.001, 0.0, 2.0),   # pr_e < 0
        (1.2, 1.0, 0.0, 2.0),      # pr_e >= 1 (equal 1)
        (1.2, 0.5, -0.01, 2.0),    # pr_a < 0
        (1.2, 0.5, 1.0, 2.0),      # pr_a >= 1 (equal 1)
        (1.2, 0.01, 0.0, 0.5),     # eps < 1
    ],
)
def test_c_f_value_errors(gamma, pr_e, pr_a, eps):
    # Domain violations for c_f must raise ValueError.
    with pytest.raises(ValueError):
        c_f(gamma, pr_e, pr_a, eps)

# Edge case: c_f with pr_e = 0.0 should be well-defined, finite, and positive for pr_a=0 and eps>1.
def test_c_f_pr_e_zero_edge():
    # Root term reduces to full expansion; ensure finite positive result.
    gamma = 1.4
    pr_e = 0.0
    pr_a = 0.0
    eps = 2.0
    value = c_f(gamma, pr_e, pr_a, eps)
    assert isinstance(value, float)
    assert math.isfinite(value)
    assert value > 0.0

# Edge case: c_f with eps = 1.0 (minimal area ratio) remains finite and valid.
def test_c_f_eps_one_edge():
    # Use pr_e < pr_a to ensure the additive term can be negative but total stays finite.
    gamma = 1.3
    pr_e = 0.01
    pr_a = 0.0
    eps = 1.0
    value = c_f(gamma, pr_e, pr_a, eps)
    assert isinstance(value, float)
    assert math.isfinite(value)
    # Expect a physically sensible (finite) thrust coefficient; typically positive here.
    assert value > 0.0

# Edge case: c_f with pr_e near unity exercises small-bracket limit and must be finite (not NaN/inf).
@pytest.mark.parametrize("pr_e", [0.999, 0.9999])
def test_c_f_pr_e_near_unity(pr_e):
    # Near-unity exit pressure ratio should not produce NaN or infinite results.
    gamma = 1.2
    pr_a = 0.0
    eps = 10.0
    value = c_f(gamma, pr_e, pr_a, eps)
    assert isinstance(value, float)
    assert math.isfinite(value)
    # The value may be dominated by the (pr_e - pr_a) * eps term; ensure numeric sanity.
    assert not math.isnan(value)
