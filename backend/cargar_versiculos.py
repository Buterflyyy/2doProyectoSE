import chromadb
from chromadb.utils import embedding_functions

# Inicializamos ChromaDB con el mismo path que usás en tu app
client = chromadb.PersistentClient(path="datos/db_biblia")

# Embedding function compatible con lo que usás en tu backend
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="versiculos",
    embedding_function=embedding_func
)

# Versículos base para poblar
versiculos = [
    "En el principio creó Dios los cielos y la tierra.",
    "Jesús lloró.",
    "El Señor es mi pastor, nada me faltará.",
    "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito...",
    "Yo soy el camino, la verdad y la vida.",
    "Amarás a tu prójimo como a ti mismo.",
    "Todo lo puedo en Cristo que me fortalece."
]

# Cargar a la colección
collection.add(
    documents=versiculos,
    ids=[f"vers_{i}" for i in range(len(versiculos))]
)

print("✅ Versículos cargados correctamente.")