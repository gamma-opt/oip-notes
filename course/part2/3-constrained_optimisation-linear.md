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
# Constrained optimisation: the linear case

## Simplex method

The simplex algorithm solves linear problems using a very simple idea.
Suppose that in a linear optimisation problem, we want to maximise an objective function of the form
```{math}
:label: lp_obj_form

a-c_1x_1-\dots-c_nx_n.
```
If we know that all {math}`x_i\geq 0`, then the maximum is achieved by setting all variables to $0$, giving us the optimal value as {math}`a`.
Thus the matter of optimizing becomes a matter of rewriting the linear program in the form of {eq}`lp_obj_form`.

The first step in doing this is to put our problem in the canonical form, where
- inequality constraints are converted to equality constraints by adding non-negative slack variables,
- the linear constraints are written so that the slack variables are left on one side, and
- all variables are constrained to have a lower-bound of zero.

Note that these can be achieved for any linear problem.
Adding slack variables to inequality constraints and rewriting them is simple. 
For the last requirement, we can make new variables to use in substitutions, i.e. $x_i\leq 5$ can be substituted with $y_i\leq 0$ along with the constraint $y_i = x_i - 5$.

To exemplify this process, consider the following LP

```{math}
:label: lp_example
\begin{align*}
\maxi &3x_1+2x_2 \\
\stf &2x_1+x_2\leq 100 \\
&x_1+x_2\leq 80 \\
&x_1\leq 40 \\
&x_1,x_2\geq 0.
\end{align*}
```


```{code-cell}
---
mystnb:
  figure:
    name: fig:lp_feasible
    caption: |
      Feasible region of {eq}`lp_example`.
tags: [remove-input]
---

using CairoMakie, LaTeXStrings

fig = Figure()
ax = Axis(fig[1,1])
hidespines!(ax)
vlines!(ax, 0, ymax=100, color=:black)
hlines!(ax, 0, xmax=100, color=:black)

poly!(ax, Point2f[(0,0), (40,0), (40,20), (20, 60), (0, 80)])

lines!(ax, Point2f[(50, 0), (0, 100)], linewidth=2, label=L"2x_1+x_2\leq 100", color=Makie.wong_colors()[4])
lines!(ax, Point2f[(80, 0), (0, 80)], linewidth=2, label=L"x_1+x_2\leq 80", color=Makie.wong_colors()[2])
vlines!(ax, 40, ymax=100, linewidth=2, label=L"x_1\leq 40", color=Makie.wong_colors()[3])
axislegend()
fig
```

Converting {eq}`lp_example` into canonical form yields

```{math}
:label: lp_canonical

\begin{align*}
\maxi &3x_1+2x_2 \\
\stf &s_1=100-2x_1-x_2 \\
&s_2=80-x_1-x_2 \\
&s_3=40-x_1 \\
&x_1,x_2,s_1,s_2,s_3\geq 0.
\end{align*}
```

In this form, the variables remaining on the left side of the linear constraints are called _basic variables_ and the remaining ones are called _non-basic variables_.
Note that right now all basic variables are the slack variables we defined as a part of our modification, but this will not be the case after one iteration of the algorithm.

The simplex algorithm proceeds by exchanging a basic variable with a non-basic variable.
More specifically, at every iteration, a basic and a non-basic variable are chosen, then the constraint associated with the basic variable is solved for the non-basic variable.
The constraint written this way allows us to substitute the non-basic variable with a new equation, which will ideally get us closer to the goal of rewriting the objective in the easy form of {eq}`lp_obj_form`.

To illustrate this with our example {eq}`lp_canonical`, suppose we pick $s_3$ and $x_1$ as our basic and non-basic variables.
The constraint associated with the former is $s_3=40-x_1$ and solving it for $x_1$ gives us $x_1=40-s_3$.
We substitute this in all occurences of $x_1$ to obtain

```{math}
\begin{align*}
\maxi &3(40-s_3)+2x_2 \\
\stf &s_1=100-2(40-s_3)-x_2 \\
&s_2=80-(40-s_3)-x_2 \\
&x_1=40-s_3 \\
&x_1,x_2,s_1,s_2,s_3\geq 0.
\end{align*}
```

```{math}
:label: lp_it1

\begin{align*}
\maxi &120+2x_2-3s_3 \\
\stf &s_1=20-x_2+2s_3 \\
&s_2=40-x_2+s_3 \\
&x_1=40-s_3 \\
&x_1,x_2,s_1,s_2,s_3\geq 0.
\end{align*}
```

Now, $x_1, s_1$ and $s_2$ are the basic variables.

Both {eq}`lp_canonical` and {eq}`lp_it1` have a solution associated with them.
We can obtain the solution by setting the non-basic variables to $0$ and solving for the remaining variables.
For {eq}`lp_canonical`, this is easy, since the variables we care about are both non-basic and we immediately have the solution as $(x_1,x_2)=(0,0)$ with the objective value $0$.
For {eq}`lp_it1`, doing the same thing gives the solution $(x_1,x_2)=(40,0)$ with the objective value $120$.
This means that we obtained a better solution in one iteration, though since there are still variables with positive coefficients in {eq}`lp_it1`, we don't know if this is the optimal solution.


```{code-cell}
---
mystnb:
  figure:
    name: fig:lp_it1
    caption: |
      The solutions associated with {eq}`lp_canonical` and {eq}`lp_it1`.
tags: [remove-input]
---

scatter!(ax, Point2f[(0,0), (40,0)], markersize=20, color=Makie.wong_colors()[6])
text!(ax, Point2f[(0,0), (40,0)], text=["It 0", "It 1"], offset=(5,5), fontsize=15)
fig
```

This process of solving and substitution is repeated until the objective function contains variables with only negative coefficients, at which point the optimum has been found.
An interesting fact is that this iteration corresponds to moving through the vertices of the feasible region, as illustrated in {numref}`fig:lp_it1`.
It can be proved that if a linear problem has an optimum in the feasible region, then at least one vertex will be an optimum.

The only question remaining is how the basic and non-basic variables to be exchanged are selected.
After all, we gave no reason above to picking $s_1$ and $x_1$ above and one may wonder if any selection is appropriate.
It turns out that this selection process, also called _pivoting_, is the fundamental factor governing the performance of the algorithm.

The first consideration we can make is that for the non-basic variables, we would like to pick one that has a positive coefficient (when we are maximising), as our goal is to get rid of the positive coefficients.
If there are multiple such candidates, a heuristic or random selection may be employed.

For the choosing of the basic variable, notice the state of the constraints (with letting $x_2=0$ since it remains a non-basic variable)
```{math}
&s_1=100-2x_1 \\
&s_2=80-x_1 \\
&s_3=40-x_1 \\
&x_1,x_2,s_1,s_2,s_3\geq 0.
```

Each equality suggests a different value for $x_1$ when the basic variable is exchanged to be non-basic and thus getting value $0$: $50, 80$ and $40$ respectively.
Note that the equalities giving different values is not inconsistent, since these are obtained from slack variables, which don't actually have fixed value.
However, the slack variables are constrained to be non-negative as well, which means two of the three values above are infeasible.
After all, if $x_1=80$ as suggested by the second constraint $s_2=80-x_1$, then the first constraint would become $s_1=100-160=-60$ which is not feasible with $s_1\geq 0$.
Consequently, since the third constraint gives the only feasible value, $s_3$ is selected as the basic variable.

If there are multiple constraints prescribing the same value for the non-basic variable to be switched, then ties can be broken with a heuristic or random selection.

<video width="800" controls muted>
    <source src="../_static/SimplexGiapetto.mp4" type="video/mp4">
</video>

## Branch-and-bound

As great and effective the simplex method is, it cannot directly be used on (mixed-)integer problems. 
Consider the problem
```{math}
:label: bnc_ip
\maxi & 4x_1-x_2 \\
\st & 7x_1-2x_2\leq 14 \\
& x_2 \leq 3 \\
& 2x_1-2x_2 \leq 3 \\
& x_1,x_2\in \integers_+.
```

If we ignore the integrality constraint and apply the simplex method, we obtain an optimum $(x_1,x_2)=(\frac{20}{7},3)$ for an objective value of $\frac{59}{7}$.
This is clearly not a feasible solution to our original problem, $x_1$ is not an integer.
Even so, this result provides an upper-bound for the solution we are looking for, as restoring the integrality will make this problem more constrained, and thus the optimal value can only go down (when maximizing).

```{code-cell}
---
mystnb:
  figure:
    name: fig:ip
    caption: |
      The integer problem {eq}`bnc_ip`. The blue points represent the integer solutions, the dashed lines are constraints added during the branch-and-bound algorithm. The orange star is the optimal solution to the linear relaxation.
tags: [remove-input]
---

fig = Figure()
ax = Axis(fig[1,1], limits=(-0.1,3.1,-0.1,3.1))
hidespines!(ax)
vlines!(ax, 0, ymax=4, color=:black)
hlines!(ax, 0, xmax=4, color=:black)

lines!(ax, Point2f[(10/3.5, 3), (2,0)], linewidth=2, label=L"7x_1-2x_2\leq 14", color=Makie.wong_colors()[4])
hlines!(ax, 3, xmax=4, linewidth=2, label=L"x_2\leq 3", color=Makie.wong_colors()[3])
lines!(ax, Point2f[(4.5, 3), (1.5, 0)], linewidth=2, label=L"2x_1-2x_2\leq 3", color=Makie.wong_colors()[2])

vlines!(ax, 2, ymax=4, linewidth=2, label=L"x_1\leq 2", color=Makie.wong_colors()[6], linestyle=:dash)
hlines!(ax, 1, xmax=4, linewidth=2, label=L"x_2\geq 1", color=Makie.wong_colors()[5], linestyle=:dash)

scatter!(ax, [0,0,0,0,1,1,1,1,2,2,2], [0,1,2,3,0,1,2,3,1,2,3])
scatter!(ax, Point2f[(20/7, 3)], color=Makie.wong_colors()[2], marker=:star5, markersize=20)
fig[1,2] = Legend(fig, ax)
fig
```

Making a problem more general by ignoring or relaxing constraints is called a _relaxation_. 
In this example, the relaxation did not give us a feasible solution with respect to integrality, but we can use it to guide further searches.
The branch-and-bound algorithm does exactly this.

Since $x_1$ is not an integer, we can add a constraint to disallow this solution and rerun the simplex algorithm.
Simply adding $x_1\neq \frac{20}{7}$ however is not ideal, since it is easily imaginable this may give rise to a practically identical optimum $(\frac{20}{7}+\delta, 3)$ where $\delta$ is very small.
Instead, we can eliminate the entire neighborhood of non-integer solutions, and end up with two _subproblems_: one with the constraint $x_1\leq 2$ and another with $x_1\geq 3$.
More generally, upon encountering a non-integer solution, we devise cuts, which allows branching into subproblems that can repeat the same process until an integer solution is found.

```{figure} ../figures/bnc.drawio.svg
:name: bnc_tree

Illustration of the branch-and-bound algorithm on {eq}`bnc_ip`, represented by $P_0$. $P_1$ does not need to be solved because the relaxation has an infeasible set of constraints and $P_4$ is pruned as its objective value is smaller than a known feasible solution in $P_3$.
```

A nice feature of this algorithm is that not every subproblem needs to be solved.
For example, as illustrated in {numref}`bnc_tree`, subproblem $P_1$ can be detected to be infeasible before the optimisation process by inspecting the constraints.
Alternatively, it can be inferred that we don't need to inspect subproblems of $P_4$, since its objective value is smaller than that of $P_3$, which already provides a feasible solution to the integer problem.

```{warning}
While in this example, an integer solution was found quickly, real-world problems can quickly get very complicated.
For example, in a problem with a much larger number of variables, the relaxation may have an optimum with a large number of non-integer variables.
In this scenario, there may be no more efficient way of continuing the search than adding constraints for one variable at a time.
Consequently, the _search tree_ for the problem, as exemplified in {numref}`bnc_tree` will be both very wide and deep.
This is exactly why solving (mixed)-integer problems are often more difficult than linear problems.
```

<video width="800" controls muted>
    <source src="../_static/BNB.mp4" type="video/mp4">
</video>