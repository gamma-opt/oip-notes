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
:tags: [remove-output]

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
:tags: [remove-output]

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

## Combined Production-Transporation Problem

In the transportation problem, we minimized the cost of transmiting electricity according to cities' demands with a set amount of supply.
In the production problem, we minimized the cost of producing electricity enough to satisfy the demand for it, without worrying about transportation costs.
Now we consider a problem where the objective is to minimize the cost, taking into account both the production and the transportation.

Suppose that there are 3 power plants, 4 cities, and a battery where we can store electricity in between quarters.
We need to consider the costs associated with electricity production (let's say it depends on the plant and the quarter), costs for transmission from plants to cities or to the battery, costs for transmission from the battery to the cities, and costs for storing in the battery.
We would like to minimize the total costs, while ensuring that each city's electricity demand is satisfied.

Here are some example costs and demands for this problem.
```{code-cell}
:tags: [remove-output]

# plant x quarter
cost_production = [4 2 7 3;
                   5 8 4 2;
                   3 6 5 8]
# plant x city
cost_transmission_plant2city = [ 8  6 10 9;
                                 9 12 13 7;
                                14  9 15 5]
cost_transmission_plant2battery = [6 4 8]

cost_transmission_battery2city = [4 2 7 5]

cost_storing = 1

demand = [40 60 75 25;
          95 20 45 85;
          60 25 90 30;
          55 40 40 50]

model = Model(HiGHS.Optimizer)
```

% Remove the solver printed statement
```{code-cell}
:tags: [remove-cell]

set_attribute(model, "output_flag", false)
```

We need to decide on how much electricity each plant is producing in each quarter.
Once we have that, we can _spend_ it on towards satisfying city demands or storing in the battery, which are represented here by {math}`p2c` and {math}`p2b`.
By having a {math}`battery` variable, it is easier to keep track of how much electricity is added or used from storage, and finally {math}`b2c` tracks this used amount.
```{code-cell}
:tags: [remove-output]

@variable(model, x[p in 1:3, q in 1:4] >= 0)              # production
@variable(model, p2c[p in 1:3, c in 1:4, q in 1:4] >= 0)  # transmission from plants to cities
@variable(model, p2b[p in 1:3, q in 1:4] >= 0)            # transmission from plants to battery
@variable(model, battery[q in 1:4] >= 0)                  # stored in battery at the end of quarter
@variable(model, b2c[c in 1:4, q in 1:4] >= 0)            # transmission from battery to cities (in q=1 should be 0)
```

Given the above variables, our objective is to minimize all costs, which comes from production, transmission, and storing in the battery.
```{code-cell}
:tags: [remove-output]

@objective(model, Min, 
    sum(cost_production[p,q]*x[p,q] for p in 1:3, q in 1:4) +
    sum(cost_transmission_plant2city[p,c]*sum(p2c[p,c,:]) for p in 1:3, c in 1:4) +
    sum(cost_transmission_plant2battery[p]*sum(p2b[p,:]) for p in 1:3) +
    sum(cost_transmission_battery2city[c]*sum(b2c[c,:]) for c in 1:4) +
    cost_storing*sum(battery)
)
```

There are a few constraints we need to impose on the model.
First is that city demands must be met.
In addition, we need to ensure that our variables make sense, for example that we can only use as much electricity as we produce, and the stored amount of electricity in a quarter depends on how much there were before, how much is added, and how much is used.
```{code-cell}
:tags: [remove-output]

# city demands are satisfied
@constraint(model, c_demand[c in 1:4, q in 1:4], sum(p2c[:,c,q]) + sum(b2c[c,q]) >= demand[c,q])

# production continuity
@constraint(model, c_prod_cont[p in 1:3, q in 1:4], sum(p2c[p,:,q])+p2b[p,q] == x[p,q])

# battery continuity
@constraint(model, c_battery_cont1, sum(p2b[:,1]) - sum(b2c[:,1]) == battery[1])
@constraint(model, c_battery_cont[q in 2:4], battery[q-1] + sum(p2b[:,q]) - sum(b2c[:,q]) == battery[q])
```

Lastly, and optionally, we impose an additional constraint that batteries don't use electricity sent in that quarter, or equivalently, that batteries receive electricity at the end of the quarter.
This may not be strictly necessary to do, but here it prevents electricity from being delivered to cities through plants in the same quarter, which bypasses the proper transmission costs.
```{code-cell}
@constraint(model, c_battery_rule[q in 2:4], sum(b2c[:,q]) <= battery[q-1])
```

This model is relatively large, so we print it in a dropdown menu.
```{code-cell}
:tags: [hide-output]

print(model)
optimize!(model)
```

TODO: Display and discuss results nicely.

```{code-cell}
if is_solved_and_feasible(model)
    println("\nSolved!\n")
    println("Objective value: ", objective_value(model))
    println("x: ", value.(x))
    println("p2c: ", value.(p2c))
    println("p2b: ", value.(p2b))
    println("battery: ", value.(battery))
    println("b2c: ", value.(b2c))
else
    print("couldn't solve")
end
```