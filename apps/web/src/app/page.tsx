// src/app/page.tsx
"use client";
import { useState } from "react";
import { DateTime } from "luxon";

export default function Home() {
  const [lat, setLat] = useState("40.0");
  const [lon, setLon] = useState("-83.0");
  const [date, setDate] = useState(DateTime.now().toISODate()!);
  const [kind, setKind] = useState("lunar_phase");
  const [result, setResult] = useState<any>(null);

  const fetchData = async () => {
    const url = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001"}/events/${kind}?lat=${lat}&lon=${lon}&date=${date}`;
    const res = await fetch(url);
    setResult(await res.json());
  };

  return (
    <main style={{minHeight:"100vh", padding:"24px", color:"#fff", background:"radial-gradient(ellipse at top, #141b2d, #0b0f1a)"}}>
      <h1 style={{fontFamily:"monospace"}}>Orbit Explorer</h1>
      <div style={{display:"grid", gap:8, maxWidth:420}}>
        <input placeholder="latitude" value={lat} onChange={e=>setLat(e.target.value)} />
        <input placeholder="longitude" value={lon} onChange={e=>setLon(e.target.value)} />
        <input type="date" value={date} onChange={e=>setDate(e.target.value)} />
        <select value={kind} onChange={e=>setKind(e.target.value)}>
          <option value="lunar_phase">lunar_phase</option>
          <option value="next_eclipse">next_eclipse</option>
        </select>
        <button onClick={fetchData}>Compute</button>
      </div>
      <pre style={{marginTop:16, background:"#101521", padding:12, borderRadius:8}}>{result ? JSON.stringify(result, null, 2) : "Results will appear here…"}</pre>
    </main>
  );
}
