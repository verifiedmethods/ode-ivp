# Project briefs for unit A1

Choose one brief with your supervisor after all three of your methods pass
their gates. Each brief lists what you must produce and what counts as your own
contribution.

| Brief | Question | Suits |
|---|---|---|
| [1](01-comparing-methods.md) | Which method reaches a target accuracy at the lowest cost? | Any final-year project in numerical analysis |
| [2](02-nigeria-population.md) | What can Nigeria's population data tell us, and what can it not? | Students interested in modelling with real data |
| [3](03-stiffness.md) | When and why do explicit methods fail? | Students heading towards block or implicit methods |

## Using the provided code in your own scripts

Write your scripts in the unit's main folder (next to `verify.py`), so that
Python can find both the provided code and your methods:

```python
from vm.problems import PROBLEMS
from vm.study import convergence_table, successive_orders, fitted_order
from vm.integrate import trajectory
from student.steps import euler_step, heun_step, rk4_step

rows = convergence_table(rk4_step, PROBLEMS["P2"], [20, 40, 80, 160, 320])
for r in rows:
    print(r["n"], r["h"], r["error"], r["evals"])
```

`trajectory(step, f, t0, y0, t_end, n)` returns all times and values, for
plotting a solution. Each row from `convergence_table` contains the number of
steps `n`, the step size `h`, the error at the final time and the number of
$f$-evaluations used.
