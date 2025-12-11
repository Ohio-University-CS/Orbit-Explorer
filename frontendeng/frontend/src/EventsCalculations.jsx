// frontendeng/frontend/src/EventCalculations.jsx
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

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
  maxWidth: "960px",
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

const backButtonStyle = {
  padding: "8px 14px",
  borderRadius: "999px",
  border: "1px solid #ff9d2b",
  background: "#111",
  color: "#ff9d2b",
  fontSize: "12px",
  fontWeight: 600,
  cursor: "pointer",
};

export default function EventCalculations() {
  const navigate = useNavigate();
  const { state } = useLocation() || {};

  const event = state?.event;
  const lat = state?.lat;
  const lon = state?.lon;
  const elevation = state?.elevation;
  const startTimeStr = state?.startTime;
  const endTimeStr = state?.endTime;

  let durationHours = null;
  let startDate = null;
  let endDate = null;

  if (startTimeStr && endTimeStr) {
    startDate = new Date(startTimeStr);
    endDate = new Date(endTimeStr);
    const diffMs = endDate - startDate;
    if (!isNaN(diffMs)) {
      durationHours = diffMs / (1000 * 60 * 60);
    }
  }

  const absLat = lat !== undefined && lat !== null ? Math.abs(parseFloat(lat)) : null;
  const distanceFromEquatorKm =
    absLat !== null ? absLat * 111.0 : null; // rough 111 km per degree

  const eventTime = event?.time ? new Date(event.time) : null;

  return (
    <div style={pageStyle}>
      <div style={shellStyle}>
        <button style={backButtonStyle} onClick={() => navigate(-1)}>
          ← Back to Results
        </button>

        <h1
          style={{
            fontSize: "26px",
            marginTop: "16px",
            marginBottom: "4px",
          }}
        >
          Event Calculations
        </h1>
        <p style={{ fontSize: "13px", color: "#f7f7f7", marginBottom: "8px" }}>
          Using your inputted latitude, longitude, elevation, and time window to
          derive quick insights for this event.
        </p>

        {!event && (
          <p style={{ marginTop: 16, color: "#ff8080", fontSize: 13 }}>
            No event data was provided. Go back to the results and open
            calculations again.
          </p>
        )}

        {event && (
          <>
            {/* Event summary */}
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
                1 · Event Summary
              </div>
              <p style={{ fontSize: 14, marginBottom: 4 }}>
                <strong>Name:</strong> {event.name || event.type || event.id}
              </p>
              <p style={{ fontSize: 14, marginBottom: 4 }}>
                <strong>Type:</strong> {event.type}
              </p>
              <p style={{ fontSize: 14, marginBottom: 4 }}>
                <strong>Event time (UTC):</strong>{" "}
                {eventTime ? eventTime.toUTCString() : "—"}
              </p>
              {event.desc && (
                <p style={{ fontSize: 13, marginTop: 8, color: "#f7f7f7" }}>
                  {event.desc}
                </p>
              )}
            </section>

            {/* Observer geometry */}
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
                2 · Observer Geometry
              </div>
              <p style={{ fontSize: 14, marginBottom: 4 }}>
                <strong>Latitude:</strong>{" "}
                {lat !== undefined ? `${lat}°` : "—"}
              </p>
              <p style={{ fontSize: 14, marginBottom: 4 }}>
                <strong>Longitude:</strong>{" "}
                {lon !== undefined ? `${lon}°` : "—"}
              </p>
              <p style={{ fontSize: 14, marginBottom: 4 }}>
                <strong>Elevation:</strong>{" "}
                {elevation !== undefined ? `${elevation} m` : "—"}
              </p>

              {distanceFromEquatorKm !== null && (
                <p style={{ fontSize: 13, marginTop: 8, color: "#f7f7f7" }}>
                  Approximate distance from the equator:{" "}
                  <strong>{distanceFromEquatorKm.toFixed(1)} km</strong>
                </p>
              )}
            </section>

            {/* Time window calculations */}
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
                3 · Time Window
              </div>

              <p style={{ fontSize: 14, marginBottom: 4 }}>
                <strong>Start (local input):</strong>{" "}
                {startTimeStr || "—"}
              </p>
              <p style={{ fontSize: 14, marginBottom: 4 }}>
                <strong>End (local input):</strong>{" "}
                {endTimeStr || "—"}
              </p>

              {durationHours !== null && !isNaN(durationHours) && (
                <p style={{ fontSize: 13, marginTop: 8, color: "#f7f7f7" }}>
                  Total duration of search window:{" "}
                  <strong>{durationHours.toFixed(2)} hours</strong>
                </p>
              )}

              {eventTime && startDate && endDate && (
                <p style={{ fontSize: 13, marginTop: 6, color: "#f7f7f7" }}>
                  This event occurs{" "}
                  <strong>
                    {((eventTime - startDate) / (1000 * 60)).toFixed(0)} minutes
                  </strong>{" "}
                  after your selected start time.
                </p>
              )}
            </section>
          </>
        )}
      </div>
    </div>
  );
}



