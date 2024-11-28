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

```{code-cell}
---
mystnb:
  figure:
    name: fig:function-examples-1
    caption: |
      Growth of different functions. Note that the $y$-axis is on a $\log_2$ scale, so the differences between the lines are very large. When $n=20$, $n!$ is more than 1 billion times the value of $e^n$.
tags: [remove-input]
---
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

In continuous problems, the number of feasible solutions was not a problem.
Even though there may be an infinite number of possibile solutions, we are able to exploit information given by objective and constraint functions to guide our search.
In mixed-integer problems, this was rendered more difficult by the presence of integer variables, but we are still able to use the same techniques via relaxations and branching when needed.
In combinatorial problems, there seldom are nice functions that we can analyse generically.

In order to avoid exhaustively searching for the exact solution, there are a few approaches we can turn towards.
Sometimes, the problem is such that it is easily solvable without going through all possibilities individually. Finding shortest paths and minimum spanning trees, examples given in {numref}`p2l5-sp` and {numref}`p2l5-mst` both have very natural algorithms that turn out yield optimal solutions.

Similarly, in cases where the general problem is difficult, a certain subset of the problem may have additional properties allowing for more efficient solutions.
For example, if we consider the set of all TSP problems where each problem instance is uniquely identified by a matrix of inter-city costs, some families of matrices impose efficiently solvable TSP problems.
A specific example is the so called Monge matrices, which guarantee solutions to the TSP that are _pyramidal_, i.e. the solution is a tour $s=<1,i_1,\dots,i_r,n,j_1,\dots,j_{n-r-2}>$ where $i_1<i_2<\dots i_r$ and $j_1>j_2>\dots>j_{n-r-2}$ as if cities are visited first in increasing order, then the remaining in decreasing order.

Another approach for some problems is dynamic programming, which is a technique to break down a problems into a sequence of smaller subproblems or decisions over timesteps. An example is provided in {numref}`p2l5-tsp`, but we won't cover dynamic programming in detail.

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

(p2l5-sp)=
### Shortest Path 

Finding the quickest way home via GPS or a connection between two computers with the fewest hops in a network are only two examples of the ubiquitous problem of finding the shortest path.
These examples along with many more problems are solved frequently using graphs.

A _graph_ is a pair $G=(V,E)$ where $V$ is a set of _nodes_ (or _vertices_) and $E$ is a set of _edges_ connecting two nodes.
Graphs are a very flexible mathematical structure that can be used in a variety of contexts. A graph is called _connected_ if every node is reachable from other nodes through some series of edges.

A _weighted graph_ is a graph $G=(V,E,w)$ where every edge has an associated weight given by some function $w$.
For example, the cities and roads of Finland could be considered as a weighted graph, where the cities are nodes, edges are present in between directly-connected cities, and edge-weights could be the distance in between the two cities.

```{figure} ../figures/graph.svg
:name: graphs
A non-connected graph on the left and a connected, weighted graph on the right.
```

Given a weighted graph $G=(V,E,w)$, the shortest path between $u\in V$ and $v\in V$ is the path $P=(e_1, \dots, e_n)$ between them that minimizes $\sum_{i=1}^n w(e_i)$.
Alternative variants of the shortest problem include finding the shortest path from an origin to all other nodes or the shortest path between all pairs of nodes.
A classical algorithm to solve this problem is Dijkstra's algorithm, which uses a (min-)priority queue to keep track of the edges with the smallest weight.

```{prf:algorithm} Dijkstra's Algorithm
:label: dijkstra
**Inputs** Graph $G$, weight function $w$, origin $o$, target $t$
1. Create a priority queue $Q$.
2. Create a vector to keep tract of distances.
3. Add $o$ to $Q$ with priority $0$ and every other vertex with priority $\infty$.
4. While $Q$ is not empty,
    1. Extract from $Q$ the next node $u$.
    2. For each neighbor $v$ of $u$.
        1. `curr_dist` $=$ distance to $u + w(u,v)$.
        2. If distance to $v$ is the least observed so far, record it and add $v$ to $Q$ with priority `curr_dist`.
        3. If $v=t$, break
5. Return distance of $t$
```

In Julia, implementations of {prf:ref}`dijkstra` that solves the single-source all-targets variant is provided by the [`Graphs.jl`](https://juliagraphs.org/Graphs.jl/stable/) package.

```{code-cell}
:tags: [remove-cell]
using Random, StatsBase, Graphs, GraphMakie

function generate_distance_matrix(n; random_seed = 1)
    rng = Random.MersenneTwister(random_seed)
    X_coord = 100 * rand(rng, n)
    Y_coord = 100 * rand(rng, n)
    d = [sqrt((X_coord[i] - X_coord[j])^2 + (Y_coord[i] - Y_coord[j])^2) for i in 1:n, j in 1:n]
    return d, X_coord, Y_coord
end

n = 15
d, xs, ys = generate_distance_matrix(n)

rng = Random.MersenneTwister(42)

g = complete_graph(n)
rem = sample(rng, collect(edges(g)), 80; replace=false)
for e in rem
    rem_edge!(g, e.src, e.dst)
end
```

```{code-cell}
source = 11
ds = dijkstra_shortest_paths(g, source, d)  # g is some graph, d is the distance matrix
```

The output `ds` contains information about the solution such as parents of nodes in the shortest path and distances as documented [here](https://juliagraphs.org/Graphs.jl/stable/algorithms/shortestpaths/#Graphs.DijkstraState). We can extract the shortest path to a given target node, such as 15, via going backwards.

```{code-cell}
target = 15
# initialize backwards search
path = [target]
curr = target

while curr != source
    parent = ds.parents[curr]
    push!(path, parent)
    curr = parent
end
reverse(path)
```

```{code-cell}
:tags: [remove-input]
c_blue = Makie.wong_colors()[1]
c_orange = Makie.wong_colors()[2]

c = []
elabs = []
for e in edges(g)
    # this is not correct in general cases and we could keep track of edges in the prev cell,
    # but I didn't want to show a variable only to use it in a hidden cell
    if e.src in path && e.dst in path
        push!(c, c_orange)
    else
        push!(c, c_blue)
    end
    push!(elabs, repr(Int(round(d[e.src,e.dst]))))
end
graphplot(g; nlabels=repr.(1:nv(g)), node_color=c_blue, edge_color=c, elabels=elabs, elabels_color=:black)
```

(p2l5-tsp)=
### TSP

The Held-Karp algorithm is a dynamic programming algorithm to solve TSP exactly.
The key idea underlying the algorithm is that given a set of cities $S=\{s_1,\dots,s_k\}$, suppose the shortest path $P$ from an origin $o$ through $S$ to a destination $e$ has $s_i$ as the penultimate city.
Then, it must be the case that the shortest path from 1 to $s_i$ going through $S\setminus \{s_i\}$ must be $P$ with the last edge removed.

This observation means that the solution of larger instances of a problem is directly related to smaller subproblems, which is exactly the kind of structure dynamic programming can exploit.

```{prf:algorithm} Held-Karp Algorithm
:label: held-karp
**Inputs** Graph $G$, number of nodes $n$
1. Pick an origin $o$
2. Initialize distance to all other nodes from $o$
3. For $i=2$ to $n-1$
    1. For every subset $S$ of size $i$
        1. For every element $k$ of $S$
            1. Determine the shortest distance from $o$ to $k$ going through only $S$.
4. Find the best cycle and return
```

An implementation of the algorithm is presented below for completeness, but we will not discuss it in depth since it is still too slow for larger instances of the problem. 
{numref}`tsp_heldkarp` displays the output of an algorithm for a managable size of $n=20$.

```julia
using Combinatorics

function held_karp(d)
    n = size(d)[1]

    # entries are tuples of 
    #  - S: bitstring (int) representing subsets of cities and
    #  - k: int representing the final city (is in S)
    # mapping to
    #  - cost of shortest path from city 1 through S ending at k
    #  - city visited before k (needed for reconstructing the path)
    g = Dict()  

    # initialize with basic distances
    for k in 2:n
        g[(1<<k, k)] = (d[1,k], 1)
    end

    # upper bound is n-1 since city 1 is not counted in the subset
    for subset_size in 2:(n-1)
        for subset in Combinatorics.combinations(2:n, subset_size)

            # the first bit is always unused, but we don't need to optimize for space
            subset_in_bits = 0
            for city in subset
                subset_in_bits |= 1<<city
            end

            # for every possible final city
            for k in subset
                # solve smaller problem S' = S \ {k}
                prev = subset_in_bits & ~(1<<k)
                
                # go through all final cities for S'
                costs = []
                for m in subset
                    if m == k
                        continue
                    end
                    push!(costs, (g[(prev, m)][1] + d[m,k], m) )
                end
                
                g[(subset_in_bits, k)] = argmin(first, costs)
            end
        end
    end

    # Recover the best result
    # which is given by the subset containing everything except city 1
    # since city 2 is represented 1<<2 (and the rest is larger), we have the first two bits not used
    # so the subset is given by 2^(n+1)-1 to get first n bits as 1 and -3 to remove the first two bits
    full_subset = 2^(n+1) - 4

    # find the best final city
    costs = []
    for k in 2:n
        push!(costs, (g[(full_subset, k)][1] + d[k,1], k))
    end

    opt, prev_city = argmin(first, costs)

    # reconstruct best path
    opt_path = []
    subset = full_subset
    for i in 1:(n-1)
        push!(opt_path, prev_city)
        prev = subset & ~(1<<prev_city)
        _, prev_city = g[(subset, prev_city)]
        subset = prev
    end

    push!(opt_path, 1)

    return opt, reverse(opt_path)
end
```

```{code-cell}
:tags: [skip-execution]
held_karp(d)  # d is some distance matrix
```

```{figure} ../figures/tsp_heldkarp.svg
:name: tsp_heldkarp
Output of the Held-Karp algorithm in a TSP instance with $n=20$.
```

(p2l5-mst)=
### Minimum Spanning Trees

A _minimum spanning tree_ (MST) of a connected, weighted graph $G=(V,E,w)$ is a subset of the edges $E'\subseteq E$ such that
- $G'=(V,E')$ is connected,
- $G'$ does not contain any cycles, and
- $\sum_{e\in E'} w(e)$ is minimal.

Finding minimum spanning trees is desirable in a variety of contexts.
For example, when building some sort of a network like an electrical grid or a computer network, MSTs can correspond to subsets that provide connectivity at the lowest cost. One algorithm for obtaining MSTs is provided by Kruskal.

```{prf:algorithm} Kruskal's algorithm
:label: kruskal
**Inputs** A graph $G=(V,E, w)$.
1. Set $E'=\emptyset$.
2. Sort $E$ in ascending order of weights.
3. For each edge $e=(u,v)$ in $E'$
    1. Add $e$ to $E'$ if $G'=(V,E' \cup \{e\})$ doesn't contain any cycles
4. Output $E'$ 
```

It can be proven that {prf:ref}`kruskal` is optimal, the MSTs outputted are minimal, but the proof is not within the scope of this course.
But we can see it in action.
Suppose for example we would like to obtain the MST for the below nodes.

% TODO consider changing this example to cities in Finland
% using GeoMakie and NaturalEarth?
```{code-cell}
:tags: [remove-input]

fig,ax,plot = scatter(xs, ys)
```

An implementation of {prf:ref}`kruskal` in Julia is provided by the [`Graphs.jl`](https://juliagraphs.org/Graphs.jl/stable/) package.

```{code-cell}
:tags: [remove-output]
using Graphs

g = complete_graph(n)  # complete graph since we want to pick over any possible node
mst_edges = kruskal_mst(g, d) # d is the distance matrix
```

```{code-cell}
:tags: [remove-input]
for e in mst_edges
    lines!(ax, xs[[e.src, e.dst]], ys[[e.src, e.dst]], color = 1, colormap = :tab10, colorrange = (1, 10))
end
fig
```