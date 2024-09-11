# Lecture 5 - Example Models

The examples below are based on {cite}`williams_model_2013`.

(p1l5:food)=
## Food Manufacture

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

Assume that at the start of January, we have a stock of 500 tons of each raw oil in storage.
We need to ensure that these stocks will exist at the end of June.
What 6-month production policy should we pursue to maximize profit?

### Solution

Recall our set of steps for modelling optimisation problems:

1. List **Parameters**;
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
\begin{align}
  \maxi & f(b_{ij}, u_{ij}, s_{ij}, p_j) = \\ 
        & -110b_{11} -130b_{12} -110b_{13} -120b_{14} -100b_{15} - 90b_{16} \\
        & -120b_{21} -130b_{22} -140b_{23} -110b_{24} -120b_{25} -100b_{26} \\
        & -130b_{31} -110b_{32} -130b_{33} -120b_{34} -150b_{35} -140b_{36} \\
        & -110b_{41} - 90b_{42} -100b_{43} -120b_{44} -110b_{45} - 80b_{46} \\
        & -115b_{51} -115b_{52} - 95b_{53} -125b_{54} -105b_{55} -135b_{56} \\
        & -5(s_{11}+\dots+s_{56}) \\
        & +150(y_1+y_2+y_3+y_4+y_5+y_6).
\end{align}
```
composed of costs of purchasing the oil, storage costs, and income from selling the blended product.

From our problem statement, we can see that there are four sources of constraints we must consider: linear production, processing limits, hardness constraints and the handling of storage.

Linear production just means that we produce as much product as we use oils in any given month $j$

```{math}
u_{1j}+u_{2j}+u_{3j}+u_{4j}+u_{5j} = p_j
```

The processing limits are easy, for month $j$ we need

```{math}
u_{1j}+u_{2j} \leq 200 \\
u_{3j}+u_{4j}+u_{5j} \leq 250.
```

The hardness constraints for month $j$ are also not complicated:

```{math}
8.8u_{1j}+6.1u_{2j}+2.0u_{3j}+4.2u_{4j}+5.0u_{5j} \leq 6y_j \\
8.8u_{1j}+6.1u_{2j}+2.0u_{3j}+4.2u_{4j}+5.0u_{5j} \geq 3y_j.
```

For storage, we link these variables together by the relation
```{math}
\text{quantity stored in month }(j-1) + \text{quantity bought in month }j

= \text{quantity used in month }j + \text{quantity stored in month }j.
```

In doing the above, we need to make the initial storage of 500 tons per oil available and ensure that it exists at the end as well.
Thus we obtain for oil $i$

```{math}
& b_{i1} -u_{i1}-s_{i1} &= -500 \\
s_{i1} +& b_{i2} -u_{i2}-s_{i2} &= 0 \\
s_{i2} +& b_{i3} -u_{i3}-s_{i3} &= 0 \\
s_{i3} +& b_{i4} -u_{i4}-s_{i4} &= 0 \\
s_{i4} +& b_{i5} -u_{i5}-s_{i5} &= 0 \\
s_{i5} +& b_{i6} -u_{i6} &=500.
```

There is also a storage limit for each type of oil, which we can implement by constraining the variables
```{math}
s_{11},\dots,s_{5,6}\leq 1000.
```

Lastly, since we cannot work with negative amounts of oil, we must add nonnegativity constraints in the definition of the decision variables. Thus, we must guarantee that $b_{ij} \ge 0, u_{ij} \ge 0,  s_{ij} \ge 0, p_j\ge 0$.

Putting it all together, the optimisation model that provides the maximum profit is given by

```{math}
\begin{align}
  \maxi & f(b_{ij}, u_{ij}, s_{ij}, p_j) = \\ 
        & -110b_{11} -130b_{12} -110b_{13} -120b_{14} -100b_{15} - 90b_{16} \\
        & -120b_{21} -130b_{22} -140b_{23} -110b_{24} -120b_{25} -100b_{26} \\
        & -130b_{31} -110b_{32} -130b_{33} -120b_{34} -150b_{35} -140b_{36} \\
        & -110b_{41} - 90b_{42} -100b_{43} -120b_{44} -110b_{45} - 80b_{46} \\
        & -115b_{51} -115b_{52} - 95b_{53} -125b_{54} -105b_{55} -135b_{56} \\
        & -5(s_{11}+\dots+s_{56}) \\
        & +150(y_1+y_2+y_3+y_4+y_5+y_6) \\
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
  & s_{11}, \dots, s_{56} \leq 1000 
\end{align}
```

(p1l5:production)=
## Factory Planning

In this example, we are at an engineering factory that makes seven different products.
The production processes of these involve the following machines:
- four grinders,
- two vertical drills,
- three horizontal drills,
- one borer, and
- one planer.

The process of making every product is different and different products require the use of machines differently.
Similarly, every product yields a certain net profit.
These figures are described in {numref}`p1l5:production_table`, where a dash means that the product doesn't use the indicated machine.

```{table} Production figures
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

In addition, due to market conditions, there are limits to how much of each product we can seel every month.

```{table} Limits on selling products
|                         | **Product 1** | **Product 2** | **Product 3** | **Product 4** | **Product 5** | **Product 6** | **Product 7** |
|:-----------------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|---------------|
|        **Profit**       | 500           | 1000          | 300           | 300           | 800           | 200           | 100           |
|       **Grinding**      | 600           | 500           | 200           | 0             | 400           | 300           | 150           |
|  **Vertical drilling**  | 300           | 600           | 0             | 0             | 500           | 400           | 100           |
| **Horizontal drilling** | 200           | 300           | 400           | 500           | 200           | 0             | 100           |
|        **Boring**       | 0             | 100           | 500           | 100           | 1000          | 300           | 0             |
|       **Planing**       | 500           | 500           | 100           | 300           | 1100          | 500           | 60            |
```

Once again, we can store products, up to 100 of each at a cost of €0.05 per unit per month.
However, this time we have no initial stock, but we would like to accumulate a one: 50 of each product by the end of June.

The factory works 24 days a month, each day containing two 8 hour shifts.

Assume that the production process can use the machines in any order.

Our objective is to determine a production schedule that maximises total profit.

### Solution

Once again, our list guides us.

1. List **Parameters**;
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
h_{16}=\dots=h_{76} = 50.
```

To model the amount of production, recall that the processes can use machines in any order.
This means that we can calculate the availability of each machine for every month in hours, and add a constraints to ensure they are not exceeded.
For example, our factory has four grinders, which multiplied with 24 days a month, 2 shifts a day and 8 hours a shift gives
```{math}
4\times 24 \times 2 \times 8 = 1536
```
hours available per month.
However, according to the maintenance schedule, in January and May we will have access to only three grinders, meaning the availability is
```{math}
3\times 24\times 2\times 8 = 1152
```
hours instead.
Thus we can write the constraints
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

Lastly, we need to link the manufacturing, holding and selling variables together.
We can only sell or store what is already available, either freshly manufactured or from the previous month's inventory, which is 0 in the first month. 
Thus for Product 1
```{math}
m_{11}-s_{11}-h_{11} &= 0 \\
h_{11} + m_{12}-s_{12}-h_{12} &= 0 \\
h_{12} + m_{13}-s_{13}-h_{13} &= 0 \\
h_{13} + m_{14}-s_{14}-h_{14} &= 0 \\
h_{14} + m_{15}-s_{15}-h_{15} &= 0 \\
h_{15} + m_{16}-s_{16}-h_{16} &= 0 \\
```
and identical constraints govern the other products.

Putting this all together, the optimisation model for the maximum profit production plan for the factory is given by

```{math}
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
```
(p1l5:combined)=
## Combined Production-Transporation Problem

In the transportation problem, we minimized the cost of transmiting electricity according to cities' demands with a set amount of supply.
In the production problem, we minimized the cost of producing electricity enough to satisfy the demand for it, without worrying about transportation costs.
Now we consider a problem where the objective is to minimize the cost, taking into account both the production and the transportation.

Suppose that there are 3 power plants, 4 cities, and a battery where we can store electricity in between quarters, electricity sent to which can only be used the next quarter.
We need to consider the costs associated with electricity production (let's say it depends on the plant and the quarter), costs for transmission from plants to cities or to the battery, costs for transmission from the battery to the cities, and costs for storing in the battery.
We would like to minimize the total costs, while ensuring that each city's electricity demand is satisfied.

Suppose the demand is the same as in , the additional parameters are as given below, and the cost of storing electricity is €1.

```{list-table} Transportation costs for the combined problem
:name: table_combined_transportation
:header-rows: 1
:stub-columns: 1
:widths: 25 20 20 20 20 20 25
:align: "right"

* - From \ To
  - City 1
  - City 2
  - City 3
  - City 4
  - Battery
  - Supply  
    (million kwh)
* - Plant 1
  - €8
  - €6
  - €10
  - €9
  - €6
  - 35
* - Plant 2
  - €9
  - €12
  - €13
  - €7
  - €4
  - 50
* - Plant 3
  - €14
  - €9
  - €16
  - €5
  - €8
  - 40
* - Battery
  - €4
  - €2
  - €7
  - €5
  -
  -
* - Demand  
    (million kwh)
  - 45
  - 20
  - 30
  - 30
  -
  - 
```

% Maybe make the production problem use these values, and just add link to it instead of a new table
```{list-table} Production costs for the combined problem
:name: table_combined_production
:header-rows: 1
:stub-columns: 1

* - 
  - Q1
  - Q2
  - Q3
  - Q4
* - Plant 1
  - €4
  - €2
  - €7
  - €3
* - Plant 2
  - €5
  - €8
  - €4
  - €2
* - Plant 3
  - €3
  - €6
  - €5
  - €8
```

### Solution

With the parameters described as above, we need to define some decision variables.
First is for production, which is simpler this time since we don't have overtime labor.
- $x_{ij}$ - amount of power produced at plant $i$ in quarter $j$, for $i=1,2,3$ and $j=1,2,3,4$.

Next is transportation, which can happen from power plants to cities, from plants to the battery, or from the battery to the cities.
- $p2c_{ijk}$ - amount of transporation from plant $i$ to city $k$ in quarter $j$, for $i=1,2,3$, $j=1,2,3,4$, and $k=1,2,3,4$,
- $p2b_{ij}$ - amount of transportation from plant $i$ to the battery in quarter $j$, for $i=1,2,3$ and $j=1,2,3,4$,
- $b2c_{jk}$ - amount of transportation from the battery to city $k$ in quarter $j$, for $j=1,2,3,4$ and $k=1,2,3,4$.

Lastly, we need to consider the use of the battery.
- $bat_j$ - amount of power stored in the battery at the end of quarter $j$, for $j=1,2,3,4$.

We can decompose the objective function into production, transportation and storage costs, the sum of which we want to minimise.
```{math}
p(x_{11},\dots,x_{34}) = & 4x_{11} + 2x_{12} + 7x_{13} + 3x_{14} + 5x_{21} + 8x_{22} + 4x_{23} + 2x_{24} + 3x_{31} + 6x_{32} + 5x_{33} + 8x_{34} \\
t(p2c_{ijk}, p2b_{ij}, b2c_{jk}) = & 8\sum_j p2c_{1j1} + 6\sum_j p2c_{1j2} + 10\sum_j p2c_ {1j3} + 9\sum_j p2c_{1j4} \\
& + 9\sum_j p2c_{2j1} + 12\sum_j p2c_{2j2} + 13\sum_j p2c_{2j3} + 7\sum_j p2c_{2j4} \\
& + 14\sum_j p2c_{3j1} + 9\sum_j p2c_{3j2} + 16\sum_j p2c_{3j3} + 8\sum_j p2c_{3j4} \\ 
& + 6\sum_j p2b_{1j} + 4\sum_j p2b_{2j} + 8\sum_j p2b_{3j} + 4\sum_j b2c_{j1} \\
& + 2\sum_j b2c_{j2} + 7\sum_j b2c_{j3} + 5\sum_j b2c_{j4} \\
s(bat_1,\dots,bat_4) = & bat_1 + bat_2 + bat_3 + bat_4 \\
```

```{math}
\mini f(x_{ij}, p2c_{ijk}, p2b_{ij}, b3c_{jk}, bat_j) = p(x_{ij}) + t(p2c_{ijk}, p2b_{ij}, b2c_{jk}) + s(bat_j)
```

The most immediate constraint is to meet the quarterly demands of the cities, using transmission from plants and the battery.
For example, for city 1 in the first quarter, we have
```{math}
p2c_{111} + p2c_{211} + p2c_{311} + p2c_{411} + b2c_{11} \geq 40.
```

This in turn highlights the need for sufficient production, i.e. we can only transmit as much electricity as we produce. 
For the first plant in the first quarter, this can be written as
```{math}
p2c_{111} + p2c_{112} + p2c_{113} + p2c_{114} + p2b_{11} = x_{11} 
```

Next, we need to ensure that the battery is used in a continuous manner, and the used and stored amounts make sense.
For the sake of writing the constraint neatly, suppose $bat_0=0$, then for quarter 1 we have
```{math}
bat_0 + p2b_{11} + p2b_{21} + p2b_{31} - b2c_{11} - b2c_{12} - b2c_{13} - b2c_{14} = bat_1
```

Finally, we need to ensure that electricity sent to the battery is used only in the later quarters.
This means that the amount of use in a given quarter cannot exceed what was in store at the end of the last quarter.
In the first quarter, this means
```{math}
b2c_{11} + b2c_{12} + b2c_{13} + b2c_{14} \leq bat_0
```
% In the above constraint, everything is necessarily 0. But modeling it this way is arguably clearer/simpler (at least for me). Should we take a note of this?

We should also not forget that all the variables here are non-negative.

All in all, we end up with the optimisation model
```{math}
\mini f(x_{ij}, p2c_{ijk}, p2b_{ij}, b3c_{jk}, bat_j) = & p(x_{ij}) + t(p2c_{ijk}, p2b_{ij}, b2c_{jk}) + s(bat_j) \\
\st & p2c_{111} + p2c_{211} + p2c_{311} + p2c_{411} + b2c_{11} \geq 40 \\
    & p2c_{121} + p2c_{221} + p2c_{321} + p2c_{421} + b2c_{21} \geq 60 \\
    & p2c_{131} + p2c_{231} + p2c_{331} + p2c_{431} + b2c_{31} \geq 75 \\
    & p2c_{141} + p2c_{241} + p2c_{341} + p2c_{441} + b2c_{41} \geq 25 \\
    & p2c_{112} + p2c_{212} + p2c_{312} + p2c_{412} + b2c_{12} \geq 95 \\
    & p2c_{122} + p2c_{222} + p2c_{322} + p2c_{422} + b2c_{22} \geq 20 \\
    & p2c_{132} + p2c_{232} + p2c_{332} + p2c_{432} + b2c_{32} \geq 45 \\
    & p2c_{142} + p2c_{242} + p2c_{342} + p2c_{442} + b2c_{42} \geq 85 \\
    & p2c_{113} + p2c_{213} + p2c_{313} + p2c_{413} + b2c_{13} \geq 60 \\
    & p2c_{123} + p2c_{223} + p2c_{323} + p2c_{423} + b2c_{23} \geq 25 \\
    & p2c_{133} + p2c_{233} + p2c_{333} + p2c_{433} + b2c_{33} \geq 90 \\
    & p2c_{143} + p2c_{243} + p2c_{343} + p2c_{443} + b2c_{43} \geq 30 \\
    & p2c_{114} + p2c_{214} + p2c_{314} + p2c_{414} + b2c_{14} \geq 55 \\
    & p2c_{124} + p2c_{224} + p2c_{324} + p2c_{424} + b2c_{24} \geq 40 \\
    & p2c_{134} + p2c_{234} + p2c_{334} + p2c_{434} + b2c_{34} \geq 40 \\
    & p2c_{144} + p2c_{244} + p2c_{344} + p2c_{444} + b2c_{44} \geq 50 \\
    & p2c_{111} + p2c_{112} + p2c_{113} + p2c_{114} + p2b_{11} = x_{11} \\
    & p2c_{121} + p2c_{122} + p2c_{123} + p2c_{124} + p2b_{12} = x_{12} \\
    & p2c_{131} + p2c_{132} + p2c_{133} + p2c_{134} + p2b_{13} = x_{13} \\
    & p2c_{141} + p2c_{142} + p2c_{143} + p2c_{144} + p2b_{14} = x_{14} \\
    & p2c_{211} + p2c_{212} + p2c_{213} + p2c_{214} + p2b_{21} = x_{21} \\
    & p2c_{221} + p2c_{222} + p2c_{223} + p2c_{224} + p2b_{22} = x_{22} \\
    & p2c_{231} + p2c_{232} + p2c_{233} + p2c_{234} + p2b_{23} = x_{23} \\
    & p2c_{241} + p2c_{242} + p2c_{243} + p2c_{244} + p2b_{24} = x_{24} \\
    & p2c_{311} + p2c_{312} + p2c_{313} + p2c_{314} + p2b_{31} = x_{31} \\
    & p2c_{321} + p2c_{322} + p2c_{323} + p2c_{324} + p2b_{32} = x_{32} \\
    & p2c_{331} + p2c_{332} + p2c_{333} + p2c_{334} + p2b_{33} = x_{33} \\
    & p2c_{341} + p2c_{342} + p2c_{343} + p2c_{344} + p2b_{34} = x_{34} \\
    & p2b_{11} + p2b_{21} + p2b_{31} - b2c_{11} - b2c_{12} - b2c_{13} - b2c_{14} = bat_1 \\
    & bat_1 + p2b_{12} + p2b_{22} + p2b_{32} - b2c_{21} - b2c_{22} - b2c_{23} - b2c_{24} = bat_2 \\
    & bat_2 + p2b_{13} + p2b_{23} + p2b_{33} - b2c_{31} - b2c_{32} - b2c_{33} - b2c_{34} = bat_3 \\
    & bat_3 + p2b_{14} + p2b_{24} + p2b_{34} - b2c_{41} - b2c_{42} - b2c_{43} - b2c_{44} = bat_4 \\
    & b2c_{11} + b2c_{12} + b2c_{13} + b2c_{14} \leq 0 \\
    & b2c_{21} + b2c_{22} + b2c_{23} + b2c_{24} \leq bat_1 \\
    & b2c_{31} + b2c_{32} + b2c_{33} + b2c_{34} \leq bat_2 \\
    & b2c_{41} + b2c_{42} + b2c_{43} + b2c_{44} \leq bat_3 \\
    & x_{11},\dots,x_{34} \geq 0 \\
    & p2c_{111},\dots,p2c_{344} \geq 0 \\
    & p2b_{11},\dots,p2b_{34} \geq 0 \\
    & b2c_{11},\dots,b2c_{44} \geq 0 \\
    & bat_1, bat_2, bat_3, bat_4 \geq 0
```

Even though this problem is conceptionally not very difficult and the model not complicated, it exemplifies how models can get very large and difficult to keep track of very quickly.
In the next lecture, we will discuss how to formulate problems so that they are easier to work with.