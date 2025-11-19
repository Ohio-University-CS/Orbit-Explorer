// frontendeng/frontend/src/Signup.js
import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';

function Signup() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    try {
      const res = await axios.post('http://localhost:8081/signup', {
        username,
        password,
      });

      console.log('Signup response:', res.data);
      setMessage(res.data.message || 'Signup successful');

      // go straight into the Three.js page
      navigate('/cosmic');
    } catch (err) {
      console.error('Signup error:', err.response?.data || err.message);
      setMessage(err.response?.data?.message || 'Signup error');
    }
  };

  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{ height: '100vh', backgroundColor: '#FF964F' }}
    >
      <div className="p-4 bg-white rounded shadow" style={{ width: '350px' }}>
        <h3 className="text-center mb-4">Sign Up</h3>

        {message && (
          <div className="alert alert-info text-center">{message}</div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Email / Username</label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter Email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
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
            />
          </div>

          <button
            className="btn w-100"
            style={{ backgroundColor: '#FF964F', color: 'white' }}
          >
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
}

export default Signup;

