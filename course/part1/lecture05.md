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
| January  | 110   | 120   | 130   | 110   | 115   |
| February | 130   | 130   | 110   | 90    | 115   |
| March    | 110   | 140   | 130   | 100   | 95    |
| April    | 120   | 110   | 120   | 120   | 125   |
| May      | 100   | 120   | 150   | 110   | 105   |
| June     | 90    | 100   | 140   | 80    | 95    |
```
The final product sells at €150 per ton.

We can process a maximum of 200 tons of vegetable oil and 250 tons of non-vegetable oil in any given month. In addition, we can store up to 1000 tons of each raw oil for later use at a cost of €5 per ton per month.

Lastly, we need to ensure that the resulting product has appropriate hardness, which should be in between 3 and 6 units.
Hardness blends linearly with the input oils, which have the hardness values

```{list-table} Oil hardness values
:header-rows: 0

* - VEG 1
  - 8.8
* - VEG 2
  - 6.1
* -
  -
* - OIL 1
  - 2.0
* - OIL 2
  - 4.2
* - OIL 3
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
## Production Planning

%TODO: Tweak the problem so that we can obtain more interesting solutions?

Upon our success, Powerco approaches us with another project at a different location.
In this location, we again have 3 plants and 4 cities, however we are asked to make a quarterly electricity production plan for the entire year.
{numref}`table_production_demand` contains the projected demand from each of the 4 cities over next year, all of which must be satisfied exactly.


```{list-table} Projected demand from the cities in terawatts
:name: table_production_demand
:header-rows: 1
:stub-columns: 1

* - 
  - Q1
  - Q2
  - Q3
  - Q4
* - City 1
  - 40
  - 60
  - 75
  - 25
* - City 2
  - 95
  - 20
  - 45
  - 85
* - City 3
  - 60
  - 25
  - 90
  - 30
* - City 4
  - 55
  - 40
  - 40
  - 50
```

{numref}`table_production_cost` contains the expected costs of producing electricity in each of the 3 facilities, taking into account costs that change over the year.

```{list-table} Costs of producing a terawatt of electricity (in thousands)
:name: table_production_cost
:header-rows: 1
:stub-columns: 1

* - 
  - Q1
  - Q2
  - Q3
  - Q4
* - Plant 1
  - €8
  - €6
  - €10
  - €9
* - Plant 2
  - €9
  - €12
  - €13
  - €7
* - Plant 3
  - €14
  - €9
  - €15
  - €5
```

In a given quarter, plant 1 can produce 60 terawatts of electricity with regular-time labor, plant 2 can produce 80, and plant 3 can produce 50.
In addition, each plant can produce more electricity with overtime labor, at an additional cost of €50000 per terawatts.
Lastly, there is a battery inventory shared across plants where any excess electricity can be stored at a cost of €10000 per terawatt.
At the beginning of the first quarter, the inventory contains 50 terawatts.
Both the inventory and all the plans work with whole number units only.

### Solution

Once again, our list guides us.

1. List **Parameters**;
2. Define **decision variables**; 
3. Formulate **objective function**;
4. Formulate **constraints**.

The parameters are listed in the tables and the text above.
Our task is to decide quarterly electricity production for each plant throughout the year.
However, we need to be careful about keeping track of different modes of production:
each plant can produce electricity with either regular-time or overtime labor, which have different limits and costs.
A simple solution is to keep track of this production in separate variables.

Another lever in our control is the battery usage, which can be used either to make up for lacking supply in meeting the demand of a quarter, or deposit oversupply to be used later.
Since transportation costs are not a factor in this problem and we only need to meet demand, we can follow only the amount of electricity in the battery at the end of the quarter.
If it is less than the previous quarter, we know it was used to meet demand, and if it is more, it must be storing additional supply.

Consequently, we define:

- $x_{ij}$ - amount of power produced with regular-time labor at plant $i$ in quarter $j$, for $i=1,2,3$ and $j=1,2,3,4$,
- $y_{ij}$ - amount of power produced with overtime labor at plant $i$ in quarter $j$, for $i=1,2,3$ and $j=1,2,3,4$, and
- $s_j$ - amount of power stored in the battery at the end of quarter $j$, for $j=1,2,3,4$.

Our objective function is the _minimisation_ of the total cost of the production schedule, which involves the costs of regular- and overtime labor, and the use of battery.

```{math}
\mini & f(x_{ij}, y_{ij}, s_i) = \\ 
      & 8x_{11} + 6x_{12} + 10x_{13} + 9x_{14} + 9x_{21} + 12x_{22} + 13x_{23} + 7x_{24} + 14x_{31} + 9x_{32} + 16x_{33} + 5x_{34} \\
      & + (8+50)y_{11} + (6+50)y_{12} + (10+50)y_{13} + (9+50)y_{14} + (9+50)y_{21} + (12+50)y_{22} + (13+50)y_{23} + (7+50)y_{24} + (14+50)y_{31} + (9+50)y_{32} + (16+50)y_{33} + (5+50)y_{34} \\
      & + 10s_1 + 10s_2 + 10s_3 + 10s_4
```

There are multiple constraints we need to keep track of.
The basic one is that none of the decision variables we defined can be negative, imposing a lower bound on each: $x_{ij},y_{ij},s_j\geq 0$.
In addition, each factory has a limited capacity for regular-time labor, which gives an upper bound as well: $x_{1j}\leq 60, x_{2j}\leq 80, x_{3j}\leq 50$.

Note that we are given a starting inventory as well, which we can keep track in a consistent manner as the above with $s_0=50$.

Next, we need to ensure that the demand is met.
In any quarter, we need to use the produced electricity along with the stored electricity from the previous quarter to meet the demands of the four cities, with any leftovers going back to the battery.
We can express these quarterly constraints as follows:

```{math}
s_0 + \sum_i \big( x_{i1} + y_{i1} \big) - s_1 = 40+95+60+55 \\
s_1 + \sum_i \big( x_{i2} + y_{i2} \big) - s_2 = 60+20+25+40 \\
s_2 + \sum_i \big( x_{i3} + y_{i3} \big) - s_3 = 75+45+90+40 \\
s_3 + \sum_i \big( x_{i4} + y_{i4} \big) - s_4 = 25+85+30+50 
```

These constraints not only enforce meeting the demand of cities (along with the nonnegativity of the variables), but also ensure the battery is used in a continuous manner, since they explicitly code the quarterly difference in battery to be related to production and demand.

Putting this all together, the optimisation model for the minimum cost electricity production plan for Powerco is given by

```{math}
\mini & f(x_{ij}, y_{ij}, s_i) = \\ 
      & 8x_{11} + 6x_{12} + 10x_{13} + 9x_{14} + 9x_{21} + 12x_{22} + 13x_{23} + 7x_{24} + 14x_{31} + 9x_{32} + 16x_{33} + 5x_{34} \\
      & + (8+50)y_{11} + (6+50)y_{12} + (10+50)y_{13} + (9+50)y_{14} + (9+50)y_{21} + (12+50)y_{22} + (13+50)y_{23} + (7+50)y_{24} + (14+50)y_{31} + (9+50)y_{32} + (16+50)y_{33} + (5+50)y_{34} \\
      & + 10s_1 + 10s_2 + 10s_3 + 10s_4 \\
\st & s_0 + \sum_i \big( x_{i1} + y_{i1} \big) - s_1 = 250 \\
    & s_1 + \sum_i \big( x_{i2} + y_{i2} \big) - s_2 = 145 \\
    & s_2 + \sum_i \big( x_{i3} + y_{i3} \big) - s_3 = 250 \\
    & s_3 + \sum_i \big( x_{i4} + y_{i4} \big) - s_4 = 190 \\
    & 60 \geq x_{11},\dots,x_{14}\geq 0 \\
    & 80 \geq x_{21},\dots,x_{24}\geq 0 \\
    & 50 \geq x_{31},\dots,x_{34}\geq 0 \\
    & y_{11},\dots,y_{34}\geq 0 \\
    & s_1,\dots,s_4\geq 0 \\
    & s_0 = 50
```
(p1l5:combined)=
## Combined Production-Transporation Problem

In the transportation problem, we minimized the cost of transmiting electricity according to cities' demands with a set amount of supply.
In the production problem, we minimized the cost of producing electricity enough to satisfy the demand for it, without worrying about transportation costs.
Now we consider a problem where the objective is to minimize the cost, taking into account both the production and the transportation.

Suppose that there are 3 power plants, 4 cities, and a battery where we can store electricity in between quarters, electricity sent to which can only be used the next quarter.
We need to consider the costs associated with electricity production (let's say it depends on the plant and the quarter), costs for transmission from plants to cities or to the battery, costs for transmission from the battery to the cities, and costs for storing in the battery.
We would like to minimize the total costs, while ensuring that each city's electricity demand is satisfied.

Suppose the demand is the same as in {numref}`table_production_demand`, the additional parameters are as given below, and the cost of storing electricity is €1.

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