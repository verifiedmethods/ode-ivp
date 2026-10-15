# Unit A1 design: ODE initial value problems

Status: approved 15 October 2026; prototype v0.1.0.dev0 implemented (local, unpublished). The numbers in Section 4 come from a reference run on 15 October 2026 (NumPy 2, SciPy, classical formulas); the script is kept in the private `solutions` repository.

## 1. Purpose

A1 is the first unit of verifiedmethods and the prototype that goes to supervisors with the outreach emails. It teaches three one-step methods for $y' = f(t, y)$, $y(t_0) = y_0$:

| Method | Update | Order | $f$-evaluations per step |
|---|---|---|---|
| Euler | $y_{n+1} = y_n + h f(t_n, y_n)$ | 1 | 1 |
| Heun (improved Euler) | $k_1 = f(t_n, y_n)$, $k_2 = f(t_n + h, y_n + h k_1)$, $y_{n+1} = y_n + \tfrac{h}{2}(k_1 + k_2)$ | 2 | 2 |
| Classical RK4 | $k_1 = f(t_n, y_n)$, $k_2 = f(t_n + \tfrac{h}{2}, y_n + \tfrac{h}{2} k_1)$, $k_3 = f(t_n + \tfrac{h}{2}, y_n + \tfrac{h}{2} k_2)$, $k_4 = f(t_n + h, y_n + h k_3)$, $y_{n+1} = y_n + \tfrac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$ | 4 | 4 |

**Who it is for:** final-year undergraduates (the "comparative study of Euler and Runge–Kutta methods" project), and MSc students as a refresher before block methods (A5).

**What the student does:** writes the three step functions, then carries out and writes up a verification study: observed convergence order, error against cost, and stability. The code is the easy part (PLAN Section 4.2); the analysis is the project.

## 2. Student experience

1. Download the offline zip (or copy the starter repository on GitHub).
2. Fill in `student/student_info.txt`: name, matriculation number, institution, supervisor, and an AI-use disclosure.
3. Implement `euler_step`, `heun_step`, `rk4_step` in `student/steps.py`. Each stub raises `NotImplementedError`.
4. Run `python verify.py`. It runs every check for each method that is implemented, writes `report/verification-report.html` (self-contained, opens offline in any browser; print to PDF if needed) and `report/verification-report.json`, and prints a one-line summary per method.
5. Follow the tutorial and one project brief for the write-up.

Target: from unzip to a first report in under 15 minutes for a student who already has Python, NumPy, SciPy and Matplotlib.

## 3. Test problems

| ID | Problem | Interval | Exact solution | Why |
|---|---|---|---|---|
| P1 | $y' = y$, $y(0) = 1$ | $[0, 1]$ | $e^t$ | The simplest case; links to the stability function. |
| P2 | $y' = y - t^2 + 1$, $y(0) = 0.5$ | $[0, 2]$ | $(t+1)^2 - \tfrac12 e^t$ | Non-autonomous, so wrong time arguments in the stages lower the observed order. Standard textbook example (Burden and Faires), familiar to students. |
| P3 | Logistic: $y' = r y (1 - y/K)$, $r = 0.8$, $K = 10$, $y(0) = 1$ | $[0, 5]$ | $\dfrac{K y_0 e^{rt}}{K + y_0 (e^{rt} - 1)}$ | Nonlinear; used in the population brief. |
| P4 | Harmonic oscillator: $y_1' = y_2$, $y_2' = -y_1$, $y(0) = (1, 0)$ | $[0, 2\pi]$ | $(\cos t, -\sin t)$ | A system: checks vector support; Euler's energy growth is visible. |
| P5 | Lotka–Volterra: $x' = ax - bxy$, $y' = -cy + dxy$, $(a,b,c,d) = (1, 0.1, 1.5, 0.075)$, $(x,y)(0) = (10, 5)$ | $[0, 15]$ | none | Compared with SciPy `solve_ivp` (DOP853, `rtol = atol = 1e-13`). |
| P6 | Stiff test: $y' = \lambda y$, $\lambda = -50$, $y(0) = 1$ | $[0, 4]$ | $e^{\lambda t}$ | Stability limits: $h < 2/|\lambda|$ for Euler and Heun, $h < 2.7853/|\lambda|$ for RK4. |

## 4. Checks

The report separates **gates**, which must pass, from **reported results**, which are shown with the theoretical expectation but carry no pass threshold. The student's write-up interprets the reported results.

### 4.1 Gates (per method)

| # | Gate | Tolerance and reason |
|---|---|---|
| G1 | **One step matches the method.** One step from three stored cases (P2 at $t = 0.4$, P3 at $t = 1$, P4 at $t = 0.5$; $h = 0.1$) agrees with the stored expected values. | Relative difference $\le 10^{-12}$: only rounding separates a correct implementation from the stored values (measured $\le 2.2 \times 10^{-16}$). The expected values are computed by the private reference implementation and stored as numbers; no reference code ships with the unit. |
| G2 | **Cost per step.** Exactly 1, 2 or 4 calls to $f$ per step. | Exact count. This defines the method's cost, and it catches implementations that call a library solver inside the step. |
| G3 | **Works on systems, without side effects.** On P4 the step returns an array of the input's shape, and does not modify the input `y` in place. | Exact. In-place modification is the most common NumPy bug in hand-written RK code. |
| G4 | **Observed convergence order.** On P2 with $n = 20, 40, 80, 160, 320$ steps, the least-squares slope of $\log \|e\|$ against $\log h$ over $n = 40$ to $320$. | $|p_{\text{obs}} - p| \le 0.1$. Reference slopes: Euler 0.98, Heun 1.99, RK4 3.99. The margin covers the pre-asymptotic range without letting a lower-order method pass. |

### 4.2 Reported results (no threshold)

| # | Result | Expected (reference run) |
|---|---|---|
| R1 | Error at $t_{\text{end}}$ against the exact solution for P1 to P4, $n = 10$ to $640$, with the observed order between successive halvings | e.g. P2 at $n = 320$: Euler $1.7 \times 10^{-2}$, Heun $7.7 \times 10^{-5}$, RK4 $1.1 \times 10^{-10}$ |
| R2 | Convergence plot: $\|e\|$ against $h$ on log–log axes for P2, with reference slopes 1, 2 and 4 | straight lines of slope 1, 2, 4 |
| R3 | Cost plot: $\|e\|$ against the number of $f$-evaluations for P2 | RK4 cheapest for any accuracy below about $10^{-3}$ |
| R4 | Agreement with SciPy on P5, relative error at $t = 15$ with $n = 1500$ and $15000$ | Euler $1.3 \times 10^{-1}$ / $1.1 \times 10^{-2}$; Heun $1.4 \times 10^{-4}$ / $1.4 \times 10^{-6}$; RK4 $1.7 \times 10^{-9}$ / $5 \times 10^{-14}$ |
| R5 | Stability on P6 at $0.95\times$ and $1.05\times$ the theoretical step-size limit: $|y(4)|$ | bounded ($\le 3 \times 10^{-5}$) below the limit; grows ($\ge 8 \times 10^{3}$) above it, for all three methods |

### 4.3 Checks on the checks (maintainer tests)

The development test suite runs deliberately broken implementations and requires each to fail at least one gate. A prototype script ran these on 15 October 2026 (RK4 versions; the observed order on P2 is in brackets):

| Common mistake | Caught by (measured) |
|---|---|
| Stages evaluated at $t_n$ instead of $t_n + h/2$ or $t_n + h$ | G1, G4 ($p = 0.99$) |
| Wrong weights, $(k_1 + k_2 + k_3 + k_4)/4$ | G1, G4 ($p = 1.97$) |
| $k_2$ used in place of $k_3$ in $k_4$ | G1, G4 ($p = 3.0$) |
| Missing $h$ in the update | G1, G4 |
| Returning the increment instead of $y_{n+1}$ | G1, G4 |
| Modifying `y` in place (`y += ...`) | G3 only ($p = 4.0$, so only this gate catches it) |
| Scalar-only code (`float(y)`) | G1, G3 |
| Calling `scipy.integrate.solve_ivp` inside the step | G1, G2, G4 |
| Euler code submitted as RK4 | G1, G2, G4 |

## 5. Verification report

**Contents:** unit and version; student information from `student_info.txt`; date; run mode (CI or local); code fingerprint (SHA-256 of `student/steps.py`, or the git commit in CI); check-suite fingerprint (SHA-256 of the files in `vm/`); a gates table and a reported-results table per method; the R2 and R3 plots; the environment (Python, NumPy, SciPy, Matplotlib versions, OS); and a fixed statement of what the report shows and does not show.

**Trust model:**

- **Any self-reported value can be forged.** A determined student can edit the checks, `verify.py` or the CI workflow, including the fingerprints the report prints. No report the student produces is proof on its own.
- **The definitive check is the supervisor's rerun:** copy the student's `student/` folder into a fresh copy of the unit and run `python verify.py` (about two minutes). This uses only the student's `steps.py` and the supervisor's own checks.
- **CI mode raises the bar but is not proof.** The workflow downloads the official `vm/` and `verify.py` from the verifiedmethods release instead of using the student's copy. Getting around it means editing the workflow file, which shows in the repository history.
- **Fingerprints catch accidents and casual edits.** The check-suite fingerprint is published on the unit page for each release, so an edited copy is visible at a glance.
- **Either mode:** the report cannot establish authorship. CONTRIBUTION.md and the viva questions cover that.

**Format:** HTML with inline PNG plots, so it is a single file that opens offline, plus JSON for any later tooling.

## 6. Repository layout

```
ode-ivp/
  README.md                 what the unit is; quick start
  verify.py                 entry point
  student/
    steps.py                euler_step, heun_step, rk4_step (stubs)
    student_info.txt        name, matric no., institution, supervisor, AI-use disclosure
  vm/                       provided code; students do not edit it
    problems.py             P1 to P6
    integrate.py            fixed-step driver; f-evaluation counter
    study.py                convergence and cost studies
    checks.py               gates and reported results
    expected.json           stored one-step values for G1
    report.py               HTML and JSON report
  tutorial/                 the tutorial (also published on the site)
  briefs/                   project briefs, with small data files
  supervisors/              viva questions, rubric, AI-use statement
  .github/workflows/verify.yml   CI for student copies (official vm/ from the release)
  tests/                    maintainer tests, including Section 4.3
  docs/dev/design.md        this document
```

The private `solutions` repository holds the reference implementation and the script that generates `expected.json`. It is never published.

**Dependencies:** Python 3.10 or later; NumPy, SciPy and Matplotlib only. No pytest for students; `verify.py` has its own small runner. Maintainer CI runs on Python 3.10 to 3.13 on Linux and Windows, because most students use Windows laptops.

## 7. Tutorial outline

1. The problem $y' = f(t, y)$, and why we solve it numerically.
2. Euler's method: derivation from the Taylor series; implement `euler_step`; run `verify.py` for the first time.
3. **Primer: measuring error and convergence order.** Error against $h$ on log–log axes, and $p_{\text{obs}} = \log(\|e_h\| / \|e_{h/2}\|) / \log 2$. (This primer becomes Unit 0 later.)
4. Heun and RK4: implement them; read the gates.
5. Comparing methods properly: error against cost, not error at one step size.
6. Stability: $y' = \lambda y$, the stability functions $R(z) = 1 + z$, $1 + z + z^2/2$, $\sum_{k=0}^{4} z^k / k!$, and the stiff example.
7. Reading your verification report: what it shows and what it does not.
8. Choosing a project brief.

## 8. Project briefs (prototype: three)

1. **Comparing Euler, Heun and RK4 properly.** Which method reaches a target accuracy of $10^{-6}$ on P2 and P3 at the lowest cost? Answer with the error–cost plot and observed orders, not with a single step size.
2. **Nigeria's population with the logistic model.** Solve the logistic model with parameters given in the brief, compare the methods, and compare with World Bank population figures for Nigeria (CC BY 4.0, bundled as a small CSV). Stretch goal: estimate $r$ and $K$ by least squares.
3. **When explicit methods fail: stiffness.** Find the stability limits on P6 and on a stiff two-component reaction system by experiment, and compare them with the theory from the stability functions.

Each brief states what counts as the student's contribution, and states that changing parameters alone is not a contribution.

## 9. Supervisor pack (prototype)

- About ten viva questions, for example: "Why does halving $h$ reduce the RK4 error by about 16?"; "Show where your code evaluates $k_2$, and explain why at $t + h/2$"; "What does the stability function of Euler's method say about $h$ for $y' = -50y$?"; "Why is comparing methods at one step size misleading?".
- A one-page rubric for the computational chapter.
- An AI-use statement: AI tools may be used for explanation and debugging, with disclosure in `student_info.txt`. The analysis and write-up must be the student's own. It will be aligned with the NUC framework when that is published.

## 10. Decisions (approved 15 October 2026)

1. Methods: Euler, Heun and classical RK4 for v0.1.
2. Gate G4 tolerance: $\pm 0.1$ on the observed order.
3. Main convergence problem: P2 (Burden and Faires).
4. Student information: name, matriculation number, department, institution, supervisor, AI-use disclosure.
5. Briefs: the three in Section 8.
