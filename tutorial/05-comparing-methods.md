# 5. Comparing methods properly

RK4 is more accurate than Euler for the same $h$, but each RK4 step costs four
evaluations of $f$ and each Euler step costs one. A fair comparison asks:

> **For a target accuracy, which method needs the least work?**

Work is measured by the number of evaluations of $f$, because for real problems
evaluating $f$ dominates the cost.

## The error–cost plot

Figure R3 in your report plots the error against the number of
$f$-evaluations, on log–log axes. To read it:

1. Choose a target error, say $10^{-6}$, and draw a horizontal line at that
   height.
2. Where each method's line crosses it, read off the work needed.
3. The method furthest to the left is the cheapest for that accuracy.

For a method of order $p$ that uses $s$ evaluations per step, $N$ steps cost
$W = sN$ evaluations, so $e \approx C h^p \propto W^{-p}$: on the error–cost
plot the slope is $-p$. Higher order wins once the target accuracy is small
enough, which is why RK4 is so widely used.

## Do not compare at one step size

A table that shows Euler, Heun and RK4 at a single $h$ hides three things: the
cost of each method, whether each code reaches its theoretical order (which is
the evidence that it is correct), and how the comparison changes with the
target accuracy. Your write-up should use the convergence plot (R2), the
error–cost plot (R3) and the observed orders (R1) instead.
