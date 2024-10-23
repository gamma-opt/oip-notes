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

## Randomized methods

### Randomised methods

#### GRASP 

#### simulated annealing

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