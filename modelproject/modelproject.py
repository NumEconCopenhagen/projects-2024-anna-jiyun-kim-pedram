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

equilibrium_condition = best_response - (q + q_R)

# Solving for equilibrium quantities
equilibrium_solution = sm.solve(equilibrium_condition, q)

# Create lambdified functions
equilibrium_func = sm.lambdify((q_R, c, b, m), equilibrium_solution)

def modelE(q_R_values, c_value, b_value, m_value):
    equilibrium_q_i = equilibrium_func(q_R_values, c_value, b_value, m_value)
    return equilibrium_q_i

