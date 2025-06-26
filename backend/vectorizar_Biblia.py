import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

# 1. Cargamos el dataset limpio
df = pd.read_csv("datos/biblia_ordenada.csv")

# 2. Usamos el modelo por defecto de sentence-transformers
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# 3. Creamos la base persistente
client = chromadb.PersistentClient(path="datos/db_biblia")

# 4. Creamos o accedemos a la colección
collection = client.get_or_create_collection(name="versiculos", embedding_function=embedding_func)

# 5. Insertamos los versos (por ahora solo si no hay nada)
if collection.count() == 0:
    print("Vectorizando versículos...")

    documentos = df["texto"].tolist()
    ids = [f"id_{i}" for i in range(len(documentos))]

    batch_size = 5000  # menor al máximo permitido
    for i in range(0, len(documentos), batch_size):
        print(f"Vectorizando lote {i // batch_size + 1}...")
        collection.add(
            documents=documentos[i:i+batch_size],
            ids=ids[i:i+batch_size]
        )

    print("¡Listo! Versículos vectorizados y guardados.")
else:
    print("Ya existen vectores, no se volvió a insertar nada.")
