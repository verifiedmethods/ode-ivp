"""Fixed-step driver, f-evaluation counter and checks on what a step returns."""

from __future__ import annotations

import numpy as np


class StudentCodeError(Exception):
    """A step function returned something the driver cannot use."""


class CountingRHS:
    """Wrap a right-hand side ``f(t, y)`` and count how often it is called."""

    def __init__(self, f):
        self._f = f
        self.calls = 0

    def __call__(self, t, y):
        self.calls += 1
        return self._f(t, y)


def check_output(result, y: np.ndarray, name: str) -> np.ndarray:
    """Return ``result`` as a float array with the shape of ``y``, or explain why not."""
    if result is None:
        raise StudentCodeError(f"{name} returned None. Did you forget the 'return' statement?")
    try:
        arr = np.asarray(result, dtype=float)
    except (TypeError, ValueError) as exc:
        raise StudentCodeError(f"{name} returned {type(result).__name__}, which is not a numeric array: {exc}") from exc
    if arr.shape != y.shape:
        raise StudentCodeError(
            f"{name} returned an array of shape {arr.shape}; it must have the same shape as y, {y.shape}."
        )
    return arr


def integrate(step, f, t0: float, y0, t_end: float, n: int, name: str = "step") -> np.ndarray:
    """Take ``n`` equal steps from ``t0`` to ``t_end``; return the value at ``t_end``."""
    h = (t_end - t0) / n
    y = np.array(y0, dtype=float)
    with np.errstate(over="ignore", invalid="ignore"):
        for i in range(n):
            t = t0 + i * h  # computed from i, so rounding does not accumulate in t
            y = check_output(step(f, t, y, h), y, name)
    return y


def trajectory(step, f, t0: float, y0, t_end: float, n: int, name: str = "step"):
    """Like :func:`integrate`, but return all times and values (for plots in the briefs)."""
    h = (t_end - t0) / n
    y = np.array(y0, dtype=float)
    ts = t0 + h * np.arange(n + 1)
    ys = np.empty((n + 1,) + y.shape)
    ys[0] = y
    with np.errstate(over="ignore", invalid="ignore"):
        for i in range(n):
            y = check_output(step(f, ts[i], y, h), y, name)
            ys[i + 1] = y
    return ts, ys
