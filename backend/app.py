from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import responder_pregunta

app = FastAPI()

# Permitir conexión desde tu frontend React (ajustable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Recomendado cambiar a ["http://localhost:3000"] si sabés el origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregunta(BaseModel):
    texto: str

@app.post("/preguntar")
def preguntar(pregunta: Pregunta):
    respuesta = responder_pregunta(pregunta.texto)
    return {"respuesta": respuesta}