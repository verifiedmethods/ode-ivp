"""Your work for unit A1: three one-step methods for y' = f(t, y).

Write each function below, then run   python verify.py   in this unit's
folder. The tutorial (tutorial/ folder) explains each method; section numbers
are given in each function.

All three functions receive the same arguments:

    f : the right-hand side. f(t, y) returns dy/dt as a NumPy array with the
        same shape as y.
    t : the current time t_n (a float).
    y : the current value y_n, a 1-D NumPy array (length 1 for a single
        equation, length 2 for a system of two equations, and so on).
    h : the step size (a float).

and must return y_{n+1} as a NEW NumPy array with the same shape as y.

Rules that the checks enforce:
  * Use only NumPy (no solvers from SciPy or elsewhere).
  * Call f exactly as often as the method needs: Euler once, Heun twice,
    RK4 four times. Keep each stage value in a variable.
  * Do not change y in place: write  y_new = y + ...,  not  y += ...
  * Work with whole arrays; do not convert y to a float.
"""

import numpy as np  # noqa: F401  (you will probably need it)


def euler_step(f, t, y, h):
    """One step of Euler's method (tutorial section 2). Order 1."""
    raise NotImplementedError("Write Euler's method here (tutorial section 2).")


def heun_step(f, t, y, h):
    """One step of Heun's method, the improved Euler method (tutorial section 4). Order 2."""
    raise NotImplementedError("Write Heun's method here (tutorial section 4).")


def rk4_step(f, t, y, h):
    """One step of the classical fourth-order Runge-Kutta method (tutorial section 4). Order 4."""
    raise NotImplementedError("Write the classical RK4 method here (tutorial section 4).")
