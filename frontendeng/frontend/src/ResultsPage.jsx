import React from "react";
import { useNavigate } from "react-router-dom";

export default function ResultsPage() {
  const navigate = useNavigate();
  return (
    <div className="h-screen w-screen flex justify-center items-center bg-black">
      <button
        onClick={() => navigate("/")}
        className="bg-orange-500 text-white text-3xl px-16 py-8 rounded-xl hover:scale-110 transition"
        style={{ backgroundColor: "#FF964F", width: "100vw", height: "100vh", border: "none" }}
      >
        BACK TO COSMIC 
      </button>
    </div>
  );
}
