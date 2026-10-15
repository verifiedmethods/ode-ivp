import numpy as np
import pytest

from vm.checks import METHODS, RK4_REAL_STABILITY_LIMIT
from vm.problems import PROBLEMS


@pytest.mark.parametrize("pid", [p for p in PROBLEMS if PROBLEMS[p].exact is not None])
def test_exact_solution_satisfies_the_equation(pid):
    p = PROBLEMS[pid]
    assert np.allclose(p.exact(p.t0), p.initial(), rtol=0, atol=1e-14)
    eps = 1e-5
    for t in np.linspace(p.t0 + 0.1, p.t_end - 0.1, 7):
        dydt = (p.exact(t + eps) - p.exact(t - eps)) / (2 * eps)
        rhs = p.f(t, p.exact(t))
        scale = max(1.0, float(np.max(np.abs(rhs))))
        assert np.max(np.abs(dydt - rhs)) / scale < 1e-7


def test_lotka_volterra_reference_is_finite_and_positive():
    ref = PROBLEMS["P5"].solution_at_end()
    assert ref.shape == (2,) and np.all(np.isfinite(ref)) and np.all(ref > 0)


def test_rk4_stability_limit_is_the_root_of_the_stability_polynomial():
    z = -RK4_REAL_STABILITY_LIMIT
    assert abs(1 + z + z**2 / 2 + z**3 / 6 + z**4 / 24 - 1.0) < 1e-12


def test_euler_and_heun_limits():
    limits = {m.key: m.stability_limit for m in METHODS}
    assert limits["euler"] == 2.0 and limits["heun"] == 2.0
    assert abs((1 - 2.0 + 2.0**2 / 2) - 1.0) < 1e-15  # Heun: R(-2) = 1
