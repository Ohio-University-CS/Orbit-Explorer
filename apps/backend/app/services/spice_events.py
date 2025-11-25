from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from functools import partial

from app.schemas.event_item import EventItem
from app.schemas.event_criteria import EventCriteria

from app.schemas.location import GeodeticLocation

import psycopg2

import spiceypy as sp
import numpy as np

def datetime_to_utc_string(dt: datetime) -> str:
    """
    Convert a datetime.datetime object to a CSPICE-compatible UTC string.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime.datetime, got {type(dt)}")
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def find_occultations(observer_spk, observer_id, target, occulter, start_utc, end_utc):
    """
    Find all occultations of a target by an occulter from a topocentric observer.

    Parameters
    ----------
    observer_spk : str
        Filename of the observer SPK.
    observer_id : int
        NAIF ID of the observer in the SPK.
    target : str
        Name of the target body (e.g., "SUN").
    occulter : str
        Name of the occulting body (e.g., "MOON").
    start_utc : str
        Start UTC time (e.g., "2026-09-24T00:00:00").
    end_utc : str
        End UTC time (e.g., "2026-09-25T00:00:00").

    Returns
    -------
    occultation_events : list of tuples
        Each tuple is (start_utc, end_utc) of an occultation.
    """

    # Load kernels
    sp.furnsh(observer_spk)        # Observer SPK
    sp.furnsh('app/kernels/de442s.bsp')  # Planetary ephemeris
    sp.furnsh('app/kernels/pck_00011.tpc')  # Planet constants
    sp.furnsh('app/kernels/naif0012.tls')   # Leap seconds

    # Convert UTC to ET
    et_start = sp.str2et(start_utc)
    et_end   = sp.str2et(end_utc)

    # Create a confinement window
    cnfine = sp.cell_double(2)
    sp.wninsd(et_start, et_end, cnfine)

    # Output window for occultation intervals
    result_window = sp.cell_double(2000)  # large enough

    # Find occultations
    sp.gfoclt('ANY', target, 'ellipsoid', occulter, 'ellipsoid',
              observer_id, 'J2000', 'NONE', cnfine, 100.0, result_window)

    # Extract start/end times
    occultation_events = []
    for i in range(0, sp.wncard(result_window), 2):
        et0 = sp.wnfetd(result_window, i)[0]
        et1 = sp.wnfetd(result_window, i+1)[0]
        utc0 = sp.et2utc(et0, 'C', 3)
        utc1 = sp.et2utc(et1, 'C', 3)
        occultation_events.append((utc0, utc1))

    # Clean up
    sp.kclear()

    return occultation_events

def create_observer_spk(lat_deg, lon_deg, alt_km, start_utc, end_utc, spk_filename, observer_id=-999):
    """
    Create a tiny SPK file for a fixed observer on Earth.

    Parameters
    ----------
    lat_deg : float
        Observer latitude in degrees.
    lon_deg : float
        Observer longitude in degrees.
    alt_km : float
        Observer altitude above mean sea level (km).
    start_utc : str
        Start UTC string (e.g., "2026-09-24T00:00:00").
    end_utc : str
        End UTC string (e.g., "2026-09-24T01:00:00").
    spk_filename : str
        Output SPK filename.
    observer_id : int, optional
        NAIF ID for the observer, by default -999.

    Returns
    -------
    None
    """

    # Load necessary kernels
    sp.furnsh('app/kernels/de442s.bsp')  # planetary ephemeris
    sp.furnsh('app/kernels/pck_00011.tpc')  # planetary constants
    sp.furnsh('app/kernels/naif0012.tls')   # leap seconds

    # Get Earth's radii
    radii = sp.bodvrd('EARTH', 'RADII', 3)
    re, _, rp = radii[1]

    # Convert observer geodetic to rectangular J2000 coordinates
    obs_xyz = sp.georec(
        np.radians(lon_deg),
        np.radians(lat_deg),
        alt_km,
        re,
        (re - rp)/re
    )

    # Convert UTC to ephemeris times
    et_start = sp.str2et(start_utc)
    et_end   = sp.str2et(end_utc)

    # Open a new SPK file
    handle = sp.spkopn(spk_filename, 'Observer SPK', 0)

    # Create a single-state Chebyshev segment
    # For a fixed observer, velocity is zero in J2000
    state = np.array(obs_xyz.tolist() + [0.0, 0.0, 0.0])
    states = state.reshape((1,6))  # 1 row, 6 columns
    epochs = np.array([et_start])

    # state = [x, y, z, 0,0,0]
    state = np.array(obs_xyz.tolist() + [0.0, 0.0, 0.0])
    step = 1.0  # any nonzero value, won't matter for single-state
    sp.spkw08(handle,
            observer_id,  # user-defined observer
            399,          # Earth
            'J2000',
            et_start,
            et_end,
            'ObserverSegment',
            1,            # Chebyshev degree 1 for fixed
            state,
            et_start,     # epoch1
            1.0)         # step size
    # Close the SPK
    sp.spkcls(handle)

    print(f"SPK created: {spk_filename} for observer ID {observer_id}")

def spice_get_occultations(location, start_dt: datetime, end_dt: datetime, step_sec=60, N=36):
    sp.furnsh('app/kernels/de442s.bsp')
    sp.furnsh('app/kernels/pck_00011.tpc')
    sp.furnsh('app/kernels/naif0012.tls')

    lat_deg = 39.3244
    lon_deg = -82.1014
    alt_km = 0.02

    # Earth's radii
    re, _, rp = sp.bodvrd('EARTH', 'RADII', 3)[1]
    obs_xyz = sp.georec(np.radians(lon_deg),
                        np.radians(lat_deg),
                        alt_km,
                        re, (re - rp)/re)


    start_utc = datetime_to_utc_string(start_dt)
    end_utc   = datetime_to_utc_string(end_dt)

    et_start = sp.str2et(start_utc)
    et_end = sp.str2et(end_utc)
    times = np.arange(et_start, et_end, step_sec)

    target = 'SUN'
    occulting = 'MOON'

    target_radii = sp.bodvrd(target, 'RADII', 3)[1]
    occulting_radii = sp.bodvrd(occulting, 'RADII', 3)[1]

    occultation_events = []

    # Precompute limb angles
    theta = np.linspace(0, 2*np.pi, N, endpoint=False)
    
    # Limb offsets in target-centered frame (unit vectors)
    # ecentr = target position relative to geocenter, will update per et
    # smajor, sminor = semi-major/minor axes of limb ellipse (from edlimb)
    twopi = 2*np.pi

    for et in times:
        # Target/occulting state relative to geocenter
        obs_target_state = sp.spkezr(target, et, 'J2000', 'NONE', '399')[0][:3]
        obs_occulting_state = sp.spkezr(occulting, et, 'J2000', 'NONE', '399')[0][:3]

        # Vector from observer to target/occulting
        vec_target = obs_target_state - obs_xyz
        vec_occult = obs_occulting_state - obs_xyz

        # Limb ellipse of target
        limb = sp.edlimb(target_radii[0], target_radii[1], target_radii[2], obs_target_state)
        ecentr = limb.center
        smajor = limb.semi_major
        sminor = limb.semi_minor

        # All limb points in one array
        points = ecentr + np.outer(np.cos(theta), smajor) + np.outer(np.sin(theta), sminor)
        vectors = points - obs_xyz  # vectors from observer to limb points

        # Transform observer and vectors into occulting frame
        occulting_frame_name = f"IAU_{occulting}"
        xform = sp.pxform('J2000', occulting_frame_name, et)
        obspos_occulting = sp.mxv(xform, obs_xyz)
        vec_occulting = np.array([sp.mxv(xform, v) for v in vectors])

        # Surfpt for all limb points
        for i, v in enumerate(vec_occulting):
            try:
                # obspos_occulting: observer in body-fixed frame
                # v: line-of-sight vector in same frame
                ray_occulting_pt = sp.surfpt(
                    obspos_occulting, v,
                    occulting_radii[0], occulting_radii[1], occulting_radii[2]
                )
            except sp.utils.exceptions.NotFoundError:
                ray_occulting_pt = None  # no intersection

            if ray_occulting_pt is not None:
                # Intersection exists
                occultation_events.append((et, ray_occulting_pt))
            else:
                # No intersection; skip or log
                pass
    sp.kclear()
    return occultation_events

async def get_events(location: GeodeticLocation, start_time: datetime, end_time: datetime, whitelisted_event_types: List[str], event_specific_criteria: List[EventCriteria]) -> List[EventItem]:
    events = []
    
    occulations = spice_get_occultations(location, start_time, end_time)
    for idx, e in enumerate(occulations):
        events.append(EventItem(
            id=f"event_{idx:03d}"
        ))

    dummy_event = EventItem(
        id="event_001",
        type="solar_eclipse",
        name="Partial Solar Eclipse",
        time=start_time,
        desc=f"Dummy event at lat {location.lat}, lon {location.lon}"
    )

    return [dummy_event]

async def event_types():
    try:
        conn = get_conn()
        cur = conn.cursor()
        event_types_list = []

        cur.execute("SELECT id, parent_id, name FROM celestial_event_types")
        for row in cur.fetchall():
            id, parent_id, name = row
            event_types_list.append({
                "id": id,
                "parent_id": parent_id,
                "name": name
            })

        cur.close()
        conn.close()
        return event_types_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get event types: {e}")