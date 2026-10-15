import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def p2_flow(t, y, h):
    """Exact solution operator of P2, y' = y - t^2 + 1: the value at t + h of the solution through (t, y)."""
    c = ((t + 1.0) ** 2 - y) * np.exp(-t)
    return (t + h + 1.0) ** 2 - c * np.exp(t + h)


def synthetic_step(order, calls=1):
    """A 'method' of known global order on P2: the exact flow plus a local error h^(order+1).

    It calls f ``calls`` times (and ignores the results) so the cost gate can be tested.
    No real Runge-Kutta code appears in the public tests.
    """

    def step(f, t, y, h):
        for _ in range(calls):
            f(t, y)
        return p2_flow(t, y, h) + h ** (order + 1)

    return step


@pytest.fixture
def root():
    return ROOT
