import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API_BASE =
  (typeof import.meta !== "undefined" &&
    import.meta.env &&
    import.meta.env.VITE_API_BASE) ||
  process.env.REACT_APP_API_BASE ||
  "http://localhost:8000";

// FULL-WIDTH PAGE, BLACK BACKGROUND
const pageStyle = {
  minHeight: "100vh",
  background: "#000",
  color: "#fff",
  display: "flex",
  justifyContent: "center",
  alignItems: "flex-start",
  padding: "40px 16px",
  fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
};

const shellStyle = {
  width: "100%",
  maxWidth: "1120px",
  background: "#050505",
  borderRadius: "24px",
  padding: "28px 24px 32px",
  boxShadow: "0 0 40px rgba(0,0,0,0.85)",
  border: "1px solid #ff9d2b",
};

const sectionStyle = {
  marginTop: "20px",
  padding: "18px 18px 20px",
  borderRadius: "16px",
  background: "#0c0c0c",
  border: "1px solid #ff9d2b4d",
};

const labelStyle = {
  display: "block",
  fontSize: "13px",
  marginBottom: "4px",
  color: "#ffffff",
};

const hintText = {
  fontSize: "12px",
  color: "#f7f7f7",
};

const inputStyle = {
  width: "100%",
  padding: "10px 12px",
  borderRadius: "10px",
  border: "1px solid #ffb13d",
  background: "#050505",
  color: "#ffffff",
  fontSize: "14px",
  outline: "none",
};

const chipRowStyle = {
  display: "flex",
  flexWrap: "wrap",
  gap: "8px",
  marginTop: "8px",
};

const chipStyle = (active) => ({
  padding: "6px 10px",
  borderRadius: "999px",
  border: active ? "1px solid #ffb13d" : "1px solid #ffb13d80",
  background: active ? "#ff9d2b" : "#111",
  color: active ? "#000" : "#ffffff",
  fontSize: "12px",
  cursor: "pointer",
});

const primaryButtonStyle = {
  marginTop: "18px",
  width: "100%",
  padding: "16px 0",
  borderRadius: "999px",
  border: "none",
  background: "#ff9d2b",
  color: "#000",
  fontWeight: 700,
  letterSpacing: "0.08em",
  textTransform: "uppercase",
  fontSize: "14px",
  cursor: "pointer",
  boxShadow: "0 10px 20px rgba(0,0,0,0.9)",
};

const resultCardStyle = {
  marginTop: "10px",
  padding: "10px 12px",
  borderRadius: "12px",
  background: "#050505",
  border: "1px solid #ffb13d80",
  fontSize: "13px",
};

const viewButtonStyle = {
  marginTop: "8px",
  padding: "6px 12px",
  borderRadius: "999px",
  border: "none",
  background: "#ffffff",
  color: "#000",
  fontSize: "12px",
  fontWeight: 600,
  cursor: "pointer",
};

export default function OccultationSearch() {
  const navigate = useNavigate();

  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [elevation, setElevation] = useState("");

  const [availableTypes, setAvailableTypes] = useState([]);
  const [selectedTypes, setSelectedTypes] = useState(["OCCULTATION"]);

  const [criteria, setCriteria] = useState([
    { name: "occultation_filter", description: "" },
  ]);

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorText, setErrorText] = useState("");

  // Load values saved on the Cosmic page
  useEffect(() => {
    try {
      const savedStart = window.localStorage.getItem("oe_startTimeLocal");
      const savedLat = window.localStorage.getItem("oe_latitude");
      const savedLon = window.localStorage.getItem("oe_longitude");

      if (savedStart) setStartTime(savedStart);
      if (savedLat) setLat(savedLat);
      if (savedLon) setLon(savedLon);
    } catch (e) {
      console.warn("localStorage not available", e);
    }
  }, []);

  // Load event types from backend
  useEffect(() => {
    async function loadTypes() {
      try {
        const res = await fetch(`${API_BASE}/events/types`);
        if (!res.ok) {
          throw new Error("Failed to load event types");
        }
        const data = await res.json();
        const names = data.map((t) => t.event_name || t.name || t.id);
        setAvailableTypes(names);
      } catch (err) {
        console.error(err);
        setAvailableTypes([]);
      }
    }

    loadTypes();
  }, []);

  const toggleType = (name) => {
    setSelectedTypes((prev) =>
      prev.includes(name) ? prev.filter((t) => t !== name) : [...prev, name]
    );
  };

  const updateCriterion = (index, field, value) => {
    setCriteria((prev) =>
      prev.map((c, i) => (i === index ? { ...c, [field]: value } : c))
    );
  };

  const addCriterion = () => {
    setCriteria((prev) => [...prev, { name: "", description: "" }]);
  };

  const onSearch = async (e) => {
    e.preventDefault();
    setErrorText("");
    setLoading(true);
    setResults([]);

    try {
      if (!startTime || !endTime) {
        throw new Error("Start and end time are required.");
      }
      if (!lat || !lon) {
        throw new Error("Latitude and longitude are required.");
      }

      const startEpoch = Math.floor(new Date(startTime).getTime() / 1000);
      const endEpoch = Math.floor(new Date(endTime).getTime() / 1000);

      const payload = {
        start_time: startEpoch,
        end_time: endEpoch,
        loc: {
          lat: parseFloat(lat),
          lon: parseFloat(lon),
          elevation: elevation ? parseFloat(elevation) : 0,
        },
        whitelisted_event_types: selectedTypes,
        event_specific_criteria: criteria
          .filter((c) => c.name.trim() || c.description.trim())
          .map((c) => ({
            name: c.name.trim(),
            description: c.description.trim(),
          })),
      };

      const res = await fetch(`${API_BASE}/events/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `HTTP error ${res.status}`);
      }

      const data = await res.json();
      setResults(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setErrorText("Search failed. Please check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const openVisualization = (event) => {
    navigate("/visualize", { state: { event } });
  };

  return (
    <div style={pageStyle}>
      <div style={shellStyle}>
        <h1 style={{ fontSize: "28px", marginBottom: "4px", color: "#ffffff" }}>
          Occultation Search
        </h1>
        <p style={{ fontSize: "13px", color: "#f7f7f7", marginBottom: "8px" }}>
          Choose a time window, observer location, and event types, then search.
        </p>

        {/* 1. Time window */}
        <section style={sectionStyle}>
          <div
            style={{
              fontSize: "13px",
              opacity: 0.9,
              marginBottom: "6px",
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              color: "#ff9d2b",
            }}
          >
            1 · Time Window (Local / EST)
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "12px",
            }}
          >
            <div>
              <label style={labelStyle}>Start time</label>
              <input
                type="datetime-local"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                style={inputStyle}
              />
            </div>
            <div>
              <label style={labelStyle}>End time</label>
              <input
                type="datetime-local"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                style={inputStyle}
              />
            </div>
          </div>
        </section>

        {/* 2. Observer location */}
        <section style={sectionStyle}>
          <div
            style={{
              fontSize: "13px",
              opacity: 0.9,
              marginBottom: "6px",
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              color: "#ff9d2b",
            }}
          >
            2 · Observer Location
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
              gap: "12px",
            }}
          >
            <div>
              <label style={labelStyle}>Latitude (°)</label>
              <input
                type="text"
                value={lat}
                onChange={(e) => setLat(e.target.value)}
                style={inputStyle}
                placeholder="e.g. 40.0000"
              />
            </div>
            <div>
              <label style={labelStyle}>Longitude (°)</label>
              <input
                type="text"
                value={lon}
                onChange={(e) => setLon(e.target.value)}
                style={inputStyle}
                placeholder="e.g. -80.0000"
              />
            </div>
            <div>
              <label style={labelStyle}>Elevation (m)</label>
              <input
                type="number"
                value={elevation}
                onChange={(e) => setElevation(e.target.value)}
                style={inputStyle}
                placeholder="e.g. 100"
              />
            </div>
          </div>
        </section>

        {/* 3. Event types */}
        <section style={sectionStyle}>
          <div
            style={{
              fontSize: "13px",
              opacity: 0.9,
              marginBottom: "6px",
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              color: "#ff9d2b",
            }}
          >
            3 · Event Types
          </div>
          <p style={hintText}>
            These names come directly from the{" "}
            <code style={{ color: "#ffffff" }}>celestial_event_types</code>{" "}
            table.
          </p>

          <div style={chipRowStyle}>
            {availableTypes.length === 0 && (
              <span style={{ fontSize: "12px", color: "#ff8080" }}>
                Could not load event types.
              </span>
            )}
            {availableTypes.map((name) => (
              <button
                key={name}
                type="button"
                style={chipStyle(selectedTypes.includes(name))}
                onClick={() => toggleType(name)}
              >
                {name}
              </button>
            ))}
          </div>
        </section>

        {/* 4. Optional criteria */}
        <section style={sectionStyle}>
          <div
            style={{
              fontSize: "13px",
              opacity: 0.9,
              marginBottom: "6px",
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              color: "#ff9d2b",
            }}
          >
            4 · Optional Criteria
          </div>

          {criteria.map((c, idx) => (
            <div key={idx} style={{ marginTop: idx === 0 ? 0 : 10 }}>
              <label style={labelStyle}>Criteria name</label>
              <input
                type="text"
                value={c.name}
                onChange={(e) =>
                  updateCriterion(idx, "name", e.target.value)
                }
                style={inputStyle}
                placeholder="e.g. occultation_depth"
              />
              <label style={{ ...labelStyle, marginTop: 8 }}>Description</label>
              <textarea
                value={c.description}
                onChange={(e) =>
                  updateCriterion(idx, "description", e.target.value)
                }
                style={{
                  ...inputStyle,
                  resize: "vertical",
                  minHeight: "70px",
                }}
                placeholder="Describe how the backend should interpret this."
              />
            </div>
          ))}

          <button
            type="button"
            onClick={addCriterion}
            style={{
              marginTop: "10px",
              padding: "6px 12px",
              borderRadius: "999px",
              border: "1px solid #ffb13d",
              background: "#111",
              color: "#ffffff",
              fontSize: "12px",
              cursor: "pointer",
            }}
          >
            + Add criterion
          </button>

          {errorText && (
            <p style={{ marginTop: 10, fontSize: 12, color: "#ff8080" }}>
              {errorText}
            </p>
          )}
        </section>

        {/* Search button */}
        <button
          type="button"
          onClick={onSearch}
          style={primaryButtonStyle}
          disabled={loading}
        >
          {loading ? "Searching..." : "Search Occultations"}
        </button>

        {/* 5. Results */}
        <section style={sectionStyle}>
          <div
            style={{
              fontSize: "13px",
              opacity: 0.9,
              marginBottom: "6px",
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              color: "#ff9d2b",
            }}
          >
            5 · Results
          </div>

          {results.length === 0 && !loading && (
            <p style={hintText}>No events returned yet.</p>
          )}

          {results.map((ev) => (
            <div key={ev.id} style={resultCardStyle}>
              <div style={{ fontWeight: 600, marginBottom: 2, color: "#fff" }}>
                {ev.name || ev.type || ev.id}
              </div>
              <div
                style={{
                  fontSize: 12,
                  color: "#f7f7f7",
                  marginBottom: 2,
                }}
              >
                Type: {ev.type}
              </div>
              <div style={{ fontSize: 12, color: "#d8d8d8" }}>
                Time: {ev.time ? new Date(ev.time).toString() : "—"}
              </div>
              {ev.desc && (
                <div
                  style={{
                    fontSize: 12,
                    color: "#ffffff",
                    marginTop: 2,
                  }}
                >
                  {ev.desc}
                </div>
              )}

              <button
                type="button"
                style={viewButtonStyle}
                onClick={() => openVisualization(ev)}
              >
                View 3D Visualization
              </button>
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}










