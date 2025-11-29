import { useEffect } from "react";
import * as THREE from "react";
import SceneInit from "./lib/ScreenInit";
import { useInputContext } from "./context/InputContext.jsx";
import { Routes, Route, useNavigate } from "react-router-dom";


import InputsPage from "./InputsPage.jsx";

function App() {
  const navigate = useNavigate();
  const { inputs } = useInputContext();

  useEffect(() => {
    const test = new SceneInit("myThreeJSCanvas");
    test.initScene();
    test.animate();

    const geometry = new THREE.BoxGeometry(16, 16, 16);
    const material = new THREE.MeshNormalMaterial();
    const mesh = new THREE.Mesh(geometry, material);

    test.scene.add(mesh);
  }, []);

  return (
    <Routes>
      <Route path="/" element={<canvas id="myThreeJSCanvas" />} />
      <Route path="/inputs" element={<InputsPage />} />
      <Route path="/next" element={<NextPage />} />
    </Routes>
  );
}

export default App;
