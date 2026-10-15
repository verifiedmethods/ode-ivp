import types

import numpy as np

from conftest import synthetic_step
from vm.checks import METHODS, gate_cost, gate_one_step, gate_order, gate_systems, load_expected, run_all, run_method

SPEC = {m.key: m for m in METHODS}


def test_expected_values_are_consistent():
    exp = load_expected()
    assert set(exp["values"]) == set(SPEC)
    for key, vals in exp["values"].items():
        assert len(vals) == len(exp["cases"])
        for case, v in zip(exp["cases"], vals):
            assert len(v) == len(case["y"]) and np.all(np.isfinite(v))


def test_cost_gate_counts_calls():
    assert gate_cost(synthetic_step(4, calls=4), SPEC["rk4"]).passed
    g = gate_cost(synthetic_step(4, calls=40), SPEC["rk4"])
    assert not g.passed and "library solver" in g.hint


def test_systems_gate_detects_in_place_change_and_scalar_output():
    def in_place(f, t, y, h):
        y += h * np.asarray(f(t, y))
        return y

    def scalar(f, t, y, h):
        return float(y[0])

    def fine(f, t, y, h):
        return y + h * np.asarray(f(t, y))

    assert not gate_systems(in_place, SPEC["euler"]).passed
    g = gate_systems(scalar, SPEC["euler"])
    assert not g.passed and "shape" in g.measured
    assert gate_systems(fine, SPEC["euler"]).passed


def test_one_step_gate_rejects_a_different_method():
    g = gate_one_step(synthetic_step(4), SPEC["rk4"], load_expected())
    assert not g.passed and g.hint


def test_order_gate_with_synthetic_methods():
    ok, _ = gate_order(synthetic_step(2), SPEC["heun"])
    assert ok.passed and abs(ok.value - 2) < 0.1
    bad, _ = gate_order(synthetic_step(1), SPEC["heun"])
    assert not bad.passed and "order is about" in bad.hint


def test_not_implemented_and_missing_functions():
    def stub(f, t, y, h):
        raise NotImplementedError

    mod = types.SimpleNamespace(euler_step=stub, heun_step=stub)
    results = run_all(mod, "steps.py")
    assert [r.status for r in results] == ["not implemented", "not implemented", "missing"]


def test_errors_in_student_code_are_explained(tmp_path):
    src = tmp_path / "steps.py"
    src.write_text("def euler_step(f, t, y, h):\n    return y + h * undefined_name\n", encoding="utf-8")
    ns = {}
    exec(compile(src.read_text(), str(src), "exec"), ns)
    r = run_method(ns["euler_step"], SPEC["euler"], load_expected(), str(src))
    assert r.status == "checked" and not r.all_passed
    g1 = r.gates[0]
    assert "NameError" in g1.hint and "line 2" in g1.hint


def test_cost_gate_explains_a_step_that_never_calls_f():
    g = gate_cost(lambda f, t, y, h: y.copy(), SPEC["euler"])
    assert not g.passed and "0 times" in g.hint and "f(t, y)" in g.hint


def test_systems_gate_hint_matches_the_problem():
    g_none = gate_systems(lambda f, t, y, h: None, SPEC["euler"])
    assert "return" in g_none.hint and "y +=" not in g_none.hint

    def in_place(f, t, y, h):
        y += h * np.asarray(f(t, y))
        return y

    g_inplace = gate_systems(in_place, SPEC["euler"])
    assert "y +=" in g_inplace.hint and "float(y)" not in g_inplace.hint


def test_one_step_hint_for_euler_does_not_mention_stages():
    g = gate_one_step(lambda f, t, y, h: y + 2 * h * np.asarray(f(t, y)), SPEC["euler"], load_expected())
    assert not g.passed and "t + h/2" not in g.hint and "increment" in g.hint
