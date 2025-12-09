// frontendeng/frontend/src/components/TopMenu.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

export default function TopMenu() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_uuid");
    navigate("/login");
  };

  return (
    <nav
      className="navbar navbar-expand-lg"
      style={{
        background: "#050505",
        borderBottom: "2px solid #ff9d2b",
        padding: "0.5rem 1rem",
        position: "sticky",
        top: 0,
        zIndex: 9999,
        marginBottom: "30px"
      }}
    >
      <div className="container-fluid">
        <span className="navbar-brand mb-0 h1" style={{ color: "#ff9d2b" }}>
          Orbit Explorer
        </span>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#topMenuCollapse"
          aria-controls="topMenuCollapse"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" style={{ color: "#ff9d2b" }}></span>
        </button>

        <div className="collapse navbar-collapse" id="topMenuCollapse">
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <button
                className="btn nav-link text-white"
                style={{ color: "#ff9d2b" }}
                onClick={() => navigate("/")}
              >
                Home
              </button>
            </li>
            <li className="nav-item">
              <button
                className="btn nav-link text-white"
                style={{ color: "#ff9d2b" }}
                onClick={() => navigate("/search")}
              >
                Search
              </button>
            </li>
            <li className="nav-item">
              <button
                className="btn nav-link text-white"
                style={{ color: "#ff9d2b" }}
                onClick={() => navigate("/settings")}
              >
                Settings
              </button>
            </li>
            <li className="nav-item">
              <button
                className="btn nav-link text-white"
                style={{ color: "#ff9d2b" }}
                onClick={() => navigate("/account")}
              >
                Account
              </button>
            </li>
            <li className="nav-item">
              <button
                className="btn nav-link text-white"
                style={{ color: "#ff9d2b" }}
                onClick={handleLogout}
              >
                Log Out
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
