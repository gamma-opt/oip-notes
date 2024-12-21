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
  display_name: Julia 1.10.5
  language: julia
  name: julia-1.10
---

# Nonlinear Optimisation

## Introduction

We now turn our focus to the assumption of linearity we have been carrying so far. Earlier, we have stated that we would stick with models that can be stated as linear functions, both in the objective function and in the constraints. The reason for that is purely **algorithmic**, and there is nothing that, from a conceptual point, prevents the use of nonlinear functions.

In general, by assuming linearity in our optimisation models as we have been doing so far, we are assuming that:

- Returns and/ or costs are **constant** and not affected by scale;
- The use of resources by an activity is **proportional** to the level of activity;
- The total use of resource by a number of activities is the **sum** of the uses by the individual activity.

Clearly, these are simplifying but still reasonably good approximations in many settings. However there are a couple of settings where one cannot simply ignore how quantities and properties interact with each other, which is exactly what leads us to dealing with nonlinear models.

If one were to consider computational aspects, then there are several important issues to take into account. The reason why mathematical programming modellers go beyond their means to obtain (mixed-integer) linear programming models is because the of **simplex method**, the algorithm underlying the solution of such problems is a practical success. Since its conception in the 50's, it has seem a myriad of developments that has turned it into a robust and reliable algorithm for solving mathematical programming problems.

However, with the exception of a few special cases, if there is any nonlinearity in the model, we cannot use simplex-method based algorithms, and departing from them can be scary in many ways. For problems with continuous variables only, the alternative is to use a interior point (or barrier) method. These methods, developed in the 90's based on much earlier results, have seen significant developments in terms of their implementation, and have become, in many cases, almost as common as the algorithm of choice to solve continuous mathematical programming models, including strictly nonlinear. We will discuss their differences in detail later on in the course.

For now, what you need to keep in mind is this: the line that separates mathematical programming models that can be comfortably treated and those that cannot has nothing to do with nonlinearity, but rather, with **convexity**. Interior point methods (and the simplex method too) are engineered to converge to points where first-order optimality conditions hold. But these can only be guaranteed to be optimal points if the problem at hand is convex; otherwise, nothing stronger can be said about the solution found without more specialised way to search for the feasible region.

%Add a remark about mixed integer problems, who are nonconvex problems whose linear relaxation is convex. That is sort of the reason why whether they are tractable sometimes, but sometimes they suck. It is about how much the "nonconvex part" dominates the convex part (or how strong or weak the relaxation is -- too much?)

## Convex problems

We say that an optimisation problem is a **convex** if it has

- A **convex objective** function to be minimised or a concave objective function to be maximised;
- A **convex feasibility** set.

More formally, let our optimisation problem be defined in the following general way:

```{math}
:label: opt-problem

\mini & f(x) \\
\st   & g(x) \le 0 \\
      & h(x) = 0.
```

```{prf:definition} Convex optimisation problem
The mathematical optimisation problem {eq}`opt-problem` is a convex optimisation problem if and only if:
  1. $f(x)$ is a convex function;
  2. $g(x)$ is a convex function;
  3. $h(x)$ is a linear (or affine) function.
```

We discussed the notion of convexity in {numref}`p1l2`, and concluded that for convex functions, first-order optimality (zero-gradient) conditions are sufficient to certify the optimality of a candidate solution. It turns out that, if the subdomain (in in our case, the feasibility set) is a convex set, a generalisation of these first-order conditions (known as Karush-Kuhn-Tucker, or KKT conditions) exist and are also **necessary and sufficient** for optimality. Interior point methods, the flagship method for nonlinear optimisation problems, are engineered to search for points that satisfy KKT conditions.

```{warning}
Interior point methods, or any other optimisation methods can be very well used to solve nonconvex optimisation problems. The issue is that, for these problems, the KKT conditions are necessary (i.e., they have to hold) **but not sufficient** to certificate optimality of the solution found. It is up to the user to know whether that solution can be certified as a global optimal solution.  
```

```{note}
Linear functions are convex, and thus, linear programming problems are convex problems. That is why both interior point method and the simplex method can be safely employed for finding (global) optimal solutions for linear programming problems.
```

### Objective function as a convex function

There are few functions that are convex functions and frequently appear as objective functions in mathematical programmes. Next, we list a few of them.

#### Quadratic functions

Quadratic functions are functions that involve the multiplication of two decision variables. A typical example is illustrated in {ref}`p1l10:agricultural_pricing` example below, where a price, which is dependent of the quantity produced, is multiplied by the actual quantity produced. Another common setting is when some sort of **regularisation** is imposed to decision variables, which is typically achieved by minimising their squared value.

The general form of a quadratic function can be stated as

```{math}
f(x) = c^\top x + x^\top Qx,
```

where $x$ represents our decision variables (a $n$-dimensional vector assuming we have $n$ decision variables), $c$ is an $n$-dimensional vector of parameters and $Q$ is the matrix of the quadratic form.

```{note}
The matrix of the quadratic form $ax_1^2 + bx_1x_2 + cx_2^2$ is given by: {math}`\begin{bmatrix} a & \frac{b}{2} \\ \frac{b}{2} & c \end{bmatrix}`. 

**This generalises for $n$ dimensions:** let $q_{ij}$ be the element of $Q$ in row $i$ and column $j$. The main diagonal has the coefficient of the quadratic terms $q_{ii}x_i^2$, $i=1,...,n$, and for the $q_{ij}x_ix_j$ we have $q_{ij} / 2$ in the $i^\text{th}$ row and $j^\text{th}$ column  as well as the $j^\text{th}$ row and $i^\text{th}$ column of $Q$.
```

The quadratic function $f$ is convex depending on the matrix $Q$. The technical term is that $Q$ needs to be positive semidefinite (PSD), which roughly means that when we multiply $Q$ by a vector $x$, it does not flip the sign of any of the coordinates of $x$. There are many ways one can attest whether the matrix $Q$ is PSD, but perhaps the simpler is to use a linear algebra package to check if its eigenvalues are non-negative (i.e., positive or zero).

```{warning}
Notice that our standard form is a minimisation. When **maximising**, we want the objective function to be a **concave** function for the problem to be convex. In that case, we need to verify if $Q$ is negative semi-definite, which will be the case if its eigenvalues are nonpositive.
```


#### Polynomials, exponential and logarithms 

More seldom, one may see the need of using other functions that are not quadratic. Some other common convex functions include:

- *Powers*: $x^a$ is concave for $ 0 \le a \le 1$ and convex for $a \ge 1$ or $a \le 0$;
- *Exponential*: $e^{ax}$ with $a > 0$ is convex for any $x \in \reals$;
- *Logarithms:* $\log x$ is concave and $x \log x$ is convex for $x > 0$;

Below is a plot of these functions, which showcase well their convex nature.

```{code-cell}
:tags: ["remove-input"]

using CairoMakie
x = range(0, 4, 100)
fig = Figure()
ax = Axis(fig[1,1])

lines!(ax, x, exp, label=L"e^x")
lines!(ax, x, x->x^2, label=L"x^2")
lines!(ax, x, x->x*log(x), label=L"x \log x")
axislegend(labelsize=20)

fig
```

There are a few other functions that are convex. Also, there are a few operations that preserve convexity. The most important one is perhaps the following:

````{prf:definition} Non-negative weighted sum
:label: def-convex-weighted-sum

Let $f_i(x)$, and $w_i \ge 0$, $i \in \braces{1,\dots,n}$ be $n$ convex functions and nonnegative weights, respectively. The function 

```{math}
  g(x) = \sum_{i=1}^n w_i f_i(x)
```

is convex.
````

This is a useful result because, typically, to verify whether a function is convex or not, we must break it into parts and verify whether they are convex functions and if they have been combined by convexity preserving operations.

For example, before we mentioned that $f(x) = c^\top x + x^\top Qx$ was convex, which can be verified by splitting $f$ into $f_1(x) = c^\top x$, which is convex (and concave simultaneously), and $f_2(x) = x^\top Q x$, which is convex if $Q$ is PSD. By making $w_1 = w_2 = 1$, we can use {prf:ref}`def-convex-weighted-sum` to show that $f$ is convex.

### Constraints as convex sets

We now focus on the terms $g$ and $h$. Whenever we impose an image value to a function (or a set of them, via an inequality), we are implicitly defining a **set**. For example, when we state that $h(x) = 0$, this creates a set of all $x$ that when inputted in $h$ return zero; likewise $g(x) \le 0$ represents the set of all solutions $x$ that when inputted to $g$, return a negative number or zero.

We can infer the convexity of these set of solutions by analysing the convexity of the functions:

- For equality constraints, the only way in which $h(x)=0$ can generate a convex set is if $h$ is linear;
- For inequalities, the set of constraints will be convex if $g(x)$ is a convex function in $g(x) \le 0$.

```{note}
Remember that if $g$ is convex, $-g$ is concave. Thus we can infer that, by multiplying $g(x) \le 0$ by -1, we see that for greater-or-equal-than constraints, we obtain convex sets whenever the function is concave. 
```

## Examples of convex problems

### Classification as an optimisation problem

One of the most classical problems in machine learning is that of **binary classification**, where given some $n$ data points $(x^1, x^2, ..., x^n)$, the goal is to obtain a function $f$ that separates the partitions.
Specifically, we will now focus on linear classification, where we seek an affine function $f(x)=a^\top x - b$, or equivalently the parameters $a$ and $b$, that gives us an appropriate classifier, i.e.,

```{math}
f(x^i) = \begin{cases} 
1&\text{if } a^\top x^i - b > 0 \\
-1&\text{if } a^\top x^i - b < 0.
\end{cases}
```

For example, our problem may be of detecting spam in emails, where we'd like to distinguish between regular ones and emails that can be ignored (i.e., spam). Our features then may be the word count, count of repeated word stems and/or others.

Suppose we have the following data we would like to classify, based on two features and with the colors indicating the true classification $y^i, i\in I=\{1,2,\dots,n\}$.

```{code-cell}
:tags: [remove-output]
using Random
using Distributions: MvNormal

Random.seed!(42)

m1 = [1,3]
sd1 = 1
m2 = [7,7]
sd2 = 1
N = 50 # number of examples per group

class_neg = rand(MvNormal(m1, sd1), N)
class_pos = rand(MvNormal(m2, sd2), N)
```

```{code-cell}
:tags: [remove-input]
using CairoMakie

DEF_COLORS = Makie.wong_colors()

fig = Figure(fontsize=30)
ax = Axis(fig[1,1],
    xlabel="feature 1", 
    ylabel="feature 2",
    limits=(-2, 10, 0, 10)
    )
scatter!(ax, class_neg)
scatter!(ax, class_pos)

fig
```

Many lines classify this set of data correctly, including the one defined by $a=\begin{bmatrix}5\\1\end{bmatrix}, b=30$.

```{code-cell}
:tags: [remove-input]
ablines!(ax, [30], [-5]; color=:red)
fig
```

Arguably, this is not the best classifier. For example, suppose we use this trained classifier to infer about a new observation (i.e., data point) $(5,4)$. Intuitively, we may guess that this point belongs to the orange class, since it is much closer to it.
However, our line classifies this point otherwise.

```{code-cell}
:tags: [remove-input]
temp = scatter!(ax, [(5,4)], color=DEF_COLORS[2], marker=:diamond)
fig
```

To make our classifier more **robust**, we may want to pick the maximum-margin line, which maximises the distance to the nearest data points in either classes. The width of the margin is $\frac{2}{\|a\|}$ ([see why here](#margin_width)), thus maximizing the width corresponds to minimizing $\|a\|=\sqrt{a_1^2+a_2^2}$, which we can formulate this as an optimisation problem:

```{math}
\mini & \|a\|^2 \\
\st & a^\top x_i - b \geq 1, \forall i\in I, \text{ if } y_i = 1\\
& a^\top x_i - b \leq -1, \forall i\in I, \text{ if } y_i = -1.
```

Here, we minimise $\|a\|^2$ instead as a small shortcut, since the minimum will not change by squaring the square root (this property is called monotonicity and is often exploited to yield strictly convex ``equivalents'' of noncovex/ nondifferentiable functions, such as the square root).
The constraints ensure that the points are classified correctly, for example if $y_i=1$ for some $i\in I$, then the point should be above the top margin, i.e. $a^\top x_i-b\geq 1$. Similarly, if $y_i=-1$, then the point should be below the bottom margin, i.e., $a^\top x_i-b \leq -1$.

This problem is obviously nonlinear: the squared-norm is composed of quadratic terms. It is in fact a convex problem: the objective is the sum of quadratic terms, thus a convex function, and the constraints are affine functions (with changing signs), and thus are also convex.

```{admonition} Why is the margin width equal to $\frac{2}{\|a\|}$?
:class: note, dropdown
:name: margin_width

A proof is [here](https://youtu.be/_PwhiWxHK8o?t=1020).
```

The training of our robust classifier can be posed as the following optimisation model:

```{code-cell}
using JuMP, Ipopt

model = Model(Ipopt.Optimizer)
set_silent(model)
@variable(model, a[1:2])
@variable(model, b)

@objective(model, Min, sum(a.^2))

@constraint(model, c1[i=1:N], sum(a.*class_pos[:,i])-b >= 1)
@constraint(model, c2[i=1:N], sum(a.*class_neg[:,i])-b <= -1)

optimize!(model)

println(value.(a))
println(value(b))
```

Below we plot the resulting model obtained given our training data, including the margins on either side.

```{code-cell}
:tags: [remove-input]

max_margin_a = value.(a)
max_margin_b = value(b)
mult = 1/max_margin_a[2]  # need to multiply stuff by this to make a[2] coefficient 1 in drawing the abline
intercept = max_margin_b*mult
slope = -max_margin_a[1]*mult
ablines!(ax, [intercept], [slope], color=DEF_COLORS[3])
ablines!(ax, [intercept-mult, intercept+mult], [slope, slope], linestyle=:dash, color=DEF_COLORS[3])
fig
```

Note that in the above, the diamond-shaped point representing our new observation is within the margin because it was not included in the training data. However, the fact that it is correctly classified by the maximum-margin classifier is testament to the robustness of this method.

(p1l10:agricultural_pricing)=
### Agricultural pricing

This example is adapted from {cite}`williams_model_2013`. We are consulted by the government of a country to help with pricing their dairy products. There are four products for us to consider:

- milk,
- butter, and
- two varieties of cheese: Cheese 1 and Cheese 2.

All these products are made directly or indirectly using the country's raw milk production, which is divided into fat and dry matter. The total yearly availability for the two ingredients are 600 000 tons of fat and 750 000 tons of dry matter. The compositions of the products in terms of the ingredients are provided in {numref}`agri:composition`.

```{table} Percentage compositions of the products
:name: agri:composition
|          | **Fat** | **Dry matter** | **Water**   |
|:--------:|:-------:|:--------------:|:-----------:|
|   Milk   |    4    |        9       | 87          |
|  Butter  |    80   |        2       | 18          |
| Cheese 1 |    35   |       30       | 35          |
| Cheese 2 |    25   |       40       | 35          |
```

In addition, we are given the **price elasticities** of demand in {numref}`agri:elasticity`. The price elasticity of a product is a measure of the sensitivity of the demand for the product to its price and is defined as

```{math}
E = \frac{\text{\% decrease in demand}}{\text{\% increase in price}}.
```

Similarly, the substitution effect between two types of cheese is measured by **cross-elasticity** of the demand. The cross-elasticity from a product A to product B is given by

```{math}
E_{AB} = \frac{\text{\% increase in demand for A}}{\text{\% increase in price of B}}.
```

These can be approximated based on price and consumption data. The estimated elasticities are given in {numref}`agri:elasticity`.

```{table} Elasticity of products
:name: agri:elasticity
| Milk | Butter | Cheese 1 | Cheese 2 | Cheese 1 to Cheese 2 | Cheese 2 to Cheese 1 |
|:----:|:------:|:--------:|:--------:|:--------------------:|:--------------------:|
|  0.4 |   2.7  |    1.1   |    0.4   |          0.1         |          0.4         |
```

Our objective is to maximise the total revenue in terms of price and resultant demand. However, we are asked to ensure that the new prices are such that last year's total consumption costs would not have increased with them. To this end, we are also given price and consumption data from last year in {numref}`agri:last_year`.

```{table} Information from last year
:name: agri:last_year
|                                  | Milk | Butter | Cheese 1 | Cheese 2 |
|:--------------------------------:|:----:|:------:|:--------:|:--------:|
| Consumption (1000 tons)          | 4820 | 320    | 210      | 70       |
| Price (€/ton)                    | 297  | 720    | 1050     | 815      |
```

#### Solution

Let $p_m, p_b, p_{c1}$ and $p_{c2}$ be the prices of milk, butter, cheese 1 and cheese 2 in €1000 per ton, and $x_m, x_b, x_{c1}$ and $x_{c2}$ be the corresponding quantities in thousands of tons.

Our goal is to maximize profit

```{math}
\maxi_{p, x} \sum_{i \in \braces{m,b,c1,c2}} p_i x_i.
```

Notice that, since the variables $p_i$ and $x_i$, $i \in \braces{m,b,c1,c2}$, multiply each other, this is a nonlinear problem. 

We are constrained by the limited supply of fat and dry matter, which can be stated as

```{math}
0.04 x_m + 0.8 x_b + 0.35 x_{c1} + 0.25 x_{c2} \leq 600 \\
0.09 x_m + 0.02 x_b + 0.3 x_{c1} + 0.4 x_{c2} \leq 750.
```

Note that since $x_i$ are measured in 1000 tons, we must divide the right hand side so the units on both sides match. In addition, the total consumption costs of this year should not be larger than last year's under the new prices and quantities. Thus,

```{math}
4820 p_m + 320 p_b + 210 p_{c1} + 70 p_{c2} \leq 1939.49,
```

where 1939.49 is obtained by summing the price times consumption values for all products as presented in {numref}`agri:last_year`.

Lastly, we need to relate the quantity variables to the price variables using the elasticity information. The elasticity relationships are defined as follows

```{math}
\dx{x_m} &= -E_m\dx{p_m}, \\
\dx{x_b} &= -E_b\dx{p_b}, \\
\dx{x_{c1}} &= -E_{c1}\dx{p_{c1}} + E_{c1c2}\dx{p_{c2}}, \\
\dx{x_{c2}} &= -E_{c2}\dx{p_{c2}} + E_{c2c1}\dx{p_{c1}},
```

where $\dx {\cdot} > 0$ represents a positive infinitesimal variation in $\cdot$. Notice the negative sign of some of the substitution, denote the inverse relationship between prices and quantities. The above differential equations can be linearly approximated as

```{math}
\lx{x}{m} &= -E_m\lx{p}{m} \\
\lx{x}{b} &= -E_b\lx{p}{b} \\
\lx{x}{c1} &= -E_{c1}\lx{p}{c1}+E_{c1c2}\lx{p}{c2} \\
\lx{x}{c2} &= -E_{c2}\lx{p}{c2}+E_{c2c1}\lx{p}{c1}
```

where $\bar{x}_m$ and $\bar{p}_m$ are the quantity and price for milk from the last year, and similarly for other variables and products. As long as $x_i$ and $p_i$ do not differ significantly from $\bar{x}_i$ and $\bar{p}_i$, these approximations should work reasonably well.

```{note}
We do not know the true function that describes the price elasticity and product substitutions, but we do know that these are rates and, as such, their values can be interpreted as derivatives that can be used in a first-order Taylor approximation. As we seen before, these are reasonably precise, as long as we do not step to far way from the point for which we have the derivative calculated.
```

With that, our complete model is given by

```{math}
\maxi &\sum_{i \in \{m,b,c1,c2\}} p_i x_i \\
\st & 0.04 x_m + 0.8 x_b + 0.35 x_{c1} + 0.25 x_{c2} \leq 600 \\
& 0.09 x_m + 0.02 x_b + 0.3 x_{c1} + 0.4 x_{c2} \leq 750 \\
& 4820 p_m + 320 p_b + 210 p_{c1} + 70 p_{c2} \leq 1939.49 \\
& \frac{x_m - 4820}{4820} = -0.4\frac{p_m-0.297}{0.297} \\
& \frac{x_b - 320}{320} = -2.7\frac{p_b-0.72}{0.72} \\
& \frac{x_{c1} - 210}{210} = -1.1\frac{p_{c1}-1.05}{1.05} + 0.1\frac{p_{c2}-0.815}{0.815} \\
& \frac{x_{c2} - 70}{70} = -0.4\frac{p_{c2}-0.815}{0.815} + 0.4\frac{p_{c1}-1.05}{1.05} \\
& p_i \ge 0, \ \forall i \in \{m,b,c1,c2\} \\
& x_i \ge 0, \ \forall i \in \{m,b,c1,c2\}
```

We can implement this in `JuMP` as follows.

```{code-cell}
using JuMP, Ipopt

cons = [4820, 320, 210, 70]
price = [297, 720, 1050, 815] ./ 1000
elas = [0.4, 2.7, 1.1, 0.4]
elas_c1c2 = 0.1
elas_c2c1 = 0.4
cont_fat = [0.04, 0.8, 0.35, 0.25]
cont_dry = [0.09, 0.02, 0.3, 0.4]
lim_fat = 600
lim_dry = 700
price_index = sum(cons.*price)

model = Model(Ipopt.Optimizer)
set_silent(model)

@variable(model, x[1:4] >= 0)
@variable(model, p[1:4] >= 0)

@objective(model, Max, sum(x.*p))

@constraint(model, fat, sum(cont_fat.*x) <= lim_fat)
@constraint(model, dry, sum(cont_dry.*x) <= lim_dry)
@constraint(model, index, sum(cons.*p) <= price_index)

@constraint(model, milk, (x[1]-cons[1])/cons[1] == -elas[1]*(p[1]-price[1])/price[1])
@constraint(model, butter, (x[2]-cons[2])/cons[2] == -elas[2]*(p[2]-price[2])/price[2])
@constraint(model, cheese1, (x[3]-cons[3])/cons[3] == -elas[3]*(p[3]-price[3])/price[3] + elas_c1c2*(p[4]-price[4])/price[4])
@constraint(model, cheese2, (x[4]-cons[4])/cons[4] == -elas[4]*(p[4]-price[4])/price[4] + elas_c2c1*(p[3]-price[3])/price[3])

optimize!(model)
is_solved_and_feasible(model)
```

To summarize the results, we compare to the last year.

```{code-cell}
:tags: [remove-input]
new_cons = value.(x)
new_price = value.(p)
labs = ["Milk", "Butter", "Cheese 1", "Cheese 2"]
tbl = (cons = vcat(cons, new_cons),
       grp = vcat(map(x->repeat([x],4),1:2)...),
       cat = repeat([1,2,3,4],2),
       labs = vcat(repeat(["last year"], 4), repeat(["this year"], 4)...),
       off_l = [(-42,0),(-42,0),(-46,0),(-42,0)],
       off_r = [(12,0),(12,0),(12,0),(8,0)]
)
colors = Makie.wong_colors()

fig = Figure()
ax_cons = Axis(fig[1,1], yscale=log10, xticks=(1:4, labs), title="Comparison to last year", limits=(nothing, nothing, nothing, 10000), ylabel="Consumption (1000 tons, log-scale)")
barplot!(ax_cons, tbl.cat, tbl.cons, dodge=tbl.grp, color=colors[tbl.cat], bar_labels=tbl.labs, dodge_gap=0.1)

text!(Point.(1:4,35), text="€".*string.(Int.(price.*1000)), offset=tbl.off_l)
text!(Point.(1:4,35), text="€".*string.(Int.(round.(new_price.*1000))), offset=tbl.off_r)

fig
```

```{code-cell}
:tags: [remove-input]
using Printf
@printf "Revenue (last year): %i \n" sum(price.*cons.*1000000)
@printf "Revenue (this year): %i" sum(new_price.*new_cons.*1000000)
```

````{admonition} Is this solution a global optimum?
:class: dropdown, warning

To answer this question, we need to verify whether the problem is convex. As the constraints are all linear, the answer to whether the problem is convex lies with analysing the objective function. It turns out that, in its current form, the objective function is a **convex function that is being maximised**, and as such, in principal, it may seem as a nonconvex problem.

However, the problem can be reformulated into an **equivalent** convex version. Here, equivalence means that once solved, but problems return the same optimal solution and objective value. To obtain this equivalent convex formulation, we can use the equality constraints which essentially state that the variables $x_i$ can be written as a function of $p_i$. 

Performing the appropriate substitutions, we obtain the equivalent model

```{math}
\maxi &\sum -6492p_m^2 - 1200 p_B^2 - 220 p_{c1}^2 - 34p_{c2}^2 + \\
& 53p_{c1}p_{c2} + 6748p_m + 1184p_b + 420p_{c1} + 70 p_{c2} \\
\st & 260p_m + 960 p_b + 70.25 p_{c1} - 0.6 p_{c2} \geq 782 \\
& 584 p_m + 24 p_b + 55.2 p_{c1} + 5.8 p_{c2} \geq 782 \\
& 4.82 p_m + 0.32 p_b + 0.21 p_{c1} + 0.07 p_{c2} \geq 35 \\
& p_m \leq 1.039 \\ 
& p_b \leq 0.987 \\
& p_{c1} -26 p_{c2} \leq 420 \\
&-27 p_{c1} + 34 p_{c2}\leq 70.
```

The constraints are still linear, but the objective function now can be shown to be concave, yielding a convex problem. To see that, notice that the matrix is given by $Q$

```{math}
Q = \begin{bmatrix} -6492 & & & \\
                      & -1200 & & \\
                      & & -220 & 53/2& \\
                      & & 53/2 & -34
\end{bmatrix}  
```
Calculating its eigenvalues, we can see that they are all negative, implying that $Q$ is negative semi-definite and, as such, yields a concave quadratic function. Therefore, this problem is convex.
<!-- 
```{code-cell}
:tags: [remove-input]

using LinearAlgebra

A = [-6492 0 0 0; 
     0 -1200 0 0;  
     0 0  -220 53/2;
     0 0  53/2 -34]

eigenvalues, eigenvectors = eigen(A)
eigenvalues
``` -->

The existence of a convex equivalent to out problem means that the solution obtained previously is was a global optimal in the first place.

````