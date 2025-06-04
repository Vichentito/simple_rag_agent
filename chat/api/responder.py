# responder.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar la clave de OpenAI desde .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generar_respuesta(pregunta: str, comentarios: list[str]) -> str:
    prompt = (
        "Basándote en los siguientes comentarios de clientes:\n"
        + "\n".join(f"- {c}" for c in comentarios)
        + f"\n\nResponde a la siguiente pregunta: {pregunta}"
    )

    respuesta = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente útil que responde preguntas basándose en comentarios de clientes. Menciona absolutamente todos los temas del los que hablen los clientes sin omitir ninguno.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return respuesta.choices[0].message.content.strip()
