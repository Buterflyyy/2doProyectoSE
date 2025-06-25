import os
import requests
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

# 1. Cargar la clave GROQ desde el .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Inicializar ChromaDB y la colección
client = chromadb.PersistentClient(path="chatbot/datos/db_biblia")
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_or_create_collection(name="versiculos", embedding_function=embedding_func)

# 3. Función principal
def responder_pregunta(pregunta: str, k=5):
    # Paso 1: buscar versículos relevantes
    resultados = collection.query(query_texts=[pregunta], n_results=k)

    if not resultados["documents"] or not resultados["documents"][0]:
        print("⚠️ No se encontraron versículos relevantes.")
        return

    versiculos = resultados["documents"][0]
    contexto = "\n".join(versiculos)

    # Paso 2: armar el prompt para Groq
    prompt = f"""Eres un experto bíblico. Responde con claridad y fidelidad al texto.

Contexto:
{contexto}

Pregunta: {pregunta}
Respuesta:"""

    # Paso 3: llamar a la API de Groq
    url = "https://api.groq.com/openai/v1/chat/completions"
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
        response = requests.post(url, headers=headers, json=body)
        data = response.json()

        if "choices" in data:
            respuesta = data["choices"][0]["message"]["content"]
            print(f"\n🔎 Pregunta: {pregunta}\n")
            print("📖 Respuesta:")
            print(respuesta)
        else:
            print("❌ Error inesperado:")
            print(data)
    except Exception as e:
        print(f"❌ Ocurrió un error al conectar con Groq: {e}")

# 4. Punto de entrada
if __name__ == "__main__":
    responder_pregunta("¿Quién es Moíses?")