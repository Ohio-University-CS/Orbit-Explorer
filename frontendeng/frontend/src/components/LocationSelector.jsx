import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import Map from "ol/Map.js";
import View from "ol/View.js";
import TileLayer from "ol/layer/Tile.js";
import OSM from "ol/source/OSM.js";
import { fromLonLat, toLonLat } from "ol/proj.js";
import { defaults as defaultControls } from "ol/control/defaults.js";

const API_BASE =
  (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_BASE) ||
  process.env.REACT_APP_API_BASE ||
  "http://localhost:8000";

// --- Helpers for validation ---
const isValidLatitude = lat => !isNaN(lat) && lat >= -90 && lat <= 90;
const isValidLongitude = lon => !isNaN(lon) && lon >= -180 && lon <= 180;
const isValidAltitude = alt => !isNaN(alt) && alt >= -0.5 && alt <= 100000;

export default function LocationSelector({ value, onChange }) {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [latInput, setLatInput] = useState(value?.lat ?? "");
  const [lonInput, setLonInput] = useState(value?.lon ?? "");
  const [altInput, setAltInput] = useState(value?.alt_km ?? "");

  const [showMap, setShowMap] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [nameInput, setNameInput] = useState("");
  const [descInput, setDescInput] = useState("");
  const [map, setMap] = useState(null);
  const mapContainerRef = useRef(null);
  const [tempCoords, setTempCoords] = useState(null);

  const [selectedLocationId, setSelectedLocationId] = useState(null);

  const getAuthHeaders = () => {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Not authorized");
    return { Authorization: `Bearer ${token}` };
  };

  // Load saved locations
  useEffect(() => {
    async function fetchLocations() {
      setLoading(true);
      setError("");
      try {
        const headers = getAuthHeaders();
        const res = await axios.get(`${API_BASE}/users/locations`, { headers });
        setLocations(res.data || []);
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to load locations");
      } finally {
        setLoading(false);
      }
    }
    fetchLocations();
  }, []);

  // Init map
  useEffect(() => {
    if (!showMap) return;
    if (!map) {
      const mapObj = new Map({
        target: mapContainerRef.current,
        layers: [new TileLayer({ source: new OSM() })],
        view: new View({ center: fromLonLat([0, 0]), zoom: 2 }),
        controls: defaultControls({ zoom: true, rotate: false, attribution: false }),
      });
      mapObj.on("click", evt => setTempCoords(toLonLat(evt.coordinate)));
      setMap(mapObj);
    } else {
      map.setTarget(mapContainerRef.current);
    }
  }, [showMap, map]);

  // Push only valid values to parent
  useEffect(() => {
    if (typeof onChange !== "function") return;

    const lat = parseFloat(latInput);
    const lon = parseFloat(lonInput);
    const alt_km = parseFloat(altInput) || 0;

    if (isValidLatitude(lat) && isValidLongitude(lon)) {
      onChange({ lat, lon, alt_km });
    } else {
      onChange(null); // invalid or empty inputs
    }
  }, [latInput, lonInput, altInput, onChange]);

  const getCurrentLocation = () => {
    if (!navigator.geolocation) return alert("Geolocation not supported");
    navigator.geolocation.getCurrentPosition(
      pos => {
        const lat = pos.coords.latitude.toFixed(6);
        const lon = pos.coords.longitude.toFixed(6);
        if (!isValidLatitude(lat) || !isValidLongitude(lon)) {
          return alert("Geolocation returned invalid coordinates");
        }
        setLatInput(lat);
        setLonInput(lon);
      },
      err => alert("Geolocation failed: " + err.message)
    );
  };

  const confirmMapCoords = () => {
    if (!tempCoords) return alert("Click a coordinate on the map first");
    const [lon, lat] = tempCoords.map(c => parseFloat(c.toFixed(6)));
    if (!isValidLatitude(lat) || !isValidLongitude(lon)) {
      return alert("Selected coordinates are invalid");
    }
    setLatInput(lat);
    setLonInput(lon);
    setShowMap(false);
  };

  const saveNewLocation = async () => {
    const lat = parseFloat(latInput);
    const lon = parseFloat(lonInput);
    const alt_km = parseFloat(altInput) || 0;

    if (!nameInput.trim()) return alert("Name is required");
    if (!isValidLatitude(lat)) return alert("Latitude must be between -90 and 90");
    if (!isValidLongitude(lon)) return alert("Longitude must be between -180 and 180");
    if (!isValidAltitude(alt_km)) return alert("Altitude is invalid");

    try {
      const headers = getAuthHeaders();
      const payload = {
        loc_name: nameInput.trim(),
        loc_description: descInput.trim() || null,
        latitude: lat,
        longitude: lon,
        alt_km,
      };
      const res = await axios.post(`${API_BASE}/users/locations/add`, payload, { headers });

      const newLoc = { ...payload, id: res.data.id, user_uuid: res.data.user_uuid };
      setLocations(prev => [...prev, newLoc]);
      setSelectedLocationId(newLoc.id);

      setShowAddModal(false);
      setNameInput("");
      setDescInput("");
      alert("Location saved!");
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Failed to save location");
    }
  };

  const selectSavedLocation = loc => {
    setLatInput(loc.latitude);
    setLonInput(loc.longitude);
    setAltInput(loc.alt_km || 0);
    setSelectedLocationId(loc.id);
  };

  const inputRowStyle = {
    display: "flex",
    gap: "8px",
    flexWrap: "wrap",
    alignItems: "flex-start",
  };
  const inputContainerStyle = { display: "flex", flexDirection: "column", flex: "1 1 80px" };
  const inputStyle = { padding: "4px 6px", borderRadius: "6px" };
  const buttonStyle = { flex: "1 1 auto", padding: "4px 6px", fontSize: "13px", borderRadius: "6px", cursor: "pointer" };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
      {/* Dropdown */}
      <select
        style={{ ...inputStyle, flex: "1 1 100%" }}
        value={selectedLocationId || ""}
        onChange={e => {
          const loc = locations.find(l => l.id === parseInt(e.target.value));
          if (loc) selectSavedLocation(loc);
        }}
      >
        <option value="">Select Saved Location</option>
        {locations.map(loc => (
          <option key={loc.id} value={loc.id}>
            {loc.loc_name}
          </option>
        ))}
      </select>

      {loading && <div>Loading...</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}

      {/* Lat / Lon / Alt inputs */}
      <div style={inputRowStyle}>
        <div style={inputContainerStyle}>
          <label className="text-light">Latitude</label>
          <input
            type="number"
            value={latInput}
            onChange={e => setLatInput(e.target.value)}
            style={inputStyle}
          />
        </div>
        <div style={inputContainerStyle}>
          <label className="text-light">Longitude</label>
          <input
            type="number"
            value={lonInput}
            onChange={e => setLonInput(e.target.value)}
            style={inputStyle}
          />
        </div>
        <div style={inputContainerStyle}>
          <label className="text-light">Altitude (km)</label>
          <input
            type="number"
            value={altInput}
            onChange={e => setAltInput(e.target.value)}
            style={inputStyle}
          />
        </div>
      </div>

      {/* Buttons */}
      <div style={inputRowStyle}>
        <button style={buttonStyle} onClick={() => setShowMap(true)}>Pick from Map</button>
        <button style={buttonStyle} onClick={getCurrentLocation}>Current Location</button>
      </div>

      <button style={{ ...buttonStyle, width: "150px" }} onClick={() => setShowAddModal(true)}>Save Location</button>

      {/* Add Location Modal */}
      {showAddModal && (
        <div style={{
          position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)",
          display: "flex", justifyContent: "center", alignItems: "center", zIndex: 9999
        }}>
          <div style={{ background: "white", padding: "12px", borderRadius: "8px", width: "300px" }}>
            <input
              type="text"
              placeholder="Name"
              value={nameInput}
              onChange={e => setNameInput(e.target.value)}
              style={{ ...inputStyle, width: "100%", marginBottom: "6px" }}
            />
            <input
              type="text"
              placeholder="Description"
              value={descInput}
              onChange={e => setDescInput(e.target.value)}
              style={{ ...inputStyle, width: "100%", marginBottom: "6px" }}
            />
            <div style={{ display: "flex", gap: "6px" }}>
              <button style={buttonStyle} onClick={saveNewLocation}>Save</button>
              <button style={buttonStyle} onClick={() => setShowAddModal(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {/* Map Modal */}
      {showMap && (
        <div style={{
          position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)",
          display: "flex", justifyContent: "center", alignItems: "center", zIndex: 9999
        }}>
          <div style={{ background: "white", padding: "8px", borderRadius: "8px" }}>
            <div ref={mapContainerRef} style={{ width: "400px", height: "300px" }}></div>
            <div style={{ display: "flex", gap: "4px", marginTop: "4px" }}>
              <button style={buttonStyle} onClick={confirmMapCoords}>Use</button>
              <button style={buttonStyle} onClick={() => setShowMap(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
