# Brief 3: When explicit methods fail: stiffness

## Background

Tutorial section 6 shows that on $y' = \lambda y$ each method is stable only
for $h|\lambda|$ below a limit: 2 for Euler and Heun, about 2.785 for RK4.

Consider a linear system with one slow and one fast process (as in a
two-compartment model of a drug moving between blood and tissue):

$$
\begin{aligned}
y_1' &= -50.5\,y_1 + 49.5\,y_2, \\
y_2' &= \;\;\,49.5\,y_1 - 50.5\,y_2,
\end{aligned}
\qquad y(0) = (2, 0), \quad t \in [0, 5].
$$

The matrix has eigenvalues $-1$ and $-100$, with eigenvectors $(1, 1)$ and
$(1, -1)$, so the exact solution is

$$
y(t) = e^{-t} \begin{pmatrix} 1 \\ 1 \end{pmatrix}
     + e^{-100t} \begin{pmatrix} 1 \\ -1 \end{pmatrix}.
$$

After $t \approx 0.1$ the fast part has died away (it is below $10^{-4}$) and the
solution changes slowly, yet the fast eigenvalue still controls stability.

## Question

What limits the step size for each method on this problem: accuracy or
stability? How much work does stiffness cost?

## What you must produce

1. **Theory:** derive the step-size limit for each method on this system from
   the eigenvalues and the stability functions. Check that the exact solution
   above satisfies the equations and the initial condition.
2. **Experiment on P6** ($y' = -50y$): find each method's stability limit by
   experiment (bisection on $h$ is a good approach), and compare with theory.
3. **Experiment on the system:** find the limits again and compare with your
   theory. Plot a stable and an unstable solution for each method.
4. **Cost of stiffness:** for a target error of $10^{-4}$ at $t = 5$ (absolute
   error in the max norm; the solution itself is only about $7 \times 10^{-3}$ there), find the
   largest $h$ that meets the target *and* is stable, for each method. Which
   condition, accuracy or stability, decides it? Compare the work with what the
   accuracy alone would need if the fast process were absent ($y' = -y$).
5. **Verification report** with all gates passed, and your completed
   `CONTRIBUTION.md`.

## Extension

Implement backward Euler for this linear system (each step solves a $2 \times 2$
linear system; `numpy.linalg.solve` is allowed here), show that it is stable for
every $h$, and measure its observed order.

## Your contribution

The derivations in item 1, the experimental design in items 2 and 3, and the
cost analysis in item 4.
