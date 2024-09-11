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

# Lecture 7

In this lecture, we revisit the production and combined problem from [](lecture05.md) and implement them in

## Production Planning

Now, we revisit the example in {numref}`p1l5:production`.
Our goal is to make a factory production plan over a period of six months, so that we maximize profits.

```{code-cell}
:tags: [remove-output]
using JuMP, HiGHS, DataFrames

I = 7 # number of products
J = 6 # number of months
K = 5 # number of machines

profit = [10, 6, 8, 4, 11, 9, 3]

machine_usage = [0.5  0.7  0    0    0.3  0.2 0.5;
                 0.1  0.2  0    0.3  0    0.6 0;
                 0.2  0    0.8  0    0    0   0.6;
                 0.05 0.03 0    0.07 0.1  0   0.08;
                 0    0    0.01 0    0.05 0   0.05]

n_machines = [4, 2, 3, 1, 1]
maintenance = [1 0 0 0 0;
               0 0 2 0 0;
               0 0 0 1 0;
               0 1 0 0 0;
               1 1 0 0 0;
               0 0 1 0 1]

holding_cost = 0.5
market_limits = [500 1000 300 300  800 200 100;
                 600  500 200   0  400 300 150;
                 300  600   0   0  500 400 100;
                 200  300 400 500  200   0 100;
                   0  100 500 100 1000 300   0;
                 500  500 100 300 1100 500  60]
holding_limit = 100
holding_target = 50
days_per_month = 24
shifts_per_day = 2
hours_per_shift = 8

model = Model(HiGHS.Optimizer)
```

% Remove the solver printed statement
```{code-cell}
:tags: [remove-cell]

set_attribute(model, "output_flag", false)
```

We start by defining a variable for each decision we must make, that is how much products we manufacture, hold and sell.
These cannot be negative, and there are upper limits to storing and selling.

```{code-cell}
:tags: ["remove-output"]

@variable(model, 0 <= m[1:I, 1:J])
@variable(model, 0 <= h[1:I, 1:J] <= holding_limit)
@variable(model, 0 <= s[i in 1:I, j in 1:J] <= market_limits[j,i])
```

The objective is to maximize profit after holding costs.

```{code-cell}
:tags: ["remove-output"]

@objective(model, Max, sum(s[i,j]*profit[i] for i in 1:I, j in 1:J) - holding_cost*sum(h))
```

We have a couple of constraints.
First is to meet the target inventory at the end of June.
```{code-cell}
:tags: ["remove-output"]

@constraint(model, holding_jun[i in 1:I], h[i,6] == holding_target)
```

Another is the continuity of the product variables.
```{code-cell}
:tags: ["remove-output"]

@constraint(model, continuity_jan[i in 1:I], m[i,1]-s[i,1]-h[i,1] == 0)
@constraint(model, continuity[i in 1:I, j in 2:J], h[i,j-1]+m[i,j]-s[i,j]-h[i,j] == 0)
```

Lastly, we need constraints about machine usage.
```{code-cell}
:tags: ["remove-output"]

@constraint(model, usage[j in 1:J, k=1:K], sum(machine_usage[k,:].*m[:,j]) <= days_per_month*shifts_per_day*hours_per_shift*(n_machines[k]-maintenance[j,k]))
```

Having specified the model, we can ask `JuMP` to show it to us.

```{code-cell}
:tags: ["hide-output"]
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
println("Manufacturing")
label = ["Product $(i)" for i in 1:I]
a = DataFrame(transpose(value.(m)), label)
display(a)
println("Holding")
b = DataFrame(transpose(value.(h)), label)
display(b)
println("Selling")
c = DataFrame(transpose(value.(s)), label)
display(c)
```

## Combined Problem

Finally, we cover the combined production-transportation problem presented in {numref}`p1l5:combined`.

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