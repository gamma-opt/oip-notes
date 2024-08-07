# Lecture 7

## Algebraic formulations

Some text here.

### Transportation Problem

Recall that in {ref}`p1l5:transportation`, we discussed an example of the transportation problem.
In that example, Powerco was distributing electricity from 3 power plants to 4 cities.
Each power plant produced a certain amount of supply that is used to meet the demands of the cities, but also different costs associated with transporting the electricity to a given city.
The objective is to find a distribution plan that minimizes the total cost.

```{code-cell}
:tags: [remove-output]

using JuMP, HiGHS

supply = [35, 50, 40]
demand = [45, 20, 30, 30]
cost = [ 8  6 10 9;
         9 12 13 7;
        14  9 15 5]

model = Model(HiGHS.Optimizer)
```
% Remove the solver printed statement
```{code-cell}
:tags: [remove-cell]

set_attribute(model, "output_flag", false)
```

Next, we define a decision variable for each decision Powerco must make, that is how much power plant {math}`i` (for {math}`i=1,2,3`) sends to city {math}`j` ({math}`j=1,2,3,4`).
This amount cannot be negative, so we also add a nonnegativity constraint in the definition of the variable.

```{code-cell}
@variable(model, x[1:3, 1:4] >= 0);
```

```{note}
This is equivalent to manually adding constrains $x_{11} \ge 0, x_{12} \ge 0, ... x_{34} \ge 0$ manually.
```


The objective is to minimize the cost of power transmission.
```{code-cell}
@objective(model, Min, sum(cost[i,j]*x[i,j] for i in 1:3, j in 1:4));
```

We need to ensure that each plant can only transmit up to its capacity,
```{code-cell}
@constraint(model, c_supply[i in 1:3], sum(x[i,:]) <= supply[i]);
```
and that each city has its demands met.
```{code-cell}
@constraint(model, c_demand[j in 1:4], sum(x[:,j]) >= demand[j]);
```

With the model specified in `JuMP`, we can print it to see the equations directly.
```{code-cell}
print(model)
```

Now, we solve to see what we get.
```{code-cell}
optimize!(model)
is_solved_and_feasible(model)
```

Great, we have a feasible solution.
Let's see what it entails.
```{code-cell}
println("Objective value: ", objective_value(model))
```

```{code-cell}
using DataFrames
a = DataFrame(value.(x), ["City $(i)" for i in 1:4])
display(a)
```

%TODO: Plot this as a graph

The minimum transmission cost is €1020, with the above distribution plan.




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