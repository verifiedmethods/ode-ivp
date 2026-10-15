"""Convergence and cost studies."""

from __future__ import annotations

import math

import numpy as np

from .integrate import CountingRHS, integrate
from .problems import Problem


def convergence_table(step, problem: Problem, ns, name: str = "step"):
    """Error at ``t_end`` (max norm) for each number of steps in ``ns``.

    Returns a list of dicts with keys ``n``, ``h``, ``error`` and ``evals``
    (the measured number of f-evaluations for the whole run).
    """
    ref = problem.solution_at_end()
    rows = []
    for n in ns:
        f = CountingRHS(problem.f)
        y = integrate(step, f, problem.t0, problem.initial(), problem.t_end, n, name)
        err = float(np.max(np.abs(y - ref)))
        rows.append({"n": int(n), "h": (problem.t_end - problem.t0) / n, "error": err, "evals": f.calls})
    return rows


def successive_orders(rows):
    """Observed order between successive rows, ``log(e_i / e_{i+1}) / log(h_i / h_{i+1})``."""
    out = []
    for a, b in zip(rows[:-1], rows[1:]):
        if a["error"] > 0 and b["error"] > 0 and math.isfinite(a["error"]) and math.isfinite(b["error"]):
            out.append(math.log(a["error"] / b["error"]) / math.log(a["h"] / b["h"]))
        else:
            out.append(float("nan"))
    return out


def fitted_order(rows) -> float:
    """Least-squares slope of log(error) against log(h); NaN if any error is zero or not finite."""
    hs = np.array([r["h"] for r in rows])
    errs = np.array([r["error"] for r in rows])
    if np.any(~np.isfinite(errs)) or np.any(errs <= 0):
        return float("nan")
    return float(np.polyfit(np.log(hs), np.log(errs), 1)[0])
