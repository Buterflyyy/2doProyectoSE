import chromadb
from chromadb.utils import embedding_functions
from transformers import pipeline  # Usaremos transformers

# 1. Configuramos el cliente para usar la base persistente
client = chromadb.PersistentClient(path="chatbot/datos/db_biblia")

# 2. Definimos la función de embeddings
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 3. Cargamos la colección existente
collection = client.get_or_create_collection(name="versiculos", embedding_function=embedding_func)

# Crear el pipeline para generación de texto con el modelo GPT-2
chatbot = pipeline("text-generation", model="gpt2")

def responder_pregunta(pregunta: str, k=5):
    # Obtener los resultados de los versículos más relevantes
    resultados = collection.query(
        query_texts=[pregunta],
        n_results=k
    )

    versiculos = resultados["documents"][0]
    contexto = "\n".join(versiculos)

    # Generar la respuesta usando GPT-2 (transformers)
    prompt = f"""
    Sos un experto en la Biblia. Respondé la siguiente pregunta de forma clara y directa,
    basándote exclusivamente en los siguientes versículos:

    {contexto}

    Pregunta: {pregunta}
    Respuesta:
    """

    # Generar respuesta
    respuesta = chatbot(prompt, max_length=100)[0]['generated_text']
    
    # Mostrar la respuesta
    print(f"\n🔎 Pregunta: {pregunta}")
    print("\n📖 Respuesta:")
    print(respuesta)


if __name__ == "__main__":
    responder_pregunta("¿Cuántos días estuvo Jesús en el desierto?")
