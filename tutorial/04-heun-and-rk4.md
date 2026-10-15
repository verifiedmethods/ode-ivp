# 4. Heun's method and classical RK4

Euler's method uses the slope only at the start of the step. **Runge–Kutta
methods** evaluate $f$ several times within the step (the *stages*) and combine
the slopes to cancel more terms of the Taylor series.

## Heun's method (improved Euler), order 2

Take an Euler step to predict the end of the step, then average the slopes at
both ends:

$$
\begin{aligned}
k_1 &= f(t_n, y_n), \\
k_2 &= f(t_n + h,\; y_n + h k_1), \\
y_{n+1} &= y_n + \frac{h}{2}\,(k_1 + k_2).
\end{aligned}
$$

Two evaluations of $f$ per step; global error $O(h^2)$.

## Classical fourth-order Runge–Kutta (RK4), order 4

$$
\begin{aligned}
k_1 &= f(t_n, y_n), \\
k_2 &= f\!\left(t_n + \tfrac{h}{2},\; y_n + \tfrac{h}{2} k_1\right), \\
k_3 &= f\!\left(t_n + \tfrac{h}{2},\; y_n + \tfrac{h}{2} k_2\right), \\
k_4 &= f(t_n + h,\; y_n + h k_3), \\
y_{n+1} &= y_n + \frac{h}{6}\,(k_1 + 2k_2 + 2k_3 + k_4).
\end{aligned}
$$

Four evaluations of $f$ per step; global error $O(h^4)$.

## Your task

Write `heun_step` and `rk4_step` in `student/steps.py`, then run
`python verify.py`.

Points to watch (each is caught by a gate):

- Evaluate each stage at the right **time**: $t_n$, $t_n + h/2$ or $t_n + h$.
  Problem P2, $y' = y - t^2 + 1$, depends on $t$, so a wrong time lowers the
  observed order.
- Use $k_3$, not $k_2$, inside $k_4$.
- Store each $k_i$ in a variable and call $f$ exactly 2 (Heun) or 4 (RK4) times.
- Build a new array for $y_{n+1}$; do not change `y` in place.

## A question for your write-up

All three methods are "Runge–Kutta methods" with 1, 2 and 4 stages. Is it true
in general that $s$ stages give order $s$? (Look up the *Butcher barriers*: no
explicit Runge–Kutta method of order 5 has only 5 stages.)
