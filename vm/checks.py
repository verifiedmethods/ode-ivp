"""Gates and reported results for unit A1 (design note, section 4).

A *gate* must pass. A *reported result* is shown next to the theoretical
expectation with no pass threshold; the student's write-up interprets it.
"""

from __future__ import annotations

import json
import math
import traceback
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .integrate import CountingRHS, StudentCodeError, check_output, integrate
from .problems import PROBLEMS, STIFF_LAMBDA
from .study import convergence_table, fitted_order, successive_orders

EXPECTED_PATH = Path(__file__).with_name("expected.json")

ONE_STEP_RTOL = 1e-12
ORDER_TOL = 0.1
ORDER_NS = (20, 40, 80, 160, 320)  # the fit uses ORDER_NS[1:]
TABLE_NS = (10, 20, 40, 80, 160, 320, 640)
TABLE_PROBLEMS = ("P1", "P2", "P3", "P4")
P5_NS = (1500, 15000)
STABILITY_FACTORS = (0.95, 1.05)

# Largest h|lambda| on the negative real axis for which |R(h lambda)| <= 1.
# For RK4 it is the nonzero real root of 1 + z/2 + z^2/6 + z^3/24 = 0.
RK4_REAL_STABILITY_LIMIT = 2.785293563405282


@dataclass(frozen=True)
class MethodSpec:
    key: str
    name: str
    function: str
    order: int
    evals: int
    stability_limit: float
    tutorial_section: str


METHODS = (
    MethodSpec("euler", "Euler", "euler_step", 1, 1, 2.0, "2"),
    MethodSpec("heun", "Heun", "heun_step", 2, 2, 2.0, "4"),
    MethodSpec("rk4", "Classical RK4", "rk4_step", 4, 4, RK4_REAL_STABILITY_LIMIT, "4"),
)


@dataclass
class GateResult:
    id: str
    title: str
    passed: bool
    measured: str
    tolerance: str
    reason: str
    hint: str = ""
    value: float | None = None

    def to_dict(self):
        return dict(self.__dict__)


@dataclass
class MethodResult:
    spec: MethodSpec
    status: str  # "not implemented", "missing", "checked"
    gates: list = field(default_factory=list)
    reported: dict = field(default_factory=dict)
    message: str = ""

    @property
    def n_passed(self) -> int:
        return sum(g.passed for g in self.gates)

    @property
    def all_passed(self) -> bool:
        return self.status == "checked" and all(g.passed for g in self.gates)

    def to_dict(self):
        return {
            "method": self.spec.key,
            "name": self.spec.name,
            "function": self.spec.function,
            "theoretical_order": self.spec.order,
            "status": self.status,
            "message": self.message,
            "gates_passed": self.n_passed,
            "gates_total": len(self.gates),
            "gates": [g.to_dict() for g in self.gates],
            "reported": self.reported,
        }


def load_expected(path: Path = EXPECTED_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def explain(exc: BaseException, student_file: str) -> str:
    """Describe an exception raised by student code, pointing at the line in their file."""
    if isinstance(exc, StudentCodeError):
        return str(exc)
    name = Path(student_file).name
    frames = [fr for fr in traceback.extract_tb(exc.__traceback__) if Path(fr.filename).name == name]
    where = ""
    if frames:
        fr = frames[-1]
        where = f" (line {fr.lineno} of {name}: {(fr.line or '').strip()})"
    return f"Your code raised {type(exc).__name__}: {exc}{where}"


# --------------------------------------------------------------------------- gates


def gate_one_step(step, spec: MethodSpec, expected: dict) -> GateResult:
    worst, worst_case = 0.0, ""
    for case, values in zip(expected["cases"], expected["values"][spec.key]):
        prob = PROBLEMS[case["problem"]]
        y = np.array(case["y"], dtype=float)
        out = check_output(step(prob.f, case["t"], y.copy(), case["h"]), y, spec.function)
        exp = np.array(values, dtype=float)
        rel = float(np.max(np.abs(out - exp)) / np.max(np.abs(exp)))
        if not math.isfinite(rel):
            rel = math.inf
        if rel > worst:
            worst, worst_case = rel, f"{case['problem']} at t = {case['t']}"
    passed = worst <= ONE_STEP_RTOL
    hint = ""
    if not passed:
        hint = (
            f"Largest difference in the {worst_case} case. Compare your formula with tutorial section "
            f"{spec.tutorial_section}: check the time at which each stage is evaluated (t, t + h/2, t + h), "
            "the multiples of h inside each stage, and the final weights."
        )
    return GateResult(
        "G1", "One step matches the method",
        passed, f"largest relative difference {worst:.1e}",
        f"≤ {ONE_STEP_RTOL:.0e}",
        "Three stored cases (P2, P3, P4; h = 0.1). Only rounding separates a correct step from the stored values.",
        hint, worst,
    )


def gate_cost(step, spec: MethodSpec) -> GateResult:
    prob = PROBLEMS["P2"]
    f = CountingRHS(prob.f)
    y = np.array([1.2], dtype=float)
    check_output(step(f, 0.4, y, 0.1), y, spec.function)
    passed = f.calls == spec.evals
    hint = ""
    if not passed:
        hint = f"{spec.name} evaluates f exactly {spec.evals} time(s) per step."
        if f.calls > 2 * spec.evals:
            hint += " Many more calls than that usually means a library solver is being called inside the step."
        elif f.calls > spec.evals:
            hint += " Store each stage value (k1, k2, ...) in a variable instead of calling f again."
    return GateResult(
        "G2", "Cost per step",
        passed, f"{f.calls} call(s) to f",
        f"exactly {spec.evals}",
        "The number of f-evaluations defines the method's cost; extra calls also reveal library solvers.",
        hint, float(f.calls),
    )


def gate_systems(step, spec: MethodSpec) -> GateResult:
    prob = PROBLEMS["P4"]
    y = np.array([np.cos(0.5), -np.sin(0.5)])
    before = y.copy()
    result = step(prob.f, 0.5, y, 0.1)
    problems = []
    try:
        shape = np.shape(np.asarray(result, dtype=float))
    except (TypeError, ValueError):
        shape = None
    if result is None:
        problems.append("returned None")
    elif shape != (2,):
        problems.append(f"returned shape {shape} for a system of 2 equations")
    if not np.array_equal(y, before):
        problems.append("changed the input y in place")
    passed = not problems
    hint = ""
    if not passed:
        hint = (
            "Work with whole NumPy arrays (no float(y) or y[0]), and build a new array for the result: "
            "write y_new = y + ..., not y += ... (which changes the caller's array)."
        )
    return GateResult(
        "G3", "Works on systems, without side effects",
        passed, "correct" if passed else "; ".join(problems),
        "exact",
        "P4 is a system of two equations. Changing y in place is the most common NumPy bug in hand-written RK code.",
        hint,
    )


def gate_order(step, spec: MethodSpec):
    rows = convergence_table(step, PROBLEMS["P2"], ORDER_NS, spec.function)
    p = fitted_order(rows[1:])
    passed = math.isfinite(p) and abs(p - spec.order) <= ORDER_TOL
    hint = ""
    if not passed:
        if math.isfinite(p):
            hint = (
                f"Your observed order is about {p:.2f}, but {spec.name} has order {spec.order}. "
                "Common causes: a stage evaluated at the wrong time, a wrong weight, or a missing factor of h."
            )
        else:
            hint = "Some errors were zero or not finite, so no order could be fitted."
    gate = GateResult(
        "G4", "Observed convergence order",
        passed, f"p_obs = {p:.3f}" if math.isfinite(p) else "p_obs not defined",
        f"|p_obs - {spec.order}| ≤ {ORDER_TOL}",
        "Least-squares slope of log(error) against log(h) on P2 for n = 40 to 320 steps; "
        "the margin covers the pre-asymptotic range without letting a lower-order method pass.",
        hint, p if math.isfinite(p) else None,
    )
    return gate, rows


# --------------------------------------------------------------------------- reported results


def report_error_tables(step, spec: MethodSpec):
    tables = {}
    for pid in TABLE_PROBLEMS:
        rows = convergence_table(step, PROBLEMS[pid], TABLE_NS, spec.function)
        orders = successive_orders(rows)
        tables[pid] = {"rows": rows, "orders": orders, "title": PROBLEMS[pid].title, "equation": PROBLEMS[pid].equation}
    return tables


def report_scipy_agreement(step, spec: MethodSpec):
    prob = PROBLEMS["P5"]
    ref = prob.solution_at_end()
    out = []
    for n in P5_NS:
        y = integrate(step, prob.f, prob.t0, prob.initial(), prob.t_end, n, spec.function)
        out.append({"n": n, "h": (prob.t_end - prob.t0) / n, "relative_error": float(np.max(np.abs(y - ref)) / np.max(np.abs(ref)))})
    return {"equation": prob.equation, "reference": "SciPy solve_ivp, DOP853, rtol = atol = 1e-13", "rows": out}


def report_stability(step, spec: MethodSpec):
    prob = PROBLEMS["P6"]
    h_limit = spec.stability_limit / abs(STIFF_LAMBDA)
    out = []
    for factor in STABILITY_FACTORS:
        n = max(1, round((prob.t_end - prob.t0) / (factor * h_limit)))
        h = (prob.t_end - prob.t0) / n
        y = integrate(step, prob.f, prob.t0, prob.initial(), prob.t_end, n, spec.function)
        mag = float(np.max(np.abs(y)))
        out.append({
            "h": h, "h_over_limit": h / h_limit, "abs_y_end": mag,
            "behaviour": "decays" if mag < 1.0 else "grows",
        })
    return {
        "equation": prob.equation,
        "h_limit": h_limit,
        "theory": f"stable for h < {spec.stability_limit:.4f}/|λ| = {h_limit:.5f}",
        "rows": out,
    }


# --------------------------------------------------------------------------- driver


def run_method(step, spec: MethodSpec, expected: dict, student_file: str) -> MethodResult:
    # Probe once, so that an untouched stub is reported as "not implemented".
    try:
        step(PROBLEMS["P2"].f, 0.0, np.array([0.5]), 0.1)
    except NotImplementedError:
        return MethodResult(spec, "not implemented", message=f"{spec.function} is not implemented yet.")
    except Exception:  # the gates below report the error properly
        pass

    result = MethodResult(spec, "checked")
    for gate_fn in (gate_one_step, gate_cost, gate_systems):
        args = (step, spec, expected) if gate_fn is gate_one_step else (step, spec)
        try:
            result.gates.append(gate_fn(*args))
        except Exception as exc:
            result.gates.append(_failed_gate(gate_fn, exc, student_file))
    try:
        gate, rows = gate_order(step, spec)
        result.gates.append(gate)
        result.reported["order_study"] = rows
    except Exception as exc:
        result.gates.append(_failed_gate(gate_order, exc, student_file))

    for key, fn in (
        ("error_tables", report_error_tables),
        ("scipy_agreement", report_scipy_agreement),
        ("stability", report_stability),
    ):
        try:
            result.reported[key] = fn(step, spec)
        except Exception as exc:
            result.reported[key] = {"error": explain(exc, student_file)}
    return result


_GATE_TITLES = {
    "gate_one_step": ("G1", "One step matches the method"),
    "gate_cost": ("G2", "Cost per step"),
    "gate_systems": ("G3", "Works on systems, without side effects"),
    "gate_order": ("G4", "Observed convergence order"),
}


def _failed_gate(gate_fn, exc, student_file) -> GateResult:
    gid, title = _GATE_TITLES[gate_fn.__name__]
    return GateResult(gid, title, False, "could not run", "", "", explain(exc, student_file))


def run_all(module, student_file: str, expected: dict | None = None):
    expected = expected or load_expected()
    results = []
    for spec in METHODS:
        step = getattr(module, spec.function, None)
        if step is None or not callable(step):
            results.append(MethodResult(spec, "missing", message=f"steps.py has no function named {spec.function}."))
            continue
        results.append(run_method(step, spec, expected, student_file))
    return results
