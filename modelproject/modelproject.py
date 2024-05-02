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
q = sm.symbols("q") #Output of firm i
q_R = sm.symbols("q_R") # rest of output
c = sm.symbols("c") #Cost
m = sm.symbols("m") #Parameter for the slope of the price function
b = sm.symbols("b") # Intercept of the price function

# Define price function
price_function = sm.Eq(p, m * (q + q_R) + b)

# Define profit function
profit_function = p * q - c * q

# Solve for price function
p_eq = sm.solve(price_function, p)

# Substitute price and create objective function
objective = profit_function.subs(p, p_eq[0])

# Lambdify functions
objective_lambd = sm.lambdify((q, q_R, c, b, m), objective)

# First-order derivative of profit function with respect to quantity
objective_diff = sm.diff(objective, q)

# Best Response function
best_response = sm.lambdify((q, q_R, c, b, m), objective_diff)

# Second derivatives for generating the Jacobian matrix for firm i and rest
best_response_diff_i = sm.diff(objective_diff, q)
best_response_diff_R = sm.diff(objective_diff, q_R)

jacobian_q_i = sm.lambdify((q, q_R), best_response_diff_i)
jacobian_q_R = sm.lambdify((q, q_R), best_response_diff_R)

def h(q_values, q_R_values, c_values, b_value, m_value):
    return np.array([best_response(q_values[i], q_R_values[i], c_values[i], b_value, m_value) for i in range(len(q_values))])

def hp(q_values, q_R_values, b_value):
    N = len(q_values)
    jacobian_matrix = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if j == i:
                jacobian_matrix[i, j] = jacobian_q_i(q_values[i], q_R_values[i])
            else:
                jacobian_matrix[i, j] = jacobian_q_R(q_values[i], q_R_values[i])
    return jacobian_matrix

def solve_model(N=50, b=1, seed=2000, draw_from_distribution=True, constant_value=9999, display=True):
    N_init = N

    if draw_from_distribution:
        np.random.seed(seed)
        c_values = 0.01 * np.random.lognormal(mean=0, sigma=1, size=N)
    else:
        c_values = np.full((N,), constant_value)

    c_values_init = c_values.copy()

    x = np.zeros(N)
    x_nonneg = np.zeros(N, dtype=bool)

    while not all(x_nonneg):
        result = root(lambda x: h(x, np.sum(x) - x, c_values, b, 0.5), x, jac=lambda x: hp(x, np.sum(x)-x, b))
        x = result.x
        x_nonneg = (x >= 0).astype(bool)
        
        c_values = c_values[x_nonneg]
        x = x[x_nonneg]
        N = np.sum(x_nonneg)

    profit = objective_lambd(result.x, np.sum(result.x) - result.x, c_values, b, 0.5)

    if display:
        print(result)
        print('\nx =', result.x[0:5], '\nh(x) =', h(result.x, c_values, b, 0.5)[0:5], '\nsum(x) =', np.sum(result.x), '\ncost =', c_values[0:5],'\nProfit =', profit[0:5],'\nb =', b,'\nN_firms =', N)

    for i in range(N_init):
        if i in result.success:
            continue
        else:
            x = np.insert(x, i, 0)
            profit = np.insert(profit, i, 0)

    sol = SimpleNamespace()
    sol.c_values_init = c_values_init
    sol.c_values = c_values
    sol.x = x
    sol.N = N
    sol.N_init = N_init
    sol.profit = profit

    return sol


