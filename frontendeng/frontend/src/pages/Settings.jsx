// frontendeng/frontend/src/pages/Settings.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import TopMenu from "../components/TopMenu";

import { setFavicon } from "../setFavicon";

const API_BASE =
  import.meta.env?.VITE_API_BASE ||
  process.env.REACT_APP_API_BASE ||
  "http://localhost:8000";

export default function Settings() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorText, setErrorText] = useState("");

  useEffect(() => {
    setFavicon("/icons/space.ico");
  }, []);

  useEffect(() => {
    document.title = 'Settings';
  }, []);

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      setErrorText("");

      try {
        const token = localStorage.getItem("access_token");
        if (!token) throw new Error("Not authorized");

        const headers = { Authorization: `Bearer ${token}` };
        const res = await axios.get(`${API_BASE}/users/info`, { headers });

        setUser(res.data);
      } catch (err) {
        console.error(err);
        setErrorText(err.message || "Failed to fetch user info");
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

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

  return (
    <div style={starBg}>
      <TopMenu />
      <div className="container" style={{ maxWidth: 800, marginTop: 24 }}>
        <h1 className="text-center mb-4" style={orangeText}>Settings</h1>

        {loading && <p className="text-white">Loading user info...</p>}
        {errorText && <p className="text-danger">{errorText}</p>}

        {user && (
          <div style={panelBg}>
            <div className="mb-3">
              <label className="form-label text-white">First Name</label>
              <input className="form-control" type="text" value={user.first_name || ""} readOnly />
            </div>
            <div className="mb-3">
              <label className="form-label text-white">Last Name</label>
              <input className="form-control" type="text" value={user.last_name || ""} readOnly />
            </div>
            <div className="mb-3">
              <label className="form-label text-white">Username</label>
              <input className="form-control" type="text" value={user.username || ""} readOnly />
            </div>
            <div className="mb-3">
              <label className="form-label text-white">Email</label>
              <input className="form-control" type="email" value={user.email || ""} readOnly />
            </div>
            <div className="mb-3">
              <label className="form-label text-white">Account Created</label>
              <input
                className="form-control"
                type="text"
                value={user.created_at ? new Date(user.created_at).toLocaleString() : ""}
                readOnly
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
