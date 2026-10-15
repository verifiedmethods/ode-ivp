# 0. Setting up

## Install Python (once)

Either of these works:

- **Anaconda or Miniconda** (recommended on Windows): it comes with NumPy,
  SciPy and Matplotlib. Use the "Anaconda Prompt" as your terminal.
- **Python from python.org**: then install the three packages once, while you
  have internet access:

  ```
  python -m pip install -r requirements.txt
  ```

Check your installation:

```
python -c "import numpy, scipy, matplotlib; print('ready')"
```

## Run the checks for the first time

Open a terminal in this unit's folder (the folder that contains `verify.py`)
and run:

```
python verify.py
```

You should see:

```
verifiedmethods A1: ODE initial value problems (version ...)
  Euler          euler_step is not implemented yet.
  Heun           heun_step is not implemented yet.
  Classical RK4  rk4_step is not implemented yet.
Report: .../report/verification-report.html
```

That is correct: you have not written anything yet. Open the report file in
any web browser to see what it looks like.

## Fill in your details

Open `student/student_info.txt` in a text editor and fill in every line. These
details appear at the top of your report.

## The folders

| Folder or file | What it is | Do you edit it? |
|---|---|---|
| `student/steps.py` | Your three step functions | **Yes** |
| `student/student_info.txt` | Your details and AI-use disclosure | **Yes** |
| `student/CONTRIBUTION.md` | Contribution statement for your appendix | **Yes** |
| `verify.py`, `vm/` | The checks and the report generator | No |
| `tutorial/`, `briefs/` | This tutorial and the project briefs | No |
