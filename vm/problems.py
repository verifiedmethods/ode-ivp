"""Test problems P1 to P6 (design note, section 3).

Every right-hand side takes ``(t, y)`` with ``y`` a 1-D NumPy array (length 1
for a scalar equation) and returns an array of the same shape.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Optional

import numpy as np

RHS = Callable[[float, np.ndarray], np.ndarray]


@dataclass(frozen=True)
class Problem:
    id: str
    title: str
    equation: str
    f: RHS
    t0: float
    y0: tuple
    t_end: float
    exact: Optional[Callable[[float], np.ndarray]] = None

    def initial(self) -> np.ndarray:
        return np.array(self.y0, dtype=float)

    def solution_at_end(self) -> np.ndarray:
        """Exact solution at ``t_end``, or a tight SciPy reference if there is none."""
        if self.exact is not None:
            return np.asarray(self.exact(self.t_end), dtype=float)
        return _scipy_reference(self.id)


# P3 parameters (logistic growth)
LOGISTIC_R = 0.8
LOGISTIC_K = 10.0

# P5 parameters (Lotka-Volterra)
LV_A, LV_B, LV_C, LV_D = 1.0, 0.1, 1.5, 0.075

# P6 parameter (stiff linear test equation)
STIFF_LAMBDA = -50.0


def _logistic_exact(t: float) -> np.ndarray:
    r, K, y0 = LOGISTIC_R, LOGISTIC_K, 1.0
    e = np.exp(r * t)
    return np.array([K * y0 * e / (K + y0 * (e - 1.0))])


PROBLEMS = {
    p.id: p
    for p in (
        Problem(
            "P1", "Exponential growth", "y' = y, y(0) = 1, on [0, 1]",
            lambda t, y: y, 0.0, (1.0,), 1.0,
            lambda t: np.array([np.exp(t)]),
        ),
        Problem(
            "P2", "Non-autonomous scalar equation", "y' = y - t^2 + 1, y(0) = 0.5, on [0, 2]",
            lambda t, y: y - t**2 + 1.0, 0.0, (0.5,), 2.0,
            lambda t: np.array([(t + 1.0) ** 2 - 0.5 * np.exp(t)]),
        ),
        Problem(
            "P3", "Logistic growth", "y' = 0.8 y (1 - y/10), y(0) = 1, on [0, 5]",
            lambda t, y: LOGISTIC_R * y * (1.0 - y / LOGISTIC_K), 0.0, (1.0,), 5.0,
            _logistic_exact,
        ),
        Problem(
            "P4", "Harmonic oscillator (system)", "y1' = y2, y2' = -y1, y(0) = (1, 0), on [0, 2 pi]",
            lambda t, y: np.array([y[1], -y[0]]), 0.0, (1.0, 0.0), 2.0 * np.pi,
            lambda t: np.array([np.cos(t), -np.sin(t)]),
        ),
        Problem(
            "P5", "Lotka-Volterra predator-prey", "x' = x - 0.1 x y, y' = -1.5 y + 0.075 x y, (x, y)(0) = (10, 5), on [0, 15]",
            lambda t, y: np.array([LV_A * y[0] - LV_B * y[0] * y[1], -LV_C * y[1] + LV_D * y[0] * y[1]]),
            0.0, (10.0, 5.0), 15.0,
        ),
        Problem(
            "P6", "Stiff test equation", "y' = -50 y, y(0) = 1, on [0, 4]",
            lambda t, y: STIFF_LAMBDA * y, 0.0, (1.0,), 4.0,
            lambda t: np.array([np.exp(STIFF_LAMBDA * t)]),
        ),
    )
}


@lru_cache(maxsize=None)
def _scipy_reference(problem_id: str) -> np.ndarray:
    from scipy.integrate import solve_ivp

    p = PROBLEMS[problem_id]
    sol = solve_ivp(p.f, (p.t0, p.t_end), p.initial(), method="DOP853", rtol=1e-13, atol=1e-13)
    if not sol.success:  # pragma: no cover
        raise RuntimeError(f"SciPy reference for {problem_id} failed: {sol.message}")
    return sol.y[:, -1].copy()
