import sympy as sy

def print_matrix(matrix: sy.Matrix, n: int):
    for i in range(n):
        for j in range(n):
            print(matrix[i, j], end=" ")
        print()
    print()

def t_and_c(
        A: sy.Matrix,
        b: sy.Matrix,
        method: str,
        w: float) -> (sy.Matrix, sy.Matrix):
    D = sy.DiagMatrix(A.diagonal())
    L, U = -A.lower_triangular(-1), -A.upper_triangular(+1),

    if method == "jacobi":
        T = D.inv() * (L + U)
        C = D.inv() * b
    else:
        T = (D - w*L).inv() * ((1-w)*D + w*U)
        C = w*(D - w*L).inv() * b

    print_matrix(T, A.rows)
    print(C)
    return T, C

def Iterative_methods(
        A: list,
        b: list,
        x0: list,
        tol: float,
        niter: int,
        method: str,
        relativeError: bool,
        w: float = 1) -> (list, dict, str):
    try:
        A = sy.Matrix(A)
        b = sy.Matrix(b)
        x0 = sy.Matrix(x0)
        print(w)
        if A.rows != A.cols or A.rows != b.rows or x0.rows != A.rows:
            return None, "Invalid dimensions"
        if not (0 <= w and w <= 2):
            return None, "W must be between 0 and 2"
    except Exception:
        return None, "Error in the input"
    err = tol + 1
    n = 0

    E, x_values = [100], [[float(x) for x in x0.flat()]]

    diag = A.diagonal()
    if 0 in diag:
        return None, "A contains zeros in its diagonal"

    T, C = t_and_c(A, b, method, w)

    while err > tol and n < niter:
        x1 = T*x0 + C
        if relativeError:
            err = (x1 - x0).norm(sy.oo)/x1.norm(sy.oo)
        else:
            err = (x1 - x0).norm(sy.oo)
        x0 = x1
        x_values.append([float(x) for x in x1.flat()])
        E.append(float(err))
        n += 1
    if n == niter:
        return None, f'Method failed in {n} iterations'

    data = {
        "T": [[float(x) for x in row] for row in T.tolist()],
        "C": [float(x) for x in C.flat()],
        "x": [float(x) for x in x0.flat()],
        "columns": ["n", "x", "error"],
        "rows": [[i, x_values[i], E[i]] for i in range(n+1)]
    }

    return data, None

