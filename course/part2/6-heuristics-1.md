# Heuristics

*Heuristic* algorithms sacrifice accuracy for speed, by producing reasonably good solutions much quicker than an optimal algorithm may require.

## Solution construction v. improvement
Many heuristics fall under a _constructive_ versus _perturbative_ search duality.
In constructive search, algorithms make up solutions by iteratively building up one.
A widely used example is _greedy_ approaches where the algorithm at each iteration selects the smallest cost or largest value addition.
For TSP, we can write a greedy algorithm as
```{prf:algorithm} Greedy Traveling Salesperson Problem Algorithm
**Inputs:** vertices and a distance matrix
1. Choose a vertex at random (uniformly)
2. While there are still vertices we have not visited
    1. Add the closest vertex to our route
3. Add the initial vertex to our route to complete the path
```

Greedy approaches are popular ...
- easy to conceive
- very efficient
- sometimes optimal

Other constructive heuristics? (different problem?)

Perturbative search
-- introduce
-- give tsp example and algorithm
-- give non tsp example? (same for greedy)
-- mention being stuck at local optima


### Exploration v. exploitation
Something like both greedy and local search will accept choices that improve immediately, which will be suboptimal if one is stuck in a local optimum. There are a number of strategies to try combatting this
- restarts
- allowing non-improving steps


## A selection of methods

### Bisection and variants (univariate)

## Nelder-mead? (multi-dimensional)

