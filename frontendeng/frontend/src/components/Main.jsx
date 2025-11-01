import React from 'react'
import videoBg from '../assets/OrbitExplorerr.mp4';

const Main = () => {
    return (
        <div
            style={{
                position: 'relative',
                height: '100vh',
                width: '100%',
                overflow: 'hidden'
            }}
            >
                <video 
                src={videoBg}
                autoPlay 
                loop 
                muted 
                playsInline 
                style={{
                    position: 'absolute',
                    inset: 0,
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    transform: 'translateZ(0)',
                    zIndex: -1
                }}
                />
            </div>
    );
};

export default Main;