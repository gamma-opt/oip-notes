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
  display_name: Julia 1.10.3
  language: julia
  name: julia-1.10
---

# Lecture 9

## Set Covering (Facility location)

Note: set covering seems like a good opportunity to have an interactive visualisation for the simple problem.

This example is based on Section 9.2 of {cite}`winston2022operations`.

There are six cities in Kilroy County.
The county must determine where to build fire stations.
The county wants to build the minimum number of fire stations needed to ensure that at least one station is within 15 minutes of each city.
The time (in minutes) required to get between the cities are shown in {numref}`table_setcover`.
Formulate an IP that will tell Kilroy where fire stations should be built.

```{list-table} Distance between cities (in minutes)
:name: table_setcover
:header-rows: 1
:stub-columns: 1

* - 
  - City 1
  - City 2
  - City 3
  - City 4
  - City 5
  - City 6
* - City 1
  - 0
  - 10
  - 20
  - 30
  - 30
  - 20
* - City 2
  - 10
  - 0
  - 25
  - 35
  - 20
  - 10
* - City 3
  - 20
  - 25
  - 0
  - 15
  - 30
  - 20
* - City 4
  - 30
  - 35
  - 15
  - 0
  - 15
  - 25
* - City 5
  - 30
  - 20
  - 30
  - 15
  - 0
  - 14
* - City 6
  - 20
  - 10
  - 20
  - 25
  - 14
  - 0
```

### Solution

```{code-cell}
:tags: [remove-output]

using JuMP, HiGHS

time = [ 0 10 20 30 30 20;
        10  0 25 35 20 10;
        20 25  0 15 30 20;
        30 35 15  0 15 25;
        30 20 30 15  0 14;
        20 10 20 25 14  0]

model = Model(HiGHS.Optimizer)
```

% Remove the solver printed statement
```{code-cell}
:tags: [remove-cell]

set_attribute(model, "output_flag", false)
```

We start by defining the decision variables, which represent whether a fire station gets built in a given city.
Note that since there are only two options, these are binary variables
```{code-cell}
:tags: [remove-output]

@variable(model, x[1:6], Bin)
```

The objective is to minimize the number of fire stations
```{code-cell}
@objective(model, Min, sum(x))
```

Lastly, we want every city to have a fire station within 15 minutes of it.
How do we encode that?
Consider City 1, which has itself and City 2 within 15 minutes of distance.
Then, what we do want could be expressed as
```{math}
x_1+x_2 \geq 1
```
so both cities not having a station could be excluded.
We add such constaints for every city.
```{code-cell}
for i in 1:6
    @constraint(model, sum(x[(time .<= 15)[i,:]]) >= 1)
end
```

At the end, our model looks like this.
```{code-cell}
print(model)
```
Let's solve it.

```{code-cell}
optimize!(model)
is_solved_and_feasible(model)
println("Objective value: ", objective_value(model))
println("x: ", value.(x))
```

Thus it is sufficient to build 2 fire stations, in cities 2 and 4.

## Travelling Salesperson Problem

The travelling salesperson problem (TSP) is one of the most famous combinatorial optimisation problems, perhaps due to its interesting mix os simplicity while being computationally challenging.
Assume that we must visit a collection of {math}`n` cities at most once, and return to our initial point, forming a so-called _tour_. When travelling from city {math}`i` to a city {math}`j`, we incur in the cost {math}`C_{ij}`, representing, for example, distance or time. 
Our objective is to minimise the total cost of our tour.
Notice that this is equivalent to finding the minimal cost permutation of {math}`n-1` cities, discarding the city which represents our starting and end point.

```{figure} ../figures/random_graph.svg
:name: random_graph
:align: center

An example collection of cities (or points) for which we'd like to find the minimum cost tour for.
```

TODO: Add interactive visualization? or just solved graph at the end?

To pose the problem as an integer programming model, let us define {math}`x_{ij}=1` if city {math}`j` is visited directly after city {math}`i`, and {math}`x_{ij}=0` otherwise.
Let {math}`N=\{1,\dots,n\}` be the set of cities.
We assume that {math}`x_{ii}` is not defined for {math}`i\in N`.
A naive model for the travelling salesperson problem would be

```{math}
:nowrap:

\begin{align*}
\mini_{x} &\sum_{i\in N}\sum_{j\in N} C_{ij}x_{ij} \\
\st &\sum_{j\in N\setminus\{i\}}x_{ij}=1,~\forall i\in N \\
&\sum_{i\in N\setminus\{j\}} x_{ij}=1,~\forall j\in N \\
&x_{ij}\in\{0,1\},~\forall i,\forall j\in N : i\neq j
\end{align*}
```

However, this formulation has an issue.
Although it can guarantee that all cities are only visited once, it cannot enforce an important feature of the problem which is that the tour cannot present disconnections, i.e., contain sub-tours.
In other words, the salesperson must physically visit from city to city in the tour, and cannot "teleport" from one city to another.

```{figure} ../figures/tsp_subtours.svg
:name: subtours
:align: center

A feasible solution for the naive TSP model. Notice the two sub-tours formed.
```

In order to prevent sub-tours, we must include constraints that can enforce the full connectivity of the tour.
There are mainly two types of such constraints.
The first is called _cut-set constraints_ and is defined as
```{math}
\sum_{i\in S}\sum_{j\in N\setminus S} x_{ij}\geq 1,~\forall S\subset N, 2\leq |S|\leq n-1.
```

The cut-set constraints act by guaranteeing that among any subset of nodes {math}`\subseteq N` there is always at least one arc {math}`(i,j)` connecting one of the nodes in {math}`S` and a node not in {math}`S`.

An alternative type of constraint is called _sub-tour elimination_ constraint and is of the form
```{math}
\sum_{i\in S}\sum_{j\in S}x_{ij}\leq |S|-1,~\forall S\subset N,2\leq |S|\leq n-1.
```

Differently from the cutset constraints, the sub-tour elimination constraints prevent the cardinality of the nodes in each subset from matching the cardinality of arcs within the same subset.

There are some differences between these two constraints and, typically cutset, constraints are preferred for being stronger.
In any case, either of them suffers from the same problem: the number of such constraints quickly becomes computationally prohibitive as the number of nodes increases. 
This is because one would have to generate a constraint to each possible node subset combination from sizes 2 to n − 1.

A possible remedy to this consists of relying on delayed constraint generation. 
In this case, one can start from the naive formulation T SP and from the solution, observe whether there are any sub-tours formed.
That being the case, only the constraints eliminating the observed sub-tours need to be generated, and the problem can be warm-started.
This procedure typically terminates far earlier than having all of the possible cutset or sub-tour elimination constraints generated.

```{figure} ../figures/tsp_feasible.svg
:name: feasible
:align: center

A feasible solution without subtours.
```