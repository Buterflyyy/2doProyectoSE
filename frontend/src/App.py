from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir llamadas desde el frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Podés poner ["http://localhost:5173"] si querés más seguridad
    allow_methods=["*"],
    allow_headers=["*"],
)

class PreguntaInput(BaseModel):
    pregunta: str

@app.post("/preguntar")
def responder_pregunta(input: PreguntaInput):
    # Por ahora devolvemos algo de prueba para confirmar que funciona
    return {"respuesta": f"🎯 Esto sí funciona: preguntaste '{input.pregunta}'"}