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

However, if one were to consider computational aspects, then there are several important issues to take into account. The reason why mathematical programming modellers go beyond their means to obtain (mixed-integer) linear programming models is because the simplex method, the algorithm underlying the solution of such problems is a practical success. Since its conception in the 50's, it has seem a myriad of developments that has turned it into a robust and reliable algorithm for solving mathematical programming problems.

The issue is that, with the exception of a few special cases, if there is any nonlinearity in the model, we cannot use simplex-method based algorithms, and departing from them can be scary in many ways. For problems with continuous variables only, the alternative is to use a interior point (or barrier) method. These methods, developed in the 90's based on much earlier results, have seen significant developments in terms of their implementation, and have become, in many cases, almost as common as the algorithm of choice to solve continuous mathematical programming models, including strictly nonlinear. We will discuss their differences in detail later on in the course.

For now, what you need to keep in mind is this: the line that separates mathematical programming models that can be comfortably treated and those that cannot has nothing to do with nonlinearity, but rather, with convexity. Interior point methods (and the simplex method too) are first-order methods, meaning that they are engineered to converge to points where first-order optimality conditions hold. But these can only be guaranteed to be optimal points if the problem at hand is convex; otherwise, nothing stronger can be said about the solution found without more specialised way to search for the feasible region.

Add a remark about mixed integer problems, who are nonconvex problems whose linear relaxation is convex. That is sort of the reason why whether they are tractable sometimes, but sometimes they suck. It is about how much the "nonconvex part" dominates the convex part (or how strong or weak the relaxation is -- too much?)


## Convex problems

### Objective function as a convex function

We say a problem is convex if...

### Constraints as convex sets


## Examples of convex problems

- Fitting a regression with regularisation
- Quadratic problem from the book of models

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