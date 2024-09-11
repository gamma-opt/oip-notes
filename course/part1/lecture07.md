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

## Distribution Problem

Finally, we cover the distribution problem presented in {numref}`p1l5:distribution`.

```{code-cell}
:tags: [remove-output]

I = 2 # number of factories
J = 4 # number of depots
K = 6 # number of customers

fac2dep = [0.5 0.5 1.0 0.2;
           missing 0.3 0.5 0.2]
fac2c = [1.0 missing 1.5 2.0 missing 1;
         2.0 missing missing missing missing missing]

dep2c = [missing 1.5 0.5 1.5 missing 1.0;
         1.0 0.5 0.5 1.0 0.5 missing;
         missing 1.5 2.0 missing 0.5 1.5;
         missing missing 0.2 1.5 0.5 1.5]

fac_capacity = [150000, 200000]
dep_throughput = [70000, 50000, 100000, 40000]
demands = [50000 10000 40000 35000 60000 20000]

model = Model(HiGHS.Optimizer)
```

% Remove the solver printed statement
```{code-cell}
:tags: [remove-cell]

set_attribute(model, "output_flag", false)
```

Then we define our variables.
```{code-cell}
:tags: [remove-output]

@variable(model, x[1:I,1:J] >= 0)
@variable(model, y[1:I,1:K] >= 0)
@variable(model, z[1:J,1:K] >= 0)
```

Given the above variables, our objective is to minimize distribution costs.

```{code-cell}
:tags: [remove-output]

@objective(model, Min, 
    sum(coalesce.(fac2dep,0)[i,j]*x[i,j] for i in 1:I, j in 1:J)
    + sum(coalesce.(fac2c,0)[i,k]*y[i,k] for i in 1:I, k in 1:K)
    + sum(coalesce.(dep2c,0)[j,k]*z[j,k] for j in 1:J, k in 1:K)
)
```

There are a few constraints we need to impose on the model.
```{code-cell}
:tags: [remove-output]

# factory capacities are not exceeded
@constraint(model, capacity[i in 1:I], sum(x[i,:]) + sum(y[i,:]) <= fac_capacity[i])

# depot throughput it obeyed
@constraint(model, throughput_in[j in 1:J], sum(x[:,j]) <= dep_throughput[j])
@constraint(model, throughput_out[j in 1:J], sum(z[j,:]) == sum(x[:,j]))

# customer demands met
@constraint(model, demand[k in 1:K], sum(y[:,k]) + sum(z[:,k]) == demands[k])

# unavailable routes
for idx in findall(ismissing, fac2dep)
    @constraint(model, x[idx]==0)
end
for idx in findall(ismissing, fac2c)
    @constraint(model, y[idx]==0)
end
for idx in findall(ismissing, dep2c)
    @constraint(model, z[idx]==0)
end
```

This model is relatively large, so we print it in a dropdown menu.
```{code-cell}
:tags: [hide-output]

print(model)
optimize!(model)
is_solved_and_feasible(model)
```

Great, we have a feasible solution. Let’s see what it entails.
```{code-cell}
println("Objective value: ", objective_value(model))
```

```{code-cell}
label_fac = ["Helsinki", "Jyväskylä"]
label_dep = ["Turku", "Tampere", "Kuopio", "Oulu"]

println("Factory to depots")
a = DataFrame(transpose(value.(x)), label_fac)
display(a)
println("Factory to customers")
b = DataFrame(transpose(value.(y)), label_fac)
display(b)
println("Depot to customers")
c = DataFrame(transpose(value.(z)), label_dep)
display(c)
```