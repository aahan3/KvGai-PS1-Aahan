import math, sympy
from sympy import symbols, sympify, solve
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from scipy.integrate import solve_ivp

def time_value(eq):
    
    a_val = 3
    b_val = 4
    c_val = 5


    eq = eq.replace("x", "x(t)")
    eq = eq.replace("x(t)''", "Derivative(x(t), t, 2)")
    eq = eq.replace("x(t)'", "Derivative(x(t), t)")
    
    left, right = eq.split("=")
    sympy_eq = f"Eq({left}, {right})"
    print(sympy_eq)

    t = symbols('t')
    a, b, c = symbols('a b c')
    x = Function('x')

    ode = parse_expr(
        sympy_eq,
        local_dict={
            'x': x,
            't': t,
            'a': a,
            'b': b,
            'c': c,
            'Derivative': Derivative,
            'Eq': Eq
        }
    )
    print(ode)
    rhs = solve(ode, x(t).diff(t,2))[0]
    print(rhs)

    x0, x1 = symbols('x0 x1')
    rhs = rhs.subs(Derivative(x(t), t), x1)
    rhs = rhs.subs(x(t), x0)
    f_rhs = lambdify(
    (t, x0, x1, a, b, c),
    rhs
    )
    def system(t, y):

        x0 = y[0]
        x1 = y[1]

        return [
            x1,
            f_rhs(t, x0, x1, a_val, b_val, c_val)
        ]
    sol = solve_ivp(
    system,
    [0, 10],
    [1, 0]
    )
    print(sol)
   


if __name__ == "__main__":
    time_value("x'' + a*x' + b*x = c")