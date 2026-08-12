from google import genai
from google.genai import types
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def load_cv():
    with open("data/ivan_cv.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_system_prompt() -> str:
    cv = load_cv()
    return f"""Eres el agente de CV de {cv['name']}.
Representas su perfil profesional de forma clara, honesta y natural.

INFORMACIÓN COMPLETA:
{json.dumps(cv, ensure_ascii=False, indent=2)}

REGLAS IMPORTANTES:
- Responde SOLO con información del CV. Nunca inventes datos.
- Si no tienes la información, di: "No tengo ese dato en mi perfil."
- Si preguntan salario o información privada, declina amablemente.
- Sé conversacional y natural. Máximo 3 párrafos por respuesta.
- Sé honesto sobre niveles de habilidad técnica.
- Responde siempre en español.
"""

async def get_response(messages: list) -> str:
    try:
        history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])]
                )
            )

        last_msg = messages[-1]["content"]

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=history + [types.Content(
                role="user",
                parts=[types.Part(text=last_msg)]
            )],
            config=types.GenerateContentConfig(
                system_instruction=build_system_prompt(),
                temperature=0.3,
            )
        )
        return response.text

    except Exception as e:
        print(f"Error en Gemini: {e}")
        return "Lo siento, ocurrió un error al procesar tu pregunta. Por favor intenta de nuevo."