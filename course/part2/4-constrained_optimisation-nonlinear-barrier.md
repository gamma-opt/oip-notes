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

# Constrained optimisation: the nonlinear case

We now focus on nonlinear optimisation problems, i.e., problems in which the objective function and or some (or all) the constraints are not linear expressions. 

 Optimisation methods that are suited to constrained nonlinear problems are often categorised into two types:

- **local methods**: employ numerical methods that search for solutions satisfying first-order (i.e, KKT) optimality conditions;
- **global methods** employ a local solvers together with specialised space search methods (e.g., spatial branching that has a similar search strategy to the branch-and-bound method).

The range of existing methods for solving constrained nonlinear problems is quite broad. In general, the main difference between them is what theoretical framework they are based on and how they iterate to satisfy KKT optimality conditions. Often, a progressively improving approximation of the problem is considered instead, and how this is set also differentiate the existing methods.

Local methods are typically more efficient from a computational perspective. This is why convexity is such an important and desired feature. As you may recall from our previous lectures, in the case of convex problems (see [Part 1, Lecture 2](../part1/2-functions_and_optimisation.md) for a definition of a convex problem), these methods that are expected to converge to global optimal solutions.

Global methods, on the other hand, are computationally intensive and require a great deal of techniques to be combined such that the optimality of a given solution can be proven. Although remarkable progress has been made in the recent decades, they are still considerably less reliable in terms of computational performance.

We will focus on a class of methods that has become the method of choice for solving nonlinear optimisation problems, which is generally called barrier (or interior point) methods. These methods combine two key ideas:

- The employent of Newton's method to find solutions to KKT optimality conditions;
- The use of barrier functions to eliminate inequalities.

```{admonition} Interior point method v. barrier method
:class: note
Classically, these methods were called interior point methods as a reference to the fact that the search for optimal solutions remains constrained within the feasible region. However, more recent (and efficient) variants employ features that allow the solution to leave the interior of the feasible region, making the denomination "Barrier methods" more accurate.
```

## Employing Newton's method for equality constrained problems

There is a variant of Newton's method that can be employed to find solutions to systems of nonlinear equations, which is called the **Newton-Raphson** method.

The Newton-Raphson method can be described as follows: let $f : \reals^n \to \reals$, with each equation $f_i$ in the system of equations being diffentiable. We seek $x^*$ that solves the system of equations.

$$ 
f(x) = \begin{bmatrix} f_1(x) \\ \vdots \\ f_n(x) \end{bmatrix} = \begin{bmatrix} 0 \\ \vdots \\ 0 \end{bmatrix}.
$$

For that, we start from a initial guess $x^k$ satisfying $f(x^k) = 0$ and iterate by finding $x^{k+1}$ that solve the linear (or first-order Taylor) approximation of $f$ at $x^k$. Under suitable conditions, doing so repeatedly gives us a sequence of points $\{x^k\}_{k=0, 1, \dots}$ that converges to $x^*$.

Let us makes this description more technically formal. At $x^k$, the first-order approximation of $f(x)$ is 

$$ 
f(x^k + d) = f(x^k) + \nabla f(x^k)^\top d,
$$

where $\nabla f(x^k)$ is given by

$$
\nabla f(x^k) = \begin{bmatrix} \nabla f_1(x^k)^\top \\ \vdots \\ \nabla f_n(x^k)^\top \end{bmatrix}.
$$

```{note}
The matrix $\nabla f(x^k)$ the known as the Jacobian of $f(x)$, and is the first-order equivalent of the Hessian $\nabla^2 f(x^k)$.
```

We want to obtain a vector $d$ such that $f(x^k + d) = 0$. Therefore, $d$ is

$$
f(x^k) + \nabla f(x^k)^\top d = 0 \Rightarrow d = -\nabla f(x^k)^{-1}f(x^k).
$$

{prf:ref}`alg:NR` provides a pseudocode for the Newton-Raphson method.

```{prf:algorithm} Newton-Raphson method
:label: alg:NR
**Inputs** system of equations {math}`f`, initial point {math}`x_0`, convergence criterion `converged`.
1. {math}`k=0`
2. **while** not `converged()`:
    1. {math}`d = -\nabla f(x^k)^{-1}f(x^k)`
    3. {math}`x_{k+1}=x_k + d`
    4. {math}`k=k+1`
3. **return** {math}`x_k`.
```

Let us consider a numerical example. As a convergence criterion, we set that if the Euclidean norm of the vector $d$ is less than $\epsilon = 0.01$, we assume that the algorithm has converged.

Suppose we want to find the solution for $f$ with $x^0 = (1,0,1)$, where

```{math}
f(x) = \begin{bmatrix}f_1(x) \\ f_2(x) \\ f_3(x) \end{bmatrix} = \begin{bmatrix} x_1^2 + x_2^2 + x_3^2 -3 \\ x_1^2 + x_2^2 - x_3 - 1 \\ x_1 + x_2 + x_3 - 3 \end{bmatrix}  
```

In this case, we have that 
```{math}
\nabla f(x)=\begin{bmatrix} 2x_1 & 2x_2 & 2x_3 \\ 2x_1 & 2x_2 & -1 \\ 1 & 1 & 1\end{bmatrix}.
```

The intial vector $d^0$ is 

```{math}
d^0 = -[\nabla f(x^0)]^{-1}f(x^0) = - \begin{bmatrix} 2 & 0 & 2 \\ 2 & 0 & -1 \\ 1 & 1 & 1\end{bmatrix}^{-1}\begin{bmatrix} -1 \\ -1 \\ -1 \end{bmatrix} = \begin{bmatrix} 1/2 \\ 1/2 \\ 0 \end{bmatrix} 
```

Thus $x^1 = x^0 + d^0 = \begin{bmatrix} 3/2 & 1/2 & 1\end{bmatrix}$. As $||x^1 - x^0|| = || d^0 || \approx 0.7$, the method carries on until $|| d^k|| < \epsilon$ $x^* = (1, 1, 1)$ is reached after approx. 20 iterations.

```{code-cell}
---
mystnb:
  figure:
    name: fig:newton_residuals
    caption: |
      The convergence of the above Newton-Raphson example, illustrated by the norm of residuals at every iteration.
tags: [remove-input]
---
using CairoMakie, LinearAlgebra, LaTeXStrings

f(x) = [
    sum(x.^2)-3, 
    x[1]^2+x[2]^2-x[3]-1,
    sum(x)-3
]

df(x) = [
    2x[1] 2x[2] 2x[3];
    2x[1] 2x[2] -1;
     1     1     1
]

x = [1,0,1]
eps = 0.01

fig = Figure()
ax = Axis(fig[1,1], xticks=1:8, xlabel="Iteration", ylabel=L"|| x_i-x_{i-1} ||", ylabelsize=22)

norms = []
while true
    d = - df(x) \ f(x)
    x += d
    push!(norms, LinearAlgebra.norm(d))
    if LinearAlgebra.norm(d) < eps
        break
    end
end

scatter!(ax, 1:8, norms)

fig
```

````{admonition} Types of problems best suited for Newton-Raphson
:class: note 
The bulk of the computational effort in the method is associated with calculating the inverse of the Jacobian in $d = -\nabla f(x^k)^{-1}f(x^k)$. 

If $f$ is **linear**, our problem simplifies to solving the linear system of equations $Ax=b$.
This is a very common task in linear algebra and it can often be achieved more efficiently than first inverting the matrix $f(x^k)=A$, then multiplying with $b$.
These are often encoded in the so-called `solve` functions or `\` (backslash) operators.
In `Julia`, this would be done using 

```{code} julia
d = -∇f(x^k) \ f(x^k)
```

````

## Using Newton's method with equality constraints

One interesting insight is that we can employ {prf:ref}`alg:NR` to find solutions to the systems of equations representing the KKT conditions of (equality) constrained optimisation problems. Assume our problem to be stated in the following form

```{math}
\begin{align*}
\mini \ &f(x) \\
\st   &Ax = b.
\end{align*}
```

```{note}
To make our notation a little easier to follow, we are explicitly assuming that $h(x) = Ax - b$. The method can be adapted for nonlinear constraint functions $h(x)$ using first-order approximations of $h$. Notice that these would yield nonconvex problems. 
```

First, we must consider the second-order approximation of $f$ at $x^k$, with $Ax^k = b$.

$$
f(x^k + \Delta x) = f(x^k) + \nabla f(x^k)^\top \Delta x + \frac{1}{2}\Delta x H(x^k) \Delta x,
$$

where $H(x^k)$ is the Hessian of $f$ at $x^k$ and $\Delta x = x - x^k$.  

The KKT conditions for the second-order approximation problem state that $x^k + \Delta x$ is optimal if exists $\mu$ such that

```{math}
:label: eq:Newton-system
\begin{align}
&\nabla f(x^k) + H(x^k)\Delta x + A^\top\mu = 0 \\
&A(x^k + \Delta x) = b \Rightarrow A\Delta x = 0.
\end{align}
```

For convenience, {eq}`eq:Newton-system` are typically stated in a matrix form known as the Newton system, given by

```{math}
\begin{bmatrix}
H(x^k) & A^\top \\
A & 0
\end{bmatrix}
%
\begin{bmatrix}
\Delta x \\
\mu
\end{bmatrix} = 
%
\begin{bmatrix}
-\nabla f(x^k) \\
0
\end{bmatrix}
```

```{note}
The use of the second-order approximation of $f$ is so that the Hessian is constant and the resulting system is a linear system of equations, which allows us to benefit from known efficient and robust computational linear algebra techniques.
```

Let us once again consider a numerical example. We want to solve $\mini \braces{x_1^ 2 - 2x_1x_2 + 4x_2^ 2 : 0.1x_1 - x_2 = 1}$. Assume we start from $x^0 = (11, 0.1)$.  The Jacobian is given by

$$
\nabla f(x) = \begin{bmatrix} 2x_1 - 2x_2 \\ -2x_1 + 8x_2 \end{bmatrix}; H(x) = \begin{bmatrix} 2 & -2 \\ -2 & 8 \end{bmatrix}; A = [0.1, -1].
$$

and the Newton system is

$$
\begin{bmatrix} H(x^k) & A^\top \\ A & 0 \end{bmatrix} \begin{bmatrix} \Delta x \\ \mu \end{bmatrix} =  \begin{bmatrix} -\nabla f(x^k) \\ 0 \end{bmatrix} = 
\begin{bmatrix} 2 & -2 & 0.1 \\ -2 & 8 & -1 \\ 0.1 & -1 & 0 \end{bmatrix} \begin{bmatrix} \Delta x_1 \\ \Delta x_2 \\ \mu \end{bmatrix} = \begin{bmatrix} -2x_1 + 2x_2 \\ 2x_1 - 8x_2 \\ 0\end{bmatrix}.
$$

For $x^0$, we obtain $d^1 = [\Delta x^1, \mu^1]^\top = [-11.714, -1.171, -7.142]^\top$, making $x^1 = x^0 + [-11.714, -1.171]^\top = [-0.714, -1.071]^\top$.

To test whether $x^1$ is optimal, we can check whether $x_1, \mu^1$ satisfy the KKT conditions in {eq}`eq:Newton-system`. In this case, they do, and thus $x^1$ is the optimal solution.

```{warning}
When making calculations with matrices and vectors, it is important to pay attention to the vectors dimensions and make sure they agree. That is why we are making the point of reminding you that $[...]^\top$ is originally a column vector that we are writing in row format for convenience.
```

## The barrier method

### The barrier function
The element missing in our development is a mechanism to deal with inequality constraints. For that, interior point methods rely on **barrier** functions, which are responsible for representing feasibility conditions. In particular, they act as a proxy of an indicator function for the feasibility. For example, let our problem be of the form

```{math}
\begin{align*}
\mini \ &f(x) \\
\st &g_i(x) \leq 0, \ i \in [m] \\
& Ax = b. 
\end{align*}
```

We would like our indicator function to behave such that whenever the inequality is violated by $x$ (i.e., $g(x)>0$), than it would "shoot to infinity" (remember we are minimising). Otherwise, we would like it to not play any role in the optimisation. Thus, we could reformulate our problem as

```{math}
\begin{align*}
\mini \ & f(x) + \sum_{i=1}^m I(g_i(x)) \\
\st &Ax = b, 
\end{align*}
```

where

```{math}
\begin{equation*}
I(u) = \begin{cases} 0, &\text{if } u \leq 0 \\
                     \infty, &\text{if } u > 0  
       \end{cases}
\end{equation*}.
```



From a numerical standpoint, the indicator function creates problem since it is non-differentiable. As such, many proposals for functions that can act as surrogates have been considered in this setting. The most widely accepted as providing a great trade-off betwee computational suitability while imposing the "barring" effect we seek are **logarithmic barriers**, defined as

$$
\begin{equation*}
\Phi_\rho(u) = -\rho \ln(-u),
\end{equation*}
$$

where $\rho > 0$ sets the accuracy (as referenced against the original indicator function) of the barrier term $\Phi_\rho(u)$. {numref}`fig:log_barrier` illustrates the logarithmic barrier applied to a constraint $u \le 0$. Notice how, as one decreases the value of the parameter $\rho$ from 1, the more closely the logarithmic barrier resembles the indicator function.

```{code-cell}
---
mystnb:
  figure:
    name: fig:log_barrier
    caption: |
      Logarithmic barriers with varying $\rho$.
tags: [remove-input]
---
n = 1000
f(x) = -log(-x)
x = range(-3, stop=-1e-10, length=n)

fig = Figure()
ax = Axis(fig[1,1], limits=(-3, 0.5, -1.5, 2))
lines!(ax, x, f, label = L"\rho = 1")
lines!(ax, x, 0.5*f.(x), label = L"\rho = 0.5")
lines!(ax, x, 0.1*f.(x), label = L"\rho = 0.1")
lines!(ax, [x;0], vcat(zero(x),2), linestyle=:dash, label=L"I(u)")

axislegend(position=:lt)
fig
```


### The barrier problem

The barrier function can be used to recast an optimisation problem in a format that can be solved using the constrained Newton method. First, notice that, in general, our optimisation problem can be cast in the form of

```{math}
\begin{align*}
\mini \ &f(x) \\
\st   &Ax = b \\
&x \ge 0.
\end{align*}
```

It is precisely the nonnegativity conditions that prevent us from being able to use Newton's method to solve it. This can be circumvented posing the equivalent **barrier problem**

```{math}
:label: barrier_problem

\begin{equation}
\begin{aligned}
\mini \ & f(x) - \rho\sum_{i=1}^n\ln(x_i) \\
\st & Ax = b 
\end{aligned}
\end{equation}
```

which remove the inequality constraints $x \ge 0$ and yields a form that is tractable by Newton's method.

```{admonition} Reformulation of linear constraints
:class: note

Inequalities can be trivially converted to equalities by adding nonnegative slack variables, with those slack variables then being added to the vector of decision variables $x$. As such, it turns out that {eq}`barrier_problem` can be derived to a fairly general range of optimisation problems.
```

Let us define some matrix notation, which will help make our overall notation more compact. Recall that $x \in \reals^n$. Let

$$
X = \diag(x) = \begin{bmatrix} x_1 & 0 & \dots & 0 \\ 
0 & x_2 & \dots& 0 \\
& & \ddots & \\
0 & 0 & \dots & x_n \end{bmatrix}
$$

and $e$ be a vector of one's of adequate size. Thus $X^{-1} = \diag\left(\frac{1}{x}\right)$ and $X^{-1}e = \left[\dots \frac{1}{x_i} \dots\right]^\top$.

Let us analyse the KKT conditions of the barrier problem. First, we must recall that we utilise the second order approximation of $f$ at $x^k$

$$
f(x) \approx f(x^k) + \nabla f(x^k)^\top (x-x^k) + \frac{1}{2}^\top H(x^k) (x-x^k),
$$

where, as before, $H(x^k)$ is the Hessian of $f$ at $x^k$. We can then pose the Lagrangian function

$$ 
L(x,\mu) = f(x) - \rho\sum_{i=1}^n\ln(x_i) - \mu^\top(b - Ax),
$$

which when substituted with the approximation becomes

$$ 
L(x,\mu) = \nabla f(x^k)^\top (x-x^k) + \frac{1}{2}^\top H(x^k) (x-x^k) - \rho\sum_{i=1}^n\ln(x_i) - \mu^\top(b - Ax).
$$

This leads to the following KKT (optimality) conditions

```{math}
\begin{align*}
&\frac{\partial L(x, \mu)}{\partial x} = \nabla f(x^k) + H(x^k)(x-x^k) - \rho X^{-1}e - A^\top\mu = 0 \\
&\frac{\partial L(x, \mu)}{\partial \mu} = b - Ax = 0.
\end{align*}
```

We a little algebraic manipulation, we can restate the optimality conditions in a more convenient form. For that, let $z = \rho X^{-1}e$. Then $Xz = \rho e$ or $XZe = \rho e$, with $Z = \diag(z)$. With these, the KKT optimality conditions can be rewritten as

```{math} 
:label: KKT_barrier

\begin{equation}
\begin{aligned}
& A^\top\mu + z = \nabla f(x^k) + H(x^k)(x-x^k)  \\
& Ax = b  \\
& XZe = \rho e. 
\end{aligned}
\end{equation}
```

As before, we assume that we are given a point $x^k$ and we would like to move to a point $x=x^k + \Delta x$ that satisfy the KKT conditions {eq}`KKT_barrier`., which we can obtain by solving the Newton system

```{math}
:label: infNS_barrier

\begin{equation}
\begin{bmatrix}
-H(x^k) & A^\top & I \\
A & 0 & 0 \\
Z^k & 0 & X^k      
\end{bmatrix}
%
\begin{bmatrix}
\Delta x \\
\Delta \mu \\
\Delta z 
\end{bmatrix} 
= -
\begin{bmatrix}
A^\top\mu^k + z^k - \nabla f(x^k) \\
Ax^k - b \\
X^kZ^ke - \rho e.
\end{bmatrix}
\end{equation}
````

Notice that from the optimality conditions {eq}`KKT_barrier` we know that $A^\top\mu^k + z^k = \nabla f(x^k)$ and $Ax^k = b$, which allows us to simplify the Newton system to

```{math}
:label: NS_barrier

\begin{equation}
\begin{bmatrix}
-H(x^k) & A^\top & I \\
A & 0 & 0 \\
Z^k & 0 & X^k      
\end{bmatrix}
%
\begin{bmatrix}
\Delta x \\
\Delta \mu \\
\Delta z 
\end{bmatrix} 
=
\begin{bmatrix}
0 \\
0 \\
-X^kZ^ke + \rho e
\end{bmatrix}.
\end{equation}
```

Let us consider a numerical example. Consider the problem

$$
\mini \braces{f(x) = x_1 + x_2 : 2x_1 + x_2 \geq 8, \ x_1 + 2x_2 \geq 10, \ x_1, x_2 \geq 0}.
$$

First, we must convert the inequalities to equalities by adding slack variables $x_3$ and $x_4$ with negative coefficients (since these are greater-or-equal then constraints). The problem than becomes

$$
\mini \braces{f(x) = x_1 + x_2 : 2x_1 + x_2 - x_3 = 8, \ x_1 + 2x_2 - x_4 = 10, \ x_1, x_2, x_3, x4 \geq 0}.
$$

The matrix $A$ is given by $A = \begin{bmatrix} 2 & 1 & -1 & 0 \\ 1 & 2 & 0 & -1 \end{bmatrix}$. Since $f$ is linear, we do not need to consider its second order approximation and, inf fact, its Hessian is zero. Then, given an initial point $(xˆk, z^k)$ our Newton system is given by

```{math}
\begin{bmatrix}
0 & 0 & 0 & 0 & 2 & 1 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 2 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 & 1 \\
2 & 1 & -1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
1 & 2 & 0 & -1 & 0 & 0 & 0 & 0 & 0 & 0 \\
z_1^k & 0 & 0 & 0 & 0 & 0 & x_1^k & 0 & 0 & 0 \\
0 & z_2^k & 0 & 0 & 0 & 0 & 0 & x_2^k & 0 & 0 \\
0 & 0 & z_3^k & 0 & 0 & 0 & 0 & 0 & x_3^k & 0 \\
0 & 0 & 0 & z_4^k & 0 & 0 & 0 & 0 & 0 & x_4^k 
\end{bmatrix}
\begin{bmatrix}
\Delta x_1 \\
\Delta x_2 \\
\Delta x_3 \\
\Delta x_4 \\
\Delta \mu_1 \\
\Delta \mu_2 \\
\Delta z_1 \\
\Delta z_2 \\
\Delta z_3 \\
\Delta z_4
\end{bmatrix}
= 
 \begin{bmatrix}
0 \\
0 \\
0 \\
0 \\
0 \\
0 \\
- x_1^kz_1^k + \rho \\
- x_2^kz_2^k + \rho \\
- x_3^kz_3^k + \rho \\
- x_4^kz_4^k + \rho \\
\end{bmatrix}
```

```{admonition} Barrier method or interior point method?
:class: note

The format above represents a classic version of the method. Because feasibility conditions were assumed to be satisfied at all iterations, the method was first named as **interior point method**. 

Later, it became known that considering the Newton system {eq}`infNS_barrier` instead, while allowing for infeasible solutions, can lead to a convergent algorithm that has better computational behaviour. This makes the name **barrier method** more appropriate as the points are not anymore necessarily in the interior of the feasible region at all iterations.
```

The final element in the algorithm relates to the coefficient of the barrier term $\rho$. In practice, barrier methods typically start with a larger value of $\rho$ and then at each Newton step, decreases it to guide the solution towards the optimal of the original problem. This is motivated by avoiding numerical issues related to have a steeper barrier function when the method is still far away from points closer to the inflexion of the barrier. Putting this all together, we can stat the pseudocode of the barrier method as follows.

```{prf:algorithm} Barrier method
:label: alg:barrier
**Inputs** feasible solution $(x^k,\mu^k,z^k)$, initial $\rho^k$, $\beta \in (0,1)$, convergence criterion `converged`.
1. {math}`k=0`
2. **while** not `converged()`:
    1. compute $\Delta w^{k+1} = (\Delta x^{k+1}, \Delta \mu^{k+1}, \Delta z^{k+1})$ using {eq}`NS_barrier`
    2. {math}`w_{k+1}=w_k + \Delta w^{k+1}`
    3. {math}`\rho^{k+1} = \beta\rho^k`
    4. {math}`k=k+1`
3. **return** {math}`w_k`.
```

One interesting point to notice is that the barrier method does not solve the KKT conditions for each $\rho$ but instead only take one "Newton step" each time. Still the algorithm can be demonstrated to converge in this regime, while avoiding "wasting" computational operations finding a solution for an approximate problem. Recall that our interest lies on solving the problem for when $\rho$ is close to zero.

```{admonition} Barrier methods for linear problems
:class: tip

It turns out that barrier method works very well for linear problems as well. Indeed, the barrier method has become another standard method used for solving linear problems, and has become the algorithm of choice for solving truly large linear optimisation problems.
```