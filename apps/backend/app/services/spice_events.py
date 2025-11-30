from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
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

#import matplotlib
#matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt

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

class SPICE_BODY:
    def __init__(self, spk_file: Optional[Path] = None, pck_file: Optional[Path] = None, fk_file: Optional[Path] = None, naif_id: str = ""):
        """
        Initializes the SPICE_BODY instance with optional kernel files (SPK, PCK, FK).
        
        Args:
            spk_file (Optional[Path]): Path to the SPK file.
            pck_file (Optional[Path]): Path to the PCK file.
            fk_file (Optional[Path]): Path to the FK file.
            naif_id (str): NAIF ID for the body (used for identification purposes).
        """
        self.spk_file = spk_file
        self.pck_file = pck_file
        self.fk_file = fk_file
        self.naif_id = naif_id

    def furnsh_spk(self) -> None:
        """
        Furnish the SPK file if it exists.
        """
        if self.spk_file and self.spk_file.exists():
            sp.furnsh(str(self.spk_file))
        elif self.spk_file:
            print(f"SPK file not found: {self.spk_file}")

    def furnsh_pck(self) -> None:
        """
        Furnish the PCK file if it exists.
        """
        if self.pck_file and self.pck_file.exists():
            sp.furnsh(str(self.pck_file))
        elif self.pck_file:
            print(f"PCK file not found: {self.pck_file}")

    def furnsh_fk(self) -> None:
        """
        Furnish the FK file if it exists.
        """
        if self.fk_file and self.fk_file.exists():
            sp.furnsh(str(self.fk_file))
        elif self.fk_file:
            print(f"FK file not found: {self.fk_file}")

    def unload_spk(self) -> None:
        """
        Unload the SPK file if it was loaded.
        """
        if self.spk_file and self.spk_file.exists():
            sp.unload(str(self.spk_file))
        elif self.spk_file:
            print(f"SPK file is not loaded or not found: {self.spk_file}")

    def unload_pck(self) -> None:
        """
        Unload the PCK file if it was loaded.
        """
        if self.pck_file and self.pck_file.exists():
            sp.unload(str(self.pck_file))
        elif self.pck_file:
            print(f"PCK file is not loaded or not found: {self.pck_file}")

    def unload_fk(self) -> None:
        """
        Unload the FK file if it was loaded.
        """
        if self.fk_file and self.fk_file.exists():
            sp.unload(str(self.fk_file))
        elif self.fk_file:
            print(f"FK file is not loaded or not found: {self.fk_file}")

    def furnish_all_kernels(self) -> None:
        """
        Furnish all available kernels (SPK, PCK, FK) if they exist.
        """
        self.furnsh_spk()
        self.furnsh_pck()
        self.furnsh_fk()

    def unload_all_kernels(self) -> None:
        """
        Unload all available kernels (SPK, PCK, FK) if they are loaded.
        """
        self.unload_spk()
        self.unload_pck()
        self.unload_fk()

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

earth = SPICE_BODY()
earth.spk_file = kernel_file(KernelType.SPK, ObjectType.PLANET, "de432s.bsp")
earth.pck_file = kernel_file(KernelType.PCK, None, "pck00011.tpc")
earth.naif_id = "399"


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

    lat_rad = location.lat * np.pi/180
    lon_rad = location.lon * np.pi/180
    x, y, z = sp.georec(lon_rad, lat_rad, location.alt_km, re, f)
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
        "bounds": ("@1000-JAN-01", "@3000-JAN-01")
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
        str(pinpoint_path.resolve()),
        "-def", str(defs_path.resolve()),
        "-pck", str(pck_path.resolve()),
        "-spk", str(output_spk.resolve()),
        "-fk", str(output_fk.resolve())
    ]

    try:
        # Let pinpoint print directly to terminal
        result = subprocess.run(cmd, check=True)
        print(result.stdout)
        print(result.stderr)
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
    The format is 'YYYY-MM-DDTHH:MM:SS.SSSSSS UTC' (up to 6 decimal places).
    """
    if not isinstance(dt, datetime):
        raise TypeError(f"Expected datetime.datetime, got {type(dt)}")
    
    # Format the datetime object to include microseconds (up to 6 digits)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond:06d}"

def handle_occultations(site_name: str, start_time: datetime, end_time: datetime):
    response = {
        "occultations": [],
    }

    moon = SPICE_BODY()
    moon.spk_file = kernel_file(KernelType.SPK, ObjectType.PLANET, "de432s.bsp")
    moon.pck_file = kernel_file(KernelType.PCK, None, "pck00011.tpc")
    moon.naif_id = "301"

    site = SPICE_BODY()
    site.spk_file = kernel_file(KernelType.SPK, ObjectType.SITE, f"{site_name}.spk")
    site.fk_file = kernel_file(KernelType.FK, ObjectType.SITE, f"{site_name}.tf")
    site.naif_id = site_name

    sun = SPICE_BODY()
    sun.spk_file = kernel_file(KernelType.SPK, ObjectType.PLANET, "de432s.bsp")
    sun.pck_file = kernel_file(KernelType.PCK, None, "pck00011.tpc")
    sun.naif_id = "10"

    occultations_ANY = find_occultations(
        "ANY",
        obsrvr=site,
        front=moon,
        fframe='IAU_MOON',
        back=sun,
        bframe='IAU_SUN',
        start=start_time,
        end=end_time,
        step=60.0
    )

    print("ANY OCCULTATIONS")
    for start_dt, end_dt in occultations_ANY:
        print(f"Start: {start_dt}, End: {end_dt}")

        occultations = find_occultations(
            "FULL",
            obsrvr=site,
            front=moon,
            fframe='IAU_MOON',
            back=sun,
            bframe='IAU_SUN',
            start=start_dt,
            end=end_dt,
            step=1.0
        )

        print("FULL OCCULTATIONS")
        for start_dt, end_dt in occultations:
            print(f"Start: {start_dt}, End: {end_dt}")

        occultations = find_occultations(
            "PARTIAL",
            obsrvr=site,
            front=moon,
            fframe='IAU_MOON',
            back=sun,
            bframe='IAU_SUN',
            start=start_dt,
            end=end_dt,
            step=60.0
        )


        print("PARTIAL OCCULTATIONS")
        for start_dt, end_dt in occultations:
            print(f"Start: {start_dt}, End: {end_dt}")

        occultations = find_occultations(
            "ANNULAR",
            obsrvr=site,
            front=moon,
            fframe='IAU_MOON',
            back=sun,
            bframe='IAU_SUN',
            start=start_dt,
            end=end_dt,
            step=30.0
        )


        print("ANNULAR OCCULTATIONS")
        for start_dt, end_dt in occultations:
            print(f"Start: {start_dt}, End: {end_dt}")

    n=15
    delta_time = timedelta(seconds=n)

    for start_dt, end_dt in occultations_ANY:
        times = []
        dt = start_dt  # Initialize dt with start time

        while dt <= end_dt:
            times.append(dt)
            dt = dt + delta_time
        if dt - delta_time < end_dt:
            times.append(end_dt)


        occultation_res = {
            "start_utc": start_dt,
            "end_utc": end_dt,
            "computational_data": {},
        }

        occulting_relpos = get_relative_pos(
            targ=moon,
            times=times,
            ref_frame="J2000",
            abcorr="NONE",
            obsrvr=site
        )

        occulted_relpos = get_relative_pos(
            targ=sun,
            times=times,
            ref_frame="J2000",
            abcorr="NONE",
            obsrvr=site
        )


        occulting_rngs_list = []
        occulting_azs_list = []
        occulting_els_list = []

        occulted_rngs_list = []
        occulted_azs_list = []
        occulted_els_list = []


        for pos in occulting_relpos["pos"]:
            occulting_rng, occulting_az, occulting_el = sp.recazl(pos, True, True)
            occulting_rngs_list.append(occulting_rng)
            occulting_azs_list.append(occulting_az)
            occulting_els_list.append(occulting_el)

        for pos in occulted_relpos["pos"]:
            occulted_rng, occulted_az, occulted_el = sp.recazl(pos, True, True)
            occulted_rngs_list.append(occulted_rng)
            occulted_azs_list.append(occulted_az)
            occulted_els_list.append(occulted_el)


        occultation_res["computational_data"]["sample_times"] = times
        occultation_res["computational_data"]["occulting_dist"] = occulting_rngs_list
        occultation_res["computational_data"]["occulting_azimuths"] = occulting_azs_list
        occultation_res["computational_data"]["occulting_elevations"] = occulting_els_list

        occultation_res["computational_data"]["occulted_dist"] = occulted_rngs_list
        occultation_res["computational_data"]["occulted_azimuths"] = occulted_azs_list
        occultation_res["computational_data"]["occulted_elevations"] = occulted_els_list

        response["occultations"].append(occultation_res)
        # Convert the lists to NumPy arrays
        occulting_rngs = np.array(occulting_rngs_list)
        occulting_azs = np.array(occulting_azs_list)
        occulting_els = np.array(occulting_els_list)

        occulted_rngs = np.array(occulted_rngs_list)
        occulted_azs = np.array(occulted_azs_list)
        occulted_els = np.array(occulted_els_list)

    for start_dt, end_dt in []:
        dt = start_dt  # Initialize dt with start time


        while dt <= end_dt:
            phase_angle = calculate_phase_angle(dt, moon, sun, site)
            print(f"PHASE ANGLE at {dt}: {phase_angle}")

            # Increment dt by delta_time
            dt = dt + delta_time

        # After the loop, handle the last value of dt just before end_dt
        if dt - delta_time < end_dt:
            # Calculate the phase angle for the last time step before end_dt
            phase_angle = calculate_phase_angle(dt - delta_time, moon, sun, site)
            print(f"PHASE ANGLE at {dt - delta_time}: {phase_angle}")
    return response


def get_relative_pos(targ: SPICE_BODY, times: List[datetime], ref_frame: str, abcorr: str, obsrvr: SPICE_BODY) -> Dict[str, List]:
    # Load necessary kernels
    lsk_loc = str(kernel_file(KernelType.LSK, None, "naif0012.tls.pc"))
    earth_fixed = str(kernel_file(KernelType.PCK, None, "earth_fixed.tf"))

    sp.furnsh(lsk_loc)
    earth.furnish_all_kernels()
    sp.furnsh(earth_fixed)

    targ.furnish_all_kernels()
    obsrvr.furnish_all_kernels()

    positions = []
    light_times = []

    for dt in times:
        # Convert datetime to ephemeris time (ET)
        et = sp.str2et(datetime_to_utc_string(dt))

        # Get the position and light time
        otp = sp.spkpos(
            targ.naif_id,
            et,
            ref_frame,
            abcorr,
            obsrvr.naif_id
        )

        positions.append(otp[0]) 
        light_times.append(otp[1])

    sp.unload(lsk_loc)
    sp.unload(earth_fixed)
    targ.unload_all_kernels()
    obsrvr.unload_all_kernels()

    return {
        "pos": positions,
        "lt": light_times
    }

def find_occultations(occtyp, obsrvr: SPICE_BODY, front, fframe, back: SPICE_BODY, bframe, start: datetime, end: datetime, step: float):
    lsk_loc = str(kernel_file(KernelType.LSK, None, "naif0012.tls.pc"))
    earth_fixed = str(kernel_file(KernelType.PCK, None, "earth_fixed.tf"))

    sp.furnsh(lsk_loc)
    earth.furnish_all_kernels()
    sp.furnsh(earth_fixed)

    back.furnish_all_kernels()
    obsrvr.furnish_all_kernels()

    # Convert UTC to ephemeris seconds past J2000
    et_start = sp.str2et(datetime_to_utc_string(start))
    et_end   = sp.str2et(datetime_to_utc_string(end))
    
    # Create confinement window
    cnfine = sp.utils.support_types.SPICEDOUBLE_CELL(1000)
    sp.wninsd(et_start, et_end, cnfine)

    # Result window
    result = sp.utils.support_types.SPICEDOUBLE_CELL(1000)  # max 500 intervals (start/end pairs)
    
    # Call the occultation finder
    sp.gfoclt(
        occtyp,
        front.naif_id,
        'ELLIPSOID',
        fframe,
        back.naif_id,
        'ELLIPSOID',
        bframe,
        'LT',
        obsrvr.naif_id,
        step,
        cnfine,
        result
    )

    # Extract intervals from result
    n = sp.wncard(result)
    intervals = []
    for i in range(n):
        start, end = sp.wnfetd(result, i)
        # convert back to UTC
        start_utc = sp.et2utc(start, 'C', 6) #max is 14, datetime only supports 6
        end_utc   = sp.et2utc(end, 'C', 6)
        start_dt  = datetime.strptime(start_utc, "%Y %b %d %H:%M:%S.%f")
        end_dt    = datetime.strptime(end_utc, "%Y %b %d %H:%M:%S.%f")
        intervals.append((start_dt, end_dt))

    sp.unload(lsk_loc)
    sp.unload(earth_fixed)
    back.unload_all_kernels()
    earth.unload_all_kernels()
    obsrvr.unload_all_kernels()

    return intervals


def calculate_phase_angle(dt: datetime, target: SPICE_BODY, illmn: SPICE_BODY, obsrvr: SPICE_BODY):

    lsk_loc = str(kernel_file(KernelType.LSK, None, "naif0012.tls.pc"))
    earth_fixed = str(kernel_file(KernelType.PCK, None, "earth_fixed.tf"))

    sp.furnsh(lsk_loc)
    sp.furnsh(earth_fixed)

    target.furnish_all_kernels()
    illmn.furnish_all_kernels()
    earth.furnish_all_kernels()
    obsrvr.furnish_all_kernels()

    et = sp.str2et(datetime_to_utc_string(dt))

    abcorr = "LT+S"
    angle = sp.phaseq(
        et,
        target.naif_id,
        illmn.naif_id,
        obsrvr.naif_id,
        abcorr
    )

    sp.unload(lsk_loc)
    sp.unload(earth_fixed)
    target.unload_all_kernels()
    illmn.unload_all_kernels()
    earth.unload_all_kernels()
    obsrvr.unload_all_kernels()

    return angle

async def get_events(location: GeodeticLocation, start_time: datetime, end_time: datetime, whitelisted_event_types: List[str], event_specific_criteria: List[EventCriteria]) -> List[EventItem]:
    events = []

    conn = get_conn()
    site_name = create_site_or_fetch(location, conn)
    occulations_obj = handle_occultations(site_name, start_time, end_time)

    dummy_event = EventItem(
        id="event_001",
        type="solar_eclipse",
        name="Partial Solar Eclipse",
        time=start_time,
        desc=f"Dummy event at lat {location.lat}, lon {location.lon}"
    )

    return [dummy_event]


async def get_occultations(location: GeodeticLocation, start_time: datetime, end_time: datetime, occulting_naif_id: str, occulted_naif_id: str) -> object:
    conn = get_conn()
    site_name = create_site_or_fetch(location, conn)
    occultations_obj = handle_occultations(site_name, start_time, end_time)
    return occultations_obj

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