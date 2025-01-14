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

# Basics of calculus for optimisation

Before we proceed further, we will need to revisit (or visit for the first time) some key concepts form calculus. Essentially, we are interested in understanding how we can pose the conditions that a given solution must satisfy such that we can guarantee that the solution can called optimal. There several particular aspects to be considered, the most crucial is whether we are dealing with unconstrained or constrained optimisation problems. We will first consider the case without constraints.

## One-dimensional function calculus

In [Lecture 2](../part1/2-functions_and_optimisation.md), we discussed some central aspects related to analysing functions and, very importantly, we discussed the notion of derivatives and gradients.

As a refresher, let us revisit the main definitions we will be using. We start with continuity and differentiation, since our focus will be placed for now on differentiable functions. First, we exclusively focus on one-dimensional functions.

````{prf:definition}
:label: p2l1:continuity_def

Let {math}`f:\reals \to \reals` be a function. We say that {math}`lim_{x \to a} f(x) = c` if, as $x$ becomes closer to $a$, $f(x)$ becomes closer to $c$ (i.e., asymptotically). Moreover, $f$ is continuous at point {math}`a \in \reals` if 
```{math}
\lim_{x \to a}f(x) = f(a).
```
If {math}`\lim_{x \to a}f(x) = f(a)` for all $a \in \reals$, we say that the function is continuos.
````

If a function is continuos, we can hope for it to be differentiable as well. Let's us restate a slightly different definition of  differentiability than that presented in [Lecture 2](../part1/2-functions_and_optimisation.md).


````{prf:definition}
:label: differentiability_def_delta

A function {math}`f:\reals \to \reals` is differentiable if the derivative
```{math}
f'(a) = \lim_{ \Delta x \to 0}\frac{f(a + \Delta x )-f(a)}{\Delta x}
```
exists for all $x \in \reals$.
````

```{note}
Both definitions are equivalent, though here we consider it without an explicit domain $X$. If you define $\Delta x = x - a$ and you can see they are equivalent.
```

The importance of differentiability is that the derivative provides information regarding the local behaviour of $x$, that is

- if $f'(x) > 0$, the function is **increasing** at $x$. That is, for an arbitrarily small $\epsilon > 0$, $f(x + \epsilon) > f(x)$.
- Likewise, $f'(x) < 0$ means that the function is **decreasing** at $x$.

Another important notion that we will use is that of $n^\text{th}$-order derivatives. Let us first define it formally.

````{prf:definition}
The $n^\text{th}$-order derivative $f^{(n)}(a)$ of $f$ at $a$ is the derivative of $f^{(n-1)}(a)$ at $a$. As a convention, we assume $f^{(0)}(a) = f(a)$.
````

Notice that as we take derivatives of derivatives, we can infer information regarding how fast or how slow a function value change is changing. Think about it: if the growth rate (i.e., its derivative) of a function is increasing rather than being constant, the function must be "bending upwards" as $x$ increases. Analogously, if this rate is decreasing, the function must be bending downwards. Thus, we can use second order derivatives to infer about the **curvature** of functions around a given point.

## Critical points and optimality

We can use derivatives to infer whether points are locally optimal. Let us first define the notion of local optimality.

````{prf:definition}
:label: local_optima

A point $a$ is locally optimal for $f$ if, within a neighbourhood $N$ of arbitrary size, we have that $f(a) \le f(x)$ (local minimum) or $f(a) \ge f(x)$ (local maximum) for all $x \in N$.
````

Notice two things about definition {prf:ref}`local_optima`. First is the fact that a point can a local maximum or a local minimum. If it is both at once, we must have that $f(a) = f(x)$ for $x \in N$. The second is that if the neighbourhood can be set as large as the whole set or real numbers, then we can say that these are **global** optima.

Points that are candidates to optimal points share one thing in common: at them, the function changes from increasing to decreasing (for minima; the opposite for maxima). The points at which this change in function value tendency happens are those where $f'(x) = 0$.

````{note}
One way of seeing this is thinking about the first-order Taylor approximation of $f$ at a candidate point $a$. The first-order approximation would be given as
```{math}
J(x) = f(a) + f'(a)(x - a)
```
which is the expression of the tangent line of $f$ at $a$. If $f'(a) =0$, this means that at $a$, $J(x) = f(a)$ for all $x$. In other words, the tangent line is a horizontal line that crosses the y-axis at $f(a)$.
````

Now, suppose we use $f'(x)=0$ as the condition a point $x$ must satisfy to be an optimum and that we identify $a$ as a point for which $f'(a)=0$. How can we know whether this point is a point of maximum or minimum?

Second-order information can provide answer for that. Recall that the second-order information informs us of the rate of change in the increase or decrease rate of a function value. Thus, if the function value went from decreasing to increasing, its rate of value change must be positive; otherwise, it must be negative. Thus, we have that

- if $f'(a) = 0$ and $f''(a) > 0$, then $a$ is a local minimum;
- if $f'(a) = 0$ and $f''(a) < 0$, then $a$ is a local maximum.

There is however one inconclusive case: when both $f'(a) = 0$ and $f''(a) = 0$. This means that at $a$ the curvature of $f$ changes, meaning that we have an **inflexion point**, which is neither a minimum not a maximum.

```{code-cell}
---
mystnb:
  figure:
    name: fig:sine
    caption: |
      Sine function illustrating a minimum, an inflection point and a maximum.
tags: [remove-input]
---
using CairoMakie

fig, ax, plot = lines(-pi:0.1:pi, sin)
scatter!(Point2f[(-pi/2,-1),(0,0),(pi/2,1)], color=Makie.wong_colors()[2])
fig
```

## Taylor approximation

Before we move on, let us finish with a incredibly useful concept that allows us to approximate **any** differentiable function simply by using its derivatives. This is a result of the so-called Taylor's theorem.

````{prf:theorem}
:label: taylors_theorem

Let $f$ be $n$-times differentiable on an open interval containing $x$ and $a$. Then, the Taylor series expansion of $f$ is

```{math}
\begin{align}
  f(x) = & f(a) + f'(a)(x - a) + \frac{1}{2}f''(a)(x - a)^2 + ... \\
         & + \frac{1}{n!}f^{(n)}(x - a)^n + R_{n+1}(x) \\
       = & \sum_{i=0}^n \frac{1}{i!}f^{(i)}(a)(x-a)^i + R_{n+1}(x), 
\end{align}
```
where $R_{n+1}(x)$ represents the residual associated with the $n+1$-order and subsequent terms.
````

The Taylor expansion is exact, once an infinite number of terms are considered. Its practical use however is as an $n^\text{th}$-order  **approximation**, which corresponds to the Taylor expansion to the $n^\text{th}$ order, without the residual term. The figure below illustrates how the Taylor approximation can be used to approximate the function. Notice how well it approximates the function in the vicinity of the point of interest (our $a$) and how it becomes a better approximation as higher orders are considered.

Adapted from [Michael Schlottke-Lakemper's code](https://gist.github.com/sloede/a680cf36245e1794801a6bcd4530487a).

```{code-cell}
using WGLMakie, Bonito
WGLMakie.activate!()

function base_graph(fun)
    fig = Figure(size=(800, 600), fontsize=30)
    ax = Axis(fig[1,1],
              title="Taylor series for sine/cosine",
              xlabel="x",
              ylabel="y",
              xticks=MultiplesTicks(5, pi, "π")
              )
    lines!(ax, -7..7, fun, label="f(x)")

    xlims!(ax, -7, 7)
    ylims!(ax, -5, 5)
    return fig, ax
end

function draw_x0(ax, x0, y)
    scatter!(ax, x0, y, color=:red, markersize=20, label="x₀")
end

function draw_taylor(ax, x, y)
    lines!(ax, x, y, linewidth=3, label="Tₙ(x)")
end

function tcosn(x, n, x0)
  sin_x0, cos_x0 = sincos(x0)
  result = cos_x0
  for i in 1:4:n
    result -= sin_x0 * (x - x0)^i/factorial(i)
  end
  for i in 2:4:n
    result -= cos_x0 * (x - x0)^i/factorial(i)
  end
  for i in 3:4:n
    result += sin_x0 * (x - x0)^i/factorial(i)
  end
  for i in 4:4:n
    result += cos_x0 * (x - x0)^i/factorial(i)
  end
  return result
end

function tsinn(x, n, x0)
  sin_x0, cos_x0 = sincos(x0)
  result = sin_x0
  for i in 1:4:n
    result += cos_x0 * (x - x0)^i/factorial(i)
  end
  for i in 2:4:n
    result -= sin_x0 * (x - x0)^i/factorial(i)
  end
  for i in 3:4:n
    result -= cos_x0 * (x - x0)^i/factorial(i)
  end
  for i in 4:4:n
    result += sin_x0 * (x - x0)^i/factorial(i)
  end
  return result
end

App() do session::Session
    fun = Observable{Any}(sin)
    taylor = Observable{Any}(tsinn)

    dropdown = Dropdown(["Sine", "Cosine"])
    on(dropdown.value) do value
        if value == "Sine"
            fun[] = sin
            taylor[] = tsinn
        else#if value == "Cosine"
            fun[] = cos
            taylor[] = tcosn
        end
    end

    slider_x0 = Bonito.Slider(-7:0.1:7)
    slider_x0[] = 0  # set starting value
    y = @lift($fun($slider_x0))

    slider_deg = Bonito.Slider(1:5)
    xvals = range(-7, 7, 100)
    yvals = @lift($taylor.(xvals, $slider_deg, $slider_x0))
    
    fig, ax = base_graph(fun)
    draw_taylor(ax, xvals, yvals)
    draw_x0(ax, slider_x0.value, y)
    axislegend(ax, position=:rb)

    return Bonito.record_states(session, 
                                DOM.div(
                                    fig, 
                                    DOM.div("Taylor polynomial degrees: ", slider_deg, slider_deg.value),
                                    DOM.div("x₀: ", slider_x0, slider_x0.value),
                                    dropdown
                                    ))
end
```

## Unconstrained optimality conditions

Let us now devise the optimality conditions that a candidate point must satisfy in a more general (i.e., multidimensional) setting. For that, let our function of interest be of the form $f : \mathbb{R}^n \to \mathbb{R}$. As we seen in [Lecture 2](../part1/2-functions_and_optimisation.md), the partial derivatives of $f$ with respect to each of its components $x_i$, $i \in \{1,\dots,n\}$, is 

```{math}
\frac{\partial f(x)}{\partial x_i} = \lim_{ h \to 0}\frac{f(x_1, \dots, x_i+h, \dots, x_n)-f(x_1, \dots, x_n)}{h}.
```

Then, we also seen that the gradient of $f$ at $x$ is defined as

```{math}
\nabla f(x) = \left[\frac{\partial f(x)}{\partial x_1}, \dots, \frac{\partial f(x)}{\partial x_i}, \dots, \frac{\partial f(x)}{\partial x_n} \right].
```

The gradient plays the role of our first-order derivative information for multi-dimensional functions. For second-order derivative information, we rely on the Hessian matrix, which is defined as

```{math}
\nabla^2f(x) = H(x) = 
\begin{bmatrix} 
  \frac{\partial^2 f(x)}{\partial x_1^2} & \dots & \frac{\partial^2 f(x)}{\partial x_1\partial x_n} \\
  \vdots   & \ddots & \vdots \\
  \frac{\partial^2 f(x)}{\partial x_n\partial x_1} & \dots & \frac{\partial^2 f(x)}{\partial x_n^2}
\end{bmatrix}.
```

Analogous to the univariate case, gradients and Hessian describe the function's local growth behaviour and shape (more precisely, curvature), respectively.

One last point worth mentioning relates to second-order Taylor approximations for multivariate functions. Most optimisation techniques will consider second order approximations of the functions being optimised. As such, gradients and Hessian will frequently be mentioned and utilised in our derivations. The second-order approximation of $f$ at $x_0$ is given by

```{math}
f(x) = f(a) + \nabla f(a)^\top (x - a) + \frac{1}{2}(x - a)^\top H(a)(x - a).
```

```{admonition} Note: Second-order expansion of $f$
:class: note

Analogously to the univariate case, the second-order Taylor expansion of $f$ at $a$ is given by

$$
f(x) = f(a) + \nabla f(a)^\top (x - a) + \frac{1}{2}(x - a)^\top H(a)(x - a) + o(\| x - a \|^2)
$$

where the residual $o(\| x - a \|^2)$ is presented in the [little-o notation](https://en.wikipedia.org/wiki/Big_O_notation\#Little-o_notation) which essentially means that the residual goes to zero ``faster'' than $\| x - a \|^2$ and as such, can be safely ignored for small $\Delta x = x -a$.  
```

## Unconstrained optimality conditions

In [Lecture 2](../part1/2-functions_and_optimisation.md), we briefly hinted to the zero-gradient condition as a necessary condition for optimality. Here, we look in further detail why this is the case. To be able to do so, we must define the notion of **descent direction**.

```{prf:definition}
:label: descent_direction

Let $f : \reals^n \to \reals$ be differentiable. The vector $d = (x - x_0)$ is a descent direction for $f$ at $x_0$ if $\nabla f(x_0)^\top d < 0$.
```

Some points are worth highlighting in {prf:ref}`descent_direction`. First, the vector $d$ gives the straight direction that must be followed for one to go from point $x_0$ to point $x$. Also, the sign of the scalar product $\nabla f(x_0)^\top d$ holds a relationship with the angle formed between the vectors $\nabla f(x_0)$ and $d$: a negative value indicates that they form an angle greater than $90^\circ$ whilst a positive value indicate angle of less than $90^\circ$. 

When we say that $d$ is a descent direction, it means that the direction $d$ holds a component in the **opposite** direction of the gradient $\nabla f(x_0)$ and, as such, any movement in that direction from $x_0$ will lead to a point in which the function $f$ value decreases.

Analogously, we can think of ascent directions, which are those for which $\nabla f(x_0)^\top d > 0$. In that case, any movement in the direction of $d$ would increase the function value in relation to $f(x_0)$. 

```{note}
Notice that for every ascent direction $d$ there is an descent direction $-d$.
````

% TODO: include figures from introduction to optimisation showing descent direction. We can consider enriching it to include the eigenvectors scaled by eigenvalues of the Hessian

With the notion of descent direction at hand, it becomes clear that a minimum point is one for which no descent direction can be identified. And, for that to be the case in unconstrained settings, where from $x_0$ we can move towards any point $x \in \reals^n$, this will only be the case when $\nabla f(x) = 0$. For completeness, we state the so called first-order necessary optimality conditions

```{prf:theorem} First-order optimality conditions
:label: first-order-optimality

Let $f : \reals^n \to \reals$ be differentiable. If $\overline{x}$ is a local optimum, then $\nabla f(\overline{x}) = 0$.
```

## Constrained optimality conditions

Constrained problems are, in general, more challenging to solve. In the presence of constraints, first-order conditions for the equivalent unconstrained problem may never be achieved, meaning that we must consider not only objective function shapes but also the feasible set geometry.

% Add figure from introopt showing the optimal point for a nonlinear problem (2nd slide)

We must thus consider an alternative framework for optimality conditions. In that, we must consider both objective function optimality and constraint satisfaction simultaneously. The theoretical framework that allows for analysing constrained optimisation problems from that perspective is know and Lagrangian duality. 

### Equality-constrained problems

Let us develop the analysis ourselves. We start with equality constraint problems of the form

```{math}
\begin{align*}
  \mini z = & f(x) \\
  \st h_i(x) = 0, i \in [l],
\end{align*}
```

where $f: \reals^n \rightarrow \reals$ and $h:\reals^n \rightarrow \reals^l$, all differentiable.

We start by associating with each equality constraint a (Lagrangian) multiplier, $\mu_i$, $i \in [l]$, defining the so-called Lagrangian function

```{math}
L(x,\mu) = f(x) + \sum_{i=1}^l \mu_i h_i(x).
```

With that at hand, we can analyse it under the frame of unconstrainted optimisation again, since $L(x, \mu)$ is effectively an unconstrained function. Notice that the terms $h_i(x)$, for all $i \in [l]$, act as a infeasibility measure in this case which we hope to minimise. Also, notice that no sign constraints are imposed to the multipliers $\mu_i$, $i \in [l]$.

First-order optimality conditions require that $\nabla L(x,\mu) = 0$, which, in turn, leads to

```{math}
\begin{align*}
& \frac{\partial L(x, \mu)}{\partial x} = 0 \Rightarrow \nabla f(x) + \sum_{i=1}^l \mu_i \nabla h_i(x)  = 0\\
& \frac{\partial L(x, \mu)}{\partial \mu_i} = 0 \Rightarrow h_i(x) = 0, i =1,\dots, l.
\end{align*}
```

These conditions tells us the following: that we are looking for a point that satisfy the constraints $h_i(x) = 0$, $\forall i \in [l]$ and that is such that the gradient of the objective function ($\nabla f(x)$) is the opposite of a scaled combination of the gradients of the constraints ($\nabla f(x) = - \sum_{i=1}^l \mu_i \nabla h_i(x)$). Notice that they yield $n + m$ equations with $n + m$ unknowns. Thus, if we can find a solution $(x,\mu)$ to these equations, we have also found a point that satisfy the optimality conditions! Theorem {prf:ref}`thm-eq_const` formally state optimality conditions for constrained problems with equality constraints only.

````{prf:theorem} Optimality conditions - equality-constrained problems
:label: thm-eq_const

Let $P$ be $\mini \braces{f(x) : h(x) = 0}$ with differentiable $f: \reals^n \rightarrow \reals$ and $h:\reals^n \rightarrow \reals^l$. If $\overline{x}$ is optimal for $P$, then $(\overline{x}, \overline{\mu})$ satisfies 

```{math}
\begin{align}
& \frac{\partial L(x, \mu)}{\partial x} = 0 \Rightarrow \nabla f(x) + \sum_{i=1}^l \mu_i \nabla h_i(x) = 0 \\
& \frac{\partial L(x, \mu)}{\partial \mu} = 0 \Rightarrow h(x) = 0.
\end{align}
```

Moreover, if $f$ is convex and $h$ is affine, then these conditions are not only necessary, but also sufficient for optimality of $\overline{x}$.
````

One important thing to notice from {prf:ref}`thm-eq_const` is that, just as it is the case with unconstrained optimisation, convexity can be used to infer global optimality. Otherwise, the conditions stated in {prf:ref}`thm-eq_const` are only necessary: a solution may satisfy these conditions but not be optimal, as they are only necessary but not sufficient otherwise.

Let's see how these can be used in an example. 
Consider the problem 
```{math}
:label: constrained_problem1
\maxi & -2x_1^2 - x_2^2 + x_1x_2 + 8 x_1 + 3 x_2 \\
\st & 3x_1 + x_2 = 10.
```

The Lagrangian function is given by

$$
L(x_1,x_2,\mu) = -2x_1^2 - x_2^2 + x_1x_2 + 8 x_1 + 3 x_2 + \mu(3x_1 + x_2 - 10)
$$

The optimality conditions are given by the following set of equations:

```{math}
\begin{align*}
&\partial \frac{L(x_1,x_2,\mu)}{\partial x_1} = -4x_1 + x_2 + 8 + 3\mu = 0 \\
&\partial \frac{L(x_1,x_2,\mu)}{\partial x_2} = -2x_2 + x_1 + 3 + \mu = 0 \\
&\partial \frac{L(x_1,x_2,\mu)}{\partial \mu} = 3x_1 + x_2 - 10 = 0
\end{align*}
```

Solving this system of equations we obtain the solution $\overline{x} = (2.46, 2.60)$ and $\overline{\mu} = -0.25$. 

```{code-cell}
---
mystnb:
  figure:
    name: fig:constrained_optimum
    caption: |
      Contour and optimum of {eq}`constrained_problem1`.
tags: [remove-input]
---
using LaTeXStrings
CairoMakie.activate!()

f(x) = -2*x[1]^2 - x[2]^2 + x[1]*x[2] + 8x[1] + 3x[2]

# Plotting the contours of the function to be optimised
n = 1000
x = range(-7,stop=14,length=n)
y = range(-10,stop=10,length=n)
z = [f([x[i],y[j]]) for i = 1:n, j = 1:n]

levels = [-150 + 15i for i =2:2:10]
mylevels = [levels; 12; 15; 25]

fig = Figure()
ax = Axis(fig[1,1], limits=(-10,20,-10,10), xlabel=L"x_1", ylabel=L"x_2")
contour!(ax, x,y,z, levels=mylevels, labels=true, colorrange=(-120,20))
ablines!(ax, [10], [-3], label=L"3x_1+x_2=10")
scatter!(ax, Point2f[(69/28,73/28)], label=L"\bar{x}", color=Makie.wong_colors()[2])
axislegend()
fig
```

```{warning} How do we know it is a maximum?
These optimality conditions are a constrained equivalent to first-order conditions. As such, it is up to you to recognise that the objective function is concave and we are maximising, making the problem convex and the conditions from {prf:ref}`thm-eq_const` necessary and sufficient for optimality, in this case the maximum. Notice that if we were minimising instead, this point would satisfy the conditions but would not be optimal (there would be no optimal in fact as the objective function can decrease *ad infinitum*).  
```

### Inequality-constrained problems

Let us now consider inequalities as constraints. That is, our problem now takes the form of 

```{math}
\begin{align*}
(P) : \mini z = & \ f(x) \\
\st & g_i(x) \leq 0, \ i = 1,\dots,m.
\end{align*}
```

We proceed in the same manner as before, adding multipliers $\lambda_i$, $\forall i \in [m]$ to each of the constraints and form the Lagrangian function  

$$L(x, \lambda) = f(x) + \sum_{i=1}^m \lambda_i g_i(x).$$

The difference now is that we require **additional conditions** on how those multipliers behave. Essentially, differently from the equality constraint case, it may be that the constraint is such that $g_i(x) < 0$, meaning that it is not binding and, as such, does not play any role in the optimality conditions of the point $x$. As such, we must make sure that only when $g_i(x) = 0$ (i.e., they are binding) they play are role in the optimality conditions. For these to work as intended, we must impose that $\lambda_i \ge 0$ (as the inequality are satisfied by one of its sides) and that $\lambda_i g_i(x) = 0$, $\forall i \in [m]$. The second condition enforces that in the cases where $g_i(x) < 0$, the constraint plays no role in the optimality conditions.

Putting these all together, we arrive at the following optimality conditions.

```{prf:theorem} Optimality conditions - inequality constrained problems
Let $P$ be $\mini \braces{f(x) : g(x) \leq 0}$ with differentiable $f: \reals^n \rightarrow \reals$ and $g:\reals^n \rightarrow \reals^m$. If $\overline{x}$ is optimal for $P$, then $(\overline{x}, \overline{\lambda})$ satisfies 
\begin{align*}
& \nabla f(\overline{x}) + \sum_{i=1}^m \overline{\lambda}_i \nabla g_i(\overline{x}) = 0 \\
& g(\overline{x}) \leq 0  \\
& \overline{\lambda}_i g_i(\overline{x}) = 0 , \ i = 1,\dots,m \\
& \overline{\lambda}_i \geq 0, \ i = 1,\dots,m.
\end{align*}
```

Once again. Notice that these conditions are only necessary for optimality, but not sufficient. The most general form of these conditions are known as Karush-Kuhn-Tucker (or KKT) conditions, which represent the general optimality conditions for constrained optimisation problems. For completeness, they are stated in {prf:ref}`kkt_conditions`.

```{prf:theorem} Karush-Kuhn-Tucker (KKT) conditions
:label: kkt_conditions

Let $P$ be $\mini \braces{f(x) : g(x) \leq 0, h(x) = 0}$ with differentiable $f: \reals^n \rightarrow \reals$, $g:\reals^n \rightarrow \reals^m$ and $h:\reals^n \rightarrow \reals^l$. If $\overline{x}$ is optimal for $P$, then $(\overline{x}, \overline{\lambda}, \overline{\mu})$ satisfies 
\begin{align*}
& \nabla f(\overline{x}) + \sum_{i=1}^m \overline{\lambda}_i \nabla g_i(\overline{x}) + \sum_{i=1}^l \overline{\mu}_i \nabla h_i(\overline{x})= 0 \\
& g_i(\overline{x}) \leq 0, \ i = 1,\dots,m  \\
& h_i(\overline{x}) = 0, \ i = 1,\dots,l \\
& \overline{\lambda}_i g_i(\overline{x}) = 0, \ i = 1,\dots,m \\
& \overline{\lambda}_i \geq 0, \ i = 1,\dots,m.
\end{align*}
```

For the KKT conditions to be necessary and sufficient, we require that $f$ is convex, $g_i$ is convex, $\forall i \in [m]$ and that there exists at least one $x$ such that $g_i(x) < 0$, $\forall i \in [m]$. This last condition is additional to our previosuly seen convexity requirements. These **constraint qualification** conditions loosely implies that the gradients associated with $g_i(x)$ do not "cancel each other out" and the first condition in {prf:ref}`kkt_conditions` reliably describes an equilibrium point where the optimal point resides.

```{note}
The constraint qualification condition we used is known as **Slater's constraint qualification**. There exists other more general conditions that can be considered instead, for example linear independence constraint qualification (LICQ) and Mangasarian-Fromovitz constraint qualification (MFCQ), which also render the KKT conditions necessary and sufficient for optimality.
```

Let us consider another example: consider the problem
```{math}
:label: constrained_problem2
\mini & (x_1 - 3)^2 + (x_2 - 3)^2 \\
\st & -x_1 + x_2 \leq 4 \\
& 2x_1 + 3x_2 \leq 11
```

The Lagrangian function is given by

$$
L(x_1,x_2,\lambda_1,\lambda_2) = (x_1 - 3)^2 + (x_2 - 3)^2 + \lambda_1(-x_1 + x_2 - 4) + \lambda_2(2x_1 + 3x_2 - 11).
$$

As such, the KKT conditions are:
```{math}
\begin{align*}
&\begin{bmatrix}2x_1 -6 \\ 2x_2 -6
\end{bmatrix} + \lambda_1 \begin{bmatrix} -1 \\ 1
\end{bmatrix} + \lambda_2\begin{bmatrix} 2 \\ 3\end{bmatrix}
= 0 \\ 
&x_1 + x_2 - 2 \leq 0 \\
&2x_1 + 3x_2 - 11 \leq 0 \\
&\lambda_1(x_1 + x_2 - 2) = 0 \\
&\lambda_2(2x_1 + 3x_2 - 11) = 0 \\
&\lambda_1, \lambda_2 \geq 0
\end{align*}
```

Notice that in this case,to solve the KKT conditions, we need to make an assumption on how the complementarity conditions $\lambda_i g_i(x) = 0$, $i \in [m]$, are satisfied. In this case, they imply that one of the following cases must hold:

1. both $\lambda_1 = 0$ and $\lambda_2 = 0$; thus $g_1(x) < 0$ and $g_2(x) < 0$;
2. $\lambda_1 > 0$ and $\lambda_2 = 0$; thus $g_1(x) = 0$  and $g_2(x) < 0$;
3. $\lambda_1 = 0$ and $\lambda_2 > 0$; thus $g_1(x) < 0$  and $g_2(x) = 0$;
4. both $\lambda_1 > 0$ and $\lambda_2 > 0$; thus $g_1(x) = 0$ and $g_2(x) = 0$.

One might need to test all cases to find solutions satisfying the KKT conditions. In this example, $\lambda_1= 0, \lambda_2 > 0$ leads to a (unique optimal) solution satisfying KKT conditions: $(\overline{x}_1,\overline{x}_2,\overline{\lambda}_1,\overline{\lambda}_2) = (2.38, 2.07, 0, 0.61)$.

% Add figure and make once again a comment on the equilibrium part (ex2).
```{code-cell}
---
mystnb:
  figure:
    name: fig:constrained_optimum2
    caption: |
      Contour and optimum of {eq}`constrained_problem2`.
tags: [remove-input]
---

f(x) = (x[1] - 3)^2 + (x[2] - 3)^2 

n = 500
x1 = range(-5,stop=10,length=n)
x2 = range(-5,stop=10,length=n)
z = [f([x1[i],x2[j]]) for j = 1:n, i = 1:n]

fig = Figure()
ax = Axis(fig[1,1], limits=(0,10,0,10), xlabel=L"x_1", ylabel=L"x_2")

contour!(ax, x1,x2,z, levels=[0.1, 1.2307, 6, 15, 28], labels=true, colorrange=(0,35))
ablines!(ax, [2], [1], label=L"-x_1+x_2\leq 2")
ablines!(ax, [11/3], [-2/3], label=L"2x_1+3x_2\leq 11")
scatter!(ax, Point2f[(2.38462,2.07692)], label=L"\bar{x}", color=Makie.wong_colors()[2])
axislegend()
fig
```