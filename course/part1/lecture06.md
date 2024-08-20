---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.2
kernelspec:
  display_name: Julia 1.10.4
  language: julia
  name: julia-1.10
---

# Lecture 6 - Symbolic formulation

## Motivation for symbolic formulations

One aspect that might have become evident is that, as models start to have more numerous entities, such as production plants, demand points, arcs, and time periods, very quickly the mathematical programming model becomes less and less human readable. This, in turn, compromises model validation and maintenance. Furthermore, it makes it inefficient and prone to error to make updates in the model's input data.

A best-practice approach is to have the *model data* separated from the *model formulation*. Effectively, this dissociates the maintenance of the model and its data source, while allowing for the creation of multiple instantiations of the same model.

To achieve that, we must rely on abstract entities that represent the elements of the problem. We describe those next.

## Elements of a symbolic formulation

### Model data

The model data, or input data, is represented by *indices* and their *sets* and *parameters*.

- **Indices and sets**: these represent entities in the problem that are discrete and can be grouped by what they represent in the model.
- **Parameters**: are numerical values representing quantities that are associate to indices or combinations of indices.

We have come across these before. For example, in the transportation problem, we defined the plants as $i = 1, 2, 3$. If we define the set $I = \braces{1,2,3}$, then we can say that the cities are defined as $i \in I$. Now, we can represent the production capacity of each plant as $C_i$ for $i \in I$.

```{note}
It is a convention to represent sets with capital letters and indices with lower case letters (often the same).
```

### Model formulation

The model formulation is composed by *variables*, *objective function*, and *constraints*. We have considered their role in detail before, so we now focus on how to pose them such that they are data independent.

Let us start with **decision variables**. The convention is to index decision variables with the defined indices. So, suppose we have a index set $j \in J$, representing some entity in our model. Then, to define a decision variable for each of these, we define $x_j$, $\forall j \in J$. This indicates that we have a decision variable $x$ for each index $j$ in the set $J$.

This can be extended to as many indices as necessary. Going back to our transportation problem, where we had $i \in I$ plants and $j \in J$ demand points, our flow variables could be represented as $x_{ij}$, $\forall i \in I, j \in J$.

Once we have variables defined, we can use them to pose objective functions. A compact way to do so is to express them as summation of products between parameters and variables. Coming back to our variable $x_j$, $\forall j \in J$, suppose we have a cost coefficient $c_j$, $j \in J$, associated with each. Then, our objective function can be posed as

```{math}
\mini_{x} c_1x_1 + c_2x_2 + \dots + c_{|J|}x_{|J|} \equiv \mini_{x} \sum_{j \in J} c_jx_j.
```

Notice a couple of nice features about this way of posing our objective function. First, there is the fact that it is a much more compact notation, which can be quickly read by a human. Second, it *remains compact*, regardless of the cardinality of the index set $J$ (represented $| \ \cdot \ |$).

The same logic can be applied to constraints, being the main difference that we must consider not only the summation domains, but also the *replication* domain (or the indexing) of the constraints. Suppose we have a parameter $a_{ij}$, for $i \in I, j \in J$ multiplying our variables $x_j$, $j \in J$ and that their combined sum must be less or equal a quantity $b_i$, defined for each $i \in I$. For simplicity, assume for now that $|I| = |J| = 2$. Assume that each constraint must be summed in the domain of $i \in I$ and replicated $j \in J$. Since we have two indices for each set, we would have the following constraints

```{math}
\begin{aligned}
    & a_{11}x_1 + a_{12} \le b_1 \\
    & a_{21}x_1 + a_{22} \le b_2.
\end{aligned}
```

The above can be equivalently represent by the single constraint statement

```{math}
    \sum_{j \in J} a_{ij}x_{j} \le b_i, \ \forall i \in I.
```

Again, notice how much more compact is this set of constraints. Again, with a single statement we can represent sets of constraints at once, in a far more compact notation. Let us explore these ideas a bit further returning to our transportation problem.

## Example - transportation problem

Let's revisit our transportation problem and pose it as model written in symbolic formulation.

### Indices and sets

The transportation problem has two sets of entities: a set of plants $i \in I$ and a set of demand points (clients) $j \in J$.

### Parameters

There are three parameters: 

- plant capacities, represented by $C_i$, $i \in I$,
- demand amounts at each client, represented by $D_j$, $j \in J$,
- unit transportation cost between each plant $i$ and demand point $j$, represented by $T_{ij}$, $i \in I$, $j \in J$. 

### Variables

Our transportation model has only one type of decision variable: let $x_{ij}$ be the amount transported from plan $i$ to client $j \in J$. Naturally, we must enforce that these amounts are not negative.

### Objective function

Our objective is to minimise the aggregated transportation cost, which is defined as

```{math}
:label: p1l6:obj
\mini_x \sum_{i \in I} \sum_{j \in J} T_{ij}x_{ij}.
```

Notice how we need a double summation since we have two indices to sum over.

### Constraints

There are two main constraint sets in the transportation problem: 

- **Supply limit**: all that is send from each plant $i \in I$ must be less than or equal to the plant $i$ capacity $C_i$. Thus, we have that

```{math}
\sum_{j \in J} x_{ij} \le C_i, \forall i \in I.
```

- **Demand fulfillment**: the accumulated total that is sent from plants $i \in I$ to each client $j \in J$ must be equal to the client $j$ demand $D_j$. Therefore, we have

```{math}
\sum_{i \in I} x_{ij} = D_j, \forall j \in J.
```

Putting the whole model together, we obtain

```{math}
\begin{equation}
\begin{aligned}
    \mini_x & \sum_{i \in I} \sum_{j \in J} T_{ij}x_{ij} \\
    \st & \sum_{j \in J} x_{ij} \le C_i, \forall i \in I \\
    & \sum_{i \in I} x_{ij} = D_j, \forall j \in J \\
    & x_{ij} \ge 0, \ \forall i \in I, j \in J.
\end{aligned}
\end{equation}
```

## Code

### Small problem

Recall that in {numref}`p1l5:transportation`, we discussed an instance of the transportation problem.
Here, we show how to solve the problem programmatically.
First, we determine the parameters of our problem.

```{code-cell}
:tags: [remove-output]

using JuMP, HiGHS

supply = [35, 50, 40]
demand = [45, 20, 30, 30]
cost = [ 8  6 10 9;
         9 12 13 7;
        14  9 15 5]
```

Then, we wrap the model in a function, so that we can easily use it for different instances of the problem.

```{code-cell}
function solve_transportation(cost, supply, demand)
    I,J = size(cost)

    model = Model(HiGHS.Optimizer)
    @variable(model, x[1:I, 1:J] >= 0)
    @objective(model, Min, sum(cost[i,j]*x[i,j] for i in 1:I, j in 1:J))
    @constraint(model, c_supply[i in 1:I], sum(x[i,:]) <= supply[i])
    @constraint(model, c_demand[j in 1:J], sum(x[:,j]) >= demand[j])

    set_attribute(model, "output_flag", false) # Remove the solver printed statement
    optimize!(model)
    @assert is_solved_and_feasible(model)

    return value.(x), model
end

x, model = solve_transportation(cost, supply, demand);
```

In order to solve the problem, we first need to define the model.
In `JuMP`, this requires creating a `Model` object, which is given an optimizer that actually implements the optimisation algorithms.

```julia
model = Model(HiGHS.Optimizer)
```

Next, we define a decision variable for each decision Powerco must make, that is how much power plant {math}`i` (for {math}`i=1,2,3`) sends to city {math}`j` ({math}`j=1,2,3,4`).
`JuMP` allows one to set nonnegativity constraints of variables in their definition, so we make use of that as well.

```julia
@variable(model, x[1:I, 1:J] >= 0);
```

```{note}
This is equivalent to manually adding the constrains $x_{11} \ge 0, x_{12} \ge 0, ... x_{34} \ge 0$.
```

The objective can be specified using a comprehension, writing out all terms in the double summation {eq}`p1l6:obj`, which we can then sum over.
```julia
@objective(model, Min, sum(cost[i,j]*x[i,j] for i in 1:I, j in 1:J));
```
Multiple constraints obeying the same form can be defined and labeled in a single statement.
Here is the supply limit:
```julia
@constraint(model, c_supply[i in 1:I], sum(x[i,:]) <= supply[i]);
```
and here is demand fulfillment.
```julia
@constraint(model, c_demand[j in 1:J], sum(x[:,j]) >= demand[j]);
```

With the model specified in `JuMP`, we can print it to see the equations directly.
```{code-cell}
print(model)
```

At the end of the function, we perform the optimisation and ensure that the problem is solved, so that the returned values are ready for our use.
```julia
optimize!(model)
@assert is_solved_and_feasible(model)
```

We can inspect both the resulting objective value and the decision variables themselves.
```{code-cell}
println("Objective value: ", objective_value(model))
```

```{code-cell}
using DataFrames
a = DataFrame(x, ["City $(i)" for i in 1:4])
display(a)
```

The minimum transmission cost is €1020, with the above distribution plan.

In this small problem, we had 12 decision variables (one for each plant-city combination) as well as a non-negativity constraint for each of the variables, 3 constraints to ensure supply is not exceeded, and 4 constraints to ensure demand is met, for a total of 19 constraints.
However, with symbolic formulation, we can immediately handle much larger models.

### Larger instance

Here, we randomly generate an instance of the problem with $I=50$ plants and $J=100$ clients.
Here, the transportation costs are defined as the distance between a given plant and a client.

```{code-cell}
using Random
Random.seed!(42)

I = 50 # factories
J = 100 # clients
 
x_coord = 1000*rand(I+J)
y_coord = 1000*rand(I+J)

C = 30*rand(I) # factory capacity
D = 10*rand(J) # client demand

T = zeros(I,J) # cost 

for i = 1:I
    for j = 1:J
        T[i,j] = 10*sqrt((x_coord[i] - x_coord[j+I])^2 + 
            (y_coord[i] - y_coord[j+I])^2)
    end
end
        
if sum(C) < sum(D)
    C[N] = C[N] + sum(D) - sum(C)  # Adjust capacity to obtain feasibility
end
```

Since it is the same problem, we can just reuse the function we defined above.

```{code-cell}
x, model = solve_transportation(T, C, D);
```

Since there are too many variables, printing the solution is not viable.
However, we can visualise it.

```{code-cell}
:tags: ["remove-input"]
using CairoMakie

f = Figure()
ax = Axis(f[1,1])

for i=1:I
    for j=1:J
        if x[i,j] > 0.0
            lines!(ax, x_coord[[i, j+I]], y_coord[[i, j+I]], color=:black)
        end
    end
end

scatter!(ax, x_coord[1:I], y_coord[1:I], label="Plants")
scatter!(ax, x_coord[I+1:I+J], y_coord[I+1:I+J], label="Clients")
axislegend()
f
```
