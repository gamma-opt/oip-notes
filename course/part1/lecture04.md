# Lecture 4

## Optimisation modelling
- Explain how functions can represent real-world interactions between inputs and outputs

## Objective functions
- Illustrate that functions can represent costs, revenue, profit, performance
- Objective functions are functions with a "mission": maximise or minimise

The objective function is the function that describes our objective, which is to maximise or minimise some quantity.
Examples include maximizing profits, utility, return on investment, or satisfaction, and minimize costs, redundancy, waste, or risk.

## Defining constraints
- Show that functions can be also be used to state logical relations of the problem we are modelling
- The relation can be =, >=, or <=
- Show that they generate a set that can be used as a subdomain

A factory cannot produce an infinite quantity of product, even if their goal is to maximize production, or a firm often cannot have 0 costs.
Most if not all optimisation problems involve optimising an objective with respect to _constraints_, which specify the restrictions that must be obeyed.
For example, a firm may need to meet the demands of their customers exactly, and would like to minimize costs while doing so.
Similarly, a factory may want to maximize the quantity of blended products produced, using a set amount of available ingredients.

Let us make these examples more specific.
For the first one, suppose that the costs of the firm is equal to the amount of services rendered {math}`x` times unit cost {math}`c`.
The firm must meet the total demand of services requested by their customers, which we call {math}`D`.
We can write this problem as
TODO: Replace with actual example
```{math}
\mini cx \\
\st x=D
```

In the second example, suppose the factory uses two ingredients, and have {math}`s_1` and {math}`s_2` stored, ready to be used.
If the blended product uses both ingredients in equal quantity, we can write this problem as
```{math}
\maxi x_1+x_2 \\
\st x_1\leq s_1 \\
x_2\leq s_2
```

Notice that in the above examples, we have used both _equality_ and _inequality_ constraints.
Different constraints are appropriate for different situations, but they all act to restrict the _search space_ for the optimisation problem.
In the blended product example, we cannot have a solution with {math}`x_1>s_1`, because that would violate the constraints, so it must be that {math}`x_1\leq s_1`.