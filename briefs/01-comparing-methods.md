# Brief 1: Comparing Euler, Heun and RK4 properly

## Question

For a target accuracy, which of the three methods needs the least work, and how
does the answer change with the target?

## What you must produce

1. **Convergence study** on P2 and P3: errors for at least six step sizes (each
   half the previous), observed orders between successive step sizes, and a
   least-squares order from the asymptotic range. State which range you used and
   why.
2. **Error–cost plot** for both problems (error against number of
   $f$-evaluations, log–log), with all three methods.
3. **Answer the question** for three targets: $10^{-2}$, $10^{-6}$ and
   $10^{-10}$. For each target and problem, estimate the number of
   $f$-evaluations each method needs (interpolate on the log–log plot, or use
   $e \approx C h^p$ fitted to your data). Which method is cheapest? Is there a
   target for which Euler or Heun beats RK4?
4. **Rounding:** find, for RK4 on P1, the step size below which the error stops
   decreasing. Explain why.
5. **Verification report** with all gates passed, and your completed
   `CONTRIBUTION.md`.

## Your contribution

Your contribution is the study design (step sizes, ranges, targets), the
estimates of work for each target, and the interpretation. Choose and justify
one further problem of your own with a known exact solution (for example from
your physics or engineering courses) and repeat items 1 to 3 on it.

## Common pitfalls

- Comparing at a single step size (see tutorial section 5).
- Fitting the order over the pre-asymptotic range or into the rounding floor.
- Plotting error against $h$ only, which hides the cost.
