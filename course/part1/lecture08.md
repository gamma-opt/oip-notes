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
&4x_t + 7x_c \leq 60\\
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

Another tool we will need in our modelling toolkit are _binary variables_, which allow us to formulate "yes or no" decisions among other uses.


## Logical conditionals: Big $M$

Sometimes, one may want to model conditions of the form "if A, then B".
For example, consider a problem where a firm is considering opening factories at different locations $i$, in order to maximize the total amount of production $\sum x_i$.
Here, we need $x_i=0$ if location $i$ is not selected as for a facility, but $x_i\geq 0$ otherwise.
Say $y_i$ is a binary variable that indicates if the location is selected or not, then we can write the above as the logical statement

```{math}
(y_i \land x_i\geq 0) \lor (\neg y_i \land x_i=0)
```

To write this in a way an optimization solver will understand, we can reformulate it to the following:

```{math}
x_i &\leq M y_i \\
x_i &\geq 0 \\
y_i &\in \{0,1\}
```

where $M$ is a sufficiently big number, hence the name "Big $M$".
What exactly is happening here?
Suppose $y_i=0$.
This means that there won't be a factory at this location, and thus there cannot be any production.
The constraint $x_i\leq M y_i$ enforces that by becoming $x_i\leq 0$ (in conjunction with $x_i\geq 0$).

Now suppose $y_i=1$.
Here, production should be permissible.
For $M$ that is big enough, such as an inherently unrealistic amount of production, then the constraint functionally becomes $x_i\leq \infty$, becoming irrelevant for the determination of the optimal value of $x_i$.
