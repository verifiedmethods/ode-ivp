# 7. Reading your verification report

Run `python verify.py` and open `report/verification-report.html`.

## The first page

- **Details:** your information from `student_info.txt`, the date, and two
  fingerprints. The **student-code fingerprint** identifies the exact
  `steps.py` that was checked: change one character and it changes. The
  **check-suite fingerprint** identifies the checks themselves.
- **Summary:** for each method, how many of the four gates passed, and the
  observed order.

## Gates (must pass)

| Gate | Question it answers |
|---|---|
| G1 One step matches the method | Does one step give the same numbers as the method, up to rounding? |
| G2 Cost per step | Does the step call $f$ exactly as often as the method requires? |
| G3 Works on systems | Does it work for a system of equations, without changing `y` in place? |
| G4 Observed convergence order | Does the error fall at the rate the theory predicts? |

When a gate fails, the report gives a hint. Fix the code, run
`python verify.py` again, and repeat until all gates pass.

## Reported results (no pass mark)

R1 to R5 have no pass mark: they are the evidence for your write-up. Explain
them in your own words: the observed orders (R1), the convergence and cost plots
(R2, R3), the agreement with SciPy (R4) and the stability results (R5).

## What the report shows, and what it does not

The report shows that the code with that fingerprint passed the checks. It
does **not** show who wrote the code. Your supervisor may check it by running
your `steps.py` in their own copy of the unit, and may ask you to explain any
line of it (for example, why $k_2$ is evaluated at $t + h/2$). Make sure you
can.

## Using AI tools

You may use AI tools to understand the methods or to find a bug, if you say so
in `student_info.txt`. Your analysis and write-up must be your own. If an AI
tool writes your code for you, you will still need to explain every line of it
in your viva.
