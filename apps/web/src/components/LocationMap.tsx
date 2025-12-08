"use client";

import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import { useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

export default function LocationMap({
  lat,
  lon,
  onSelect,
}: {
  lat: number;
  lon: number;
  onSelect: (lat: number, lon: number, label?: string) => void;
}) {
  const [position, setPosition] = useState<[number, number]>([lat, lon]);
  const [label, setLabel] = useState("");

  function MapClickHandler() {
    useMapEvents({
      click: async (e) => {
        const { lat, lng } = e.latlng;
        setPosition([lat, lng]);

        // Call backend reverse geocode
        const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";
        const url = `${base}/events/reverse_geocode?lat=${lat}&lon=${lng}`;

        try {
          const r = await fetch(url);
          const data = await r.json();

          const readable = `${data.city || ""} ${data.state || ""} ${
            data.country || ""
          }`.trim();

          setLabel(readable);
          onSelect(lat, lng, readable);
        } catch {
          setLabel("");
          onSelect(lat, lng);
        }
      },
    });
    return null;
  }

  return (
    <div
      style={{
        height: "300px",
        width: "100%",
        borderRadius: 6,
        overflow: "hidden",
      }}
    >
      <MapContainer
        center={position}
        zoom={4}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution="© OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapClickHandler />
        <Marker position={position} icon={markerIcon} />
      </MapContainer>

      {label && (
        <div
          style={{
            marginTop: 6,
            fontSize: 14,
            padding: "4px 6px",
            background: "#1a2234",
            borderRadius: 4,
            color: "#e6f0ff",
          }}
        >
          {label}
        </div>
      )}
    </div>
  );
}
