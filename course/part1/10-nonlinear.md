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
