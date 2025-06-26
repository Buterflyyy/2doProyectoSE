import os
import chromadb
from chromadb.utils import embedding_functions

# 🧭 Ruta absoluta hacia la base de datos
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "datos", "db_biblia")

# Inicializar cliente con ruta segura
client = chromadb.PersistentClient(path=DB_PATH)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(name="versiculos", embedding_function=embedding_func)

print(f"🧠 Total de documentos: {collection.count()}")
print("📌 Muestra:", collection.peek(3))