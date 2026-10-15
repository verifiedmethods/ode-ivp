# Viva questions for unit A1

Choose three or four. Ask the student to answer with their own code and report
in front of them. A student who wrote and understood the code can answer them
quickly; a student who copied it usually cannot.

## About the code

1. Show me where your RK4 step evaluates $k_2$. Why at $t + h/2$, and why with
   $y + \tfrac{h}{2} k_1$?
2. Your Heun step calls $f$ twice. What would change if it called $f$ three
   times? (Cost, and gate G2.)
3. Why must the step return a new array instead of changing `y` in place? What
   goes wrong otherwise?
4. Change one weight in your RK4 step (for example $2k_2 \to k_2$) and predict
   what happens to the observed order. Then run `verify.py` and check.

## About the results

5. Why does halving $h$ reduce the RK4 error by about 16? What did your table
   show, and where did that stop being true?
6. Why is the observed order away from its theoretical value for the largest
   step sizes?
7. Using your error–cost plot: which method would you use for an accuracy of
   $10^{-8}$, and why?
8. What is the stability function of Euler's method? What does it say about $h$
   for $y' = -50y$?
9. On the stiff problem, the exact solution is about $10^{-87}$ but your
   computed value grew to thousands. Explain.
10. Why is comparing methods at one step size misleading?

## About the project

11. What does your project add beyond the unit's provided problems?
12. How did you check that the numerical error is small compared with the
    effects you discuss?
