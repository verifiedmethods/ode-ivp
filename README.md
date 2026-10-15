# Unit A1: ODE initial value problems

Part of **verifiedmethods**: open, verification-first units for the
computational methods used in Nigerian STEM projects and theses.

In this unit you write three methods for $y' = f(t, y)$ (Euler, Heun and the
classical fourth-order Runge–Kutta method), then show with evidence that they
work: observed convergence order, error against cost, and stability. A single
command checks your code and writes a **verification report** that your
supervisor can read in two minutes.

> **Status:** prototype (version 0.1.0.dev0), not yet released.

## Quick start

You need Python 3.10 or later with NumPy, SciPy and Matplotlib
(`python -m pip install -r requirements.txt`). Then, in this folder:

```
python verify.py
```

1. Fill in `student/student_info.txt`.
2. Follow the [tutorial](tutorial/README.md), writing your methods in
   `student/steps.py`.
3. Run `python verify.py` after each change, and open
   `report/verification-report.html` in a browser.
4. When all methods pass, choose a [project brief](briefs/README.md).

Everything runs offline, in a few seconds, on a modest laptop.

## For supervisors

See [supervisors/](supervisors/README.md): how to confirm a report, viva
questions, a marking rubric, and an AI-use statement.

## What is in this folder

| Path | Contents |
|---|---|
| `student/` | The student's files: `steps.py`, `student_info.txt`, `CONTRIBUTION.md` |
| `verify.py`, `vm/` | The checks and the report generator (do not edit) |
| `tutorial/` | The tutorial, in nine short sections |
| `briefs/` | Three project briefs, with data |
| `supervisors/` | Material for supervisors |
| `tests/`, `docs/dev/`, `tools/` | For maintainers (not in the student download) |

## Licence

Code: BSD 3-Clause (see `LICENSE`). Tutorial, briefs and supervisor material:
CC BY 4.0 (see `LICENSE-docs`). Population data: World Bank, CC BY 4.0.

## Citation

See `CITATION.cff`. A DOI will be added at the first release.
