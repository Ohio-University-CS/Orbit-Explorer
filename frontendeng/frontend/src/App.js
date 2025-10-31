import React from "react";

function clickMe() {
  alert('You clicked me!');
}
 
export default function App() {
  return (
    <div>
      <button onClick={clickMe}>
        Button
      </button>
    </div>
  );
}