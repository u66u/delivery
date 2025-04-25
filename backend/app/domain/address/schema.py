from pydantic import BaseModel
from uuid import UUID

class NewAddress(BaseModel):
    label: str
    city: str
    street: str
    apartment: str
    building: str
    floor: str | None = None
    entrance: str | None = None
    details: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    
class AddressResponse(NewAddress):
    id: UUID