'use client'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Html, Line } from '@react-three/drei'
import { useEffect, useMemo, useRef, useState } from 'react'
import * as THREE from 'three'

type BodyName = 'sun'|'mercury'|'venus'|'earth'|'moon'|'mars'|'jupiter'|'saturn'|'uranus'|'neptune'
type Vec3 = [number, number, number]

// Simple scales so things are visible (log-ish). Distances in AU from API.
const DIST = 50   // multiplier for AU → scene units
const RAD  = 0.009; // multiplier for radius_km → scene units (tweak)

function Planet({ name, pos, radius_km, color='#aaa' }:{name:BodyName; pos:Vec3; radius_km:number; color?:string}) {
  const r = Math.max(0.15, Math.cbrt(radius_km) * RAD) // tame extremes
  return (
    <group position={pos}>
      <mesh>
        <sphereGeometry args={[r, 32, 32]} />
        <meshStandardMaterial emissive={name==='sun' ? new THREE.Color('#ffcc66') : undefined} color={color} />
      </mesh>
      <Html distanceFactor={8}><div style={{fontSize:12, color:'#e6f0ff'}}>{name}</div></Html>
    </group>
  )
}

export default function SolarSystem({ initial, frame, speed }:{ initial:any; frame:string; speed:number }) {
  const [state, setState] = useState<any>(initial)
  const timeRef = useRef<number>(Date.now())

  // live-update: advance time locally and refetch every ~30s via parent if needed
  useFrame((_, delta) => {
    if (!state) return
    timeRef.current += delta * 1000 * speed // speed seconds per real second
  })

  // compute planet nodes from state
  const bodies = useMemo(() => {
    if (!state?.bodies) return []
    const map: Record<BodyName, any> = state.bodies
    const order: BodyName[] = ['sun','mercury','venus','earth','moon','mars','jupiter','saturn','uranus','neptune']
    return order
      .filter(n => map[n])
      .map(n => ({
        name: n,
        pos: (map[n].xyz_au as Vec3).map(v => v*DIST) as Vec3,
        radius_km: map[n].radius_km as number,
        color: n==='sun' ? '#ffdb70' :
               n==='earth' ? '#6aa0ff' :
               n==='moon' ? '#bbb' :
               n==='mars' ? '#ff7b57' : '#a7b3c9'
      }))
  }, [state])

  return (
    <Canvas dpr={[1,2]} camera={{ position: [0, 40, 110], fov: 45 }}>
      <color attach="background" args={['#0b0f1a']} />
      <ambientLight intensity={0.25} />
      <pointLight position={[0,0,0]} intensity={2.2} />

      {bodies.map(b => (
        <Planet key={b.name} name={b.name as BodyName} pos={b.pos} radius_km={b.radius_km} color={b.color}/>
      ))}

      {/* simple circular orbits (visual only) */}
      {bodies.filter(b=>b.name!=='sun' && b.name!=='moon').map(b=>{
        const r = Math.hypot(b.pos[0], b.pos[2])
        const pts = new THREE.EllipseCurve(0,0,r,r).getSpacedPoints(256).map(p=>new THREE.Vector3(p.x,0,p.y))
        return <Line key={b.name+'_orbit'} points={pts} lineWidth={0.5} color="#2a3550" />
      })}

      <OrbitControls enableDamping />
    </Canvas>
  )
}
