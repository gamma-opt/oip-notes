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

%TODO: Identify a good reference material to build upon. 

# Functions and optimisation

## What is a function?

% Discuss the formal definition of a function and how it relates to the idea of converting inputs to outputs
% Describe function properties (unique outputs)
% Mention example, and show that they can have multiple shapes, discontinuities

% _Maybe have a faster intro, "You may be familiar with the concept of functions, here we review the key parts of it" etc._

For using mathematics as a framework for explaining the world around us to express problems of our interest, the need for relating one group of quantities to another quickly arises. For example, we may be interested in purchasing a certain number {math}`n` of items and wonder about the associated cost {math}`c`, or given a certain year {math}`t` we may be interested in the population {math}`p` of Finland at the start of that year.

There are multiple ways of thinking about functions, for example one may imagine an algebraic formula or a graph, but one general definition is the following (cite Stewart Calculus 9th ed):

```{prf:definition}
:label: def-function

A **function** {math}`f` is a rule that assigns each element {math}`x` in a set, say {math}`X`, to exactly one element {math}`f(x)` in another set, say {math}`Y`.
```

{prf:ref}`def-function` is specific enough to satisfy what we may expect from functions, for example with a formula {math}`f(x)=(x+2)^2` we cannot input the same value for {math}`x` and end up with different outputs {math}`f(x)`. Instead, for both the formula and our definition, every input has a unique output.

On the other hand, {prf:ref}`def-function` is also very general and flexible, making functions a powerful conceptual tool in mathematics. The formula {math}`f(x)=(x+2)^2` is clearly a function. We can also have functions in multiple variables, such as {math}`f(x,y)=x+y`, as long as we don't violate the unique outputs rule. This would only require that every element of the set {math}`X` is an ordered pair {math}`(x,y)` instead of a single number. Alternatively, we can define functions that are difficult to describe as algebraic formulas. Recall the example with the population of Finland at year {math}`t`, we cannot write a formula for this for multiple reasons, one of which is that we don't yet know many of its values, for example at {math}`t=2100`.

In mathematical optimisation, our main objective will be searching for points in the function domain $X$ that yield the maximum (or minimum) value $f(x)$. And, as we will see, the ways of achieving this objective is deeply intertwined with "how the function looks like", i.e., its analytical properties. For the purpose of optimisation tasks, three properties stand out. They are:
  1. **Continuity**
  2. **Differentiability**
  3. **Convexity**  

We will next provide formal definitions of all these, but for now, we can visualise some functions to see what they mean. 

% TODO not sure why this doesn't seem to work https://mystmd.org/guide/reuse-jupyter-outputs#label-a-notebook-cell
```{code-cell} julia
:tags: ["remove-input"]

using CairoMakie

x = range(-π, π, 101)
xlims = (-π, π)

function sigmoid(x)
    t = exp(-abs(x))
    ifelse(x ≥ 0, inv(1 + t), t / (1 + t))
end

f1 = x -> x/π
f2 = x -> 2x/π

fig = Figure(size = (1200, 800))

ax1 = Axis(fig[1,1], limits = (xlims, nothing))
ax2 = Axis(fig[1,2], limits = (xlims, nothing))
ax3 = Axis(fig[2,1], limits = (xlims, nothing))
ax4 = Axis(fig[2,2], limits = (xlims, nothing))

lines!(ax1, x[51:end], repeat([1], 51); linewidth = 3, color = 1, colormap = :tab10, colorrange = (1, 10))
lines!(ax1, x[begin:51], repeat([0], 51); linewidth = 3, color = 1, colormap = :tab10, colorrange = (1, 10))
lines!(ax2, x[begin:50], f1.(x[begin:50]); linewidth = 3)
lines!(ax2, x[50:end], f2.(x[50:end]); linewidth = 3, color = 1, colormap = :tab10, colorrange = (1, 10))
lines!(ax3, x, sigmoid.(x); linewidth = 3)
lines!(ax4, x, exp.(x); linewidth = 3)

fig
```

In the above figure, four functions are illustrated.
- On the top left, the function
```{math}
f(x) = \begin{cases}0&x<0\\1&x\geq 1\end{cases}
```
is continuous and differentiable, except at $x=0$ where it is neither.
- On the top right, the function is continuous everywhere and differentiable except at $x=0$. It is also convex.
- Bottom left function is $\sigma(x)$, which is continuous and differentiable everywhere, but not convex.
- Bottom right function $e^x$ is continuous, differentiable and convex.

Being able to say whether functions are continuous, differentiable, and/or convex allows us to choose the appropriate way to search for optimum points $x \in X$. There are essentially two ways that we can go about searching for optima:

  1. Analytically, by posing the mathematical conditions that a point need to satisfy and using basic algebraic techniques to find such point, or
  2. Use optimisation methods, which are algorithms that are designed to, starting from a initial point $x_0$, move (most of the time) towards a point that satisfy the analytical conditions that we know a optimal solution would.

For most practical cases, we rely on the second idea. That is, we rely on algorithms to search for points that satisfy what we call **optimality conditions**, which are, in turn, informed by the analysis described in 1.

## Analysing a function

%Looking at function values to say something about its shape
%- Difference of function values and the notion of derivatives and gradients
%- When you can calculate them, the notion of smoothness and continuity
%- Using gradients to "feel" how the function behaves locally
%- Find points where minimum or maximum function evaluation happen using gradients

In optimisation, we are interested in finding the maxima or the minima of functions. If the function does not have a nice structure but rather is a mere collection of points, it may be difficult to figure out the extrema without looking at every single value the function can take. For example, consider the number of people going into a shop throughout days of a given year. It may be possible that on June 15th there were 5 customers and on June 16th there were 0. This information does not necessarily indicate anything about June 17th.

### Continuity
The key point is that, in the presence of structure, we may be able to make inferences about the function. Take, for example, continuity, which roughly means that the graph of the function is an uninterrupted line. One formal definition is the following:

````{prf:definition}
:label: continuity

A function {math}`f:X\to \reals` is continuous at point {math}`a\in X` if 
```{math}
\lim_{x \to a}f(x) = f(a).
```
````

Intuitively, {prf:ref}`continuity` means that for sufficiently nearby inputs, a continuous function outputs nearby values. Continuity is a useful property for it removes concerns related to whether the function is defined for a given input or not and whether we can rely on neighbouring evaluations to estimate whether its value is increasing or decreasing.

### Differentiability

This idea of using function evaluations to infer how a function behaves around a given point $x \in X$ is central for computational optimisation methods. Let $x_k$ and $x_{k+1} = x_k + \Delta x$, with $\Delta x > 0$ represent two close-by points in the domain $X$ of $f$. We can then use the rate $d$

```{math}
d = \frac{f(x_{k+1}) - f(x_k)}{x_{k+1} - x_{k}}
```

to guide our search. For example, suppose we would like to find $x \in X$ that maximises $f$. We can use $d$ by looking at its sign:
  1. if $d > 0$ we know that going in the direction of $x_{k+1}$ is a good idea,
  2. whereas if $d < 0$, going in the direction of $x_{k+1}$ is not.

If we take this idea to the limit, i.e., make $\Delta x \to 0$, we recover the *derivative* of the function at $x$, which is precisely an indication of how the function behaves locally in terms of its value. If we can be sure that derivatives are unique and available everywhere in the domain of $f$, we say that the function is *differentiable*.

````{prf:definition}
:label: differentiability

A function {math}`f:X\to \reals` is differentiable at {math}`a \in X \subseteq \reals` if the derivative
```{math}
f'(a) = \lim_{ x \to a}\frac{f(x )-f(a)}{x - a}
```
exists.
````

````{admonition} Why is differentiability stronger than continuity?
:class: seealso, dropdown

Suppose {math}`f` is differentiable at {math}`a`. Then, the limit in {prf:ref}`differentiability` exists and so
```{math}
\lim_{h\to 0} f(a+h)-f(a) &= \lim_{h\to 0}(f(a+h)-f(a))\frac{h}{h} \\
&=  \lim_{h\to 0}\frac{f(a+h)-f(a)}{h}h \\
&= \bigg(\lim_{h\to 0}\frac{f(a+h)-f(a)}{h}\bigg) \bigg(\lim_{h\to 0} h\bigg) \\
&= f'(a)\cdot 0 = 0.
```
This directly implies the definition of continuity {math}`\lim_{h\to 0} f(a+h)=\lim_{x\to a} f(x)=f(a)`.

However, continuity does not imply differentiability.
For example, the function {math}`|x|` is continuous at {math}`x=0` but not differentiable, since the one-sided limits do not match.
````

The derivative {math}`f'(x)` tells us the instantaneous rate of change at a given point {math}`x`, it is equal to the slope of the tangent line going through the point {math}`f(x)`. To see that, notice the following

```{math}
\begin{align}
  & f'(a) = \lim_{x \to a}\frac{f(x) - f(a)}{x - a} \\
  & \Leftrightarrow \lim_{x \to a} \left(\frac{f(x)-f(a)}{x - a} - f'(a)\right) = 0 \\
  & \Leftrightarrow \lim_{\Delta x \to 0} \frac{f(x) - f(a) - f'(a)(x-a)}{x-a} = 0 \\
  & \Leftrightarrow \lim_{\Delta x \to 0} \frac{f(x) - J(x)}{x - a} = 0
\end{align}
```

where $J(x) = f(a) + f'(a)(x - a)$ is the linear approximation of $f(x)$ at $x = a$, i.e., the tangent line to $f$ going through $f(a)$. Clearly, this information is useful in our search for extrema, although we also must take into account how further we move in the direction of interest.

% TODO: Add an numerical example where we do a series of steps towards the an extrema using derivative information. We will need to use a decaying step size for 
% it to make sense
```{code-cell} julia
:tags: ["remove-input"]

using WGLMakie, Bonito
WGLMakie.activate!()

xlims = (-π, π)

app = App() do session
    slider = Bonito.Slider(x)
    fig, ax, lplot = lines(x, sin.(x); linewidth = 3)
    xlims!(ax, xlims)

    p = @lift(Point($slider[], sin($slider[])))
    splot = scatter!(ax, p; color = 2, colormap = :tab10, colorrange = (1, 10))

    slope = cos(slider[])
    intercept = sin(slider[]) - slope*slider[]
    abplot = ablines!(ax, [intercept], [slope]; color = 3, colormap = :tab10, colorrange = (1, 10))

    onjs(session, slider.value, js"""function on_update(new_val) {
        $(splot).then(plots=>{
            const scatter = plots[0]
            scatter.geometry.attributes.pos.array[0] = new_val
            scatter.geometry.attributes.pos.array[1] = Math.sin(new_val)
            scatter.geometry.attributes.pos.needsUpdate = true
        })
    }
    """)
    onjs(session, slider.value, js"""function on_update(new_val) {
        const slope = Math.cos(new_val);
        const intercept = Math.sin(new_val) - slope*new_val;
        const start_y = slope*(-Math.PI) + intercept;
        const end_y = slope*Math.PI + intercept;

        $(abplot).then(plots=>{
            const abplot = plots[0]
            // change the y coord for the (start/end)points of the line
            abplot.geometry.attributes.linepoint_end.data.array[3] = start_y
            abplot.geometry.attributes.linepoint_end.data.array[5] = end_y
            abplot.geometry.attributes.linepoint_end.needsUpdate = true
        })
    }
    """)

    return DOM.div(slider, fig)
end
```

<!-- As an example, suppose we want to minimize a quadratic function {math}`f(x)=ax^2+bx+c` with {math}`a> 0`.
Since this is a quadratic function, we can infer some global information, i.e. {math}`f` is a parabola, which means it has a single (global) minimum.
If we had a guess {math}`x_0`, we could improve it by calculating the derivative at that point {math}`f(x_0)`. which would tell us which direction to move towards.
We could even note that the derivative is 0 at the minimum, and thus solve this equation to record the minimum at {math}`-\frac{b}{2a}`. -->

So far, we have been talking about functions of a single variable, but similar ideas extend to multivariate functions.
In fact, {prf:ref}`continuity` for continuity applies as written, assuming now {math}`X=\reals^n` for {math}`n\in\mathbb{N}^+`.

Differentiability in higher dimensions is somewhat analogous. First, we must define the multidimensional equivalent to the tangent line. For that, we need to first the notion of partial derivatives, which is essentially taking derivatives with one of the components of $f$.

````{prf:definition}
:label: partial_derivative

Consider the function $f(x_1,x_2)$ such that {math}`f: X \subseteq \reals^2 \to \reals`. The *partial derivative* of $f$ with respect to $x_1$ is
```{math}
\frac{\partial f(x)}{\partial x_1} = \lim_{ h \to 0}\frac{f(x_1+h, x_2)-f(x_1, x_2)}{h},
```
provided this limit exists. Analogously, the derivative of $f$ with respect to $x_2$ is
```{math}
\frac{\partial f(x)}{\partial x_2} = \lim_{ h \to 0}\frac{f(x_1, x_2+h)-f(x_1, x_2)}{h},
```
provided this limit exists. 

The vector $\nabla f(x_1, x_2) = \left[\frac{\partial f(x)}{\partial x_1}, \frac{\partial f(x)}{\partial x_2}\right]$ is the *gradient* of $f$ at $(x_1, x_2)$.
````

The multidimensional equivalent to the tangent line, or the tangent hyperplane, is defined as

```{math}
J(a, b) = f(a , b) + \nabla f(a,b)^\top (x_1 - a, x_2 - b),
```

where $\nabla f(a, b)$ is the *gradient* of $f$ at $(a, b)$.

```{code-cell} julia
:tags: ["remove-input"]

f(x,y) = -x^2-y^2
z = [f(i,j) for i in x, j in x]
# restrict slider_range to nicely behaving tangent planes, easier than fixing the visual otherwise
m = 0.5
slider_range = filter(x->x<m && x>-m, x)

app = App() do session
    x_slider = Bonito.Slider(slider_range)
    y_slider = Bonito.Slider(slider_range)
    x_slider[] = 0
    y_slider[] = 0
    fig, ax, plot = surface(x, x, z)

    p = @lift(Point($x_slider[], $y_slider[], f($x_slider[], $y_slider[])))
    splot = scatter!(ax, p; color = 2, colormap = :tab10, colorrange = (1, 10))

    z2 = [0 for i in x, j in x]
    surplot = surface!(ax, x, x, z2)

    evaljs(session, js"""
        const observables = $([x_slider.value, y_slider.value])
        const f = (x,y) => -(x**2)-(y**2)
        const der = (x) => -2*x

        function update(args) {
            const [x, y] = args;
            $(splot).then(plots=>{
                const scatter = plots[0]
                scatter.geometry.attributes.pos.array[0] = x
                scatter.geometry.attributes.pos.array[1] = y
                scatter.geometry.attributes.pos.array[2] = f(x,y)
                scatter.geometry.attributes.pos.needsUpdate = true
            });
            $(surplot).then(plots=>{
                const surface = plots[0]
                for (let i = 0; i<=101*101; i++){
                    const x0 = surface.geometry.attributes.position.array[3*i]
                    const y0 = surface.geometry.attributes.position.array[3*i+1]
                    surface.geometry.attributes.position.array[3*i+2] = der(x)*(x0-x) + der(y)*(y0-y) + f(x,y)
                    surface.geometry.attributes.position.needsUpdate = true
                }
            });
        }
        Bonito.onany(observables, update)
        update(observables.map(x=> x.value))
        """)
    
    return DOM.div(x_slider, y_slider, fig)
end
```

With that, we are ready to define differentiability for the multidimensional case.

````{prf:definition}
:label: differentiability_multi

Consider the function {math}`f: X \subseteq \reals^2 \to \reals`. Suppose its partial derivatives are defined at $(a,b) \in x$. Let $J(a, b) = f(a, b) + \nabla f(a,b)^\top (x_1 - a, x_2 - b)$ with $\nabla f(a,b)$ being the gradient of $f$ at $(a,b)$.

We say that $f$ is differentiable at $(a,b)$ if

```{math}
\lim_{(x_1, x_2) \to (a,b)} \frac{f(x_1, x_2) - J(x_1, x_2)}{||(x_1, x_2) - (a,b)||} = 0.
```

If either of the partial derivatives do not exist, or the above limit does not exist or is not 0, then $f$ is not differentiable at $(a,b)$. 

````

As we will see later, the gradient plays a crucial role in many of the optimisation methods that we will use. This is precisely because it serves as an indicator of how the fnction behaves locally, by serving as the normal vector of the tangent plane at that point. We will return to that point in part two. For the purpose of our  discussion, let us now focus on how to use the gradient to find minima and maxima. 


## Function shapes, convexity and its role in optimisation

One crucial feature about gradients is that they can be used to identify points that are candidate to being optimal. To see that, assume taht $f$ is differentiable, in line with {ref:prf}`differentiability_multi`. Assume that $f : \reals^2 \to \reals$ for simplicity and that we are at point $(a,b)$. For a sufficiently small step away from $(a,b)$ towards any point $(x_1, x_2)$, we seen that $J(a, b) = f(a , b) + \nabla f(a,b)^\top (x_1 - a, x_2 - b)$ is a arbitrarily good approximation for $f(x_1,x_2)$. We can use this to realise something about optimality: if $(a,b)$ is to be an optimal point (say, a minimum point), we must have

```{math}
f(a,b) \le f(x_1, x_2), \text{ for all } (x_1,x_2) \in X,
```

which, can only be true if $\nabla f(a,b) = 0$. Thus, having zero gradients is a necessary condition for a point to be optimal. Cleary, verifying that the gradient is zero is not sufficient for one to state that $(a,b)$ is an optimal point, because one must also that into account curvature.  Figure XXX below illustrates some alternative cases. Noticer that in two of them we can trust the zero-gradient condition to be the indication of optimality, while it is not the case in the others.

%TODO: Draw this: have a couple of functions, where one is concave and the other is convex. 

The next natural step after identifying points with zero gradient would be further analysing the function curvature, which can be done using second-order derivatives (i.e., the derivatives of derivatives). However, it turns out that most optimisation algorithms do not consider second-order information, simply because it is too expensive from a computational standpoint.

However, not all is lost. Indeed, for a particular class of problems, it turns out that we can rely on the zero-gradient condition as a sufficient certificate to atest optimality. These are so-called convex problems, which are optimisation problems involving convex functions. Let us first define a convex function.

````{prf:definition}
:label: convex_function

A function is convex if for all $x, y \in \reals^n$ and $\lambda \in [0,1]$ we have that

```{math}
 f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda) f(y).
```

````

```{attention}
Notice we have defined it considering $n$ dimensions instead of one or two, as before. This is simply to make our notation more compact (and our results more general).
```

According to definition {ref:prf}`convex_function`, a convex function is such that, if we take any two points and connect with a line, the line should sit above $f$ between these two points. This simple technique can be to classify the functions from Figure XXX. 
%TODO: use this idea to classify the example functions above which are convex and which are not.

To say why the zero-gradient condition is sufficient for optimality, notice that, from the definition of convexity we have:

```{math}
\begin{align*}
  & f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda) f(y) \\
  \Rightarrow  & f(x + \lambda(y-x)) \le \lambda (f(y) - f(x)) \\
  \Rightarrow  & f(y) - f(x) \ge \frac{f(x + \lambda(y-x)) - f(x)}{\lambda}, \text{ for } \lambda \in (0,1]
  \Rightarrow  & f(y) - f(x) \ge \lim_{\lambda \to 0} \frac{f(x + \lambda(y-x)) - f(x)}{\lambda}, \text{ for } \lambda \in (0,1]
  \Rightarrow  & f(y) - f(x) \ge \nabla f(x)(y-x).
\end{align* }  
```

From the last line we can conclude that, if $\nabla f(x) = 0$, that implies that $f(x) \le f(y)$ for all $y$, which is precisely the definition of optimality.

<!-- - Define the notion of convexity from an intuitive standpoint
- Discuss that if a function is convex one only need to find THE point where nabla f = 0 to find the optimum -->


## Function domains

<!-- - Describe the notion of for what values it makes sense to evaluate the function (done)
- Define domain formally
- Define subdomains, i.e., subsets of the domain that are of interest
- Discuss open and closed domains -->

Going back to the population of Finland example, we may not know some values of the function, since the year 2100 has not happened yet.
However, if we were to limit our years of interest to the range 1990-2024, then we could get all the data from [Statistics Finland](https://stat.fi) and have a fully defined function. This illustrates the importance of the set of input values, called the **domain**, of a function {math}`f`, or the set {math}`X` in {prf:ref}`def-function`. Similarly, the set {math}`Y`, called the **codomain**, represents where the outputs {math}`f(x)` are located. With these two sets, a function can be formally described as {math}`f: X \to Y`.

As we will see in our future lectures, often we are interested in optimising functions within **subdomains**, that is, subsets of its original domain. In mathematical programming, these subsets are typically generated by functions as well. We will defer the discussion on how functions can generate subdomains, but one critical point must be made about these sets: subdomains make everything more difficult! 

For example, even if $f$ is convex, it may be that the point $x$ for which $\nabla f(x) = 0$ is not part of the subdomain. In this case, we need a more comprehensive analysis that take into account the structure of the subdomain. We will come back to this point later. 