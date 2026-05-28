from pydantic import BaseModel
from typing import Literal, Dict


# =====================================================
# 1D PARAMETERS
# =====================================================

class Parameters1D(BaseModel):

    a: float
    b: float
    c: float


# =====================================================
# 1D INITIAL CONDITIONS
# =====================================================

class InitialConditions1D(BaseModel):

    x0: float
    v0: float


# =====================================================
# 2D INITIAL CONDITIONS
# =====================================================

class InitialConditions2D(BaseModel):

    x0: float
    y0: float


# =====================================================
# 2D EQUATIONS
# =====================================================

class Equations2D(BaseModel):

    dx: str
    dy: str


# =====================================================
# 1D SIMULATION
# =====================================================

class Simulation1D(BaseModel):

    system_dimension: Literal["1d"]

    simulation: str

    equation: str

    parameters: Parameters1D

    initial_conditions: InitialConditions1D


# =====================================================
# 2D SIMULATION
# =====================================================

class Simulation2D(BaseModel):

    system_dimension: Literal["2d"]

    simulation: str

    equations: Equations2D

    # DYNAMIC PARAMETERS
    parameters: Dict[str, float]

    initial_conditions: InitialConditions2D