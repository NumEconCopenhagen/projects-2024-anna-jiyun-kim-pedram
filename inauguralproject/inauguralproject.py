import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.optimize import minimize
from types import SimpleNamespace

class MarketModel():
    def __init__(self, N = 75):

        self.par = SimpleNamespace()

        # a. set preferences
        self.par.alpha = 1/3
        self.par.beta = 2/3

        # b. define endowments knowing that; w1A + w1B = w1 and w2A + w2B = w2
        self.par.w1A = 0.8
        self.par.w2A = 0.3
        self.par.w1B = 1 - self.par.w1A
        self.par.w2B = 1 - self.par.w2A
        self.par.w1 = self.par.w1A + self.par.w1B
        self.par.w2 = self.par.w2A + self.par.w2B

        #Set p2 as numeria
        self.par.p2 = 1

        #Used to define the number of points along each axis, for which the model evaluates potential pareto improvements.
        self.N = N
        #Initial values for question 2
        self.par.N1 = 10
        self.par.N2 = 5

    #Define the utility for A
    def utility_A(self, x1, x2):
        u = x1**self.par.alpha * x2**(1-self.par.alpha)
        return u

    #Define the utility for B
    def utility_B(self, x1, x2):
        u =  x1**self.par.beta * x2**(1-self.par.beta)
        return u

    #Define A's demand
    def demand_A(self, p1, p2):
        x1 = self.par.alpha * (p1 * self.par.w1A + p2 * self.par.w2A) / p1
        x2 = (1 - self.par.alpha) * (p1 * self.par.w1A + p2 * self.par.w2A) / p2
        return x1, x2

    #Define B's demand
    def demand_B(self, p1, p2):
        x1 = self.par.beta * (p1 * self.par.w1B + p2 * self.par.w2B) / p1
        x2 = (1 - self.par.beta) * (p1 * self.par.w1B + p2 * self.par.w2B) / p2
        return x1, x2

    #Check market clearing conditions.
    def check_market_clearing(self,p1):

            x1A,x2A = self.demand_A(p1)
            x1B,x2B = self.demand_B(p1)

            eps1 = x1A-par.w1A + x1B-(1-par.w1A)
            eps2 = x2A-par.w2A + x2B-(1-par.w2A)

            return eps1,eps2

    #Define the pareto improvements
    def find_pareto_improvements(self):
        #Initialize an empty list to store the Pareto improvements found
        pareto_improvement_set = [] 
        #Iterates over the grid points within the ranges [0, self.par.w1] and [0,self.par.w2]
        for x1 in np.linspace(0, self.par.w1, self.N + 1):
            for x2 in np.linspace(0, self.par.w2, self.N + 1):
                # For each combination of x1 and x2 in the grid, the utility or A and B are calculated
                A_utility = self.utility_A(x1, x2)
                B_utility = self.utility_B(self.par.w1 - x1, self.par.w2 - x2)
                #Checks if the combination of (x1, x2) represents a Pareto improvement
                if A_utility >= self.utility_A(self.par.w1A, self.par.w2A) and B_utility >= self.utility_B(self.par.w1B, self.par.w2B):
                    #If the combination of x1 and x2  gives a pareto improvement, x1 and x2 are added to the empty list. 
                    pareto_improvement_set.append((x1, x2))
        return pareto_improvement_set

    #Plotting the edgeworth box
    def plot_edgeworth_box(self):
        #Call the list with pareto improvements
        pareto_improvement_set = self.find_pareto_improvements()
        #Takes the x-coordinates (x_A1_pareto) from the list and the y-coordinates (x_2A_pareto). If there are no pareto improvements, it assigns an empty list. 
        x_A1_pareto, x_A2_pareto = zip(*pareto_improvement_set) if pareto_improvement_set else ([], [])
        #Creating a scatter using matplotlib.pyplot.scatter() with the x- and y-coordinates from above. 
        fig, ax = plt.subplots()
        ax.scatter(x_A1_pareto, x_A2_pareto, color='green', label='Pareto Improvements')

        #Set the labels
        ax.set_xlabel('Good x1')
        ax.set_ylabel('Good x2')
        ax.set_title('Edgeworth Box')
        ax.legend()
        plt.show()

         # Calculate errors for different values of p1 for question 2
    def calculate_errors(self):
        #p1 ranges from 0.5 to 2.5 in the steps determined by 2/N
        P1 = np.arange(0.5, 2.6, 2 / self.par.N1)
        #Create an empty list
        errors = []

        #Iterate over each value of p1 where p2 is numeraire
        for p1 in P1:
            x1A, x2A = self.demand_A(p1, self.par.p2)
            x1B, x2B = self.demand_B(p1, self.par.p2)    
            
    
            #Calculates the errors for both goods for each value in the pricevector. 
            error_1 = x1A + x1B - (self.par.w1A + self.par.w1B)
            error_2 = x2A + x2B - (self.par.w2A + self.par.w2B)
    
            #Creates a tupple 
            errors.append((error_1, error_2))

        # Print errors for each p1
        for i, p_1 in enumerate(P1):
            print(f"For p1 = {p_1:.2f}, Error: ε(p, ω) = ({errors[i][0]:.4f}, {errors[i][1]:.4f})")
            #Determine whether the market for good 1 is in equilibrium at a given price p1
    
    #Demand of good 1 for A and B to solve question 3
    def demand_A1(self, p1):
        u = self.par.alpha * (p1 * self.par.w1A + self.par.p2 * self.par.w2A) / p1
        return u
    def demand_B1(self, p1):
        u = self.par.beta * (p1 * self.par.w1B + self.par.p2 * self.par.w2B) / p1
        return u
    def market_clearing_condition(self, p1):
        #Calculate the excess demand (or excess supply). Since the total quantity supplied is 1, 1 is subtracted from the total demand 
        return self.demand_A1(p1) + self.demand_B1(p1) - 1
    #Question 4a, define demand of good two for person A
    def demand_A2(self, p1):
        u = (1-self.par.alpha) * (p1 * self.par.w1A + self.par.p2 * self.par.w2A) / p1
        return u
    def q4a(self):
        P101 = 0.5 + 2* np.arange(self.N)/self.N
        #Optimization loop
        max_utility = -np.inf
        optimal_p1 = None
        for p1 in P101:
            #calculate demands for A at this price
            x1A = demand_A1(self, p1)
            x2A = demand_A2(self, p1)

            # Calculate utility for A at this price
            current_utility = utility_A(x1A, x2A)
            # Update maximum utility and optimal price if current utility is higher
            if current_utility > max_utility:
                max_utility = current_utility
                optimal_p1 = p1
                print("Optimal price p1 in P1:", optimal_p1)
                print("Maximum utility for A:", max_utility)
    
