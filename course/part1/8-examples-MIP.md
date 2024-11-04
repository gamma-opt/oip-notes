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

# Mathematical programming models: (mixed-)integer examples

In this lecture, we develop further the notion of modelling problem using integer-valued decision variables. When a model is sucht that both continuous and integer variables are present, we say that it is a mixed-integer programming (MIP) model. 

First, we start by introducing the famous **Travelling Salesperson Problem**, which can be formulated as an integer programming model. Then we expand some of our previous examples from the previous lectures, such that they include additional decisions that can be modelled using integer variables.

## Travelling Salesperson Problem

The travelling salesperson problem (TSP) is one of the most famous combinatorial optimisation problems, perhaps due to its interesting mix os simplicity while being computationally challenging. Assume that we must visit a collection of {math}`n` cities at most once, and return to our initial point, forming a so-called **tour**. When travelling from city {math}`i` to a city {math}`j`, we incur in the cost {math}`C_{ij}`, representing, for example, distance or travel time. Our objective is to minimise the total cost of our tour.
Notice that this is equivalent to finding the minimal cost permutation of {math}`n-1` cities, discarding the city which represents our starting and end point.

```{figure} ../figures/random_graph.svg
:name: random_graph
:align: center

An example collection of cities (or points) for which we would like to find the minimum cost tour for.
```

To pose the problem as an integer programming model, let us define {math}`x_{ij}=1` if city {math}`j` is visited directly after city {math}`i`, and {math}`x_{ij}=0` otherwise.
Let {math}`N=\{1,\dots,n\}` be the set of cities.
We assume that {math}`x_{ii}` is not defined for {math}`i\in N`.
A naive model for the travelling salesperson problem would be

```{math}
:nowrap:

\begin{align*}
\mini_{x} &\sum_{i\in N}\sum_{j\in N} C_{ij}x_{ij} \\
\st &\sum_{j\in N\setminus\{i\}}x_{ij}=1,~\forall i\in N \\
&\sum_{i\in N\setminus\{j\}} x_{ij}=1,~\forall j\in N \\
&x_{ij}\in\{0,1\},~\forall i,\forall j\in N : i\neq j.
\end{align*}
```

However, this formulation has an issue. Although it can guarantee that all cities are only visited once, it cannot enforce an important feature of the problem which is that the tour cannot present disconnections, i.e., contain **sub-tours**. In other words, the salesperson must physically visit from city to city in the tour, and cannot "teleport" from one city to another.

```{figure} ../figures/tsp_subtours.svg
:name: subtours
:align: center

A feasible solution for the naive TSP model. Notice the two sub-tours formed.
```

In order to prevent sub-tours, we must include constraints that can enforce the full connectivity of the tour. There are mainly two types of such constraints.
The first is called **cut-set constraints** and is defined as

```{math}
\sum_{i\in S}\sum_{j\in N\setminus S} x_{ij}\geq 1,~\forall S\subset N, 2\leq |S|\leq n-1.
```

The cut-set constraints act by guaranteeing that among any subset of nodes {math}`S \subseteq N` there is always at least one arc {math}`(i,j)` connecting one of the nodes in {math}`S` and a node not in {math}`S`.

An alternative type of constraint is called **sub-tour elimination** constraint and is of the form

```{math}
\sum_{i\in S}\sum_{j\in S}x_{ij}\leq |S|-1,~\forall S\subset N,2\leq |S|\leq n-1.
```

Differently from the cut-set constraints, the sub-tour elimination constraints prevent the cardinality of the nodes in each subset from matching the cardinality of arcs within the same subset.

There are some differences between these two constraints and, typically cut-set constraints are preferred for being more effective from a computational standpoint. In any case, either of them suffers from the same problem: the number of such constraints quickly becomes **computationally prohibitive** as the number of nodes increases. This is because one would have to generate a constraint to each possible node subset combination from sizes 2 to n − 1.

A possible remedy to this consists of relying on delayed constraint generation. In this case, one can start from the naive formulation TSP and from the solution, observe whether there are any sub-tours formed. That being the case, only the constraints eliminating the observed sub-tours need to be generated, and the problem can be warm-started. This procedure typically terminates far earlier than having all of the possible cut-set or sub-tour elimination constraints generated.

```{figure} ../figures/tsp_feasible.svg
:name: feasible
:align: center

A feasible solution without sub-tours.
```

% TODO: a JuMP implementation of the TSP with perhaps a few rounds of cuts to generate a valid solution. We have an example like that in LinOpt if needed.


## Revisiting the food manufacture problem

Recall the  {ref}`p1l5:food` problem. Suppose we want to add some additional conditions on the problem:

- The food produced may never be made up of more than three oils in any month.
- If an oil is used in a month, at least 20 tons must be used.
- If either of VEG 1 or VEG 2 are used in a month, then OIL 3 must also be used.

Conditions of such nature are not uncommon. Often, it is desirable to avoid handling too many ingredients or having them used in too-small amounts. Alternatively, some ingredients may interact with each other in certain ways, for example causing an undesirable chemical reaction, leading to us wanting to impose logical conditions in the model. That said, how can we extend the previous model to take these restrictions into account?

### Solution

All the above conditions depend on whether some oil is used in the blend or not. This is a true/false condition, thus we need integer variables to model it. For that, let

- $d_{ij}$ - whether or not oil $i$ is used in month $j$.

The value of $d_{ij}$ should be linked to that of $u_{ij}$, which represents the amount of use. If $u_{ij}$ is present in the blend, that is it is positive, then $d_{ij}$ should be 1.
Logically, this can be stated as

```{math}
u_{ij} > 0 \iff d_{ij} = 1,
```

which is equivalent to

```{math}
(u_{ij} > 0 \implies d_{ij} = 1) \land (d_{ij} = 1 \implies u_{ij} > 0).
```

We can model this biconditional using the following constraints

```{math}
u_{ij} &\leq M d_{ij} \\
u_{ij} &\geq \epsilon d_{ij},
```

which is the familiar big-M method and its counterpart, where $\epsilon > 0$ is an arbitrarily small constant. In fact, since we have limits on what nonzero values $u_{ij}$ can take, we can take this a step further. Suppose $i$ is a vegetable oil, so we need it to be at most 200 but at least 20. These conditions can be modelled as 

```{math}
u_{ij} &\leq 200 d_{ij} \\
u_{ij} &\geq 20 d_{ij}
```

Here if $d_{ij}=1$, then $u_{ij}$ cannot exceed 200, but need at least 20. If $d_{ij}=0$, then both right-hand sides are zero, which forces $u_{ij}$ to be zero. Repeating this for every oil and month gives us one of the additional conditions we want like to impose.

With $d_{ij}$ defined and linked to $u_{ij}$, the other conditions are straightforward to implement. To limit the number of ingredients in a blend to three oils, we can just include the constraint

```{math}
\sum_{i}d_{ij} \leq 3, \forall j \in J.
```

Finally, the last condition can be logically stated as

```{math}
(d_{1j} \lor d_{2j}) \implies d_{5j},
```

which we can rewrite as

```{math}
(d_{1j} + d_{2j} \geq 1) \implies d_{5j} = 1
```

and

```{math}
(d_{1j} + d_{2j} < 1) \lor d_{5j} = 1.
```

In words, the first statement says that if one or both of $d_{1j}$ or $d_{2j}$ are 1, then $d_{5j}$ must be 1. The second statement says that if $d_{1j}$ and $d_{2j}$ are less than 1, i.e., they are 0, the statement is already satisfied and, as such, there is nothing to be stated regarding the value of $d_{5j}$. This can formulated mathematically as follows.

Let us start with the latter case first. On one hand, assuming that $d_{1j}$ or $d_{2j}$ are not 1, we have that the left-hand side is 1. Thus, we do not care about what value $d_{5j}$ would take, other tha it can be 0 or 1. Thus, we would end up with a mathematical statement such as

```{math}
0\leq d_{5j}
```

which is trivially satisfied.

In the former case, we may have that the left-hand side takes value 1 or 2, but now $d_{5j}$ can only be 1. For this to fit into the above form, we have to multiply the right-hand side of the constraint by 2, yielding.

```{math}
(1\text{ or } 2) \leq 2d_{5j},
```

which yields the constraint
```{math}
d_{1j} + d_{2j} \leq 2d_{5j}, \forall j \in J.
```

````{note}
Alternatively, one may notice that $(d_{1j} + d_{2j} \geq 1) \implies d_{5j} = 1$ may be stated as 

```{math}
(d_{1j}  \geq 1 \implies d_{5j} = 1) \land (d_{2j} \geq 1) \implies d_{5j} = 1)
```

which can then be represented by the constraints

```{math}
\begin{align*}
  d_{1j} \leq d_{5j}, \forall j \in J \\ 
  d_{2j} \leq d_{5j}, \forall j \in J.
\end{align*}  
```

Notice that if we sum the two constraints, we obtain the $d_{1j} + d_{2j} \leq 2d_{5j}, \forall j \in J$. This example illustrates well the fact that seldom there is only one way of modelling problems as mathematical programming models. 
````

With all the additional constraints ready, we can now solve the problem

```{code-cell}
:tags: [remove-cell]
using JuMP, HiGHS

cost = [110 130 110 120 100  90;
        120 130 140 110 120 100;
        130 110 130 120 150 140;
        110  90 100 120 110  80;
        115 115  95 125 105 135]
hardness = [8.8, 6.1, 2.0, 4.2, 5.0]
hardness_ul = 6
hardness_ll = 3
price_product = 150
process_limit_veg = 200
process_limit_non = 250
n_veg = 2
storage_limit = 1000
initial_oil = 500
target_oil = 500
cost_storing = 5
```

```{code-cell}
I,J = size(cost)

model = Model(HiGHS.Optimizer)

@variable(model, d[1:I, 1:J], Bin)  # new
@variable(model, b[1:I, 1:J] >= 0)
@variable(model, u[1:I, 1:J] >= 0)
@variable(model, storage_limit >= s[1:I, 1:J] >= 0)
@variable(model, p[1:J] >= 0)


@objective(model, Max, price_product*sum(p) - sum(cost[i,j]*b[i,j] for i in 1:I, j in 1:J) - cost_storing*sum(s))

@constraint(model, c_cond1_ul_veg[i in 1:n_veg, j in 1:J], u[i,j] <= process_limit_veg*d[i,j]) # new
@constraint(model, c_cond1_ul_non[i in n_veg+1:I, j in 1:J], u[i,j] <= process_limit_non*d[i,j]) # new
@constraint(model, c_cond1_ll[i in 1:I, j in 1:J], u[i,j] >= 20*d[i,j]) # new
@constraint(model, c_cond2[j in 1:J], sum(d[:,j]) <= 3)
@constraint(model, c_cond3[j in 1:J], d[1,j]+d[2,j] <= 2*d[5,j])
@constraint(model, c_production[j in 1:J], sum(u[:,j]) == p[j])
@constraint(model, c_processing_veg[j in 1:J], sum(u[begin:n_veg,j]) <= process_limit_veg)
@constraint(model, c_processing_non[j in 1:J], sum(u[n_veg+1:end,j]) <= process_limit_non)
@constraint(model, c_hardness_ul[j in 1:J], sum(hardness[i]*u[i,j] for i in 1:I) <= hardness_ul*p[j])
@constraint(model, c_hardness_ll[j in 1:J], sum(hardness[i]*u[i,j] for i in 1:I) >= hardness_ll*p[j])
@constraint(model, c_storage_start[i in 1:I], b[i,1]-u[i,1]-s[i,1] == -initial_oil)
@constraint(model, c_storage[i in 1:I, j in 2:J], s[i,j-1]+b[i,j]-u[i,j]-s[i,j] == 0)
@constraint(model, c_storage_end[i in 1:I], s[i,J] == target_oil)

set_attribute(model, "output_flag", false) # Remove the solver printed statement
optimize!(model)
@assert is_solved_and_feasible(model)
```

% TODO: let's make this a bit more engaging. One idea is to compare it with the previous version. It should yield a worse solution (since it has more constraints)

```{code-cell}
println("Objective value: ", objective_value(model))
```

```{code-cell}
:tags: ["remove-input"]
using DataFrames
oils = ["Veg 1", "Veg 2", "Oil 1", "Oil 2", "Oil 3"]
months = ["January", "February", "March", "April", "May", "June"]
df_b = DataFrame(transpose(value.(b)), oils)
df_u = DataFrame(transpose(value.(u)), oils)
df_s = DataFrame(transpose(value.(s)), oils)
df_p = DataFrame(transpose([value.(p)])..., months)
println("Amount purchased (variables b)")
display(df_b)
println("Amount used (variables u)")
display(df_u)
println("Amount stored (variables s)")
display(df_s)
println("Production amount (variables p)")
display(df_p)
```

## Factory planning 2

Recall the problem {ref}`p1l5:production`.
Now, instead of the given maintenance schedule, suppose it is up to us to find one that maximizes the profits.

- Each machine except the grinders must be down for maintenance in any one of the six months.
- Only two of the four grinders each need to be down in any one of the six months.

### Solution
Now, we need to keep track of how many machines are down for maintenance, so we make a new variable
- $d_{kj}$ - number of machines of type $k$ that are down for maintenance in month $j$,

where $k=1,\dots,5$ is grinders, vertical drills, horizontal drills, borers and planers respectively.
Of course, $d_{kj}$ are integer variables, and each type $k$ will impose a different upper bound, based on the number of machines available in total.

With these variables defined, we can impose the appropriate number of maintenances with the constraints
```{math}
\sum^6_{j=1}d_{kj} = \begin{cases}2 &\text{ for }i=1,2, \\
3 &\text{ for }i=3, \\
1 &\text{ for }i=4, \\
1 &\text{ for }i=5.
\end{cases}
```

Lastly, we need these variables to actually affect the amount of production possible.
We do so by modifying our constraints from before to decrease if there is some maintenance going on.
For the case of grinders as an example, instead of what we had before
```{math}
0.5m_{11}+0.7m_{21}+0.3m_{51}+0.2m_{61}+0.5m_{71}\leq 1152 \\
0.5m_{12}+0.7m_{22}+0.3m_{52}+0.2m_{62}+0.5m_{72}\leq 1536 \\
0.5m_{13}+0.7m_{23}+0.3m_{53}+0.2m_{63}+0.5m_{73}\leq 1536 \\
0.5m_{14}+0.7m_{24}+0.3m_{54}+0.2m_{64}+0.5m_{74}\leq 1536 \\
0.5m_{15}+0.7m_{25}+0.3m_{55}+0.2m_{65}+0.5m_{75}\leq 1152 \\
0.5m_{16}+0.7m_{26}+0.3m_{56}+0.2m_{66}+0.5m_{76}\leq 1536
```
we now have a uniform number of available hours minus maintenance
```{math}
0.5m_{1j}+0.7m_{2j}+0.3m_{5j}+0.2m_{6j}+0.5m_{7j}\leq 1536 -384\d_{1,j},
```
and similarly for the remaining machine types.

Now we can solve the modified problem
```{code-cell}
:tags: [remove-cell]
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
set_attribute(model, "output_flag", false)
```

```{code-cell}
:tags: ["remove-output"]

maintenance = [2, 2, 3, 1, 1]

@variable(model, 0 <= d[k in 1:K, 1:J] <= n_machines[k], Int) # new
@variable(model, 0 <= m[1:I, 1:J])
@variable(model, 0 <= h[1:I, 1:J] <= holding_limit)
@variable(model, 0 <= s[i in 1:I, j in 1:J] <= market_limits[j,i])

@objective(model, Max, sum(s[i,j]*profit[i] for i in 1:I, j in 1:J) - holding_cost*sum(h))

@constraint(model, maintenance[k in 1:K], sum(d[k,:]) == maintenance[k])
@constraint(model, usage[k in 1:K, j in 1:J], sum(machine_usage[k,:].*m[:,j]) <= days_per_month*shifts_per_day*hours_per_shift*(n_machines[k]-d[k,j])) # modified
@constraint(model, holding_jun[i in 1:I], h[i,6] == holding_target)
@constraint(model, continuity_jan[i in 1:I], m[i,1]-s[i,1]-h[i,1] == 0)
@constraint(model, continuity[i in 1:I, j in 2:J], h[i,j-1]+m[i,j]-s[i,j]-h[i,j] == 0)

optimize!(model)
@assert is_solved_and_feasible(model)
```

```{code-cell}
println("Objective value: ", objective_value(model))
```

```{code-cell}
:tags: ["remove-input"]
println("Manufacturing")
label = ["Product $(i)" for i in 1:I]
label2 = ["Machine type $(i)" for i in 1:K]
a = DataFrame(transpose(value.(m)), label)
display(a)
println("Holding")
b = DataFrame(transpose(value.(h)), label)
display(b)
println("Selling")
c = DataFrame(transpose(value.(s)), label)
display(c)
println("Maintenance")
e = DataFrame(transpose(value.(d)), label2)
display(e)
```