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
  display_name: Julia 1.10.5
  language: julia
  name: julia-1.10
---

(p2l1)=
# Basics of calculus for optimisation

## Revisit unconstrained optimality conditions (and gradients)

## Second-order optimality condition and Hessians

## Taylor approximation

Adapted from [Michael Schlottke-Lakemper's code](https://gist.github.com/sloede/a680cf36245e1794801a6bcd4530487a).

```{code-cell}
using WGLMakie, Bonito

function base_graph(fun)
    fig = Figure(size=(800, 600), fontsize=30)
    ax = Axis(fig[1,1],
              title="Taylor series for sine/cosine",
              xlabel="x",
              ylabel="y",
              xticks=MultiplesTicks(5, pi, "π")
              )
    lines!(ax, -7..7, fun, label="f(x)")

    xlims!(ax, -7, 7)
    ylims!(ax, -5, 5)
    return fig, ax
end

function draw_x0(ax, x0, y)
    scatter!(ax, x0, y, color=:red, markersize=20, label="x₀")
end

function draw_taylor(ax, x, y)
    lines!(ax, x, y, linewidth=3, label="Tₙ(x)")
end

function tcosn(x, n, x0)
  sin_x0, cos_x0 = sincos(x0)
  result = cos_x0
  for i in 1:4:n
    result -= sin_x0 * (x - x0)^i/factorial(i)
  end
  for i in 2:4:n
    result -= cos_x0 * (x - x0)^i/factorial(i)
  end
  for i in 3:4:n
    result += sin_x0 * (x - x0)^i/factorial(i)
  end
  for i in 4:4:n
    result += cos_x0 * (x - x0)^i/factorial(i)
  end
  return result
end

function tsinn(x, n, x0)
  sin_x0, cos_x0 = sincos(x0)
  result = sin_x0
  for i in 1:4:n
    result += cos_x0 * (x - x0)^i/factorial(i)
  end
  for i in 2:4:n
    result -= sin_x0 * (x - x0)^i/factorial(i)
  end
  for i in 3:4:n
    result -= cos_x0 * (x - x0)^i/factorial(i)
  end
  for i in 4:4:n
    result += sin_x0 * (x - x0)^i/factorial(i)
  end
  return result
end

App() do session::Session
    fun = Observable{Any}(sin)
    taylor = Observable{Any}(tsinn)

    dropdown = Dropdown(["Sine", "Cosine"])
    on(dropdown.value) do value
        if value == "Sine"
            fun[] = sin
            taylor[] = tsinn
        else#if value == "Cosine"
            fun[] = cos
            taylor[] = tcosn
        end
    end

    slider_x0 = Slider(-7:0.1:7)
    slider_x0[] = 0  # set starting value
    y = @lift($fun($slider_x0))

    slider_deg = Slider(1:5)
    xvals = range(-7, 7, 100)
    yvals = @lift($taylor.(xvals, $slider_deg, $slider_x0))
    
    fig, ax = base_graph(fun)
    draw_taylor(ax, xvals, yvals)
    draw_x0(ax, slider_x0.value, y)
    axislegend(ax, position=:rb)

    return Bonito.record_states(session, 
                                DOM.div(
                                    fig, 
                                    DOM.div("Taylor polynomial degrees: ", slider_deg, slider_deg.value),
                                    DOM.div("x₀: ", slider_x0, slider_x0.value),
                                    dropdown
                                    ))
end
```

## Constrained optimality conditions: Karush-Kuhn-Tucker

## Interpretations of the KKt conditions