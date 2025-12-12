import React from "react";

function NextPage() {
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

export default NextPage;
