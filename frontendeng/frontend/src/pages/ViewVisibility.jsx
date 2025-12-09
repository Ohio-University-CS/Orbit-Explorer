import React, { useState, useMemo, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";
import "bootstrap/dist/css/bootstrap.min.css";

import { setFavicon } from "../setFavicon";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

export default function ViewVisibility() {
  const location = useLocation();
  const navigate = useNavigate();

  const stateData = location.state?.data;
  const planet = stateData?.planet;
  const measurements = stateData?.data || [];

  
    useEffect(() => {
      setFavicon("/icons/space.ico");
    }, []);
  
    useEffect(() => {
      document.title = 'View Visibility';
    }, []);
  

  // ---------------- Hooks at the top ----------------
  const [currentGraph, setCurrentGraph] = useState("magnitude");

  const times = useMemo(() => measurements.map(d => new Date(d.time_utc).toLocaleTimeString()), [measurements]);
  const magnitudes = useMemo(() => measurements.map(d => d.magnitude), [measurements]);

  const events = useMemo(() => {
    if (!measurements.length) return [];
    let minMagIndex = 0;

    for (let i = 0; i < measurements.length; i++) {
      if (measurements[i].magnitude < measurements[minMagIndex].magnitude) minMagIndex = i;
    }

    return [
      { label: "Start", time: measurements[0].time_utc },
      { label: "End", time: measurements[measurements.length - 1].time_utc },
      { label: "Brightest (Min Magnitude)", time: measurements[minMagIndex].time_utc },
    ];
  }, [measurements]);
  // ---------------------------------------------------

  if (!planet || !measurements.length) {
    return (
      <div style={{ padding: "16px", minHeight: "100vh", backgroundColor: "#121212", color: "white" }}>
        <h3>No visibility data available</h3>
        <button className="btn btn-outline-warning mt-2" onClick={() => navigate(-1)}>Back</button>
      </div>
    );
  }

  const panelBg = { backgroundColor: "#1a1a1a", color: "white", padding: "12px", borderRadius: "8px" };
  const orangeBorder = { border: "1px solid orange" };

  const createChartData = (yData, label, color) => ({
    labels: times,
    datasets: [
      {
        label,
        data: yData,
        borderColor: color,
        backgroundColor: color,
        tension: 0.2,
      },
    ],
  });

  const chartOptions = yLabel => ({
    responsive: true,
    plugins: { legend: { labels: { color: "white" } } },
    scales: {
      x: { ticks: { color: "white" } },
      y: { ticks: { color: "white" }, title: { display: true, text: yLabel, color: "white" } },
    },
  });

  return (
    <div style={{ padding: "16px", minHeight: "100vh", backgroundColor: "#121212" }}>
      <button className="btn btn-sm btn-outline-warning mb-3" onClick={() => navigate(-1)}>
        ← Back
      </button>

      <h2 style={{ color: "orange", marginBottom: "12px" }}>{planet} Visibility</h2>

      <div style={{ ...panelBg, ...orangeBorder, marginBottom: "16px" }}>
        {/* Graph toggle buttons */}
        <div style={{ marginBottom: "12px" }}>
          <button
            className={`btn btn-sm me-2 ${currentGraph === "magnitude" ? "btn-warning" : "btn-outline-warning"}`}
            onClick={() => setCurrentGraph("magnitude")}
          >
            Magnitude
          </button>
        </div>

        {/* Render chart based on toggle */}
        {currentGraph === "magnitude" && (
          <Line data={createChartData(magnitudes, "Magnitude", "orange")} options={chartOptions("Magnitude")} />
        )}

        {/* Key events */}
        <div style={{ marginTop: "16px" }}>
          <h5 style={{ color: "orange" }}>Key Events / Notes</h5>
          <ul style={{ color: "lightgray" }}>
            {events.map((ev, idx) => (
              <li key={idx}>
                <strong>{ev.label}:</strong> {new Date(ev.time).toLocaleString()}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
