from pydantic import BaseModel

class SmartyAutoAddress(BaseModel):
    street_line: str or None = None
    secondary: str or None = None
    city: str or None = None
    zipcode: str or None = None
    state: str or None = None
    entries: int or None = None

class Property(BaseModel):
    climate_zone: int or None = None
    full_street_address: str or None = None
    unit: str or None = None
    apn: str or None = None
    owner: str or None = None
    year_built: str or None = None
    square_feet: str or None = None
    lot_size: str or None = None
    bedrooms: str or None = None
    total_rooms: str or None = None
    project_extent: str or None = None
    construction_worker: str or None = None