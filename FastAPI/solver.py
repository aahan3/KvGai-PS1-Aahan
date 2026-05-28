from sympy import *
from sympy.parsing.sympy_parser import parse_expr

from scipy.integrate import solve_ivp

import numpy as np


# =====================================================
# 1D SOLVER
# =====================================================

def solve_1d(simulation_data):

    equation = simulation_data.equation

    # Fixed parameters for 1d
    a_val = simulation_data.parameters.a
    b_val = simulation_data.parameters.b
    c_val = simulation_data.parameters.c

    # Initial conditions
    x0_val = simulation_data.initial_conditions.x0
    v0_val = simulation_data.initial_conditions.v0

    # Symbols
    t = symbols('t')

    x0, x1 = symbols('x0 x1')

    a, b, c = symbols('a b c')

    # =================================================
    # PARSE EQUATION
    # =================================================

    rhs = parse_expr(

        equation,

        local_dict={
            "x0": x0,
            "x1": x1,
            "a": a,
            "b": b,
            "c": c
        }
    )

    # =================================================
    # SUBSTITUTE PARAMETERS
    # =================================================

    rhs = rhs.subs({

        a: a_val,
        b: b_val,
        c: c_val
    })

    # =================================================
    # CREATE NUMERICAL FUNCTION
    # =================================================

    f_rhs = lambdify(

        (t, x0, x1),

        rhs,

        modules="numpy"
    )

    # =================================================
    # FIRST ORDER SYSTEM
    # =================================================

    def system(t, y):

        position = y[0]
        velocity = y[1]

        return [

            velocity,

            f_rhs(
                t,
                position,
                velocity
            )
        ]

    # =================================================
    # SOLVE SYSTEM
    # =================================================

    t_eval = np.linspace(0, 10, 500)

    sol = solve_ivp(

        system,

        [0, 10],

        [x0_val, v0_val],

        t_eval=t_eval
    )

    # =================================================
    # RETURN DATA
    # =================================================

    return {

        "system_dimension": "1d",

        "t_values": sol.t.tolist(),

        "x_values": sol.y[0].tolist(),

        "v_values": sol.y[1].tolist()
    }


# =====================================================
# 2D SOLVER
# =====================================================

def solve_2d(simulation_data):

    equations = simulation_data.equations

    dx_eq = equations.dx
    dy_eq = equations.dy

    # =================================================
    # INITIAL CONDITIONS
    # =================================================

    x0_val = simulation_data.initial_conditions.x0
    y0_val = simulation_data.initial_conditions.y0

    # =================================================
    # PARAMETERS
    # =================================================

    parameters = simulation_data.parameters

    # =================================================
    # SYMBOLS
    # =================================================

    t = symbols('t')

    x, y = symbols('x y')

    # =================================================
    # CREATE DYNAMIC PARAMETER SYMBOLS
    # =================================================

    parameter_symbols = {}

    for param_name in parameters.keys():

        parameter_symbols[param_name] = symbols(
            param_name
        )

    # =================================================
    # LOCAL DICTIONARY
    # =================================================

    local_dict = {

        "x": x,
        "y": y,
        "t": t,

        **parameter_symbols
    }

    # =================================================
    # PARSE EQUATIONS
    # =================================================

    dx_rhs = parse_expr(

        dx_eq,

        local_dict=local_dict
    )

    dy_rhs = parse_expr(

        dy_eq,

        local_dict=local_dict
    )

    # =================================================
    # FIND FREE PARAMETER SYMBOLS
    # =================================================

    all_symbols = dx_rhs.free_symbols.union(
        dy_rhs.free_symbols
    )

    reserved_symbols = {
        x,
        y,
        t
    }

    free_parameter_symbols = (
        all_symbols - reserved_symbols
    )

    # =================================================
    # BUILD SUBSTITUTION DICTIONARY
    # =================================================

    subs_dict = {}

    for sym in free_parameter_symbols:

        name = str(sym)

        if name not in parameters:

            raise ValueError(
                f"Missing parameter: {name}"
            )

        subs_dict[sym] = parameters[name]

    # =================================================
    # SUBSTITUTE PARAMETERS
    # =================================================

    dx_rhs = dx_rhs.subs(
        subs_dict
    )

    dy_rhs = dy_rhs.subs(
        subs_dict
    )

    # =================================================
    # CREATE NUMERICAL FUNCTIONS
    # =================================================

    f_dx = lambdify(

        (t, x, y),

        dx_rhs,

        modules="numpy"
    )

    f_dy = lambdify(

        (t, x, y),

        dy_rhs,

        modules="numpy"
    )

    # =================================================
    # SYSTEM
    # =================================================

    def system(t, state):

        x_val = state[0]
        y_val = state[1]

        return [

            f_dx(
                t,
                x_val,
                y_val
            ),

            f_dy(
                t,
                x_val,
                y_val
            )
        ]

    # =================================================
    # SOLVE TRAJECTORY
    # =================================================

    t_eval = np.linspace(0, 20, 1000)

    sol = solve_ivp(

        system,

        [0, 20],

        [x0_val, y0_val],

        t_eval=t_eval
    )

    # =================================================
    # VECTOR FIELD GRID
    # =================================================

    x_grid = np.linspace(-100, 100, 50)

    y_grid = np.linspace(-100, 100, 50)

    X, Y = np.meshgrid(
        x_grid,
        y_grid
    )

    DX = np.zeros_like(X)

    DY = np.zeros_like(Y)

    # =================================================
    # COMPUTE VECTOR FIELD
    # =================================================

    for i in range(X.shape[0]):

        for j in range(X.shape[1]):

            x_val = X[i, j]
            y_val = Y[i, j]

            try:

                dx_val = f_dx(
                    0,
                    x_val,
                    y_val
                )

                dy_val = f_dy(
                    0,
                    x_val,
                    y_val
                )

                DX[i, j] = dx_val
                DY[i, j] = dy_val

            except:

                DX[i, j] = 0
                DY[i, j] = 0

    # =================================================
    # NORMALIZE VECTORS
    # =================================================

    magnitude = np.sqrt(
        DX**2 + DY**2
    )

    magnitude[magnitude == 0] = 1

    DX = DX / magnitude
    DY = DY / magnitude

    # =================================================
    # RETURN DATA
    # =================================================

    return {

        "system_dimension": "2d",

        # =============================================
        # TRAJECTORY
        # =============================================

        "trajectory": {

            "t_values": sol.t.tolist(),

            "x_values": sol.y[0].tolist(),

            "y_values": sol.y[1].tolist()
        },

        # =============================================
        # VECTOR FIELD
        # =============================================

        "vector_field": {

            "X": X.tolist(),

            "Y": Y.tolist(),

            "DX": DX.tolist(),

            "DY": DY.tolist()
        }
    }


# =====================================================
# MAIN ENTRY
# =====================================================

def solve_system(simulation_data):

    dimension = simulation_data.system_dimension

    if dimension == "1d":

        return solve_1d(
            simulation_data
        )

    elif dimension == "2d":

        return solve_2d(
            simulation_data
        )

    else:

        return {

            "error": "Unsupported system dimension"
        }