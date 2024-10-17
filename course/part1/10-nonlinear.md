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

We now turn our focus to the assumption of linearity we have been carrying so far. Earlier, we have stated that we would stick with models that can be stated as linear functions, both in the objective function and in the constraints. The reason for that is purely algorithmic, and there is nothing that, from a conceptual point, prevents the use of nonlinear functions.

In general, by assuming linearity in our optimisation models as we have been doing so far, we are assuming that:

- Returns and/ or costs are constant and not affected by scale;
- The use of resources by an activity is proportional to the level of activity;
- The total use of resource by a number of activities is the sum of the uses by the individual activity.

Clearly, these are simplifying but still reasonably good approximations in many settings. However there are a couple of settings where one cannot simply ignore how quantities and properties interact with each other, which is exactly what leads us to dealing with nonlinear models.

If one were to consider computational aspects, then there are several important issues to take into account. The reason why mathematical programming modellers go beyond their means to obtain (mixed-integer) linear programming models is because the simplex method, the algorithm underlying the solution of such problems is a practical success. Since its conception in the 50's, it has seem a myriad of developments that has turned it into a robust and reliable algorithm for solving mathematical programming problems.

The issue is that, with the exception of a few special cases, if there is any nonlinearity in the model, we cannot use simplex-method based algorithms, and departing from them can be scary in many ways. For problems with continuous variables only, the alternative is to use a interior point (or barrier) method. These methods, developed in the 90's based on much earlier results, have seen significant developments in terms of their implementation, and have become, in many cases, almost as common as the algorithm of choice to solve continuous mathematical programming models, including strictly nonlinear. We will discuss their differences in detail later on in the course.

For now, what you need to keep in mind is this: the barrier that separates mathematical programming models that can be comfortably treated and those that cannot has nothing to do with nonlinearity, but rather, with convexity. Interior point methods (and the simplex method too) are first-order methods, meaning that they are engineered to converge to points where first-order optimality conditions hold. But these can only be guaranteed to be optimal points if the problem at hand is convex; otherwise, nothing stronger can be said about the solution found without more specialised way to search for the feasible region.

%Add a remark about mixed integer problems, who are nonconvex problems whose linear relaxation is convex. That is sort of the reason why whether they are tractable sometimes, but sometimes they suck. It is about how much the "nonconvex part" dominates the convex part (or how strong or weak the relaxation is -- too much?)


## Convex problems

We say that an optimisation problem is a convex if it has

- A convex objective function to be minimised or a concave objective function to be maximised;
- A convex feasibility set.

More formally, let our optimisation problem be defined in the following general way:

```{math}
:label: opt-problem
\begin{equation}
  \begin{aligned} 
  \mini & f(x) \\
  \st   & g(x) \le 0 \\
        & h(x) = 0.
  \end{aligned}      
\end{equation}
```

```{prf:definition}
The mathematical optimisation problem {eq}`opt-problem` is a convex optimisation problem if and only if:
  1. $f(x)$ is a convex function;
  2. $g(x)$ is a convex function;
  3. $h(x)$ is a linear (or affine) function.
```

We discussed the notion of convexity in Lecture 1, and concluded that for convex functions, first-order optimality (zero-gradient) conditions are sufficient to certify the optimality of a candidate solution. It turns out that, if the subdomain (in in our case, the feasibility set) is a convex set, a generalisation of these first-order conditions (known as Karush-Kuhn-Tucker, or KKT conditions) exist and are also necessary and sufficient for optimality. Interior point methods, the flagship method for nonlinear optimisation problems, are engineered to search for points that satisfy KKT conditions.

```{warning}
Interior point methods, or any other optimisation methods vcan be very well used to solve nonconvex optimisation problems. The issue is that, for these problems, the KKT conditions are necessary (i.e., they have to hold) but not sufficient to certificate optimality of the solution found. It is up to the user to know whether that solution can be certified as a global optimal solution.  
```

```{note}
Linear functions are convex, and thus, linear programming problems are convex problems. That is why both interior point method and the simplex method, which is also a zero-gradient solution seeking method, can be safely employed.

```

### Objective function as a convex function

There are few functions that are convex functions and frequently appear as objective functions in mathematical programmes. Next, we list a few of them.

#### Quadratic functions

Quadratic functions are functions that involve the multiplication of two decision variables. A typical example is illustrated in {ref}`p1l10:agricultural_pricing` below, where a price, which is dependent of the quantity produced, is multiplied by the actual quantity produced. Another common setting is when some sort of _regularisation_ is imposed to decision variables, which is typically achieved by minimising their squared value.

The general form of a quadratic function can be stated as

```{math}
f(x) = c^\top x + x^\top Qx,
```

where $x$ represents our decision variables (a $n$-dimensional vector assuming we have $n$ decision variables), $c$ is an $n$-dimensional vector of parameters and $Q$ is the matrix of the quadratic form.

```{note}
The matrix of the quadratic form $ax_1 + bx_1x_2 + cx_2$ is given by: {math}```\begin{equation} \begin{bmatrix} a & \frac{b}{2} \\ \frac{b}{2} c \end{bmatrix} \end{equation}```. This generalises for $n$ dimensions: the main diagonal has the coefficient of the quadratic terms and for the $q_{ij}x_ix_j$ we have $q_{ij} / 2$ in= the $i^\text{th}$ row and $j^\text{th}$ column as well as the $j^\text{th}$ row and $i^\text{th}$ column.
```

The quadratic function $f$ is convex depending on the matrix $Q$. The technical term is that $Q$ needs to be positive semidefinite (PSD), which roughly means that when we multiply $Q$ by a vector $x$, it does not flip the sign of any of the coordinates of $x$. There are many ways one can attest whether the matrix $Q$ is PSD, but perhaps the simpler is to use a linear algebra package to check if its eigenvalues are non-negative (i.e., positive or zero).

#### Polynomials, exponential and logarithms 

More seldom, one may see the need of using other functions that quadratic. Somm other common convex functions include:

- *Powers*: $x^a$ is concave for $ 0 \le a \le 1$ and convex for $a \ge 1$ or $a \le 0$;
- *Exponential*: $e^{ax}$ is convex for any $x \in \reals$;
- *Logarithms:* $\log x$ is concave and $x \log x$ is convex for $x > 0$;
- *Nonnegative weighted sums*: the sum of convex functions, when weighted by non-negative terms is convex. 

There are a few other functions that are convex. Also, there are a few operations (such as the non-negative weighted sum) that preserve convexity. Typically, to verify whether a function is convex or not, we must break it into parts and verify whether they are convex functions and if they have been combined by convexity preserving operations.

### Constraints as convex sets

We now focus on the terms $g$ and $h$. Whenever we impose an image to a function (or a set of them, via an inequality), we are implicitly defining a set. For example, when we state that $h(x) = 0$, this creates a set of all $x$ that when inputted in $h$ return zero; likewise $g(x) \le 0$ represents the set of all solutions $x$ that when inputted to $g$, return a negative number or zero.

We can infer the convexity of these set of solutions by analysing the convexity of the functions:

- For equality constraints, the only way in which $h(x)=0$ can generate a convex set is if $h$ is linear;
- For inequalities, the set of constraints will be convex if $g(x)$ is a convex function in $g(x) \le 0$.

```{note}
Remember that if $g$ is convex, $-g$ is concave. Thus we can infer that, by multiplying $g(x) \le 0$ by -1, we see that for greater-or-equal-than constraints, we obtain convex sets whenever the function is concave. 
```

## Examples of convex problems

### Classification as an optimisation problem

One of the most classical problems in machine learning is that of binary classification, where given some data that is partitioned into two classes, the goal is to obtain a function $f$ that separates the partitions.
Specifically, we will now focus on linear classification, where we seek an affine function $f(x)=a^\top x - b$, or equivalently the parameters $a$ and $b$, that gives us an appropriate classifier, i.e.

```{math}
f(x_i) = \begin{cases} 
1&\text{if } a^\top x_i - b > 0 \\
-1&\text{if } a^\top x_i - b < 0 \\
\end{cases}
```

For example, our problem may be of detecting spam in emails, where we'd like to distinguish between regular ones and emails that can be ignored.
Our features then may be the word count, count of repeated word stems and/or others.

Suppose we have the following data we would like to classify, based on two features and with the colors indicating the true classification $y_i, i\in I$.

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
    xlabel="feat₁", 
    ylabel="feat₂",
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

But arguably this one is not the best classifier.
Suppose we had another datapoint at $(5,4)$. Intuitively, we may guess that this point belongs to the orange class, since it is much closer there.
However, our line classifies this point otherwise.

```{code-cell}
:tags: [remove-input]
temp = scatter!(ax, [(5,4)], color=DEF_COLORS[2], marker=:diamond)
fig
```

To make our classifier more _robust_, we may want to pick the _maximum-margin_ line, which maximises the distance to the nearest datapoints in either classes.
The width of the margin is $\frac{2}{\|a\|}$ ([see why here](#margin_width)), thus maximizing the width corresponds to minimizing $\|a\|=\sqrt{a_1^2+a_2^2}$, which allows us to formulate this as an optimisation problem:

```{math}
\mini & \|a\|^2 \\
\st & a^\top x_i - b \geq 1, \forall i\in I, \text{ if } y_i = 1\\
& a^\top x_i - b \leq -1, \forall i\in I, \text{ if } y_i = -1.
```

Here, we minimise $\|a\|^2$ instead as a small shortcut, since the minimum won't change by omitting the square root (this property is called _monotonicity_).
The constraints ensure that the points are classified correctly, for example if $y_i=1$ for some $i\in I$, then the point should be above the top margin, i.e. $a^\top x_i-b\geq 1$.
Similarly, if $y_i=-1$, then the point should be below the bottom margin, i.e. $a^\top x_i-b \leq -1$.

This problem is obviously nonlinear: the squared-norm is composed of quadratic terms.
It is in fact a convex problem: the norm is a convex function, and the constraints are affine functions (with changing signs), so are also convex.


```{admonition} Why is the margin width equal to $\frac{2}{\|a\|}$?
:class: note, dropdown
:name: margin_width

A proof is [here](https://youtu.be/_PwhiWxHK8o?t=1020).
```

To solve this programatically, we can create a model as

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

And plot the result on our data, including the margins on either side.

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

Note that in the above, the diamond point we added manually is within the margin because it was not included in the training data.
However, the fact that it is correctly classified by the maximum-margin classifier is testament to the robustness of this method.

(p1l10:agricultural_pricing)=
### Agricultural pricing

This example is from {cite}`williams_model_2013`.

We are consulted by the government of a country to help with pricing their dairy products.
There are four products for us to consider:

- milk,
- butter, and
- two varieties of cheese: Cheese 1 and Cheese 2.

All these products are made directly or indirectly using the country's raw milk production, which is divided into fat and dry matter.
The total yearly availability for the two ingredients are 600 000 tons of fat and 750 000 tons of dry matter.
The compositions of the products in terms of the ingredients are provided in {numref}`agri:composition`.

```{table} Percentage compositions of the products
:name: agri:composition
|          | **Fat** | **Dry matter** | **Water**   |
|:--------:|:-------:|:--------------:|:-----------:|
|   Milk   |    4    |        9       | 87          |
|  Butter  |    80   |        2       | 18          |
| Cheese 1 |    35   |       30       | 35          |
| Cheese 2 |    25   |       40       | 35          |
```

In addition, we are given the _price elasticities_ of demand in {numref}`agri:elasticity`.
The price elasticity of a product is a measure of the sensitivity of the demand for the product to its price and is defined as

```{math}
E = \frac{\text{\% decrease in demand}}{\text{\% increase in price}}.
```

Similarly, the substitution effect between two types of cheese is measured by cross-elasticity of demand.
The cross-elasticity from a product A to product B is given by

```{math}
E_{AB} = \frac{\text{\% decrease in demand for A}}{\text{\% increase in price of B}}.
```

```{table} Elasticity of products
:name: agri:elasticity
| Milk | Butter | Cheese 1 | Cheese 2 | Cheese 1 to Cheese 2 | Cheese 2 to Cheese 1 |
|:----:|:------:|:--------:|:--------:|:--------------------:|:--------------------:|
|  0.4 |   2.7  |    1.1   |    0.4   |          0.1         |          0.4         |
```

Our objective is to maximise the total revenue in terms of price and resultant demand.
However, we are asked to ensure that the new prices are such that last year's total consumption costs would not have increased with them.
To this end, we are also given price and consumption data from last year in {numref}`agri:last_year`.

```{table} Information from last year
:name: agri:last_year
|                                  | Milk | Butter | Cheese 1 | Cheese 2 |
|:--------------------------------:|:----:|:------:|:--------:|:--------:|
| Consumption (1000 tons) | 4820 |   320  |    210   |    70    |
| Price (€/ton)                    | 297  | 720    | 1050     | 815      |
```

#### Solution

Let $p_m, p_b, p_{c1}$ and $p_{c2}$ be the prices of milk, butter, cheese 1 and cheese 2 in €1000 per ton, and $x_m, x_b, x_{c1}$ and $x_{c2}$ be the corresponding quantities in thousands of tons.

Our goal is to maximize profit
```{math}
\maxi \sum p_i x_i.
```
Since both $p_i$ and $x_i$ are variables, this is a nonlinear problem.

We are constrainted by the limited supply of fat and dry matter

```{math}
0.04 x_m + 0.8 x_b + 0.35 x_{c1} + 0.25 x_{c2} \leq 600 \\
0.09 x_m + 0.02 x_b + 0.3 x_{c1} + 0.4 x_{c2} \leq 750.
```

Note that since $x_i$ are in the units 1000 tons, we divide the right hand side to match.
In addition, the consumption costs  of last year should not be larger with the new prices

```{math}
4820 p_m + 320 p_b + 210 p_{c1} + 70 p_{c2} \leq 1939.49.
```

Lastly, we need to relate the quantity variables to the price variables using the elasticity information

```{math}
\newcommand{\dx}[1]{\frac{d#1}{#1}}
\dx{x_m} &= -E_m\dx{p_m}, \\
\dx{x_b} &= -E_b\dx{p_b}, \\
\dx{x_{c1}} &= -E_{c1}\dx{p_{c1}} + E_{c1c2}\dx{p_{c2}}, \\
\dx{x_{c2}} &= -E_{c2}\dx{p_{c2}} + E_{c2c1}\dx{p_{c1}}.
```

These equations are not ideal, solving them will result in non-convex functions in our constraints.
In order to avoid this, we approximate them linearly

```{math}
\newcommand{\lx}[2]{\frac{#1_{#2}-\bar{#1}_{#2}}{\bar{#1}_{#2}}}
\lx{x}{m} &= -E_m\lx{p}{m} \\
\lx{x}{b} &= -E_b\lx{p}{b} \\
\lx{x}{c1} &= -E_{c1}\lx{p}{c1}+E_{c1c2}\lx{p}{c2} \\
\lx{x}{c2} &= -E_{c2}\lx{p}{c2}+E_{c2c1}\lx{p}{c1}
```

where $\bar{x}_m$ and $\bar{p}_m$ are the quantity and price for milk from the last year, and similarly for other variables and products.
As long as $x_i$ and $p_i$ don't differ significantly from $\bar{x}_i$ and $\bar{p}_i$, these approximations should work reasonably well.

% This part is not needed unless we want to make the model seperable (which will require further treatment as well)
%Since all terms except $x$'s and $p$'s are known, we can solve them to obtain quantities we can plug in to the previous equations.
%For example, for milk we can derive
%```{math}
%\lx{x}{m} &= -E_m\lx{p}{m} \\
%\implies x_m &= -E_m\bar{x}_m\lx{p}{m} + \bar{x}_m
%```
%and plug in known values to get
%```{math}
%x_m = -6492 p_m + 6748.
%```
%Doing the same for the remaining products yield
%```{math}
%x_b &= -1200 p_b + 1184 \\
%x_{c1} &= -220 p_{c1} + 26 p_{c2} + 420 \\
%x_{c2} &= -34 p_{c2} + 27 p_{c1} + 70
%```

With that, our full model is

```{math}
\maxi &\sum p_i x_i \\
\st & 0.04 x_m + 0.8 x_b + 0.35 x_{c1} + 0.25 x_{c2} \leq 600 \\
& 0.09 x_m + 0.02 x_b + 0.3 x_{c1} + 0.4 x_{c2} \leq 750 \\
& 4820 p_m + 320 p_b + 210 p_{c1} + 70 p_{c2} \leq 1939.49 \\
& \frac{x_m - 4820}{4820} = -0.4\frac{p_m-0.297}{0.297} \\
& \frac{x_b - 320}{320} = -2.7\frac{p_b-0.72}{0.72} \\
& \frac{x_{c1} - 210}{210} = -1.1\frac{p_{c1}-1.05}{1.05} + 0.1\frac{p_{c2}-0.815}{0.815} \\
& \frac{x_{c2} - 70}{70} = -0.4\frac{p_{c2}-0.815}{0.815} + 0.4\frac{p_{c1}-1.05}{1.05}
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
@variable(model, p[1:4])

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
using Printf
@printf "Revenue (last year): %i \n" sum(price.*cons.*1000000)
@printf "Revenue (this year): %i" sum(new_price.*new_cons.*1000000)
```