from scipy import optimize
import numpy as np
import sympy as sm
import matplotlib.pyplot as plt
from types import SimpleNamespace
from scipy.optimize import root
from scipy.optimize import minimize 


class MarketModel():

        # Define the best response functions using numerical optimization
        def best_response1(q2, A, alpha, c):
            q1 = (A - q2 - alpha * c) / 2
            return q1

        def best_response2(A, q1, alpha, c):
            q2 = (A - q1 - alpha * c) / 2
            return q2

        # Define the function to find the equilibrium by minimizing the squared differences
        def find_equilibrium(x, A, alpha, c):
            q1, q2 = x
            br1 = best_response1(q2, A, alpha, c)
            br2 = best_response2(q1, A, alpha, c)
            return (q1 - br1) ** 2 + (q2 - br2) ** 2
            
    

