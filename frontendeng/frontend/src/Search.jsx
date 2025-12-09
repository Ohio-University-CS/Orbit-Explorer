// frontendeng/frontend/src/CelestialSearch.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import LocationSelector from "./components/LocationSelector";
import TopMenu from "./components/TopMenu";
import axios from "axios";
import dayjs from "dayjs";
import "bootstrap/dist/css/bootstrap.min.css";

const API_BASE =
  import.meta.env?.VITE_API_BASE ||
  process.env.REACT_APP_API_BASE ||
  "http://localhost:8000";

const BODY_TYPES = ["Planet", "Moon", "Asteroid", "Sun"];
const EVENT_TYPES = [
  { name: "OCCULTATION", label: "Occultation" },
  { name: "BODY_POSITION", label: "Body Position" },
  { name: "PLANET_VISIBILITY", label: "Planet Visibility" },
];

export default function CelestialSearch() {
  const navigate = useNavigate();

  // Time / Location / Event Type
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [selectedEventType, setSelectedEventType] = useState(EVENT_TYPES[0].name);

  // Celestial bodies
  const [planets, setPlanets] = useState([]);
  const [moons, setMoons] = useState([]);
  const [asteroids, setAsteroids] = useState([]);

  // Occultation selection
  const [occultingType, setOccultingType] = useState("");
  const [occultingBody, setOccultingBody] = useState("");
  const [occultedType, setOccultedType] = useState("");
  const [occultedBody, setOccultedBody] = useState("");

  // Body Position selection
  const [bodyPositionType, setBodyPositionType] = useState("");
  const [bodyPositionBody, setBodyPositionBody] = useState("");

  // Planet visibility
  const [selectedPlanets, setSelectedPlanets] = useState([]); // array of naif_id

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorText, setErrorText] = useState("");

  // Styles
  const orangeBorder = { border: "2px solid #ff9d2b" };
  const orangeText = { color: "#ff9d2b" };
  const panelBg = { background: "#111" };

  const getAuthHeaders = () => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Not authorized");
    return { Authorization: `Bearer ${token}` };
  };

  const safeFmt = (t) => {
    if (!t) return "—";
    // Normalize "YYYY-MM-DDTHH:MM" into full ISO if needed
    if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(t)) {
      t = t + ":00";
    }
    const d = new Date(t);
    if (isNaN(d)) return "—";
    return d.toLocaleString();
  };


  useEffect(() => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) navigate("/login");
    } catch {
      navigate("/login");
    }
  }, [navigate]);

  // Load body lists
  useEffect(() => {
    async function loadBodies() {
      try {
        const headers = getAuthHeaders();
        const [planetsRes, moonsRes, asteroidsRes] = await Promise.all([
          axios.post(`${API_BASE}/events/bodies/planets`, {}, { headers }),
          axios.post(`${API_BASE}/events/bodies/moons`, {}, { headers }),
          axios.post(`${API_BASE}/events/bodies/asteroids`, {}, { headers }),
        ]);
        setPlanets(planetsRes.data || []);
        setMoons(moonsRes.data || []);
        setAsteroids(asteroidsRes.data || []);
      } catch (err) {
        console.error("Failed to load celestial bodies", err);
        setErrorText("Failed to load celestial bodies");
      }
    }
    loadBodies();
  }, []);

  useEffect(() => {
    if (planets && planets.length > 0) {
      setSelectedPlanets(planets.map(p => p.naif_id));
    }
  }, [planets]);

  useEffect(() => {
    setResults([]);
    setErrorText("");
  }, [selectedEventType]);

  const applyPreset = (preset) => {
    const today = dayjs();
    let start, end;
    switch (preset) {
      case "today":
        start = today.startOf("day");
        end = today.endOf("day");
        break;
      case "next7":
        start = today;
        end = today.add(7, "day");
        break;
      case "nextWeekend": {
        const dayOfWeek = today.day();
        const fri = today.add((5 - dayOfWeek + 7) % 7, "day").startOf("day");
        const sun = fri.add(2, "day").endOf("day");
        start = fri;
        end = sun;
        break;
      }
      case "thisMonth":
        start = today.startOf("month");
        end = today.endOf("month");
        break;
      case "thisYear":
        start = today.startOf("year");
        end = today.endOf("year");
        break;
      default:
        return;
    }
    setStartTime(start.format("YYYY-MM-DDTHH:mm"));
    setEndTime(end.format("YYYY-MM-DDTHH:mm"));
  };

  const getBodiesByType = (type) => {
    switch (type) {
      case "Planet":
        return planets;
      case "Moon":
        return moons;
      case "Asteroid":
        return asteroids;
      case "Sun":
        return [{ name: "Sun", naif_id: 10 }];
      default:
        return [];
    }
  };

  const togglePlanetSelection = (naif_id) => {
    setSelectedPlanets(prev => {
      if (prev.includes(naif_id)) return prev.filter(x => x !== naif_id);
      return [...prev, naif_id];
    });
  };

  const searchEvent = async (endpoint, payload, headers) => {// Send empty body {} but include headers properly
    const res = await axios.post(`${API_BASE}${endpoint}`, payload, { headers });
    let normalized = [];

    if (selectedEventType === "OCCULTATION") {
      normalized = res.data.occultations || [];
    } else if (selectedEventType === "BODY_POSITION") {
      if (Array.isArray(res.data)) normalized = res.data;
      else if (res.data?.ra_rad !== undefined) normalized = [res.data];
      else if (res.data?.positions) normalized = res.data.positions;
    } else if (selectedEventType === "PLANET_VISIBILITY") {
      normalized = res.data || [];
    }

    console.log("norm:")
    console.log(normalized)
    setResults(normalized);
  };

  const onSearch = async (e) => {
    e?.preventDefault();
    setErrorText("");
    setResults([]);
    setLoading(true);

    try {
      const token = localStorage.getItem("access_token");
      if (!token) throw new Error("Not authorized");

      if (
        !selectedLocation ||
        !isFinite(parseFloat(selectedLocation.lat)) ||
        !isFinite(parseFloat(selectedLocation.lon))
      ) {
        throw new Error("Please select a valid location before searching");
      }

      const locationPayload = {
        lat: parseFloat(selectedLocation.lat),
        lon: parseFloat(selectedLocation.lon),
        alt_km: parseFloat(selectedLocation.alt_km ?? 0),
      };
      const headers = { Authorization: `Bearer ${token}` };

      if (selectedEventType === "OCCULTATION") {
        if (!occultingBody || !occultedBody)
          throw new Error("Select occulting and occulted bodies");
        const payload = {
          location: locationPayload,
          start_time: new Date(startTime).toISOString(),
          end_time: new Date(endTime).toISOString(),
          occulting_naif_id: occultingBody,
          occulted_naif_id: occultedBody
        };
        await searchEvent("/events/search/occultations", payload, headers);

      } else if (selectedEventType === "BODY_POSITION") {
        if (!bodyPositionBody) throw new Error("Select a body");
        const payload = {
          location: locationPayload,
          dt: new Date(startTime).toISOString(),
          body_naif_id: bodyPositionBody
        };
        await searchEvent("/events/observe", payload, headers);

      } else if (selectedEventType === "PLANET_VISIBILITY") {
        const planetsToSend = selectedPlanets.length ? selectedPlanets : planets.map(p => p.naif_id);
        const payload = {
          location: locationPayload,
          start_time: new Date(startTime).toISOString(),
          end_time: new Date(endTime).toISOString(),
          body_naif_id: planetsToSend
        };
        await searchEvent("/events/visibility/planets", payload, headers);

      } else {
        throw new Error("Unsupported event type");
      }

    } catch (err) {
      console.error(err);
      setErrorText(err.message || "Search failed");
    } finally {
      setLoading(false);
    }
  };

  const saveEvent = async (event) => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) throw new Error("Not authorized");

      const headers = { Authorization: `Bearer ${token}` };

      // Flexible payload for any event type
      const savePayload = {
        event_type: selectedEventType,
        payload: {
          location: selectedLocation,
          start_time: event.start_time || startTime,
          end_time: event.end_time || endTime,
          occulting_naif_id: event.occulting_naif_id,
          occulted_naif_id: event.occulted_naif_id,
          body_naif_id: event.body_naif_id || event.naif_id,
          raw_event: event // store full event for reference
        }
      };

      const res = await axios.post(`${API_BASE}/users/event/save`, savePayload, { headers });
      const savedId = res.data?.id;
      console.log(res);
      alert(`Event saved! Access it at /event/${savedId}`);

    } catch (err) {
      console.error("Failed to save event", err);
      alert(`Failed to save event: ${err.message || err}`);
    }
  };

  const fmt = (s) => s ? new Date(s).toLocaleString() : "";

  const starBg = {
    background:
      `radial-gradient(2px 2px at 20% 30%, #fff 30%, transparent 31%),
       radial-gradient(1px 1px at 70% 80%, #fff 30%, transparent 31%),
       radial-gradient(1.2px 1.2px at 40% 60%, #fff 30%, transparent 31%),
       radial-gradient(0.8px 0.8px at 80% 20%, #fff 30%, transparent 31%),
       radial-gradient(0.6px 0.6px at 15% 80%, #fff 30%, transparent 31%),
       radial-gradient(0.9px 0.9px at 55% 40%, #fff 30%, transparent 31%),
       linear-gradient(#000, #03030a)`,
    minHeight: "100vh",
    padding: "24px 12px",
  };

  return (
    <div style={starBg}>
      <TopMenu />
      <div className="container">
        <div className="mx-auto" style={{ maxWidth: 1120 }}>
          <div style={{ ...orangeBorder, borderRadius: 16, padding: 18, background: "#050505" }}>
            <h1 className="text-center mb-3" style={orangeText}>Celestial Search</h1>

            {/* Event Type */}
            <div className="mb-3 p-3 rounded" style={{ ...orangeBorder, ...panelBg }}>
              <h5 style={orangeText}>Event Type</h5>
              <select
                className="form-select"
                value={selectedEventType}
                onChange={e => setSelectedEventType(e.target.value)}
              >
                {EVENT_TYPES.map(et => <option key={et.name} value={et.name}>{et.label}</option>)}
              </select>
            </div>

            {/* Time Range */}
            <div className="mb-3 p-3 rounded" style={{ ...orangeBorder, ...panelBg }}>
              <h5 style={orangeText}>Time Range</h5>
              <div className="mb-2 d-flex flex-wrap gap-2">
                <button className="btn btn-outline-light btn-sm me-2 mb-2" onClick={() => applyPreset("today")}>Today</button>
                <button className="btn btn-outline-light btn-sm me-2 mb-2" onClick={() => applyPreset("next7")}>Next 7 Days</button>
                <button className="btn btn-outline-light btn-sm me-2 mb-2" onClick={() => applyPreset("nextWeekend")}>Next Weekend</button>
                <button className="btn btn-outline-light btn-sm me-2 mb-2" onClick={() => applyPreset("thisMonth")}>This Month</button>
                <button className="btn btn-outline-light btn-sm me-2 mb-2" onClick={() => applyPreset("thisYear")}>This Year</button>
              </div>

              <div className="row g-2">
                <div className="col-sm-6">
                  <label className="form-label text-light">Start</label>
                  <input className="form-control" type="datetime-local" value={startTime} onChange={e => setStartTime(e.target.value)} />
                </div>
                <div className="col-sm-6">
                  <label className="form-label text-light">End</label>
                  <input className="form-control" type="datetime-local" value={endTime} onChange={e => setEndTime(e.target.value)} />
                </div>
              </div>
            </div>

            {/* Location */}
            <div className="mb-3 p-3 rounded" style={{ ...orangeBorder, ...panelBg }}>
              <h5 style={orangeText}>Location</h5>
              <LocationSelector value={selectedLocation} onChange={setSelectedLocation} />
              <small className="text-light">Search will use the values currently in the location input boxes.</small>
            </div>

            {/* OCCULTATION specific */}
            {selectedEventType === "OCCULTATION" && (
              <div className="mb-3 p-3 rounded" style={{ ...orangeBorder, ...panelBg }}>
                <h5 style={orangeText}>Occultation Bodies</h5>
                <div className="row">
                  <div className="col-md-6 mb-2">
                    <div style={{ ...orangeBorder, padding: 10, borderRadius: 8, background: "#111" }}>
                      <h6 style={orangeText}>Occulting</h6>
                      <label className="form-label small text-light ">Type</label>
                      <select className="form-select mb-2" value={occultingType} onChange={e => { setOccultingType(e.target.value); setOccultingBody(""); }}>
                        <option value="">Select Type</option>
                        {BODY_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
                      </select>
                      <label className="form-label small text-light">Body</label>
                      <select className="form-select" value={occultingBody} onChange={e => setOccultingBody(e.target.value)}>
                        <option value="">Select Body</option>
                        {getBodiesByType(occultingType).map(b => <option key={b.naif_id} value={b.naif_id}>{b.name}</option>)}
                      </select>
                    </div>
                  </div>

                  <div className="col-md-6 mb-2">
                    <div style={{ ...orangeBorder, padding: 10, borderRadius: 8, background: "#111" }}>
                      <h6 style={orangeText}>Occulted</h6>
                      <label className="form-label small text-light">Type</label>
                      <select className="form-select mb-2" value={occultedType} onChange={e => { setOccultedType(e.target.value); setOccultedBody(""); }}>
                        <option value="">Select Type</option>
                        {BODY_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
                      </select>
                      <label className="form-label small text-light">Body</label>
                      <select className="form-select" value={occultedBody} onChange={e => setOccultedBody(e.target.value)}>
                        <option value="">Select Body</option>
                        {getBodiesByType(occultedType).map(b => <option key={b.naif_id} value={b.naif_id}>{b.name}</option>)}
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* BODY_POSITION specific */}
            {selectedEventType === "BODY_POSITION" && (
              <div className="mb-3 p-3 rounded" style={{ ...orangeBorder, ...panelBg }}>
                <h5 style={orangeText}>Select Body</h5>
                <div style={{ ...orangeBorder, padding: 10, borderRadius: 8, background: "#111" }}>
                  <label className="form-label small text-light">Type</label>
                  <select className="form-select mb-2" value={bodyPositionType} onChange={e => { setBodyPositionType(e.target.value); setBodyPositionBody(""); }}>
                    <option value="">Select Type</option>
                    {BODY_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
                  </select>

                  <label className="form-label small text-light">Body</label>
                  <select className="form-select" value={bodyPositionBody} onChange={e => setBodyPositionBody(e.target.value)}>
                    <option value="">Select Body</option>
                    {getBodiesByType(bodyPositionType).map(b => <option key={b.naif_id} value={b.naif_id}>{b.name}</option>)}
                  </select>
                </div>
              </div>
            )}

            {/* PLANET_VISIBILITY specific */}
            {selectedEventType === "PLANET_VISIBILITY" && (
              <div className="mb-3 p-3 rounded" style={{ ...orangeBorder, ...panelBg }}>
                <h5 style={orangeText}>Planet Visibility</h5>
                <div style={{ ...orangeBorder, padding: 10, borderRadius: 8, background: "#111" }}>
                  <p className="mb-2 text-white small">Select planets to include (default = all):</p>
                  <div className="d-flex flex-wrap">
                    {planets.map(p => (
                      <div key={p.naif_id} className="form-check me-3 mb-2">
                        <input
                          className="form-check-input"
                          type="checkbox"
                          id={`planet-${p.naif_id}`}
                          checked={selectedPlanets.includes(p.naif_id)}
                          onChange={() => togglePlanetSelection(p.naif_id)}
                        />
                        <label className="form-check-label text-white" htmlFor={`planet-${p.naif_id}`}>
                          {p.name}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
            <div className="d-grid mb-3">
              <button className="btn btn-primary" onClick={onSearch} disabled={loading}>
                {loading ? "Searching..." : "Search"}
              </button>
            </div>
            <div>
              {results.length === 0 && !loading && (
                <p className="text-light">No results yet.</p>
              )}

              {results.map((ev, idx) => {
                let description = "";
                let linkText = "View Observation";
                let linkState = { data: ev };
                let route = "/observe-object";

                if (selectedEventType === "OCCULTATION") {
                  description = `${ev.occulted_name} occulted by ${ev.occulting_name}`;
                  linkState = { body: ev.occulted_name, data: ev };
                  route = "/view-occultation";

                } else if (selectedEventType === "BODY_POSITION") {
                  description = `Body position`;
                  linkState = { body: ev.body_name || "Body", data: ev };
                  route = "/observe-object";

                } else if (selectedEventType === "PLANET_VISIBILITY") {
                  description = `${ev.planet || "Planet"} visiblility`;
                  linkText = "View Visibility";
                  route = "/view-visibility";
                }

                return (
                  <div
                    key={idx}
                    className="mb-2 p-2 rounded"
                    style={{
                      ...panelBg,
                      ...orangeBorder,
                      paddingLeft: "20px"
                    }}
                  >
                    <button
                      className="btn btn-link text-warning p-0 mb-1"
                      onClick={() => navigate(route, { state: linkState })}
                    >
                      {description} {linkText}
                    </button>

                    <button
                      className="btn btn-sm btn-outline-success ms-2"
                      onClick={() => saveEvent(ev)}
                    >
                      Save Event
                    </button>
                  </div>
                );
              })}
            </div>

            {errorText && <p className="text-danger">{errorText}</p>}
          </div>
        </div>
      </div>
    </div>
  );
}