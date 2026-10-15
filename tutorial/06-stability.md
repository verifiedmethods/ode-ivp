# 6. Stability and stiffness

## The test equation

Apply each method to $y' = \lambda y$ with $\lambda < 0$. The exact solution
$y = e^{\lambda t}$ decays to zero. One step of each method multiplies $y_n$ by
a fixed number $R(z)$, where $z = h\lambda$:

| Method | Stability function $R(z)$ |
|---|---|
| Euler | $1 + z$ |
| Heun | $1 + z + \dfrac{z^2}{2}$ |
| RK4 | $1 + z + \dfrac{z^2}{2} + \dfrac{z^3}{6} + \dfrac{z^4}{24}$ |

(Check the Euler and Heun rows yourself by applying the formulas to
$f(t, y) = \lambda y$.) After $n$ steps, $y_n = R(z)^n y_0$, so the numerical
solution decays only if $|R(z)| < 1$.

For real negative $z$ this gives a **step-size limit**:

| Method | Stable for |
|---|---|
| Euler | $h\,\lvert\lambda\rvert < 2$ |
| Heun | $h\,\lvert\lambda\rvert < 2$ |
| RK4 | $h\,\lvert\lambda\rvert < 2.785$ |

## Stiffness

Problem P6 is $y' = -50y$. Its solution is essentially zero after $t = 0.2$, yet
Euler's method needs $h < 2/50 = 0.04$ for the whole interval, or the computed
solution grows without bound. When stability, not accuracy, forces the step
size to be small, the problem is called **stiff**.

Result R5 in your report runs each method just below and just above its limit.
Below the limit the solution decays; above it, it grows to thousands or
millions, although the exact solution is about $10^{-87}$.

Stiff problems are common: chemical reactions with fast and slow rates, circuit
models, and many epidemic models with fast and slow compartments. The remedy is
an **implicit** method, such as backward Euler,
$y_{n+1} = y_n + h f(t_{n+1}, y_{n+1})$, whose stability function
$1/(1 - z)$ satisfies $|R(z)| < 1$ for every $z < 0$. Implicit methods, and the
block methods common in Nigerian research, come in a later unit.
