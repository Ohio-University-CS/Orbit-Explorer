import React from 'react';
import styled from 'styled-components';
import Main from "./components/Main";

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

function clickMe(){
  alert('You clicked me!');
}

export default function App() {
  return (
    <div style = {{ position: "relative", height: "100vh", width: "100%"}}>
        {/* Fullscreen */}
        <Main />

        {/*Button container */}
        <div 
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: "20px"
        }}
        >

          <Button onClick={clickMe}>LOGIN</Button>
          <Button onClick={clickMe}>SIGN UP</Button>
    </div>
    </div>
  );
}
