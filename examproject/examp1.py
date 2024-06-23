from types import SimpleNamespace
import numpy as np
from scipy.optimize import minimize



class ProductionEconomyClass:
    def __init__(self):

        self.par = SimpleNamespace()
        # firms
        self.par.A = 1.0
        self.par.gamma = 0.5
        # households
        self.par.alpha = 0.3
        self.par.nu = 1.0
        self.par.epsilon = 2.0
        # government
        self.par.tau = 0.0
        self.par.T = 0.0
        # Question 3
        self.par.kappa = 0.1
        self.par.w = 1
    
    # Firm optimal labor demand
    def l_star_firm(self, p):
        par = self.par
        return (p * par.A * par.gamma / par.w) ** (1 / (1 - par.gamma))

    # Firm optimal output level
    def y_star_firm(self, p):
        par = self.par
        return par.A * (self.l_star_firm(p)) ** par.gamma

    # Firm implied profit
    def pi_star_firm(self, p):
        par = self.par
        return ((1 - par.gamma) / par.gamma) * par.w * (p * par.A * par.gamma / par.w) ** (1 / (1 - par.gamma))

    # Consumer optimal consumption good 1
    def c13(self, p1, p2, T, l):
        par = self.par
        return par.alpha * ((par.w * l + T + self.pi_star_firm(p1) + self.pi_star_firm(p2)) / p1)


    # Consumer optimal consumption good 2
    def c23(self, p1, p2, tau, T, l):
        par = self.par
        return (1 - par.alpha) * ((par.w * l + T + self.pi_star_firm(p1) + self.pi_star_firm(p2)) / (p2 + tau))

    # Consumer optimal labor behavior
    def l_star_consumer(self, p1, p2):
        par = self.par
        # Objective function to minimize
        def lstar(l):
            c1 = self.c13(p1, p2, par.T, l)
            c2 = self.c23(p1, p2, par.tau, par.T, l)
            return -(np.log(c1**par.alpha * c2**(1-par.alpha)) - par.nu*l**(1+par.epsilon)/(1+par.epsilon))
        
        # Optimize
        initial_guess = [0.1]
        bounds = [(0, None)]
        result = minimize(lstar, initial_guess, bounds=bounds, method='SLSQP')
        return result.x[0]

    # Market Clearing Condition: Labor market
    def excessdemand_labor(self, p1, p2):
        par = self.par
        l1 = self.l_star_firm(p1)
        l2 = self.l_star_firm(p2)
        l_opt = self.l_star_consumer(p1, p2)
        return l1 + l2 - l_opt

    #Market Clearing Condition: Good market 1
    def excessdemand_goodmarket1(self, p1, p2):
        par = self.par
        l_opt = self.l_star_consumer(p1, p2)
        c1 = self.c13(p1, p2, par.T, l_opt)
        y1 = self.y_star_firm(p1)
        return c1 - y1

    # Market Clearing Condition: Good market 2
    def excessdemand_goodmarket2(self, p1, p2):
        par = self.par
        l_opt = self.l_star_consumer(p1, p2)
        c2 = self.c23(p1, p2, par.tau, par.T, l_opt)
        y2 = self.y_star_firm(p2)
        return c2 - y2
    
    # The objective function for finding equilibrium prices
    def objectiveprice(self, p):
        p1, p2 = p
        excess_labor = self.excessdemand_labor(p1, p2)
        excess_goodsmarket2 = self.excessdemand_goodmarket2(p1, p2)
        return excess_labor**2 + excess_goodsmarket2**2  # check that labor market clears and good market 2 clears

    # Consumer utility function
    def utility_all(self, p1, p2, tau):
        par = self.par
        l_star = self.l_star_consumer(p1, p2)
        T = tau * self.c23(p1, p2, tau, 0, l_star)
        c1 = self.c13(p1, p2, T, l_star)
        c2 = self.c23(p1, p2, tau, T, l_star)
        return np.log(c1 ** par.alpha * c2 ** (1 - par.alpha)) - par.nu * l_star ** (1 + par.epsilon) / (1 + par.epsilon)

    # Consumer budgetconstraint
    def budget_constraint(self, p1, p2, tau, l):
        par = self.par
        T = tau * self.c23(p1, p2, tau, 0, l)  # Calculate T using the formula
        c1 = self.c13(p1, p2, T, l)
        c2 = self.c23(p1, p2, tau, T, l)
        pi_1 = self.pi_star_firm(p1)
        pi_2 = self.pi_star_firm(p2)
        return p1 * c1 + (p2 + tau) * c2 - (par.w * l + T + pi_1 + pi_2)

    # Social Welfare
    def social_welfare(self, p1, p2, tau):
        par = self.par
        utility = self.utility_all(p1, p2, tau)
        swf = utility + par.kappa * self.y_star_firm(p2)
        return -swf

    # Tau that maximizes SWF
    def optimize_tau(self, p1, p2):
        par = self.par
        initial_guess = [0.1]
        bounds = [(0, None)]
        constraints = {
            'type': 'eq',
            'fun': lambda tau: self.budget_constraint(p1, p2, tau, self.l_star_consumer(p1, p2))
        }
        result = minimize(lambda tau: self.social_welfare(p1, p2, tau), initial_guess, bounds=bounds, constraints=constraints, method='SLSQP')
        return result.x[0]