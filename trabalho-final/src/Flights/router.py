from ast import Raise
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from .models import Flight, Ticket
from .schemas import FlightRequest, FlightResponse, FlightSearchRequest, FlightSearchResponse, TicketPurchaseRequest, TicketResponse
from sqlalchemy.orm import Session
from src.Users.models import User
from src.Users.auth_utils import get_current_user
from src.Airports.models import Route
from utils import validate_foreign_key


router = APIRouter()
 
@router.get('/flights', response_model=List[FlightResponse])
def list_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()


@router.get('/flights/{id}', response_model=FlightResponse)
def get_flight_by_id(id: int, db: Session = Depends(get_db)):
    return retrieve_flight_by_id(id, db)


@router.post('/flights', response_model=FlightResponse, status_code=201)
def insert_flight(request: FlightRequest, db: Session = Depends(get_db)):

    validate_foreign_key(db, Route, request.route_id)

    if request.number_of_available_seats <= 0:
        raise HTTPException(status_code=400, detail="Number of available seats must be at least 1")


    new_flight = Flight(
        **request.model_dump()  # Convert Pydantic model to dict
    )
    
    db.add(new_flight)
    
    try:
        db.commit()
        db.refresh(new_flight)  
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="Failed to insert flight")

    return new_flight

@router.put('/flights/{id}', response_model = FlightResponse)
def update_flight(id: int, request: FlightRequest, db: Session = Depends(get_db)):

    flight = retrieve_flight_by_id(id, db)

    validate_foreign_key(db, Route, request.route_id)

    if request.number_of_available_seats <= 0:
        raise HTTPException(status_code=400, detail="Number of available seats must be at least 1")


    
    flight.route_id = request.route_id
    flight.datetime = request.datetime
    flight.ticket_price = request.ticket_price
    flight.vailable_seats = request.number_of_available_seats
    
    db.add(flight)
    
    try:
        db.commit()
        db.refresh(flight)  
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="Failed to update flight")

    return flight

@router.delete('/flights/{id}', response_model=FlightResponse)
def delete_flight(id: int, db: Session = Depends(get_db)):
    
    tickets_exist = db.query(Ticket).filter(Ticket.flight_id == id).first()
    if tickets_exist:
        raise HTTPException(status_code=400, detail="Cannot delete flight with existing tickets")
    
    flight = retrieve_flight_by_id(id, db)
    db.delete(flight)
    db.commit()

    return flight
    

def retrieve_flight_by_id(id: int, db: Session = Depends(get_db)) -> Flight:

    flight = db.query(Flight).filter(Flight.id==id).first()

    if flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
   
    return flight

@router.get('/tickets', response_model=List[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()

@router.post('/purchase-tickets', response_model=TicketResponse)
def purchase_tickets(request: TicketPurchaseRequest, current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):

    flight = retrieve_flight_by_id(request.flight_id, db)

    if request.number_of_seats <= 0:
        raise HTTPException(status_code=400, detail="Number of seats must be at least 1")


    
    if (request.number_of_seats > flight.number_of_available_seats):
        raise HTTPException(status_code=400, detail="Not enough available seats")
    
    total_cost = request.number_of_seats*flight.ticket_price
    if (total_cost > current_user.account_balance):
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    flight.number_of_available_seats -= request.number_of_seats
    current_user.account_balance -= total_cost


    db.add(flight)

    new_ticket = Ticket(user_id=current_user.id, 
                        flight_id=request.flight_id, 
                        number_of_seats=request.number_of_seats)
    
    db.add(new_ticket)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not process the transaction")

    return new_ticket


@router.post('/search-flights', response_model=List[FlightSearchResponse])
def search_flights(request: FlightSearchRequest, db: Session = Depends(get_db)):

    if request.number_of_seats <= 0:
        raise HTTPException(status_code=400, detail="Number of seats must be at least 1")

    all_routes = db.query(Route).all()
    route_of_interest = None
    for route in all_routes:
        if (route.origin.code == request.origin_code and route.destination.code == request.destination_code):
            route_of_interest = route
            break

    if route_of_interest is None:
        raise HTTPException(status_code=404, detail="Route not found")

    flights_of_interest = route.flights

    available_flights = []
    for flight in flights_of_interest:
        if flight.number_of_available_seats >= request.number_of_seats:
            available_flights.append(FlightSearchResponse(datetime=flight.datetime,
                                                          total_price=(request.number_of_seats)*(flight.ticket_price)))

    if not available_flights:
        raise HTTPException(status_code=404, detail="No flights available")

    available_flights.sort(key=lambda flight: flight.total_price)

    return available_flights



