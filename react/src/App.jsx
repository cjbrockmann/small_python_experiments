import { useEffect, useMemo, useState } from 'react'
import './App.css'

function App() {
  const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'
  const [plaetze, setPlaetze] = useState([])
  const [fahrzeugtyp, setFahrzeugtyp] = useState('PKW')
  const [isLoading, setIsLoading] = useState(true)
  const [isBusy, setIsBusy] = useState(false)
  const [status, setStatus] = useState('')
  const [error, setError] = useState('')

  const belegtePlaetze = useMemo(
    () => plaetze.filter((platz) => platz.belegt).length,
    [plaetze],
  )

  const freiePlaetze = useMemo(
    () => plaetze.filter((platz) => !platz.belegt).length,
    [plaetze],
  )

  async function ladeStatus() {
    try {
      setError('')
      const response = await fetch(`${apiBase}/parkhaus/status`)
      if (!response.ok) {
        throw new Error('Status konnte nicht geladen werden.')
      }
      const data = await response.json()
      setPlaetze(data.plaetze ?? [])
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    ladeStatus()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleEinfahrt() {
    setIsBusy(true)
    setError('')
    setStatus('')
    try {
      const response = await fetch(`${apiBase}/parkhaus/einfahrt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fahrzeugtyp }),
      })
      const data = await response.json()
      setPlaetze(data.plaetze ?? [])
      setStatus(data.message ?? 'Einfahrt verarbeitet.')
      if (data.status === 'error') {
        setError(data.message ?? 'Einfahrt fehlgeschlagen.')
      }
    } catch {
      setError('API ist nicht erreichbar.')
    } finally {
      setIsBusy(false)
    }
  }

  async function handleAusfahrt(platz) {
    setIsBusy(true)
    setError('')
    setStatus('')
    try {
      const response = await fetch(`${apiBase}/parkhaus/ausfahrt/${platz}`, {
        method: 'POST',
      })
      const data = await response.json()
      setPlaetze(data.plaetze ?? [])
      setStatus(data.message ?? 'Ausfahrt verarbeitet.')
      if (data.status === 'error') {
        setError(data.message ?? 'Ausfahrt fehlgeschlagen.')
      }
    } catch {
      setError('API ist nicht erreichbar.')
    } finally {
      setIsBusy(false)
    }
  }

  return (
    <main className="app">
      <header className="app-header">
        <h1>Parkhaus Dashboard</h1>
        <p>React Frontend fuer die Parkhaus API</p>
      </header>

      <section className="toolbar">
        <div className="control-group">
          <label htmlFor="fahrzeugtyp">Fahrzeugtyp</label>
          <select
            id="fahrzeugtyp"
            value={fahrzeugtyp}
            onChange={(event) => setFahrzeugtyp(event.target.value)}
            disabled={isBusy}
          >
            <option value="PKW">PKW</option>
            <option value="SUV">SUV</option>
            <option value="Elektro">Elektro</option>
            <option value="Motorrad">Motorrad</option>
          </select>
          <button type="button" onClick={handleEinfahrt} disabled={isBusy || isLoading}>
            Einfahrt
          </button>
        </div>
        <div className="stats">
          <span>Frei: {freiePlaetze}</span>
          <span>Belegt: {belegtePlaetze}</span>
          <span>Gesamt: {plaetze.length}</span>
        </div>
      </section>

      {status && <p className="status">{status}</p>}
      {error && <p className="error">{error}</p>}

      <section className="grid">
        {isLoading ? (
          <p>Lade Parkhausstatus...</p>
        ) : (
          plaetze.map((platz) => (
            <article
              key={platz.platz}
              className={`platz ${platz.belegt ? 'belegt' : 'frei'}`}
            >
              <h2>Platz {platz.platz}</h2>
              <p>{platz.belegt ? platz.fahrzeugtyp : 'frei'}</p>
              <p>{platz.auto_id ?? '-'}</p>
              <button
                type="button"
                onClick={() => handleAusfahrt(platz.platz)}
                disabled={!platz.belegt || isBusy}
              >
                Ausfahrt
              </button>
            </article>
          ))
        )}
      </section>
    </main>
  )
}

export default App
