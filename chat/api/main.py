from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from processor import FeedbackProcessor
from responder import generar_respuesta
import uvicorn

app = FastAPI()
processor = FeedbackProcessor("base.csv")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restringe esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de entrada
class PreguntaInput(BaseModel):
    pregunta: str


@app.post("/chat")
def chat(payload: PreguntaInput):
    resultado = processor.search_similar_feedback(payload.pregunta)
    respuesta = generar_respuesta(payload.pregunta, resultado["respuestas"])
    return {
        "pregunta": resultado["pregunta"],
        "seccion_detectada": resultado["seccion_detectada"],
        "respuestas_similares": resultado["respuestas"],
        "respuesta_generada": respuesta,
    }


# Ejecutar como script
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
