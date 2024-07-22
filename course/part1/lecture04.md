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
For example, a company may have a storage depot, where they can store their product for their future stock.
In an optimization problem formulated to obtain a production schedule for this company, this depot may be encoded as
```{math}
:label: constraint_eq
stored_{t-1} + added_t - removed_t = stored_t
```
where the number of products stored in time period {math}`i` is equal to what was stored in the previous period plus what is added minus what is removed.

```{figure} ../figures/depot.drawio.svg
Continuity in the depot imposed by Equation {eq}`constraint_eq`.
```

Suppose further that the company has a set amount of ingredients available at every time period to make their product, and they need to meet the demands of their customers.
These restrictions could be modelled as
```{math}
used_{it}\leq available_i
```
and
```{math}
produced_{t} \geq demand_t
```

Notice that in the above examples, we have used both _equality_ and _inequality_ constraints.
Different constraints are appropriate for different situations, but they all act to restrict the _search space_ for the optimisation problem.
In this example, we cannot have {math}`used_{it}>available_i` because we cannot use an amount of ingredient larger than what is available to us.
Similarly, if the equality {eq}`constraint_eq` is not satisfied, we may be making up additional products or forgetting some in storage.