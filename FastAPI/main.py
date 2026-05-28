from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from ai import generate_simulation, explain_system
from solver import solve_system


app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)
def classify_validation_error(error_text):

    lower = error_text.lower()

    # =====================================
    # HIGHER DIMENSIONAL SYSTEMS
    # =====================================

    if (
        "theta" in lower
        or "x3" in lower
        or "x4" in lower
        or "theta1" in lower
    ):

        return (
            "This system requires more than "
            "2 state variables and is not "
            "currently supported."
        )

    # =====================================
    # MISSING DX/DY
    # =====================================

    if (
        "equations.dx" in lower
        or "equations.dy" in lower
    ):

        return (
            "The AI generated an invalid "
            "2D dynamical system."
        )

    # =====================================
    # MISSING INITIAL CONDITIONS
    # =====================================

    if (
        "initial_conditions" in lower
    ):

        return (
            "The generated system had invalid "
            "initial conditions."
        )

    return (
        "Unable to generate a valid "
        "simulation for this prompt."
    )


# =====================================================
# REQUEST MODEL
# =====================================================

class PromptRequest(BaseModel):

    prompt: str


# =====================================================
# ROOT ROUTE
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Physics Visualizer API Running"
    }


# =====================================================
# SIMULATION ROUTE
# =====================================================

@app.post("/simulate")
def simulate(req: PromptRequest):

    try:

        # =====================================
        # GENERATE AI SYSTEM
        # =====================================

        simulation_data = generate_simulation(
            req.prompt
        )

        print("\nSIMULATION DATA:")
        print(simulation_data)

        # =====================================
        # SOLVE SYSTEM
        # =====================================

        solution_data = solve_system(
            simulation_data
        )

        print("\nSOLUTION DATA:")
        print(solution_data)

        # =====================================
        # RETURN SUCCESS
        # =====================================

        return {

            "success": True,

            "simulation_data":
                simulation_data.model_dump(),

            "solution_data":
                solution_data
        }

    except ValidationError as e:

        message = classify_validation_error(
            str(e)
        )

        return {

            "success": False,

            "error_type": "validation_error",

            "message": message
        }


    except Exception as e:

        print("\nERROR:")
        print(str(e))

        return {

            "success": False,

            "error_type": "general_error",

            "message":

            (
                "Unable to generate a valid simulation "
                "for this prompt."
            )
        }

@app.post("/explain")
def explain(request: dict):

    try:

        simulation_data = request["simulation_data"]

        solution_data = request["solution_data"]

        explanation = explain_system(

            simulation_data,
            solution_data
        )

        return {

            "success": True,

            "explanation": explanation
        }

    except Exception as e:

        return {

            "success": False,

            "message": str(e)
        }