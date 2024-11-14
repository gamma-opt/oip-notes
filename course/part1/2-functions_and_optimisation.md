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


(p1l2)=
# Functions and optimisation

## What is a function?

When using mathematics as a framework for explaining the world around us in order to express problems of our interest, the need for relating one group of quantities to another quickly arises. For example, we may be interested in purchasing a certain number {math}`n` of items and wonder about the associated cost {math}`c`, or given a certain year {math}`t` we may be interested in the population {math}`p` of Finland at the start of that year.

There are multiple ways of thinking about functions, for example one may imagine an algebraic formula or a graph, but one general definition is the following {cite}`stewart_calculus_2021`:

```{prf:definition}
:label: def-function

A **function** {math}`f` is a rule that assigns each element {math}`x` in a set, say {math}`X`, to exactly one element {math}`f(x)` in another set, say {math}`Y`.
```

{prf:ref}`def-function` is specific enough to satisfy what we may expect from functions, for example with a formula {math}`f(x)=(x+2)^2` we cannot input the same value for {math}`x` and end up with different outputs {math}`f(x)`. Instead, for both the formula and our definition, every input has a unique output.

On the other hand, {prf:ref}`def-function` is also very general and flexible, making functions a powerful conceptual tool in mathematics. The formula {math}`f(x)=(x+2)^2` is clearly a function. We can also have functions in multiple variables, such as {math}`f(x,y)=x+y`, as long as we do not violate the unique outputs rule. This would only require that every element of the set {math}`X` is an ordered pair {math}`(x,y)` instead of a single number. Alternatively, we can define functions that are difficult to describe as algebraic formulas. Recall the example with the population of Finland at year {math}`t`, we cannot write a formula for this for multiple reasons, one of which is that we don't yet know many of its values, for example at {math}`t=2100`.

In mathematical optimisation, our main objective will be searching for points in the function domain $X$ that yield the maximum (or minimum) value $f(x)$. And, as we will see, the ways of achieving this objective is deeply intertwined with "how the function looks like", i.e., its **analytical properties**. For the purpose of optimisation tasks, three properties stand out. They are:

  1. **Continuity**
  2. **Differentiability**
  3. **Convexity**  

We will next provide formal definitions of all these, but for now, let us visualise some functions to see what they mean. 

% In myst there is a way of capturing the code output and wrapping it in a figure
% https://mystmd.org/guide/reuse-jupyter-outputs#label-a-notebook-cell
% But it doesn't work in jupyter-book v1

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
foo = x -> if x < 0 f1(x) else f2(x) end

fig = Figure(size = (1200, 800))

ax1 = Axis(fig[1,1], limits = (xlims, nothing))
ax2 = Axis(fig[1,2], limits = (xlims, nothing))
ax3 = Axis(fig[2,1], limits = (xlims, nothing))
ax4 = Axis(fig[2,2], limits = (xlims, nothing))

lines!(ax1, x[51:end], repeat([1], 51); linewidth = 3, color = 1, colormap = :tab10, colorrange = (1, 10))
lines!(ax1, x[begin:51], repeat([0], 51); linewidth = 3, color = 1, colormap = :tab10, colorrange = (1, 10))
lines!(ax2, x, foo; linewidth = 3)
lines!(ax3, x, sigmoid; linewidth = 3)
lines!(ax4, x, exp; linewidth = 3)

fig
```

In the above figure, four functions are illustrated.

- On the top left, the function
- 
```{math}
f(x) = \begin{cases}0&x<0\\1&x\geq 1\end{cases}
```

is continuous and differentiable, except at $x=0$ where it is neither.

- On the top right, the function is continuous everywhere and differentiable except at $x=0$. It is also convex.
- Bottom left function is the standard logistic function $\sigma(x)$, which is continuous and differentiable everywhere, but not convex.
- Bottom right function $e^x$ is continuous, differentiable and convex.

Being able to say whether functions are continuous, differentiable, and/or convex allows us to choose the appropriate way to search for optimum points $x \in X$. There are essentially two ways that we can go about searching for optima:

  1. **Analytically**, by posing the mathematical conditions that a point need to satisfy and using basic algebraic techniques to find such point, or
  2. **Use optimisation methods**, which are algorithms that are designed to, starting from a initial point $x_0$, move (most of the time) towards a point that satisfy the analytical conditions that we know a optimal solution would.

For most practical cases, we rely on the second idea. That is, we rely on algorithms to search for points that satisfy what we call **optimality conditions**, which are, in turn, informed by the analysis described in 1.

## Analysing a function

### Continuity

How optimisation methods move towards optimal points is determined by inferences we can make about the function based on structure that it may have.
Take, for example, continuity, which roughly means that the graph of the function is an uninterrupted line. One formal definition is the following:

````{prf:definition}
:label: continuity_def

A function {math}`f:X\to \reals` is continuous at point {math}`a\in X` if 
```{math}
\lim_{x \to a}f(x) = f(a).
```
````

Intuitively, {prf:ref}`continuity_def` means that for sufficiently nearby inputs, a continuous function gives nearby outputs. Continuity is a useful property since it removes concerns related to whether the function is defined for a given input or not and allows us to rely on neighbouring evaluations to estimate whether the function's value is increasing or decreasing.

### Differentiability

This idea of using function evaluations to infer how a function behaves around a given point $x \in X$ is central for computational optimisation methods. Let $x_k$ and $x_{k+1} = x_k + \Delta x$, with $\Delta x > 0$, represent two close-by points in the domain $X$ of $f$. We can then use the rate $d$

```{math}
d = \frac{f(x_{k+1}) - f(x_k)}{x_{k+1} - x_{k}}
```

to guide our search. For example, suppose we would like to find $x \in X$ that maximises $f$. We can use $d$ by looking at its sign:

1. if $d > 0$ we know that going in the direction of $x_{k+1}$ is a good idea,
2. whereas if $d < 0$, going in the direction of $x_{k+1}$ is not.

If we take this idea to the limit, i.e., make $\Delta x \to 0$, we recover the **derivative** of the function at $x$, which is precisely an indication of how the function behaves locally in terms of its value. If we can be sure that derivatives are unique and available everywhere in the domain of $f$, we say that the function is *differentiable*.

````{prf:definition}
:label: differentiability_def

A function {math}`f:X\to \reals` is differentiable at {math}`a \in X \subseteq \reals` if the derivative
```{math}
f'(a) = \lim_{ x \to a}\frac{f(x )-f(a)}{x - a}
```
exists.
````

````{admonition} Why is differentiability stronger than continuity?
:class: seealso, dropdown

Suppose {math}`f` is differentiable at {math}`a`. Then, the limit in {prf:ref}`differentiability_def` exists and so
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
  & f'(a) = \lim_{x \to a}\frac{f(x) - f(a)}{x - a} \\
  & \Leftrightarrow \lim_{x \to a} \left(\frac{f(x)-f(a)}{x - a} - f'(a)\right) = 0 \\
  & \Leftrightarrow \lim_{\Delta x \to 0} \frac{f(x) - f(a) - f'(a)(x-a)}{x-a} = 0 \\
  & \Leftrightarrow \lim_{\Delta x \to 0} \frac{f(x) - J(x)}{x - a} = 0
```

where $J(x) = f(a) + f'(a)(x - a)$ is the linear approximation of $f(x)$ at $x = a$, i.e., the tangent line to $f$ going through $f(a)$. One important conclusion we gather from the above is that, if a given point $x$ is sufficiently close to $a$, $f(x)$ and $J(x)$ are close in value, and as such $J$ to approximate $f$. Clearly, this information is useful in our search for optimal points, although we also must take into account how far we move in the direction of interest.

An example of using derivative information for finding an optimum is plotted below. Notice that this process is not perfect and different starting locations may lead to different optima.

```{code-cell}
:tags: [remove-input]
f(x) = x^4 - 3*x^3 + x^2 + x
xs = range(-1, 3, 100)

fig, ax, plot = lines(xs, f)
limits!(-1, 3, -2.5, 2)
x1 = [2.5, 1.1, 2.3, 1.5, 2.08, 1.8, 2]
x2 = [-0.6, 0.3, -0.4, 0, -0.2]

for (i, x) in enumerate([x1,x2])
  points = collect(zip(x, map(f,x)))
  scatter!(ax, points, color=1+i, colormap=:tab10, colorrange=(1,10))
  lines!(ax, points, color=1+i, colormap=:tab10, colorrange=(1,10))
end

fig
```

The figure below shows the sine function, along with the tangent line. Notice how the orange line is a good approximation of the blue line close to the green dot. Also, notice how we can, by looking at the inclination of the tangent line tell whether the function is going up or down in value. Make sure you move the slider to see the tangent line at different points.

```{code-cell} julia
:tags: ["remove-input"]

using WGLMakie, Bonito
WGLMakie.activate!()

xlims = (-π, π)

app = App() do session
    slider = Bonito.Slider(x; style=Styles("grid-column" => "2"))
    fig, ax, lplot = lines(x, sin; linewidth = 3)
    xlims!(ax, xlims)

    p = @lift(Point($slider[], sin($slider[])))
    splot = scatter!(ax, p; color = 3, colormap = :tab10, colorrange = (1, 10), markersize=20)

    slope = cos(slider[])
    intercept = sin(slider[]) - slope*slider[]
    abplot = ablines!(ax, [intercept], [slope]; color = 2, colormap = :tab10, colorrange = (1, 10), linewidth=2)

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
    grid = Grid(
      slider, 
      DOM.div(fig; style=Styles("grid-column" => "1 / 4", "justify-self" => "center")); 
      width="800px", 
      height="500px", 
      justify_content="center",
      rows = "25px 1fr",
      columns = "145px 1fr 100px"
    )

    return grid
end
```

<!-- As an example, suppose we want to minimize a quadratic function {math}`f(x)=ax^2+bx+c` with {math}`a> 0`.
Since this is a quadratic function, we can infer some global information, i.e. {math}`f` is a parabola, which means it has a single (global) minimum.
If we had a guess {math}`x_0`, we could improve it by calculating the derivative at that point {math}`f(x_0)`. which would tell us which direction to move towards.
We could even note that the derivative is 0 at the minimum, and thus solve this equation to record the minimum at {math}`-\frac{b}{2a}`. -->

So far, we have been talking about functions of a single variable, but similar ideas extend to multivariate functions (that is, function with more than one (dimension) variable as their input (in their domain)).
In fact, {prf:ref}`continuity_def` for continuity applies as written, assuming now {math}`X=\reals^n` for {math}`n\in\mathbb{N}^+`.

First, we must define the multidimensional equivalent to the tangent line. For that, we need to first the notion of partial derivatives, which is essentially taking derivatives with one of the components of $f$.

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

Here is how it looks like for a function $f(x,y) = -x^2 - y^2$. As before, notice how the inclination the plane has, generally governed by the gradient vector of the function, can be used to infer how the function behaves around the point (in orange).

```{margin}
This plot can be moved with left-click and rotated with Ctrl+left-click.
```

```{code-cell} julia
:tags: ["remove-input"]

x = range(-π/2, π/2, 101)

f(x,y) = -x^2-y^2
z = [f(i,j) for i in x, j in x]
# restrict slider_range to nicely behaving tangent planes, easier than fixing the visual otherwise
m = 0.5
slider_range = filter(x->x<m && x>-m, x)

app = App() do session
    x_slider = Bonito.Slider(slider_range; style=Styles("grid-column" => "2"))
    y_slider = Bonito.Slider(slider_range; style=Styles("grid-column" => "2"))
    x_slider[] = 0
    y_slider[] = 0
    fig = Figure(size = (600, 600))
    ax = LScene(fig[1,1])
    plot = surface!(ax, x, x, z)

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

    x_label = DOM.div("x:", style=Styles("justify-self" => "end", "grid-column" => "1", "grid-row" => "1"))
    y_label = DOM.div("y:", style=Styles("justify-self" => "end", "grid-column" => "1", "grid-row" => "2"))
    grid = Grid(
      x_label,
      y_label,
      x_slider,
      y_slider, 
      DOM.div(fig; style=Styles("grid-column" => "1 / 4", "justify-self" => "center")); 
      width="800px", 
      height="700px", 
      justify_content="center",
      rows = "25px 25px 1fr",
      columns = "145px 1fr 100px"
    )

    return grid
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

As we will see later, the gradient plays a **crucial role** in many of the optimisation methods that we will use. This is precisely because the gradient vector serves as an indicator of how the function behaves locally, pointing towards the direction of of "fastest" value increase. We will return to that point in part two. For the purpose of our discussion, let us now focus on how to use the gradient to find minima and maxima.

## Function shapes, convexity and its role in optimisation

One crucial feature about gradients is that they can be used to identify points that are candidate to being optimal. To see that, assume that $f$ is differentiable, in line with {prf:ref}`differentiability_multi`. Assume that $f : \reals^2 \to \reals$ for simplicity and that we are at point $(a,b)$. For a sufficiently small step away from $(a,b)$ towards any point $(x_1, x_2)$, we have seen that $J(a, b) = f(a , b) + \nabla f(a,b)^\top (x_1 - a, x_2 - b)$ is an arbitrarily good approximation for $f(x_1,x_2)$. We can use this to realise something about optimality: if $(a,b)$ is to be an optimal point (say, a minimum point), we must have

```{math}
f(a,b) \le f(x_1, x_2), \text{ for all } (x_1,x_2) \in X,
```

which, can only be true if $\nabla f(a,b) = 0$. Otherwise, we could move in its opposite direction and find another point $(x_1,x_2)$ where $f(x_1,x_2) < f(a,b)$. Thus, having zero gradients is a necessary condition for a point to be optimal. Cleary, verifying that the gradient is zero is not sufficient for one to state that $(a,b)$ is an optimal point, because one must also that into account curvature.

The function plotted below illustrates some alternative cases. Notice that in two of the cases (purple and red) we can trust the zero-gradient condition to be the indication of optimality, while it is not the case for the saddle point in orange.

```{code-cell}
:tags: [skip-execution, remove-cell]
# This cell produces the video below, but needs manual running
x = range(-π, π, 101)
foo2(x,y) = sin(x)*sin(y)
z = [foo2(i,j) for i in x, j in x]
fig = Figure(size=(800, 450))
ax = Axis3(fig[1,1], viewmode=:fit)
hidespines!(ax)
hidedecorations!(ax)
#ax = LScene(fig[1,1])

surface!(ax, x, x, z)
scatter!(ax, [-π/2, pi/2, 0, π/2, -pi/2], [π/2, -pi/2, 0, π/2, -pi/2], [-1, -1, 0, 1, 1]; color = [4,4,2,5,5], colormap = :tab10, colorrange = (1, 10), markersize=20)

azimuth_it = range(0, 2*pi, 300)
record(fig, "course/_static/critical_points.mp4", azimuth_it) do az
  ax.azimuth = az
end
```

<video id="critical_points" width="800" controls loop autoplay>
    <source src="../_static/critical_points.mp4" type="video/mp4">
</video>

The next natural step after identifying points with zero gradient would be further analysing the function curvature, which can be done using second-order derivatives (i.e., the derivatives of derivatives). For example, consider the functions plotted below, where $x^2$ is convex and $-x^2$ is concave. Their derivatives are $2x$ and $-2x$ respectively, both of which are 0 when $x=0$. Yet their second derivatives are $2$ and $-2$, where the difference in the sign indicates exactly the difference in curvature. However, it turns out that most optimisation algorithms do not consider second-order information, simply because it is too expensive from a computational standpoint.

```{code-cell}
:tags: ["remove-input"]

fig = Figure(size = (800, 300))

ax1 = Axis(fig[1,1], limits = (xlims, nothing))
ax2 = Axis(fig[1,2], limits = (xlims, nothing))

lines!(ax1, x, x -> x^2; linewidth = 3, label = L"x^2")
lines!(ax2, x, x -> -x^2; linewidth = 3, label=L"-x^2")

axislegend(ax1)
axislegend(ax2)

fig
```

```{note}
In part 2, we discuss in more details why one can use second-order derivatives to infer the function curvature and what necessary and sufficient conditions for a point to be a minimum or a maximum. For now, we do not need to delve further in that direction.

```

Still, not all is lost. Indeed, for a particular class of problems, it turns out that we can rely on the zero-gradient condition as a sufficient certificate to test optimality. These are so-called **convex problems**, which are optimisation problems involving convex functions. Let us first define a convex function.

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

According to definition {prf:ref}`convex_function`, a convex function is such that, if we take any two points and connect with a line, the line should sit above $f$ between these two points. This simple technique can be used to classify the functions plotted below, where the left column contains convex functions and the right non-convex.

% In (old) jupyter-book, we can't wrap code outputs in a figure
% There is a way in the new one though https://mystmd.org/guide/reuse-jupyter-outputs#outputs-as-figures
```{code-cell}
:tags: [remove-input]
:label: test
x = range(-pi, pi, 100)
f(x,y) = (x^2-y^2)/2
fig = Figure(size=(800,600))
ax1 = Axis(fig[1,1])
lines!(ax1, range(1,10,100), exp)

ax2 = Axis(fig[1,2])
lines!(ax2, x, sin)

ax3 = Axis3(fig[2,1])
surface!(ax3, x, x, (x,y) -> x^2 + y^2)

ax4 = Axis3(fig[2,2])
surface!(ax4, x, x, f)

fig
```

To see why the zero-gradient condition is sufficient for optimality, notice that, from the definition of convexity we have:

```{math}
  & f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda) f(y) \\
  \Rightarrow  & f(x + \lambda(y-x)) \le \lambda (f(y) - f(x)) \\
  \Rightarrow  & f(y) - f(x) \ge \frac{f(x + \lambda(y-x)) - f(x)}{\lambda}, \text{ for } \lambda \in (0,1] \\
  \Rightarrow  & f(y) - f(x) \ge \lim_{\lambda \to 0} \frac{f(x + \lambda(y-x)) - f(x)}{\lambda}, \text{ for } \lambda \in (0,1] \\
  \Rightarrow  & f(y) - f(x) \ge \nabla f(x)(y-x).
```

From the last line we can conclude that, if $\nabla f(x) = 0$, that implies that $f(x) \le f(y)$ for all $y$, which is precisely the definition of optimality.



## Function domains

Going back to the population of Finland example, we may not know some values of the function, since the year 2100 has not happened yet.
However, if we were to limit our years of interest to the range 1990-2024, then we could get all the data from [Statistics Finland](https://stat.fi) and have a fully defined function. This illustrates the importance of the set of input values, called the **domain**, of a function {math}`f`, or the set {math}`X` in {prf:ref}`def-function`. Similarly, the set {math}`Y`, called the **codomain**, represents where the outputs {math}`f(x)` are located. With these two sets, a function can be formally described as {math}`f: X \to Y`.

As we will see in our future lectures, often we are interested in optimising functions within **subdomains**, that is, subsets of its original domain. In mathematical programming, these subsets are typically generated by functions as well. We will defer the discussion on how functions can generate subdomains, but one critical point must be made about these sets: subdomains make everything more difficult! 

For example, even if $f$ is convex, it may be that the point $x$ for which $\nabla f(x) = 0$ is not part of the subdomain. In this case, we need a more comprehensive analysis that take into account the structure of the subdomain. We will come back to this point later. 