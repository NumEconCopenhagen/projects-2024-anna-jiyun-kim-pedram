from scipy import optimize
import numpy as np
import sympy as sm
import matplotlib.pyplot as plt
from types import SimpleNamespace
from scipy.optimize import root



def solve_ss(alpha, c):
    """ Example function. Solve for steady state k. 

    Args:
        c (float): costs
        alpha (float): parameter

    Returns:
        result (RootResults): the solution represented as a RootResults object.

    """ 
    
    # a. Objective function, depends on k (endogenous) and c (exogenous).
    f = lambda k: k**alpha - c
    obj = lambda kss: kss - f(kss)

    #. b. call root finder to find kss.
    result = optimize.root_scalar(obj,bracket=[0.1,100],method='bisect')
    
    return result



#Define variables used in the model simulation
p = sm.symbols("p") #Price
x = sm.symbols("x") #Output of firm i
x_R = sm.symbols("x_R") # rest of output
c = sm.symbols("c") #Cost
m = sm.symbols("m") #Parameter for the slope of the price function
b = sm.symbols("b") # Intercept of the price function

# Define price function
price_function = sm.Eq(p, m * (x + x_R) + b)

# Define profit function
profit_function = p * x - c * x

# Solve for price function
p_eq = sm.solve(price_function, p)

# Substitute price and create objective function
objective = profit_function.subs(p, p_eq[0]).subs(m,m)

# Lambdify functions
objective_lambd = sm.lambdify((x, x_R, c, b, m), objective)


# First-order derivative of profit function with respect to quantity
objective_diff = sm.diff(objective, x)

# Best Response function
best_response = sm.lambdify((x, x_R, c, b, m), objective_diff)

# Second derivatives for generating the Jacobian matrix for firm i and rest
best_response_diff_i = sm.diff(objective_diff, x)
best_response_diff_R = sm.diff(objective_diff, x_R)

jacobian_x_i = sm.lambdify((x, x_R, c, b, m), best_response_diff_i)
jacobian_x_R = sm.lambdify((x, x_R, c, b, m), best_response_diff_R)


# Defining the function to be optimized
def h(x, c_vec, b, m, N):
    y = np.zeros(N)
    for i in range(N):

        y[i] = best_response(x[i], sum(x) - x[i], c_vec[i], b, m)
    return y


# Defining the Jacobian of the function to be optimized
def hp(x, b, m, N):
    y = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if j == i:
                # Diagonal of the Jacobian Matrix
                y[i,j] = jacobian_x_i(x[i], sum(x) - x[i], b, m)
            else:
                # Off-Diagonal of the Jacobian Matrix
                y[i,j] = jacobian_x_R(x[i], sum(x) - x[i], b, m)
    return y

# Algoritm for solving market equilibrium
def solve_model(N=50, b=10, m=2, seed=2000, draw_from_distribution=True, constant_value=9999, display=True):

    N_init = N

    # if/else statement to draw from log normal distribution
    if draw_from_distribution:
        np.random.seed(seed)
        c_vec = 0.01 * np.random.lognormal(mean=0, sigma=1, size=N)
    else:
        c_vec = np.full((N,), constant_value)

    c_vec_init = c_vec.copy()

    # Setting up the initial values for x
    index = np.array(range(N))
    x0 = np.zeros(N)
    x_nonneg = np.zeros(N, dtype=bool)

    while not all(x_nonneg):

        # Solving the optimization problem using scipy.optimize.root() function
        result = optimize.root(lambda x0: h(x0, c_vec, b, m, N), x0, jac=lambda x0: hp(x0, b, m, N))

        x0 = result.x
        x_nonneg = (x0 >= 0).astype(bool)
        
        c_vec = c_vec[x_nonneg]
        x0    = x0[x_nonneg]
        N     = np.sum(x_nonneg)
        index = index[x_nonneg]

    profit=objective_lambd(result.x, np.sum(result.x)-result.x, c_vec, b, m)

    # Printing the results
    if display == True:
        print(result)
        print('\nx =', result.x[0:5], '\nh(x) =', h(x0,c_vec,b,m,N)[0:5], '\nsum(x) =', sum(result.x), '\nmarginal cost=',c_vec[0:5],'\nprofit=', profit[0:5],'\nb= ',b,'\nN_firms =',N)

    for i in range(N_init):
        if i in index:
            continue
        else:
            x0=np.insert(x0,i,0)
            profit=np.insert(profit,i,0)

    sol = SimpleNamespace()
    sol.c_vec_init=c_vec_init
    sol.c_vec=c_vec
    sol.x0=x0
    sol.index=index
    sol.N=N
    sol.N_init=N_init
    sol.profit=profit

    return sol

