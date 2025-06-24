import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI  # ✅ Usamos la nueva clase del paquete openai
import os

# Clave secreta de OpenAI (podés ponerla directamente o usar variables de entorno)
client_openai = OpenAI(api_key="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")

# 1. Configuramos ChromaDB con base persistente
client_chroma = chromadb.PersistentClient(path="chatbot/datos/db_biblia")

# 2. Definimos la función de embeddings
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 3. Accedemos a la colección existente
collection = client_chroma.get_or_create_collection(name="versiculos", embedding_function=embedding_func)


def responder_pregunta(pregunta: str, k=5):
    # 4. Consultamos la colección con la pregunta
    resultados = collection.query(
        query_texts=[pregunta],
        n_results=k
    )

    # 5. Extraemos los versículos y formamos el contexto
    versiculos = resultados["documents"][0]
    contexto = "\n".join(versiculos)

    prompt = f"""
Sos un experto en la Biblia. Respondé la siguiente pregunta de forma clara y directa,
basándote exclusivamente en los siguientes versículos:

{contexto}

Pregunta: {pregunta}
Respuesta:
"""

    # 6. Enviamos la pregunta a la API de OpenAI
    respuesta = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Respondé como un experto bíblico, de forma clara y fiel al texto."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    # 7. Mostramos el resultado
    print(f"\n🔎 Pregunta: {pregunta}")
    print("\n📖 Respuesta:")
    print(respuesta.choices[0].message.content)


if __name__ == "__main__":
    responder_pregunta("¿Cuántos días estuvo Jesús en el desierto?")
