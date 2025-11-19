/*
Solar Storms:

SOLAR_FLARE: A sudden burst of energy from the Sun, typically associated with sunspots.

CORONAL_MASS_EJECTION (CME): Large expulsions of plasma and magnetic field from the Sun’s corona.

Other Planetary Events:

MERCURY_TRANSIT: A rare event when Mercury passes directly between Earth and the Sun.

VENUS_TRANSIT: A rare event when Venus passes directly between Earth and the Sun (last occurred in 2012, next one in 2117).

Tidal Events:

TIDAL_LOCKING: The process where a moon orbits a planet in such a way that it shows the same face to the planet at all times.

Astronomical Units (AU) and Perihelion/Aphelion:

PERIHELION: The point at which a planet is closest to the Sun.

APHELION: The point at which a planet is farthest from the Sun.

Astrophysical Events:

SUPERNOVA: The explosion of a star, often resulting in a burst of radiation.

BLACK_HOLE: Could refer to significant observations, like the discovery or merger of black holes.

NEUTRON_STAR: The formation of neutron stars or neutron star collisions.


*/


-- ------------------------------
-- 1. Eclipses
-- ------------------------------

-- Insert LUNAR_ECLIPSE and its subtypes
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('LUNAR_ECLIPSE', NULL),
    ('PENUMBRAL', (SELECT id FROM celestial_event_types WHERE event_name = 'LUNAR_ECLIPSE')),
    ('PARTIAL', (SELECT id FROM celestial_event_types WHERE event_name = 'LUNAR_ECLIPSE')),
    ('TOTAL', (SELECT id FROM celestial_event_types WHERE event_name = 'LUNAR_ECLIPSE')),
    ('CENTRAL', (SELECT id FROM celestial_event_types WHERE event_name = 'LUNAR_ECLIPSE')),
    ('SELENELION', (SELECT id FROM celestial_event_types WHERE event_name = 'LUNAR_ECLIPSE'));

-- Insert SOLAR_ECLIPSE and its subtypes
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('SOLAR_ECLIPSE', NULL),
    ('PARTIAL', (SELECT id FROM celestial_event_types WHERE event_name = 'SOLAR_ECLIPSE')),
    ('TOTAL', (SELECT id FROM celestial_event_types WHERE event_name = 'SOLAR_ECLIPSE')),
    ('ANNULAR', (SELECT id FROM celestial_event_types WHERE event_name = 'SOLAR_ECLIPSE')),
    ('HYBRID', (SELECT id FROM celestial_event_types WHERE event_name = 'SOLAR_ECLIPSE'));

-- ------------------------------
-- 2. Celestial Alignments
-- ------------------------------

-- Insert SYZYGY and its subtypes
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('SYZYGY', NULL),
    ('PERIGEE_SYZYGY', (SELECT id FROM celestial_event_types WHERE event_name = 'SYZYGY')),
    ('OPPOSITION', (SELECT id FROM celestial_event_types WHERE event_name = 'SYZYGY')),
    ('CONJUNCTION', (SELECT id FROM celestial_event_types WHERE event_name = 'SYZYGY')),
    ('QUADRATURE', (SELECT id FROM celestial_event_types WHERE event_name = 'SYZYGY'));

-- ------------------------------
-- 3. Planetary Motion
-- ------------------------------

-- Insert RETROGRADE_MOTION
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('RETROGRADE_MOTION', NULL);

-- ------------------------------
-- 4. Small Bodies
-- ------------------------------

-- Insert METEOR and its subtypes
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('METEOR', NULL),
    ('SHOWER', (SELECT id FROM celestial_event_types WHERE event_name = 'METEOR')),
    ('OUTBURST', (SELECT id FROM celestial_event_types WHERE event_name = 'METEOR'));

-- Insert COMET
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('COMET_APPEARANCE', NULL);

-- Insert ASTEROID
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('ASTEROID_FLYBY', NULL);

-- ------------------------------
-- 5. Transits / Occultations
-- ------------------------------

-- Insert TRANSIT and OCCULTATION
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('TRANSIT', NULL),
    ('OCCULTATION', NULL);

-- ------------------------------
-- 6. Seasonal / Solar Events
-- ------------------------------

-- Insert SEASONAL and its subtypes
INSERT INTO celestial_event_types (event_name, parent_id) VALUES
    ('SEASONAL', NULL),
    ('EQUINOX', (SELECT id FROM celestial_event_types WHERE event_name = 'SEASONAL')),
    ('SOLSTICE', (SELECT id FROM celestial_event_types WHERE event_name = 'SEASONAL'));