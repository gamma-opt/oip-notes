
m = Model(HiGHS.Optimizer)

M = 100

@variable(m, x_t >= 0, Int)
@variable(m, x_c >= 0, Int)
@variable(m, y_t10, Bin)
@variable(m, y_t01, Bin)
@variable(m, y_t00, Bin)
@variable(m, y_c, Bin)

@objective(m, Max, 1000*x_t + 500*x_c - 5000*y_t10 - 8700*y_t01 - 600*y_c)

@constraint(m, 3*x_t + 5*x_c <= 40 + M*(1-y_t10 - y_t00))
@constraint(m, 7*x_t + 4*x_c <= 60 + M*(1-y_t10 - y_t00))
@constraint(m, 2*x_t + 5*x_c <= 40 + M*(1-y_t01 - y_t00))
@constraint(m, 5*x_t + 4*x_c <= 60 + M*(1-y_t01 - y_t00))
@constraint(m, x_t <= M*(y_t10 + y_t01))
@constraint(m, x_c <= M*y_c)
@constraint(m, y_t10 + y_t01 + y_t00 == 1)

optimize!(m)



