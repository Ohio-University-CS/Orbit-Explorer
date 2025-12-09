import React, { useState, useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const API_BASE =
  import.meta.env?.VITE_API_BASE ||
  process.env.REACT_APP_API_BASE ||
  "http://localhost:8000";

export default function ObserveObject() {
  const location = useLocation();
  const navigate = useNavigate();
  const { id } = useParams();

  const initialBody = location.state?.body || null;
  const initialData = location.state?.data || null;

  const [body, setBody] = useState(initialBody);
  const [data, setData] = useState(initialData);

  const [loading, setLoading] = useState(!initialData);
  const [error, setError] = useState("");

  const token = localStorage.getItem("access_token");
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    if (data) return;
    if (!id) return;

    const loadEvent = async () => {
    try {
        const res = await axios.post(
        `${API_BASE}/users/events/${id}`,
        {},
        { headers }
        );

        console.log(res);
        const payload = res.data?.payload;
        if (!payload) {
        setError("No payload found in event.");
        return;
        }

        const raw = payload.raw_event;
        if (!raw) {
        setError("No raw_event found in payload.");
        return;
        }

        // BODY_POSITION format → raw_event IS the data
        setBody("Body Position"); // or something custom
        setData(raw);

    } catch (err) {
        console.error(err);
        setError("Failed to load event data");
    } finally {
        setLoading(false);
    }
    };

    loadEvent();
  }, [id]);

  // ----------------------------------------
  // UI STATES (matching occultation theme)
  // ----------------------------------------

  if (loading) {
    return (
      <div style={{ padding: 16, minHeight: "100vh", backgroundColor: "#121212", color: "white" }}>
        Loading observation...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: 16, minHeight: "100vh", backgroundColor: "#121212", color: "white" }}>
        <h3 style={{ color: "red" }}>{error}</h3>
        <button className="btn btn-outline-warning mt-2" onClick={() => navigate(-1)}>
          ← Back
        </button>
      </div>
    );
  }

  if (!body || !data) {
    return (
      <div style={{ padding: 16, minHeight: "100vh", backgroundColor: "#121212", color: "white" }}>
        <h3>No observation data available</h3>
        <button className="btn btn-outline-warning mt-2" onClick={() => navigate(-1)}>
          ← Back
        </button>
      </div>
    );
  }

  // ----------------------------------------
  // MAIN VIEW
  // ----------------------------------------

  return (
    <div style={{ padding: 16, minHeight: "100vh", backgroundColor: "#121212" }}>
      <button className="btn btn-sm btn-outline-warning mb-3" onClick={() => navigate(-1)}>
        ← Back
      </button>

      <h2 style={{ color: "orange", marginBottom: 12 }}>{body} Observation</h2>

      <div
        style={{
          backgroundColor: "#1a1a1a",
          color: "white",
          padding: 16,
          borderRadius: 8,
          border: "1px solid orange",
        }}
      >
        <table className="table table-dark table-striped mb-4">
          <thead>
            <tr>
              <th>RA (°)</th>
              <th>Dec (°)</th>
              <th>Alt (°)</th>
              <th>Az (°)</th>
              <th>Distance (km)</th>
              <th>Visible</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{data.ra_deg?.toFixed(2)}</td>
              <td>{data.dec_deg?.toFixed(2)}</td>
              <td>{data.alt_deg?.toFixed(2)}</td>
              <td>{data.az_deg?.toFixed(2)}</td>
              <td>{data.distance_km?.toLocaleString()}</td>
              <td>{data.visible ? "Yes" : "No"}</td>
            </tr>
          </tbody>
        </table>

        <div style={{ color: "lightgray" }}>
          <h5 style={{ color: "orange" }}>Key Notes</h5>
          <ul>
            <li>Altitude above horizon: {data.alt_deg?.toFixed(2)}°</li>
            <li>Azimuth direction: {data.az_deg?.toFixed(2)}°</li>
            <li>Distance from observer: {data.distance_km?.toLocaleString()} km</li>
            <li>
              Object is currently {data.visible ? "visible" : "not visible"} from the observer's
              location.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
