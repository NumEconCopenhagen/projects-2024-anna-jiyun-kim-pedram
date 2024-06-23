import numpy as np  # Import numpy
#define algorithm
def sample(seed=2024):
    rng = np.random.default_rng(seed)
    X = rng.uniform(size=(50, 2))
    y = rng.uniform(size=(2,))
    return X, y

def block_1(A, B, C, y):
    denominator = ((B[1]-C[1])*(A[0]-C[0]) + (C[0]-B[0])*(A[1]-C[1]))
    r1 = ((B[1]-C[1])*(y[0]-C[0]) + (C[0]-B[0])*(y[1]-C[1])) / denominator
    r2 = ((C[1]-A[1])*(y[0]-C[0]) + (A[0]-C[0])*(y[1]-C[1])) / denominator
    r3 = 1 - r1 - r2
    return r1, r2, r3

def block_2(X, y):
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

def plot_pointtriangle(X, y, A, B, C, D):
    import matplotlib.pyplot as plt

    if np.isnan(A).any() or np.isnan(B).any() or np.isnan(C).any() or np.isnan(D).any():
        print("NaN")
        return

    plt.figure(figsize=(8, 8))
    plt.scatter(X[:, 0], X[:, 1], c='blue', label='Points in X')
    plt.scatter(y[0], y[1], c='red', label='Point y', zorder=5)

    if A is not None and not np.isnan(A).any():
        plt.scatter(*A, c='green', label='Point A', zorder=5)
    if B is not None and not np.isnan(B).any():
        plt.scatter(*B, c='orange', label='Point B', zorder=5)
    if C is not None and not np.isnan(C).any():
        plt.scatter(*C, c='purple', label='Point C', zorder=5)
    if D is not None and not np.isnan(D).any():
        plt.scatter(*D, c='brown', label='Point D', zorder=5)

    if A is not None and B is not None and C is not None and not np.isnan(A).any() and not np.isnan(B).any() and not np.isnan(C).any():
        plt.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'green', label='Triangle ABC', linestyle='dashed')
    if C is not None and D is not None and A is not None and not np.isnan(C).any() and not np.isnan(D).any() and not np.isnan(A).any():
        plt.plot([C[0], D[0], A[0], C[0]], [C[1], D[1], A[1], C[1]], 'orange', label='Triangle CDA', linestyle='dashed')

    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    plt.title('Points and Triangles')
    plt.legend()
    plt.grid(True)
    plt.show()


