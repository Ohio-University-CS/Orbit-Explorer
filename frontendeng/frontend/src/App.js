import React from 'react';
import styled from 'styled-components';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import Main from './components/Main';
import CosmicFrame from './components/CosmicFrame';

const Button = styled.button`
  background-color: #FF964F;
  color: white;
  width: 250px;
  padding: 20px 0;
  font-size: 24px;
  border-radius: 10px;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0,0,0,.2);
  transition: all 250ms ease;
  border: none;
  &:hover { background-color: black; transform: scale(1.05); }
`;

function LoadingScreen() {
  const navigate = useNavigate();
  return (
    <div style={{ position:'relative', height:'100vh', width:'100%' }}>
      <Main />
      <div style={{ position:'absolute', inset:0, display:'flex', flexDirection:'column',
                    justifyContent:'center', alignItems:'center', gap:'20px' }}>
        <Button onClick={() => alert('You clicked login!')}>LOGIN</Button>
        <Button onClick={() => alert('You clicked signup!')}>SIGN UP</Button>
        <Button onClick={() => navigate('/cosmic')}>EXPLORE</Button>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoadingScreen />} />
        <Route path="/cosmic" element={<CosmicFrame />} />
      </Routes>
    </BrowserRouter>
  );
}
