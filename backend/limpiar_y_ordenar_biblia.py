import pandas as pd
import os

# Construir ruta al archivo CSV original
base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "..", "datos", "biblia.csv")

# Leer el CSV sin índice automático
df = pd.read_csv(csv_path)

# Eliminar columnas innecesarias como 'Unnamed: 0' si existe
if 'Unnamed: 0' in df.columns:
    df.drop(columns=['Unnamed: 0'], inplace=True)

# Renombrar columnas correctamente
df.columns = ['libro', 'capitulo', 'verso', 'texto']

# Eliminar filas problemáticas (si existen)
df.dropna(subset=['capitulo', 'verso'], inplace=True)

# Guardar archivo limpio y ordenado
output_path = os.path.join(base_dir, "..", "datos", "biblia_ordenada.csv")
df.to_csv(output_path, index=False)

print("✅ ¡Biblia ordenada correctamente sin columnas basura!")
