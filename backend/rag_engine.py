import os
import requests
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

# Cargar variables de entorno
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Inicializar cliente de ChromaDB
client = chromadb.PersistentClient(path="datos/db_biblia")
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_or_create_collection(
    name="versiculos", embedding_function=embedding_func
)

def responder_pregunta(pregunta: str, k: int = 6) -> str:
    resultados = collection.query(query_texts=[pregunta], n_results=k)
    versiculos = resultados["documents"][0]

    if not versiculos:
        return "No se encontraron versículos relevantes."

    contexto = "\n".join(versiculos)
    prompt = f"""Eres un experto bíblico. Responde con claridad y fidelidad al texto.

Contexto:
{contexto}

Pregunta: {pregunta}
Respuesta:"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "Responde como un experto bíblico, claro y fiel al texto."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        return "Ocurrió un error inesperado al generar la respuesta."
    except Exception as e:
        return f"Error al conectar con Groq: {e}"