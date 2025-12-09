// frontendeng/frontend/src/App.js
import React from "react";
import styled from "styled-components";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";

import Main from "./components/Main";             // animated background
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Search from "./Search";
import EventVisualization from "./EventVisualization";
import ViewOccultation from "./pages/ViewOccultation";

import Settings from "./pages/Settings";
import Account from "./pages/Account";
import ViewVisibility from "./pages/ViewVisibility";
import ObserveObject from "./pages/ObserveObject";
import Event from "./pages/Event";

// Orange / black button style
const Button = styled.button`
  background-color: #ff964f;
  color: #ffffff;
  width: 250px;
  padding: 20px 0;
  font-size: 24px;
  border-radius: 10px;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
  transition: all 200ms ease;
  border: none;

  &:hover {
    background-color: #000000;
    color: #ff964f;
    transform: scale(1.05);
  }
`;

// Landing screen = Main background + login/signup/explore buttons
function LandingScreen() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        position: "relative",
        height: "100vh",
        width: "100%",
        overflow: "hidden",
      }}
    >
      {/* Animated background */}
      <Main />

      {/* Centered buttons overlay */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: "20px",
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            pointerEvents: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "20px",
          }}
        >
          <Button onClick={() => navigate("/login")}>LOGIN</Button>
          <Button onClick={() => navigate("/signup")}>SIGN UP</Button>
          <Button onClick={() => navigate("/search")}>EXPLORE</Button>
        </div>
      </div>
    </div>
  );
}

// Frame that shows the Three.js inputs UI built into /public/cosmic
function CosmicFrame() {
  return (
    <div style={{ height: "100vh", width: "100vw", margin: 0, padding: 0 }}>
      <iframe
        title="Cosmic Inputs"
        src="/cosmic/index.html"
        style={{ border: "none", width: "100%", height: "100%" }}
      />
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Landing with buttons */}
        <Route path="/" element={<LandingScreen />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/account" element={<Account />} />

        <Route path="/view-occultation/:id?" element={<ViewOccultation />} />
        <Route path="/view-visibility/:id?" element={<ViewVisibility/>} />
        <Route path="/event/:id" element={<Event />} /> {}
        <Route path="/observe-object/:id?" element={<ObserveObject/>} />

        {/* Auth pages */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Three.js inputs page */}
        <Route path="/cosmic" element={<CosmicFrame />} />

        {/* Occultation search + visualization */}
        <Route path="/search" element={<Search />} />
        <Route path="/visualize" element={<EventVisualization />} />

      </Routes>
    </Router>
  );
}

export default App;
