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

# Lecture 8 - modelling integer decisions

Next, we focus on extending the types of variables we can consider in our optimisation models. An important type of variable that allows us to more realistic model problems is to consider them as *integer* valued. Essentially, we are constraining such variables to only take values from the set of integer numbers, typically represented by $\mathbb{Z}$.

## Considering integer valued decision variables

Conceptually, this is a somewhat small change in the model formulation, but one with major consequences to how difficult the optimisation model is to solve. Let us return to our example in {numref}`p1l4:first-model`. One point we raised is that the problem was modelled considering that the number of tables and chairs, represented by decision variables $x_t$ and $x_c$ could take fractional values. Now, let us assume that we require the number of tables and chairs to be integer. Thus, we can modify our model formulation as 

```{math}
\begin{align}
\text{maximise}_{x_t,x_c} \ &1000x_t + 500x_c \\
\text{subject to: } &3x_t + 5x_c \leq 40\\
&7x_t + 4x_c \leq 60\\
&x_t, x_c \in \mathbb{Z}_+.
\end{align}
```

```{admonition} Alternative notation for integer-valued variables
:class: note
$x \in \mathbb{Z}_+$ means that $x$ is non-negative and integer valuated. Some references prefer to use the more straightforward notation  "$x \ge 0$ and integer".  
```

Similarly, modelling this require a simple adaptation in the code.

```{code-cell}
using JuMP, HiGHS

m = Model(HiGHS.Optimizer)

@variable(m, x_t >= 0, Int)
@variable(m, x_c >= 0, Int)

@objective(m, Max, 1000*x_t + 500*x_c)

@constraint(m, 3*x_t + 5*x_c <= 40)
@constraint(m, 7*x_t + 4*x_c <= 60)

optimize!(m)

print("\nSOLUTION!!!\n")
print("\nTotal of tables: ", value(x_t), "\nTotal of chairs: ", value(x_c), "\n")
```


## Modelling true/false statements using binary variables

One particular type of integer decision variables considerably augment our modelling capabilites. Specifically, binary variables, i.e., $x \in \{0,1\}$ are useful for modelling on/off or true/false decisions, which often play central roles in modelling real-world problems.

More generally, binary variables are well-suited to the expression of logical statements.
Some examples are:
- If we manufacture product A, we must also manufacture product B or at least one of products C and D.
- No more than five of the ingredients in this class may be included in the blend.
- Either operation A must be finished before operation B starts or vice versa.

These statements can be formulated in propositional logic using _connectives_, such as $\land, \lor, \implies$ and $\neg$.
We can formulate these expressions into constraint equations as follows.
Suppose $X_i$ stands for the proposition $\delta_i=1$, where $\delta_i$ are binary variables.
Then
```{math}
X_1\lor X_2 &\text{ is equivalent to } \delta_1+\delta_2\geq 1, \\
X_1\land X_2 &\text{ is equivalent to } \delta_1=1,\delta_2=1, \\
\neg X_1 &\text{ is equivalent to } \delta_1=0, \\
X_1\implies X_2 &\text{ is equivalent to } \delta_1-\delta_2\leq 0.
```

Let us give a couple of examples of some modelling capabilities possible because of binary variables.

### Modelling fixed costs using big-M constraints

Let $p$ and $F$ be scalars. Assume that our cost function $f(x)$ is composed not only of a variable cost, say $px$, but also a fixed cost $F$ that must be incurred only if $x > 0$. More precisely:

```{math}
f(x) = \begin{cases} p^\top x + F, \text{ if } x > 0 \\ 0, \text{ if } x = 0.\end{cases}
```

We want to minimise $f(x)$ such that $x \in X$. In order to represent its behaviour correctly we require an additional binary variable. Let $y \in \braces{0,1}$ be this variable. Then, minimising $f(x)$ is equivalent to minimising the following optimisation problem:

```{math}
\mini_{x,y} & px  + Fy \\
\st & x \le My \\
& x \in X \\
& y \in \{0,1\},
```
where $M$ is sufficiently large constant, often referred to as a *big M*. Notice how the constraint plays a role in guaranteeing that the objective function behaves as we expect. If $x=0$, the minimisation naturally *pushes* $y$ to be zero, as it would otherwise be suboptimal to pay $F$ (by setting $y=1$). Analogously, for any $x > 0 $, $y$ must be set to $1$, which automatically incurs the cost $F$ in the objective function. 

```{admonition} Beware of big M constants
:class: warning
Big M constants must have their value carefully set. Set too small, they may artificially constraint the problem; set too large, they may compromise computational performance.
```

Let's revisit the carpenter's problem from {numref}`p1l4:first-model` as an example. Assume that in other to start producing tables and chairs, the carpenter must invest in acquiring tools. The tools required for making tables cost $5000$ and those for making chairs cost $600$. How can we modify the original model to consider these new requirements?

For that, we must define two additional binary variables, namely $y_t$ and $y_c$ that assume value 1 if the tools for making chairs and tables are acquired. Then, original model can be modified as follows

```{math}
\begin{align}
  \text{maximise}_{x_t,x_c} \ &1000x_t + 500x_c - 5000y_t - 600y_c\\
  \text{subject to: } 
  &3x_t + 5x_c \leq 40\\
  &7x_t + 4x_c \leq 60\\
  & x_t \le My_t \\
  & x_c \le My_c \\
  &x_t, x_c \geq 0 \\
  &y_t, y_c \in \{0,1\}.
\end{align}
```

We can implement this similarly as before.

```{code-cell}
m = Model(HiGHS.Optimizer)

M = 100

@variable(m, x_t >= 0, Int)
@variable(m, x_c >= 0, Int)
@variable(m, y_t, Bin)
@variable(m, y_c, Bin)

@objective(m, Max, 1000*x_t + 500*x_c - 5000*y_t - 600*y_c)

@constraint(m, 3*x_t + 5*x_c <= 40)
@constraint(m, 7*x_t + 4*x_c <= 60)
@constraint(m, x_t <= M*y_t)
@constraint(m, x_c <= M*y_c)

optimize!(m)

print("\nSOLUTION!!!\n")
print("\nTotal of tables: ", value(x_t), "\nTotal of chairs: ", value(x_c), "\n")
```

Previously, the optimal solution produced as many tables as possible and made a single chair with leftover materials.
Here, we observe that the high startup costs for table production is sufficient to make the same strategy suboptimal, leading to a focus on chairs instead.

### Modelling disjunctions

Another useful modelling capability that binary variables allows it to model *disjunctions*, i.e., constraints that are mutually exclusive between one another regarding their satisfaction.

Suppose we have two constraints , say $a_1^\top x \le b_1$ and $a_2^\top x \le b_2$ such that only one of them must hold, but not both simultaneously. To model that, we once again need a binary variable $y \in \{0,1\}$ that will take value $y=1$ if one of the constraints, say $a_1^\top x \le b_1$, is enforced and 0 if the other is enforced. Notice that this implies that they are related by an exclusive or (XOR) condition. This can be modelled by the following set of constraints

% \top doesn't render well without a line above
```{math}
\\
a_1^\top x \le b_1 + M(1 - y) \\
a_2^\top x \le b_2 + My,
```

where $M$ is once again a big-M constant. Notice that the role that the constant $M$ plays is different than before. Now, when the $M$ is active (e.g., when $y = 0$ in the first constraint) the constraint becomes *loose*, meaning that the left-hand side is trivially less or equal than $M$, assuming $M$ is appropriately large.

Returning to the carpenter's example, let us assume that we have two options of tools for making tables, form which the carpenter has to choose one and only one. They differ in terms of costs and how efficient they are in terms of resource utilisation. The options are summarised in the table below

```{list-table} Additional problem parameters
:name: 
* - Cost of table tool 1
  - 5000\$
* - Cost of table tool 2
  - 7000\$
* - Time needed per table using tool 1
  - 3h
* - Time needed per table using tool 2
  - 2h
* - Wood needed per table using tool 1
  - 7 units
* - Wood needed per table using tool 2
  - 5 units
```

The updated carpenter's model becomes

```{math}
\begin{align}
\text{maximise}_{x_t,x_c} \ &1000x_t + 500x_c - 5000y_t^1 - 7000y_t^2 - 600y_c\\
\text{subject to: } 
&3x_t + 5x_c \leq 40 + M(1 - y_t^1)\\
&7x_t + 4x_c \leq 60 + M(1 - y_t^1)\\
&2x_t + 5x_c \leq 40 + M(1 - y_t^2)\\
&5x_t + 4x_c \leq 60 + M(1 - y_t^2)\\
&y_t^1 + y_t^2 = 1 \\
& x_t \le M(y_t^1 + y_t^2)\\
& x_c \le My_c \\
&x_t, x_c \geq 0 \\
&y_t^1, y_t^2, y_c \in \{0,1\}.
\end{align}
```

```{code-cell}
m = Model(HiGHS.Optimizer)

M = 100

@variable(m, x_t >= 0, Int)
@variable(m, x_c >= 0, Int)
@variable(m, y_t1, Bin)
@variable(m, y_t2, Bin)
@variable(m, y_c, Bin)

@objective(m, Max, 1000*x_t + 500*x_c - 5000*y_t1 - 7000*y_t2 - 600*y_c)

@constraint(m, 3*x_t + 5*x_c <= 40 + M*(1-y_t1))
@constraint(m, 7*x_t + 4*x_c <= 60 + M*(1-y_t1))
@constraint(m, 2*x_t + 5*x_c <= 40 + M*(1-y_t2))
@constraint(m, 5*x_t + 4*x_c <= 60 + M*(1-y_t2))
@constraint(m, x_t <= M*(y_t1+y_t2))
@constraint(m, x_c <= M*y_c)
@constraint(m, y_t1 + y_t2 == 1)

optimize!(m)

print("\nSOLUTION!!!\n")
print("\nTotal of tables: ", value(x_t), "\nTotal of chairs: ", value(x_c), "\n")
print("Debug", value(y_t1), value(y_t2), value(y_c))
```

% Current formulation always buys a table tool, even when not making tables

With the improved table tool, more tables can be produced, which shifts the scales back to a table-focused production.

Notice that in this case we used two variables, $y_t^1$ and $y_t^2$, instead of only one. Clearly, they are equivalent, but the latter require us to explicitly state $y_t^1 + y_t^2 = 1$ since it requires an exclusive or condition. This is indeed how we would generalise this idea to consider multiple disjunctive constraints. More formally, if we have an arbitrary number of disjunctions $a_i^\top x \le b_i$ with $i \in [N]$, we can model then as

```{math}
\begin{align}
& a_i^\top x \le b_i + M(1-y_i) \\ 
& \sum_{i \in [N]} y_i = 1. 
\end{align}
```
