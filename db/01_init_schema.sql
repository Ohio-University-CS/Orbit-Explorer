CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    first_name TEXT,
    last_name TEXT,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uuid TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS celestial_event_types (
    id SERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    parent_id INT REFERENCES celestial_event_types(id),
    description TEXT
);

CREATE TABLE IF NOT EXISTS sites (
    id SERIAL PRIMARY KEY,              -- auto-increment integer
    guid CHAR(21) UNIQUE NOT NULL,      -- 21-character site ID / name
    lat DOUBLE PRECISION NOT NULL,      -- latitude in degrees
    lon DOUBLE PRECISION NOT NULL,      -- longitude in degrees
    alt_km DOUBLE PRECISION NOT NULL,   -- altitude in km
    site_name TEXT,                     -- optional human-readable name
    site_description TEXT,              -- optional description
    idcode INTEGER GENERATED ALWAYS AS IDENTITY (
        START WITH 399000
        INCREMENT BY 1
    ),
    UNIQUE (lat, lon, alt_km)           -- unique coordinates
);

CREATE TABLE IF NOT EXISTS bodies (
    id SERIAL PRIMARY KEY,
    naif_id TEXT UNIQUE NOT NULL,
    body_type TEXT NOT NULL CHECK (
        body_type IN ('planet', 'moon', 'asteroid', 'comet', 'spacecraft', 'site', 'barycenter')
    ),
    body_desc TEXT,
);