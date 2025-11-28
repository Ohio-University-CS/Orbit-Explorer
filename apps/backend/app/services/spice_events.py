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

import subprocess
import os
import uuid
import random
import string
from pathlib import Path
from enum import Enum
APP_ROOT = Path(__file__).resolve().parent.parent

# Database connection function
def get_conn():
    return psycopg2.connect(
        host="db",
        port=5432,
        database="orbit_explorer",
        user="postgres",
        password="123456"
    )

class KernelType(Enum):
    SPK = "spk"
    FK  = "fk"
    PCK = "pck"
    LSK = "lsk"
    DSK = "dsk"
    STAR = "star"

class ObjectType(Enum):
    SITE = "sites"
    COMET = "comets"
    ASTEROID = "asteroids"
    SPACECRAFT = "spacecraft"
    LAGRANGE_POINT = "lagrange_point"
    PLANET = "planets"
    SATELLITE = "satellites"
    STATION = "stations"
    TNO = "tno"

SPICE_ROOT = APP_ROOT / "spice"
SPICE_KERNELS_ROOT = SPICE_ROOT / "kernels"

# Map KernelType + ObjectType to paths
KERNEL_PATHS = {
    KernelType.SPK: {
        ObjectType.SITE: SPICE_KERNELS_ROOT /  "spk/sites",
        ObjectType.ASTEROID: SPICE_KERNELS_ROOT / "spk/asteroids",
        ObjectType.COMET: SPICE_KERNELS_ROOT / "spk/comets",
        ObjectType.LAGRANGE_POINT: SPICE_KERNELS_ROOT / "spk/lagrange_point",
        ObjectType.PLANET: SPICE_KERNELS_ROOT / "spk/planets",
        ObjectType.SATELLITE: SPICE_KERNELS_ROOT / "spk/satellites",
        ObjectType.STATION: SPICE_KERNELS_ROOT / "spk/stations",
        ObjectType.TNO: SPICE_KERNELS_ROOT / "spk/tno",
    },
    KernelType.FK: {
        ObjectType.SITE: SPICE_KERNELS_ROOT /  "fk/sites",
        ObjectType.STATION: SPICE_KERNELS_ROOT / "fk/stations",
        ObjectType.PLANET: SPICE_KERNELS_ROOT / "fk/planets",
        ObjectType.SATELLITE: SPICE_KERNELS_ROOT / "fk/satellites",
    },
    KernelType.DSK: {
        ObjectType.SITE: SPICE_KERNELS_ROOT /  "dsk/sites",
        ObjectType.STATION: SPICE_KERNELS_ROOT / "dsk/stations",
        ObjectType.PLANET: SPICE_KERNELS_ROOT / "dsk/planets",
        ObjectType.SATELLITE: SPICE_KERNELS_ROOT / "dsk/satellites",
    },
    KernelType.PCK: SPICE_KERNELS_ROOT / "pck",
    KernelType.LSK: SPICE_KERNELS_ROOT / "lsk",
    KernelType.STAR: SPICE_KERNELS_ROOT / "stars",
}

class SPICE_MISC_DIRS():
    TEMP = APP_ROOT / "spice/temp"

class SPICE_BINARIES:
    PINPOINT = SPICE_ROOT / "bin/PC_Linux_64bit/pinpoint"

def kernel_file(kernel_type: KernelType, object_type: ObjectType | None, file_name: str):
    """
    Build a full kernel file path using enums.
    """
    if kernel_type in [KernelType.PCK, KernelType.LSK]:
        return KERNEL_PATHS[kernel_type] / file_name
    
    if object_type is None:
        raise ValueError(f"Object type must be specified for {kernel_type}")
    
    folder = KERNEL_PATHS[kernel_type][object_type]
    return folder / file_name

def geodetic_to_xyz(location: GeodeticLocation):
    """
    Convert geodetic coordinates (WGS84) to Earth-centered, Earth-fixed XYZ in km.
    """
    pck_path    = APP_ROOT / "spice/kernels/pck/pck00011.tpc"
    sp.furnsh(str(pck_path))

    # Get Earth radii from kernel pool
    radii = sp.bodvrd("EARTH", "RADII", 3)[1]
    re = radii[0]
    rp = radii[2]

    # Compute flattening
    f = (re - rp) / re

    x, y, z = sp.georec(location.lon, location.lat, location.alt_km, re, f)
    return x, y, z

def generate_site_guid(length=21):
    # Ensure the first character is an uppercase letter
    first_char = random.choice(string.ascii_uppercase)
    
    # Generate uppercase hex for the remaining characters
    rest = uuid.uuid4().hex[:length-1].upper()
    
    return first_char + rest

def write_defs_file(s, output_file: Path):
    def fmt(x):
        return ("+" + str(x)) if x >= 0 else str(x)

    with output_file.open("w") as f:
        xyz = f"{fmt(s['x'])}, {fmt(s['y'])}, {fmt(s['z'])}"
        f.write(r"\begindata" + "\n\n")
        f.write(f"SITES = ( '{s['id']}' )\n\n")

        f.write(f"{s['id']}_CENTER = 399\n")
        f.write(f"{s['id']}_FRAME  = 'EARTH_FIXED'\n")
        f.write(f"{s['id']}_IDCODE = {s['idcode']}\n")
        f.write(f"{s['id']}_XYZ = ( {xyz} )\n")
        f.write(f"{s['id']}_BOUNDS = ( {s['bounds'][0]}, {s['bounds'][1]} )\n")
        f.write(f"{s['id']}_UP = 'Z'\n")
        f.write(f"{s['id']}_NORTH = 'X'\n\n")
    
        f.write(r"\begintext" + "\n")

def create_site_or_fetch(location: GeodeticLocation, conn: psycopg2.extensions.connection):
    guid = generate_site_guid(21)

    # ------------------------
    # Database insert/fetch
    # ------------------------
    sql = """
    INSERT INTO sites (guid, lat, lon, alt_km, site_name, site_description)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (lat, lon, alt_km) DO NOTHING
    RETURNING idcode;
    """
    with conn.cursor() as cur:
        cur.execute(sql, (guid, location.lat, location.lon, location.alt_km, None, None))
        row = cur.fetchone()
        if row:
            idcode = row[0]
        else:
            cur.execute("SELECT idcode, guid FROM sites WHERE lat=%s AND lon=%s AND alt_km=%s",
                        (location.lat, location.lon, location.alt_km))
            existing = cur.fetchone()
            if existing is None:
                raise RuntimeError("Site conflict but no existing row found")
            idcode, guid = existing
            return guid
        conn.commit()

    #mainly for testing, so it's seperate from database
    create_site_helper(guid, idcode, location)
    return guid

def create_site_helper(guid, idcode, location):
    # ------------------------
    # Build site object
    # ------------------------
    site = {
        "id": guid,
        "idcode": idcode,
        "bounds": ("@2025-JAN-01", "@2300-JAN-01")
    }
    site["x"], site["y"], site["z"] = geodetic_to_xyz(location)

    pinpoint_path = SPICE_BINARIES.PINPOINT
    
    pck_path = kernel_file(KernelType.PCK, None, "pck00011.tpc")

    # Write defs file
    defs_path = SPICE_MISC_DIRS.TEMP / f"{guid}.defs"
    write_defs_file(site, defs_path)

    output_spk = kernel_file(KernelType.SPK, ObjectType.SITE, f"{guid}.spk")
    output_fk  = kernel_file(KernelType.FK, ObjectType.SITE, f"{guid}.tf")

    if output_spk.exists():
        output_spk.unlink()

    if output_fk.exists():
        output_fk.unlink()

    cmd = [
        str(pinpoint_path),
        "-def", str(defs_path),
        "-pck", str(pck_path),
        "-spk", str(output_spk),
        "-fk", str(output_fk)
    ]

    try:
        # Let pinpoint print directly to terminal
        result = subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(">>> PINPOINT FAILED! Return code:", e.returncode)
        raise

    # ------------------------
    # Clean up temp defs file
    # ------------------------
    if defs_path.exists():
        defs_path.unlink()

def datetime_to_utc_string(dt: datetime) -> str:
    """
    Convert a datetime.datetime object to a CSPICE-compatible UTC string.
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime.datetime, got {type(dt)}")
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def handle_occultations(site_name: str, start_time, end_time):
    site_spk = kernel_file(KernelType.SPK, ObjectType.SITE, f"{site_name}.spk")
    site_fk = kernel_file(KernelType.FK, ObjectType.SITE, f"{site_name}.tf")

    occultations = find_occultations(
        "ANY",
        observer_spk=str(site_spk),
        observer_fk=str(site_fk),
        obsrvr=site_name,
        front='MOON',
        fframe='IAU_MOON',
        back='SUN',
        bframe='IAU_SUN',
        start_utc='2026-09-24T00:00:00',
        end_utc='2027-09-25T00:00:00'
    )

    return occultations

def find_occultations(occtyp, observer_spk, observer_fk, obsrvr , front, fframe, back, bframe, start_utc, end_utc):
    # Load SPKs

    lsk_loc = str(kernel_file(KernelType.LSK, None, "naif0012.tls.pc"))
    earth_loc = str(kernel_file(KernelType.PCK, None, "pck00011.tpc"))
    planets_loc = str(kernel_file(KernelType.SPK, ObjectType.PLANET, "de432s.bsp"))
    earth_fixed = str(kernel_file(KernelType.PCK, None, "earth_fixed.tf"))
    sp.furnsh(lsk_loc)
    sp.furnsh(earth_loc)
    sp.furnsh(earth_fixed)
    sp.furnsh(planets_loc)
    sp.furnsh(observer_spk)
    sp.furnsh(observer_fk)

    # Convert UTC to ephemeris seconds past J2000
    et_start = sp.str2et(start_utc)
    et_end   = sp.str2et(end_utc)
    
    # Create confinement window
    cnfine = sp.utils.support_types.SPICEDOUBLE_CELL(2)
    sp.wninsd(et_start, et_end, cnfine)

    # Result window
    result = sp.utils.support_types.SPICEDOUBLE_CELL(1000)  # max 500 intervals (start/end pairs)
    
    # Call the occultation finder
    sp.gfoclt(
        occtyp,
        front,
        'ELLIPSOID',
        fframe,
        back,
        'ELLIPSOID',
        bframe,
        'LT',
        obsrvr,
        60.0,
        cnfine,
        result
    )

    # Extract intervals from result
    n = sp.wncard(result)
    intervals = []
    for i in range(n):
        start, end = sp.wnfetd(result, i)
        # convert back to UTC
        start_utc = sp.et2utc(start, 'C', 0)
        end_utc   = sp.et2utc(end, 'C', 0)
        intervals.append((start_utc, end_utc))
    
    # Clean up
    sp.unload(observer_spk)
    
    print("interrvals:------")
    print(intervals)
    return intervals

async def get_events(location: GeodeticLocation, start_time: datetime, end_time: datetime, whitelisted_event_types: List[str], event_specific_criteria: List[EventCriteria]) -> List[EventItem]:
    events = []

    conn = get_conn()
    site_name = create_site_or_fetch(location, conn)
    occulations = handle_occultations(site_name, start_time, end_time)

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