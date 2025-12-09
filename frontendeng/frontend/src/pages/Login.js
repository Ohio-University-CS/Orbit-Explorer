import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import { setFavicon } from "../setFavicon";

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  
    useEffect(() => {
      setFavicon("/icons/space.ico");
    }, []);
  
    useEffect(() => {
      document.title = 'Login';
    }, []);
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    try {
      const res = await axios.post('http://localhost:8000/auth/login', {
        username,
        password,
      });

      const token = res.data.access_token;

      if (!token) {
        setMessage("Login failed: No token returned");
        return;
      }

      localStorage.setItem("access_token", token);
      setMessage("Login successful");

      navigate("/search");
    } catch (err) {
      console.error("Login error:", err.response?.data || err.message);
      setMessage(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "Login error"
      );
    }
  };

  const goHome = () => navigate("/");
  const goSignup = () => navigate("/signup");

  const panelStyle = {
    backgroundColor: "#1a1a1a",
    color: "white",
    padding: "24px",
    borderRadius: "8px",
    boxShadow: "0 0 12px rgba(0,0,0,0.5)",
    width: "360px",
  };

  const btnPrimary = {
    backgroundColor: "#FF964F",
    color: "white",
  };

  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{ height: "100vh", backgroundColor: "#121212" }}
    >
      <div style={panelStyle}>
        <h3 className="text-center mb-4" style={{ color: "#FF964F" }}>Login</h3>

        {message && (
          <div
            className="alert text-center"
            style={{ color: "white", backgroundColor: "#333", border: "1px solid #FF964F" }}
          >
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{
                backgroundColor: "#121212",
                color: "#ccc",
                border: "1px solid #FF964F",
              }}
              placeholderTextColor="#888"
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Password</label>


            <input
              type="password"
              className="form-control"
              placeholder="Enter Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{
                backgroundColor: "#121212",
                color: "#ccc",
                border: "1px solid #FF964F",
              }}
              placeholderTextColor="#888"
            />
          </div>

          <button type="submit" className="btn w-100 mb-3" style={btnPrimary}>
            Login
          </button>
        </form>

        <button className="btn w-100 mb-2" style={{ backgroundColor: "#333", color: "white", border: "1px solid #FF964F" }} onClick={goHome}>
          Home
        </button>

        <button className="btn w-100" style={{ backgroundColor: "transparent", color: "#FF964F", border: "1px solid #FF964F" }} onClick={goSignup}>
          Register
        </button>
      </div>
    </div>
  );
}
