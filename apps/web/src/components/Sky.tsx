"use client";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

export default function Sky({az=180, el=45}:{az?:number; el?:number}) {
  const rad = (d:number)=> d*Math.PI/180;
  const r = 5;
  const x = r * Math.cos(rad(el)) * Math.sin(rad(az));
  const y = r * Math.sin(rad(el));
  const z = r * Math.cos(rad(el)) * Math.cos(rad(az));
  return (
    <div style={{height:300}}>
      <Canvas>
        <ambientLight intensity={0.3}/>
        <pointLight position={[x,y,z]} intensity={2}/>
        <mesh>
          <sphereGeometry args={[1,32,32]} />
          <meshStandardMaterial metalness={0.2} roughness={0.8}/>
        </mesh>
        <OrbitControls />
      </Canvas>
    </div>
  );
}
