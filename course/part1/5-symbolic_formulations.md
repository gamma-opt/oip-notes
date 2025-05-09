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
  display_name: Julia 1.10.4
  language: julia
  name: julia-1.10
---

# Symbolic formulation

## Motivation for symbolic formulations

One aspect that might have become evident is that, as models start to have more numerous entities, such as production plants, demand points, arcs, and time periods, very quickly the mathematical programming model becomes less and less human readable. This, in turn, compromises model validation and maintenance. Furthermore, it makes it inefficient and prone to error to make updates in the model's input data.

A best-practice approach is to have the **model data** separated from the **model formulation**. Effectively, this dissociates the maintenance of the model and its data source, while allowing for the creation of multiple instantiations of the same model. To achieve that, we must rely on abstract entities that represent the elements of the problem. We describe those next.

## Elements of a symbolic formulation

### Model data

The input data, or model data, is represented by **indices** and their **sets** and **parameters**.

- **Indices and sets**: represent entities in the problem that are discrete and can be grouped by what they represent in the model.
- **Parameters**: are numerical values representing quantities that are associated with indices or combinations of indices.

We have come across these before. For example, in the {ref}`p1l5:distribution` problem, we defined the factories as $i = 1:\text{Helsinki}, 2:\text{Jyväskylä}$. If we define the set $I = \braces{1,2}$, then we can say that the cities are defined as $i \in I$. Now, we can represent the monthly supply capacity of each plant as $C_i$ for all $i \in I$, or equivalently $\forall i \in I$.

```{note}
It is a convention to represent sets with capital letters and indices with lower case letters (often the same).
```

### Model formulation

The model formulation is composed by **variables**, **objective function**, and **constraints**. We have considered their role in detail before, so we now focus on how to pose them such that they are independent of the input data.

Let us start with **decision variables**. Most of the time, our decision variables will be indexed with the defined indices. So, suppose we have a index set $j \in J$, representing some entity in our model. Then, to define a decision variable for each of these, we define $x_j$, $\forall j \in J$. This indicates that we have a decision variable $x$ for each index $j$ in the set $J$.

This can be extended to as many indices as necessary. Going back to our distribution planning problem, where we had $i \in I$ factories and $j \in J$ depots, our flow variables could be represented as $x_{ij}$, $\forall i \in I, j \in J$.

Once we have variables defined, we can use them to pose objective functions. A compact way to do so is to express them as summation of products between parameters and variables (recall our linearity premise discussed in {numref}`p1l4-linear_models`). Coming back to our variable $x_j$, $\forall j \in J$, suppose we have a cost coefficient $C_j$, $j \in J$, associated with each. Then, our objective function can be posed as

```{math}
\mini_{x} C_1x_1 + C_2x_2 + \dots + C_{|J|}x_{|J|} \equiv \mini_{x} \sum_{j \in J} C_jx_j.
```

Notice a couple of nice features about this way of posing our objective function. First, there is the fact that it is a much more compact notation, which can be quickly read by a human. Second, it **remains compact**, regardless of the cardinality of the index set $J$ (represented $| \ \cdot \ |$).

```{note}

The use of the decision variable $x$ as an subscript in $\mini_{x}$ is a handy reminder of which symbols are the decision variables when it is not obvious from context alone. 

```

The same logic can be applied to constraints, being the main difference that we must consider not only the summation domains, but also the **replication** domain (or the indexing) of the constraints. Suppose we have a parameter $a_{ij}$, for $i \in I, j \in J$ multiplying our variables $x_j$, with $j \in J$, and that their combined sum must be less or equal a quantity $b_i$, defined for each $i \in I$. For simplicity, assume for now that $|I| = |J| = 2$. Assume that each constraint must be summed in the domain of $i \in I$ and replicated $j \in J$. Since we have two indices for each set, we would have the following constraints

```{math}
\begin{aligned}
    & a_{11}x_1 + a_{12} \le b_1 \\
    & a_{21}x_1 + a_{22} \le b_2.
\end{aligned}
```

The above can be equivalently represent by the single constraint statement

```{math}
    \sum_{j \in J} a_{ij}x_{j} \le b_i, \ \forall i \in I.
```

Again, notice how much more compact is this set of constraints. With a single statement we can represent sets of constraints at once, in a far more compact notation. Let us explore these ideas a bit further returning to our transportation problem.

## Example - Food manufacture

Let us revisit our food manufacture problem ({numref}`p1l5:food`) and pose it as model written in symbolic formulation.

### Indices and sets

The food manufacture problem has two sets of entities: a set of oils $i \in I = \{1,2,\dots,5\}$ and a set of time periods (months) $j \in J=\{1,2,\dots,6\}$.
In the case of months, there is a clear ordering for the elements, so the index $j-1$ has a defined meaning, i.e., the month before $j$.

### Parameters

There are 10 (groups of) parameters:

- Oil prices for different months, which we represent by $C_{ij}$, for each $i \in I$, $j\in J$,
- Oil hardness $H_i$, for $i \in I$,
- Hardness lower and upper limits $H^L$ and $H^U$, respectively,
- Blended product price $P$,
- Monthly processing limits $L^1$ for vegetable oils and $L^2$ for non-vegetable oils,
- Number of vegetable oil options $N$, which implies the number of non-vegetable oil options is $|I|-N$.
- Monthly storage limit per oil $S$,
- Initial oil inventory $S^0$,
- Target oil inventory $S^T$, and
- Store cost per ton per month $C^S$.

### Variables

Our blending model has four types of decision variables:

- $b_{ij}$ - amount of oil $i$ purchased in month $j$,
- $u_{ij}$ - amount of oil $i$ used for blending in month $j$,
- $s_{ij}$ - amount of oil $i$ stored in month $j$, and
- $p_j$ - amount of product produced (and sold) in month $j$.

Naturally, we must enforce that these amounts are not negative.

### Objective function

Our objective is to maximize profit, which is defined as

```{math}
:label: p1l6:obj
\maxi \sum_{j \in J} Pp_j - \sum_{i \in I} \sum_{j \in J} C_{ij}b_{ij} - \sum_{i \in I} \sum_{j\in J}C^S s_{ij}.
```

Notice how we need a double summation for two terms since we have two indices to sum over.

### Constraints

There are five main constraint sets in the transportation problem: 

- **Linear production**: The quantity of oil used is the quantity of final product, in any given month $j$. Thus we have that

```{math}
\sum_{i \in I} u_{ij} = p_j, \forall j \in J.
```

- **Processing limits**: Every month, we can refine only up to a certain amount of vegetable and non-vegetable oils. Therefore we have

```{math}
\begin{rcases}
\begin{aligned}
\sum_{i=1}^N u_{ij} &\leq L^1 \\
\sum_{i=N+1}^{|I|} u_{ij}&\leq L^2
\end{aligned}
\end{rcases} \forall j \in J
```

- **Hardness interval**: The product hardness must lie within the correct interval. We can incorporate this with

```{math}
\begin{rcases}
\sum_{i \in I} H_iu_{ij} \leq H^U y_j \\
\sum_{i \in I} H_iu_{ij} \geq H^L y_j \\
\end{rcases} \forall j \in J
```

- **Storage balance**: Using and storing product must happen correctly.

```{math}
\begin{rcases}
\begin{aligned}
S^0 + b_{ij}-u_{ij}-s_{ij} &= 0, j=1 \\
s_{i(j-1)} + b_{ij} -u_{ij} - s_{ij} &= 0, \forall j \in \{2,3,\dots,6\} \\
s_{i5} + b_{i6} -u_{i6} &= S^T, j=6
\end{aligned}
\end{rcases} \forall i \in I
```

- **Storage limits**: We can store up to $S$ units of each oil per month.

```{math}
\begin{align}
s_{ij}\leq S, \forall i \in I, j \in J.
\end{align}
```

Putting the whole model together, we obtain the following model formulation. Notice that we have reorganised some of the constraints such that it resembles how it is implemented, which we will do next.

```{math}
\maxi & \sum_{j \in J} Pp_j - \sum_{i \in I} \sum_{j \in J} C_{ij}b_{ij} - \sum_{i \in I} \sum_{j\in J}C^S s_{ij} \\
\st & \sum_{i \in I} u_{ij} = p_j, \forall j \in J \\
& \sum_{i=1}^N u_{ij} \leq L^1, \forall j \in J \\
& \sum_{i=N+1}^{|I|} u_{ij} \leq L^2, \forall j \in J \\
& \sum_{i \in I} H_iu_{ij} \leq H^U y_j, \forall j \in J \\
& \sum_{i \in I} H_iu_{ij} \geq H^D y_j, \forall j \in J \\
& S^0 + b_{i1}-u_{i1}-s_{i1} = 0, \forall i \in I, j = 1 \\
& s_{i5} + b_{i6} -u_{i6} = S^T, \forall i \in I, j = 6 \\
& s_{i(j-1)} + b_{ij} -u_{ij} - s_{ij} = 0, \forall i \in I, \forall j \in \{2,3,4,5\} \\
& s_{ij} \leq S, \forall i \in I, \forall j \in J \\
& b_{ij}, u_{ij}, s_{ij}, p_j \geq 0, \forall i \in I, \forall j \in J. \\

```

## Code

Here, we show how to solve the food manufacturing problem programmatically. We will solve the problem once again using Julia and `JuMP`.

```{code-cell}
using JuMP, HiGHS, Parameters
```

Since this is a larger problem than what we have seen before, it may be worth being more principled about how we write the code.
For example, for this problem, we will first solve the instance described in {numref}`p1l5:food`, then randomly generate a larger instance of the problem to solve.
We will write our code in a way so that it will work for both (and any other) instances of the problem.

```{seealso}
:class: dropdown

Some design patterns to make this process easy and robust is described [in this JuMP tutorial](https://jump.dev/JuMP.jl/stable/tutorials/getting_started/design_patterns_for_larger_models/).
One pattern we make use is to declare a data structure for the parameters.
```

Let us first define a class (or structure, in Julia parlance) that will store our input data.

```{code-cell}
:tags: [remove-output]

@with_kw struct FoodParams
    cost::Matrix{Int64}
    hardness::Vector{Float64}
    hardness_ul::Int64
    hardness_ll::Int64
    price_product::Int64
    process_limit_veg::Int64
    process_limit_non::Int64
    n_veg = Int64
    storage_limit::Int64
    initial_oil::Int64
    target_oil::Int64
    cost_storing::Int64
end
```

```{note}
The `@with_kw` macros is a Julia trick to prevent us from having to use the syntax `struct.argument` and refer directly to `argument` once we have used `@unpack struct` in our code. This is purely for aesthetical reasons, to improve the code readability.
```


This way, we can define only a single, generic function that takes `FoodParams` as inputs, and just change the input for different instances.

(food_manufacture_small)=
### Small problem

Now, we are ready to solve the instance discussed in {numref}`p1l5:food`.
First, we determine the parameters of our problem.

```{code-cell}
:tags: [remove-output]

small_params = FoodParams(
    cost = [110 130 110 120 100  90;
            120 130 140 110 120 100;
            130 110 130 120 150 140;
            110  90 100 120 110  80;
            115 115  95 125 105 135],
    hardness = [8.8, 6.1, 2.0, 4.2, 5.0],
    hardness_ul = 6,
    hardness_ll = 3,
    price_product = 150,
    process_limit_veg = 200,
    process_limit_non = 250,
    n_veg = 2,
    storage_limit = 1000,
    initial_oil = 500,
    target_oil = 500,
    cost_storing = 5
)
```

Then, we wrap the model in a function that receive the data structure as an input.

```{code-cell}
:tags: ["remove-output"]

function solve_food_manufacture(params::FoodParams)
    @unpack_FoodParams params
    I,J = size(cost)

    model = Model(HiGHS.Optimizer)
    @variable(model, b[1:I, 1:J] >= 0)
    @variable(model, u[1:I, 1:J] >= 0)
    @variable(model, storage_limit >= s[1:I, 1:J] >= 0)
    @variable(model, p[1:J] >= 0)

    @objective(model, Max, price_product*sum(p) - sum(cost[i,j]*b[i,j] for i in 1:I, j in 1:J) - cost_storing*sum(s))

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

    return value.(b), value.(u), value.(s), value.(p), model
end

b, u, s, p, model = solve_food_manufacture(small_params)
```

What is happening here? Let's inspect step by step.
First, we unpack the input `params` using [`Parameters.jl`](https://github.com/mauro3/Parameters.jl), which makes the object parameters available in the function scope, allowing us to write for example `cost` instead of `params.cost`.
```julia
@unpack_FoodParams params
```

In order to solve the problem, we need to define the model.
```julia
model = Model(HiGHS.Optimizer)
```

Next, we define a decision variable for each decision that must be made, that is how much oils are purchased, used and stored, and how much product is produced.
`JuMP` allows one to set upper and lower limits, which is ideal for nonnegativity constraints and others.

```julia
@variable(model, b[1:I, 1:J] >= 0)
@variable(model, u[1:I, 1:J] >= 0)
@variable(model, storage_limit >= s[1:I, 1:J] >= 0)
@variable(model, p[1:J] >= 0)
```

```{note}
The first line is equivalent to manually adding the constrains $b_{11} \ge 0, ... p_{6} \ge 0$, and the third line is similar.
```

The objective can be specified using comprehensions, writing out all terms in the summation terms of {eq}`p1l6:obj`, which we can then sum over.

```julia
@objective(model, Min, price_product*sum(p) - sum(cost[i,j]*b[i,j] for i in 1:I, j in 1:J) - cost_storing*sum(s))
```

Multiple constraints obeying the same form can be defined and labeled in a single statement. Here, we define the same linear production constraint for every month,

```julia
@constraint(model, c_production[j in 1:J], sum(u[:,j]) == p[j])
```

and other constraints are replicated similarly.

````{warning}
Note that the above function is not perfectly generalized.
For example, the fact that there are only two types of oil is hard-coded here

```julia
@constraint(model, c_processing_veg[j in 1:J], sum(u[begin:n_veg,j]) <= process_limit_veg)
@constraint(model, c_processing_non[j in 1:J], sum(u[n_veg+1:end,j]) <= process_limit_non)
```

along with the use of the parameter `n_veg`. An alternative for a scenario where we have $A$ different types of oil, each containing $a_1,\dots,a_A$ options, repectively, could have been to specify an array of length $A$ that is made up of $a_1,\dots,a_A$.

This level of generalization is sufficient for our demonstration, but remember and follow consistently your assumptions when you are writing models.
````

With the model specified in `JuMP`, we can print it to see the equations directly.

```{code-cell}
:tags: ["hide-output"]
print(model)
```

At the end of the function, we perform the optimisation and ensure that the problem is solved, so that the returned values are ready for our use.

```julia
optimize!(model)
@assert is_solved_and_feasible(model)
```

We can inspect both the resulting objective value and the decision variables themselves.

```{code-cell}
println("Objective value: ", objective_value(model))
```

```{code-cell}
using DataFrames
oils = ["Veg 1", "Veg 2", "Oil 1", "Oil 2", "Oil 3"]
months = ["January", "February", "March", "April", "May", "June"]
df_b = DataFrame(transpose(b), oils)
df_u = DataFrame(transpose(u), oils)
df_s = DataFrame(transpose(s), oils)
df_p = DataFrame(transpose([p])..., months)
println("Amount purchased (variables b)")
display(df_b)
println("Amount used (variables u)")
display(df_u)
println("Amount stored (variables s)")
display(df_s)
println("Production amount (variables p)")
display(df_p)
```
% &nbsp; is non-breaking space
The maximum profit is €107&nbsp;843, with the above distribution plan.

In this small problem, we had 12 decision variables (one for each plant-city combination) as well as a non-negativity constraint for each of the variables, 3 constraints to ensure supply is not exceeded, and 4 constraints to ensure demand is met, for a total of 19 constraints. However, with symbolic formulation, we can immediately handle much larger models.

### Larger instance

Here, we randomly generate an instance of the problem with $I=20$ oils and $J=12$ months.

```{code-cell}
:tags: ["remove-output"]

using Random
Random.seed!(42)

I = 20 # oils
J = 12 # months
n_veg = 12

mean_hardness_veg = 7
mean_hardness_non = 4
hardness_veg = clamp.(11 .+ 2*randn(n_veg), 1, Inf)
hardness_non = clamp.(3 .+ 1*randn(I-n_veg), 1, Inf)

large_params = FoodParams(
    cost = round.(120 .+ 20*randn((I,J))),
    hardness = vcat(hardness_veg, hardness_non),
    hardness_ul = 10,
    hardness_ll = 5,
    price_product = 150,
    process_limit_veg = 800,
    process_limit_non = 1000,
    n_veg = n_veg;
    storage_limit = 1000,
    initial_oil = 500,
    target_oil = 500,
    cost_storing = 5
)
```

Notice that the separation of the model (i.e., its symbolic formulation) and the data allows us to simply reuse the function we defined above.

```{code-cell}
:tags: ["remove-output"]
b, u, s, p, model = solve_food_manufacture(large_params)
```

Since there are too many variables, printing the solution is not viable. However, we can visualise it.

```{code-cell}
:tags: ["remove-input"]
using CairoMakie

pos = vcat([repeat([i], I) for i in 1:J]...)

f = Figure()
ax_b = Axis(f[1,1], xticks=1:J, title="Amount purchased (variables b)", width = 400, height = 300)
ax_u = Axis(f[1,2], xticks=1:J, title="Amount used (variables u)", width = 400, height = 300)
ax_s = Axis(f[2,1:2], xticks=1:J, title="Amount stored (variables s)", width = 400, height = 300)
barplot!(ax_b, pos, vec(b), stack=pos, color=repeat(1:I,J))
barplot!(ax_u, pos, vec(u), stack=pos, color=repeat(1:I,J))
barplot!(ax_s, pos, vec(s), stack=pos, color=repeat(1:I,J))
Legend(f[1:2,3], [PolyElement(polycolor = i, polycolormap=:viridis, polycolorrange= (1, I)) for i in 1:I], ["Oil $(i)" for i in 1:I], "Oils")
resize_to_layout!(f)
f
```

On the top right, we can see that every month, the production capacity is used fully, and the composition of the blends vary.
On the bottom graph, we see that the last month storage is filled, since there is a constraint to ensure a certain level of stocks.
And the storing pattern is linked to the buying pattern as it should be: in the first months, production relies on stored oils, so stocks decrease.
Eventually, more oil is being bought and the ingredient stocks are rebuilt.
