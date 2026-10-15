# 1. The initial value problem

An **initial value problem (IVP)** asks for a function $y(t)$ such that

$$
y'(t) = f(t, y(t)), \qquad y(t_0) = y_0 .
$$

The function $f$ gives the rate of change; the initial value $y_0$ fixes which
solution we want. Examples you may know:

- growth: $y' = ry$, solution $y = y_0 e^{rt}$;
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

The checks use six problems, P1 to P6, listed at the end of your report. Four of
them have exact solutions, so we can measure the error exactly; P5 has no exact
solution and is compared with a very accurate SciPy computation; P6 tests
stability (section 6).
