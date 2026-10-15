# 3. Primer: measuring error and convergence order

This section is the heart of the unit. Many project reports compare methods by
printing a table of errors at one step size. That shows *which number is
smaller*, not *whether the code is right*. A convergence study shows both.

## Error

When the exact solution is known, the error at the final time $T$ is

$$
e(h) = \max_i \big| y_N^{(i)} - y^{(i)}(T) \big| ,
$$

the largest error over the components of $y$ (the *max norm*).

## Order

A method of order $p$ has, for small enough $h$,

$$
e(h) \approx C\,h^p .
$$

Taking logarithms, $\log e = \log C + p \log h$: on a **log–log plot** of error
against $h$, the points lie on a straight line of **slope $p$**. Halving $h$
divides the error by about $2^p$: by 2 for Euler, 4 for order 2, 16 for RK4.

From two step sizes $h$ and $h/2$ the **observed order** is

$$
p_{\text{obs}} = \frac{\log\big(e(h) / e(h/2)\big)}{\log 2}.
$$

Your report prints $p_{\text{obs}}$ between successive rows of each error table
(table R1), and gate G4 fits a straight line through several step sizes by least
squares, which is less sensitive to any single point.

## Why the order is not exactly $p$

- **Large $h$ (pre-asymptotic range):** $e(h) \approx C h^p$ only holds when $h$
  is small. For the first rows of a table the observed order can be well away
  from $p$. That is expected, and it is why G4 uses $n = 40$ to $320$ steps.
- **Very small $h$ (rounding):** computers store about 16 significant digits.
  Once the error reaches about $10^{-14}$ to $10^{-15}$, rounding errors stop it
  decreasing, and the observed order drops. For RK4 on P1 this happens after
  about 2000 steps, beyond the tables in your report; brief 1 asks you to find
  where.

## What to do

After your Euler step passes, look at table R1 in your report. Check that the
order column approaches 1 for every problem. Which problem reaches order 1
fastest, and why might that be?
