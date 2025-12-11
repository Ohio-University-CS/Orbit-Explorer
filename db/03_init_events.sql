CREATE TABLE IF NOT EXISTS celestial_events (
    id SERIAL PRIMARY KEY,
    type_id INT NOT NULL REFERENCES celestial_event_types(id),
    name TEXT NOT NULL,
    event_time TIMESTAMPTZ NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    elevation DOUBLE PRECISION DEFAULT 0,
    description TEXT
);

DELETE FROM celestial_events;

INSERT INTO celestial_events (type_id, name, event_time, latitude, longitude, elevation, description)
VALUES
(
    (SELECT id FROM celestial_event_types WHERE event_name = 'OCCULTATION'),
    'Bright star occultation',
    '2025-12-08 00:46:00+00',
    35.0, 34.0, 0.0,
    'Example occultation visible near lat 35, lon 34.'
);

INSERT INTO celestial_events (type_id, name, event_time, latitude, longitude, elevation, description)
VALUES
(
    (SELECT id FROM celestial_event_types WHERE event_name = 'TRANSIT'),
    'Example transit',
    '2025-12-08 01:10:00+00',
    35.0, 34.0, 0.0,
    'Example transit event near the same region.'
);

INSERT INTO celestial_events (type_id, name, event_time, latitude, longitude, elevation, description)
VALUES
(
    (SELECT id FROM celestial_event_types WHERE event_name = 'ASTEROID_FLYBY'),
    'Near-Earth asteroid flyby',
    '2025-12-08 01:50:00+00',
    51.5, -0.1, 0.0,
    'Example asteroid flyby visible near London.'
);

INSERT INTO celestial_events (type_id, name, event_time, latitude, longitude, elevation, description)
VALUES
(
    (SELECT id FROM celestial_event_types WHERE event_name = 'METEOR'),
    'Meteor shower peak',
    '2025-12-08 01:20:00+00',
    40.0, -105.0, 0.0,
    'Example meteor shower visible over Colorado.'
);

INSERT INTO celestial_events (type_id, name, event_time, latitude, longitude, elevation, description)
VALUES
(
    (SELECT id FROM celestial_event_types WHERE event_name = 'COMET_APPEARANCE'),
    'Bright comet at perihelion',
    '2025-12-08 01:30:00+00',
    -33.9, 151.2, 0.0,
    'Example comet appearance near Sydney.'
);
