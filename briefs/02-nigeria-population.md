# Brief 2: Nigeria's population with the logistic model

## Background

The logistic model

$$
P'(t) = r\,P\left(1 - \frac{P}{K}\right)
$$

describes growth at rate $r$ that slows as the population $P$ approaches a
carrying capacity $K$. The file `briefs/data/nigeria_population.csv` contains
Nigeria's total population for 1960 to 2025 (World Bank, CC BY 4.0).

Two models, both starting from $P(1960) = 45.05$ million (time in years from
1960, population in millions):

| Model | $r$ (per year) | $K$ (millions) |
|---|---|---|
| A | 0.0326 | 500 |
| B | 0.0289 | 1000 |

Both were chosen so that they follow the 1960 to 2025 data closely.

## Question

How well do the models fit the data, how far apart are their projections, and
what does that say about what the data can determine?

## What you must produce

1. **Solve both models** from 1960 to 2100 with Euler, Heun and RK4. Choose step
   sizes so that the numerical error is negligible compared with the
   differences you discuss, and **show** that it is: run each method with $h$
   and $h/2$, and use the observed order to estimate the error (tutorial
   section 3). The logistic equation has an exact solution: use it to confirm
   your estimate.
2. **Compare with the data**: plot both models and the data for 1960 to 2025;
   report the largest relative difference for each model.
3. **Compare the projections** for 2050 and 2100. How far apart are they?
4. **Discuss**: two models with very different $K$ fit 65 years of data about
   equally well. Why? (Hint: compare $P$ with $K$ over the data period; what
   does the logistic equation look like when $P \ll K$?) What would the data
   need to show for $K$ to be determined?
5. **Verification report** with all gates passed, and your completed
   `CONTRIBUTION.md`.

## Extension (for strong students)

Estimate $r$ and $K$ by least squares (for example with
`scipy.optimize.curve_fit`, using the exact solution of the logistic equation),
and report the uncertainty of the estimates. You should find that $K$ is far
less certain than $r$. Compare your projections with published population
projections, such as the United Nations World Population Prospects, and
explain the differences.

## Your contribution

The verification of numerical accuracy (item 1), the comparison with data, and
above all the discussion in item 4. Changing $r$ and $K$ alone is not a
contribution.

## Data source

World Bank, World Development Indicators, indicator SP.POP.TOTL (Population,
total), Nigeria; last updated 8 October 2026; licence CC BY 4.0.
