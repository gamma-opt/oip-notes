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

# Metaheuristics

% TODO Add some introduction
% In this section we'll show some algorithms... We implement them here but you can use a library like metaheuristics...

% Focus on going downhill while trying to avoid local minima

## Point methods

```{code-cell}
function cost_f(solution, d)
    c = 0
    for i in 2:n
        c += d[solution[i-1],solution[i]]
    end
    c += d[solution[1], solution[n]]
    return c
end

function create_neighbor(solution)

end
```

### GRASP

% TODO Check: 
% - just call this a metaheuristic
% - local search or perturbative
_Greedy randomised adaptive search procedure_ (GRASP) is an algorithm that combines greediness with local search techniques.
This is achieved by repeating an iteration consisting of two phases until some termination criterion is satisfied.
In the first phase, a new solution is constructed, similar to that in a greedy approach.
However, instead of picking the best candidate, all candidates above a goodness threshold are collected, forming the _restricted candidate list_, from which one is chosen randomly.
Once a solution is formed, the algoritm moves to the second phase, where neighboring solutions are explored for better performers.

% TODO Should the objective function be added as input?
```{prf:algorithm} GRASP
1. While termination criterion is unmet

    Construction
    1. Initialize an empty solution.
    2. While the solution is incomplete
        1. Construct a RCL from the best performing elements.
        2. Add a random element from the RCL to the solution.

    Local Search

    3. While the local search termination criterion is unmet
        1. Generate a neighbor from the current solution.
        2. If the neighbor is better, replace the current solution with it.
    4. If this new solution is the best so far, replace the previous best.
2. Return the best solution.
```

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
% TODO change to use lin-kernighan?
```{code-cell}
function second_phase(solution, d, n, n_iter)
    best = solution
    best_cost = cost_f(solution, d)
    for _ in 1:n_iter
        neighbor = copy(solution)
        removed = popat!(neighbor, rand(1:n))
        insert!(neighbor, rand(1:n), removed)
        cost = cost_f(neighbor, d)
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

    while true
        sol = first_phase(d, n, a)
        sol = second_phase(sol, d, n, second_phase_iters)

        cost = cost_f(sol, d)
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

### Simulated Annealing

_Simulated annealing_ is a method that takes inspiration from thermodynamics.
At high temperature, the molecules of a liquid will have high energy and mobility.
If frozen immediately, the resulting molecular structure will likely be highly irregular.
However, if cooled slowly such as in the process of annealing in metallurgy, the molecules are able to attain a regular arrangment, even possibly achieving the minimum energy state for the system.
The notions of high energy and slow cooling are translated into optimisation to try to achieve the minimum energy state, corresponding to the minimum of an optimisation problem.
More specifically, the simulated annealing algorithm works by starting with an initial solution and exploring the solution space via neighbors.
However, worse solutions are sometimes accepted, with probability proportional to the system's current "temperature".
Temperature decreases with every iteration and so does the mobility of the solution, as acceptance will be constrained to better performing solutions.
Ideally, the high mobility at high temperatures will allow the algorithm to discover the region near the global minimum, which will then be achieved via the smaller changes at lower temperatures.

```{prf:algorithm} Simulated annealing
:label: alg_sa
**Inputs** Objective function $f$
1. Generate a random solution as current state $x$.
2. While the termination criterion is unmet
    1. Get the current temperature $T$.
    2. Create a random neighbor $x'$ of the current state $x$.
    3. Calculate performance difference $\Delta=f(x')-f(x)$.
    4. If $\Delta<0$ (i.e. $x'$ is better than $x$), accept it as current state.
    5. If not, accept $x'$ with probability $e^{-\Delta}/T$.
3. Return $x$.
```

In {prf:ref}`alg_sa`, there are two points worth discussing in greater detail.
First is the acceptance probability.
If a new solution is better performing, it is always accepted.
If the new solution is instead worse, then the probability of acceptance depends on how much worse it is, i.e. $\Delta$, and the temperature $T$.
As the temperature tends to 0, the probability will be concentrated on the global minimum.

The second point is the cooling schedule of the algorithm, i.e. how the temperature decreases across iterations.
This plays a crucial role in the algorithm's performance, as we would like to cool down slowly enough to capture the global minimum but without waiting for an infinite amount  of time to guarantee that.
% From Numerical Recipes
There is no universally good choice, but possible schedules worth trying include:
- Exponential schedule: setting $T=T*\alpha$ after every $m$ moves,
- Move budget: setting $T=T_0(1-k/K)^\alpha$ after every $m$ moves, where $k$ is the number of moves made so far and $K$ is the total number of moves allowed. $\alpha$ here is some positive hyperparameter. 

```{code-cell}
function tsp_sa(d, n, n_iters)
    sol = shuffle(1:n)
    for it in 1:n_iters
        T = n_iters/it
        neighbor = create_neighbor(sol)
        delta = cost_f(neighbor, d) - cost_f(sol)
        if delta < 0 || rand() < exp(-delta/T)
            sol = neighbor
        end
    end
    return sol
end
```

## Population methods

The methods we have covered so far relied on keeping ttrack of a single point moving around in the solution space.
Some methods differ from this approach in that they are _population_ based, where avoiding local minima is achieved through spreading a collection of individuals throughout the solution space.

### Genetic Algorithms

_Genetic algorithms_ take inspiration from biology and simulate a natural-selection-like process in order to obtain good solutions.
On a high level, genetic algorithms work by treating each individual solution in a population as a chromosome, whose fitness is inversely proportional to the value of the objective function at that point, since we are minimising.
Every iteration represents a generation, during which a subpopulation is selected based on their fitness to reproduce, leading to a new generation.
The reproduction step incorporates recombination, where pairs of "parent" solutions combine their genetic information similar to sexual reproduction, adding diversity to the optimisation process.
Lastly, random mutations can occur on individual chromosomes, adding in additional diversity to the process.

#### Chromosomes

The representation of solutions as chromosomes is critical to the design of the recombination and mutation operations, and the performance of the algorithm.
Most frequently, bit strings are used to represent solutions.
For example in a 0-1 knapsack problem this would be natural, since every bit could correspond to whether an item is included in the selection or not.
For TSP, it may be easier to consider integer sequences as we have done in earlier examples.
Alternative representations are also possible, as long as recombination and mutation operations can be clearly defined.

#### Selection

There are a number of different strategies for picking parents for the next generation.

- Genetic algorithms
-- mutations
-- recombination
-- selection
- More?

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