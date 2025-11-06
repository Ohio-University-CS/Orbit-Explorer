import React from 'react';
import styled from 'styled-components';
import Main from "../components/Main";
import { Link } from "react-router-dom";
import CustomButton from "../components/CustomButton.jsx"

function clickMe(){
  alert('You clicked me!');
}

export default function Home() {

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

          <CustomButton onClick={clickMe}>LOGIN</CustomButton>
          <CustomButton onClick={clickMe}>SIGN UP</CustomButton>
          <Link to="/search">
            <CustomButton>Search for events</CustomButton>
          </Link>
    </div>
    </div>
  );
}
