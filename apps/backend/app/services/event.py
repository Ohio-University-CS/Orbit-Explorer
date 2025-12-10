#replaced by spice_events for now, nvm using both
import json

from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime, timedelta
from functools import partial

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria
from app.schemas.location import GeodeticLocation

import psycopg2
from psycopg2 import errors


from skyfield.magnitudelib import planetary_magnitude
from skyfield.api import load, wgs84
from skyfield.searchlib import find_discrete
from skyfield.toposlib import Topos
from skyfield import almanac

from skyfield.data import mpc
from skyfield.constants import AU_KM

import spiceypy as spice
import numpy as np


# Database connection function
def get_conn():
    return psycopg2.connect(
        host="db",
        port=5432,
        database="orbit_explorer",
        user="postgres",
        password="123456",
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


def is_body_up(ephemeris, target, latitude_deg, longitude_deg, elevation_m=0,
               horizon_degrees=-0.5666666666666667, radius_degrees=0):
    """
    Returns a function that takes a Skyfield Time object and returns True if
    the target body is above the horizon at that time, False otherwise.
    
    Parameters:
        ephemeris      - Skyfield ephemeris object
        target         - target body (planet, Sun, Moon, star)
        latitude_deg   - observer latitude in degrees
        longitude_deg  - observer longitude in degrees
        elevation_m    - observer elevation in meters
        horizon_degrees - altitude in degrees of horizon (default: -0.5667 for Sun)
        radius_degrees - apparent radius of the object (default: 0)
    
    Returns:
        function(time) -> bool
    """
    # Observer location
    topos = wgs84.latlon(latitude_deg, longitude_deg, elevation_m)

    # Build the "body up" function using Skyfield's almanac
    body_up_fn = almanac.risings_and_settings(
        ephemeris,
        target,
        topos,
        horizon_degrees=horizon_degrees,
        radius_degrees=radius_degrees
    )

    def check(time):
        """Return True if body is up at given Skyfield Time object"""
        return body_up_fn(time)

    return check

def get_planet_visibility(observer_lat, observer_lon, observer_elevation_m,
                          start_time, end_time, time_step_minutes=30,
                          planets=None):
    """
    Compute planet visibility (magnitude) for an observer on Earth.
    Returns list of dicts: [{planet: name, data: [{time_utc, magnitude}]}]
    Only native Python types returned.
    """

    if planets is None:
        planets = ['mercury', 'venus', 'mars', 'jupiter barycenter',
                   'saturn barycenter', 'uranus barycenter', 'neptune barycenter']

    ts = load.timescale()
    eph = load('de421.bsp')
    earth = eph['earth']

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
            # Geocentric magnitude (from Earth center)
            astrometric_geo = earth.at(t).observe(target)
            mag = float(planetary_magnitude(astrometric_geo))  # convert numpy.float64 → float

            planet_data.append({
                'time_utc': t.utc_iso(),
                'magnitude': mag
            })

        results.append({
            'planet': planet_name,
            'data': planet_data
        })

    return results

def get_planets():
    """
    Returns basic info for major planets using fixed NAIF IDs.
    """
    return [
        {'naif_id': 199, 'name': 'Mercury', 'desc': 'Innermost planet'},
        {'naif_id': 299, 'name': 'Venus', 'desc': 'Second planet from the Sun'},
        {'naif_id': 399, 'name': 'Earth', 'desc': 'Our home planet'},
        {'naif_id': 499, 'name': 'Mars', 'desc': 'Red planet'},
        {'naif_id': 5,   'name': 'Jupiter', 'desc': 'Gas giant'},
        {'naif_id': 6,   'name': 'Saturn', 'desc': 'Gas giant with rings'},
        {'naif_id': 7,   'name': 'Uranus', 'desc': 'Ice giant'},
        {'naif_id': 8,   'name': 'Neptune', 'desc': 'Ice giant'},
        {'naif_id': 9,   'name': 'Pluto', 'desc': 'Dwarf planet'},
    ]


def get_moons():
    """
    Returns NAIF IDs for major moons. Does not use Skyfield lookups.
    """
    moons = []

    # Earth
    moons.append({'naif_id': 301, 'name': 'Moon', 'planet': 'Earth', 'desc': "Earth's natural satellite"})

    # Mars
    moons.append({'naif_id': 401, 'name': 'Phobos', 'planet': 'Mars', 'desc': "Innermost moon of Mars"})
    moons.append({'naif_id': 402, 'name': 'Deimos', 'planet': 'Mars', 'desc': "Outer moon of Mars"})

    # Jupiter
    moons.extend([
        {'naif_id': 501, 'name': 'Io', 'planet': 'Jupiter', 'desc': 'Moon of Jupiter'},
        {'naif_id': 502, 'name': 'Europa', 'planet': 'Jupiter', 'desc': 'Moon of Jupiter'},
        {'naif_id': 503, 'name': 'Ganymede', 'planet': 'Jupiter', 'desc': 'Moon of Jupiter'},
        {'naif_id': 504, 'name': 'Callisto', 'planet': 'Jupiter', 'desc': 'Moon of Jupiter'},
    ])

    # Saturn
    moons.extend([
        {'naif_id': 601, 'name': 'Mimas', 'planet': 'Saturn', 'desc': 'Moon of Saturn'},
        {'naif_id': 602, 'name': 'Enceladus', 'planet': 'Saturn', 'desc': 'Moon of Saturn'},
        {'naif_id': 603, 'name': 'Tethys', 'planet': 'Saturn', 'desc': 'Moon of Saturn'},
        {'naif_id': 604, 'name': 'Dione', 'planet': 'Saturn', 'desc': 'Moon of Saturn'},
        {'naif_id': 605, 'name': 'Rhea', 'planet': 'Saturn', 'desc': 'Moon of Saturn'},
        {'naif_id': 606, 'name': 'Titan', 'planet': 'Saturn', 'desc': 'Moon of Saturn'},
        {'naif_id': 608, 'name': 'Iapetus', 'planet': 'Saturn', 'desc': 'Moon of Saturn'},
    ])

    # Uranus
    moons.extend([
        {'naif_id': 701, 'name': 'Miranda', 'planet': 'Uranus', 'desc': 'Moon of Uranus'},
        {'naif_id': 702, 'name': 'Ariel', 'planet': 'Uranus', 'desc': 'Moon of Uranus'},
        {'naif_id': 703, 'name': 'Umbriel', 'planet': 'Uranus', 'desc': 'Moon of Uranus'},
        {'naif_id': 704, 'name': 'Titania', 'planet': 'Uranus', 'desc': 'Moon of Uranus'},
        {'naif_id': 705, 'name': 'Oberon', 'planet': 'Uranus', 'desc': 'Moon of Uranus'},
    ])

    # Neptune
    moons.extend([
        {'naif_id': 801, 'name': 'Triton', 'planet': 'Neptune', 'desc': 'Moon of Neptune'},
        {'naif_id': 802, 'name': 'Nereid', 'planet': 'Neptune', 'desc': 'Moon of Neptune'},
    ])

    return moons


def get_asteroids():
    """
    Returns a small sample of known asteroids.
    """
    asteroids = [
        {'naif_id': 2000001, 'name': 'Ceres', 'desc': 'Largest asteroid / dwarf planet'},
        {'naif_id': 2000002, 'name': 'Pallas', 'desc': 'Second largest asteroid'},
        {'naif_id': 2000004, 'name': 'Vesta', 'desc': 'Third largest asteroid'},
        {'naif_id': 2000007, 'name': 'Hygiea', 'desc': 'Fourth largest asteroid'},
    ]
    return asteroids