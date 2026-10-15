# 1. The initial value problem

An **initial value problem (IVP)** asks for a function $y(t)$ such that

$$
y'(t) = f(t, y(t)), \qquad y(t_0) = y_0 .
$$

The function $f$ gives the rate of change; the initial value $y_0$ fixes which
solution we want. Examples you may know:

- growth: $y' = ry$, solution $y = y_0 e^{r(t - t_0)}$;
- logistic population growth: $y' = ry(1 - y/K)$;
- a mass on a spring, written as a system of two first-order equations:
  $y_1' = y_2$, $y_2' = -y_1$.

For most problems in science and engineering there is no formula for $y(t)$, so
we compute approximations $y_n \approx y(t_n)$ at times
$t_n = t_0 + nh$, where $h$ is the **step size**. A **one-step method** computes
$y_{n+1}$ from $y_n$ alone:

$$
y_{n+1} = y_n + h\,\Phi(t_n, y_n, h).
$$

Different methods use different increment functions $\Phi$. In this unit you
will write three of them.

## Systems

If $y$ has several components (a *system* of equations), everything works the
same with $y$ a vector. In the code, `y` is always a 1-D NumPy array: length 1
for a single equation, length 2 for the spring, and so on. Write your methods
with whole-array arithmetic (`y + h * k1`), and they will work for any length.

## The test problems

The checks use six problems. Five have exact solutions, so the error can be
measured exactly; P5 has none and is compared with a very accurate SciPy
computation.

| Problem | Equation | Interval | Exact solution | Used for |
|---|---|---|---|---|
| P1 | $y' = y$, $y(0) = 1$ | $[0, 1]$ | $e^t$ | error tables |
| P2 | $y' = y - t^2 + 1$, $y(0) = 0.5$ | $[0, 2]$ | $(t+1)^2 - \tfrac12 e^t$ | error tables, gate G4 |
| P3 | $y' = 0.8\,y\,(1 - y/10)$, $y(0) = 1$ | $[0, 5]$ | logistic curve | error tables |
| P4 | $y_1' = y_2$, $y_2' = -y_1$, $y(0) = (1, 0)$ | $[0, 2\pi]$ | $(\cos t, -\sin t)$ | error tables, gate G3 |
| P5 | $x' = x - 0.1xy$, $y' = -1.5y + 0.075xy$, $(x, y)(0) = (10, 5)$ | $[0, 15]$ | none | comparison with SciPy |
| P6 | $y' = -50y$, $y(0) = 1$ | $[0, 4]$ | $e^{-50t}$ | stability (section 6) |
