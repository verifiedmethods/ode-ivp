# 2. Euler's method

## Derivation

Taylor's theorem gives, for a smooth solution,

$$
y(t + h) = y(t) + h\,y'(t) + \frac{h^2}{2}\,y''(\xi)
         = y(t) + h\,f(t, y(t)) + \frac{h^2}{2}\,y''(\xi)
$$

for some $\xi$ between $t$ and $t + h$. Dropping the last term gives
**Euler's method**:

$$
y_{n+1} = y_n + h\,f(t_n, y_n).
$$

The term we dropped is the **local truncation error**, of size $O(h^2)$ per
step. To reach a fixed final time $T$ we take $N = (T - t_0)/h$ steps, so these
errors add up to a **global error** of size $O(h)$: Euler's method has
**order 1**. Halving $h$ should roughly halve the error. Section 3 shows how to
check that.

## Your task

Open `student/steps.py` and write `euler_step(f, t, y, h)`. It must:

1. evaluate $f$ once, at $(t, y)$;
2. return $y + h f(t, y)$ as a **new** array (do not write `y += ...`).

Then run `python verify.py`. If your Euler step is correct you will see
`4/4 gates passed` and an observed order close to 1.

## If a gate fails

The report says which gate failed and gives a hint. The most common Euler
mistakes are forgetting the factor $h$, and returning $h f(t, y)$ (the
increment) instead of $y + h f(t, y)$.
