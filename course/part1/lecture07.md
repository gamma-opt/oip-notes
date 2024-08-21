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
Our goal is to make a quarterly electricity production plan over a period of a year, so that 3 power plants would produce enough electricity for the consumption of 4 cities.

```{code-cell}
:tags: [remove-output]
using JuMP, HiGHS, DataFrames

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
over_cap_cost = 50    # per terawatt

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
However, if it wasn't, i.e. the number of terawatts produced plus previous inventory didn't exceed demand, the next months inventory would be negative.
This violates the constraint on the variables `i` we set up originally, so the demand constraint is implicit here.

Having specified the model, we can ask `JuMP` to show it to us.

```{code-cell}
:tags: [remove-output]
print(model)
```

```{code-cell}
:tags: [remove-input]

io = IOBuffer()
JuMP._print_latex(io, model)
latex = String(take!(io))
lines = split(latex, "\n")
newlines = []
push!(newlines, lines[1])
push!(newlines, lines[2][begin:133] * "\\\\\n&" * lines[2][134:249] * "\\\\\n&" * lines[2][250:end])
for i in 3:6
    push!(newlines, lines[i])
end
for i in 27:length(lines)-1
    left = lines[i-20][begin:end-2]
    right = lines[i][begin+3:end]
    push!(newlines, left*",\\quad "*right)
end
push!(newlines, lines[end])
latex = join(newlines, "\n")
display("text/latex", latex)
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