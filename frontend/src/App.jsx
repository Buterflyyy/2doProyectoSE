import { useState } from 'react'
import './App.css'

function App() {
  const [pregunta, setPregunta] = useState('')
  const [respuesta, setRespuesta] = useState('')
  const [cargando, setCargando] = useState(false)

  const hacerPregunta = async () => {
    if (!pregunta.trim()) return
    setCargando(true)
    try {
      console.log('🛫 Enviando JSON:', JSON.stringify({ pregunta }))
      const resp = await fetch('http://localhost:8000/preguntar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto: pregunta })
      })
      const data = await resp.json()
      console.log('📦 Respuesta del backend:', data) // ← Agregá esto
      setRespuesta(data.respuesta || 'No se pudo obtener respuesta')
    } catch (err) {
      setRespuesta('Ocurrió un error al consultar el servidor 😔')
    } finally {
      setCargando(false)
    }
  }

 return (
  <div className="page">
    <div className="container">
      <h1>Asistente Bíblico 🕊️</h1>
      <input
        type="text"
        value={pregunta}
        onChange={(e) => setPregunta(e.target.value)}
        placeholder="Escribí una pregunta bíblica..."
      />
      <button onClick={hacerPregunta} disabled={cargando}>
        {cargando ? 'Buscando...' : 'Preguntar'}
      </button>
      <br />
      {respuesta && (
        <div className="respuesta">
          <strong>Respuesta:</strong> {respuesta}
        </div>
      )}
    </div>
  </div>
)
}

export default App