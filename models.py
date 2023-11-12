from pydantic import BaseModel

class SmartyAutoAddress(BaseModel):
    street_line: str or None = None
    secondary: str or None = None
    city: str or None = None
    zipcode: str or None = None
    state: str or None = None
    entries: int or None = None