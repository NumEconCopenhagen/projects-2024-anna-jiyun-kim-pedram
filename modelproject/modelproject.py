from scipy import optimize
import numpy as np
import sympy as sm
import matplotlib.pyplot as plt


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

#Define price
price_function = sm.Eq(p, m*(q+q_R) + b)

#Define profit
profit_function = p*q - c*q

#Solve the price
p_eq = sm.solve(price_function, p)

#Sub price and create objective
objec = profit_function.subs(p,p_eq[0])

#Lambdify functions
objec_l = sm.lambdify(args=(q, q_R, c, b, m), expr = objec)

#FOC profit wrt. quantity
objec_diff = sm.diff(objec, q)

#Best Response (BR)
bestR = sm.lambdify(args=(q, q_R, c, b, m), expr = objec_diff)

#second derivatives generated for generating jacobian matrix for firm i and rest
bestR_diff_i = sm.diff(objec_diff, q)
bestR_diff_R = sm.diff(objec_diff, q_R)

jacob_q_i = sm.lambdify(args=(q, q_R), expr = bestR_diff_i)
jacob_q_R = sm.lambdify(args=(q, q_R), expr = bestR_diff_R)