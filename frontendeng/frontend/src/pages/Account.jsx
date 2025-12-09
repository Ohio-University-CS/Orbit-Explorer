
// frontendeng/frontend/src/pages/Account.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import TopMenu from "../components/TopMenu";

const API_BASE =
    import.meta.env?.VITE_API_BASE ||
    process.env.REACT_APP_API_BASE ||
    "http://localhost:8000";

export default function Account() {
    const navigate = useNavigate();

    const [events, setEvents] = useState([]);
    const [locations, setLocations] = useState([]);
    const [loadingEvents, setLoadingEvents] = useState(true);
    const [loadingLocations, setLoadingLocations] = useState(true);
    const [errorText, setErrorText] = useState("");

    const token = localStorage.getItem("access_token");
    const user_uuid = localStorage.getItem("user_uuid");

    const headers = { Authorization: `Bearer ${token}` };

    // Fetch saved events
    useEffect(() => {
        const fetchEvents = async () => {
            setLoadingEvents(true);
            setErrorText("");
            try {
                const res = await axios.get(`${API_BASE}/users/saved-events`, { headers });
                setEvents(res.data || []);
            } catch (err) {
                console.error(err);
                setErrorText("Failed to fetch saved events");
            } finally {
                setLoadingEvents(false);
            }
        };
        if (token) fetchEvents();
    }, []);

    // Fetch saved locations
    useEffect(() => {
        const fetchLocations = async () => {
            setLoadingLocations(true);
            setErrorText("");
            try {
                const res = await axios.get(`${API_BASE}/users/locations`, { headers });
                setLocations(res.data || []);
            } catch (err) {
                console.error(err);
                setErrorText("Failed to fetch saved locations");
            } finally {
                setLoadingLocations(false);
            }
        };
        if (token) fetchLocations();
    }, []);

    // Delete a saved event
    const deleteEvent = async (id) => {
        if (!window.confirm("Delete this saved event?")) return;
        try {
            await axios.post(`${API_BASE}/users/event/remove`, { id, user_uuid }, { headers });
            setEvents(events.filter(e => e.id !== id));
        } catch (err) {
            console.error(err);
            setErrorText("Failed to delete event");
        }
    };

    // Delete a saved location
    const deleteLocation = async (id) => {
        if (!window.confirm("Delete this saved location?")) return;
        try {
            await axios.post(`${API_BASE}/users/location/remove`, { id, user_uuid }, { headers });
            setLocations(locations.filter(l => l.id !== id));
        } catch (err) {
            console.error(err);
            setErrorText("Failed to delete location");
        }
    };

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

    const orangeText = { color: "#ff9d2b" };
    const panelBg = { background: "#111", border: "2px solid #ff9d2b", borderRadius: 12, padding: 16 };

    const fmtTime = (t) => t ? new Date(t * 1000).toLocaleString() : "";
    return (
        <div style={starBg}>
            <TopMenu />
            <div className="container" style={{ maxWidth: 1000, marginTop: 24 }}>
                <h1 className="text-center mb-4" style={orangeText}>Account</h1>

                {errorText && <p className="text-danger">{errorText}</p>}

                {/* Saved Events */}
                <div style={panelBg} className="mb-4">
                    <h3 style={orangeText}>Saved Events</h3>
                    {loadingEvents ? (
                        <p className="text-white">Loading events...</p>
                    ) : events.length === 0 ? (
                        <p className="text-white">No saved events</p>
                    ) : (
                        events.map((e, idx) => {
                            const eventType = e.event_type || "Event";
                            const occulter = e.payload?.occulting_naif_id ? `Occulter: ${e.payload.occulting_naif_id}` : "";
                            const occulted = e.payload?.occulted_naif_id ? `Occulted: ${e.payload.occulted_naif_id}` : "";
                            const body = e.payload?.body_naif_id ? `Body: ${e.payload.body_naif_id}` : "";
                            const location = e.loc?.loc_name || "Unknown Location";

                            const description = [eventType, occulter, occulted, body]
                                .filter(Boolean)
                                .join(" | ");

                            return (
                                <div
                                    key={idx}
                                    className="d-flex justify-content-between align-items-center mb-2 p-2 rounded"
                                    style={{ border: "1px solid #ff9d2b", background: "#222", cursor: "pointer" }}
                                    onClick={() => navigate(`/event/${e.id}`, { state: { event: e } })}
                                >
                                    <div className="text-white">
                                        {description}
                                    </div>
                                    <button
                                        className="btn btn-sm btn-outline-danger"
                                        onClick={(ev) => {
                                            ev.stopPropagation();
                                            deleteEvent(e.id);
                                        }}
                                    >
                                        Delete
                                    </button>
                                </div>
                            );
                        })
                    )}
                </div>


                {/* Saved Locations */}
                <div style={panelBg} className="mb-4">
                    <h3 style={orangeText}>Saved Locations</h3>
                    {loadingLocations ? (
                        <p className="text-white">Loading locations...</p>
                    ) : locations.length === 0 ? (
                        <p className="text-white">No saved locations</p>
                    ) : (
                        locations.map((l, idx) => (
                            <div key={idx} className="d-flex justify-content-between align-items-center mb-2 p-2 rounded" style={{ border: "1px solid #ff9d2b", background: "#222" }}>
                                <div className="text-white">
                                    {l.loc_name || "Unnamed"}<br />
                                    Lat: {l.latitude}, Lon: {l.longitude}, Alt: {l.alt_km} km<br />
                                    {l.loc_description}
                                </div>
                                <button className="btn btn-sm btn-outline-danger" onClick={() => deleteLocation(l.id)}>Delete</button>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}