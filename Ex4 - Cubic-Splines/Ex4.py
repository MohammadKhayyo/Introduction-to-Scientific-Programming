import math
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify


def fill_x_y(_from, _to, number_of_splines):
    """Divides the range into equal pieces, then fills the x-values array and the y-values array.
    The function used here is (sin(x) + cos(x))^(1/3).
    Returns both arrays.
    """
    x = np.array([])
    y = np.array([])
    jumps = (abs(_to - _from) / number_of_splines)
    for i in range(0, number_of_splines + 1):
        if i == 0:
            x = np.append(x, _from)
        elif i == number_of_splines:
            x = np.append(x, _to)
        else:
            x = np.append(x, (_from + jumps * i))
        root_function = np.cbrt(math.sin(x[i]) + math.cos(x[i]))
        y = np.append(y, root_function)
    return x, y


def initialization(x, y, number_of_splines):
    """The initialization phase of Tomas algorithm. Returns 2 arrays."""
    b = np.array([])
    h = np.array([])
    for i in range(0, number_of_splines):
        h = np.append(h, x[i + 1] - x[i])
        b = np.append(b, 6 * (y[i + 1] - y[i]) / h[i])
    return h, b


def reduction(h, b, number_of_splines):
    """Reduction phase of Tomas algorithm."""
    u = np.array([0])
    v = np.array([0])
    u = np.append(u, (2 * (h[0] + h[1])))
    v = np.append(v, (b[1] - b[0]))
    for i in range(2, number_of_splines):
        u = np.append(u, 2 * (h[i] + h[i - 1]) - ((h[i] ** 2) / u[i - 1]))
        v = np.append(v, (b[i] - b[i - 1]) - (((h[i - 1] ** 2) / u[i - 1]) * v[i - 1]))
    return u, v


def bottom_top_solution(u, v, h, number_of_splines):
    """bottom top solution of Tomas algorithm. Returns the array z containing the z-values."""
    z = np.zeros(number_of_splines + 1)
    for i in range(number_of_splines - 1, 0, -1):
        z[i] = (v[i] - (h[i] * z[i + 1])) / u[i]
    return z


def calculate_coefficients_c_d(y, z, h, number_of_splines):
    """Calculates the coefficients c(i) and d(i), and appends them to arrays c d."""
    c = np.array([])
    d = np.array([])
    for i in range(0, number_of_splines):
        d = np.append(d, (y[i] / h[i]) - ((z[i] * h[i]) / 6))
        c = np.append(c, (y[i + 1] / h[i]) - ((z[i + 1] * h[i]) / 6))
    return c, d


def calculate_polynomial(x, c, d, h, z, number_of_splines):
    """Calculates the polynomial for each spline. Returns a list containing the polynomials."""
    s = []
    for i in range(0, number_of_splines):
        s.append((z[i] / (6 * h[i])) * ((x[i + 1] - x_var) ** 3)
                 + ((z[i + 1] / (6 * h[i])) * ((x_var - x[i]) ** 3))
                 + (c[i] * (x_var - x[i])) + (d[i] * (x[i + 1] - x_var)))
    return s


def graph_function(_from, _to, number_of_splines, cubic_splines):
    """Graphs the function by drawing it using matplotlib. Each spline is drawn in a different color."""
    x = np.arange(_from, _to, 0.001)
    y = lambdify(x_var, np.cbrt(np.sin(x)+np.cos(x)), "numpy")
    plt.plot(x, y(x))
    jumps = (abs(_to - _from) / number_of_splines)
    for i in range(0, number_of_splines):
        x_range = np.arange(_from + jumps * i, _from + jumps * (i + 1), 0.001)
        y_image = lambdify(x_var, cubic_splines[i], "numpy")
        plt.plot(x_range, y_image(x_range))
        plt.title("{:d} - Splines".format(number_of_splines) + " with The Function")
    plt.grid(True)
    plt.axhline(0, color='k')
    plt.axvline(0, color='k')
    axes = plt.gca()
    axes.set_xlim([int(_from - 1), int(_to + 1)])
    axes.set_ylim([int(- 3), int(3)])
    plt.xlabel("X - axis")
    plt.ylabel("Y - axis")
    plt.show()


def main():
    """Main function of the program. Has a list containing the numbers of splines, and two values indicating the range.
    The function interpolates a mathematical function using "Cubic Splines", then draws it using matplotlib.
    Read more about Splines: https://en.wikipedia.org/wiki/Spline_interpolation"""
    splines_list = [2, 4, 6, 12]
    _from = -6
    _to = 6
    for i in range(0, len(splines_list)):
        number_of_splines = splines_list[i]
        x, y = fill_x_y(_from, _to, number_of_splines)
        h, b = initialization(x, y, number_of_splines)
        u, v = reduction(h, b, number_of_splines)
        z = bottom_top_solution(u, v, h, number_of_splines)
        c, d = calculate_coefficients_c_d(y, z, h, number_of_splines)
        cubic_splines = calculate_polynomial(x, c, d, h, z, number_of_splines)
        graph_function(_from, _to, number_of_splines, cubic_splines)


x_var = symbols('x')
main()
