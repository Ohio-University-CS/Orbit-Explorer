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