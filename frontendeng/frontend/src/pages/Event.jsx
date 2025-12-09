// frontendeng/frontend/src/pages/Event.jsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const API_BASE =
    import.meta.env?.VITE_API_BASE ||
    process.env.REACT_APP_API_BASE ||
    "http://localhost:8000";

export default function Event() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [errorText, setErrorText] = useState("");

    const token = localStorage.getItem("access_token");
    const headers = { Authorization: `Bearer ${token}` };

    const redirectMap = {
        OCCULTATION: `/view-occultation/${id}`,
        PLANET_VISIBILITY: `/view-visibility/${id}`,
        BODY_POSITION: `/observe-object/${id}`,
    };

    useEffect(() => {
        const fetchEvent = async () => {
            setLoading(true);
            setErrorText("");

            try {
                const res = await axios.post(
                    `${API_BASE}/users/events/${id}`,
                    {},
                    { headers }
                );

                const evt = res.data;
                const type = evt?.event_type;

                if (type && redirectMap[type]) {
                    navigate(redirectMap[type], { replace: true });
                    return;
                }

                setErrorText("Unknown event type.");
            } catch (err) {
                console.error("Event load failed:", err);
                setErrorText("Failed to fetch event.");
            } finally {
                setLoading(false);
            }

        };

        if (token) fetchEvent();
    }, [id]);

    if (loading) return <p className="text-white">Loading event...</p>;
    if (errorText) return <p className="text-danger">{errorText}</p>;

    return (
        <div style={{ background: "#000", minHeight: "100vh", padding: 24 }}>
            <div className="container text-white" style={{ maxWidth: 800 }}>
                <h2>Error</h2>
                <p>{errorText}</p>
            </div>
        </div>
    );
}
