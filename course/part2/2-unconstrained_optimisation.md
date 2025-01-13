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
  display_name: Julia 1.10.3
  language: julia
  name: julia-1.10
---

# Unconstrained optimisation methods

## Gradient descent and variants

We have seen in {numref}`p2l1` that the gradient {math}`\nabla f(x_0)` describes the direction of steepest ascent at some point {math}`x_0`.
A consequence of this is that the negative gradient {math}`-\nabla f(x_0)` corresponds to the direction of the steepest descent at {math}`x_0`.

````{admonition} Why? Linearity of Differentiation
:class: seealso, dropdown
A function being differentiable means that it can be locally well-approximated with a linear function. So consider a line (or a plane for a multivariate function): the directions of steepest ascent and descent are necessarily opposite in this case, and thus the same holds **locally** for a differentiable function as well.

Exploring this idea further leads to the fact that differentiation is a linear operation, which formalizes the above intuition with
```{math}
\nabla -f(x_0) &= \nabla (-1 \cdot f(x_0)) \\
&= -1 \nabla f(x_0) = -\nabla f(x_0)
```
which means that the direction of steepest ascent for a function {math}`f` must necessarily be the direction of steepest descent for {math}`-f`.
````

Suppose we want to optimise a differentiable function.
The gradient provides a straightforward and greedy approach to doing so: calculate the correct direction, take a step, and repeat until some convergence criterion is satisfied.
```{prf:algorithm} Gradient descent
:label: alg:gd
**Inputs** Objective {math}`f`, initial point {math}`x_0`, convergence criterion `converged`.
1. {math}`k=0`
2. **while** not `converged()`:
    1. {math}`d=-\frac{\nabla f(x_k) }{ \|\nabla f(x_k) \| }`
    2. Determine step size / learning rate {math}`\lambda`
    3. {math}`x_{k+1}=x_k+\lambda d`
    4. {math}`k=k+1`
3. **return** {math}`x_k`.
```

There are a number of noteworthy aspects of {prf:ref}`alg:gd`.
First is that it is specifically for gradient **descent**, since in line 2.1 the derivative term has a negative sign.
Gradient ascent is the same algorithm with the sign flipped.
Second is that the derivative is normalized with its norm.
This is due to the fact that we are only interested in the direction information from the derivative, and the magnitude is decided by the step size in line 2.2.
This decision can be made dynamically at every step, using exact or inexact line search methods (TODO: Add ref to heuristics lecture), or a set learning rate may be set as an algorithm parameter.

Gradient descent is simple and straightforward, it be highly sensitive to the step size selection or the curvature of the objective function.
However, it also provides a solid foundation for extensions.
One ubiquitious example is _stochastic_ gradient descent, where the gradient is approximated by a random selection of partial derivatives, reducing the computational burden significantly.

```{margin}
Note the normalization by the norm in {prf:ref}`alg:sgd` line 2.2.
Here the idea is the same as before: the normalized gradient provides the direction, and the step size provides the magnitude.
In many implementations of SGD however, the gradient is left unnormalized, in which case step size is influenced or even fully determined by its magnitude.
```

```{prf:algorithm} Stochastic Gradient descent
:label: alg:sgd
**Inputs** Objective {math}`f`, initial point {math}`x_0`, convergence criterion `converged`.
1. {math}`k=0`
2. **while** not `converged()`:
    1. Pick an observation $i$ randomly.
    2. {math}`d=-\frac{\nabla_i f(x_k) }{ \|\nabla_i f(x_k) \| }`
    3. Determine step size / learning rate {math}`\lambda`
    4. {math}`x_{k+1}=x_k+\lambda d`
    5. {math}`k=k+1`
3. **return** {math}`x_k`.
```

Another variation is the _momentum method_, which modify the update step to incorporate information about previous iterations, imitating accelaration and deceleration caused for example by gravity on an object falling down a slope.
If the slope remains the same, the object will gain speed, and if the slope direction changes, the object won't abandon its previous direction entirely.

```{prf:algorithm} Gradient descent with momentum
:label: alg:gd_momentum
**Inputs** Objective {math}`f`, initial point {math}`x_0`, convergence criterion `converged`, momentum decay {math}`\beta`.
1. {math}`k=0, m_0=0`
2. **while** not `converged()`:
    1. {math}`d=-\frac{\nabla f(x_k) }{ \|\nabla f(x_k) \| }`
    2. Determine step size / learning rate {math}`\lambda`
    3. {math}`m_{k+1} = \beta m_k + \lambda d`
    4. {math}`x_{k+1}=x_k+m_{k+1}`
    5. {math}`k=k+1`
3. **return** {math}`x_k`.
```
Here, the momentum decay factor {math}`\beta` is between 0 and 1 and controls the momentum influence.

Going back to the determination of the learning rate, line search may not work well for all complicated functions.
An alternative idea is to determine it based on gradient information.
For example, we can start with an aggressive learning rate, and decrease it once loss decreases significantly, such as in {numref}`fig:adaptive-lr`.

```{code-cell}
---
mystnb:
  figure:
    name: fig:adaptive-lr
    caption: |
      The learning rate is constant in the flat region but decreases once loss starts to decrease.
tags: [remove-input]
---
using CairoMakie

x = range(-5, 5, 101)
f = x -> -exp(-x^2)
df = x -> 2x*exp(-x^2)
fig = Figure()

ax = Axis(fig[1,1])
lines!(ax, x, f)

xs = [-5, -4, -3, -2, -1.25, -1, -0.80, -0.65, -0.55, -0.47, -0.40]
scatter!(ax, xs, f; color = Makie.wong_colors()[2])

fig
```

There are multiple ways of implementing such a mechanism, one is to keep a decaying average of the previous gradients
```{math}
\lambda^k = \beta_\lambda \lambda^{k-1}+(1-\beta_\lambda)\nabla f(x_k)
```
where $0\leq \beta_\lambda\leq 1$ is some decay parameter.
Here, with more iterations, older values of the gradient will be practically zero, thus only the more recent figures will affect the final result.
Consequently, if a flat region is encountered after a rapid descent, the learning rate will go up again as needed.
```{margin}
Using the decaying average of gradients without momentum leads to an algorithm called _RMSProp_.
```
Combining this idea of the "adaptive gradient" with momentum gives a commonly used optimizer called _Adam_ (from "adaptive moments").

```{prf:algorithm} Adam
:label: alg:adam
**Inputs** Objective {math}`f`, initial point {math}`x_0`, convergence criterion `converged`, momentum decay {math}`\beta`, base learning rate $\lambda$, learning rate decay {math}`\beta_\lambda`.
1. {math}`k=0, m_0=0`
2. **while** not `converged()`:
    1. {math}`d=-\frac{\nabla f(x_k) }{ \|\nabla f(x_k) \| }`
    2. {math}`\lambda^k = \lambda (\delta+\beta_\lambda \lambda^{k-1}+(1-\beta_\lambda) \nabla f(x_k)^2)^{-1/2}`
    3. {math}`m_{k+1} = \beta m_k + \lambda d`
    4. {math}`x_{k+1}=x_k+m_{k+1}`
    5. {math}`k=k+1`
3. **return** {math}`x_k`.
```
Here, $\delta$ is a small scalar used to ensure we don't divide by 0.

```{margin}
Adapted from [Emilien Dupont's code](https://emiliendupont.github.io/2018/01/24/optimization-visualization/).
```

% This requires `d3.v4.js `, which is currently provided via _config.yml.
% TODO: Add number of steps
% TODO: Add marker to final point to show where it converged
% TODO: Add multiple functions to choose from?
```{raw} html
<body>
<div id="d3-gd"></div>
<select name="gd-func"></select>
</body>
<style>
.sgd {
    stroke: black;
}

.momentum {
    stroke: blue;
}

.rmsprop {
    stroke: red;
}

.adam {
    stroke: green;
}

.SGD {
    fill: black;
}

.Momentum {
    fill: blue;
}

.RMSProp {
    fill: red;
}

.Adam {
    fill: green;
}

circle:hover {
  fill-opacity: .3;
}
</style>
<body>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="https://d3js.org/d3-contour.v1.min.js"></script>
<script src="https://d3js.org/d3-scale-chromatic.v1.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjs/13.0.0/math.min.js"></script>
<script>

/* Constants */

const width = 800,
    height = 500,
    nx = parseInt(width / 5), // grid sizes
    ny = parseInt(height / 5),
    h = 1e-7, // step used when approximating gradients
    drawing_time = 30; // max time to run optimization

// Parameters describing where function is defined
const domain_x = [-2, 2],
    domain_y = [-2, 2],
    domain_f = [-2, 8],
    contour_step = 0.5; // Step size of contour plot

const scale_x = d3.scaleLinear()
                .domain([0, width])
                .range(domain_x);

const scale_y = d3.scaleLinear()
                .domain([0, height])
                .range(domain_y);

const thresholds = d3.range(domain_f[0], domain_f[1], contour_step);

const contours = d3.contours()
    .size([nx, ny])
    .thresholds(thresholds);

const color_scale = d3.scaleLinear()
    .domain(d3.extent(thresholds))
    .interpolate(function() { return d3.interpolateYlGnBu; });

/* Value of f at (x, y) */
function f(x, y) {
    return -2 * Math.exp(-((x - 1) * (x - 1) + y * y) / .2) + -3 * Math.exp(-((x + 1) * (x + 1) + y * y) / .2) + x * x + y * y;
}

/* Returns gradient of f at (x, y) */
function grad_f(f,x,y) {
    let grad_x = (f(x + h, y) - f(x, y)) / h
        grad_y = (f(x, y + h) - f(x, y)) / h
    return [grad_x, grad_y];
}

function hess_f(f,x,y) {
    const xx = (f(x + h, y) - 2*f(x, y) + f(x - h, y)) / (h * h),
          xy = (f(x + h, y + h) - f(x, y + h) - f(x + h, y) + f(x, y)) / (h * h),
          yy = (f(x, y + h) - 2*f(x, y) + f(x, y - h)) / (h * h);
    return [[xx, xy], [xy, yy]];
}


const func_names = ["Two Gaussians", "Rosenbrock", "Himmelblau"];
const funcs = {
    "Two Gaussians": [
        function f(x,y) {
            return -2 * Math.exp(-((x - 1) * (x - 1) + y * y) / .2) + -3 * Math.exp(-((x + 1) * (x + 1) + y * y) / .2) + x * x + y * y;
        }, get_values
    ],
    "Rosenbrock":
        function f(x,y) {
            return (1-x)*(1-x) + 100*(y-x*x)*(y-x*x);
        },
    "Himmelblau":
        function f(x,y) {
            return (6.25*x*x+2*y-11)*(6.25*x*x+2*y-11) + (2.5*x+4*y*y-7)*(2.5*x+4*y*y-7);
        }
}

d3.select('select[name="gd-func"]')
    .on('change', function() {
        const func = d3.select(this).property('value');
        create_interactive_plot("#d3-gd", gradient_container, funcs[func]);
        })
    .selectAll('option')
    .data(func_names)
    .enter()
    .append('option')
    .attr('value', d=>d)
    .text(d => d);




/* Returns values of f(x,y) at each point on grid as 1 dim array. */
function get_values(fun, nx, ny) {
    let grid = new Array(nx * ny);
    for (i = 0; i < nx; i++) {
        for (j = 0; j < ny; j++) {
            let x = scale_x( parseFloat(i) / nx * width ),
                y = scale_y( parseFloat(j) / ny * height );
            // Set value at ordering expected by d3.contour
            grid[i + j * nx] = fun(x, y);
        }
    }
    return grid;
}


function draw_contour(selector, mousedown_fn, obj_f) {
    const svg = d3.select(selector)
                  .append("svg")
                  .attr("width", width)
                  .attr("height", height);

    const function_g = svg.append("g").on("mousedown", mousedown_fn);

    let f_values = get_values(obj_f, nx, ny);

    function_g.selectAll("path")
            .data(contours(f_values))
            .enter().append("path")
            .attr("d", d3.geoPath(d3.geoIdentity().scale(width / nx)))
            .attr("fill", function(d) { return color_scale(d.value); })
            .attr("stroke", "none");
    
    return svg;
}

function create_menu(svg, labels) {
    const menu_g = svg.append("g");
    let draw_state = Object.fromEntries(labels.map(x => [x, true]));

    function press () {
        let type = d3.select(this).attr("class");
        if (draw_state[type]) {
            d3.select(this).attr("fill-opacity", 0);
            draw_state[type] = false;
        } else {
            d3.select(this).attr("fill-opacity", 0.5)
            draw_state[type] = true;
        }
    }

    menu_g.append("rect")
        .attr("x", 0)
        .attr("y", height - 40)
        .attr("width", width)
        .attr("height", 40)
        .attr("fill", "white")
        .attr("opacity", 0.2);

    menu_g.selectAll("circle")
        .data(labels)
        .enter()
        .append("circle")
        .attr("cx", function(d,i) { return width/labels.length  * (i + 0.25);} )
        .attr("cy", height - 20)
        .attr("r", 10)
        .attr("stroke-width", 0.5)
        .attr("stroke", "black")
        .attr("class", function(d) { console.log(d); return d;})
        .attr("fill-opacity", 0.5)
        .attr("stroke-opacity", 1)
        .on("mousedown", press);

    menu_g.selectAll("text")
        .data(labels)
        .enter()
        .append("text")
        .attr("x", function(d,i) { return width/labels.length * (i + 0.25) + 18;} )
        .attr("y", height - 14)
        .text(function(d) { return d; })
        .attr("text-anchor", "start")
        .attr("font-family", "Helvetica Neue")
        .attr("font-size", 15)
        .attr("font-weight", 200)
        .attr("fill", "white")
        .attr("fill-opacity", 0.8);

    return draw_state;
}

// these functions should accept x0, y0, plus anything more specified here
const gradient_container = {
    "SGD": [get_sgd_path, 2e-2, 500],
    "Momentum": [get_momentum_path, 1e-2, 200, 0.8],
    "RMSProp": [get_rmsprop_path, 1e-2, 300, 0.99, 1e-6],
    "Adam": [get_adam_path, 1e-2, 100, 0.7, 0.999, 1e-6]
}

function create_interactive_plot(selector, method_container, obj_f) {
    const svg = draw_contour(selector, mouse_fn, obj_f);
    let draw_state = create_menu(svg, Object.keys(method_container));
    const path_g = svg.append("g");

    function mouse_fn(event) {
        const point = d3.pointer(event);
        minimize(scale_x(point[0]), scale_y(point[1]));
    }

    function minimize(x0,y0) {
        path_g.selectAll("path").remove();
        for (const [name, [f, ...rest]] of Object.entries(method_container)){
            if (draw_state[name]) {
                let data = f(obj_f, x0, y0, ...rest);
                draw_path(data, name.toLowerCase(), path_g)
            }
        }
    }
}

create_interactive_plot("#d3-gd", gradient_container, f);


/*
 * Set up optimization/gradient descent functions.
 * SGD, Momentum, RMSProp, Adam.
 */

function get_sgd_path(f, x0, y0, learning_rate, num_steps) {
    let sgd_history = [{"x": scale_x.invert(x0), "y": scale_y.invert(y0)}];
    let x1, y1, gradient;
    for (i = 0; i < num_steps; i++) {
        gradient = grad_f(f, x0, y0);
        x1 = x0 - learning_rate * gradient[0]
        y1 = y0 - learning_rate * gradient[1]
        sgd_history.push({"x" : scale_x.invert(x1), "y" : scale_y.invert(y1)})
        x0 = x1
        y0 = y1
    }
    return sgd_history;
}

function get_momentum_path(f, x0, y0, learning_rate, num_steps, momentum) {
    let v_x = 0,
        v_y = 0;
    let momentum_history = [{"x": scale_x.invert(x0), "y": scale_y.invert(y0)}];
    let x1, y1, gradient;
    for (i=0; i < num_steps; i++) {
        gradient = grad_f(f, x0, y0)
        v_x = momentum * v_x - learning_rate * gradient[0]
        v_y = momentum * v_y - learning_rate * gradient[1]
        x1 = x0 + v_x
        y1 = y0 + v_y
        momentum_history.push({"x" : scale_x.invert(x1), "y" : scale_y.invert(y1)})
        x0 = x1
        y0 = y1
    }
    return momentum_history
}

function get_rmsprop_path(f, x0, y0, learning_rate, num_steps, decay_rate, eps) {
    let cache_x = 0,
        cache_y = 0;
    let rmsprop_history = [{"x": scale_x.invert(x0), "y": scale_y.invert(y0)}];
    let x1, y1, gradient;
    for (i = 0; i < num_steps; i++) {
        gradient = grad_f(f, x0, y0)
        cache_x = decay_rate * cache_x + (1 - decay_rate) * gradient[0] * gradient[0]
        cache_y = decay_rate * cache_y + (1 - decay_rate) * gradient[1] * gradient[1]
        x1 = x0 - learning_rate * gradient[0] / (Math.sqrt(cache_x) + eps)
        y1 = y0 - learning_rate * gradient[1] / (Math.sqrt(cache_y) + eps)
        rmsprop_history.push({"x" : scale_x.invert(x1), "y" : scale_y.invert(y1)})
        x0 = x1
        y0 = y1
    }
    return rmsprop_history;
}

function get_adam_path(f, x0, y0, learning_rate, num_steps, beta_1, beta_2, eps) {
    let m_x = 0,
        m_y = 0,
        v_x = 0,
        v_y = 0;
    let adam_history = [{"x": scale_x.invert(x0), "y": scale_y.invert(y0)}];
    let x1, y1, gradient;
    for (i = 0; i < num_steps; i++) {
        gradient = grad_f(f, x0, y0)
        m_x = beta_1 * m_x + (1 - beta_1) * gradient[0]
        m_y = beta_1 * m_y + (1 - beta_1) * gradient[1]
        v_x = beta_2 * v_x + (1 - beta_2) * gradient[0] * gradient[0]
        v_y = beta_2 * v_y + (1 - beta_2) * gradient[1] * gradient[1]
        x1 = x0 - learning_rate * m_x / (Math.sqrt(v_x) + eps)
        y1 = y0 - learning_rate * m_y / (Math.sqrt(v_y) + eps)
        adam_history.push({"x" : scale_x.invert(x1), "y" : scale_y.invert(y1)})
        x0 = x1
        y0 = y1
    }
    return adam_history;
}


/*
 * Functions necessary for path visualizations
 */

const line_function = d3.line()
                      .x(function(d) { return d.x; })
                      .y(function(d) { return d.y; });

function draw_path(path_data, type, path_g) {
    const gradient_path = path_g.selectAll(type)
                        .data(path_data)
                        .enter()
                        .append("path")
                        .attr("d", line_function(path_data.slice(0,1)))
                        .attr("class", type)
                        .attr("stroke-width", 3)
                        .attr("fill", "none")
                        .attr("stroke-opacity", 0.5)
                        .transition()
                        .duration(drawing_time)
                        .delay(function(d,i) { return drawing_time * i; })
                        .attr("d", function(d,i) { return line_function(path_data.slice(0,i+1));})
                        .remove();

    path_g.append("path")
                   .attr("d", line_function(path_data))
                   .attr("class", type)
                   .attr("stroke-width", 3)
                   .attr("fill", "none")
                   .attr("stroke-opacity", 0.5)
                   .attr("stroke-opacity", 0)
                   .transition()
                   .duration(path_data.length * drawing_time)
                   .attr("stroke-opacity", 0.5);
}

</script>
```

## Second-order methods: Newton and variants

The above gradient descent and its variants are all _first-order methods_, in that they use gradient information.
In addition to the derivative, one can also use the second derivative (or the Hessian in multivariate contexts) to end up with _second-order methods_.
These methods can often produce better convergence properties, but at the expense of the extra computational burden incurred by calculating and manipulating Hessian matrices.

The quintessential second-order method is Newton's method, the idea of which is the following.
Consider the second-order approximation of {math}`f` at {math}`x_k`, which is given by
```{math}
q(x) = f(x_k) + \nabla f(x_k)^\top (x - x_k) + \frac{1}{2}(x - x_k)^\top H(x_k)(x - x_k)
```

The method uses as direction {math}`d` that of the extremum of the quadratic approximation at {math}`x_k`, which can be obtained from the first-order condition {math}`\nabla q(x) = 0`. 
This renders
```{math}
:label: eq:newton_cond
\nabla q(x) = \nabla f(x_k) + H(x_k)(x - x_k) = 0.
```

Assuming that {math}`H^{-1}(x_k)` exists, we can use {eq}`eq:newton_cond` to obtain the following update rule, which is known as the _Newton step_
```{math}
:label: eq:newton_method
x_{k+1} = x_k - H^{-1}(x_k)\nabla f(x_k)
```


Notice that the "pure" Newton's method has embedded in the direction of the step, its length (i.e., the step size) as well. In practice, the method uses {math}`d = - H^{-1}(x_k)\nabla f(x_k)` as a direction combined with a line search to obtain optimal step sizes and prevent divergence (that is, converge to {math}`-\infty`) in cases where the second-order approximation might lead to divergence. Fixing {math}`\lambda = 1` renders the natural Newton's method, as derived in {eq}`eq:newton_method`. The Newton's method can also be seen as employing Newton-Raphson method to solve the system of equations that describe the first order conditions of the quadratic approximation at {math}`x_k`. 


```{prf:algorithm} Newton's method
:label: alg:newton
**Inputs** Objective {math}`f`, initial point {math}`x_0`, convergence criterion `converged`.
1. {math}`k=0`
2. **while** not `converged()`:
    1. {math}`d= -H^{-1}(x_k)\nabla f(x_k)`
    2. Determine step size / learning rate {math}`\lambda`
    3. {math}`x_{k+1}=x_k-\lambda d`
    4. {math}`k=k+1`
3. **return** {math}`x_k`.
```

While Newton's method can be very effective, computing the Hessian and its inversion may be prohibitively expensive for large problems.
Quasi-Newton methods circumvent this problem by approximating the Hessian instead of calculating it directly, making them a lot more efficient.
Instead of the Newton way of obtaining the direction by solving $d= -H^{-1}(x_k)\nabla f(x_k)$,
BFGS approximates $H^{-1}(x_k)$ with $B_k$ complemented with an update rule.

```{prf:algorithm} BFGS algorithm
:label: alg:bfgs
**Inputs:** Objective {math}`f`, initial point {math}`x_0`, initial inverse Hessian approximation {math}`B_0`, convergence criterion `converged`.
1. {math}`k = 0`
2. **while** not `converged()`:
    1. Compute direction {math}`d_k = -B_k \nabla f(x_k)`
    2. Determine step size / learning rate {math}`\lambda`
    3. Compute {math}`s_k = \lambda d_k`
    4. Update {math}`x_{k+1} = x_k + s_k`
    5. Compute {math}`y_k = \nabla f(x_{k+1}) - \nabla f(x_k)`
    6. Update inverse Hessian approximation:
       ```{math}
       B_{k+1} = B_k + \left(1 + \frac{y_k^\top B_k y_k}{y_k^\top s_k}\right) \frac{s_k s_k^\top}{s_k^\top y_k} - \frac{B_k y_k s_k^\top + s_k y_k^\top B_k}{s_k^\top y_k}
       ```
    7. {math}`k = k + 1`
3. **return** {math}`x_k`.
```

```{raw} html
<body>
<div id="d3-newton"></div>
</body>
<style>
.newton {
    stroke: black;
}
.Newton {
    fill: black;
}
.bfgs {
    stroke: blue;
}
.BFGS {
    fill: blue;
}
</style>
<script>

const newton_container = {
    "Newton": [get_newton_path, 300, 1e-4],
    "BFGS": [get_bfgs_path, 100, 1e-4]
}
create_interactive_plot("#d3-newton", newton_container, f);

function golden_ls(f, a, b, l) {
    const alpha = 0.618 // 1/golden_ratio
    let lam = a + (1-alpha)*(b-a)
    let mu = a + alpha*(b-a)

    let fmu = f(mu)
    let flam = f(lam)
    while (b-a > l) {
        if (flam > fmu) {
            a = lam
            lam = mu
            flam = fmu
            mu = a + alpha*(b-a)
            fmu = f(mu)
        }
        else {
            b = mu
            mu = lam
            fmu = flam
            lam = a+(1-alpha)*(b-a)
            flam = f(lam)
        }
    }
    return (a+b)/2
}

function get_newton_path(f, x0, y0, num_steps, tol) {
    let newton_history = [{"x": scale_x.invert(x0), "y": scale_y.invert(y0)}];
    let x1, y1, gradient, hessian, lr;
    for (i = 0; i < num_steps; i++) {
        gradient = grad_f(f, x0, y0);
        if (math.norm(gradient) < tol) return newton_history;
        hessian = hess_f(f, x0, y0);
        dir = math.chain(hessian).inv().multiply(gradient, -1).done()
        const foo = (l) => f(x0 + l*dir[0], y0 + l*dir[1])
        lr = golden_ls(foo, 0, 10, 1e-7)
        x1 = x0 + lr * dir[0]
        y1 = y0 + lr * dir[1]
        newton_history.push({"x" : scale_x.invert(x1), "y" : scale_y.invert(y1)})
        x0 = x1
        y0 = y1
    }
    return newton_history;
}

function get_bfgs_path(f, x0, y0, num_steps, tol) {
    let bfgs_history = [{"x": scale_x.invert(x0), "y": scale_y.invert(y0)}];
    let x1, y1, gradient, s, g, rho;
    const id_matrix = math.matrix([[1.,0.],[0.,1.]]);
    let H = id_matrix;
    let next_grad = grad_f(f, x0, y0);
    for (i = 0; i < num_steps; i++) {
        gradient = next_grad;
        if (math.norm(gradient) < tol) return bfgs_history;
        dir = math.chain(H).multiply(gradient, -1).done();
        const foo = (l) => f(x0 + l*dir.get([0]), y0 + l*dir.get([1]));
        lr = golden_ls(foo, 0, 10, 1e-7);
        x1 = x0 + lr * dir.get([0]);
        y1 = y0 + lr * dir.get([1]);
        bfgs_history.push({"x" : scale_x.invert(x1), "y" : scale_y.invert(y1)});
        s = math.matrix([[x1-x0, y1-y0]]);
        next_grad = grad_f(f, x1, y1);
        g = math.matrix([math.subtract(next_grad, gradient)]);
        rho = math.chain(g).multiply(math.transpose(s)).inv().done().get([0,0]);
        H = math.add(
                math.multiply(
                    math.subtract(id_matrix, math.multiply(rho, math.transpose(s), g)),
                    H,
                    math.subtract(id_matrix, math.multiply(rho, math.transpose(g), s))
                ),
                math.multiply(rho, math.transpose(s), s)
        );
        x0 = x1;
        y0 = y1;
    }
    return bfgs_history;
}
</script>
```
