from fastapi import APIRouter, HTTPException
import requests

reverse_router = APIRouter()

@reverse_router.get("/reverse_geocode")
def reverse_geocode(lat: float, lon: float):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "zoom": 18,
        "addressdetails": 1
    }

    r = requests.get(url, headers={"User-Agent": "OrbitExplorer/1.0"}, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Reverse geocode lookup failed")

    data = r.json()

    return {
        "display_name": data.get("display_name"),
        "address": data.get("address"),
        "lat": lat,
        "lon": lon
    }
