# Unit A1: ODE initial value problems

Part of **verifiedmethods**: open, verification-first units for the
computational methods used in Nigerian STEM projects and theses.

In this unit you write three methods for $y' = f(t, y)$ (Euler, Heun and the
classical fourth-order Runge–Kutta method), then show with evidence that they
work: observed convergence order, error against cost, and stability. A single
command checks your code and writes a **verification report** that your
lecturer can inspect alongside your explanation and a rerun of the checks.

> **Status:** pilot prerelease (version 0.1.0a1), for small teaching trials.
>
> Website: https://verifiedmethods.github.io · Contact: abdgafartunde@yahoo.com

## Quick start

Set up once (details in [tutorial section 0](tutorial/00-setup.md)): in this
folder, create a virtual environment and install NumPy, SciPy and Matplotlib.

| Windows (Command Prompt) | macOS and Linux |
|---|---|
| `py -m venv .venv` | `python3 -m venv .venv` |
| `.venv\Scripts\activate` | `source .venv/bin/activate` |
| `python -m pip install -r requirements.txt` | `python -m pip install -r requirements.txt` |

Then, with the environment active:

```
python verify.py
```

1. Fill in `student/student_info.txt`.
2. Follow the [tutorial](tutorial/README.md), writing your methods in
   `student/steps.py`.
3. Run `python verify.py` after each change, and open
   `report/verification-report.html` in a browser.
4. When all methods pass, choose a [project brief](briefs/README.md).

Before submitting, run `python verify.py --strict`. This requires all three
methods to be implemented and pass every gate. Ordinary local runs let you
check unfinished work; GitHub Actions uses strict checking automatically.

The supplied code, data and generated reports run offline after setup. The
tutorial files in this zip are Markdown source; for formatted offline reading,
save the web sections as PDFs or use a Markdown reader with equation support.

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

See `CITATION.cff`. A DOI is planned for the first stable release.
