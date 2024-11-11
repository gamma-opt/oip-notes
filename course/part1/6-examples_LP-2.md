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

# Mathematical programming models: more examples

In this lecture, we revisit more of our previous examples and implement them with the objective of exercising the process of modelling and implementing optimisation models. Our objective with this is to create familiarity with mathematical programming modelling while introducing problems whose structure frequently appears in practice.

(p1l6:production)=
## Production Planning

Now, we revisit the example in {numref}`p1l5:production`. Our goal is to make a factory production plan over a period of six months, so that we maximize profits. In {numref}`production_variables`, the relevant symbols are defined, where the indexing sets are

- $I$ - set of products,
- $J$ - set of months, and
- $K$ - set of machine types.

```{table} Variables in the Production Planning problem
:name: production_variables
| **Symbol** |                                   **Value**                                   |   **Variable name**  |
|:----------:|:-----------------------------------------------------------------------------:|:--------------------:|
|  $m_{ij}$  |                Amount of product $i$ manufactured in month $j$                |       `m[i,j]`       |
|  $h_{ij}$  |               Amount of product $i$ held in storage in month $j$              |       `h[i,j]`       |
|  $s_{ij}$  |                    Amount of product $i$ sold in month $j$                    |       `s[i,j]`       |
|    $P_i$   |                      Profit made from selling product $i$                     |      `profit[i]`     |
|  $U_{ki}$  |    Usage of machines of type $k$ required to produce a unit of product $i$    | `machine_usage[k,i]` |
|    $N_k$   |                    Number of machines of type $k$ available                   |    `n_machines[k]`   |
| $M_{jk}$   | Number of machines of type $k$ that is scheduled for maintenance in month $j$ | `maintenance[j,k]`   |
| $C_H$      | Cost of holding a product                                                     | `holding_cost`       |
| $L_{j,i}$  | Market limits of selling product $i$ in month $j$                             | `market_limits[j,i]` |
| $L_H$      | Holding limit per product                                                     | `holding_limit`      |
| $T_H$      | Holding target per product at the end of June                                 | `holding_target`     |
```

```{note}
Note the symbols and the (code) variable names in the above table. In writing mathematical models, it is often desirable to keep equations shorter and neater by using symbols. However, When it comes to writing code, there is a great deal of value in using **informative** variable names, especially in terms of readability and interpretability of the model in code form.
```

```{attention}
We adopt the convention of using **capital letters** for symbols referring to **parameters** and **lowercase** letters for symbol representing **decision variables**. In the code, we use the original symbol to represent decision variables and descriptive names to represent parameters. This are personal choices, with no convention firmly established. 
```

Given the definitions in {numref}`production_variables`, the statement of the symbolic formulation for the example in {numref}`p1l5:production` is given by

```{math}
\maxi & \sum_{i,j} P_i s_{ij} - \sum_{i,j} C_H h_{ij} \\
\st & s_{i,j} \leq L_{j,i}, \forall i\in I, j \in J \\
& \sum_i U_{ki} m_{ij} \leq 384*(N_k - M_{jk}), \forall k\in K, j\in J \\
& m_{i1} - s_{i1} - h_{i1} = 0, \forall i\in I \\
& h_{i(j-1)} + m_{ij} - s_{ij} - h_{ij} = 0, \forall i \in I, j \in J\setminus\{1\} \\
& h_{i6} = T_H, \forall i \in I \\
& h_{ij} \leq L_H, \forall i\in I, j\in J \\
& m_{ij} \geq 0, \forall i\in I, j\in J \\
& h_{ij} \geq 0, \forall i\in I, j\in J \\
& s_{ij} \geq 0, \forall i\in I, j\in J.
```

Now, we implement the above model using Julia and `JuMP`.

```{code-cell}
:tags: [remove-output]
using JuMP, HiGHS, DataFrames

I = 7 # number of products
J = 6 # number of months
K = 5 # number of machine types

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

The objective is to maximise profit whilst minimising holding costs.

```{code-cell}
:tags: ["remove-output"]

@objective(model, Max, sum(s[i,j]*profit[i] for i in 1:I, j in 1:J) - holding_cost*sum(h))
```

We have a couple of constraints that must be implemented. The first represents meeting the target inventory at the end of June (period 6).

```{code-cell}
:tags: ["remove-output"]

@constraint(model, holding_jun[i in 1:I], h[i,6] == holding_target)
```

The next one states the conservation of inventory between periods, that is that the amount manufactured plus in period $j$ the amount in stock from the previous period $j-1$ must be equal to the amount sold plus the amount of products that remain in stock in period $j$. Notice that for January ($j=1$) we need a specific constraint as the variable`h[i,0]` is not defined.

```{code-cell}
:tags: ["remove-output"]

@constraint(model, continuity_jan[i in 1:I], m[i,1]-s[i,1]-h[i,1] == 0)
@constraint(model, continuity[i in 1:I, j in 2:J], h[i,j-1]+m[i,j]-s[i,j]-h[i,j] == 0)
```

Lastly, we need constraints correctly limiting machine usage.

```{code-cell}
:tags: ["remove-output"]

@constraint(model, usage[j in 1:J, k=1:K], sum(machine_usage[k,:].*m[:,j]) <= days_per_month*shifts_per_day*hours_per_shift*(n_machines[k]-maintenance[j,k]))
```

Having specified the model, we can ask `JuMP` to show it to us.

```{code-cell}
:tags: ["hide-output"]
print(model)
```

Finally, we solve the model.

```{code-cell}
optimize!(model)
is_solved_and_feasible(model)
```

Once the optimisation has found an optimal solution, we can analyse it.

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

Next, we present the implementation of the (symbolic) mathematical programming model for the distribution problem presented in {numref}`p1l5:distribution`.The index sets are

- $I$ - set of factories
- $J$ - set of depots
- $K$ - set of customers.

In {numref}`distribution_variables` we present the list of parameters and variables used in the model.

```{table} Variables in the Distribution problem
:name: distribution_variables
| **Symbol** |                    **Value**                   |  **Variable name**  |
|:----------:|:----------------------------------------------:|:-------------------:|
|  $x_{ij}$  | Amount delivered from factory $i$ to depot $j$ |       `x[i,j]`      |
|  $y_{ik}$  |  Amount delivered from factory $i$ to city $k$ |       `y[i,k]`      |
|  $z_{jk}$  |   Amount delivered from depot $j$ to city $k$  |       `z[j,k]`      |
| $f2d_{ij}$ | Cost of delivery from factory $i$ to depot $j$ |    `fac2dep[i,j]`   |
| $f2c_{ik}$ |  Cost of delivery from factory $i$ to city $k$ |     `fac2c[i,k]`    |
| $d2c_{jk}$ |   Cost of delivery from depot $j$ to city $k$  |     `dep2c[j,k]`    |
| $C_{i}$    | Supply capacity of factory $i$                 | `fac_capacity[i]`   |
| $T_{j}$    | Throughput of depot $j$                        | `dep_throughput[j]` |
| $D_{k}$    | Demand of city $k$                             | `demands[k]`        |
```

The model formulation is given by

```{math}
\mini & \sum_{i,j, f2d_{ij}\neq 0} f2d_{ij}x_{ij} + \sum_{i,k, f2c_{ik}\neq 0} f2c_{ik}y_{ik} + \sum_{j,k, d2c_{jk}\neq 0} d2c_{jk}z_{jk} \\
\st & \sum_{j} x_{ij} + \sum_{k} x_{ik} \leq C_i, \forall i \in I \\
& \sum_{i} x_{ij} \leq T_j, \forall j \in J\\
& \sum_{k} z_{jk} = \sum_{i} x_{ij}, \forall j \in J \\
& \sum_{i} y_{ik} + \sum_{j} z_{jk} = D_k, \forall k \in K \\
& x_{ij} = 0, \forall i \in I, j \in J, \text{ if }f2d_{ij} \text{ is impossible} \\
& y_{ik} = 0, \forall i \in I, k \in K, \text{ if }f2c_{ik} \text{ is impossible} \\
& z_{jk} = 0, \forall j \in J, k \in K, \text{ if }d2c_{jk} \text{ is impossible} \\
& x_{ij} \geq 0, \forall i \in I, j \in J \\
& y_{ik} \geq 0, \forall i \in I, k \in K \\
& z_{jk} \geq 0, \forall j \in J, k \in K
```

In `JuMP`, we can implement the model as follows.

```{code-cell}
:tags: [remove-output]

I = 2 # number of factories
J = 4 # number of depots
K = 6 # number of customers

# need to be careful that the zeros here are not free, but impossible routes
fac2dep = [0.5 0.5 1.0 0.2;
           0.0 0.3 0.5 0.2]

fac2c = [1.0 0.0 1.5 2.0 0.0 1;
         2.0 0.0 0.0 0.0 0.0 0.0]

dep2c = [0.0 1.5 0.5 1.5 0.0 1.0;
         1.0 0.5 0.5 1.0 0.5 0.0;
         0.0 1.5 2.0 0.0 0.5 1.5;
         0.0 0.0 0.2 1.5 0.5 1.5]

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

Given the above variables, our objective is to minimise distribution costs.
Since we chose to use zeros for impossible routes, they will automatically disappear in element-wise multiplication (indicated by the `.` in `.*`).

```{code-cell}
:tags: [remove-output]

@objective(model, Min, sum(fac2dep.*x) + sum(fac2c.*y) + sum(dep2c.*z))
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
fix.(x[findall(iszero, fac2dep)], 0.0; force=true)
fix.(y[findall(iszero, fac2c)], 0.0; force=true)
fix.(z[findall(iszero, dep2c)], 0.0; force=true)
```

This model is relatively large, so we print it in a dropdown menu.
```{code-cell}
:tags: [hide-output]

print(model)
optimize!(model)
is_solved_and_feasible(model)
```

Once again, we obtained an optimal solution. Let us see what it entails.

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

````{note}
It is worth taking a second look at how we dealt with impossible routes in the code. Our solution uses `0.0`s to represent them in the data, which is arguably not the best choice as they may easily be mistaken with "free" (i.e., no cost) routes. This way, we can form the objective easily using element-wise multiplication

```julia
@objective(model, Min, sum(fac2dep.*x) + sum(fac2c.*y) + sum(dep2c.*z))
```

but we need to make sure the routes are not actually used

```julia
fix.(x[findall(iszero, fac2dep)], 0.0; force=true)
fix.(y[findall(iszero, fac2c)], 0.0; force=true)
fix.(z[findall(iszero, dep2c)], 0.0; force=true).
```

[`JuMP.fix`](https://jump.dev/JuMP.jl/stable/api/JuMP/#fix) ensures that the given variable is constrained to the specified value, with the `force` flag being necessary since we are overwriting the lower-bound that we made in the creation of the variable.

An alternative approach would be to filter out of the model the variables representing impossible routes

```julia
@variable(model, x[i in 1:I, j in 1:J; !iszero(fac2dep[i,j])] >= 0)
```

This way, we have less variables, but we need to be more careful in using the ones we have since the container `x` is now a different shape.
For example,

```julia
@objective(model, Min, sum(fac2dep.*x) + sum(fac2c.*y) + sum(dep2c.*z))
```

would lead to errors. For this to work, We would need to repeat the if conditions to write it properly

```julia
@objective(model, Min, 
    sum(fac2dep[i,j]*x[i,j] for i in 1:I, j in 1:J, if !iszero(fac2dep[i,j]))
    + sum(fac2c[i,k]*y[i,k] for i in 1:I, k in 1:K, if !iszero(fac2c[i,k]))
    + sum(dep2c[j,k]*z[j,k] for j in 1:J, k in 1:K, if !iszero(dep2c[j,k]))
)
```
````
