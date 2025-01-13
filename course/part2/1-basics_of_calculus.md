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
f'(a) = \lim_{ \Delta x \to 0}\frac{f(a + \Delta x )-f(a)}{\Delta}
```
exists for all $x \in \reals$.
````

```{note}
Both definitions are equivalent, though here we consider it without an explicit domain $X$. If you define $\Delta x = x - a$ and you can see they are equivalent.
```

The importance of differentiability is that the derivative provides information regarding the local behaviour of $x$, that is

- if $f'(x) > 0$, the function is **increasing** at $x$. That is, for an arbitrarily small $\epsilon > 0$, $f(x + \epsilon) > f(x)$.
- Likewise, $f'(x) < 0$ means that the function is **decreasing** at $x$.

Another important notion that we wil use is that of $n^\text{th}$-order derivatives. Let us first define it formally.

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

Notice two things about definition {prf:ref}`local_optima`. First is the fact that a point can a local maxima or a local minima. If it is both at once, we must have that $f(a) = f(x)$ for $x \in N$. The second is that if the neighbourhood can be set as large as the whole set or real numbers, then we can say that these are **global** optima.

Points that are candidates to optimal points share one thing in common: at them, the function changes from increasing to decreasing (minimum; the opposite for maximum). The points at which this change in function value tendency happens are those where $f'(x) = 0$.

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

%TODO: plot a function with a maximum a minimum and a inflection point

## Taylor approximation

Before we move on, let us finish with a incredibly useful concept that allows us to approximate **any** differentiable function simply by using its derivatives. This is a result of the so-called Taylor's theorem.

````{prf:theorem}
:label: taylors_theorem

Let $f$ be $n$-times differentiable on an open interval containing $x$ and $a$. Then, the Taylor series expansion of $f$ is

```{math}
\begin{align}
  f(x) = & f(a) + f'(a)(x - a) + \frac{1}{2}f''(a)(x - a)^2 + ... \\
         & + \frac{1}{n!}f^{(n)}(x - a)^n + R_{n+1}(x) \\
         & = \sum_{i=0}^n \frac{1}{i!}f^{(i)}(a)(x-a)^i + R_{n+1}(x), 
\end{align}
```
where $R_{n+1}(x)$ represents the residual associated with the $n+1$-order and subsequent terms.
````

The Taylor expansion is exact, once an infinite number of terms are considered. Its practical use however is as an $n^\text{th}$-order  **approximation**, which corresponds to the Taylor expansion to the $n^\text{th}$ order, without the residual term. The figure below illustrates how the Taylor approximation can be used to approximate the function. Notice how well it approximates the function in the vicinity of the point of interest (our $a$) and how it becomes a better approximation as higher orders are considered.

Adapted from [Michael Schlottke-Lakemper's code](https://gist.github.com/sloede/a680cf36245e1794801a6bcd4530487a).

```{code-cell}
using WGLMakie, Bonito

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

    slider_x0 = Slider(-7:0.1:7)
    slider_x0[] = 0  # set starting value
    y = @lift($fun($slider_x0))

    slider_deg = Slider(1:5)
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

```{note} Second-order expansion of $f$

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

## Constrained optimality conditions: Karush-Kuhn-Tucker

## Interpretations of the KKT conditions