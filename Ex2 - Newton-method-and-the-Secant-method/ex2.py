# Murad Abu-Gosh
# Mohammad khayyo
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
from sympy import lambdify


def f(x):
    # evaluate the value of x.
    return eval(equation)


def diff(a):
    # differential function
    dx = 0.000000001
    r = (f(a + dx) - f(a)) / dx
    return r


def Newton(x0: float, Epsilon: float, lam: float, M: int):
    # find root and number of iterations using Newton's method
    if abs(f(x0)) < lam:  # if first guess was very accurate to root, return it.
        return x0
    a = x0
    for i in range(M):  # iterate maximum of M times
        y = f(a)
        try:
            xn = a - (y / diff(a))
        except ZeroDivisionError:
            print("Newton's Method Failed, Division By Zero")
            return None
        if abs(xn - a) < Epsilon:  # if the difference is smaller than Epsilon,found
            return xn, i+1
        if abs(f(xn)) < lam:  # if absolute value of f(x) smaller than lam, found
            return xn, i+1
        a = xn
    else:  # maximum number of iterations reached.
        print("No solution can be found")
        return None


def Miter(a0: float, b0: float, Epsilon, lamda, M: int):
    # find root and number of iterations using Miter method
    if abs(f(a0)) < lamda:  # if one of the two guesses is correct, return it
        return a0
    if abs(f(b0)) < lamda:
        return b0
    for i in range(M):  # iterate maximum of M times
        try:
            xn = b0 - (f(b0) * ((b0 - a0) / (f(b0) - f(a0))))  # Miter method
        except ZeroDivisionError:
            print("Miter Method Failed, Division By Zero")
            return None
        if abs(f(xn)) < lamda:
            return xn, i+1
        if abs(xn - b0) < Epsilon:
            return xn, i+1
        a0 = b0
        b0 = xn
    else:  # maximum number of iterations reached
        print("No solution can be found")
        return None


def graph_print(_from, _to, root, isRoot):
    # Graph print function
    x = np.arange(_from, _to, 0.01)
    y = lambdify(var_x, eval(equation), "numpy")
    plt.plot(x, y(x))
    plt.grid(True)
    plt.axhline(0, color='k')
    plt.axvline(0, color='k')
    axes = plt.gca()
    axes.set_xlim([int(_from), int(_to)])
    axes.set_ylim([-10, 10])
    if isRoot:
        plt.scatter(root, 0, s=120, edgecolors='red')
    plt.xlabel("(X) axes")
    plt.ylabel("(Y) axes")
    plt.title("f(x)= " + equation_string)
    plt.show()


var_x = sym.Symbol('x')
equation = "(np.exp(np.sin(x)) - x + 2)"  # equation to find the root of
equation_string = "e^sin(x)-x+1"  # string representation of the function
xr = 3
epsilon = 10 ** (-11)
b, Loop_Newton = Newton(xr, epsilon, epsilon, 1000)
xa = 3
xb = 4
c, Loop_Miter = Miter(xa, xb, epsilon, epsilon, 1000)
if b is not None:
    print("root using Newton's method: ", b, " .Number of loops taken: ", Loop_Newton)
else:
    print("No solution can be found using Newton's method")

if c is not None:
    print("root using Miter method: ", c, "Number of loops taken: ", Loop_Miter)
else:
    print("No solution can be found using Miter method")
if b is not None:
    graph_print(b - 10, b + 10, b, True)
elif c is not None:
    graph_print(c - 10, c + 10, c, True)
else:
    graph_print(- 10, 10, None, False)
