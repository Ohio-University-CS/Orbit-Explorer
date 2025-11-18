from pydantic import BaseModel, Field

class GeodeticLocation(BaseModel):
    lon: float = Field(..., ge=-180.0, le=180.0, description="Longitude in degrees east")
    lat: float = Field(..., ge=-90.0, le=90.0, description="Latitude in degrees north")
    elevation: float = Field(..., description="Elevation in meters above WGS84 ellipsoid")