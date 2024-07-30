# Lecture 10

So far in the previous lectures, we have discussed optimisation of a single objective, whether it was maximizing profit, minimizing costs or something else.
In many situations, one needs to make a decision about multiple considerations and identify a good tradeoff.
For example, a machine may be designed to maximize performance while minimizing fuel costs.

## Dominance and Pareto optimality

For a single objective, it is easy to determine if one solution is better than the other, one can just compare the objective values.
For multi-objective optimisation, this is more difficult: one solution can beat the other for one of the objectives while the reverse is true for the remaining objectives.

The concept of _dominance_ is integral to the assesment of solutions in multi-objective problems.

```{prf:definition}
:label: dominance

A solution {math}`\mathbf{x}` _dominates_ solution {math}`\mathbf{x'}` if
- {math}`\mathbf{x}` is no worse than {math}`\mathbf{x'}` for all objectives, and
- {math}`\mathbf{x}` is strictly better than {math}`\mathbf{x'}` in at least one objective.

{math}`\mathbf{x'}` is _dominated by_ {math}`\mathbf{x}` if and only if {math}`\mathbf{x}` dominates {math}`\mathbf{x'}`.
```

If we have a solution dominating another, we can discard the latter from our consideration.

```{prf:definition}
:label: pareto_opt

A solution {math}`\mathbf{x}` is called _Pareto optimal_ if there is no other solution that dominates it.
The set of Pareto optimal points if claled the _Pareto frontier_.
```

The Pareto frontier represents the collection of best solutions for different tradeoff decisions.
Thus, if one does not know their preferences with respect to the different objectives, the Pareto frontier can be helpful in evaluating the alternatives.
For a known set of preferences however, this may not always be necessary and one may optimize for that preference specifically, as in [](#p1l10:weight).

## Constraint Method

In the constraint method, one of the objective functions is optimized while the rest are constrained.
For feasible constraints, this results in a (weakly?) Pareto optimal solution.
This can then be repeated for different constraints to generate a Pareto frontier.

(p1l10:weight)=
## Weight Method
