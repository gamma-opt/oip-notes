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
  display_name: Julia 1.10.5
  language: julia
  name: julia-1.10
---

# Combinatorial optimisation

So far, we have discussed a few, sometimes overlapping, varieties of mathematical programming: linear optimisation, mixed-integer optimisation, and convex optimisation.
Another class we will now consider is **combinatorial optimisation**, which involves finding an optimal solution from a finite solution space that often can be thought of as choosing a combination of items or options.
A generic combinatorial optimisation problem can be expressed as finding the minimum cost feasible subset $S$, i.e.
```{math}
\min_{S\subseteq N} \{ \sum_{i\in S} c_i | S\in \mathcal{F} \}
```
where $N$ is a set of items, $c_i$ is the cost associated with item $i$, and $\mathcal{F}\subset 2^S$ is the set of feasible solutions.

For example, the Traveling Salesperson Problem we discussed in {numref}`tsp-mip` is a classical example of combinatorial problems.
As a quick reminder, the problem is about charting a route around $n$ cities so that each is visited exactly once, and then returning to the starting city.
We had formulated this problem using variables $x_{ij}$, where $x_{ij}=1$ if the route goes from city $i$ to $j$ directly, and $x_{ij}=0$ otherwise.
The goal is to find the shortest route, i.e. minimize the cost of the route
```{math}
\mini_{x} \sum_{i\in N}\sum_{j\in N} C_{ij}x_{ij}
```
where $C_{ij}$ is the cost of going from city $i$ directly to $j$.
As an integer problem, we also needed to add some constraints to obtain feasible routes, but we will not repeat them here.

Another well known combinatorial problem is the 0-1 Knapsack Problem.
Here, we are given a set of items $x_i$, each with some cost $c_i$ and value $v_i$, along with a budget $B$ available for spending.
The goal is to choose a subset of the items within our budget tha maximizes the value.
As an integer problem, we can formulate this using the objective function
```{math}
\maxi \sum_{i=1}^n v_ix_i
```
with a constraint to not exceed the budget
```{math}
\sum_{i=1}^n c_ix_i \leq b.
```

% TODO: Add knapsack illustration

Modeling a choice like selecting an item is exactly what binary variables are for, so one may wonder how are these problems special enough to warrant their own category.
It is true that combinatorial optimisation problems can be formulated and solved as integer problems.
But recall that going from linear to mixed-integer problems introduced difficulty due to losing the continuity of variables.
Here, problems are even more discrete and linear dependencies are seldom available.
So how can these problems be solved then?

## The Combinatorial Explosion

Having finitely many decisions to make, each with a finite number of options, leads to combinatorial problems having a finite solution space.
This means that in theory, all these problems can be solved by enumeration, i.e. trying each solution one-by-one.
The problem is that very quickly the problems get too big for this to be feasible, due to their combinatorial nature.

For example, in a TSP with $n$ cities, there are $(n-1)!$ feasible routes, since at city 1 there are $n-1$ choices, then at city 2 there are $n-2$ and so on.
This gives $362880$ feasible solutions when $n=10$ and $1.22*10^{17}$ when $n=20$.
In the case of the Knapsack problem, the number of possible selections is $2^n$.
For a budget that would accept half of these selections, there would be $2^{n-1}$ feasible solutions.

While for small $n$ these numbers may not pose a problem, very quickly they exceed the realm of what is computable in a reasonable amount of time.
Some common functions are plotted below.
Note that the $y$-axis is on a $\log_2$ scale, so the difference between the lines is very large.

```{code-cell}
:tags: [remove-input]
using CairoMakie

x = 2:20
xlims = (1, π)

fig = Figure(size = (1200, 800), fontsize=24)

ax1 = Axis(fig[1,1], xlabel=L"n", ylabel=L"\log_2 ~f(n)", yscale=log2)

lines!(ax1, x, factorial; linewidth = 3, label=L"n!")
lines!(ax1, x, exp; linewidth = 3, label=L"e^n")
lines!(ax1, x, x -> x^2; linewidth = 3, label=L"n^2")
lines!(ax1, x, log2; linewidth = 3, label=L"\log_2(n)")

axislegend(position=:lt)

fig
```

```{admonition} Runtime of algorithms and computational complexity
:class: dropdown

The question of how the time/memory requirements of algorithms increase for larger inputs, i.e. the asymptotic behavior of algorithms, is key to the fields of theoretical computer science and algorithmic analysis.
Assuming that checking every route takes an equal amount of time $c$ independent of the specific route, a naive TSP algorithm in the worst case would require $c*(n-1)!$ amount of time, often denoted $O(n!)$ to highlight only the dependence on the input.
The goal in these fields is to develop efficient algorithms, where efficient ideally means _linear_, i.e. $O(n)$ or more frequently _polynomial time_, such as $O(n^2)$ or $O(n^3)$.

However, in real-life uses of these algorithms, it is important to keep in mind that asymptotic behavior does not always mirror real-life performance.
In many algorithms, the constants hidden away by the asymptotic notation may be so big that it is infeasible to use them in even the smallest problem instances.
Conversely, it is possible that an algorithm with an undesirable asymptotic complexity may work perfectly fine for your input sizes.
```

When exhaustively searching for the exact solutions is difficult, there are a few approaches we can turn towards.
Sometimes, a certain subset of the problem may have additional properties allowing for more efficient solutions.
For example, if we consider the set of all TSP problems where each problem instance is uniquely identified by a matrix of inter-city costs, some families of matrices impose efficiently solvable TSP problems.
A specific example is the so called Monge matrices, which guarantee solutions to the TSP that are _pyramidal_, i.e. the solution is a tour $s=<1,i_1,\dots,i_r,n,j_1,\dots,j_{n-r-2}>$ where $i_1<i_2<\dots i_r$ and $j_1>j_2>\dots>j_{n-r-2}$ as if cities are visited first in increasing order, then the remaining in decreasing order.

Another approach for some problems is dynamic programming but that is not in the scope of this course.

A final option is to abandon the search for exact solutions.
In many cases, having a good enough solution is sufficient, or there may be time or other resource constraints that makes anything better an impossibility.
In these instances, there are often two paths one could pursue.
The first is approximation algorithms, which find approximate solutions to problems with provable guarantees, often more efficiently than their exact counterparts.
An example for (a subset of) TSP is the Christofides-Serdyukov algorithm, which finds solutions guaranteed to be within a factor of $1.5$ of the optimal route.
These types of algorithms typically work via relaxations of the original problem or solving a new problen with additional assumptions and proving a relation to the original problem.

We can take these ideas one step further by ignoring the goal of provable guarantees and just focusing on getting good results.
In such a scheme, there may be some inputs where our algorithm may behave badly, whether by taking too long of a time or by outputing bad solutions.
But as long as for "most" inputs we get sufficiently good solutions, these disadvantages may be acceptable.
We will discuss such _heuristic_ algorithms in the next lecture.

## Exact Solution Examples

### TSP

Example with Held-Karp

### Minimum Spanning Trees

Example with Kruskal's
(next lecture, tie this in to greedy)
