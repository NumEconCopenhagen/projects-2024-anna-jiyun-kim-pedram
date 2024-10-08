import numpy as np # Import numpy 
import matplotlib.pyplot as plt # Import matplotlib.pyplot




# PROBLEM 3
#Define the algorithm in a class where it can be called and used
class Model3:
    def __init__(self, seed=2024): #define the seed
        self.seed = seed #set the seed
        self.X, self.y = self.sample(seed) #generate the sample
        self.A, self.B, self.C, self.D = self.block_2(self.X, self.y) #find the points A, B, C, D
        self.f = lambda x: x[0] * x[1] #define the function to be used in question 3
        self.F = np.array([self.f(x) for x in self.X]) #for question 3

    #Define the sample to generate points based on the seed
    def sample(self, seed): #define the sample
        rng = np.random.default_rng(seed) #define random number generator
        X = rng.uniform(size=(50, 2)) #generate 50 uniform random numbers
        y = rng.uniform(size=(2,)) #generate 2 uniform random numbers
        return X, y
    
    #define block 1 to find the barycentric coordinates. The denominator is the determinant
    def block_1(self, A, B, C, y):
        denominator = ((B[1]-C[1])*(A[0]-C[0]) + (C[0]-B[0])*(A[1]-C[1])) #determinant
        r1 = ((B[1]-C[1])*(y[0]-C[0]) + (C[0]-B[0])*(y[1]-C[1])) / denominator #barycentric coordinate r1
        r2 = ((C[1]-A[1])*(y[0]-C[0]) + (A[0]-C[0])*(y[1]-C[1])) / denominator #barycentric coordinate r2
        r3 = 1 - r1 - r2 #barycentric coordinate r3
        return r1, r2, r3
    
    #define block 2 to find the minimized points A, B, C, D given the conditions in a generator process. linalg.norm is the euclidean distance
    def block_2(self, X, y):
        A = min((x for x in X if x[0] > y[0] and x[1] > y[1]), key=lambda x: np.linalg.norm(x - y), default=None) #point A
        B = min((x for x in X if x[0] > y[0] and x[1] < y[1]), key=lambda x: np.linalg.norm(x - y), default=None) #point B
        C = min((x for x in X if x[0] < y[0] and x[1] < y[1]), key=lambda x: np.linalg.norm(x - y), default=None) #point C
        D = min((x for x in X if x[0] < y[0] and x[1] > y[1]), key=lambda x: np.linalg.norm(x - y), default=None) #point D
        #return A, B, C, D, if None, return NaN
        if A is None:
            A = np.nan
        if B is None:
            B = np.nan
        if C is None:
            C = np.nan
        if D is None:
            D = np.nan
        return A, B, C, D
    
    #check which triangle y is in and return the barycentric coordinates as well as the point y. None if y is not in any triangle
    def check_y_in_tri(self):
        r_ABC, r_CDA = None, None #set the barycentric coordinates to None
        y_ABC, y_CDA = None, None #set the point y to None
        
        in_triangle_ABC = False #set the boolean to False
        in_triangle_CDA = False #set the boolean to False
        #for ABC
        if not np.isnan(self.A).any() and not np.isnan(self.B).any() and not np.isnan(self.C).any(): #if there are no NaN values
            r_ABC = self.block_1(self.A, self.B, self.C, self.y) #find barycentric coordinates
            if 0 <= r_ABC[0] <= 1 and 0 <= r_ABC[1] <= 1 and 0 <= r_ABC[2] <= 1: #if the barycentric coordinates are between 0 and 1
                y_ABC = r_ABC[0] * self.A + r_ABC[1] * self.B + r_ABC[2] * self.C #find the point y
                in_triangle_ABC = True #set the boolean to True
                print(f"y in ABC with coordinates: {y_ABC}") #print y in ABC if true
                print(f"Barycentric coordinates of ABC: {r_ABC}") #print barycentric coordinates ABC
            else: #if the barycentric coordinates are not between 0 and 1
                print("y not in ABC")
                if r_ABC is not None: 
                    print(f"Barycentric coordinates of ABC: {r_ABC}") #print barycentric coordinates ABC
        #for CDA the same process as before
        if not np.isnan(self.C).any() and not np.isnan(self.D).any() and not np.isnan(self.A).any():
            r_CDA = self.block_1(self.C, self.D, self.A, self.y)
            if 0 <= r_CDA[0] <= 1 and 0 <= r_CDA[1] <= 1 and 0 <= r_CDA[2] <= 1:
                y_CDA = r_CDA[0] * self.C + r_CDA[1] * self.D + r_CDA[2] * self.A
                in_triangle_CDA = True
                print(f"y in CDA with coordinates: {y_CDA}") #print y in CDA if true
                print(f"Barycentric coordinates of CDA: {r_CDA}") #print barycentric coordinates CDA
            else:
                print("y not in CDA")
                if r_CDA is not None:
                    print(f"Barycentric coordinates of CDA: {r_CDA}") #print barycentric coordinates CDA
        
        return {
            "in_triangle_ABC": in_triangle_ABC,
            "in_triangle_CDA": in_triangle_CDA,
            "r_ABC": r_ABC,
            "r_CDA": r_CDA,
            "y_ABC": y_ABC,
            "y_CDA": y_CDA
        }
    


    #plot the points and the triangles, none if there are NaN values
    def plot_point_and_tri(self):
        if np.isnan(self.A).any() or np.isnan(self.B).any() or np.isnan(self.C).any() or np.isnan(self.D).any():
            print("NaN")
            return
        #set the figure and size
        plt.figure(figsize=(8, 8))
        plt.scatter(self.X[:, 0], self.X[:, 1], c='blue', label='Points in X') #plot the points in X
        plt.scatter(self.y[0], self.y[1], c='red', label='Point y', zorder=5) #plot the point y
        #plot the points if they are not NaN
        if not np.isnan(self.A).any():
            plt.scatter(*self.A, c='orange', label='Point A', zorder=5) #plot point A
        if not np.isnan(self.B).any():
            plt.scatter(*self.B, c='cyan', label='Point B', zorder=5) #plot point B
        if not np.isnan(self.C).any():
            plt.scatter(*self.C, c='black', label='Point C', zorder=5) #plot point C
        if not np.isnan(self.D).any():
            plt.scatter(*self.D, c='brown', label='Point D', zorder=5) #plot point D
        
        #plot the triangles if they are not NaN
        if not np.isnan(self.A).any() and not np.isnan(self.B).any() and not np.isnan(self.C).any(): #plot ABC
            plt.plot([self.A[0], self.B[0], self.C[0], self.A[0]], [self.A[1], self.B[1], self.C[1], self.A[1]], 'pink', label='Triangle ABC', linestyle='dashed')
        if not np.isnan(self.C).any() and not np.isnan(self.D).any() and not np.isnan(self.A).any(): #plot CDA
            plt.plot([self.C[0], self.D[0], self.A[0], self.C[0]], [self.C[1], self.D[1], self.A[1], self.C[1]], 'yellow', label='Triangle CDA', linestyle='dashed')
        
        #Define labels, title and legend
        plt.xlabel('$x_1$')
        plt.ylabel('$x_2$')
        plt.title('Points and Triangles')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    #define the function to approximate f for question 3
    def approx_f(self):
        result3 = self.check_y_in_tri() 

        f_y_ABC = np.nan #set f(y) in ABC to NaN
        f_y_CDA = np.nan #set f(y) in CDA to NaN
        #if result is in ABC
        if result3["in_triangle_ABC"]: #if y is in ABC
            f_y_ABC = result3["r_ABC"][0] * self.f(self.A) + result3["r_ABC"][1] * self.f(self.B) + result3["r_ABC"][2] * self.f(self.C) #find f(y) approx in ABC
        # if result is in CDA
        if result3["in_triangle_CDA"]: #if y is in CDA
            f_y_CDA = result3["r_CDA"][0] * self.f(self.C) + result3["r_CDA"][1] * self.f(self.D) + result3["r_CDA"][2] * self.f(self.A) #find f(y) approx in CDA
       
        # Choose best approximation
        if not np.isnan(f_y_ABC): #if f(y) in ABC is not NaN
            f_y = f_y_ABC #set f(y) to approx in ABC
        elif not np.isnan(f_y_CDA): #if f(y) in CDA is not NaN
            f_y = f_y_CDA #set f(y) to approx in CDA
        else: #if both are NaN
            f_y = np.nan #set f(y) to NaN

        # True value
        true_value = self.f(self.y) 
        
        #difference between the approximation and the true value
        diff_true = abs(f_y - true_value) 

        # Print approximation, true value and difference between them
        print("Approximation f(y):", f_y)
        print("True value f(y):", true_value)
        print("Difference:", diff_true)
        return f_y, true_value, diff_true
   
    # question 4
    def func_4(self, Y):
        prior_y = self.y  # Save the y values from before so we can reset it after. In this way this function wont interfere with the previous functions when we try to call them again
        prior_A, prior_B, prior_C, prior_D = self.A, self.B, self.C, self.D  # Save prior points A, B, C, D
        results4 = [] #list to store results
        for y in Y: 
            self.y = y 
            self.A, self.B, self.C, self.D = self.block_2(self.X, self.y) #points A, B, C, D in the new y
            print(f"\nEvaluating for y = {y}:")
            result4 = self.approx_f() #approximate for the new y
            results4.append((y, result4)) #append the results
        self.y = prior_y  # Restore prior y values
        self.A, self.B, self.C, self.D = prior_A, prior_B, prior_C, prior_D  # Restore prior points A, B, C, D 
        return results4
    #Define relative errors for question 4
    def relative_error(self, results4):
        relative_errors = []
        for y, (f_y, true_value, diff_true) in results4:
            relative_error = diff_true / true_value
            relative_errors.append((y, relative_error))
        return relative_errors
    

