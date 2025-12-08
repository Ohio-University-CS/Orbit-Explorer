# utils.py

from skyfield.api import load
from app.schemas.location import GeodeticLocation

planets = load('de421.bsp')
earth = planets['earth']

def get_body_info(name: str):
    """
    Return right ascension, declination, and distance
    for a solar system body using Skyfield.
    """
    name = name.lower()

    if name not in planets:
        return None

    ts = load.timescale()
    t = ts.now()
    body = planets[name]

    astrometric = earth.observe(body).apparent()
    ra, dec, distance = astrometric.radec()

    return {
        "name": name.capitalize(),
        "right_ascension_hours": ra.hours,
        "declination_degrees": dec.degrees,
        "distance_au": distance.au,
        "distance_km": distance.km,
        "datetime": t.utc_strftime('%Y-%m-%d %H:%M:%S UTC')
    }
