import React, { useState, useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { Line } from "react-chartjs-2";
import axios from "axios";

import { setFavicon } from "../setFavicon";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

const API_BASE =
  import.meta.env?.VITE_API_BASE ||
  process.env.REACT_APP_API_BASE ||
  "http://localhost:8000";

export default function ViewOccultation() {
  const location = useLocation();
  const navigate = useNavigate();
  const { id } = useParams();

  const [data, setData] = useState(location.state?.data || null);
  const [loading, setLoading] = useState(!location.state?.data);
  const [error, setError] = useState("");

  const [currentGraph, setCurrentGraph] = useState("elevation");

  const token = localStorage.getItem("access_token");
  const headers = { Authorization: `Bearer ${token}` };


  useEffect(() => {
    setFavicon("/icons/space.ico");
  }, []);

  useEffect(() => {
    document.title = 'View Occultation';
  }, []);


  useEffect(() => {
    if (data) return;

    const loadEvent = async () => {
      try {
        const res = await axios.post(
          `${API_BASE}/users/events/${id}`,
          {},
          { headers }
        );

        console.log(res);
        const occult = res.data?.payload?.raw_event;
        if (!occult) {
          setError("No occultation data found in event.");
          return;
        }

        setData(occult);
      } catch (err) {
        console.error(err);
        setError("Failed to load event data");
      } finally {
        setLoading(false);
      }

    };

    loadEvent();
  }, [id]);

  if (loading) return <p style={{ color: "white" }}>Loading occultation...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!data) return <p style={{ color: "white" }}>No data available.</p>;

  // Extract fields
  const { start_utc, end_utc, types, computational_data } = data;

  const sampleTimes = computational_data?.sample_times || [];
  const occultingEl = computational_data?.occulting_elevations || [];
  const occultedEl = computational_data?.occulted_elevations || [];
  const occultingAz = computational_data?.occulting_azimuths || [];
  const occultedAz = computational_data?.occulted_azimuths || [];
  const occultingDist = computational_data?.occulting_dist || [];
  const occultedDist = computational_data?.occulted_dist || [];

  const panelBg = { backgroundColor: "#1a1a1a", color: "white", padding: 12, borderRadius: 8 };
  const orangeBorder = { border: "1px solid orange" };

  const createChartData = (y1, y2, l1, l2) => ({
    labels: sampleTimes.map(t => new Date(t).toLocaleTimeString()),
    datasets: [
      { label: l1, data: y1, borderColor: "orange", backgroundColor: "orange", tension: 0.2 },
      { label: l2, data: y2, borderColor: "lightblue", backgroundColor: "lightblue", tension: 0.2 },
    ],
  });

  const chartOptions = (label) => ({
    responsive: true,
    plugins: { legend: { labels: { color: "white" } } },
    scales: {
      x: { ticks: { color: "white" } },
      y: { ticks: { color: "white" }, title: { display: true, text: label, color: "white" } },
    },
  });

  const events = [];
  if (start_utc) events.push({ label: "Start", time: start_utc });

  if (occultingEl.length && occultedEl.length) {
    let min = Infinity, idx = 0;
    for (let i = 0; i < sampleTimes.length; i++) {
      const diff = Math.abs(occultingEl[i] - occultedEl[i]);
      if (diff < min) { min = diff; idx = i; }
    }
    events.push({ label: "Maximum Overlap", time: sampleTimes[idx] });
  }

  if (end_utc) events.push({ label: "End", time: end_utc });

  return (
    <div style={{ padding: 16, minHeight: "100vh", backgroundColor: "#121212" }}>
      <button className="btn btn-sm btn-outline-warning mb-3" onClick={() => navigate(-1)}>
        ← Back
      </button>

      <h2 style={{ color: "orange", marginBottom: 12 }}>Occultation Details</h2>

      <div style={{ ...panelBg, ...orangeBorder, marginBottom: 16 }}>
        <h4 style={{ color: "orange" }}>{(types || []).join(", ")} Occultation</h4>
        <p>{new Date(start_utc).toLocaleString()} → {new Date(end_utc).toLocaleString()}</p>

        <div style={{ marginBottom: 12 }}>
          {["elevation", "azimuth", "distance"].map((g) => (
            <button
              key={g}
              className={`btn btn-sm me-2 ${currentGraph === g ? "btn-warning" : "btn-outline-warning"}`}
              onClick={() => setCurrentGraph(g)}
            >
              {g.toUpperCase()}
            </button>
          ))}
        </div>

        {currentGraph === "elevation" && (
          <Line
            data={createChartData(occultingEl, occultedEl, "Occulting Elevation", "Occulted Elevation")}
            options={chartOptions("Elevation (deg)")}
          />
        )}

        {currentGraph === "azimuth" && (
          <Line
            data={createChartData(occultingAz, occultedAz, "Occulting Azimuth", "Occulted Azimuth")}
            options={chartOptions("Azimuth (deg)")}
          />
        )}

        {currentGraph === "distance" && (
          <Line
            data={createChartData(occultingDist, occultedDist, "Occulting Distance", "Occulted Distance")}
            options={chartOptions("Distance")}
          />
        )}

        <div style={{ marginTop: 16 }}>
          <h5 style={{ color: "orange" }}>Key Events</h5>
          <ul style={{ color: "lightgray" }}>
            {events.map((ev, i) => (
              <li key={i}><strong>{ev.label}:</strong> {new Date(ev.time).toLocaleString()}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
