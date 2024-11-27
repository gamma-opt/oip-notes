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

<!--
TODOs
[] Comment the code, based on what was done in the combinatorial optimisation lectures
[] GRASP: after defining each function, we should run it to provide an concrete example of how it works
[] The iteration counter is unnecessarily difficult programming wise. Add it to the main GRASP function so it is closer to the pseudocode
[] In the pseudocode for simulated annealing we should add a step on the cooling of T
[] We should add a picture illustrating the chromosome when we explain what they are
[] The PSO part seem unfinished in comparison to the to the others. Why so?
-->

# Metaheuristics

In [Lecture 16](./6-heuristics-1.md), we discussed heuristic methods, which are general approaches for obtaining good results for difficult problems.
In this lecture, we will talk about _metaheuristics_, which can be thought of as "template algorithms" that use heuristic ideas on a high-level, so that they can be adapted to work for many problems.

A big focus of these algorithms is balancing exploration versus exploitation: making sure that we get the best result available without being stuck in a local optimum.
Keep this in mind throughout the lecture, many algorithms that fall under the umbrella of metaheuristics can be thought of as greedy approach plus some mechanism to add diversity to the solution and explore the solution space globally.

Below we also provide code examples for the methods we present, however keep in mind that many packages exist that implement the main logic of the algorithms and require only problem specific information from the user.
Such packages in Julia include [`Metaheuristics.jl`](https://jmejia8.github.io/Metaheuristics.jl/stable/), [`BlackBoxOptim.jl`](https://github.com/robertfeldt/BlackBoxOptim.jl) and [`Evolutionary.jl`](https://wildart.github.io/Evolutionary.jl/stable/).

Here are some functions we will need throughout the lecture for giving TSP examples.
```{code-cell}
:tags: [remove-output]
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

# compute the cost of a TSP cycle, given a vector of cities to visit in order
function cost_f(solution, d)
    c = 0
    for i in 2:n
        c += d[solution[i-1],solution[i]]
    end
    c += d[solution[1], solution[n]]
    return c
end
```

## Point methods

### GRASP

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
    # always start from the first city
    solution = [1]
    for _ in 2:n
        curr_city = solution[end]
        
        # vector of (city_i, distance to 1)
        candidates = filter(x->!(x[1] in solution), collect(zip(1:n, d[curr_city, :])))

        # find the bounds for the next step
        c_max = maximum(x->x[2], candidates)
        c_min = minimum(x->x[2], candidates)
        cutoff = c_min + a*(c_max - c_min)
        
        # create rcl and pick randomly to add to solution
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

    # mutate multiple times
    for _ in 1:n_iter
        neighbor = copy(solution)

        # remove random city and insert back randomly
        removed = popat!(neighbor, rand(1:n))
        insert!(neighbor, rand(1:n), removed)

        # save only if cost is decreased
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

Let's see what result we get.
```{code-cell}
:tags: [skip-execution]
count = IterationCounter(0, 1000)
path = tsp_grasp(d, .3, count, 1000)

fig, ax, plot = scatter(X_coord, Y_coord)
lines!(ax, X_coord[path], Y_coord[path], color = 1, colormap = :tab10, colorrange = (1, 10))  # reorder vector using permutation
endpoints = path[[1,n]]
lines!(ax, X_coord[endpoints], Y_coord[endpoints], color = 1, colormap = :tab10, colorrange = (1, 10))  # connect the cycle
fig
```
```{figure} ../figures/tsp_grasp.svg
GRASP algorithm output for TSP with $n=40$.
```

This is not a bad attempt though clearly suboptimal.
Tweaking the hyperparameters such as $a$ and the number of iterations, along with devising better local-search methods in the second phase of the algorithm may yield significantly better results.

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
function create_neighbor(sol)
    c = copy(sol)
    
    #randomly select two cities and swap them
    i,j = randperm(length(sol))[1:2]
    c[i],c[j] = c[j],c[i]
    return c
end

function tsp_sa(d, n, n_iters)
    sol = shuffle(1:n)
    for it in 1:n_iters
        T = n_iters/it
        neighbor = create_neighbor(sol)
        delta = cost_f(neighbor, d) - cost_f(sol, d)
        
        # if new solution is better, accept
        # otherwise, accept randomly
        if delta < 0 || rand() < exp(-delta/T)
            sol = neighbor
        end
    end
    return sol
end
```

Applying it to the same TSP problem gives us the following solution.

```{code-cell}
:tags: [skip-execution]
path = tsp_sa(d, n, 1000)

fig, ax, plot = scatter(X_coord, Y_coord)
lines!(ax, X_coord[path], Y_coord[path], color = 1, colormap = :tab10, colorrange = (1, 10))  # reorder vector using permutation
endpoints = path[[1,n]]
lines!(ax, X_coord[endpoints], Y_coord[endpoints], color = 1, colormap = :tab10, colorrange = (1, 10))  # connect the cycle
fig
```
```{figure} ../figures/tsp_sa.svg
Simulated annealing algorithm output for TSP with $n=40$.
```

Similar to GRASP, the SA solution we obtain is suboptimal but significantly better than a random permutation.
The `create_neighbor` function used above does only a simple swap of two cities.
A significant improvement to this approach would be to use the [Lin-Kernighan heuristic](https://en.wikipedia.org/wiki/Lin%E2%80%93Kernighan_heuristic) for generating neighboring solutions, which is specifically optimisation related thus we only mention for completeness.

## Population methods

The methods we have covered so far relied on keeping track of a single point moving around in the solution space.
Some methods differ from this approach in that they are _population_ based, where avoiding local minima is achieved through spreading a collection of individuals throughout the solution space.

### Genetic Algorithms

_Genetic algorithms_ take inspiration from biology and simulate a natural-selection-like process in order to obtain good solutions.
On a high level, genetic algorithms work by treating each individual solution in a population as a _chromosome_, whose fitness is inversely proportional to the value of the objective function at that point, since we are minimising.
Every iteration represents a generation, during which a subpopulation is _selected_ based on their fitness to reproduce, leading to a new generation.
The reproduction step incorporates _recombination_, where pairs of "parent" solutions combine their genetic information similar to sexual reproduction, adding diversity to the optimisation process.
Lastly, random _mutations_ can occur on individual chromosomes, adding in additional diversity to the process.

A generic genetic algorithm is given in {prf:ref}`genetic_alg`.

```{prf:algorithm} Genetic Algorithm
:label: genetic_alg
1. Initialize the current generation.
2. For $i=1,\dots,N$
    1. **Select** parents from the current generation $G_i$.
    2. **Recombine** selected parents to create the next generation $G_{i+1}$.
    3. **Mutate** individuals of $G_{i+1}$.
3. Return the solution corresponding to the individual with the highest fitness.
```

#### Chromosomes

The representation of solutions as chromosomes is critical to the design of the recombination and mutation operations, and the performance of the algorithm.
Most frequently, bit strings are used to represent solutions.
For example in a 0-1 knapsack problem this would be natural, since every bit could correspond to whether an item is included in the selection or not.
For TSP, it may be easier to consider permutations as we have done in earlier examples.
Alternative representations are also possible, as long as recombination and mutation operations can be clearly defined.

#### Selection

There are a number of different strategies for picking parents for the next generation.
They vary in the selection pressure they impose.
If pressure is too high, only the currently-best solutions will be selected and the evolution process will be concentrated into alike solutions.
Conversely, if the pressure is too low, then mediocre solutions will not be eliminated and thus will pollute the next generation, making optimisation difficult.
An ideal amount of pressure will allow seeking good solutions while exploring the solution space, thus escaping local optima.

One example method for selection is **roulette wheel selection**, also known as **fitness proportionate selection**, where parents are chosen randomly, each having probability proportional to their fitness.
This is akin to spinning a roulette wheel where the slices are bigger for individuals with higher fitness.

```{code-cell}
abstract type Selection end

struct RouletteWheelSelection <: Selection end
function select(t::RouletteWheelSelection, fitness, N)
    s = sum(fitness)
    # cumulative sum
    fitness_probs = cumsum(fitness ./ s)
    parent() = begin
        r = rand()
        for (i, prob) in enumerate(fitness_probs)
            if r < prob
                return i
            end
        end
    end
    return [[parent(), parent()] for _ in 1:N]
end
```

Another strategy is **tournament selection**, in which a subset of the population is selected randomly to "compete in a tournament" based on their fitness.
The winner, i.e. the individual with the highest fitness is selected as a parent.
If the subset to be selected is large, this reduces to greedy selection since individuals with the highest fitness will be more likely to be included.
With a smaller size, the selection pressure decreases, adding diversity to the solution evolution.

```{code-cell}
struct TournamentSelection <: Selection 
    size
end
function select(t::TournamentSelection, fitness, N)
    parents() = begin
        # pick the best two out of a random selection
        perm = randperm(length(fitness))
        return sort(perm[1:t.size], by=x->fitness[x], rev=true)[1:2]
    end
    return [parents() for _ in 1:N]
end
```


#### Recombination

In sexual reproduction, the two sets of chromosomes from parent cells exchange genetic information with one another in a process called crossing-over or recombination, resulting in an offspring that is related to its parents but with a different genetic makeup.
In genetic algorithms, this is emulated similarly, where the next generation is created via recombination of the selected individuals from the previous generation.
More specifically, two parents are selected and applied a crossover operation, which often results in two offsprings.

The exact mechanism of the recombination is dependant on the chromosome structure.
For example, if the chromosomes are bitstrings, some random substring(s) of each chromosome may be swapped.
```{figure} ../figures/recombination_twopoint.drawio.svg
A popular bitstring recombination operation is two-point crossover, where a start point and an end point are selected randomly and the region in between are exchanged.
```

```{code-cell}
abstract type Recombination end

struct TwoPointCrossover <: Recombination end
function recombine(t::TwoPointCrossover, parent_pair)
    # randomly pick start and end
    n = length(parent_pair[1])
    s, e = randperm(n)[1:2]

    # mark the selected region
    mask = falses(n)
    if s < e
        mask[s:e] .= 1
    else
        mask[1:s] .= 1
        mask[e:n] .= 1
    end

    # create the children
    child1 = copy(parent_pair[1])
    child2 = copy(parent_pair[2])
    child1[mask] = parent_pair[2][mask]
    child2[mask] = parent_pair[1][mask]
    return [child1, child2]
end
```

% http://www.permutationcity.co.uk/projects/mutants/tsp.html
For more elaborate chromosomes, for example those representing permutations, recombination is often a bit more involved, since one needs to ensure that the special structure is not destroyed as a result of the changes. An example of a recombination for permutation is called _order crossover_. In order crossover, a subset of values from the permutation is randomly selected. Each offspring is then constructed as a copy of one of the parents, except the selected subset of values is reordered to match the other parent.

```{figure} ../figures/recombination_order.drawio.svg
Example of an order crossover where $S=\{1,3,4,7\}$ is selected. For the top offspring, the values are retained in the position from the first parent and for the bottom offspring, the second parent.
```

```{code-cell}
struct OrderCrossover <: Recombination 
    size
end
function recombine(t::OrderCrossover, parent_pair)
    # randomly make a selection
    n = length(parent_pair[1])
    values = randperm(n)[1:t.size]

    child1 = []
    child2 = []
    p1i = 1
    p2i = 1
    for i in 1:n
        # if not selected value, copy normally
        if !(parent_pair[1][i] in values)
            push!(child1, parent_pair[1][i])
        # if selected value
        else
            # find the next selected value (so that we can swap)
            while !(parent_pair[2][p2i] in values)
                p2i += 1
            end
            push!(child1, parent_pair[2][p2i])
            p2i += 1
        end

        # same as above, for child2
        if !(parent_pair[2][i] in values)
            push!(child2, parent_pair[2][i])
        else
            while !(parent_pair[1][p1i] in values)
                p1i += 1
            end
            push!(child2, parent_pair[1][p1i])
            p1i += 1
        end

    end
    return [child1, child2]
end
```

#### Mutation

Mutations introduce random changes in individuals, resulting in a larger diversity in the population and prevent being stuck in a local optimum.
Ideally, the mutations should be small and unbiased so that they don't interfere with specialisation and only help in the exploration of the solution space.
Similar to recombination, the mutation mechanism is heavily influenced by chromosome representation.
In bitstrings, this can be as simple as flipping a randomly selected bit (or a certain number of them).
```{figure} ../figures/mutation_bitflip.drawio.svg
Bitflip mutation example.
```

```{code-cell}
abstract type Mutation end

struct BitflipMutation <: Mutation 
    p
end
function mutate!(t::BitflipMutation, chromosome)
    mask = rand(length(chromosome)) .< p
    chromosome[mask] = !chromosome[mask]
    return nothing
end
```

Two common examples of permutation mutations are rotations and swaps.
In a rotation, a subsequence of the chromosome is randomly selected, along with a rotation number $k$. Then, within the subsequence, every item is shifted to some direction $k$ times, wrapping over to the start of the subsequence when needed. The rest of the chromosome is left intact.

```{code-cell}
struct RotationMutation <: Mutation 
    size
    k
end
function mutate!(t::RotationMutation, chromosome)
    n = length(chromosome)
    original = copy(chromosome)
    start = rand(1:n)
    selection = start:(start+t.size-1)
    # if selection exceeds the end of the chromosome, wrap back to start
    if start + t.size - 1 > n
        rem = (start + t.size) % n
        selection = vcat(1:rem, start:n)
    end
    placement = circshift(selection, t.k)
    chromosome[placement] = original[selection]
    return nothing
end
```

In a swap, two items (or non-overlapping subsequences) are randomly selected and swapped.

```{code-cell}
struct SwapMutation <: Mutation end
function mutate!(t::SwapMutation, chromosome)
    p1, p2 = randperm(length(chromosome))[1:2]
    tmp = chromosome[p1]
    chromosome[p1] = chromosome[p2]
    chromosome[p2] = tmp
    return nothing
end
```

```{figure} ../figures/mutation_permutation.drawio.svg
Permutation mutation examples.
```

Finally, we need a method for initialising the first population.
As long as the individuals are sufficiently spread, the exact mechanism of initialisation should not be critical to performance.

```{code-cell}
function initialise(n_cities, gen_size)
    [randperm(n_cities) for _ in 1:gen_size]
end
```

Combining everything together according to {prf:ref}`genetic_alg`, we get

```{code-cell}
function tsp_ga(f, n_cities, n_iters, gen_size; 
                t_sel=RouletteWheelSelection(),
                t_rec=OrderCrossover(10),
                t_mut=RotationMutation(5, 3)
)
    population = initialise(n_cities, gen_size)
    fitnesses = f.(population)
    for _ in 1:n_iters
        parent_idxs = select(t_sel, fitnesses, gen_size/2)

        # Ref() allows sharing the same element for vectorisation
        parents = getindex.(Ref(population), parent_idxs)
        offspring_pairs = recombine.(Ref(t_rec), parents)

        # combine all chromosomes into one vector
        population = vcat(offspring_pairs...)
        
        mutate!.(Ref(t_mut), population)
        fitnesses = f.(population)
    end
    max_fit, i = findmax(fitnesses)
    return population[i], max_fit
end
```

```{code-cell}
:tags: [skip-execution]
fitness(x) = -cost_f(x, d)
tsp_ga(fitness, n, 100, 100)
```

### Particle swarm optimisation

_Particle swarm optimisation_ (PSO) is similar to genetic algorithms in using a population of individuals that represent candidate solutions.
However, instead of emulating evolution, PSO simulates the movement of a _swarm_ of _particles_ across the solution space.
The movements of each particle is influenced by their individual experience and that of the entire swarm, allowing for an exploration of the solution space while seeking improvement.

```{prf:algorithm} Particle swarm
:label: alg_pso
**Inputs** Objective function $f$
1. Initialize the swarm
2. While the termination criterion is unmet
    1. For each particle in the swarm
        1. Update velocity and position
        2. If new position is better than particle's personal best or the entire swarm's best, replace them
3. Return the swarm's best position
```

The crucial feature of PSO is the velocity update.
For continuous problems, the update rule is
```{math}
:label: pso_update_continuous
v_i = av_i + b_p r_p (p_i-x_i) + b_g r_g (g_i-x_i)
```
where $v_i$ is the velocity of the $i$th particle and $x_i$ its current position.
$p_i$ and $g_i$ are the best positions of the particle and the swarm so far, and thus $(p_i-x_i)$ and $(g_i-x_i)$ can be thought of as **local** and **global** attraction, also referred to as cognitive and social contributors.
$b_p$ and $b_g$ are user-defined weights that control the contribution of the local and global attractions.
However, these are augmented by $r_p$ and $r_g$, which are randomly generated in $[0,1]$, adding stochastic variety to the movement.
The user-defined inertia $a$ ensures that the movement of the particle is not wholly independent from the previous movement.

Another important aspect of PSO is the social interaction provided by the topology of the swarm.
In the basic algorithm in {prf:ref}`alg_pso`, we have used a global topology, i.e. every individual can communicate with one another, since the swarm's best solution is accessible to all.
One can imagine that this is not ideal in all problems, for example a local minimum that is significantly better than the current best solution may attract the entire swarm to it too fast before sufficient exploration can take place.
Such a scenario can be avoided if the communication of particles is constrained to a local neighborhood or some grouping of the particles independent of their current location.

It should be noted that the continuous velocity update in {eq}`pso_update_continuous` may not be appropriate for problems in discrete space, such as TSP.
In such situations, good update rules may be problem-specific.
Here, we will formulate one for TSP with permutation solutions like in prior examples.
Let us consider the swap of two positions as our fundamental operation.
Then, we define 
- the difference between to positions, for example $p_i-x_i$, as the shortest sequence of swaps $(s_1,\dots,s_k)$ required to convert $x_i$ to $p_i$,
- the multiplication $a \cdot (s_1,\dots,s_k)$ of a swap sequence with a scalar $a$ where $0<s\leq 1$ as the swap sequence $(s_1,\dots,s_{\ceil{ak}})$,
- the addition of two swap sequences $(s_1,\dots,s_k)+(s'_1,\dots,s'_l)$ as the swap sequenece $(s_1,\dots,s_k,s'_1,\dots,s'_l)$,
- and the addition of a swap sequence and a position (i.e. a permutation) as the application of each swap in the sequence on the permutation in order.

One way of implementing these in Julia is to create a `struct` to represent each particle and define the above operations for this new object type, along with other functions for convenience.

```{code-cell}
import Base: *, -, +

const Swap = Tuple{Int, Int}
const SwapSequence = Vector{Swap}
const Permutation = Vector{Int}

mutable struct Particle
    perm::Permutation
    vel::SwapSequence
    best::Permutation
    best_f::Float64
    Particle(perm, vel, best, best_f) = perm[sortperm(perm)] == 1:length(perm) ? new(perm, vel, best, best_f) : error("invalid permutation")
end

Particle(perm, best_f) = Particle(perm, [], perm, best_f)

Base.getindex(x::Particle, i::Int) = x.perm[i]
Base.setindex!(x::Particle, val::Int, key::Int) = (x.perm[key] = val; val)
Base.copy(x::Particle) = Particle(copy(x.perm), copy(x.vel), copy(x.best), x.best_f)
Base.length(x::Particle) = length(x.perm)
Base.keys(x::Particle) = keys(x.perm)
Base.iterate(x::Particle) = iterate(x.perm)
Base.iterate(x::Particle, i::Int) = iterate(x.perm, i)



function -(x::Union{Particle,Permutation}, y::Particle)
    y = copy(y) # we don't want to mutate the original y
    seq = SwapSequence()
    for i in 1:length(x)
        if x[i] != y[i]
            j = findfirst(k->k==x[i], y)
            y[i], y[j] = y[j], y[i]
            push!(seq, (i, j))
        end
    end
    seq
end

function *(a::Float64, seq::SwapSequence)
    if a <= 0 || a > 1
        throw(DomainError(x, "0 < a <= 1 must hold for multiplying with SwapSequence"))
    end
    l = length(seq)
    if l == 0
        return seq
    end
    new_l = Int(ceil(a*l))
    seq[1:new_l]
end

+(seq1::SwapSequence, seq2::SwapSequence) = vcat(seq1,seq2)
+(seq1::SwapSequence, seq2::SwapSequence, seq3::SwapSequence) = vcat(seq1,seq2, seq3)
function +(x::Particle, seq::SwapSequence)
    x = copy(x)
    for (i,j) in seq
        x[i], x[j] = x[j], x[i]
    end
    x
end

function initialize(swarm_size, n_particle, cost_f)
    swarm::Vector{Particle} = []
    for _ in 1:swarm_size
        perm = randperm(n_particle)
        push!(swarm, Particle(perm, cost_f(perm)))
    end
    return swarm
end
```

```{code-cell}
function pso(f; inertia, attr_l, attr_g, swarm_size, n_particle, n_iters)
    swarm::Vector{Particle} = initialize(swarm_size, n_particle, f)
    f_g, i_g = findmin(f, swarm)
    swarm_best = copy(swarm[i_g])
    for _ in 1:n_iters
        for i in 1:length(swarm)
            particle = swarm[i]
            v = inertia*particle.vel + attr_l*rand()*(particle.best - particle) + attr_g*rand()*(swarm_best - particle)
            particle += v
            particle.vel = v
            cost = f(particle)
            if cost < f_g
                f_g = cost
                particle.best = particle.perm
                particle.best_f = cost
                swarm_best = copy(particle)
            elseif cost < particle.best_f
                particle.best = particle.perm
                particle.best_f = cost
            end
            swarm[i] = particle
        end
    end
    return swarm_best, f_g
end
```