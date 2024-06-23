import numpy as np # Import numpy 
import matplotlib.pyplot as plt # Import matplotlib.pyplot
#Define the algorithm in a class where it can be called and used
class Model3:
    def __init__(self, seed=2024):
        self.seed = seed
        self.X, self.y = self.sample(seed)
        self.A, self.B, self.C, self.D = self.block_2(self.X, self.y)
        self.f = lambda x: x[0] * x[1] #define the function to be used in question 3
        self.F = np.array([self.f(x) for x in self.X]) #for question 3

    #Define the sample to generate points based on the seed
    def sample(self, seed):
        rng = np.random.default_rng(seed)
        X = rng.uniform(size=(50, 2))
        y = rng.uniform(size=(2,))
        return X, y
    
    #define block 1 to find the barycentric coordinates. The denominator is the determinant
    def block_1(self, A, B, C, y):
        denominator = ((B[1]-C[1])*(A[0]-C[0]) + (C[0]-B[0])*(A[1]-C[1]))
        r1 = ((B[1]-C[1])*(y[0]-C[0]) + (C[0]-B[0])*(y[1]-C[1])) / denominator
        r2 = ((C[1]-A[1])*(y[0]-C[0]) + (A[0]-C[0])*(y[1]-C[1])) / denominator
        r3 = 1 - r1 - r2
        return r1, r2, r3
    
    #define block 2 to find the points A, B, C, D given the conditions
    def block_2(self, X, y):
        A = min((x for x in X if x[0] > y[0] and x[1] > y[1]), key=lambda x: np.linalg.norm(x - y), default=None) #linalg.norm is the euclidean distance
        B = min((x for x in X if x[0] > y[0] and x[1] < y[1]), key=lambda x: np.linalg.norm(x - y), default=None)
        C = min((x for x in X if x[0] < y[0] and x[1] < y[1]), key=lambda x: np.linalg.norm(x - y), default=None)
        D = min((x for x in X if x[0] < y[0] and x[1] > y[1]), key=lambda x: np.linalg.norm(x - y), default=None)
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
        r_ABC, r_CDA = None, None
        y_ABC, y_CDA = None, None
        
        in_triangle_ABC = False
        in_triangle_CDA = False
        #for ABC
        if not np.isnan(self.A).any() and not np.isnan(self.B).any() and not np.isnan(self.C).any():
            r_ABC = self.block_1(self.A, self.B, self.C, self.y)
            if 0 <= r_ABC[0] <= 1 and 0 <= r_ABC[1] <= 1 and 0 <= r_ABC[2] <= 1:
                y_ABC = r_ABC[0] * self.A + r_ABC[1] * self.B + r_ABC[2] * self.C
                in_triangle_ABC = True
        # for CDA
        if not np.isnan(self.C).any() and not np.isnan(self.D).any() and not np.isnan(self.A).any():
            r_CDA = self.block_1(self.C, self.D, self.A, self.y)
            if 0 <= r_CDA[0] <= 1 and 0 <= r_CDA[1] <= 1 and 0 <= r_CDA[2] <= 1:
                y_CDA = r_CDA[0] * self.C + r_CDA[1] * self.D + r_CDA[2] * self.A
                in_triangle_CDA = True
        
        return {
            "in_triangle_ABC": in_triangle_ABC, #return if y is in the triangle
            "in_triangle_CDA": in_triangle_CDA, #return if y is in the triangle
            "r_ABC": r_ABC, #return the barycentric coordinates of ABC
            "r_CDA": r_CDA, #return the barycentric coordinates of CDA
            "y_ABC": y_ABC, #return the point y if in ABC
            "y_CDA": y_CDA #return the point y if in CDA
        }

    #plot the points and the triangles, none if there are NaN values
    def plot_point_and_tri(self):
        if np.isnan(self.A).any() or np.isnan(self.B).any() or np.isnan(self.C).any() or np.isnan(self.D).any():
            print("NaN")
            return
        #set the figure
        plt.figure(figsize=(8, 8))
        plt.scatter(self.X[:, 0], self.X[:, 1], c='blue', label='Points in X')
        plt.scatter(self.y[0], self.y[1], c='red', label='Point y', zorder=5)
        #plot the points if they are not NaN
        if not np.isnan(self.A).any():
            plt.scatter(*self.A, c='green', label='Point A', zorder=5)
        if not np.isnan(self.B).any():
            plt.scatter(*self.B, c='orange', label='Point B', zorder=5)
        if not np.isnan(self.C).any():
            plt.scatter(*self.C, c='purple', label='Point C', zorder=5)
        if not np.isnan(self.D).any():
            plt.scatter(*self.D, c='brown', label='Point D', zorder=5)
        
        #plot the triangles if they are not NaN
        if not np.isnan(self.A).any() and not np.isnan(self.B).any() and not np.isnan(self.C).any():
            plt.plot([self.A[0], self.B[0], self.C[0], self.A[0]], [self.A[1], self.B[1], self.C[1], self.A[1]], 'green', label='Triangle ABC', linestyle='dashed')
        if not np.isnan(self.C).any() and not np.isnan(self.D).any() and not np.isnan(self.A).any():
            plt.plot([self.C[0], self.D[0], self.A[0], self.C[0]], [self.C[1], self.D[1], self.A[1], self.C[1]], 'orange', label='Triangle CDA', linestyle='dashed')
        
        #Define labels, title and legend
        plt.xlabel('$x_1$')
        plt.ylabel('$x_2$')
        plt.title('Points and Triangles')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    #define the function to approximate f for question 3
    def approx_f(self):
        result = self.check_y_in_tri()

        f_y_ABC = np.nan
        f_y_CDA = np.nan
        
        if result["in_triangle_ABC"]:
            f_y_ABC = result["r_ABC"][0] * self.f(self.A) + result["r_ABC"][1] * self.f(self.B) + result["r_ABC"][2] * self.f(self.C)
            print(f"y is in the triangle ABC with coordinates: {result['y_ABC']}")
            print(f"Barycentric coordinates in triangle ABC: {result['r_ABC']}")
        else:
            print("y is not in the triangle ABC")
            if result["r_ABC"] is not None:
                print(f"Barycentric coordinates for ABC: {result['r_ABC']}")
        
        if result["in_triangle_CDA"]:
            f_y_CDA = result["r_CDA"][0] * self.f(self.C) + result["r_CDA"][1] * self.f(self.D) + result["r_CDA"][2] * self.f(self.A)
            print(f"y is in the triangle CDA with coordinates: {result['y_CDA']}")
            print(f"Barycentric coordinates in triangle CDA: {result['r_CDA']}")
        else:
            print("y is not in the triangle CDA")
            if result["r_CDA"] is not None:
                print(f"Barycentric coordinates for CDA: {result['r_CDA']}")
        
        # Choose the best approximation
        if not np.isnan(f_y_ABC):
            f_y = f_y_ABC
        elif not np.isnan(f_y_CDA):
            f_y = f_y_CDA
        else:
            f_y = np.nan

        # True value of f(y)
        true_value = self.f(self.y)

        # Print the approximation as well as the true value
        print("Approximation f(y):", f_y)
        print("True value f(y):", true_value)
        return f_y, true_value

