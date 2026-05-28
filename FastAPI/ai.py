from openai import OpenAI

from prompt import SYSTEM_PROMPT,key,EXPLAINER_PROMPT

import json
import os

from models import (
    Simulation1D,
    Simulation2D
)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)




def generate_simulation(prompt: str):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",
        
        max_tokens=300,
    
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    content = response.choices[0].message.content
    cleaned = (
    content
    .replace("```json", "")
    .replace("```", "")
    .strip()
    )
    parsed_json = json.loads(cleaned)

    print("\nRAW AI OUTPUT:")
    print(parsed_json)

    # =================================================
    # VALIDATE WITH PYDANTIC
    # =================================================

    if parsed_json["system_dimension"] == "1d":

        validated = Simulation1D(
            **parsed_json
        )

    elif parsed_json["system_dimension"] == "2d":

        validated = Simulation2D(
            **parsed_json
        )

    else:

        raise ValueError(
            "Unsupported system dimension"
        )

    return validated

def explain_system(simulation_data, solution_data):

    prompt = f"""
Simulation:
{simulation_data}

Solution:
{solution_data}

Explain the system behavior.
"""

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": EXPLAINER_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content