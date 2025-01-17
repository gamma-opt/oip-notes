# Constrained optimisation: the nonlinear case

We now focus on nonlinear optimisation problems, i.e., problems in which the objective function and or some (or all) the constraints are not linear expressions. 

 Optimisation methods that are suited to constrained nonlinear problems are often categorised into two types:

- **local methods**: employ numerical methods that search for solutions satisfying first-order (i.e, KKT) optimality conditions;
- **global methods** employ a local solvers together with specialised space search methods (e.g., spatial branching that has a similar search strategy to the branch-and-bound method).

The range of existing methods for solving constrained nonlinear problems is quite broad. In general, the main difference between them is what theoretical framework they are based on and how they iterate to satisfy KKT optimality conditions. Often, a progressively improving approximation of the problem is considered instead, and how this is set also differentiate the existing methods.

Local methods are typically more efficient from a computational perspective. This is why convexity is such an important and desired feature. As you may recall from our previous lectures, in the case of convex problems (see [Part 1, Lecture 2](2-functions_and_optimisation.md) for a definition of a convex problem), these methods that are expected to converge to global optimal solutions.

Global methods, on the other hand, are computationally intensive and require a great deal of techniques to be combined such that the optimality of a given solution can be proven. Although remarkable progress has been made in the recent decades, they are still considerably less reliable in terms of computational performance.

We will focus on a class of methods that has become the method of choice for solving nonlinear optimisation problems, which is generally called barrier (or interior point) methods. These methods combine two key ideas:

- The employent of Newton's method to find solutions to KKT optimality conditions;
- The use of barrier functions to eliminate inequalities.

```{note} Interior point method v. barrier method
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
The matrix $\nabla f(x^k)$ the known as the Jacobian of $f(x)$, and isthe first-order equivalent of the Hessian $\nabla^2 f(x^k)$.
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

%TODO: could we do the above via code, somehow?

## Using Newton's method with equality constraints






## Barriers


## The barrier method

## The constrained Newton method for the barrier problem: IPM