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

# Title

% TODO Add some introduction
% In this section we'll show some algorithms... We implement them here but you can use a library like metaheuristics...

## Randomized methods

### GRASP

% TODO Check: 
% - just call this a metaheuristic
% - local search or perturbative
_Greedy randomised adaptive search procedure_ (GRASP) is an algorithm that combines greediness with local search techniques.
This is achieved by repeating an iteration consisting of two phasesn until some termination criterion is satisfied.
In the first phase, a new solution is constructed, similar to that in a greedy approach.
However, instead of picking the best candidate, all candidates above a goodness threshold are collected, forming the _restricted candidate list_, from which one is chosen randomly.
Once a solution is formed, the algoritm moves to the second phase, where neighboring solutions are explored for better performers.

As an example, we can implement a GRASP algorithm for TSP.

In the first phase, we construct a solution using a distance matrix $d$ and some cutoff strategy.
In the below code, this is achieved by obtaining a range of the candidate costs and allowing only a fraction of this range, which is controlled by $a\in [0,1]$.
If $a=0$, then `cutoff = c_min` and thus solution construction will be purely greedy.
If $a=1$, then `rcl` will contain every candidate, thus solution construction will be entirely random.
```{code-cell}
function first_phase(d, n, a)
    solution = [1]
    for _ in 2:n
        curr_city = solution[end]
        candidates = filter(x->!(x[1] in solution), collect(zip(1:n, d[curr_city, :])))

        c_max = maximum(x->x[2], candidates)
        c_min = minimum(x->x[2], candidates)
        cutoff = c_min + a*(c_max - c_min)
        
        rcl = [i for (i,c) in candidates if c <= cutoff]
        next_city = rand(rcl)
        push!(solution, next_city)
    end
    return solution
end
```

In the second phase, the solution is mutated in a neighborhood.
In this implementation, we remove a randomly selected city and insert it at a random location, but one can imagine other descriptions of neighborhood and appropriate mutations.
```{code-cell}
function second_phase(solution, n, cost_f, n_iter)
    best = solution
    best_cost = cost_f(solution)
    for _ in 1:n_iter
        neighbor = copy(solution)
        removed = popat!(neighbor, rand(1:n))
        insert!(neighbor, rand(1:n), removed)
        cost = cost_f(neighbor)
        if cost < best_cost
            best = neighbor
            best_cost = cost
        end
    end
    return best
end
```

Putting the two phases together we get the GRASP algorithm.
```{code-cell}
function tsp_grasp(d, a, terminate, second_phase_iters=100)
    n = size(d)[1]
    best = nothing
    best_cost = Inf

    function cost_f(solution)
        c = 0
        for i in 2:n
            c += d[solution[i-1],solution[i]]
        end
        c += d[solution[1], solution[n]]
        return c
    end

    while true
        sol = first_phase(d, n, a)
        sol = second_phase(sol, n, cost_f, second_phase_iters)

        cost = cost_f(sol)
        if cost < best_cost
            best_cost = cost
            best = sol
        end

        if terminate(sol)
          return best
        end
    end
end
```

In the code above, the termination criterion implementation is left to the user, it could be anything from a simple iteration count to something more involved looking at improvements across iterations.
A simple example is provided by the following.
```{code-cell}
mutable struct IterationCounter
    iters::Int
    limit::Int
end

IterationCounter() = IterationCounter(0, 100)

function (c::IterationCounter)(_)
    if c.iters > c.limit
      return true
    end
    c.iters += 1
    return false
end
```

Need better local search logic probably
```{code-cell}
using Random, CairoMakie

function generate_distance_matrix(n; random_seed = 1)
    rng = Random.MersenneTwister(random_seed)
    X_coord = 100 * rand(rng, n)
    Y_coord = 100 * rand(rng, n)
    d = [sqrt((X_coord[i] - X_coord[j])^2 + (Y_coord[i] - Y_coord[j])^2) for i in 1:n, j in 1:n]
    return d, X_coord, Y_coord
end

n = 40
d, X_coord, Y_coord = generate_distance_matrix(n)

count = IterationCounter(0, 1000)
path = tsp_grasp(d, .3, count, 1000)

fig, ax, plot = scatter(X_coord, Y_coord)
lines!(ax, X_coord[path], Y_coord[path], color = 1, colormap = :tab10, colorrange = (1, 10))  # reorder vector using permutation
endpoints = path[[1,n]]
lines!(ax, X_coord[endpoints], Y_coord[endpoints], color = 1, colormap = :tab10, colorrange = (1, 10))  # connect the cycle
fig
```

### simulated annealing



## Metaheuristics

### Evolutionary methods

### Particle swarm

### Example: Knapsack Problem

Should there be a problem example here or should it be left for Workshop 3?
I think it may be easier to have an example, so we can exemplify/illustrate solution construction, neighbour search, mutation etc.

0/1 knapsack (from http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/)
Optimum is 295.

GRASP code following example in source code.

```{code-cell}
using Metaheuristics

struct KPInstance
    profit
    weight
    capacity
end

capacity = 269

# (value, weight)
profit = [55, 10,47, 5, 4, 50, 8, 61, 85, 87]
weight = [95, 4, 60, 32, 23, 72, 80, 62, 65, 46]

f, search_space, _ = Metaheuristics.TestProblems.knapsack(profit, weight, capacity)
```

## Randomised methods: GRASP

Greedy Randomized Adaptive Search Procedure

```{code-cell}
instance = KPInstance(profit, weight, capacity)

function Metaheuristics.compute_cost(candidates, constructor, instance::KPInstance)
    # Ration profit / weight
    ratio = instance.profit[candidates] ./ instance.weight[candidates]
    # It is assumed minimizing non-negative costs
    maximum(ratio) .- ratio
end

options = Options(seed = 1, iterations=1000)

candidates = rand(search_space)
constructor = Metaheuristics.GreedyRandomizedContructor(;candidates, instance, α = 0.95)
local_search = Metaheuristics.BestImprovingSearch()
neighborhood = Metaheuristics.TwoOptNeighborhood()
grasp = GRASP(;constructor, local_search, options)
result = optimize(f, search_space, grasp)
```

## Randomised methods: Simulated Annealing

In Metaheuristics.jl SA doesn't currently support working with permutations, as I've used above.
I hacked something and may make a PR later but it needs more work.

```{code-cell}
sa = SA(;N=100, options)
optimize(f, search_space, sa)
```

## Evolutionary methods (Genetic algorithms -> memetic / differential )

Metaheuristics.jl have some options like [Differential Evolution](https://jmejia8.github.io/Metaheuristics.jl/stable/algorithms/#Differential-Evolution) and [ε Constrained Differential Evolution](https://jmejia8.github.io/Metaheuristics.jl/stable/algorithms/#\\varepsilonDE), in addition to the classic GA. Not sure which one is better.

There is no memetic option (unless εDE counts), which means I need to find something else.

## Particle swarm

PSO also doesn't support permutations.

```{code-cell}
pso = PSO(;N = 100, C1=1.5, C2=1.5, ω = 0.7)
optimize(f, search_space, pso)
```