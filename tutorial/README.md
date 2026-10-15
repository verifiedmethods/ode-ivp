# Unit A1 tutorial: ODE initial value problems

This tutorial takes you from Euler's method to the classical fourth-order
Runge–Kutta method, and teaches you to *verify* your code: to show, with
evidence, that it does what the theory says. Work through the sections in
order; each one ends with something to do.

| Section | Topic |
|---|---|
| [0](00-setup.md) | Setting up Python and running `verify.py` for the first time |
| [1](01-the-problem.md) | The initial value problem |
| [2](02-euler.md) | Euler's method: write `euler_step` |
| [3](03-error-and-order.md) | Primer: measuring error and convergence order |
| [4](04-heun-and-rk4.md) | Heun's method and classical RK4: write `heun_step` and `rk4_step` |
| [5](05-comparing-methods.md) | Comparing methods properly: error against cost |
| [6](06-stability.md) | Stability and stiffness |
| [7](07-your-report.md) | Reading your verification report |
| [8](08-choosing-a-brief.md) | Choosing a project brief |

**What you need:** a laptop (4 GB of memory is enough), Python 3.10 or later
with NumPy, SciPy and Matplotlib, and about two to four hours for sections 0
to 7. No internet connection is needed once Python is installed.

**What you hand in:** your `student/steps.py`, your verification report, your
completed `student/CONTRIBUTION.md`, and the write-up for your project brief.
