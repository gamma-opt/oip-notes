# Introduction

Every aspect of our lives is permeated by decisions we are constantly making. Small decisions such as whether to bring an umbrella with us, or big decisions, such as choosing a house to buy, share many of the features that make decisions hard. And, once we go to a scale where the decisions affect not only our own lives, but whole systems and potentially the lives of many, things can quickly get overwhelming.

First, there is the notion of *complexity*. Often decisions are tangled in a system of multiple moving parts that are far too complicated to be fully grasped. Typically, we have a good idea of the local and immediate consequence of our decisions, but it quickly becomes far too complicated when we try to understand the consequences to the overall system.

On top of that, there is *uncertainty*. Not being sure about the future is a big component in why we hesitate to make some decisions. Like bringing an umbrella with you, which would be highly beneficial if it indeed rains while you are outside, but a nuisance otherwise. Most decisions have to be made without the knowledge of how the future will unveil.

Finally, there is the notion of *consequence*. Measuring the consequence of our decisions requires understanding how the parts move together and having a description of how the uncertainty behaves, so then we can clearly see how alternative compares, and ultimately choose the best decision.

This course is about how we can use mathematics to quantify how complex systems behave under uncertainty and, hopefully, make better decisions.

## The science of decision-making

The idea of bringing science to decision making is the main motto of a field called Operations Research. Basically, one is interested in understanding how analytical reasoning can be used to quantify the consequences of decisions such that they can be compared and best courses of action can be taken.

The approach is very much like other fields of science. We perform experiments under controlled conditions and observe the results, so we can reason about hypotheses. The main difference is that our experiments cannot be done using test tubes and laboratories, since we cannot simply use trial and error on real-life systems without consequences. That would be akin to repeatedly building, and destroying, say, depots at different places to decide which distribution network configuration is the best, which is an obviously impractical approach. That is why we must rely on models.

But instead or cardboard and styrofoam, these models are built using **mathematical equations** that can represent the relationship between parts and logical implications associated with each decision. Once we have this mathematical representation, it can be coded to a computer to form a digital twin with which we can perform experiments otherwise infeasible in the physical world. Because these digital twins are essentially mathematical equations, we can use mathematical techniques to shift the system towards optimal configurations.

```{figure} ../figures/scientific-method-scheme.drawio.svg
:name: scientific-method
:align: center

A comparison between the scientific method (on the left) and the process of developing mathematical programming models to support decision making
```

{numref}`scientific-method` illustrates the parallels between the scientific method (on the left) and the process of devising optimisation models to support decision making. The colours are meant to indicate which step relate to which. The extra line on the right relates to the fact that often, as it is the case of most other applied sciences, a few iterations reflecting on whether the model represents sufficiently well the problem might take course. 
 
## What is mathematical optimisation?  

Mathematical optimisation is an area of applied mathematics interested in understanding the properties that functions have and how these can be exploited to find points where their values are minimum or maximum within a given region or the whole domain of the function. Once these properties are known, we can state the conditions that are required for a point to be a maximal or minimal point, and design algorithms that can search for that point.

```{figure} ../figures/optimisation.gif
:name: optimisation-gif
:align: center

Animation representing the process of looking for the optimal solution of a function within a specific domain
```
{numref}`optimisation-gif` shows an example, where the function we are trying to optimise is represented by level curves, like in a map, with lighter colours representing regions with larger values, and darker colours lower values. The algorithm is being employed to find a point with minimum value while guaranteeing that the search returns a solution within the blue boundaries.

```{note}
The algorithm used in this animation is called projected gradient. We will cover gradient methods later on in our course. 
```

You might be asking yourself: what does that have to do with optimal decisions? 

## Mathematical programming: modelling decision-making problems using mathematical optimisation

Turns out that we can use a really powerful analogy to connect decision making and mathematical optimisation. We can think that the coordinates of the point in our domain represent decisions we must make, such as how much of a given product we must produce or what capacity should we allocate to a production plant. The search region is made of conditions that represent, say, safety requirements, or physical limitations that have to be imposed in the decisions we make. Last, we can have the function measuring the quality of a solution, for example the total cost of operating a given production system, or the expected service level it would provide.

This analogy is broadly known as **mathematical programming**, which is one of the main topic of our course. Simply put, mathematical programming is a language in which we use this analogy to build mathematical models representing the problem we have at hand, posing it in a form of a mathematical optimisation problem that, in turn, allows us to understand what are the optimal decisions that can be made for that system.

This course is precisely about being able to represent real-world problems via mathematical programming, so they can be optimised accordingly. This is a powerful paradigm that builds upon several mathematical concepts. Let us start by covering the most fundamental of them, but it will not be long before we are able to pose and solve our first optimisation model.