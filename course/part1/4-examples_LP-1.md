# Mathematical programming models: examples

Let us practice the idea of posing problems as mathematical programming models. Before we do so let us discuss a fundamental aspect associated with mathematical programming models: the notion of **linearity**.

(p1l4-linear_models)=
## Why linear models? 

As you familiarise yourself with mathematical programming, you may notice that modellers dedicate a considerable amount of effort to make sure that mathematical optimisation models are linear whenever it is possible. First, let us define what me mean by a linear model. Let

```{math}
:label: eq-linear-model

\begin{aligned}
\mini & f(x) \\
\st & g(x) \le 0 \\
    & h(x) = 0
\end{aligned}
```

be our optimisation model. We say that {eq}`eq-linear-model` is **linear** if $f$ is a linear function in $x$ and $g$ are affine functions in $x$.

```{note}
Let $a$ and $b$ be nonzeros scalars. The function $f(x) = ax$ is *linear* in $x$ while $g(x) = ax + b$ is *affine* in $x$. The difference is that $f$ touches the origin $(0,0)$ while $g$ does not.
```

The reason why we should model our problems using linear equations is purely practical (or computational). It stems from the combination of two mathematical facts:

1. **Linear problems are convex.** As such, any solution that can identify a local optimum automatically retrieves a global optimum.
2. **Linear problems have a very particular structure.** That structure can be exploited to define optimality conditions that allow for "jumping" between candidate solutions until identifying a locally optimal one.

The most successful method for solving linear problems, the **simplex method**, combine both ideas in its design, resulting in robust, robust, and consequently widely used, optimisation algorithm that holds the place of algorithm of choice in most practical applications of mathematical programming. Detaching from linear optimisation is, therefore, avoided whenever possible.

```{note}
More recently, the obsession for linearity has been a little "less" justified due to the development progress of an alternative solution framework called **interior-point (or barrier) methods**, which naturally accommodates for nonlinear functions without considerable increments in computational burden. 

In the words of Prof. Tyrrell Rockafellar:

> "...in fact, the great watershed in optimization isn't between linearity and nonlinearity, but convexity and nonconvexity." {cite}`rockafellar_lagrange_1993`

```

## Examples

Modelling using mathematical programming requires practice in identifying the elements that compose the problem and stating the equations that correctly capture the relationship between these elements. Next, we work through a few "realistic" examples. These examples are based on {cite}`williams_model_2013`.

(p1l5:food)=
### Food Manufacture

Suppose that we are at the helm of a food production company, where our main product is manufactured by the blending of vegetable and non-vegetable oils.
We can purchase oils either for immediate delivery or for delivery in a later month.
The prices for the oils are given in {numref}`table_food_manufacture`.

```{table} Oil prices in €/ton
:name: table_food_manufacture
|          | VEG 1 | VEG 2 | OIL 1 | OIL 2 | OIL 3 |
|----------|-------|-------|-------|-------|-------|
| *January*  | 110   | 120   | 130   | 110   | 115   |
| *February* | 130   | 130   | 110   | 90    | 115   |
| *March*    | 110   | 140   | 130   | 100   | 95    |
| *April*    | 120   | 110   | 120   | 120   | 125   |
| *May*      | 100   | 120   | 150   | 110   | 105   |
| *June*     | 90    | 100   | 140   | 80    | 95    |
```
The final product sells at €150 per ton.

We can process a maximum of 200 tons of vegetable oil and 250 tons of non-vegetable oil in any given month. In addition, we can store up to 1000 tons of each raw oil for later use at a cost of €5 per ton per month.

Lastly, we need to ensure that the resulting product has appropriate hardness, which should be in between 3 and 6 units.
Hardness blends linearly with the input oils, which have the hardness values

```{list-table} Oil hardness values
:header-rows: 0

* - *VEG 1*
  - 8.8
* - *VEG 2*
  - 6.1
* -
  -
* - *OIL 1*
  - 2.0
* - *OIL 2*
  - 4.2
* - *OIL 3*
  - 5.0
```

Assume that all production in a given month is sold. Also, at the start of January, we have a stock of 500 tons of each raw oil in storage. We need to ensure that these stocks will exist at the end of June. What 6-month production policy should we pursue to maximise profit?

#### Solution

Recall our set of steps for modelling optimisation problems:

1. List **parameters**;
2. Define **decision variables**; 
3. Formulate **objective function**;
4. Formulate **constraints**. 

Listing the parameters has already been done for us, so we can proceed to defining our decision variables. 
In this case, we want to decide how much oil of each type we would like to purchase in a month, how much of it to store and how much to use for processing.
This is then repeated 6 times, one for each month in the half-year period.
Thus we define

- $b_{ij}$ - amount of oil $i$ purchased in month $j$,
- $u_{ij}$ - amount of oil $i$ used for blending in month $j$,
- $s_{ij}$ - amount of oil $i$ stored in month $j$,
- $p_j$ - amount of product produced in month $j$,

where we label oils 1 to 5 as vegetable oil 1 and 2, followed by non-vegetable oil 1, 2 and 3.
This means we have 91 decision variables, all of which are non-negative.

Once the variables have been defined, we can pose our objective function. In this case, our function is the total profit, which we would like to *maximize*. Thus, we have that

```{math}
\maxi & f(b_{ij}, u_{ij}, s_{ij}, p_j) = \\ 
      & 150(p_1+p_2+p_3+p_4+p_5+p_6) \\
      & -110b_{11} -130b_{12} -110b_{13} -120b_{14} -100b_{15} - 90b_{16} \\
      & -120b_{21} -130b_{22} -140b_{23} -110b_{24} -120b_{25} -100b_{26} \\
      & -130b_{31} -110b_{32} -130b_{33} -120b_{34} -150b_{35} -140b_{36} \\
      & -110b_{41} - 90b_{42} -100b_{43} -120b_{44} -110b_{45} - 80b_{46} \\
      & -115b_{51} -115b_{52} - 95b_{53} -125b_{54} -105b_{55} -135b_{56} \\
      & -5(s_{11}+\dots+s_{56}).
```
which is composed of costs of purchasing the oil, storage costs, and income from selling the blended product.

From our problem statement, we can see that there are five sources of constraints we must consider: linear production, processing limits, hardness constraints, storage continuity and storage limits.

Linear production just means that we produce as much product as we use oils in any given month $j$

```{math}
u_{1j}+u_{2j}+u_{3j}+u_{4j}+u_{5j} = p_j.
```

The processing limits are easy, for month $j$ we need

```{math}
u_{1j}+u_{2j} &\leq 200 \\
u_{3j}+u_{4j}+u_{5j} &\leq 250.
```

The hardness constraints for month $j$ are also not complicated:

```{math}
8.8u_{1j}+6.1u_{2j}+2.0u_{3j}+4.2u_{4j}+5.0u_{5j} &\leq 6y_j \\
8.8u_{1j}+6.1u_{2j}+2.0u_{3j}+4.2u_{4j}+5.0u_{5j} &\geq 3y_j.
```

For storage, we link these variables together by the relation
```{math}
\text{quantity stored in month }(j-1) + \text{quantity bought in month }j

= \text{quantity used in month }j + \text{quantity stored in month }j.
```

In doing the above, we need to make the initial storage of 500 tons per oil available and ensure that it exists at the end as well.
Thus we obtain for oil $i$

```{math}
:label: p1l5:food_storage
 b_{i1} -u_{i1}-s_{i1} &= -500 \\
s_{i1} + b_{i2} -u_{i2}-s_{i2} &= 0 \\
s_{i2} + b_{i3} -u_{i3}-s_{i3} &= 0 \\
s_{i3} + b_{i4} -u_{i4}-s_{i4} &= 0 \\
s_{i4} + b_{i5} -u_{i5}-s_{i5} &= 0 \\
s_{i5} + b_{i6} -u_{i6}\hspace{1.2cm} &=500.
```

There is also a storage limit for each type of oil, which we can implement by constraining the variables
```{math}
s_{11},\dots,s_{5,6}\leq 1000.
```

Lastly, since we cannot work with negative amounts of oil, we must add nonnegativity constraints in the definition of the decision variables. Thus, we must guarantee that $b_{ij} \ge 0, u_{ij} \ge 0,  s_{ij} \ge 0, p_j\ge 0$.

Putting it all together, the optimisation model that provides the maximum profit is given by

```{math}
:nowrap:
\begin{align*}
\maxi & f(b_{ij}, u_{ij}, s_{ij}, p_j) = \\ 
      & 150(p_1+p_2+p_3+p_4+p_5+p_6) \\
      & -110b_{11} -130b_{12} -110b_{13} -120b_{14} -100b_{15} - 90b_{16} \\
      & -120b_{21} -130b_{22} -140b_{23} -110b_{24} -120b_{25} -100b_{26} \\
      & -130b_{31} -110b_{32} -130b_{33} -120b_{34} -150b_{35} -140b_{36} \\
      & -110b_{41} - 90b_{42} -100b_{43} -120b_{44} -110b_{45} - 80b_{46} \\
      & -115b_{51} -115b_{52} - 95b_{53} -125b_{54} -105b_{55} -135b_{56} \\
      & -5(s_{11}+\dots+s_{56}) \\
\st & u_{11}+u_{21}+u_{31}+u_{41}+u_{51} = p_1 \\
& u_{12}+u_{22}+u_{32}+u_{42}+u_{52} = p_2 \\
& u_{13}+u_{23}+u_{33}+u_{43}+u_{53} = p_3 \\
& u_{14}+u_{24}+u_{34}+u_{44}+u_{54} = p_4 \\
& u_{15}+u_{25}+u_{35}+u_{45}+u_{55} = p_5 \\
& u_{16}+u_{26}+u_{36}+u_{46}+u_{56} = p_6 \\
& u_{11}+u_{21} \leq 200 \\
& u_{12}+u_{22} \leq 200 \\
& u_{13}+u_{23} \leq 200 \\
& u_{14}+u_{24} \leq 200 \\
& u_{15}+u_{25} \leq 200 \\
& u_{16}+u_{26} \leq 200 \\
& u_{31}+u_{41}+u_{51} \leq 250 \\
& u_{32}+u_{42}+u_{52} \leq 250 \\
& u_{33}+u_{43}+u_{53} \leq 250 \\
& u_{34}+u_{44}+u_{54} \leq 250 \\
& u_{35}+u_{45}+u_{55} \leq 250 \\
& u_{36}+u_{46}+u_{56} \leq 250 \\
& 8.8u_{11}+6.1u_{21}+2.0u_{31}+4.2u_{41}+5.0u_{51} \leq 6y_1 \\
& 8.8u_{12}+6.1u_{22}+2.0u_{32}+4.2u_{42}+5.0u_{52} \leq 6y_2 \\
& 8.8u_{13}+6.1u_{23}+2.0u_{33}+4.2u_{43}+5.0u_{53} \leq 6y_3 \\
& 8.8u_{14}+6.1u_{24}+2.0u_{34}+4.2u_{44}+5.0u_{54} \leq 6y_4 \\
& 8.8u_{15}+6.1u_{25}+2.0u_{35}+4.2u_{45}+5.0u_{55} \leq 6y_5 \\
& 8.8u_{16}+6.1u_{26}+2.0u_{36}+4.2u_{46}+5.0u_{56} \leq 6y_6 \\
& 8.8u_{11}+6.1u_{21}+2.0u_{31}+4.2u_{41}+5.0u_{51} \geq 3y_1 \\
& 8.8u_{12}+6.1u_{22}+2.0u_{32}+4.2u_{42}+5.0u_{52} \geq 3y_2 \\
& 8.8u_{13}+6.1u_{23}+2.0u_{33}+4.2u_{43}+5.0u_{53} \geq 3y_3 \\
& 8.8u_{14}+6.1u_{24}+2.0u_{34}+4.2u_{44}+5.0u_{54} \geq 3y_4 \\
& 8.8u_{15}+6.1u_{25}+2.0u_{35}+4.2u_{45}+5.0u_{55} \geq 3y_5 \\
& 8.8u_{16}+6.1u_{26}+2.0u_{36}+4.2u_{46}+5.0u_{56} \geq 3y_6 \\
& b_{11} -u_{11}-s_{11} = -500 \\
& b_{21} -u_{21}-s_{21} = -500 \\
& b_{31} -u_{31}-s_{31} = -500 \\
& b_{41} -u_{41}-s_{41} = -500 \\
& b_{51} -u_{51}-s_{51} = -500 \\
& s_{11} + b_{12} -u_{12}-s_{12} = 0 \\
& s_{12} + b_{13} -u_{13}-s_{13} = 0 \\
& s_{13} + b_{14} -u_{14}-s_{14} = 0 \\
& s_{14} + b_{15} -u_{15}-s_{15} = 0 \\
& s_{21} + b_{22} -u_{22}-s_{22} = 0 \\
& s_{22} + b_{23} -u_{23}-s_{23} = 0 \\
& s_{23} + b_{24} -u_{24}-s_{24} = 0 \\
& s_{24} + b_{25} -u_{25}-s_{25} = 0 \\
& s_{31} + b_{32} -u_{32}-s_{32} = 0 \\
& s_{32} + b_{33} -u_{33}-s_{33} = 0 \\
& s_{33} + b_{34} -u_{34}-s_{34} = 0 \\
& s_{34} + b_{35} -u_{35}-s_{35} = 0 \\
& s_{41} + b_{42} -u_{42}-s_{42} = 0 \\
& s_{42} + b_{43} -u_{43}-s_{43} = 0 \\
& s_{43} + b_{44} -u_{44}-s_{44} = 0 \\
& s_{44} + b_{45} -u_{45}-s_{45} = 0 \\
& s_{51} + b_{52} -u_{52}-s_{52} = 0 \\
& s_{52} + b_{53} -u_{53}-s_{53} = 0 \\
& s_{53} + b_{54} -u_{54}-s_{54} = 0 \\
& s_{54} + b_{55} -u_{55}-s_{55} = 0 \\
& s_{15} + b_{16} -u_{16} =500 \\
& s_{25} + b_{26} -u_{26} =500 \\
& s_{35} + b_{36} -u_{36} =500 \\
& s_{45} + b_{46} -u_{46} =500 \\
& s_{55} + b_{56} -u_{56} =500 \\
& b_{11}, \dots, b_{56} \geq 0 \\
& u_{11}, \dots, u_{56} \geq 0 \\
& s_{11}, \dots, s_{56} \geq 0 \\
& p_1, \dots, p_6 \geq 0 \\
& s_{11}, \dots, s_{56} \leq 1000.
\end{align*}
```

Clearly, this model is far more complex than our {ref}`p1l4:first-model`, which is expected for being a more realistic one. We will hold on how to to solve this for now, and keep practicing the process of modelling itself.

(p1l5:production)=
### Factory Planning

In this example, we are at an engineering factory that makes seven different products.
The production processes of these involve the following machines:

- four grinders,
- two vertical drills,
- three horizontal drills,
- one borer, and
- one planer.

The process of making every product is different and different products require the use of machines differently.
Similarly, every product yields a certain net profit.
The time consumed by machine operations in hours and net profits in € are described in {numref}`p1l5:production_table`, where a dash means that the product does not use the indicated machine.

```{table} Production parameters: net profits (€) and time needed by machines (h)
:name: p1l5:production_table

|                         | **Product 1** | **Product 2** | **Product 3** | **Product 4** | **Product 5** | **Product 6** | **Product 7** |
|:-----------------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|---------------|
|        **Profit**       | 10            | 6             | 8             | 4             | 11            | 9             | 3             |
|       **Grinding**      | 0.5           | 0.7           | -             | -             | 0.3           | 0.2           | 0.5           |
|  **Vertical drilling**  | 0.1           | 0.2           | -             | 0.3           | -             | 0.6           | -             |
| **Horizontal drilling** | 0.2           | -             | 0.8           | -             | -             | -             | 0.6           |
|        **Boring**       | 0.05          | 0.04          | -             | 0.7           | 0.1           | -             | 0.08          |
|       **Planing**       | -             | -             | 0.01          | -             | 0.05          | -             | 0.05          |
```

The machines are not always available, some will be under maintenance at certain months. The maintenance schedule is

```{list-table} Maintenance schedule
:header-rows: 0

* - **January**
  - 1 Grinder
* - **February**
  - 2 Horizontal drills
* - **March**
  - 1 Borer
* - **April**
  - 1 Vertical drill
* - **May**
  - 1 Grinder and 1 Vertical drill
* - **June**
  - 1 Planer and 1 Horizontal drill
```

In addition, due to market conditions, there are limits to how much of each product we can sell every month.

```{table} Limits on selling products
|                         | **Product 1** | **Product 2** | **Product 3** | **Product 4** | **Product 5** | **Product 6** | **Product 7** |
|:-----------------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|---------------|
|        **January**       | 500           | 1000          | 300           | 300           | 800           | 200           | 100           |
|       **February**      | 600           | 500           | 200           | 0             | 400           | 300           | 150           |
|  **March**  | 300           | 600           | 0             | 0             | 500           | 400           | 100           |
| **April** | 200           | 300           | 400           | 500           | 200           | 0             | 100           |
|        **May**       | 0             | 100           | 500           | 100           | 1000          | 300           | 0             |
|       **June**       | 500           | 500           | 100           | 300           | 1100          | 500           | 60            |
```

Once again, we can store products, up to 100 of each at a cost of €0.05 per unit per month.
However, this time we have no initial stock, but we would like to accumulate a one: 50 of each product by the end of June.

The factory works 24 days a month, each day containing two 8 hour shifts. For simplicity, we assume that the production process can use the machines in any order. Our objective is to determine a production schedule that maximises total profit.

#### Solution

Once again, our list guides us.

1. List **parameters**;
2. Define **decision variables**; 
3. Formulate **objective function**;
4. Formulate **constraints**.

The parameters are listed in the tables and the text above.
This problem is somewhat similar to the food manufacturing problem.
Here, instead of having multiple raw materials and a single product, we are ignoring the raw materials and dealing with multiple products.
Our task is to decide when to manufacture, store and sell these products, thus we define three types of variables:

- $m_{ij}$ - amount of product $i$ manufactured in month $j$,
- $h_{ij}$ - amount of product $i$ held in storage in month $j$, and
- $s_{ij}$ - amount of product $i$ sold in month $j$.

Our objective function is the _maximisation_ of the total profits of the production schedule, after subtracting holding costs.

```{math}
\maxi & f(m_{ij}, h_{ij}, s_{ij}) = \\ 
      10 &( s_{11}+s_{12}+s_{13}+s_{14}+s_{15}+s_{16}) \\
      +6 &( s_{21}+s_{22}+s_{23}+s_{24}+s_{25}+s_{26}) \\
      +8 &( s_{31}+s_{32}+s_{33}+s_{34}+s_{35}+s_{36}) \\
      +4 &( s_{41}+s_{42}+s_{43}+s_{44}+s_{45}+s_{46}) \\
     +11 &( s_{51}+s_{52}+s_{53}+s_{54}+s_{55}+s_{56}) \\
      +9 &( s_{61}+s_{62}+s_{63}+s_{64}+s_{65}+s_{66}) \\
      +3 &( s_{71}+s_{72}+s_{73}+s_{74}+s_{75}+s_{76}) \\
      -0.5 &( h_{11} + \dots h_{76})
```

There are multiple constraints we need to keep track of.
The basic one is that none of the decision variables we defined can be negative, imposing a lower bound on each: $m_{ij},h_{ij},s_{ij}\geq 0$.
In addition, we can store only up to 100 of each product, which means the holding variables need an upper bound $h_{ij}\leq 100$.
Similarly, the market imposes an upper bound on how much we can sell per month:

```{math}
s_{11} \leq 500, s_{21} \leq 1000, &\dots, s_{71} \leq 100 \\
s_{12} \leq 600, s_{22} \leq 500, &\dots, s_{72} \leq 150 \\
\vdots& \\
s_{16} \leq 500, s_{26} \leq 500, &\dots, s_{76} \leq 60
```

Another easy one is ensuring that we have a stock of 50 of each product at the end, which we can do via

```{math}
:label: p1l5:production_storage
h_{16}=\dots=h_{76} = 50.
```

To model the amount of production, recall that the processes can use machines in any order.
This means that we can calculate the availability of each machine for every month in hours, and add a constraints to ensure they are not exceeded.
For example, our factory has four grinders, which multiplied with 24 days a month, 2 shifts a day and 8 hours a shift gives

```{math}
4\times 24 \times 2 \times 8 = 1536
```

hours available per month.
However, according to the maintenance schedule, in January and May we will have access to only three grinders, meaning the availability for these months is

```{math}
3\times 24\times 2\times 8 = 1152
```

hours instead. Thus we can write the constraints

```{math}
0.5m_{11}+0.7m_{21}+0.3m_{51}+0.2m_{61}+0.5m_{71}\leq 1152 \\
0.5m_{12}+0.7m_{22}+0.3m_{52}+0.2m_{62}+0.5m_{72}\leq 1536 \\
0.5m_{13}+0.7m_{23}+0.3m_{53}+0.2m_{63}+0.5m_{73}\leq 1536 \\
0.5m_{14}+0.7m_{24}+0.3m_{54}+0.2m_{64}+0.5m_{74}\leq 1536 \\
0.5m_{15}+0.7m_{25}+0.3m_{55}+0.2m_{65}+0.5m_{75}\leq 1152 \\
0.5m_{16}+0.7m_{26}+0.3m_{56}+0.2m_{66}+0.5m_{76}\leq 1536
```

for the grinders.

Repeating this for the other machines, we obtain

```{math}
0.1m_{11} + 0.2m_{21} + 0.3m_{41} + 0.6m_{61} \leq 768 \\
0.1m_{12} + 0.2m_{22} + 0.3m_{42} + 0.6m_{62} \leq 768 \\
0.1m_{13} + 0.2m_{23} + 0.3m_{43} + 0.6m_{63} \leq 768 \\
0.1m_{14} + 0.2m_{24} + 0.3m_{44} + 0.6m_{64} \leq 384 \\
0.1m_{15} + 0.2m_{25} + 0.3m_{45} + 0.6m_{65} \leq 384 \\
0.1m_{16} + 0.2m_{26} + 0.3m_{46} + 0.6m_{66} \leq 768
```

for the vertical drills,

```{math}
0.2m_{11} + 0.8m_{31} + 0.6m_{71} &\leq 1152 \\
0.2m_{12} + 0.8m_{32} + 0.6m_{72} &\leq 384 \\
0.2m_{13} + 0.8m_{33} + 0.6m_{73} &\leq 1152 \\
0.2m_{14} + 0.8m_{34} + 0.6m_{74} &\leq 1152 \\
0.2m_{15} + 0.8m_{35} + 0.6m_{75} &\leq 1152 \\
0.2m_{16} + 0.8m_{36} + 0.6m_{76} &\leq 768
```

for the horizontal drills,

```{math}
0.05m_{11} + 0.03m_{21} + 0.07m_{41} + 0.1m_{51} + 0.08m_{71} &\leq 384 \\
0.05m_{12} + 0.03m_{22} + 0.07m_{42} + 0.1m_{52} + 0.08m_{72} &\leq 384 \\
0.05m_{13} + 0.03m_{23} + 0.07m_{43} + 0.1m_{53} + 0.08m_{73} &\leq 0 \\
0.05m_{14} + 0.03m_{24} + 0.07m_{44} + 0.1m_{54} + 0.08m_{74} &\leq 384 \\
0.05m_{15} + 0.03m_{25} + 0.07m_{45} + 0.1m_{55} + 0.08m_{75} &\leq 384 \\
0.05m_{16} + 0.03m_{26} + 0.07m_{46} + 0.1m_{56} + 0.08m_{76} &\leq 384
```

for the borer, and

```{math}
0.01m_{31} + 0.05m_{51} + 0.05m_{71} &\leq 384 \\
0.01m_{32} + 0.05m_{52} + 0.05m_{72} &\leq 384 \\
0.01m_{33} + 0.05m_{53} + 0.05m_{73} &\leq 384 \\
0.01m_{34} + 0.05m_{54} + 0.05m_{74} &\leq 384 \\
0.01m_{35} + 0.05m_{55} + 0.05m_{75} &\leq 384 \\
0.01m_{36} + 0.05m_{56} + 0.05m_{76} &\leq 0
```

for the planer.

Lastly, we need to link the manufacturing, holding and selling variables together. We can only sell or store what is already available, either freshly manufactured or from the previous month's inventory, which is 0 in the first month. Thus for Product 1, we have that

```{math}
m_{11}-s_{11}-h_{11} &= 0 \\
h_{11} + m_{12}-s_{12}-h_{12} &= 0 \\
h_{12} + m_{13}-s_{13}-h_{13} &= 0 \\
h_{13} + m_{14}-s_{14}-h_{14} &= 0 \\
h_{14} + m_{15}-s_{15}-h_{15} &= 0 \\
h_{15} + m_{16}-s_{16}-h_{16} &= 0 \\
```

and identical constraints govern the other products.

```{admonition} Do the above constraints look familiar?
:class: dropdown, note
The above constraints are very similar to {eq}`p1l5:food_storage` in the food manufacturing problem, where we kept track of storage variables.
In both cases, we have a target stock to accumulate at the end of the time period, pay attention to how that is modeled.

In the previous problem, we incorporated specific values into the constraints.
Here, we preserve the form of the equations, and add the targets as a separate constraint in {eq}`p1l5:production_storage`.
Both are equivalent.
```

Putting this all together, the optimisation model for the maximum profit production plan for the factory is given by

```{math}
:nowrap:
\begin{align*}
\maxi & f(m_{ij}, h_{ij}, s_{ij}) = \\ 
      10 &( s_{11}+s_{12}+s_{13}+s_{14}+s_{15}+s_{16}) \\
      +6 &( s_{21}+s_{22}+s_{23}+s_{24}+s_{25}+s_{26}) \\
      +8 &( s_{31}+s_{32}+s_{33}+s_{34}+s_{35}+s_{36}) \\
      +4 &( s_{41}+s_{42}+s_{43}+s_{44}+s_{45}+s_{46}) \\
     +11 &( s_{51}+s_{52}+s_{53}+s_{54}+s_{55}+s_{56}) \\
      +9 &( s_{61}+s_{62}+s_{63}+s_{64}+s_{65}+s_{66}) \\
      +3 &( s_{71}+s_{72}+s_{73}+s_{74}+s_{75}+s_{76}) \\
      -0.5 &( h_{11} + \dots + h_{76}) \\
\st & s_{11} \leq 500, s_{21} \leq 1000, s_{31} \leq 300, s_{41} \leq 300, s_{51} \leq 800, s_{61} \leq 200, s_{71} \leq 100 \\
    & s_{12} \leq 600, s_{22} \leq 500, s_{32} \leq 200, s_{42} \leq 0, s_{52} \leq 400, s_{62} \leq 300, s_{72} \leq 150 \\
    & s_{13} \leq 300, s_{23} \leq 600, s_{33} \leq   0, s_{43} \leq 0, s_{53} \leq 500, s_{63} \leq 400, s_{73} \leq 100 \\
    & s_{14} \leq 600, s_{24} \leq 300, s_{34} \leq 400, s_{44} \leq 500, s_{54} \leq 200, s_{64} \leq 0, s_{74} \leq 100 \\
    & s_{15} \leq 600, s_{25} \leq 100, s_{35} \leq 500, s_{45} \leq 100, s_{55} \leq 1000, s_{65} \leq 300, s_{75} \leq 0 \\
    & s_{16} \leq 500, s_{26} \leq 500, s_{36} \leq 100, s_{46} \leq 300, s_{56} \leq 1100, s_{66} \leq 500, s_{76} \leq 60 \\
    & 0.5m_{11}+0.7m_{21}+0.3m_{51}+0.2m_{61}+0.5m_{71}\leq 1152 \\
    & 0.5m_{12}+0.7m_{22}+0.3m_{52}+0.2m_{62}+0.5m_{72}\leq 1536 \\
    & 0.5m_{13}+0.7m_{23}+0.3m_{53}+0.2m_{63}+0.5m_{73}\leq 1536 \\
    & 0.5m_{14}+0.7m_{24}+0.3m_{54}+0.2m_{64}+0.5m_{74}\leq 1536 \\
    & 0.5m_{15}+0.7m_{25}+0.3m_{55}+0.2m_{65}+0.5m_{75}\leq 1152 \\
    & 0.5m_{16}+0.7m_{26}+0.3m_{56}+0.2m_{66}+0.5m_{76}\leq 1536 \\
    & 0.1m_{11} + 0.2m_{21} + 0.3m_{41} + 0.6m_{61} \leq 768 \\
    & 0.1m_{12} + 0.2m_{22} + 0.3m_{42} + 0.6m_{62} \leq 768 \\
    & 0.1m_{13} + 0.2m_{23} + 0.3m_{43} + 0.6m_{63} \leq 768 \\
    & 0.1m_{14} + 0.2m_{24} + 0.3m_{44} + 0.6m_{64} \leq 384 \\
    & 0.1m_{15} + 0.2m_{25} + 0.3m_{45} + 0.6m_{65} \leq 384 \\
    & 0.1m_{16} + 0.2m_{26} + 0.3m_{46} + 0.6m_{66} \leq 768 \\
    & 0.2m_{11} + 0.8m_{31} + 0.6m_{71} \leq 1152 \\
    & 0.2m_{12} + 0.8m_{32} + 0.6m_{72} \leq 384 \\
    & 0.2m_{13} + 0.8m_{33} + 0.6m_{73} \leq 1152 \\
    & 0.2m_{14} + 0.8m_{34} + 0.6m_{74} \leq 1152 \\
    & 0.2m_{15} + 0.8m_{35} + 0.6m_{75} \leq 1152 \\
    & 0.2m_{16} + 0.8m_{36} + 0.6m_{76} \leq 768 \\
    & 0.05m_{11} + 0.03m_{21} + 0.07m_{41} + 0.1m_{51} + 0.08m_{71} \leq 384 \\
    & 0.05m_{12} + 0.03m_{22} + 0.07m_{42} + 0.1m_{52} + 0.08m_{72} \leq 384 \\
    & 0.05m_{13} + 0.03m_{23} + 0.07m_{43} + 0.1m_{53} + 0.08m_{73} \leq 0 \\
    & 0.05m_{14} + 0.03m_{24} + 0.07m_{44} + 0.1m_{54} + 0.08m_{74} \leq 384 \\
    & 0.05m_{15} + 0.03m_{25} + 0.07m_{45} + 0.1m_{55} + 0.08m_{75} \leq 384 \\
    & 0.05m_{16} + 0.03m_{26} + 0.07m_{46} + 0.1m_{56} + 0.08m_{76} \leq 384 \\
    & 0.01m_{31} + 0.05m_{51} + 0.05m_{71} \leq 384 \\
    & 0.01m_{32} + 0.05m_{52} + 0.05m_{72} \leq 384 \\
    & 0.01m_{33} + 0.05m_{53} + 0.05m_{73} \leq 384 \\
    & 0.01m_{34} + 0.05m_{54} + 0.05m_{74} \leq 384 \\
    & 0.01m_{35} + 0.05m_{55} + 0.05m_{75} \leq 384 \\
    & 0.01m_{36} + 0.05m_{56} + 0.05m_{76} \leq 0 \\
    & m_{11}-s_{11}-h_{11} = 0 \\
    & h_{11} + m_{12}-s_{12}-h_{12} = 0 \\
    & h_{12} + m_{13}-s_{13}-h_{13} = 0 \\
    & h_{13} + m_{14}-s_{14}-h_{14} = 0 \\
    & h_{14} + m_{15}-s_{15}-h_{15} = 0 \\
    & h_{15} + m_{16}-s_{16}-h_{16} = 0 \\
    & m_{21}-s_{21}-h_{21} = 0 \\
    & h_{21} + m_{22}-s_{22}-h_{22} = 0 \\
    & h_{22} + m_{23}-s_{23}-h_{23} = 0 \\
    & h_{23} + m_{24}-s_{24}-h_{24} = 0 \\
    & h_{24} + m_{25}-s_{25}-h_{25} = 0 \\
    & h_{25} + m_{26}-s_{26}-h_{26} = 0 \\
    & m_{31}-s_{31}-h_{31} = 0 \\
    & h_{31} + m_{32}-s_{32}-h_{32} = 0 \\
    & h_{32} + m_{33}-s_{33}-h_{33} = 0 \\
    & h_{33} + m_{34}-s_{34}-h_{34} = 0 \\
    & h_{34} + m_{35}-s_{35}-h_{35} = 0 \\
    & h_{35} + m_{36}-s_{36}-h_{36} = 0 \\
    & m_{41}-s_{41}-h_{41} = 0 \\
    & h_{41} + m_{42}-s_{42}-h_{42} = 0 \\
    & h_{42} + m_{43}-s_{43}-h_{43} = 0 \\
    & h_{43} + m_{44}-s_{44}-h_{44} = 0 \\
    & h_{44} + m_{45}-s_{45}-h_{45} = 0 \\
    & h_{45} + m_{46}-s_{46}-h_{46} = 0 \\
    & m_{51}-s_{51}-h_{51} = 0 \\
    & h_{51} + m_{52}-s_{52}-h_{52} = 0 \\
    & h_{52} + m_{53}-s_{53}-h_{53} = 0 \\
    & h_{53} + m_{54}-s_{54}-h_{54} = 0 \\
    & h_{54} + m_{55}-s_{55}-h_{55} = 0 \\
    & h_{55} + m_{56}-s_{56}-h_{56} = 0 \\
    & m_{61}-s_{61}-h_{61} = 0 \\
    & h_{61} + m_{62}-s_{62}-h_{62} = 0 \\
    & h_{62} + m_{63}-s_{63}-h_{63} = 0 \\
    & h_{63} + m_{64}-s_{64}-h_{64} = 0 \\
    & h_{64} + m_{65}-s_{65}-h_{65} = 0 \\
    & h_{65} + m_{66}-s_{66}-h_{66} = 0 \\
    & m_{71}-s_{71}-h_{71} = 0 \\
    & h_{71} + m_{72}-s_{72}-h_{72} = 0 \\
    & h_{72} + m_{73}-s_{73}-h_{73} = 0 \\
    & h_{73} + m_{74}-s_{74}-h_{74} = 0 \\
    & h_{74} + m_{75}-s_{75}-h_{75} = 0 \\
    & h_{75} + m_{76}-s_{76}-h_{76} = 0 \\
    & h_{16}=\dots=h_{76} = 50 \\
    & h_{11} \leq 100, \dots, h_{76} \leq 100 \\
    & m_{11} \geq 0, \dots, m_{76} \geq 0 \\
    & h_{11} \geq 0, \dots, h_{76} \geq 0 \\
    & s_{11} \geq 0, \dots, s_{76} \geq 0.
\end{align*}
```

(p1l5:distribution)=
### Distribution Problem

In this problem, we are searching for a minimum cost distribution routing from two factories, in Helsinki and Jyväskylä, to depots and customers.
More specifically, there are four depots where we can store our product: in Turku, Tampere, Kuopio and Oulu.
In addition, we sell the product to six customers C1 to C6, who can be supplied from either a factory or a depot.

```{figure} ../figures/distribution.drawio.svg
:name: fig:distribution
Illustration of the distribution problem.
```

The costs associated with the distribution of the products are given in {numref}`p1l5:distibution_costs`.

```{table} Distribution costs (in € per tons delivered)
:name: p1l5:distibution_costs
|             | **Helsinki factory** | **Jyväskylä factory** | **Turku depot** | **Tampere depot** | **Kuopio depot** | **Oulu depot** |
|:-----------:|----------------------|----------------------|-----------------|-------------------|------------------|----------------|
|   _Depots_  |                      |                      |                 |                   |                  |                |
|  **Turku**  | 0.5                  | -                    |                 |                   |                  |                |
| **Tampere** | 0.5                  | 0.3                  |                 |                   |                  |                |
| **Kuopio**  | 1.0                  | 0.5                  |                 |                   |                  |                |
| **Oulu**    | 0.2                  | 0.2                  |                 |                   |                  |                |
| _Customers_ |                      |                      |                 |                   |                  |                |
| **C1**      | 1.0                  | 2.0                  | -               | 1.0               | -                | -              |
| **C2**      | -                    | -                    | 1.5             | 0.5               | 1.5              | -              |
| **C3**      | 1.5                  | -                    | 0.5             | 0.5               | 2.0              | 0.2            |
| **C4**      | 2.0                  | -                    | 1.5             | 1.0               | -                | 1.5            |
| **C5**      | -                    | -                    | -               | 0.5               | 0.5              | 0.5            |
| **C6**      | 1.0                  | -                    | 1.0             | -                 | 1.5              | 1.5            |
```

Each factory has a monthly supply capacity:
- Helsinki: 150000 tons
- Jyväskylä: 200000 tons

Each depot has a monthly throughput limit:
- Turku: 70000 tons
- Tampere: 50000 tons
- Kuopio: 100000 tons
- Oulu: 40000 tons

Lastly, each customer has a montly demand that must be met exactly:
- C1: 50000 tons
- C2: 10000 tons
- C3: 40000 tons
- C4: 35000 tons
- C5: 60000 tons
- C6: 20000 tons

What distribution pattern would minimize total cost?

#### Solution

% Add note about solving this as a minimum cost flow problem?

With the parameters described as above, we need to define some decision variables.
- $x_{ij}$ - Amount supplied from factory $i$ to depot $j$, $i=1,2$, $j=1,2,3,4$,
- $y_{ik}$ - Amount supplied from factory $i$ to customer $k$, $i=1,2$, $k=1,2,3,4,5,6$, and
- $z_{jk}$ - Amount supplied from depot $j$ to customer $k$, $j=1,2,3,4$, $k=1,2,3,4,5,6$,

where we enumerate the locations in the order they appear in the lists above.

Not all these routes are feasible. We can enforce these restrictions either by omitting the variables or by constraining them to be zero.

Our objective is to minimize distribution costs, which is given by

```{math}
\mini &f(x_{ij}, y_{ij}, z_{ij}) = \\
& 0.5x_{11}+0.5x_{12}+1.0x_{13}+0.2x_{14} + 0.3x_{22}+0.5x_{23}+0.2x_{24} \\
 + &1.0y_{11}+1.5y_{13}+2.0y_{14}+1.0y_{16} + 2.0y_{21} \\
 + &1.5z_{12}+0.5z_{13}+1.5z_{14}+1.0z_{16} + 1.0z_{21}+0.5z_{22}+0.5z_{23}+1.0z_{24}+0.5z_{25} \\
 + &1.5z_{32}+2.0z_{33}+0.5z_{35}+1.5z_{36} + 0.2z_{43}+1.5z_{44}+0.5z_{45}+1.5z_{46}.
```
There are a few constraints we need to account for.
Both factories have a capacity limiting their supply.
```{math}
x_{11}+x_{12}+x_{13}+x_{14}+y_{11}+y_{12}+y_{13}+y_{14}+y_{15}+y_{16} \leq 150000 \\
x_{21}+x_{22}+x_{23}+x_{24}+y_{21}+y_{22}+y_{23}+y_{24}+y_{25}+y_{26} \leq 200000
```

We also need to make sure depot throughput is obeyed, both in terms of what the depots are receiving
```{math}
x_{11}+x_{21} \leq 70000 \\
x_{12}+x_{22} \leq 50000 \\
x_{13}+x_{23} \leq 100000 \\
x_{14}+x_{24} \leq 40000
```
and in terms of what they are supplying
```{math}
z_{11}+z_{12}+z_{13}+z_{14}+z_{15}+z_{16} &= x_{11}+x_{21} \\
z_{21}+z_{22}+z_{23}+z_{24}+z_{25}+z_{26} &= x_{12}+x_{22} \\
z_{31}+z_{32}+z_{33}+z_{34}+z_{35}+z_{36} &= x_{13}+x_{23} \\
z_{41}+z_{42}+z_{43}+z_{44}+z_{45}+z_{46} &= x_{14}+x_{24}.
```

The last constraint is to make sure customers receive sufficient supply.
```{math}
y_{11}+y_{21}+z_{11}+z_{21}+z_{31}+z_{41} = 50000 \\
y_{12}+y_{22}+z_{12}+z_{22}+z_{32}+z_{42} = 10000 \\
y_{13}+y_{23}+z_{13}+z_{23}+z_{33}+z_{43} = 40000 \\
y_{14}+y_{24}+z_{14}+z_{24}+z_{34}+z_{44} = 35000 \\
y_{15}+y_{25}+z_{15}+z_{25}+z_{35}+z_{45} = 60000 \\
y_{16}+y_{26}+z_{16}+z_{26}+z_{36}+z_{46} = 20000
```

Our full model is thus
```{math}
\mini &f(x_{ij}, y_{ij}, z_{ij}) = \\
& 0.5x_{11}+0.5x_{12}+1.0x_{13}+0.2x_{14} + 0.3x_{22}+0.5x_{23}+0.2x_{24} \\
 & +1.0y_{11}+1.5y_{13}+2.0y_{14}+1.0y_{16} + 2.0y_{21} \\
 & +1.5z_{12}+0.5z_{13}+1.5z_{14}+1.0z_{16} + 1.0z_{21}+0.5z_{22}+0.5z_{23}+1.0z_{24}+0.5z_{25} \\
 & +1.5z_{32}+2.0z_{33}+0.5z_{35}+1.5z_{36} + 0.2z_{43}+1.5z_{44}+0.5z_{45}+1.5z_{46} \\
 \st &x_{11}+x_{12}+x_{13}+x_{14}+y_{11}+y_{12}+y_{13}+y_{14}+y_{15}+y_{16} \leq 150000 \\
  & x_{21}+x_{22}+x_{23}+x_{24}+y_{21}+y_{22}+y_{23}+y_{24}+y_{25}+y_{26} \leq 200000 \\
  & x_{11}+x_{21} \leq 70000 \\
  & x_{12}+x_{22} \leq 50000 \\
  & x_{13}+x_{23} \leq 100000 \\
  & x_{14}+x_{24} \leq 40000 \\
  & z_{11}+z_{12}+z_{13}+z_{14}+z_{15}+z_{16} = x_{11}+x_{21} \\
  & z_{21}+z_{22}+z_{23}+z_{24}+z_{25}+z_{26} = x_{12}+x_{22} \\
  & z_{31}+z_{32}+z_{33}+z_{34}+z_{35}+z_{36} = x_{13}+x_{23} \\
  & z_{41}+z_{42}+z_{43}+z_{44}+z_{45}+z_{46} = x_{14}+x_{24} \\
  & y_{11}+y_{21}+z_{11}+z_{21}+z_{31}+z_{41} = 50000 \\
  & y_{12}+y_{22}+z_{12}+z_{22}+z_{32}+z_{42} = 10000 \\
  & y_{13}+y_{23}+z_{13}+z_{23}+z_{33}+z_{43} = 40000 \\
  & y_{14}+y_{24}+z_{14}+z_{24}+z_{34}+z_{44} = 35000 \\
  & y_{15}+y_{25}+z_{15}+z_{25}+z_{35}+z_{45} = 60000 \\
  & y_{16}+y_{26}+z_{16}+z_{26}+z_{36}+z_{46} = 20000.
```