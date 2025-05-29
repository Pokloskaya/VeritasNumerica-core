import sympy as sy


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n/10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


# Function to know if a list has repeated elements
def has_duplicates(list):
    return len(list) != len(set(list))


def order_together(x, y):
    combined = list(zip(x, y))
    combined.sort()
    ordered_x, ordered_y = zip(*combined)

    return ordered_x, ordered_y


# Matriz de vandermonde, vector b, polinomio, error
def Vandermonde(x: list, y: list) -> (list, list, str, str):
    if has_duplicates(x):
        return None, None, None, "The list has repeated elements"

    degree = len(x)

    # Vandermond matrix
    A = sy.zeros(degree)
    for i in range(degree):
        for j in range(degree):
            A[i, j] = x[i] ** j

    # Solve the system
    a = A.inv() * sy.Matrix(y)

    # Get the polynomial
    p = ""
    for i in range(degree):
        j = (degree-1) - i
        term = str(abs(a[j])) + ('x' if j > 0 else '') + \
            (f'^{j}' if j > 1 else '')
        if i == 0:
            p += '-' if a[j]*-1 > 0 else ''
        else:
            p += ' - ' if a[j]*-1 > 0 else ' + '
        p += term

    v_matrix = [[float(x) for x in row] for row in A.tolist()]

    return v_matrix, y, p, None


def Newton(x, y) -> (dict, str, str):
    if has_duplicates(x):
        return None, None, None, "The list has repeated elements"
    degree = len(x)
    x = sy.Matrix(x)
    y = sy.Matrix(y)

    dd = sy.zeros(degree)
    b = []
    for i in range(degree):
        for j in range(degree):
            if j == 0:
                dd[i, j] = y[i]
            elif i < j:
                dd[i, j] = dd[i, j]
            else:
                # Calculo de diferencias divididas
                dd[i, j] = (dd[i, j-1] - dd[i - 1, j-1])/(x[i] - x[i - j])

            if i == j:
                b.append(dd[i, j])  # Coeficiente 'b'

    polynomial = ""
    for i in range(degree):
        if i == 0:
            polynomial += f'{float(b[i])}'
        else:
            polynomial += ' - ' if b[i] < 0 else ' + '
            polynomial += f'({abs(float(b[i]))})'
            for j in range(i):
                if x[j] < 0:
                    polynomial += f'(x + {abs(float(x[j]))})'
                else:
                    polynomial += f'(x - {float(x[j])})'

    dd = dd.tolist()
    rows, columns = [], []
    for i in range(degree):
        rows.append([float(x) for x in dd[i]])
        if i == 0:
            columns.append('f[0]')
        else:
            columns.append(ordinal(i))

    table = {
        "columns": columns,
        "rows": rows
    }

    return table, polynomial, None


def L_k(x: list, k: int) -> (str, str):
    top = ''
    bot = 1
    for i in range(len(x)):
        if i != k:
            bot *= (x[k] - x[i])

        if x[i] < 0 and i != k:
            top += f'(x + {abs(x[i])})'
        elif i != k:
            top += f'(x - {x[i]})'

    return f'({top})/({bot})', f'\\frac{{{top}}}{{{bot}}}'


def Lagrange(x: list, y: list) -> (str, str, str):
    if has_duplicates(x):
        return None, None, "The list has repeated elements"
    degree = len(x)
    polynomial = ''
    texPolynomial = ''
    for i in range(degree):
        coef, texCoef = L_k(x, i)
        if i != 0:
            polynomial += ' + '
            texPolynomial += ' + '
        polynomial += f'{coef}{y[i]}'
        texPolynomial += f'{texCoef}{y[i]}'

    return polynomial, texPolynomial, None


def LinearSpline(x: list, y: list) -> (list, list, str):
    if has_duplicates(x):
        return None, None, "The list has repeated elements"
    x, y = order_together(x, y)
    n = len(x)
    A = sy.zeros((2*(n-1)))
    b = sy.Matrix([0 for _ in range(2*(n-1))])

    c = 0
    h = 0
    for i in range(n-1):
        A[i, c] = x[i]
        A[i, c+1] = 1
        b[i] = y[i]
        c += 2
        h += 1

    c = 0
    for i in range(1, n):
        A[h, c] = x[i]
        A[h, c+1] = 1
        b[h] = y[i]
        c += 2
        h += 1

    val = A.inv() * b
    val = val.reshape(n-1, 2).tolist()
    val = [[float(x) for x in row] for row in val]

    tracers = []
    for i in range(n-1):
        sign = '+' if val[i][1] >= 0 else '-'
        tracer = f'{val[i][0]}x {sign} {abs(val[i][1])}'
        # range and tracer
        tracers.append([[x[i], x[i+1]], tracer])
    return val, tracers, None


def CubicSpline(x: list, y: list) -> (list, list, str):
    if has_duplicates(x):
        return None, None, "The list has repeated elements"
    x, y = order_together(x, y)
    n = len(x)
    A = sy.zeros((4*(n-1)))
    b = sy.Matrix([0 for _ in range(4*(n-1))])

    c = 0
    h = 0
    for i in range(n-1):
        A[i, c] = x[i]**3
        A[i, c+1] = x[i]**2
        A[i, c+2] = x[i]
        A[i, c+3] = 1
        b[i] = y[i]
        c += 4
        h += 1

    c = 0
    for i in range(1, n):
        A[h, c] = x[i]**3
        A[h, c+1] = x[i]**2
        A[h, c+2] = x[i]
        A[h, c+3] = 1
        b[h] = y[i]
        c += 4
        h += 1

    c = 0
    for i in range(1, n-1):
        A[h, c] = 3*x[i]**2
        A[h, c+1] = 2*x[i]
        A[h, c+2] = 1
        A[h, c+4] = -3*x[i]**2
        A[h, c+5] = -2*x[i]
        A[h, c+6] = -1
        b[h] = 0
        c += 4
        h += 1

    c = 0
    for i in range(1, n-1):
        A[h, c] = 6*x[i]
        A[h, c+1] = 2
        A[h, c+4] = -6*x[i]
        A[h, c+5] = -2
        b[h] = 0
        c += 4
        h += 1

    A[h, 0] = 6*x[0]
    A[h, 1] = 2
    b[h] = 0
    h += 1
    A[h, c] = 6*x[n-1]
    A[h, c+1] = 2
    b[h] = 0

    val = A.inv() * b
    val = val.reshape(n-1, 4).tolist()
    val = [[float(x) for x in row] for row in val]

    tracers = []
    for i in range(n-1):
        signs = ['+' if val[i][j] >= 0 else '-' for j in range(4)]
        tracer = f'{val[i][0]}x^3 {signs[1]} {abs(val[i][1])}x^2 {signs[2]} {abs(val[i][2])}x {signs[3]} {abs(val[i][3])}'
        tracers.append([[x[i], x[i+1]], tracer])
    return val, tracers, None

