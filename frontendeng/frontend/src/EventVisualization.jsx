import React, { useEffect, useRef } from "react";
import * as THREE from "three";
import { useLocation, useParams, useNavigate } from "react-router-dom";

function classifyEvent(event) {
  const raw =
    (event?.type ||
      event?.event_type ||
      event?.name ||
      event?.event_name ||
      "") + "";
  const t = raw.toUpperCase();

  if (t.includes("SOLAR")) return "SOLAR_ECLIPSE";
  if (t.includes("LUNAR")) return "LUNAR_ECLIPSE";
  if (t.includes("TRANSIT")) return "TRANSIT";
  if (t.includes("METEOR") || t.includes("SHOWER") || t.includes("OUTBURST"))
    return "METEOR";
  if (t.includes("COMET")) return "COMET";
  if (t.includes("ASTEROID")) return "ASTEROID";
  if (
    t.includes("SYZYGY") ||
    t.includes("CONJUNCTION") ||
    t.includes("OPPOSITION") ||
    t.includes("QUADRATURE")
  )
    return "ALIGNMENT";
  if (t.includes("SEASONAL") || t.includes("EQUINOX") || t.includes("SOLSTICE"))
    return "SEASONAL";
  if (t.includes("OCCULTATION")) return "OCCULTATION";
  return "GENERIC";
}

export default function EventVisualization() {
  const mountRef = useRef(null);
  const { eventId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const event = location.state?.event || null;
  const mode = classifyEvent(event);

  useEffect(() => {
    if (!mountRef.current) return;

    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 0, 10);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio || 1);

    // Guard: container might have been removed in hot reloads
    if (mountRef.current) {
      mountRef.current.appendChild(renderer.domElement);
    }

    const ambient = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambient);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1.1);
    keyLight.position.set(6, 8, 10);
    scene.add(keyLight);

    const group = new THREE.Group();
    scene.add(group);

    let extraAnimate = () => {};

    const bigSphereGeo = new THREE.SphereGeometry(3, 64, 64);
    const mediumSphereGeo = new THREE.SphereGeometry(1.4, 48, 48);
    const smallSphereGeo = new THREE.SphereGeometry(0.6, 32, 32);

    // --- Different visualizations per event mode ---

    if (mode === "SOLAR_ECLIPSE") {
      const sunMat = new THREE.MeshStandardMaterial({
        color: 0x331000,
        emissive: 0xffa500,
        emissiveIntensity: 1.6,
      });
      const sun = new THREE.Mesh(bigSphereGeo, sunMat);
      group.add(sun);

      const moonMat = new THREE.MeshStandardMaterial({ color: 0x000000 });
      const moon = new THREE.Mesh(mediumSphereGeo, moonMat);
      moon.position.set(-7, 0, 0.5);
      group.add(moon);

      extraAnimate = () => {
        moon.position.x += 0.05;
        if (moon.position.x > 7) moon.position.x = -7;
      };
    } else if (mode === "LUNAR_ECLIPSE") {
      const earthMat = new THREE.MeshStandardMaterial({
        color: 0x1b4a73,
        roughness: 0.7,
        metalness: 0.1,
      });
      const earth = new THREE.Mesh(mediumSphereGeo, earthMat);
      earth.position.set(-2.2, 0, 0);
      group.add(earth);

      const moonMat = new THREE.MeshStandardMaterial({
        color: 0x3a0a0a,
        emissive: 0x5a1010,
        emissiveIntensity: 0.7,
      });
      const moon = new THREE.Mesh(smallSphereGeo, moonMat);
      moon.position.set(2.5, 0, -0.5);
      group.add(moon);

      extraAnimate = () => {
        moon.rotation.y += 0.01;
        earth.rotation.y += 0.008;
      };
    } else if (mode === "TRANSIT") {
      const starMat = new THREE.MeshStandardMaterial({
        color: 0xffe4b3,
        emissive: 0xfff7d0,
        emissiveIntensity: 1.3,
      });
      const star = new THREE.Mesh(bigSphereGeo, starMat);
      group.add(star);

      const planetMat = new THREE.MeshStandardMaterial({ color: 0x1476ff });
      const planet = new THREE.Mesh(smallSphereGeo, planetMat);
      planet.scale.setScalar(0.5);
      planet.position.set(-6, -0.8, 3);
      group.add(planet);

      extraAnimate = () => {
        planet.position.x += 0.04;
        if (planet.position.x > 6) planet.position.x = -6;
      };
    } else if (mode === "METEOR") {
      const planetMat = new THREE.MeshStandardMaterial({
        color: 0x323232,
        roughness: 0.9,
      });
      const planet = new THREE.Mesh(mediumSphereGeo, planetMat);
      planet.position.set(-1.5, -0.5, 0);
      group.add(planet);

      const meteorMat = new THREE.MeshStandardMaterial({
        color: 0xfff5e6,
        emissive: 0xffaa55,
        emissiveIntensity: 1.0,
      });
      const meteor = new THREE.Mesh(smallSphereGeo, meteorMat);
      meteor.scale.set(0.4, 0.4, 1.6);
      meteor.position.set(4, 3, 2);
      meteor.rotation.z = -0.6;
      group.add(meteor);

      extraAnimate = () => {
        meteor.position.x -= 0.12;
        meteor.position.y -= 0.09;
        if (meteor.position.x < -6 || meteor.position.y < -4) {
          meteor.position.set(4, 3, 2);
        }
        planet.rotation.y += 0.005;
      };
    } else if (mode === "COMET") {
      const starMat = new THREE.MeshStandardMaterial({
        color: 0x111122,
        emissive: 0x222244,
        emissiveIntensity: 0.4,
      });
      const star = new THREE.Mesh(bigSphereGeo, starMat);
      star.scale.setScalar(0.6);
      star.position.set(-2.5, 0, 0);
      group.add(star);

      const cometMat = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        emissive: 0x88d5ff,
        emissiveIntensity: 1.2,
      });
      const comet = new THREE.Mesh(smallSphereGeo, cometMat);
      comet.scale.set(0.5, 0.5, 1.8);
      comet.position.set(5, -3, 3);
      comet.rotation.z = 0.4;
      group.add(comet);

      extraAnimate = () => {
        comet.position.x -= 0.08;
        comet.position.y += 0.05;
        if (comet.position.x < -6 || comet.position.y > 4) {
          comet.position.set(5, -3, 3);
        }
        star.rotation.y += 0.01;
      };
    } else if (mode === "ASTEROID") {
      const planetMat = new THREE.MeshStandardMaterial({
        color: 0x204a36,
        roughness: 0.7,
      });
      const planet = new THREE.Mesh(mediumSphereGeo, planetMat);
      planet.position.set(0, 0, 0);
      group.add(planet);

      const asteroidMat = new THREE.MeshStandardMaterial({
        color: 0x9b7b57,
        roughness: 0.9,
      });
      const asteroid = new THREE.Mesh(smallSphereGeo, asteroidMat);
      asteroid.scale.set(0.5, 0.8, 0.5);
      asteroid.position.set(5, 0, 0);
      group.add(asteroid);

      extraAnimate = () => {
        asteroid.position.x -= 0.07;
        asteroid.position.y = Math.sin(asteroid.position.x * 0.5) * 0.6;
        asteroid.rotation.y += 0.07;
        if (asteroid.position.x < -5) asteroid.position.x = 5;
        planet.rotation.y += 0.005;
      };
    } else if (mode === "ALIGNMENT") {
      const leftMat = new THREE.MeshStandardMaterial({ color: 0x3a8ddf });
      const midMat = new THREE.MeshStandardMaterial({
        color: 0xffe0a0,
        emissive: 0xfff0c8,
        emissiveIntensity: 0.9,
      });
      const rightMat = new THREE.MeshStandardMaterial({ color: 0xd45b10 });

      const left = new THREE.Mesh(smallSphereGeo, leftMat);
      const mid = new THREE.Mesh(mediumSphereGeo, midMat);
      const right = new THREE.Mesh(smallSphereGeo, rightMat);

      left.position.set(-3.5, 0, 0);
      mid.position.set(0, 0, 0);
      right.position.set(3.5, 0, 0);

      group.add(left, mid, right);

      extraAnimate = () => {
        group.rotation.z = Math.sin(Date.now() * 0.0003) * 0.3;
        group.rotation.y += 0.004;
      };
    } else if (mode === "SEASONAL") {
      const earthMat = new THREE.MeshStandardMaterial({
        color: 0x2a7bb6,
        roughness: 0.6,
      });
      const earth = new THREE.Mesh(mediumSphereGeo, earthMat);
      group.add(earth);

      const ringGeo = new THREE.RingGeometry(4, 4.15, 64);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0xffa64d,
        side: THREE.DoubleSide,
      });
      const ring = new THREE.Mesh(ringGeo, ringMat);
      ring.rotation.x = Math.PI / 2.5;
      group.add(ring);

      extraAnimate = () => {
        earth.rotation.y += 0.01;
        ring.rotation.z += 0.0025;
      };
    } else if (mode === "OCCULTATION") {
      const starMat = new THREE.MeshStandardMaterial({
        color: 0xfff5d1,
        emissive: 0xfff4b0,
        emissiveIntensity: 1.1,
      });
      const star = new THREE.Mesh(mediumSphereGeo, starMat);
      group.add(star);

      const foregroundMat = new THREE.MeshStandardMaterial({
        color: 0x101018,
      });
      const foreground = new THREE.Mesh(mediumSphereGeo, foregroundMat);
      foreground.position.set(-5, 0, 1);
      foreground.scale.setScalar(1.2);
      group.add(foreground);

      extraAnimate = () => {
        foreground.position.x += 0.05;
        if (foreground.position.x > 5) foreground.position.x = -5;
      };
    } else {
      const bodyMat = new THREE.MeshStandardMaterial({
        color: 0x444444,
        roughness: 0.8,
      });
      const body = new THREE.Mesh(mediumSphereGeo, bodyMat);
      group.add(body);

      extraAnimate = () => {
        body.rotation.y += 0.01;
      };
    }

    let frameId;
    const animate = () => {
      extraAnimate();
      renderer.render(scene, camera);
      frameId = requestAnimationFrame(animate);
    };
    animate();

    const handleResize = () => {
      if (!mountRef.current) return;
      const w = mountRef.current.clientWidth;
      const h = mountRef.current.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelAnimationFrame(frameId);
      window.removeEventListener("resize", handleResize);

      renderer.dispose();

      // 🔐 Safe: check container + parent before removing
      const container = mountRef.current;
      if (container && renderer.domElement.parentNode === container) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [mode]);

  const title =
    event?.name || event?.event_name || event?.type || `Event ${eventId || ""}`;
  const typelabel =
    event?.type || event?.event_type || event?.event_name || "Unknown type";
  const timeLabel =
    event?.time || event?.timestamp || event?.start_time || event?.date || null;

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#000",
        color: "#fff",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          padding: "12px 20px",
          borderBottom: "1px solid #333",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          background: "#050505",
        }}
      >
        <div>
          <div style={{ fontSize: 18, fontWeight: 600 }}>{title}</div>
          <div style={{ fontSize: 12, color: "#ffb873", marginTop: 2 }}>
            {typelabel} · visualization mode: {mode}
          </div>
          {timeLabel && (
            <div style={{ fontSize: 12, color: "#ccc", marginTop: 2 }}>
              Time:{" "}
              {typeof timeLabel === "number"
                ? new Date(timeLabel * 1000).toString()
                : String(timeLabel)}
            </div>
          )}
        </div>
        <button
          onClick={() => navigate(-1)}
          style={{
            padding: "6px 12px",
            borderRadius: 999,
            background: "#ff8c32",
            border: "none",
            color: "#000",
            fontSize: 12,
            fontWeight: 600,
            cursor: "pointer",
          }}
        >
          ← Back to results
        </button>
      </div>

      <div
        ref={mountRef}
        style={{
          flex: 1,
          width: "100%",
          position: "relative",
        }}
      />
    </div>
  );
}

