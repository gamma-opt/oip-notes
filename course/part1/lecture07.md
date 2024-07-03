# Lecture 7

## Algebraic formulations

Some text here.

### Transportation Problem

Recall that in {ref}`p1l5:transportation`, we discussed an example of the transportation problem.
In that example, Powerco was distributing electricity from 3 power plants to 4 cities.
Each power plant produced a certain amount of supply that is used to meet the demands of the cities, but also different costs associated with transporting the electricity to a given city.
The objective is to find a distribution plan that minimizes the total cost.

TODO: Copy the original model here? I'm not sure if it can be done programmatically (since its on a different file and `glue` is python only).

In this small problem, we had 12 decision variables (one for each plant-city combination) as well as a non-negativity constraint for each of the variables, 3 constraints to ensure supply is not exceeded, and 4 constraints to ensure demand is met, for a total of 19 constraints.

Now, consider a generalized version of this problem where we have {math}`n` power plants and {math}`m` cities to deliver to.
Then, we can represent the supply of each plant as a vector {math}`s\in\reals^{n}` and the demand of each city as {math}`d\in\reals^{m}`.
Finally, the costs and the decision variables become matrices {math}`c\in\reals^{n\times m}` and {math}`x\in\reals^{n\times m}`.
With these at hand, we can formulate the general transportation problem as

```{math}
:nowrap:

\begin{align*}
\mini &\sum_{i=1}^n \sum_{j=1}^m c_{ij}x_{ij} \\
\st &\sum_{j=1}^m x_{ij} \leq s_i, ~\forall i=1\dots n \\
&\sum_{i=1}^n x_{ij} \geq d_j, ~\forall j=1\dots m \\
&x_{ij}\geq 0, ~\forall i=1\dots n, \forall j=1\dots m
\end{align*}
```

### Production Planning

I'm not sure if the form of the example in lec 5 is good, so I'll write this later.