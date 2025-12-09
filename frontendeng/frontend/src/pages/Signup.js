import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import { setFavicon } from "../setFavicon";

export default function Signup() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    setFavicon("/icons/space.ico");
  }, []);

  useEffect(() => {
    document.title = 'Signup';
  }, []);


  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const res = await axios.post('http://localhost:8000/auth/register', {
        username,
        password,
        email,
        first_name: firstName || null,
        last_name: lastName || null,
      });
      if (res.data.access_token) localStorage.setItem('access_token', res.data.access_token);
      setMessage(res.data.message || 'Signup successful');
      navigate('/search');
    } catch (err) {
      console.error('Signup error:', err.response?.data || err.message);
      setMessage(
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Signup error'
      );
    }
  };


  const goHome = () => navigate('/');
  const goLogin = () => navigate('/login');

  const panelStyle = {
    backgroundColor: "#1a1a1a",
    color: "white",
    padding: "24px",
    borderRadius: "8px",
    boxShadow: "0 0 12px rgba(0,0,0,0.5)",
    width: "360px",
  };

  const btnPrimary = { backgroundColor: "#FF964F", color: "white" };

  const inputStyle = {
    backgroundColor: "#121212",
    color: "#ccc",
    border: "1px solid #FF964F",
  };

  return (
    <div className="d-flex justify-content-center align-items-center" style={{ height: "100vh", backgroundColor: "#121212" }}>
      <div style={panelStyle}>
        <h3 className="text-center mb-4" style={{ color: "#FF964F" }}>Sign Up</h3>

        {message && (
          <div className="alert text-center" style={{ color: "white", backgroundColor: "#333", border: "1px solid #FF964F" }}>
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Username</label>
            <input type="text" className="form-control" placeholder="Enter Username" value={username} onChange={e => setUsername(e.target.value)} required style={inputStyle} />
          </div>

          <div className="mb-3">
            <label className="form-label">Email</label>
            <input type="email" className="form-control" placeholder="Enter Email" value={email} onChange={e => setEmail(e.target.value)} required style={inputStyle} />
          </div>

          <div className="mb-3">
            <label className="form-label">Password</label>
            <input type="password" className="form-control" placeholder="Enter Password" value={password} onChange={e => setPassword(e.target.value)} required style={inputStyle} />
          </div>

          <div className="mb-3">
            <label className="form-label">First Name (optional)</label>
            <input type="text" className="form-control" placeholder="First Name" value={firstName} onChange={e => setFirstName(e.target.value)} style={inputStyle} />
          </div>

          <div className="mb-3">
            <label className="form-label">Last Name (optional)</label>
            <input type="text" className="form-control" placeholder="Last Name" value={lastName} onChange={e => setLastName(e.target.value)} style={inputStyle} />
          </div>

          <button type="submit" className="btn w-100 mb-3" style={btnPrimary}>Sign Up</button>
        </form>

        <button className="btn w-100 mb-2" style={{ backgroundColor: "#333", color: "white", border: "1px solid #FF964F" }} onClick={goHome}>
          Home
        </button>

        <button className="btn w-100" style={{ backgroundColor: "transparent", color: "#FF964F", border: "1px solid #FF964F" }} onClick={goLogin}>
          Login
        </button>
      </div>
    </div>
  );
}
