import React from 'react';
import styled from 'styled-components';
import { Link } from "react-router-dom";
import SearchForm from "../components/SearchForm.jsx";
import CustomButton from "../components/CustomButton.jsx"


function clickMe(){
  alert('You clicked me!');
}

export default function Search() {
  return (
    <div style = {{ position: "relative", height: "100vh", width: "100%"}}>
        {/* Fullscreen */}
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
        <div>
            <SearchForm/>
        </div>
        <Link to="/">
          <CustomButton>Back</CustomButton>
        </Link>
    </div>
    </div>
  );
}
