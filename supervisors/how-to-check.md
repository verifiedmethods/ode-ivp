# Confirming a verification report

A report produced on the student's own computer could, in principle, have been
edited. The definitive check is to run the student's code yourself:

1. Download a fresh copy of the unit (the same version as on the report).
2. Copy the student's `student` folder into it, replacing the one there.
3. In that folder, run `python verify.py`.
4. Compare your report with the student's: the gates should match, and so should
   the **student-code fingerprint**. Your **check-suite fingerprint** should
   match the value published for this version on the unit's page.

Alternatively, point the checks at the student's file directly:

```
python verify.py --steps path/to/student/steps.py
```

This takes about two minutes. Passing the gates shows that the code is correct;
it does not show who wrote it. Use a few of the viva questions for that.
