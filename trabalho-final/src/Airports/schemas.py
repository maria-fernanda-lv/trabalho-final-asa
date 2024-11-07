from pydantic import BaseModel
from pydantic import ConfigDict
from typing import List

class AirportRequest(BaseModel):
    name: str
    code: str
    location: str

class AirportResponse(BaseModel):

    id: int
    name: str
    code: str
    location: str

    model_config = ConfigDict(from_attributes=True)

    

class RouteRequest(BaseModel):
    origin_code: str
    destination_code: str

class RouteResponse(BaseModel):

    id: int
    origin: AirportResponse
    destination: AirportResponse

    model_config = ConfigDict(from_attributes=True)


class ReachableAirportsResponse(BaseModel):
    origin: AirportResponse
    destinations: List[AirportResponse]
