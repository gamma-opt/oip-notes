using Random
Random.seed!(42)

I = 20 # oils
J = 12 # months
n_veg = 12

mean_hardness_veg = 7
mean_hardness_non = 4
hardness_veg = clamp.(11 .+ 2*randn(n_veg), 1, Inf)
hardness_non = clamp.(3 .+ 1*randn(I-n_veg), 1, Inf)

large_params = FoodParams(
    cost = round.(120 .+ 20*randn((I,J))),
    hardness = vcat(hardness_veg, hardness_non),
    hardness_ul = 10,
    hardness_ll = 5,
    price_product = 150,
    process_limit_veg = 800,
    process_limit_non = 1000,
    n_veg = n_veg;
    storage_limit = 1000,
    initial_oil = 500,
    target_oil = 500,
    cost_storing = 5
)
