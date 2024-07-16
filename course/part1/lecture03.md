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
  display_name: Julia 1.10.4
  language: julia
  name: julia-1.10
---

# Lecture 3

## What is a function?

- Discuss the formal definition of a function and how it relates to the idea of converting inputs to outputs
- Describe function properties (unique outputs)
- Mention example, and show that they can have multiple shapes, discontinuities

_Maybe have a faster intro, "You may be familiar with the concept of functions, here we review the key parts of it" etc._

Thinking of mathematics as a tool for explaining the world arounds us and expressing problems of interest, a need for relating one group of quantities to another quickly arises.
For example, we may be interested in purchasing a certain number {math}`n` of items and wonder about the associated cost {math}`c`, or given a certain year {math}`t` we may be interested in the population {math}`p` of Finland at the start of that year.

There are multiple ways of thinking about functions, for example one may imagine an algebraic formula or a graph, but one general definition is the following (cite Stewart Calculus 9th ed):

```{prf:definition}
:label: function

A **function** {math}`f` is a rule that assigns each element {math}`x` in a set {math}`D` to exactly one element {math}`f(x)` in a set {math}`E`.
```

{prf:ref}`function` is specific enough to satisy what we may expect from functions, for example with a formula {math}`f(x)=(x+2)^2` we cannot input the same value for {math}`x` and end up with different outputs {math}`f(x)`.
Instead, for both the formula and our definition, every input has a unique output.

On the other hand, {prf:ref}`function` is also very general and flexible, making functions a powerful conceptual tool in mathematics.
The formula example is a function, we know that.
We can also have functions in multiple variables, such as {math}`f(x,y)=x+y`, as long as we don't violate the unique outputs rule. This would only require that every element of the set {math}`D` is an ordered pair {math}`(x,y)` instead of a single number.
Alternatively, we can define functions that are difficult to describe as algebraic formulas.
Recall the example with the population of Finland at year {math}`t`, we cannot write a formula for this for multiple reasons, one of which is that we don't yet know many of its values, for example at {math}`t=2100`.

% TODO not sure why this doesn't seem to work https://mystmd.org/guide/reuse-jupyter-outputs#label-a-notebook-cell
```{code-cell} julia
:tags: ["remove-input"]

using CairoMakie
CairoMakie.activate!()

x = range(-π, π, 100)
xlims = (-π, π)

function sigmoid(x)
    t = exp(-abs(x))
    ifelse(x ≥ 0, inv(1 + t), t / (1 + t))
end

fig = Figure(size = (1200, 800))

ax1 = Axis(fig[1,1], limits = (xlims, nothing))
ax2 = Axis(fig[1,2], limits = (xlims, nothing))
ax3 = Axis(fig[2,1], limits = (xlims, nothing))
ax4 = Axis(fig[2,2], limits = (xlims, nothing))

lines!(ax1, x[51:end], repeat([1], 50); linewidth = 3, color = 1, colormap = :tab10, colorrange = (1, 10))
lines!(ax1, x[begin:50], repeat([0], 50); linewidth = 3, color = 1, colormap = :tab10, colorrange = (1, 10))
lines!(ax2, x, abs.(x); linewidth = 3)
lines!(ax3, x, sigmoid.(x); linewidth = 3)
scatter!(ax4, -3:3, [1,2,3,4,3,2,1], markersize = 10)

fig
```

## Function domains

- Describe the notion of for what values it makes sense to evaluate the function
- Define domain formally
- Define subdomains, i.e., subsets of the domain that are of interest
- Discuss open and closed domains

Going back to the population of Finland example, we may not know some values of the function, since the year 2100 has not happened yet.
However, if we were to limit our years of interest to the range 1990-2024, then we could get all the data from [Statistics Finland](https://stat.fi) and have a fully defined function.
This illustrates the importance of the set of input values, called the **domain**, of a function {math}`f`, or the set {math}`D` in {prf:ref}`function`.
Similarly, the set {math}`E`, called the **codomain**, represents where the outputs {math}`f(x)` are located.
With these two sets, a function can be described as {math}`f:X\to Y`. (Maybe ignore domain and just talk about range, or maybe not even that).

## Analysing a function

- Looking at function values to say something about its shape
- Difference of function values and the notion of derivatives and gradients
- When you can calculate them, the notion of smoothness and continuity
- Using gradients to "feel" how the function behaves locally
- Find points where minimum or maximum function evaluation happen using gradients

In optimisation, we are often interested in finding the maxima or the minima of functions, the former could be profit and the latter costs.
If the function does not have a nice structure but rather is a mere collection of points, it may be difficult to figure out the extrema without looking at every single value the function can take.
For example, consider the number of people going into a shop throughout days of a given year.
It may be possible that on June 15th there were 5 customers and on June 16th there were 0.
This information doesn't necessarily indicate anything about June 17th.

In the presence of structure, we may be able to make inferences about the function.
A common example of such structure is continuity, which roughly means that the graph of the function is an uninterrupted line.
One formal definition is the following:

````{prf:definition}
:label: continuity

A function {math}`f:X\to \reals` is continuous at point {math}`a\in X` if 
```{math}
\lim_{x\to a}f(x) = f(a).
```
````

Intuitively, this means that for sufficiently nearby inputs, a continuous function outputs nearby values.

An even stronger structure is that of differentiability.
````{prf:definition}
A function {math}`f:X\to \reals` is differentiable at {math}`a\in X\subseteq \reals` if the derivative
```{math}
f'(a) = \lim_{h\to 0}\frac{f(a+h)-f(a)}{h}
```
exists.
````

````{admonition} Why is differentiability stronger?
:class: seealso, dropdown

Add quick implication
````

The derivative {math}`f'(x)` tells us the instantaneous rate of change at a given point {math}`x`, it is equal to the slope of the tangent line going through the point {math}`f(x)`.
This information can inform our search for the extrema.
As an example, suppose we want to minimize a quadratic function {math}`f(x)=ax^2+bx+c` with {math}`a> 0`.
Since this is a quadratic function, we can infer some global information, i.e. {math}`f` is a parabola, which means it has a single (global) minimum.
If we had a guess {math}`x_0`, we could improve it by calculating the derivative at that point {math}`f(x_0)`. which would tell us which direction to move towards.
We could even note that the derivative is 0 at the minimum, and thus solve this equation to record the minimum at {math}`-\frac{b}{2a}`.

So far, we have been talking about functions of a single variable, but similar ideas extend to multivariate functions.
In fact, {prf:ref}`continuity` for continuity applies as written, assuming now {math}`X=\reals^n` for {math}`n\in\mathbb{N}^+`.

_We don't really need differentiability for \reals^n\to\reals^m. \reals^n\to\reals is enough._

As for differentiability, we need a little adjustment:

````{prf:definition}
A function {math}`f:\reals^n\to\reals^m` is differentiable at a point {math}`x\in\reals^n` if there exists a linear map {math}`J:\reals^n\to\reals^m` such that
```{math}
\lim_{h\to 0}\frac{\|f(x+h)-f(x)-J(h)\|}{\|h\|} = 0.
```
````
