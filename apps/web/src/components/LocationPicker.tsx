import { MapContainer, TileLayer, useMapEvents, Marker } from "react-leaflet";
import React, { useState } from "react";

export default function LocationPicker({ onSelect }) {
  const [position, setPosition] = useState(null);

  function LocationMarker() {
    useMapEvents({
      click(e) {
        setPosition(e.latlng);
        onSelect(e.latlng);
      }
    });

    return position ? <Marker position={position}></Marker> : null;
  }

  return (
    <MapContainer 
      center={[39.3, -82.1]} 
      zoom={7} 
      style={{ height: "400px", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <LocationMarker />
    </MapContainer>
  );
}
