from scipy import optimize
import numpy as np
import sympy as sm
import matplotlib.pyplot as plt
from types import SimpleNamespace


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


# Calculating the best response of each firm for optimization
def h(q, c_vec, N, b, m):
    y = np.zeros(N)
    for i in range(N):

        y[i] = bestR(q[i], sum(q) - q[i], c_vec[i], b, m)
    return y


# Optimizing the jacobian
def hp(q, N):
    y = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if j == i:
                y[i, j] = jacob_q_i(q[i], sum(q)-q[i])
            else:
                y[i, j] = jacob_q_R(q[i], sum(q)-q[i])
    return y

# using scipy.optimize.root to solve and find the market equilibrium
def solve_model(N=50, seed=2000, draw_from_distribution=True, constant_value=9999, display=True):

    N_init = N

    # if/else statement to draw from log normal distribution
    if draw_from_distribution:
        np.random.seed(seed)
        c_vec = np.random.lognormal(mean=0, sigma=1, size=N)
    else:
        c_vec = np.full((N,), constant_value)

    c_vec_init = c_vec.copy()

    # Setting up the initial values for q
    index = np.array(range(N))
    q0 = np.zeros(N)
    q_nonneg = np.zeros(N, dtype=bool)

    while not all(q_nonneg):

        # Solving the optimization problem using scipy.optimize.root() function
        result = optimize.root(lambda q0: h(q0, c_vec, N, b, m), q0, jac=lambda q0: hp(q0, N))
        q0 = result.q
        q_nonneg = (q0 >= 0).astype(bool)
        
        c_vec = c_vec[q_nonneg]
        q0    = q0[q_nonneg]
        N     = np.sum(q_nonneg)
        index = index[q_nonneg]

    profit=objec_l(result.q, np.sum(result.q)-result.q, c_vec)

    # Printing the results
    if display == True:
        print(result)
        print('\nq =', result.q[0:5], '\nh(q) =', h(q0,c_vec,N)[0:5], '\nsum(q) =', sum(result.q), '\nmarginal cost=',c_vec[0:5],'\nprofit=', profit[0:5],'\nN_firms =',N)

    for i in range(N_init):
        if i in index:
            continue
        else:
            q0=np.insert(q0,i,0)
            profit=np.insert(profit,i,0)

    sol = SimpleNamespace()
    sol.c_vec_init=c_vec_init
    sol.c_vec=c_vec
    sol.q0=q0
    sol.index=index
    sol.N=N
    sol.N_init=N_init
    sol.profit=profit

    return sol



