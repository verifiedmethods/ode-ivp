import math

import pytest

from conftest import synthetic_step
from vm.problems import PROBLEMS
from vm.study import convergence_table, fitted_order, successive_orders


@pytest.mark.parametrize("order", [1, 2, 3, 4])
def test_fitted_order_recovers_a_known_order(order):
    rows = convergence_table(synthetic_step(order), PROBLEMS["P2"], (40, 80, 160, 320))
    assert abs(fitted_order(rows) - order) < 0.05


def test_successive_orders_and_eval_counts():
    rows = convergence_table(synthetic_step(2, calls=3), PROBLEMS["P2"], (20, 40, 80))
    assert [r["evals"] for r in rows] == [60, 120, 240]
    orders = successive_orders(rows)
    assert len(orders) == 2 and all(abs(o - 2) < 0.15 for o in orders)


def test_fitted_order_is_nan_for_zero_error():
    rows = [{"h": 0.1, "error": 0.0}, {"h": 0.05, "error": 1e-3}]
    assert math.isnan(fitted_order(rows))
