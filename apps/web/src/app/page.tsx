'use client'
import { useEffect, useMemo, useRef, useState } from 'react'
import dynamic from 'next/dynamic'

// lazy-load the heavy scene on client only
const SolarSystem = dynamic(() => import('@/components/SolarSystem'), { ssr: false })

type Frame = 'heliocentric' | 'earth-centered' | 'observer' // observer = lat/lon/alt
type Body = 'sun' | 'mercury' | 'venus' | 'earth' | 'moon' | 'mars' | 'jupiter' | 'saturn' | 'uranus' | 'neptune'

export default function Page() {
  const [frame, setFrame] = useState<Frame>('observer')
  const [lat, setLat] = useState('40.0')
  const [lon, setLon] = useState('-83.0')
  const [alt, setAlt] = useState('0') // meters
  const [dateISO, setDateISO] = useState<string>(new Date().toISOString().slice(0,16)) // yyyy-mm-ddThh:mm
  const [speed, setSpeed] = useState(600) // seconds per sim second
  const [positions, setPositions] = useState<any|null>(null)
  const [loading, setLoading] = useState(false)

  async function fetchPositions() {
    setLoading(true)
    const url = new URL(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/positions`)
    url.searchParams.set('date', new Date(dateISO).toISOString())
    url.searchParams.set('frame', frame)
    if (frame === 'observer') {
      url.searchParams.set('lat', lat)
      url.searchParams.set('lon', lon)
      url.searchParams.set('alt', alt)
    }
    const res = await fetch(url.toString())
    const data = await res.json()
    setPositions(data)
    setLoading(false)
  }

  useEffect(() => { fetchPositions() }, []) // first load

  return (
    <div style={{display:'grid', gridTemplateColumns:'320px 1fr', height:'100vh', background:'#0b0f1a', color:'#e6f0ff'}}>
      {/* LEFT PANEL */}
      <aside style={{padding:'16px 14px', borderRight:'1px solid #1b2236'}}>
        <h2 style={{marginBottom:10, fontFamily:'monospace'}}>Orbit-Explorer</h2>

        <label>Reference frame</label>
        <select value={frame} onChange={e=>setFrame(e.target.value as Frame)} style={{width:'100%', margin:'6px 0 12px'}}>
          <option value="observer">Observer (lat/lon)</option>
          <option value="earth-centered">Earth-centered inertial</option>
          <option value="heliocentric">Heliocentric</option>
        </select>

        {frame==='observer' && (
          <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:8, marginBottom:10}}>
            <input placeholder="lat" value={lat} onChange={e=>setLat(e.target.value)} />
            <input placeholder="lon" value={lon} onChange={e=>setLon(e.target.value)} />
            <input placeholder="alt (m)" value={alt} onChange={e=>setAlt(e.target.value)} />
          </div>
        )}

        <label>Date/Time (UTC)</label>
        <input type="datetime-local" value={dateISO} onChange={e=>setDateISO(e.target.value)} style={{width:'100%', margin:'6px 0 12px'}}/>

        <label>Sim speed (sec / tick)</label>
        <input type="range" min={0} max={3600} value={speed} onChange={e=>setSpeed(Number(e.target.value))} />
        <div style={{fontSize:12, opacity:.8}}>{speed}s per sim second</div>

        <button onClick={fetchPositions} disabled={loading} style={{marginTop:12, width:'100%'}}>
          {loading ? 'Computing…' : 'Update scene'}
        </button>

        <hr style={{margin:'14px 0', borderColor:'#1b2236'}}/>

        <a href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'}/events/upcoming`} target="_blank">Upcoming events (JSON)</a>
        <p style={{fontSize:12, opacity:.8}}>Conjunctions • Oppositions • Lunar phases • Eclipse windows</p>
      </aside>

      {/* RIGHT: FULLSCREEN SCENE */}
      <div style={{position:'relative'}}>
        <SolarSystem initial={positions} frame={frame} speed={speed} />
        {!positions && (<div style={{position:'absolute', top:12, left:12, fontSize:12, opacity:.8}}>Loading ephemeris…</div>)}
      </div>
    </div>
  )
}

