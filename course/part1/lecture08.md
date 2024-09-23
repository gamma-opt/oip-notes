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

# Lecture 8 - Modelling integer decisions

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
print("Profit: ", objective_value(m))
```


## Modelling true/false statements using binary variables

One particular type of integer decision variables considerably augment our modelling capabilites. Specifically, binary variables, i.e., $x \in \{0,1\}$ are useful for modelling on/off or true/false decisions, which often play central roles in modelling real-world problems.

More generally, binary variables are well-suited to the expression of logical statements.
Some examples are:
- If we manufacture product A, we must also manufacture product B or at least one of products C and D.
- No more than five of the ingredients in this class may be included in the blend.
- Either operation A must be finished before operation B starts or vice versa.

These statements can be formulated in propositional logic using _connectives_, such as $\land$ (and), $\lor$ (or), $\implies$ (implies) and $\neg$ (not).
We can formulate these expressions into constraint equations as follows.
Suppose $X_i$ stands for the proposition $\delta_i=1$, where $\delta_i$ are binary variables.
Then
```{math}
X_1\lor X_2 &\text{ is equivalent to } \delta_1+\delta_2\geq 1, \\
X_1\land X_2 &\text{ is equivalent to } \delta_1=1,\delta_2=1 \text{ or }\delta_1\delta_2=1, \\
\neg X_1 &\text{ is equivalent to } \delta_1=0, \\
X_1\implies X_2 &\text{ is equivalent to } \delta_1-\delta_2\leq 0.
```

Let us give a couple of examples of some modelling capabilities possible because of binary variables.

### Modelling fixed costs using big-M constraints

Let $p$ and $F$ be scalars. Assume that our cost function $f(x)$ is composed not only of a variable cost, say $px$, but also a fixed cost $F$ that must be incurred only if $x > 0$. More precisely:

```{math}
f(x) = \begin{cases} p x + F, \text{ if } x > 0 \\ 0, \text{ if } x = 0.\end{cases}
```

We want to minimise $f(x)$ such that $x \in X$. In order to represent its behaviour correctly we require an additional binary variable. Let $y \in \braces{0,1}$ be this variable. Then, minimising $f(x)$ is equivalent to minimising the following optimisation problem:

```{math}
\mini_{x,y} & px  + Fy \\
\st & x \le My \\
& x \in X \\
& y \in \{0,1\},
```
where $M$ is sufficiently large constant, often referred to as a *big M*. Notice how the constraint plays a role in guaranteeing that the objective function behaves as we expect. If $x=0$, the minimisation naturally *pushes* $y$ to be zero, as it would otherwise be suboptimal to pay $F$ (by setting $y=1$). Analogously, for any $x > 0 $, $y$ must be set to $1$ in order to satisfy the constraint $x\leq My$, which automatically incurs the cost $F$ in the objective function. 

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
print("Profit: ", objective_value(m))
```

Previously, the optimal solution produced as many tables as possible and made a single chair with leftover materials.
Here, we observe that the high startup costs for table production is sufficient to make the same strategy suboptimal, leading to a focus on chairs instead.

### Modelling choices under constraints

More generally to the above capabilities, binary variables provide a mechanism to model making choices and incorporate restrictions to the process.
In our carpenting example, we are already making a decision between one of four possibilities:
- purchase no tools.
- purchase both tools,
- purchase the chair tool only, and
- purchase the table tool only.

To give a more complicated example, suppose that there are two different table-making tools available on the market.
They differ in terms of costs, time efficiency and resource utilisation.
The additional parameters describing this is summarised in the table below.

```{list-table} Additional problem parameters
:name: 
* - Cost of table tool 1
  - 5000\$
* - Cost of table tool 2
  - 8700\$
* - Time needed per table using tool 1
  - 3h
* - Time needed per table using tool 2
  - 2h
* - Wood needed per table using tool 1
  - 7 units
* - Wood needed per table using tool 2
  - 5 units
```

How should we model this?
One idea is to continue what we were doing before and have an indicator variable for each tool: we already had $y_c$ for the chair tool, and we can consider $y_t^1$ and $y_t^2$ for the two table tools.
With a new variable in hand, we need to determine how this affects our constraints.
For example, we want the big M constraint to be loose on $x_t$ if we have either tool,
which would mean changing it into
```{math}
x_t \leq M(y_t^1+y_t^2).
```

Notice that there is no constraint preventing us from purchasing both table tools.
What does this mean, especially when both tools have different resource usage?
In our example, tool 2 is strictly better then 1, albeit more expensive, but what if they had comparable costs and efficiency, like one tool using less wood and the other less time?
To model this accurately, we would need to start keeping track of how many tables are produced with each tool.

In this example however, we don't necessarily need this additional complexity.
It may be reasonable to assume that we wouldn't want to purchase both table tools and only one would be sufficient.
This way, we would only have to "activate" the correct constraint using big M and solve the above problem.
In order to restrict which tool is purchased, we impose an _exclusive-OR_ condition:
```{math}
:label: exclusive_or
y_t^1+y_t^2 = 1.
```
This would ensure that one and only 1 of the indicator variables would be active, and thus we could control the resource utilisation constraints with
```{math}
:label: resource_utilisation
&3x_t + 5x_c \leq 40 + M(1 - y_t^1)\\
&7x_t + 4x_c \leq 60 + M(1 - y_t^1)\\
&2x_t + 5x_c \leq 40 + M(1 - y_t^2)\\
&5x_t + 4x_c \leq 60 + M(1 - y_t^2).
```
Here, if for example we purchased the first tool, we have $y_t^1=1$, which nullifies the big M, imposing the actual resource constraint.
At the same time, since $y_t^2$ must be zero, the latter two constraints have the big M, leading to the constraints being satisfied trivially, rendering them insignificant for the model.

Equation {eq}`exclusive_or` solves our resource utilisation constraint problems, however, it actually is still flawed.
Since it is an equality, it forces a table tool to be purchased, even when it may be more advantageous to focus solely on chair production.
Thus we should replace it with the inequality
```{math}
y_t^1+y_t^2 \leq 1
```
which allows both variables to be zero, meaning no table tool is purchased.
However, doing so introduces yet another problem: if we don't purchase any table tools, all the resource constraints in Equation {eq}`resource_utilisation` become trivially satisfied.

Let's take a step back and consider what we are trying to do here.
There are 3 tools, each requiring a binary decision of whether we purchase them or not.
This gives a total of $2^3=8$ possible conclusions.
The chair tool part of our model is working properly and is not being influenced by the decisions about table tools, so we can limit our attention to the remaining $2^2=4$ scenarios.

The problems we have experienced above is due to representing these 4 outcome using only two variables $y_t^1$ and $y_t^2$; making sure all possible valuations of them works well with every constraint has not been straightforward.
An alternative approach we can do is to increase the number of variables.
By assigning different outcomes their own variables, we can be assured that constraints we write for each one of them need to depend only in the relevant variable.

More specifically, suppose that $y_t^{01}, y_t^{10}$ and $y_t^{00}$ represent purchasing the first tool, second tool, and neither respectively.
These are mutually exclusive events, so we need to ensure picking only one of them:
```{math}
y_t^{10} + y_t^{01} + y_t^{00} = 1
```

Then we need to make sure resource utilisation works as expected:
```{math}
&3x_t + 5x_c \leq 40 + M(1 - y_t^{01} - y_t^{00})\\
&7x_t + 4x_c \leq 60 + M(1 - y_t^{01} - y_t^{00})\\
&2x_t + 5x_c \leq 40 + M(1 - y_t^{10} - y_t^{00})\\
&5x_t + 4x_c \leq 60 + M(1 - y_t^{10} - y_t^{00}).
```
Here, the addition of $-y_t^{00}$ ensures that if no table tools are purchased, the M is still nullified, so that all constraints are active.
Since in this scenario we know $x_t$ must be 0, the chair constraints remain active in the model while the table constraints are ignored.

```{admonition} What about $y_t^{11}$?
:class: note, dropdown
Why not include the fourth possibility of purchasing both tools in a $y_t^{11}$ variable?
This goes back to the problem of model complexity: we would need to keep track of tables produced by different tools and write our constraints accordingly. This is not impossible, but in this case unnecessary, especially since purchasing the second tool only is strictly better than purchasing both tools.

As the aphorism goes: All models are wrong (or in this case incomplete), but some are useful.
```

The updated and corrected carpenter's model becomes

```{math}
\begin{align}
\text{maximise}_{x_t,x_c} \ &1000x_t + 500x_c - 5000y_t^{01} - 8700y_t^{10} - 600y_c\\
\text{subject to: } 
&3x_t + 5x_c \leq 40 + M(1 - y_t^{01} - y_t^{00})\\
&7x_t + 4x_c \leq 60 + M(1 - y_t^{01} - y_t^{00})\\
&2x_t + 5x_c \leq 40 + M(1 - y_t^{10} - y_t^{00})\\
&5x_t + 4x_c \leq 60 + M(1 - y_t^{10} - y_t^{00})\\
&y_t^{01} + y_t^{10} + y_t^{00} = 1 \\
& x_t \le M(y_t^{01} + y_t^{10})\\
& x_c \le My_c \\
&x_t, x_c \geq 0 \\
&y_t^{01}, y_t^{10}, y_t^{00}, y_c \in \{0,1\}.
\end{align}
```

and the solution we get is

```{code-cell}
m = Model(HiGHS.Optimizer)

M = 100

@variable(m, x_t >= 0, Int)
@variable(m, x_c >= 0, Int)
@variable(m, y_t01, Bin)
@variable(m, y_t10, Bin)
@variable(m, y_t00, Bin)
@variable(m, y_c, Bin)

@objective(m, Max, 1000*x_t + 500*x_c - 5000*y_t01 - 8700*y_t10 - 600*y_c)

@constraint(m, 3*x_t + 5*x_c <= 40 + M*(1-y_t01 - y_t00))
@constraint(m, 7*x_t + 4*x_c <= 60 + M*(1-y_t01 - y_t00))
@constraint(m, 2*x_t + 5*x_c <= 40 + M*(1-y_t10 - y_t00))
@constraint(m, 5*x_t + 4*x_c <= 60 + M*(1-y_t10 - y_t00))
@constraint(m, x_t <= M*(y_t01+y_t10))
@constraint(m, x_c <= M*y_c)
@constraint(m, y_t01 + y_t10 + y_t00 == 1)

optimize!(m)

print("\nSOLUTION!!!\n")
print("\nTotal of tables: ", value(x_t), "\nTotal of chairs: ", value(x_c), "\n")
print("Profit: ", objective_value(m))
```

Turns out the table tools are both too expensive to warrant their purchase.
More importantly, this section highlights the importance of being careful with modifying your model, even a small change to an individual constraint may have implications beyond itself.

````{note}
The above exclusive-OR and regular-OR constraints can be generalized to accept a certain number of values.
For example, to pick $c$ states out of $N$ could be modeled with
```{math}
\sum_{i \in [N]} y_i = c.
```
Similarly, picking _up to_ $c$ states would be
```{math}
\sum_{i \in [N]} y_i \leq c.
```
In either case however, one must be careful and ensure that these relaxations do not interfere with the rest of the model like what we discussed above.
````
