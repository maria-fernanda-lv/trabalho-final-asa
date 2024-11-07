from pydantic import BaseModel
from pydantic import ConfigDict
from typing import List
from datetime import datetime
from src.Airports.schemas import RouteResponse
from src.Users.schemas import UserResponse

class FlightRequest(BaseModel):
    route_id: int
    datetime: datetime
    ticket_price: float
    number_of_available_seats: int

class FlightResponse(BaseModel):
    id: int
    route: RouteResponse
    datetime: datetime
    ticket_price: float
    number_of_available_seats: int
    
    @property
    def formatted_datetime(self):
        return self.datetime.strftime("%Y-%m-%d %H:%M:%S")  # Adjust format as needed

    class Config:
        # This ensures that the datetime will be serialized as an ISO 8601 string
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")  # Format here too
        }


    # model_config = ConfigDict(from_attributes=True)

class FlightSearchRequest(BaseModel):
    origin_code: str
    destination_code: str
    number_of_seats: int

class FlightSearchResponse(BaseModel):
    datetime: datetime
    total_price: float

    @property
    def formatted_datetime(self):
        return self.datetime.strftime("%Y-%m-%d %H:%M:%S")  # Adjust format as needed

    class Config:
        # This ensures that the datetime will be serialized as an ISO 8601 string
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")  # Format here too
        }


class TicketPurchaseRequest(BaseModel):
    flight_id: int
    number_of_seats: int

class TicketResponse(BaseModel):
    id: int
    user: UserResponse
    flight: FlightResponse
    number_of_seats: int

    model_config = ConfigDict(from_attributes=True)