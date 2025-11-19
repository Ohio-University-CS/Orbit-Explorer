// frontendeng/frontend/src/App.js
import React from 'react';
import styled from 'styled-components';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import Main from './components/Main';
import Login from './Login';
import Signup from './Signup';

const Button = styled.button`
  background-color: #FF964F;
  color: white;
  width: 250px;
  padding: 20px 0;
  font-size: 24px;
  border-radius: 10px;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  transition: all 250ms ease;
  border: none;

  &:hover {
    background-color: black;
    transform: scale(1.05);
  }
`;

// Loading / landing screen with video + buttons
function LoadingScreen() {
  const navigate = useNavigate();

  return (
    <div style={{ position: 'relative', height: '100vh', width: '100%' }}>
      {/* Fullscreen background (loading screen) */}
      <Main />

      {/* Button overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '20px',
        }}
      >
        <Button onClick={() => navigate('/login')}>LOGIN</Button>
        <Button onClick={() => navigate('/signup')}>SIGN UP</Button>
        <Button onClick={() => navigate('/cosmic')}>EXPLORE</Button>
      </div>
    </div>
  );
}

// Frame that loads Three.js build from /public/cosmic
function CosmicFrame() {
  return (
    <div style={{ height: '100vh', width: '100vw', margin: 0, padding: 0 }}>
      <iframe
        title="Cosmic"
        src="/cosmic/index.html"
        style={{ border: 'none', width: '100%', height: '100%' }}
      />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoadingScreen />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/cosmic" element={<CosmicFrame />} />
      </Routes>
    </BrowserRouter>
  );
}

