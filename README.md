# Nombre del proyecto: Asistente Bíblico con IA

Descripción del sistema: Esta aplicación permite hacer preguntas bíblicas en lenguaje natural a través de una interfaz en React. Las respuestas son generadas mediante un backend en FastAPI, utilizando un sistema RAG con Chroma DB y el modelo Groq.

## Tecnologías usadas:
- React + Vite (frontend)
- FastAPI (backend)
- Chroma DB (base vectorial)
- SentenceTransformer (embeddings)
- Groq LLaMA3 (modelo de lenguaje)

## Cómo ejecutar el proyecto?

### Backend:
bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload

### Frontend
bash
cd frontend
npm install
npm run dev

Abre http://localhost:5173 para usar la aplicación.

### 5. Ejemplo de pregunta

```markdown
## Ejemplo de uso

> ¿Qué dice la Biblia sobre el perdón?

# El sistema consulta versículos relevantes, genera una respuesta con IA y la muestra en pantalla.

## 📂 Estructura del proyecto

- `/frontend`: código de React
- `/backend`: FastAPI + lógica de inferencia con Groq
- `/datos/db_biblia`: base vectorial de versículos