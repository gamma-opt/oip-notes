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

# Multiobjective Optimisation

So far in the previous lectures, we have discussed optimisation of a single objective, whether it was maximizing profit, minimizing costs or some other goal.
In many situations, one needs to make a decision about multiple conflicting considerations and identify a good tradeoff.
For example, instead of maximizing profits given some constraints of costs, one can maximize profits while minimizing costs simultaneously.

To illustrate this lecture, we will use a multi-objective knapsack example, adapted from [JuMP tutorials](https://jump.dev/JuMP.jl/stable/tutorials/linear/multi_objective_knapsack).
Our problem is the following

```{math}
\maxi &\sum_{i\in I}p_i x_i \\
& \sum_{i\in I} r_i x_i \\
\st &\sum_{i\in I} w_i x_i \leq c \\
&x_i \in \{0, 1\}\quad \forall i\in I.
```
In words, for a given collection $I$ of items $i\in I$ and a corresponding weight $w_i$, a profit $p_i$, and a desirability rating $r_i$ for each item, and a capacity $c$, our goal is to select a subset of $I$ that maximizes both profit and desirability without exceeding the capacity.

The associated data is the following (taken from [vOptGeneric](https://github.com/vOptSolver/vOptGeneric.jl)):

```{code-cell}
profit = [77, 94, 71, 63, 96, 82, 85, 75, 72, 91, 99, 63, 84, 87, 79, 94, 90]
desire = [65, 90, 90, 77, 95, 84, 70, 94, 66, 92, 74, 97, 60, 60, 65, 97, 93]
weight = [80, 87, 68, 72, 66, 77, 99, 85, 70, 93, 98, 72, 100, 89, 67, 86, 91]
capacity = 900
N = length(profit)
```

Let's take a look at the data.
```{code-cell}
using CairoMakie

f = Figure()
ax = Axis(f[1,1],
    xlabel="Profit", 
    ylabel="Rating"
    )
scatter!(ax, profit, desire, markersize=weight/2)
f
```

## Dominance and Pareto optimality

For a single objective, it is easy to determine if one solution is better than the other, one can just compare the objective values.
For multi-objective optimisation, this is more difficult: one solution can beat the other for one of the objectives while the reverse is true for the remaining objectives.

% Add illustration: a pareto frontier for some decision like range vs cost of electric vehicle. maybe add a dominated point as well

The concept of _dominance_ is integral to the assesment of solutions in multi-objective problems.

Let $f_1(\mathbf{x}), \dots, f_n(\mathbf{x})$ be our objectives of interest.
```{prf:definition}
:label: dominance

A solution {math}`\mathbf{x}` _dominates_ solution {math}`\mathbf{x'}` if
- {math}`\mathbf{x}` is no worse than {math}`\mathbf{x'}` for all objectives, i.e. $f_i(\mathbf{x})\leq f_i(\mathbf{x'})\text{ for all } i$, and
- {math}`\mathbf{x}` is strictly better than {math}`\mathbf{x'}` in at least one objective, i.e. $f_i(\mathbf{x})< f_i(\mathbf{x'})\text{ for some } i$.

{math}`\mathbf{x'}` is _dominated by_ {math}`\mathbf{x}` if and only if {math}`\mathbf{x}` dominates {math}`\mathbf{x'}`.
```

If we have a solution dominating another, we can discard the latter from our consideration.

Consider the following two solutions.

```{code-cell}
:tags: ["remove-input"]
sol_a = [1, 2, 3, 5, 6, 8, 10, 11, 15, 16, 17]
sol_b = [1, 2, 3, 4, 5, 6, 8, 10, 11, 15, 16]
sol_a_p = sum(profit[sol_a])
sol_a_d = sum(desire[sol_a])
sol_a_w = sum(weight[sol_a])
sol_b_p = sum(profit[sol_b])
sol_b_d = sum(desire[sol_b])
sol_b_w = sum(weight[sol_b])

f = Figure()
ax1 = Axis(f[1,1], width = 400, height = 300)
ax2 = Axis(f[1,2], width = 400, height = 300)
scatter!(ax1, profit, desire, markersize=weight/2)
scatter!(ax2, profit, desire, markersize=weight/2)
scatter!(ax1, profit[sol_a], desire[sol_a], markersize=weight[sol_a]/2, color=:orange)
scatter!(ax2, profit[sol_b], desire[sol_b], markersize=weight[sol_b]/2, color=:orange)
Label(f[2,1], "Solution A\n $(sol_a)")
Label(f[2,2], "Solution B\n $(sol_a)")
resize_to_layout!(f)
f
```
The first solution leads to a profit of {eval}`sol_a_p` and a desirability rating of {eval}`sol_a_d` at weight {eval}`sol_a_w`.
Whereas for the second solution, the profit is {eval}`sol_b_p`, the rating {eval}`sol_b_d`, and the weight {eval}`sol_b_w`.
Both solutions are feasible: they use each item once and their weights are under the capacity of {eval}`capacity`.
However, Solution A is better than Solution B in both objectives.
Thus the former **dominates** the latter, we would not be interested in Solution B when we have access to Solution A.

We can also visualise this on what is called the _decision space_, which plots the solutions (so sets of selected items for the knapsack) according to their objective values.

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


Since dominated solution can be ignored, we are interested in _non-dominated_ solutions.

```{prf:definition}
:label: pareto_opt

A solution {math}`\mathbf{x}` is called _Pareto-optimal_, or _non-dominated_, if there is no other solution that dominates it.
In other words, a point is Pareto-optimal if no other point improves at least one objective (without harming the remaining objectives).

A solution is called _weakly Pareto-optimal_ if no other solution improves all of the objectives.

The set of Pareto-optimal points is called the _Pareto frontier_.
```

% Add pareto frontier illustration

The Pareto frontier represents the collection of best solutions for different tradeoff decisions.
Thus, if one does not know their preferences with respect to the different objectives, the Pareto frontier can be helpful in evaluating the alternatives.
It thus becomes important to identify the Pareto frontier, or at the very least find as many Pareto-optimal solutions as possible, in order to enable more informed decision-making.

The question then becomes how to generate Pareto frontiers efficiently
The two classical methods of doing so are the weighted and the $\epsilon$-constraint methods.

## Weighted Method

The _weighted_ method, also known as the _weighted-sum_ method, uses a vector of weights $\lambda$ to turn the multi-objective problem into a single-objective one.

```{math}
\mini_{x\in\mathcal{X}} \sum^n_{i=1}\lambda_if_i(\mathbf{x})
```

The weights should be nonnegative and sum to one, and they can be interpreted as costs or preferences associated with different objectives.
Thus, every weight specification represents a trade-off, and the corresponding optimization problem can be solved to obtain a Pareto-optimal solution.
Then, the weights can be varied to generate a Pareto frontier.

For our example problem, we may implement this as the following.
```{code-cell}
using JuMP, HiGHS

ratio = 0.7

m = Model(HiGHS.Optimizer)
set_silent(m)
@variable(m, x[1:N], Bin)
@constraint(m, sum(weight[i] * x[i] for i in 1:N) <= capacity)
@expression(m, profit_expr, sum(profit[i] * x[i] for i in 1:N))
@expression(m, desire_expr, sum(desire[i] * x[i] for i in 1:N))
@objective(m, Max, ratio*profit_expr+(1-ratio)*desire_expr)

optimize!(m)
@assert is_solved_and_feasible(m)
print("Items: ",[i for i in 1:N if value(x[i]) > 0.9])
```

Huh, this is actually our Solution A from before, turns out it is Pareto-optimal.
We can repeat the above with a different ratio to try to obtain more points on the Pareto frontier.
Suppose that we have wrapped the previous code in a function that takes `ratio` as input, then
```{code-cell}
:tags: ["remove-cell"]
function weighted_method_knapsack(ratio)
    m = Model(HiGHS.Optimizer)
    set_silent(m)
    @variable(m, x[1:N], Bin)
    @constraint(m, sum(weight[i] * x[i] for i in 1:N) <= capacity)
    @expression(m, profit_expr, sum(profit[i] * x[i] for i in 1:N))
    @expression(m, desire_expr, sum(desire[i] * x[i] for i in 1:N))
    @objective(m, Max, ratio*profit_expr+(1-ratio)*desire_expr)

    optimize!(m)
    @assert is_solved_and_feasible(m)
    return [i for i in 1:N if value(x[i]) > 0.9]
end
```

```{code-cell}
sol_c = weighted_method_knapsack(0.4)
print("Items: ", sol_c)
```

Let's plot the solutions on the decision space.
```{code-cell}
:tags: ["remove-input"]
sol_c_p = sum(profit[sol_c])
sol_c_d = sum(desire[sol_c])
y_ul = sol_c_d+5
x_ll = sol_c_p-5

f = Figure()
ax = Axis(f[1,1], 
    limits=((x_ll, x_ul), (y_ll, y_ul)),
    xlabel="Profit", 
    ylabel="Rating"
    )
poly!(Point2f[(sol_a_p, sol_a_d), (sol_a_p, y_ul), (x_ul, y_ul), (x_ul, sol_a_d)]; color=(:lightblue, 0.5))
poly!(Point2f[(sol_a_p, sol_a_d), (sol_a_p, y_ll), (x_ll, y_ll), (x_ll, sol_a_d)]; color=(:lightcoral, 0.5))
scatter!(ax, [sol_a_p], [sol_a_d], label="Solution A", markersize=30)
scatter!(ax, [sol_b_p], [sol_b_d], label="Solution B", markersize=30)
scatter!(ax, [sol_c_p], [sol_c_d], label="Solution C", markersize=30)

axislegend(position = :rt)
f
```

We can see that solutions A and C don't dominate each other.
In fact, Solution C doesn't even dominate Solution B, if we cared only about profits and not about desirability ratings, Solution B would be a better choice than C.
However, Solution C shines over the other two when we start giving more weight to ratings, which is exactly what we did when obtaining it via the weighted method.

One can continue using the weighted method with different weightings and attempt to recover more of the Pareto frontier.

While very simple conceptually, the weighted method has a number of downsides.
First is the problem of picking weights, how should one decide their values?
A well-defined preference information may not always be available, especially when the problem is over many objectives.
A related problem is one of representation.
In most cases, we would hope to obtain various non-dominated solutions across the Pareto frontier that represents the possible trade-off decisions well.
However, the mapping between weights to the solution space is not uniform: there is no guarantee that wildly different weights won't end up with the same solutions, and similarly almost identical weights may result in very different solutions.

% Add point/illustration about not being able to recover solutions on non-convex Pareto fronts

## $\epsilon$-Constraint Method

In the constraint method, one of the objective functions is optimized while the rest are constrained within user-specified values.
For example, we may have the instance
```{math}
:label: constraint_prob
\mini &f_1(\mathbf{x}) \\
\st &f_2(\mathbf{x})\leq \epsilon_2 \\
&f_3(\mathbf{x})\leq \epsilon_3 \\
&\dots \\
&f_n(\mathbf{x})\leq \epsilon_n \\
&x \in \mathcal{X}
```
where $\epsilon_i$ are the user-specified constraints and $\mathcal{X}$ is the feasible space of the multiobjective problem.

It can be shown that for every $\lambda$ and a problem like {eq}`constraint_prob`, the solution to the problem gives a weakly Pareto-optimal solution to the multiobjective problem.
However, if the problem {eq}`constraint_prob` has a unique solution, then it is a Pareto-optimal solution for the multiobjective problem.
The Pareto frontier can be generated by changing $\lambda$ and repeatedly solving the resulting problems.

For the knapsack example, we can use this method via the [`MultiObjectiveAlgorithms.jl`](https://jump.dev/JuMP.jl/stable/packages/MultiObjectiveAlgorithms) package.

```{code-cell}
import MultiObjectiveAlgorithms as MOA
m = Model()
set_silent(m)
@variable(m, x[1:N], Bin)
@constraint(m, sum(weight[i] * x[i] for i in 1:N) <= capacity)
@expression(m, profit_expr, sum(profit[i] * x[i] for i in 1:N))
@expression(m, desire_expr, sum(desire[i] * x[i] for i in 1:N))
@objective(m, Max, [profit_expr, desire_expr])

set_optimizer(m, () -> MOA.Optimizer(HiGHS.Optimizer))
set_attribute(m, MOA.Algorithm(), MOA.EpsilonConstraint())

optimize!(m)
@assert termination_status(m) == OPTIMAL
solution_summary(m)
```

There are two important points to take note here.
First, note that the code is almost identical to what we had before.
Whereas for the weighting method we manually converted the optimisation problem into a singleobjective one, here we just added two lines to use the `MultiObjectiveAlgorithms.jl` package.

Second, the output states that there are 9 results.
This should not be surprising, we already obtained two Pareto-optimal results using the weighted method.
However, instead of having to find the right weighting boundaries between different solutions, the $\epsilon$-constraint method immediately gave us 9 results.

We can access information about individual results with
```{code-cell}
solution_summary(m; result = 7)
```
and the result itself is
```{code-cell}
print("Items: ", [i for i in 1:N if value(x[i]; result = 7) > 0.9])
```

This is our Solution A again, so both methods agree it is on the Pareto frontier.
In fact, let's plot all the solutions we just obtained.

```{code-cell}
:tags: ["remove-input"]
N_res = result_count(m)

f = Figure()
ax = Axis(f[1,1],
    xlabel="Profit",
    ylabel="Rating")
scatter!(ax,
    [value(profit_expr; result = i) for i in 1:N_res],
    [value(desire_expr; result = i) for i in 1:N_res];
    )
text!(ax,
    [value(profit_expr; result = i) for i in 1:N_res],
    [value(desire_expr; result = i) for i in 1:N_res];
    text = string.(1:N_res)
)
f
```

## Other methods

Both of the above methods work by effectively transforming the multiobjective problem into a singleobjective one.
However alternative approaches like goal programming and interactive methods exist.
We will not cover them in this course.
