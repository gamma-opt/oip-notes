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

```{admonition} Runtime of algorithms and computational complexity

placeholder
```

When exhaustively searching for the exact solutions is difficult, there are a few approaches we can turn towards.
Sometimes, a certain subset of the problem may have additional properties allowing for more efficient solutions.
For example, if we consider the set of all TSP problems where each problem instance is uniquely identified by a matrix of inter-city costs, some families of matrices impose efficiently solvable TSP problems.
A specific example is the so called Monge matrices, which guarantee solutions to the TSP that are _pyramidal_, i.e. the solution is a tour $s=<1,i_1,\dots,i_r,n,j_1,\dots,j_{n-r-2}>$ where $i_1<i_2<\dots i_r$ and $j_1>j_2>\dots>j_{n-r-2}$ as if cities are visited first in increasing order, then the remaining in decreasing order.

### Subset of the problem can be solved efficiently

### Randomization

### Dynamic programmming and Approximation Algorithms (only mention)
