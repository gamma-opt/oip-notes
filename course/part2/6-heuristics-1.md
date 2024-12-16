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

**Heuristic** algorithms sacrifice accuracy for speed, by producing reasonably good solutions much quicker than an optimal algorithm may require.

## Solution construction v. improvement
Many heuristics fall under a _constructive_ versus _local_ search duality.
In constructive search, algorithms make up solutions by iteratively building up one.
A widely used example is _greedy_ approaches where the algorithm at each iteration selects the smallest cost or largest value addition. For example, Kruskal's algorithm given in {prf:ref}`kruskal` is a greedy algorithm, because at every iteration the minimum weight edge (that doesn't introduce cycles) is added to the tree.

For TSP, we can devise a similarly greedy algorithm as follows.
```{prf:algorithm} Greedy Traveling Salesperson Problem Algorithm
:label: greedy_tsp
**Inputs:** vertices and a distance matrix
1. Choose a vertex at random (uniformly) as a starting point
2. While there are still vertices we have not visited
    1. Add the closest vertex to our route
3. Add the initial vertex to our route to complete the path
```

Greedy approaches are popular because
- they are easy to conceive and implement, since they involve taking the currently maximal/minimal step, and
- often more efficient than alternative algorithms, since they don't need to compute the globally best iteration.

In addition, for some problems like MSTs, greedy approaches can even be optimal.
However, this is more often an exception rather than the rule.

In _local search_, instead of building up a solution, the algorithm starts with some solution and iteratively tweaks it in order to get closer to an optimum.
What this means may depend a lot on the problem. For example, in TSP, swapping the visit order of two cities or changing the order of one city would both be perturbations.
However, while both these operations will likely change the objective value, there is no reason to think a priori that either perturbation alone will actually improve the objective.
In addition, if changes are not sufficiently big, e.g. swapping two adjacent cities only, they may be at risk of being stuck in a local optimum.

There are a few strategies for dealing with such situations.
For example, one can allow non-improving steps to be accepted after perturbations, which may help escape from the local optima neighborhoods.
A more general strategy is random restarts where an algorithm may be run again with a different initialisation (or a different seed if randomness is involved) and ultimately selecting the best result out of all the runs.

% Todo talk about the concept of a neighbor solution somewhere in here

## A selection of methods

In this section we present two methods that don't yield exact results, but are widely used in the optimisation practice.

### Line search

Suppose we have a univariate function $f$ and an interval $[a,c]$ that we know contains some local minimum $x^*$.
Now, suppose that this function is _unimodal_, which means that 
- $x^*$ is the unique minimum of $f$, 
- $f$ is monotonically decreasing for $x\leq x^*$, and
- $f$ is monotonically increasing for $x\geq x^*$.

We can infer that all convex functions are unimodal.
In addition, for differentiable functions, if we are sufficiently close to a local minimum, we can consider that interval as unimodal as well.
However, unimodality is clearly a more general property than convexity and differentiability.
Here, we present some methods for minimizing unimodal intervals. These methods can of course be used in any interval, but then there may be no guarantees on finding the best optimum.

The most basic one is _ternary search_, where we continually pick two points within the interval.

```{prf:algorithm} Generic line search
**Inputs** function $f$, interval $[a,d]$, tolerance $\epsilon$.
1. While $|d-a|>\epsilon$,
    1. Determine inner points $b$ and $c$.
    2. If $f(b)<f(c)$, shorten towards left, i.e. $d\leftarrow c$
    3. Otherwise, shorten towards right, i.e. $a\leftarrow b$. 
2. Return $\frac{a+d}{2}$
```

To see what is happening here, consider the points $b$ and $c$.
- If $f(b) < f(c)$, then it must be the case that $f$ is increasing for $x>c$, thus we don't need to look there and can shorten our interval to $[a,c]$.
- If $f(b) > f(c)$, we have the symmetrical result where $f$ must be decreasing for $x<b$, so we shorten the interval to $[b,d]$.
- It may be possible that $f(b)=f(c)$, in which case the minimum must be in between them, hence we can update the interval to be $[b,c]$, by adding another case to the if statement. Since the interval $[b,c]$ is contained in both the above options, this is not strictly necessary.

```{figure} ../figures/intervals.svg
Three possibilities for ternary search.
```

An important aspect of how ternary search behaves is dependant on how the two points are selected.
One option is to pick them at equal intervals, which guaranteed removing one-third of the interval.
We could also pick both points around the center to approximately halve our interval.

```{figure} ../figures/interval_reduction.drawio.svg
Different midpoints reduce the interval differently.
```

A related idea is to pick these points so that they can be re-used in the next iteration, as shown in {numref}`golden_reuse`.

```{figure} ../figures/golden.drawio.svg
:name: golden_reuse
Evaluation points of the golden line search in two iterations. If the interval $[a,d]$ is shortened to $[a,c]$, point $b$ can be reused without needing a new function evaluation.
```

The question then is how should we pick $b$ and $c$ such that we can make the search most efficient?
Ideally, the size of the the reduction on the interval should not depend on which way the interval is reduced on.
More generally, how should we pick points so that no matter which side the interval is shortened to, one of them will be reusable?
We can derive this mathematically.
A side-independent reduction means that $[a,c]$ and $[b,d]$ should be of the same length.
Since $[b,c]$ is shared in these intervals, this implies $[a,b]$ and $[c,d]$ should be of the same length.
Let
```{math}
l = \frac{b-a}{d-a}
```
be the ratio of this length to the total distance, and 
```{math}
m = \frac{c-b}{d-a}
```
be the ratio of the shared middle section $[b,c]$.
Then it must be by definition that
```{math}
\frac{d-b}{d-a} = 1-l
```
and by equal reduction of sides
```{math}
:label: equal_sides
m=1-2l.
```

In addition, reusing points across iterations continuously means we'd like to keep these ratios same in the following iterations.
Looking at the next iteration, this means that
```{math}
:label: same_scale
\frac{c-b}{c-a} = \frac{m}{1-l} = l
```

Using equations {eq}`equal_sides` and {eq}`same_scale`, we can solve for $l$
```{math}
&\frac{1-2l}{1-l} = l \\
\implies & l^2-3l+1 = 0 \\
\implies & l = 1- \varphi^{-1}
```
where $\varphi$ is the golden ratio, hence the name of this method _golden section search_.

```{code-cell}
:tags: [remove-output]
function golden_section_search(f, a, d; eps=1e-2)
    # calculate initial midpoints
    l = 1-1/MathConstants.golden
    b = (d-a)*l + a
    c = (d-a)*(1-l) + a
    fb, fc = f(b), f(c)

    while d-a>eps
        # shorten to right
        if fb > fc
            a = b
            b, fb = c, fc
            c = (d-a)*(1-l) + a
            fc = f(c)
        # shorten to left
        else
            d = c
            c, fc = b, fb
            b = (d-a)*l + a
            fb = f(b)
        end
    end
    return (a+d)/2
end
```

<video width="800" controls loop autoplay muted>
    <source src="../_static/golden.mp4" type="video/mp4">
</video>

### Nelder-Mead (multi-dimensional)

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
2. If the reflection point is the new best one, the area beyond it may contain even better points. _Expansion_ explores exactly this prospect.
3. If the reflection point is not better, then better points may be expected to be within the simplex, so _contraction_ proposes an inside point to replace the worst one.
4. If the contraction point is not better, then _shrinkage_ moves all the points (except the best one) inside, hoping to find a better landscape.

```{figure} ../figures/nelder_mead.drawio.svg
:name: nm_ops

Nelder-mead operations illustrated.
```

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

# Optim.simplex requires a user-specified initial simplex
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

<video width="800" controls loop autoplay muted>
    <source src="../_static/neldermead.mp4" type="video/mp4">
</video>

It is worth noting that while Nelder-Mead has the nice properties of a simple implementation and having an easily interpretable heuristic, it is known to be flawed and thus may not always converge to local optima {cite}`mckinnon_convergence_1998`.
In light of this, when derivative-free optimisation is required, the availability of other methods such as Powell's methods or the DIRECT algorithm should be kept in mind, which can be used in Julia for example via [`PRIMA.jl`](https://github.com/libprima/PRIMA.jl) and [`NLopt.jl`](https://github.com/jump-dev/NLopt.jl).

In addition, the advances in automatic differentiation methods may help obviate the need for differentiation-free optimisation methods.
More information about automatic differentiation in the Julia ecosystem can be found in the [JuliaDiff webpage](https://juliadiff.org/).
