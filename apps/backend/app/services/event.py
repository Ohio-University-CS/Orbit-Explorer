#replaced by spice_events for now


from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timedelta
from functools import partial

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria

from app.schemas.location import GeodeticLocation

import psycopg2


from skyfield.magnitudelib import planetary_magnitude
from skyfield.api import load, wgs84
from skyfield.searchlib import find_discrete
from skyfield.toposlib import Topos

import spiceypy as spice
import numpy as np

# Database connection function
def get_conn():
    return psycopg2.connect(
        host="db",
        port=5432,
        database="orbit_explorer",
        user="postgres",
        password="123456"
    )

def cartesian_to_altaz(x, y, z):
    """
    Convert Cartesian vector to altitude and azimuth in degrees.
    Assumes local horizon at the origin.
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    alt = np.arcsin(z / r)
    az = np.arctan2(y, x)
    return np.degrees(alt), np.degrees(az) % 360

def get_planet_visibility(observer_lat, observer_lon, observer_elevation_m,
                          start_time, end_time, time_step_minutes=30,
                          planets=None):
    """
    Compute brightness and topocentric visibility of planets from a specific Earth location,
    manually computing topocentric vectors as Earth center vector minus site vector.
    """
    if planets is None:
        planets = ['mercury', 'venus', 'mars', 'jupiter barycenter',
                   'saturn barycenter', 'uranus barycenter', 'neptune barycenter']

    ts = load.timescale()
    eph = load('de421.bsp')
    earth = eph['earth']

    # Create site object
    site = wgs84.latlon(observer_lat, observer_lon, elevation_m=observer_elevation_m)

    # Build time array
    times = []
    current_time = start_time
    while current_time <= end_time:
        times.append(ts.utc(current_time.year, current_time.month, current_time.day,
                            current_time.hour, current_time.minute, current_time.second))
        current_time += timedelta(minutes=time_step_minutes)

    results = []

    for planet_name in planets:
        target = eph[planet_name]
        planet_data = []

        for t in times:
            # ------------------------
            # Geocentric magnitude (from Earth center)
            # ------------------------
            astrometric_geo = earth.at(t).observe(target)
            mag = planetary_magnitude(astrometric_geo)

            # ------------------------
            # Topocentric vector manually
            # ------------------------
            target_vec = astrometric_geo.position.km  # np.array([x, y, z])
            site_vec = site.at(t).position.km         # np.array([x, y, z])
            topo_vec = target_vec - site_vec

            # Convert to alt/az
            alt_deg, az_deg = cartesian_to_altaz(*topo_vec)
            visible = alt_deg > 0

            planet_data.append({
                'time_utc': t.utc_iso(),
                'magnitude': mag,
                'altitude_deg': alt_deg,
                'azimuth_deg': az_deg,
                'visible': visible
            })

        results.append({'planet': planet_name, 'data': planet_data})

    return results