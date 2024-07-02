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

# Lecture 5

(p1l5:transportation)=
## Transportation Problem

This example is based on Section 7.1 of {cite}`winston2022operations` (The book cites a paper, should I cite that instead, or both?).

Suppose that a power company named Powerco is planning electricity distribution from their three power plants in order to supply the needs of four cities.
Each power plant has a certain amount of power production that can be consumed, and each city has a level of demand that must be met.
In addition, the cost of transmiting power depends both on the power plant origin and the destination city.
These data are given in {numref}`table_powerco`.

```{list-table} Costs of sending 1 million kwh of electricity from plants to cities
:name: table_powerco
:header-rows: 1
:stub-columns: 1
:widths: 25 20 20 20 20 25
:align: "right"

* - From
  - City 1
  - City 2
  - City 3
  - City 4
  - Supply  
    (million kwh)
* - Plant 1
  - €8
  - €6
  - €10
  - €9
  - 35
* - Plant 2
  - €9
  - €12
  - €13
  - €7
  - 50
* - Plant 3
  - €14
  - €9
  - €16
  - €5
  - 40
* - Demand  
    (million kwh)
  - 45
  - 20
  - 30
  - 30
  - 
```

In order to determine the best way to meet the demands of these cities while minimizing costs, Powerco would like us to model this as an LP.

### Solution

```{code-cell}
using JuMP, HiGHS

supply = [35, 50, 40]
demand = [45, 20, 30, 30]
cost = [ 8  6 10 9;
         9 12 13 7;
        14  9 15 5]

model = Model(HiGHS.Optimizer)
```
% Remove the solver printed statement
```{code-cell}
:tags: [remove-cell]

set_attribute(model, "output_flag", false)
```

We start by defining a variable for each decision Powerco must make, that is how much power plant {math}`i` sends to city {math}`j` (for {math}`i=1,2,3` and {math}`j=1,2,3,4`).
This amount cannot be negative, so we also add a constraint for that.
```{code-cell}
@variable(model, x[1:3, 1:4] >= 0);
```

The objective is to minimize the cost of power transmission.
```{code-cell}
@objective(model, Min, sum(cost[i,j]*x[i,j] for i in 1:3, j in 1:4));
```

We need to ensure that each plant can only transmit up to its capacity,
```{code-cell}
@constraint(model, c_supply[i in 1:3], sum(x[i,:]) <= supply[i]);
```
and that each city has its demands met.
```{code-cell}
@constraint(model, c_demand[j in 1:4], sum(x[:,j]) >= demand[j]);
```

With the model specified in `JuMP`, we can print it to see the equations directly.
```{code-cell}
print(model)
```

Now, we solve to see what we get.
```{code-cell}
optimize!(model)
is_solved_and_feasible(model)
```

Great, we have a feasible solution.
Let's see what it entails.
```{code-cell}
println("Objective value: ", objective_value(model))
```

```{code-cell}
using DataFrames
a = DataFrame(value.(x), ["City $(i)" for i in 1:4])
display(a)
```

The minimum transmission cost is €1020, with the above distribution plan.

## Production Planning

TODO: Tweak the problem so that we can obtain more interesting solutions?

Upon our success, Powerco approaches us with another project at a different location.
In this location, we again have 3 plants and 4 cities, however we are asked to make a quarterly electricity production plan for the entire year.
{numref}`table_production_demand` contains the projected demand from each of the 4 cities over next year, all of which must be satisfied exactly.


```{list-table} Projected demand from the cities in terawatts
:name: table_production_demand
:header-rows: 1
:stub-columns: 1

* - 
  - Q1
  - Q2
  - Q3
  - Q4
* - City 1
  - 40
  - 60
  - 75
  - 25
* - City 2
  - 95
  - 20
  - 45
  - 85
* - City 3
  - 60
  - 25
  - 90
  - 30
* - City 4
  - 55
  - 40
  - 40
  - 50
```

{numref}`table_production_cost` contains the expected costs of producing electricity in each of the 3 facilities, taking into account costs that change over the year.

```{list-table} Costs of producing a terawatt of electricity (in thousands)
:name: table_production_cost
:header-rows: 1
:stub-columns: 1

* - 
  - Q1
  - Q2
  - Q3
  - Q4
* - Plant 1
  - €8
  - €6
  - €10
  - €9
* - Plant 2
  - €9
  - €12
  - €13
  - €7
* - Plant 3
  - €14
  - €9
  - €15
  - €5
```

In a given quarter, plant 1 can produce 60 terawatts of electricity with regular-time labor, plant 2 can produce 80, and plant 3 can produce 50.
In addition, each plant can produce more electricity with overtime labor, at an additional cost of €50000 per terawatts.
Lastly, there is a battery inventory shared across plants where any excess electricity can be stored at a cost of €10000 per terawatt.
At the beginning of the first quarter, the inventory contains 50 terawatts.
Both the inventory and all the plans work with whole number units only.

### Solution

```{code-cell}
# city x quarters
demand = [40 60 75 25;
          95 20 45 85;
          60 25 90 30;
          55 40 40 50]  

# plant x quarters
cost = [ 8  6 10 9;
         9 12 13 7;
        14  9 15 5]

prod_cap = [60 80 50] # per quarter
over_cap_cost = 50    # per boat

holding_cost = 10
starting_inventory = 50

model = Model(HiGHS.Optimizer)
```

% Remove the solver printed statement
```{code-cell}
:tags: [remove-cell]

set_attribute(model, "output_flag", false)
```

We start by defining a variable for each decision Powerco must make, that is how many units to produce in a given plant.
These cannot be negative, and there is a cap beyond which production incurs additional costs, so we model before cap and after cap separately.
Since demand must be met exactly, the number of units produced also controls how many of them must be stored, which also gets its own variable.
```{code-cell}
:tags: ["remove-output"]

@variable(model, 0 <= x[f=1:3, q=1:4] <= prod_cap[f])  # n_units produced within cap in facility i quarter j
@variable(model, 0 <= y[f=1:3, q=1:4])                 # n_units produced beyond cap in facility i quarter j
@variable(model, 0 <= i[q=1:4])                        # n_units in inventory at the end of quarter j
```

The objective is to minimize all costs over the year.

```{code-cell}
:tags: ["remove-output"]

@objective(model, Min, sum(x[f,q]*cost[f,q] for f=1:3, q=1:4) 
                     + sum(y[f,q]*(cost[f,q]+over_cap_cost) for f=1:3, q=1:4)
                     + sum(i[q]*holding_cost for q=1:4))
```

We need to ensure that demand is met, and any leftovers are stored in the inventory in a continuous manner, i.e. the inventory of last quarter matches the use next quarter and so on.
The starting inventory is also available in the first month, so it is added separately, since we didn't define `i[0]`.

```{code-cell}
:tags: ["remove-output"]

@constraint(model, inventory1, starting_inventory+sum(x[:,1])+sum(y[:,1])-sum(demand[:,1]) == i[1])
@constraint(model, inventory[q=2:4], i[q-1]+sum(x[:,q])+sum(y[:,q])-sum(demand[:,q]) == i[q])
```

Note that in the above we don't explicitly say that demand is met.
However, if it wasn't, i.e. the number of boats produced plus previous inventory didn't exceed demand, the next months inventory would be negative.
This violates the constraint on the variables `i` we set up originally, so the demand constraint is implicit here.

Having specified the model, we can ask `JuMP` to show it to us.

```{code-cell}
print(model)
```

And we solve it.

```{code-cell}
optimize!(model)
is_solved_and_feasible(model)
```

Great, we have a feasible solution. Let’s see what it entails.

```{code-cell}
println("Objective value: ", objective_value(model))
```

```{code-cell}
println("Production before cap")
a = DataFrame(value.(x), ["Q$(i)" for i=1:4])
display(a)
println("Production after cap")
b = DataFrame(value.(y), ["Q$(i)" for i=1:4])
display(b)
println("Inventory use")
c = DataFrame(reshape(value.(i),1,4), ["Q$(i)" for i=1:4])  # this is a vector, so we convert it to matrix for DataFrame
display(c)
```