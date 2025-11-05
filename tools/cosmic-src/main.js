import './style.css';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

import spaceURL from './galaxy.jpg';
import earthURL from './earth.jpg';
import moonURL from './moon.jpg';
import marsURL from './mars.jpg';
// add any others you use:

// Setup

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector('#bg'),
});

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.setZ(30);
camera.position.setX(-3);

renderer.render(scene, camera);

// Torus

// Saturn sphere (same size & position as before)
const saturnTexture = new THREE.TextureLoader().load(marsURL);
const geometry = new THREE.SphereGeometry(10, 64, 64);
const material = new THREE.MeshStandardMaterial({
  map: saturnTexture,
});
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);


// Lights

const pointLight = new THREE.PointLight(0xffffff);
pointLight.position.set(5, 5, 5);

const ambientLight = new THREE.AmbientLight(0xffffff);
scene.add(pointLight, ambientLight);

// Helpers

// const lightHelper = new THREE.PointLightHelper(pointLight)
// const gridHelper = new THREE.GridHelper(200, 50);
// scene.add(lightHelper, gridHelper)

// const controls = new OrbitControls(camera, renderer.domElement);

function addStar() {
  const geometry = new THREE.SphereGeometry(0.25, 24, 24);
  const material = new THREE.MeshStandardMaterial({ color: 0xffffff });
  const star = new THREE.Mesh(geometry, material);

  const [x, y, z] = Array(3)
    .fill()
    .map(() => THREE.MathUtils.randFloatSpread(100));

  star.position.set(x, y, z);
  scene.add(star);
}

Array(200).fill().forEach(addStar);

// Background

const spaceTexture = new THREE.TextureLoader().load(spaceURL);
scene.background = spaceTexture;

// Avatar

const jeffTexture = new THREE.TextureLoader().load('earth.jpg');

const jeff = new THREE.Mesh(new THREE.SphereGeometry(3, 3, 3), new THREE.MeshBasicMaterial({ map: jeffTexture }));

scene.add(jeff);

// Moon

const moonTexture = new THREE.TextureLoader().load(moonURL);

const moon = new THREE.Mesh(
  new THREE.SphereGeometry(3, 32, 32),
  new THREE.MeshStandardMaterial({
    map: moonTexture,
  })
);

scene.add(moon);

moon.position.z = 30;
moon.position.setX(-10);

jeff.position.z = -5;
jeff.position.x = 2;

// Replace the "jeff" cube with an Earth sphere in-place (same size & position)
(() => {
  // The cube was BoxGeometry(3,3,3) → sphere radius should be half the side (1.5),
  // scaled by the current mesh scale to preserve visual size.
  const side = 3 * jeff.scale.x;        // assumes uniform scaling
  const radius = side / 2;

  const earthTex = new THREE.TextureLoader().load(earthURL);
  const newGeom = new THREE.SphereGeometry(radius, 64, 64);
  const newMat  = new THREE.MeshStandardMaterial({ map: earthTex });

  // Clean up old resources, then swap
  jeff.geometry.dispose();
  jeff.material.dispose();
  jeff.geometry = newGeom;
  jeff.material = newMat;
})();


// Scroll Animation

function moveCamera() {
  const t = document.body.getBoundingClientRect().top;
  moon.rotation.x += 0.05;
  moon.rotation.y += 0.075;
  moon.rotation.z += 0.05;

  jeff.rotation.y += 0.01;
  jeff.rotation.z += 0.01;

  camera.position.z = t * -0.01;
  camera.position.x = t * -0.0002;
  camera.rotation.y = t * -0.0002;
}

document.body.onscroll = moveCamera;
moveCamera();

// Animation Loop

function animate() {
  requestAnimationFrame(animate);

  sphere.rotation.x += 0.01;
  sphere.rotation.y += 0.005;
  sphere.rotation.z += 0.01;

  moon.rotation.x += 0.005;

  // controls.update();

  renderer.render(scene, camera);
}

// ===== Local Time & Timezone (Projects -> Time) =====
function updateLocalTime() {
  const timeEl = document.getElementById('localTime');
  const zoneEl = document.getElementById('localZone');
  if (!timeEl || !zoneEl) return;

  // User's IANA timezone from their computer (e.g., "America/New_York")
  const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Local Time';

  // Show time as HH:MM:SS with a timezone abbreviation if available
  const now = new Date();
  const timeFmt = new Intl.DateTimeFormat([], {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  // Try to get a short name like "EST"/"EDT" or "GMT-4"
  // Note: Some browsers show "GMT-4" instead of "EST/EDT"—that's OK.
  const tzNameFmt = new Intl.DateTimeFormat([], {
    timeZoneName: 'short',
  });
  const tzName = tzNameFmt.formatToParts(now).find(p => p.type === 'timeZoneName')?.value || '';

  timeEl.textContent = timeFmt.format(now);
  zoneEl.textContent = `${tz} ${tzName ? `(${tzName})` : ''}`;
}

// Start and keep ticking each second
updateLocalTime();
setInterval(updateLocalTime, 1000);

// Temperature form behavior
const tempForm = document.getElementById('tempForm');
const tempOutput = document.getElementById('tempOutput');

if (tempForm) {
  tempForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const tempValue = document.getElementById('temperature').value;
    const unit = document.getElementById('unit').value;
    tempOutput.textContent = `You entered: ${tempValue}°${unit}`;
  });
}


animate();