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

#TODO: Add the carpenters problem with integer variables.

## Modelling true/false statements using binary variables

