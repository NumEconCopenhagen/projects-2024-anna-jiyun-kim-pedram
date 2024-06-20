from types import SimpleNamespace
import numpy as np
from scipy.optimize import minimize

class MarketModel():

    def __init__(self):

        par = self.par = SimpleNamespace()

        # set preferences
        par.alpha = 1/3
        par.beta = 2/3

        # define endowments
        par.w1A = 0.8
        par.w2A = 0.3

        par.w1B = 1 - par.w1A
        par.w2B = 1 - par.w2A

        par.w1 = par.w1A + par.w1B
        par.w2 = par.w2A + par.w2B


    #Utility for A
    def utility_A(self, x1A, x2A):
        par = self.par 
        return (x1A**par.alpha) * (x2A**(1-par.alpha))

    #Utility for B
    def utility_B(self, x1B, x2B):
        par = self.par 
        return (x1B**par.beta) * (x2B**(1-par.beta))

    #Demand for A
    def demand_A(self, p1, p2):
        par = self.par
        
        #Set p2 as numeria
        p2 = 1

        #A's demand function
        x1A = par.alpha*((p1* par.w1A + p2* par.w2A)/p1)
        x2A = (1 - par.alpha)*((p1*par.w1A + p2*par.w2A)/p2) 

        #Returnig the demand
        return x1A, x2A

    #Demand for B
    def demand_B(self, p1, p2):

        par = self.par

        #Set p2 as numeria
        p2 = 1

        #B's demand function
        x1B = par.beta*((p1*par.w1B + p2*par.w2B)/p1)
        x2B = (1 - par.beta)*((p1*par.w1B + p2*par.w2B)/p2) 

        #Returning the demand
        return x1B, x2B
    
    #Condition for x1A and x2A
    def constraints(self, x):
        x1A, x2A = x
        x1B = 1 - x1A
        x2B = 1 - x2A
        return [
            self.utility_A([x1A, x2A]) - self.utility_A([self.par.w1A, self.par.w2A]),
            self.utility_B([x1B, x2B]) - self.utility_B([self.par.w1B, self.par.w2B])]
    

  

     ################################## Question 2 #############################################

   # Calculate errors for different values of p1
    def calculate_errors(self):
        
        par = self.par 

        par.N = 75
        par.p2 = 1


        #p1 ranges from 0.5 to 2.5 in the steps determined by 2/N
        p1_values = [(0.5 + 2 * i / 75) for i in range(76)]

        #Create an empty list
        errors = []

        #Iterate over each value of p1 where p2 is numeraire
        for p1 in p1_values:
            x1A, x2A = self.demand_A(p1,par.p2)
            x1B, x2B = self.demand_B(p1, par.p2)    
            
    
            #Calculates the errors for both goods for each value in the pricevector. 
            error_1 = x1A + x1B - (par.w1A + par.w1B)
            error_2 = x2A + x2B - (par.w2A + par.w2B)
    
            #Creates a tupple 
            errors.append((error_1, error_2))

        # Print errors for each p1
        return p1_values, errors




    ################################# Question 3 ####################################


    #Check market clearing conditions.
    def check_market_clearing(self,p1):
        par = self.par

        #Compute demands
        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        #Calculate errors
        eps1 = x1A - par.w1A + x1B - par.w1B
        eps2 = x2A - par.w2A + x2B - par.w2B

        #Return the distance using the Pythagorean theorem
        return np.sqrt(eps1**2 + eps2**2)
    
    #Caulculate excess demand
    def market_clearing_condition(self, p1):
        return self.demand_A(p1) + self.demand_B(p1) - 1
    

    ######################### Question 4 #############################


    

    ################### Question 5 ########################

    #Define utility
    def objective_5(self, x):
        x1A, x2A = x
        return -self.utility_A(x1A, x2A)  # Pass arguments unpacked
    


    ######### Question 6 ########################
    #Define constraints
    def constraints(self,x):
        x1A, x2A = x
        x1B = 1 - x1A
        x2B = 1 - x2A
        return self.utility_B(x1B, x2B) - self.utility_B(self.par.w1B, self.par.w2B)
    

    #Define aggregate utility for consumer A and B
    def aggregate_utility(self, x):
        x1A, x2A = x
        x1B = 1 - x1A
        x2B = 1 - x2A
        return self.utility_A(x1A, x2A) + self.utility_B(x1B, x2B)
    


    ################# Question 8 #####################

    #Define the sum of the utilities
    def objective_8(self, x):
        x1A = x[0]
        x2A = x[1]
        return -(self.utility_A(x1A, x2A) + self.utility_B(1 - x1A, 1 - x2A))
    #Define the utility for Consumer A
    def utility_A_8(self, x1A, x2A):
        return x1A**self.par.alpha * x2A**(1 - self.par.alpha)
    #Define the utility for B
    def utility_B_8(self, x1B, x2B):
        return x1B**self.par.beta * x2B**(1 - self.par.beta)