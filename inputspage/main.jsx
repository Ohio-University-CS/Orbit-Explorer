import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { InputProvider } from "./context/InputContext.jsx";

function Next() {
  return (
    <div className="w-full h-screen flex items-center justify-center bg-white">
      <button
        className="px-6 py-3 text-lg font-semibold rounded-full shadow-md"
        style={{ backgroundColor: "orange", color: "white" }}
      >
        Orange Button
      </button>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <InputProvider>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/next" element={<Next />} />
        </Routes>
      </InputProvider>
    </BrowserRouter>
  </React.StrictMode>
);
