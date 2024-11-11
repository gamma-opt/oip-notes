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
mystnb:
    execution_mode: 'inline'
---

# Multi-objective Optimisation

So far in the previous lectures, we have discussed the optimisation of a single objective, whether it was maximizing profit, minimizing costs or some other goal. However, in many situations real-life settings, one needs to make a decisions that consider multiple **conflicting objectives** at once and identify a good trade-off. For example, instead of solely maximizing profits or maximising service levels, one may be interested in maximising profits and service level simultaneously. However, these are often conflicting objectives, as higher service levels typically incur higher costs (more production, larger inventories, etc.) and thus, lower profits.

Multi-objective optimisation is the collection of concepts and methods that allow us to incorporate multiple objective functions in our mathematical optimisation model. These techniques aim at helping exposing and understanding trade-offs between objectives while still working with single-objective reformulations.

To illustrate the concepts related to multi-objective optimisation that are introduced in this lecture, we use a multi-objective knapsack example, adapted from [JuMP tutorials](https://jump.dev/JuMP.jl/stable/tutorials/linear/multi_objective_knapsack).
Our problem is the following

```{math}
\maxi &\sum_{i\in I}p_i x_i \\
& \sum_{i\in I} r_i x_i \\
\st &\sum_{i\in I} w_i x_i \leq c \\
&x_i \in \{0, 1\}\quad \forall i\in I.
```

In words, for a given collection $I$ of items $i\in I$ and a corresponding weight $w_i$, a profit $p_i$, and a desirability rating $r_i$ for each item, and a capacity $c$, our goal is to select a subset of $I$ that maximises both profit and desirability rating without exceeding the capacity.

Note that this is a maximisation problem, thus we adopt the maximisation perspective in this lecture.

The associated data is the following (taken from the [vOptGeneric](https://github.com/vOptSolver/vOptGeneric.jl) package):

```{code-cell}
profit = [77, 94, 71, 63, 96, 82, 85, 75, 72, 91, 99, 63, 84, 87, 79, 94, 90]
rating = [65, 90, 90, 77, 95, 84, 70, 94, 66, 92, 74, 97, 60, 60, 65, 97, 93]
weight = [80, 87, 68, 72, 66, 77, 99, 85, 70, 93, 98, 72, 100, 89, 67, 86, 91]
capacity = 900
N = length(profit)
println("Number of items: $(N)")
```

Let us take a look at the data. We plot each point in terms of the pair $(\text{profit}, \text{rating})$, with the size of the dot representing the items weight.

```{code-cell}
using CairoMakie

f = Figure()
ax = Axis(f[1,1],
    xlabel="Profit", 
    ylabel="Rating"
    )
scatter!(ax, profit, rating, markersize=weight/2)
f
```

Before we can solve this multi-objective problem, we first need to discuss some central concepts in multi-objective optimisation.

## Dominance and Pareto optimality

For a single objective, it is easy to determine if one solution is better than the other: one can simply compare their objective values.
For multi-objective optimisation, this is more difficult: one solution can be better than the other for one of the objectives while the reverse is true for another objective.

The concept of **dominance** is integral to the assessment of solutions in multi-objective problems.

Let $f_i : \reals^n \to \reals$ for $j \in \braces{1,\dots,n}$ be our objective functions of interest.

```{prf:definition} Dominance between solutions
:label: dominance

A solution $x$ **dominates** solution $x'$ if

- $x$ is no worse than $x'$ for all objectives, i.e., $f_i(x) \geq f_i(x') \text{ for all } i \in \braces{1,\dots,n}$, and
- $x$ is strictly better than $x'$ in at least one objective, i.e., $f_i(x) > f_i(x') \text{ for some } i \in \braces{1,\dots,n}$.

$x'$ is **dominated** by $x$ if and only if $x$ dominates $x'$.
```

Let us illustrate the notion of domination considering our knapsack example. For that, consider the following two solutions for the knapsack problem, where represent in orange the items selected in each solution.

```{code-cell}
:tags: ["remove-input"]
sol_a = [1, 2, 3, 5, 6, 8, 10, 11, 15, 16, 17]
sol_b = [1, 2, 3, 4, 5, 6, 8, 10, 11, 15, 16]
sol_a_p = sum(profit[sol_a])
sol_a_d = sum(rating[sol_a])
sol_a_w = sum(weight[sol_a])
sol_b_p = sum(profit[sol_b])
sol_b_d = sum(rating[sol_b])
sol_b_w = sum(weight[sol_b])

f = Figure()
ax1 = Axis(f[1,1], width = 400, height = 300, xlabel="Profit", ylabel="Rating")
ax2 = Axis(f[1,2], width = 400, height = 300, xlabel="Profit", ylabel="Rating")
scatter!(ax1, profit, rating, markersize=weight/2)
scatter!(ax2, profit, rating, markersize=weight/2)
scatter!(ax1, profit[sol_a], rating[sol_a], markersize=weight[sol_a]/2, color=:orange)
scatter!(ax2, profit[sol_b], rating[sol_b], markersize=weight[sol_b]/2, color=:orange)
Label(f[2,1], "Solution A\n $(sol_a)")
Label(f[2,2], "Solution B\n $(sol_a)")
resize_to_layout!(f)
f
```

**Solution A** on the left leads to a profit of {eval}`sol_a_p` and a desirability rating of {eval}`sol_a_d` at total weight {eval}`sol_a_w`.
Whereas **Solution B** has a profit of {eval}`sol_b_p`, rating {eval}`sol_b_d`, and total weight {eval}`sol_b_w`. Both solutions are feasible: each item is selected once and their total weights are under the capacity of {eval}`capacity`. However, Solution A is better than Solution B in both objectives. Thus Solution A **dominates** Solution B and, as such, we confidently prefer it between the two.

We can also visualise this on what is called the objective space_. In that, we can plot each solution (i.e., selected items) considering their objective values as coordinates. In the objective space, we can plot the regions in which other solutions would dominate and be dominated by a given solution. 

For two linear objectives, these are two of the **quadrants** formed by a vertical and a horizontal line that crosses the coordinates, or objective values, of the solution. Which of the quadrants hold the dominated and dominating solutions depends whether the objectives are being minimised or maximised. In the knapsack example, since we want to maximise both objectives, the dominated solutions would be in the lower left quadrant, while the dominating solutions would be in the top right quadrant.

Below we plot the dominating/dominated quadrants for Solution A. Notice that Solution B lies in the quadrant of solutions that are dominated by Solution A.

```{code-cell}
:tags: ["remove-input"]
# to center sol_a
x_ul = 976
y_ul = 956
x_ll = 920
y_ll = 922

f = Figure()
ax = Axis(f[1,1], 
    limits=((x_ll, x_ul), (y_ll, y_ul)),
    xlabel="Profit", 
    ylabel="Rating"
    )
vlines!(ax, [sol_a_p])
hlines!(ax, [sol_a_d])
poly!(Point2f[(sol_a_p, sol_a_d), (sol_a_p, y_ul), (x_ul, y_ul), (x_ul, sol_a_d)]; color=(:lightblue, 0.5))
poly!(Point2f[(sol_a_p, sol_a_d), (sol_a_p, y_ll), (x_ll, y_ll), (x_ll, sol_a_d)]; color=(:lightcoral, 0.5))
scatter!(ax, [sol_a_p], [sol_a_d], label="Solution A", markersize=30)
scatter!(ax, [sol_b_p], [sol_b_d], label="Solution B", markersize=30)
axislegend(position = :lt)
text!(ax, [((sol_a_p+x_ll)/2, (sol_a_d+y_ll)/2)]; text="Dominated by\n Solution A", offset=(-40,-20))
text!(ax, [((sol_a_p+x_ul)/2, (sol_a_d+y_ul)/2)]; text="Dominating\n Solution A", offset=(-40,-20))
f
```

Since dominated solution can be ignored, we is clear that we are interested in the so-called **non-dominated** solutions. Let us first formally define what we mean with the term.

```{prf:definition} Non-dominated/Pareto-optimal solutions
:label: pareto_opt

A solution $x$ is called **non-dominated** or **Pareto-optimal**, if there is no other solution that dominates it. In other words, a point is Pareto-optimal if no other point improves at least one objective without harming the remaining objectives. The set of Pareto-optimal points is called the **Pareto frontier**.
```

The Pareto frontier represents the collection of best solutions for different trade-off preferences and is helpful in evaluating the alternative solutions and how they trade off each of the objectives. It thus becomes important to be able to construct the Pareto frontier, or at the very least find as many Pareto-optimal solutions as possible, in order to enable more informed decision-making.

## Ideal and Nadir points

There are two important reference points in multi-objective optimisation: the ideal (sometimes called utopic) and nadir points. The **ideal point** coordinates are obtained by optimising each objective individually. The nadir point coordinates are somewhat more involved. For that, assume that while calculating the ideal value for each objective $f_i(x)$, $i \in \braces{1,\dots, n}$, we table the values of the other objectives $f_j(x)$, with $j \neq i$. The nadir point coordinates are given by the worst values observed for each objective.

{numref}`tab-ideal_nadir` illustrates the process of obtaining the ideal and nadir coordinates. In the table, $f_i(x_i^*)$ represents the optimal objective value for the optimisation of objective function $f_i(x)$ with $x_i^*$ being its optimal solution. In turn, $f_j(x_i^*)$ represents how the optimal solution $x_i^*$ for objective function $f_i$ performs in terms of the objective $f_j(x)$. Finally, assuming we are maximising, the coordinates of the ideal and nadir points would be given by

- Ideal: main-diagonal values of  {numref}`tab-ideal_nadir` $(f_1(x_1^*), f_2(x_2^*), \dots ,f_n(x_n^*)$.
- Nadir: minimum value in each column in {numref}`tab-ideal_nadir` $(\min_{i\in\braces{1,\dots,n}} f_1(x_i^*), \min_{i\in\braces{1,\dots,n}} f_2(x_i^*), \dots, \min_{i\in\braces{1,\dots,n}} f_n(x_i^*))$. 

```{Table} Objective function values
:name: tab-ideal_nadir

|${\bf f_1(x)}$|${\bf f_2(x)}$| ... |${\bf f_n(x)}$ |
|:------------:|:------------:|:---:|:-------------:|
|$f_1(x_1^*)$  | $f_2(x_1^*)$ | ... | $f_n(x_1^*)$  |
|$f_1(x_2^*)$  | $f_2(x_2^*)$ | ... | $f_n(x_2^*)$  |
|...           |...           | ... | ...           |
|$f_1(x_n^*)$  | $f_2(x_n^*)$ | ... | $f_n(x_n^*)$  | 
```

Notice that the nadir and ideal points provide bounds on the objective function values of each Pareto-optimal solution. In some cases, they can be useful for scaling the objective values, which may help defining relative preferences between objectives.

Below, we have the nadir and ideal points for our knapsack data.
The pareto boundary lies within the rectangle defined by the two points, which we will see later in this lecture.
```{code-cell}
:tags: ["remove-cell"]
using JuMP, HiGHS
function weighted_method_knapsack(lambda)
    m = Model(HiGHS.Optimizer)
    set_silent(m)
    @variable(m, x[1:N], Bin)
    @constraint(m, sum(weight[i] * x[i] for i in 1:N) <= capacity)
    @expression(m, profit_expr, sum(profit[i] * x[i] for i in 1:N))
    @expression(m, rating_expr, sum(rating[i] * x[i] for i in 1:N))
    @objective(m, Max, lambda * profit_expr + (1 - lambda) * rating_expr)

    optimize!(m)
    @assert is_solved_and_feasible(m)
    return [i for i in 1:N if value(x[i]) > 0.9]
end
```

```{code-cell}
:tags: [remove-input]
using LaTeXStrings

sol1 = weighted_method_knapsack(1)
sol2 = weighted_method_knapsack(0)

f = Figure()
ax = Axis(f[1,1], 
#    limits=((x_ll, x_ul), (y_ll, y_ul)),
    xlabel="Profit", 
    ylabel="Rating"
    )

sol_b_d = sum(rating[sol_b])
sol_b_w = sum(weight[sol_b])
scatter!(ax, [sum(profit[sol1]), sum(profit[sol2]), sum(profit[sol1]), sum(profit[sol2])], [sum(rating[sol2]), sum(rating[sol1]), sum(rating[sol1]), sum(rating[sol2])], markersize=30, color = [2,3,1,1], colormap = :tab10, colorrange = (1, 10))
text!(ax, [sum(profit[sol1]), sum(profit[sol2])], [sum(rating[sol2]), sum(rating[sol2])], text=["Ideal", L"\max~f_2"], offset=(-14, -30))
text!(ax, [sum(profit[sol2]), sum(profit[sol1])], [sum(rating[sol1]), sum(rating[sol1])], text=[" Nadir", L"\max~f_1"], offset=(-22, 13))
f
```

## Finding Pareto-optimal points

The question then becomes how to identify solutions that form the Pareto frontiers? The two classical methods of doing so are the **weighted** and the **$\epsilon$-constraint** methods.

```{important}
The notion of domination can be used to state our preference for solutions that dominate others. However, multi-objective problems typically have **multiple non-dominated solutions**. Our job is to be able to expose alternative non-dominated solutions (i.e., the Pareto frontier), but choosing between them require further input from the decision maker.
````

### Weighted Method

The **weighted** method, also known as the weighted-sum method, uses a vector of weights $\lambda$ to turn the multi-objective problem into a single-objective one.

```{math}
\maxi_{x\in\mathcal{X}} \sum^n_{i=1}\lambda_i f_i(x)
```

The weights should be nonnegative and sum to one, and they can be interpreted as preference ratios associated with different objectives.
Thus, every weight specification represents a trade-off, and the corresponding optimization problem can be solved to obtain a Pareto-optimal solution. Then, the weights can be varied, and for each set of weights $\lambda_i$, $i \in \braces{1,\dots,n}$, the optimisation problem returns a solution in the Pareto frontier.

Returning to our knapsack example problem, we may implement this as follows. In the implementation, we have $n = 2$ and $\lambda_1 = 0.7$ and $\lambda_2 = 1 - \lambda_1 = 0.3$. 

```{code-cell}
using JuMP, HiGHS

lambda = 0.7

m = Model(HiGHS.Optimizer)
set_silent(m)
@variable(m, x[1:N], Bin)
@constraint(m, sum(weight[i] * x[i] for i in 1:N) <= capacity)
@expression(m, profit_expr, sum(profit[i] * x[i] for i in 1:N))
@expression(m, rating_expr, sum(rating[i] * x[i] for i in 1:N))
@objective(m, Max, lambda * profit_expr + (1 - lambda) * rating_expr)

optimize!(m)
@assert is_solved_and_feasible(m)
print("Items: ",[i for i in 1:N if value(x[i]) > 0.99])
```

Notice that the solution obtained is our Solution A from before, i.e., it turns out it was Pareto-optimal. We can repeat the above with a different set of weights to try to obtain more points on the Pareto frontier. We say try, because, in principle, we may with a different set of weights still find the same solution.

To make the search systematic, we can wrap the previous code in a function that takes $\lambda$ as input, then

```{code-cell}
sol_c = weighted_method_knapsack(0.4)
print("Items: ", sol_c)
```

Let us plot the solutions on the decision space. Also, we now plot the dominated (in red) and dominating (in blue) solution quadrants for both Solution A and the new Solution C.

```{code-cell}
:tags: ["remove-input"]
sol_c_p = sum(profit[sol_c])
sol_c_d = sum(rating[sol_c])
y_ul = sol_c_d+5
x_ll = sol_c_p-5

f = Figure()
ax = Axis(f[1,1], 
    limits=((x_ll, x_ul), (y_ll, y_ul)),
    xlabel="Profit", 
    ylabel="Rating"
    )
poly!(Point2f[(sol_c_p, sol_c_d), (sol_c_p, y_ul), (x_ul, y_ul), (x_ul, sol_c_d)]; color=(:lightblue, 0.5))
poly!(Point2f[(sol_c_p, sol_c_d), (sol_c_p, y_ll), (x_ll, y_ll), (x_ll, sol_c_d)]; color=(:lightcoral, 0.5))
poly!(Point2f[(sol_a_p, sol_a_d), (sol_a_p, y_ul), (x_ul, y_ul), (x_ul, sol_a_d)]; color=(:lightblue, 0.5))
poly!(Point2f[(sol_a_p, sol_a_d), (sol_a_p, y_ll), (x_ll, y_ll), (x_ll, sol_a_d)]; color=(:lightcoral, 0.5))
scatter!(ax, [sol_a_p], [sol_a_d], label="Solution A", markersize=30)
scatter!(ax, [sol_b_p], [sol_b_d], label="Solution B", markersize=30)
scatter!(ax, [sol_c_p], [sol_c_d], label="Solution C", markersize=30)
text!(ax, [sol_a_p,sol_b_p,sol_c_p], [sol_a_d, sol_b_d, sol_c_d], text=["A","B","C"], offset=(20, -8), fontsize=20)

f
```

We can see that solutions A and C do not dominate each other. Solution C also does not dominate Solution B. Indeed, if we cared only about profits and not about desirability ratings, Solution B would be a better choice than C. However, Solution C is preferred over the other two if we give more weight to ratings, which is exactly what we did by decreasing $\lambda_1$ and increasing $\lambda_2$.

Notice that Solutions A and C, found using the weighted method, are solutions in the Pareto frontier. Moreover, one can continue using the weighted method with different weightings and attempt to recover more of the Pareto frontier.

While very simple conceptually, the weighted method has a number of downsides. First is the problem of picking weights, how should one decide their values? A well-defined preference information may not always be available, especially when the problem is over many objectives.

A related problem is one of representation. In most cases, we would hope to obtain various non-dominated solutions across the Pareto frontier that represents the possible trade-off decisions well. However, the mapping between weights to the solution space is not uniform: there is no guarantee that different weights will expose alternative solutions.

### $\epsilon$-Constraint Method

In the $\epsilon$-constraint method, one of the objective functions is optimised while the remaining objectives are considered as being constrained by user-specified values. For example, we may have the instance

```{math}
:label: constraint_prob

\maxi &f_1(\mathbf{x}) \\
\st &f_2(\mathbf{x})\leq \epsilon_2 \\
&f_3(\mathbf{x})\leq \epsilon_3 \\
&\dots \\
&f_n(\mathbf{x})\leq \epsilon_n \\
&x \in \mathcal{X}
```

where $\epsilon_i$ are the user-specified thresholds for each objective $i \in  \braces{1,\dots,n}$. and $\mathcal{X}$ is the feasible space of the multiobjective problem. The thresholds are typically set as fractions of the the ideal value for objective $i$ or minimal requirements for the value of the non-optimised objectives.

Let us again return to our knapsack example. This time, we will use a package that implements multi-objective methods, including the $\epsilon$-constraint method. For that, we use the package [`MultiObjectiveAlgorithms.jl`](https://jump.dev/JuMP.jl/stable/packages/MultiObjectiveAlgorithms).

```{code-cell}
import MultiObjectiveAlgorithms as MOA
m = Model()
set_silent(m)
@variable(m, x[1:N], Bin)
@constraint(m, sum(weight[i] * x[i] for i in 1:N) <= capacity)
@expression(m, profit_expr, sum(profit[i] * x[i] for i in 1:N))
@expression(m, rating_expr, sum(rating[i] * x[i] for i in 1:N))
@objective(m, Max, [profit_expr, rating_expr])

set_optimizer(m, () -> MOA.Optimizer(HiGHS.Optimizer))
set_attribute(m, MOA.Algorithm(), MOA.EpsilonConstraint())

optimize!(m)
@assert termination_status(m) == OPTIMAL
solution_summary(m)
```

There are two important points to take note here. First, note that the code is almost identical to what we had before. The main difference is that we specify an outer "layer" to the solver calling the multi-objective algorithm (MOA) solver on top of standard mathematical optimisation solver.

Second, the output states that there are 9 results. This is typical with multi-objective solvers: they are engineered to return as many (hopefully all) Pareto optimal solutions as possible. We had already obtained two Pareto-optimal results using the weighted method. However, instead of having to find the right weighting boundaries between different solutions, the $\epsilon$-constraint method gave us 9 Pareto-optimal solutions.

We can access information about individual results with

```{code-cell}
solution_summary(m; result = 7)
```

and the result itself is

```{code-cell}
print("Items: ", [i for i in 1:N if value(x[i]; result = 7) > 0.9])
```

This is our Solution A again, so both methods agree it is on the Pareto frontier. In fact, we can plot all the solutions that were obtained.

```{code-cell}
:tags: ["remove-input"]
N_res = result_count(m)

f = Figure()
ax = Axis(f[1,1],
    xlabel="Profit",
    ylabel="Rating")
scatter!(ax,
    [value(profit_expr; result = i) for i in 1:N_res],
    [value(rating_expr; result = i) for i in 1:N_res];
    )
text!(ax,
    [value(profit_expr; result = i) for i in 1:N_res],
    [value(rating_expr; result = i) for i in 1:N_res];
    text = map(x->x!="7" ? x : x*" (A)",string.(1:N_res))
)
scatter!(ax, [sum(profit[sol1]), sum(profit[sol2])], [sum(rating[sol2]), sum(rating[sol1])], color = [2,3], colormap = :tab10, colorrange = (1, 10))
text!(ax, [sum(profit[sol1])], [sum(rating[sol2])], text="Ideal", offset=(-14, -20))
text!(ax, [sum(profit[sol2])], [sum(rating[sol1])], text=" Nadir", offset=(-22, 5))
f
```

%TODO: add conclusion and point to other methods...
