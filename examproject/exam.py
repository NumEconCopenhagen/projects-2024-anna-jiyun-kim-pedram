import numpy as np # Import numpy 
import matplotlib.pyplot as plt # Import matplotlib.pyplot

class Model:
    def __init__(self, seed=2024):
        self.seed = seed
        self.X, self.y = self.sample(seed)
        self.A, self.B, self.C, self.D = self.block_2(self.X, self.y)

    def sample(self, seed):
        rng = np.random.default_rng(seed)
        X = rng.uniform(size=(50, 2))
        y = rng.uniform(size=(2,))
        return X, y

    def block_1(self, A, B, C, y):
        denominator = ((B[1]-C[1])*(A[0]-C[0]) + (C[0]-B[0])*(A[1]-C[1]))
        r1 = ((B[1]-C[1])*(y[0]-C[0]) + (C[0]-B[0])*(y[1]-C[1])) / denominator
        r2 = ((C[1]-A[1])*(y[0]-C[0]) + (A[0]-C[0])*(y[1]-C[1])) / denominator
        r3 = 1 - r1 - r2
        return r1, r2, r3

    def block_2(self, X, y):
        A = min((x for x in X if x[0] > y[0] and x[1] > y[1]), key=lambda x: np.linalg.norm(x - y), default=None)
        B = min((x for x in X if x[0] > y[0] and x[1] < y[1]), key=lambda x: np.linalg.norm(x - y), default=None)
        C = min((x for x in X if x[0] < y[0] and x[1] < y[1]), key=lambda x: np.linalg.norm(x - y), default=None)
        D = min((x for x in X if x[0] < y[0] and x[1] > y[1]), key=lambda x: np.linalg.norm(x - y), default=None)

        if A is None:
            A = np.nan
        if B is None:
            B = np.nan
        if C is None:
            C = np.nan
        if D is None:
            D = np.nan
        return A, B, C, D

    def check_y_in_tri(self):
        if not np.isnan(self.A).any() and not np.isnan(self.B).any() and not np.isnan(self.C).any():
            r_ABC = self.block_1(self.A, self.B, self.C, self.y)
            if 0 <= r_ABC[0] <= 1 and 0 <= r_ABC[1] <= 1 and 0 <= r_ABC[2] <= 1:
                y_ABC = r_ABC[0] * self.A + r_ABC[1] * self.B + r_ABC[2] * self.C
                return "ABC", y_ABC
        if not np.isnan(self.C).any() and not np.isnan(self.D).any() and not np.isnan(self.A).any():
            r_CDA = self.block_1(self.C, self.D, self.A, self.y)
            if 0 <= r_CDA[0] <= 1 and 0 <= r_CDA[1] <= 1 and 0 <= r_CDA[2] <= 1:
                y_CDA = r_CDA[0] * self.C + r_CDA[1] * self.D + r_CDA[2] * self.A
                return "CDA", y_CDA
        return None, None

    def plot_point_and_tri(self):
        if np.isnan(self.A).any() or np.isnan(self.B).any() or np.isnan(self.C).any() or np.isnan(self.D).any():
            print("NaN")
            return

        plt.figure(figsize=(8, 8))
        plt.scatter(self.X[:, 0], self.X[:, 1], c='blue', label='Points in X')
        plt.scatter(self.y[0], self.y[1], c='red', label='Point y', zorder=5)

        if not np.isnan(self.A).any():
            plt.scatter(*self.A, c='green', label='Point A', zorder=5)
        if not np.isnan(self.B).any():
            plt.scatter(*self.B, c='orange', label='Point B', zorder=5)
        if not np.isnan(self.C).any():
            plt.scatter(*self.C, c='purple', label='Point C', zorder=5)
        if not np.isnan(self.D).any():
            plt.scatter(*self.D, c='brown', label='Point D', zorder=5)

        if not np.isnan(self.A).any() and not np.isnan(self.B).any() and not np.isnan(self.C).any():
            plt.plot([self.A[0], self.B[0], self.C[0], self.A[0]], [self.A[1], self.B[1], self.C[1], self.A[1]], 'green', label='Triangle ABC', linestyle='dashed')
        if not np.isnan(self.C).any() and not np.isnan(self.D).any() and not np.isnan(self.A).any():
            plt.plot([self.C[0], self.D[0], self.A[0], self.C[0]], [self.C[1], self.D[1], self.A[1], self.C[1]], 'orange', label='Triangle CDA', linestyle='dashed')

        plt.xlabel('$x_1$')
        plt.ylabel('$x_2$')
        plt.title('Points and Triangles')
        plt.legend()
        plt.grid(True)
        plt.show()
