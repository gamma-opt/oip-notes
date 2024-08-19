# Lecture 6 - Symbolic formulation

## Motivation for symbolic formulations

One aspect that might have become evident is that, as models start to have more numerous entities, such as production plants, demand points, arcs, and time periods, very quickly the mathematical programming model becomes less and less human readable. This, in turn, compromises model validation and maintenance. Furthermore, it makes it inefficient and prone to error to make updates in the model's input data.

A best-practice approach is to have the *model data* separated from the *model formulation*. Effectively, this dissociates the maintenance of the model and its data source, while allowing for the creation of multiple instantiations of the same model.

To achieve that, we must rely on abstract entities that represent the elements of the problem. We describe those next.

## Elements of a symbolic formulation

### Model data

The model data, or input data, is represented by *indices* and their *sets* and *parameters*.

- **Indices and sets**: these represent entities in the problem that are discrete and can be grouped by what they represent in the model.
- **Parameters**: are numerical values representing quantities that are associate to indices or combinations of indices.

We have come across these before. For example, in the transportation problem, we defined the plants as $i = 1, 2, 3$. If we define the set $I = \braces{1,2,3}$, then we can say that the cities are defined as $i \in I$. Now, we can represent the production capacity of each plant as $C_i$ for $i \in I$.

```{note}
It is a convention to represent sets with capital letters and indices with lower case letters (often the same).
```

### Model formulation

The model formulation is composed by *variables*, *objective function*, and *constraints*. We have considered their role in detail before, so we now focus on how to pose them such that they are data independent.

Let us start with **decision variables**. The convention is to index decision variables with the defined indices. So, suppose we have a index set $j \in J$, representing some entity in our model. Then, to define a decision variable for each of these, we define $x_j$, $\forall j \in J$. This indicates that we have a decision variable $x$ for each index $j$ in the set $J$.

This can be extended to as many indices as necessary. Going back to our transportation problem, where we had $i \in I$ plants and $j \in J$ demand points, our flow variables could be represented as $x_{ij}$, $\forall i \in I, j \in J$.

Once we have variables defined, we can use them to pose objective functions. A compact way to do so is to express them as summation of products between parameters and variables. Coming back to our variable $x_j$, $\forall j \in J$, suppose we have a cost coefficient $c_j$, $j \in J$, associated with each. Then, our objective function can be posed as

```{math}
\mini_{x} c_1x_1 + c_2x_2 + \dots + c_{|J|}x_{|J|} \equiv \mini_{x} \sum_{j \in J} c_jx_j.
```

Notice a couple of nice features about this way of posing our objective function. First, there is the fact that it is a much more compact notation, which can be quickly read by a human. Second, it *remains compact*, regardless of the cardinality of the index set $J$ (represented $| \ \cdot \ |$).

The same logic can be applied to constraints, being the main difference that we must consider not only the summation domains, but also the *replication* domain (or the indexing) of the constraints. Suppose we have a parameter $a_{ij}$, for $i \in I, j \in J$ multiplying our variables $x_j$, $j \in J$ and that their combined sum must be less or equal a quantity $b_i$, defined for each $i \in I$. For simplicity, assume for now that $|I| = |J| = 2$. Assume that each constraint must be summed in the domain of $i \in I$ and replicated $j \in J$. Since we have two indices for each set, we would have the following constraints

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

Again, notice how much more compact is this set of constraints. Again, with a single statement we can represent sets of constraints at once, in a far more compact notation. Let us explore these ideas a bit further returning to our transportation problem.

## Example - transportation problem

Let's revisit our transportation problem and pose it as model written in symbolic formulation.

### Indices and sets

The transportation problem has two sets of entities: a set of plants $i \in I$ and a set of demand points (clients) $j \in J$.

### Parameters

There are three parameters: 

- plant capacities, represented by $C_i$, $i \in I$,
- demand amounts at each client, represented by $D_j$, $j \in J$,
- unit transportation cost between each plant $i$ and demand point $j$, represented by $T_{ij}$, $i \in I$, $j \in J$. 

### Variables

Our transportation model has only one type of decision variable: let $x_{ij}$ be the amount transported from plan $i$ to client $j \in J$. Naturally, we must enforce that these amounts are not negative.

### Objective function

Our objective is to minimise the aggregated transportation cost, which is defined as

```{math}
\mini_x \sum_{i \in I} \sum_{j \in J} T_{ij}x_{ij}.
```

Notice how we need a double summation since we have two indices to sum over.

### Constraints

There are two main constraint sets in the transportation problem: 

- **Supply limit**: all that is send from each plant $i \in I$ must be less than or equal to the plant $i$ capacity $C_i$. Thus, we have that

```{math}
\sum_{j \in J} x_{ij} \le C_i, \forall i \in I.
```

- **Demand fulfillment**: the accumulated total that is sent from plants $i \in I$ to each client $j \in J$ must be equal to the client $j$ demand $D_j$. Therefore, we have

```{math}
\sum_{i \in I} x_{ij} = D_j, \forall j \in J.
```

Putting the whole model together, we obtain

```{math}
\begin{equation}
\begin{aligned}
    \mini_x & \sum_{i \in I} \sum_{j \in J} T_{ij}x_{ij} \\
    \st & \sum_{j \in J} x_{ij} \le C_i, \forall i \in I \\
    & \sum_{i \in I} x_{ij} = D_j, \forall j \in J \\
    & x_{ij} \ge 0, \ \forall i \in I, j \in J.
\end{aligned}
\end{equation}
```

%TODO: Include the computational example currently in Lecture 7 here. Show some print statements and maybe some random generated instances with a few 100 nodes. Example code: 

<!-- using Random
M = 50 # factories
N = 100 # clients
 
x_coord = 1000*rand(M+N)
y_coord = 1000*rand(M+N)

C = 30*rand(M) # factory capacity
D = 10*rand(N) # client demand

T = zeros(M,N) # cost 

for i = 1:M
    for j = 1:N
        T[i,j] = 10*sqrt((x_coord[i] - x_coord[j+M])^2 + 
            (y_coord[i] - y_coord[j+M])^2)
    end
end
        
if sum(C) < sum(D)
    println("Capacity has been adjusted to obtain feasibility.\n")
    C[N] = C[N] + sum(D) - sum(C)
end -->

<!-- m = Model(with_optimizer(Gurobi.Optimizer)) # Creates a model and informs the solver to be used. Use HiGHS!

@variable(m, x[i = 1:M, j = 1:N] >= 0) # Variable for the total transported

@objective(m, Min, sum(T[i,j]*x[i,j] for i = 1:M, j = 1:N)) # Distribution cost

@constraint(m, cap[i = 1:M], sum(x[i,j] for j = 1:N) <= C[i]) # Capacity constraint
@constraint(m, dem[j = 1:N], sum(x[i,j] for i = 1:M) >= D[j]); # Demand constraint

println(m) # Prints the mathematical model (at your own risk!) -->

<!-- optimize!(m) # Solve the model -->

<!-- # This code plots a graph with the randomly generated instance and its solution.
using Plots

plot()

for i=1:M
    for j=1:N
        if value(x[i,j]) > 0.0
            plot!([x_coord[i],x_coord[j+M]],[y_coord[i], y_coord[j+M]], color=:black, label="")
        end
    end
end

scatter!(x_coord[1:M], y_coord[1:M], label = "Plants")
scatter!(x_coord[M+1:M+N], y_coord[M+1:M+N], label = "Clients", legend=true) -->

