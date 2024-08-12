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

# Lecture 4

In this lecture we will discuss the idea of using the notion of *functions* and their domains to represent problems in a form that can be expressed as mathematical optimisation problems. In other words, we will develop a language such that we can pose real-world problems as the mathematical statement

```{math}
:label: eq-optimisation_problem
\mini~f(x) ~\st x \in X.
```

In the above, $x$ represents a $n$-component real-valued vector (i.e., $x \in \reals^n$), $\mathop{\text{s.t.}}$ stands for "such that" or "subject to", and $X$ represents the subset of the domain of $f(x)$ that is of our interest (that is, $X \subset \reals$). For the time being, we will focus on how to obtain a *mathematical representation* of the problem at hand that then can be *optimised*. In our context, to optimise a problem means finding a solution $x \in X$ at which $f(x)$ attains its minimum value. Later, we will touch upon how such representations can be used by specialised algorithms to find optimal solutions.

```{note}
We will assume *minimisation* as a reference, but clearly, maximisation can be used in our derivations interchangeably.
```

## Optimisation modelling

%- Explain how functions can represent real-world interactions between inputs and outputs

The modelling of real-world problems as optimisation problems is, in general, using *mathematical programming*. Mathematical programming is in its core, a language to pose problems as {eq}`eq-optimisation_problem`, which in turn can be optimised taking into account properties that $f$ and $X$ possess.

A mathematical programming model comprises four key ingredients:

1. **Parameters**, which represent the input data and information that defines the problem statement. These are typically elements in the problem that are beyond our control, such as costs, revenues, efficiency rates, limits, and so forth.  
2. **Decision variables** $x$, which represent the elements of the problem that we control. These can represent production amounts, flows in a network, dimensions of a structure, or any other element that is part of the decisions we wish to make.
3. **Objective function** $f$ represents a measure of performance associated with a candidate solution $x$. Examples include maximizing profits, utility, return on investment, or satisfaction, and minimize costs, redundancy, waste, or risk.
4. **Constraints** $X$, which express the rules or conditions that a solution must satisfy for it to be considered valid.

Notice that these are presented in a deliberate order. As a rule of thumb, whenever we start the process of modelling a problem, we will follow this list in this particular order.

As the name suggests, the objective function is the function that describes our objective, which is to maximise or minimise some quantity that represents a measurement of performance. Thus, in mathematical programming, objective functions always comprise an objective (maximise or minimise) and a function $f$. For the majority of our models, the function to be optimised will be defined as $f : X \subseteq \reals^n \to \reals$.

## Defining domains by posing constraints

%- Show that functions can be also be used to state logical relations of the problem we are modelling
%- The relation can be =, >=, or <=
%- Show that they generate a set that can be used as a subdomain

One important concept in mathematical programming is how can we define sets $X$ using functions. This is possible by relating functions with particular levels of its codomain by means of (in)equalities. In particular, suppose we are given a functions $g(x) : \reals^n \to \reals$ such that $g(x) \le 0 $ describes a relationship between decisions that make them feasible to be implemented.  Then, we have that

```{math}
    X = \braces{x \in \reals^n : g(x) \le 0},
```

or $X$ is the set of all values for $x$ that satisfy $g(x) \le 0$. Notice that this idea allows us express the set of all possible (or feasible) solutions by means of posing functions that represent relationships between decision variables.

A relationship between decision variables in the form of $g(x) \le 0 $ is called a *constraint*. Most if not all optimisation problems involve optimising an objective with respect to multiple *constraints*, which specify the restrictions that a solution must obey to be considered feasible. To clarify this concept, let's use an example. Imagine a factory that produces a given product. Logically, the factory cannot produce an infinite quantity of product, even if their goal is to maximize production. Let us represent our production amount by $x$ and let's say that our factory's production capacity is a total of $C$ units. Then, the constraint $x \le C$ defines the set of feasible solutions. Notice that in this example $g(x) = x - C$ and, thus, $X = \braces{x \in \reals : x - C \le 0}$.

Constraints can be posed either as equalities or inequalities, depending on the nature of the restriction one must impose. For example, suppose that our factory can produce two variants of the same product, say $x$ and $y$, and that the combined amount produced $x + y$ must meet the demand level $D$. This can be stated as the equality constraint $x + y = D$. Whether a constraint must be posed as an equality or inequality largely depends on the business rule being stated and modelling decisions, which we will discuss in more detail in a later lecture.

One additional point that must be made is that, since solutions have to satisfy all business rules simultaneously for it to be considered feasible, we say that the set of feasible solutions is formed by the *intersection* of the sets that each constraint forms. For our running example, let $X_1 = \braces{x \in \reals : x - C \le 0}$ and $X_2 = \braces{[x,y] \in \reals^2 : x + y - D = 0}$. Then, $X = X_1 \cap X_2$, or $X = \braces{[x,y]\in \reals^2 : x - C \le 0, x + y - D = 0}$.

```{note}
It is perfectly fine to write $X = \braces{[x,y]\in \reals^2 : x \le C, x + y = D}$. The use of the right-hand side terms as zero is only to stress the connection to the general form presented in {eq}`eq-optimisation_problem`. In fact, there is no particular rule on which terms need to be on each side of the (in)equality. 

```

## Our first mathematical programming model

Let us consider a first example. A carpenter wants to plan his production of tables and chairs such that his income is maximised. Every table produced is sold for 1000\$ and every chair produced is sold for 500\$.

To produce one table, the carpenter needs 3h of work and 7 units of wood. To produce one chair, the carpenter requires 5h of work and 4 units of wood. Weekly, the carpenter has 40h of labour available and 60 units of wood. Our task is to formulate a mathematical program that maximises the carpenter's weekly outcome.

Following our list of steps, we first must identify the problem's parameters. They are summarised in the table below:

```{list-table} Problem parameters

* - Income per table
  - 1000\$
* - Income per chair
  - 500\$
* - Time needed per table
  - 3h
* - Time needed per chair
  - 5h
* - Wood needed per table
  - 7 units
* - Wood needed per chair
  - 4 units
* - Available time (weekly)
  - 40h
* - Available wood (weekly)
  - 60 units
```

Let $x_t$ be total of tables produced weekly and $x_c$ the total of chairs produced weekly. The total income of the carpenter as a function of $x_t$ and $x_c$ to be maximised is

```{math}
\maxi f(x_t, x_c) = 1000x_t + 500x_c.
```

The carpenter has raw material and labour availability constraints. These can be expressed as

```{math}
\begin{align}
\text{total amount used}&\hspace{0.7cm} \text{total amount available} \\
3x_t + 5x_c& \leq 40 \text{ (labour)}\\
4x_t + 7x_c& \leq 60 \text{ (wood)}  \\
\end{align}
```

Finally, the mathematical programming model that maximises the income of the carpenter is given by:

```{math}
\begin{align}
\text{maximise}_{x_t,x_c} \ &1000x_t + 500x_c \\
\text{subject to: } &3x_t + 5x_c \leq 40\\
&4x_t + 7x_c \leq 60\\
&x_t, x_c \geq 0.
\end{align}
```

```{admonition} Is this model correct?
:class: dropdown, caution

Attentive readers may have noticed something about the above model, namely that there is no constraint forcing $x_t$ and $x_c$ above to be integers. Does it make sense to have $x_t=3.5$? As we will see below, the optimal solution to this problem has non-integer values. We will consider this problem more generally in later lectures.
```

```{code-cell}
using JuMP, HiGHS #JuMP is for writing the mathematical model; HiGHS is the solver (Simplex method). 

m = Model(HiGHS.Optimizer) # Creates a model and informs the solver to be used.

@variable(m, x_t >= 0) # Variable for the total of tables
@variable(m, x_c >= 0) # Variables for the total of chairs

@objective(m, Max, 1000*x_t + 500*x_c) # Income function

@constraint(m, 3*x_t + 5*x_c <= 40) # Labour constraint
@constraint(m, 7*x_t + 4*x_c <= 60) # Wood availability constraint

optimize!(m) # Solve the model

print("\nSOLUTION!!!\n")
print("\nTotal of tables: ", value(x_t), "\nTotal of chairs: ", value(x_c), "\n")
```
