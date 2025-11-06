import React from 'react';
export default function CosmicFrame() {
  return (
    <div style={{ height: '100vh', width: '100vw', margin: 0, padding: 0 }}>
      <iframe title="Cosmic" src="/cosmic/index.html"
              style={{ border: 'none', width: '100%', height: '100%' }} />
    </div>
  );
}
