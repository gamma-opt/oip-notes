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

# Heuristics

*Heuristic* algorithms sacrifice accuracy for speed, by producing reasonably good solutions much quicker than an optimal algorithm may require.

## Solution construction v. improvement
Many heuristics fall under a _constructive_ versus _perturbative_ search duality.
In constructive search, algorithms make up solutions by iteratively building up one.
A widely used example is _greedy_ approaches where the algorithm at each iteration selects the smallest cost or largest value addition.

Make reference to previous section about Kruskal's being greedy, but more often than not greedy approaches don't yield optimal solutions.

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

+++

### Exploration v. exploitation
Something like both greedy and local search will accept choices that improve immediately, which will be suboptimal if one is stuck in a local optimum. There are a number of strategies to try combatting this
- restarts
- allowing non-improving steps

+++

## A selection of methods

### Bisection and variants (univariate)

### Nelder-Mead? (multi-dimensional)

Nelder-Mead is a derivative-free method to find an optimum of a function.
In absence of derivative information, Nelder-Mead makes use of only function evaluations and an update heuristic, making it simple and flexible for use in many settings, but unable to provide any optimality guarantees.

```{prf:algorithm} Nelder-Mead algorithm
:label: nelder-mead_pseudocode
**Inputs:** an $n$-dimensional function $f$ to minimize and simplex vertices $x_1,\dots,x_{n+1}$.
1. While not converged:
    1. Order the vertices such that $f(x_1)\leq f(x_2)\leq \dots \leq f(x_{n+1})$.
    2. Calculate $\tilde{x} = \frac{1}{n}\sum^n_{i=1}x_i$, the mean of all vertices except the worst one (also known as the _centroid_ of $x_1,\dots,x_n$).
    3. Calculate the **reflection** point $x_r=\tilde{x} + \alpha (\tilde{x}-x_{n+1})$
    4. If $f(x_r) < f(x_1)$, then calculate the **expansion** point $x_e=\tilde{x} + \beta (x_r-\tilde{x})$. Set $x_{n+1}=\min\{x_r, x_e\}$. Return to step 1.
    5. If $f(x_r) < f(x_n)$, then set $x_{n+1}=x_r$. Return to step 1.
    6. If $f(x_r) < f(x_{n+1})$, then set $x_{n+1}=x_r$.
    7. Calculate the **contraction** point $x_c = \tilde{x}+\gamma (x_{n+1} - \tilde{x})$.
    8. If $f(x_c) \leq f(x_{n+1})$, then set $x_{n+1}=x_c$. Return to step 1.
    9. **Shrink** all points $x_i$ with $x_i=(x_i+x_1)/2$.
2. Return the best point
```
Classically, the parameters
```{math}
\alpha = 1,\quad \beta=2,\quad \gamma=\frac{1}{2}
```
are used.

The idea of the algorithm is the following: to optimize an $n$ dimensional function, consider a simplex, which will have $n+1$ vertices.
The algorithm then iteratively replaces the worst performing vertex with a new one by performing one of four operations:

1. _Reflection_ attempts to move from the worst point $x_{n+1}$ towards (the mean of) the rest of the points, which should hopefully be a lower-value region. 
2. If the reflection point is the new best one, the area beyond it may contain even better points. _Expansion_ explores exactly this.
3. If the reflection point is not better, then better points may be expected to be within the simplex, so _contraction_ proposes an inside point to replace the worst one.
4. If the contraction point is not better, then _shrinkage_ moves all the points (except the best one) inside, hoping to find a better landscape.

Convergence for Nelder-Mead is usually assesed using the sample standard deviation of the simplex vertices $s=\sqrt{\frac{1}{n+1}\sum^{n+1}_{i=1}(x_i - \bar{x})^2}$ (where $\bar{x}$ is the mean of the vertices), compared to some tolerance $\epsilon$.
The idea here is that a low standard deviation indicates that the simplex is on a flat region, where it is unclear which direction would improve the search for an optimum.
On the other hand, a high standard deviation would imply a more complicated objective landscape, where it may be easier to find directions of improvement.

```{warning}
Nelder-Mead is making use of a simplex, but this should not be confused with the Simplex algorithm we saw in TODO: Add link to lecture, which was for linear optimisation.
```

Implementing the algorithm in {prf:ref}`nelder-mead_pseudocode` is not too difficult, but in Julia an implementation is provided by [`Optim.jl`](https://julianlsolvers.github.io/Optim.jl/stable/).
```{code-cell}
using Optim

f(x) = (x[1]^2 + x[2] - 11)^2 + (x[1] + x[2]^2 - 7)^2
x0 = [0.0, 0.0]

struct InitialSimplex <: Optim.Simplexer end
Optim.simplexer(S::InitialSimplex, initial_x) = [[-3.,-3.], [0,0], [-3,0]]

opt = Optim.Options(store_trace = true,
                    trace_simplex = true)
res = optimize(f, x0, NelderMead(initial_simplex=InitialSimplex()), opt)
```

% This is the code to produce the animation below.
% Due to a bug in Optim.jl, it won't work right now
% Related issue: https://github.com/JuliaNLSolvers/Optim.jl/issues/1112
% I made the animation by changing Optim locally to have a deepcopy in nelder_mead.jl::trace!
```{code-cell}
:tags: [skip-execution, remove-cell]
using CairoMakie

fig = Figure()
ax = Axis(fig[1,1])
xs = LinRange(-6, 6, 100)
zs = [f([x,y]) for x in xs, y in xs]
levels = 10.0.^range(0.3, 3.5; length=10)
contour!(ax, xs, xs, zs; levels)

tr = Optim.simplex_trace(res)

framerate = 5
simplex = Observable(Point2f.(tr[1]))
triplot!(ax, simplex)
record(fig, "neldermead.mp4", tr; framerate=framerate) do s
    simplex[] = Point2f.(s)
end
```

<video width="800" controls loop autoplay>
    <source src="../_static/neldermead.mp4" type="video/mp4">
</video>

It is worth noting that while Nelder-Mead has the nice properties of a simple implementation and having an easily interpretable heuristic, it is known to be flawed and thus may not always converge to local optima {cite}`mckinnon_convergence_1998`.
In light of this, when derivative-free optimisation is required, the availability of other methods such as Powell's methods or the DIRECT algorithm should be kept in mind, which can be used in Julia for example via [`PRIMA.jl`](https://github.com/libprima/PRIMA.jl) and [`NLopt.jl`](https://github.com/jump-dev/NLopt.jl).

In addition, the advances in automatic differentiation methods may help obviate the need for differentiation-free optimisation methods.
More information about automatic differentiation in the Julia ecosystem can be found in the [JuliaDiff webpage](https://juliadiff.org/).
