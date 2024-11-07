from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from .models import Airport, Route
from .schemas import AirportRequest, AirportResponse, RouteRequest, RouteResponse, ReachableAirportsResponse
from utils import validate_foreign_key

router = APIRouter()
 
@router.get('/airports', response_model=List[AirportResponse])
def list_airports(db: Session = Depends(get_db)):
    return db.query(Airport).all()

@router.get('/airports/{id}', response_model=AirportResponse)
def get_airport_by_id(id: int, db: Session = Depends(get_db)):
    return retrieve_airport_by_id(id, db)


@router.post('/airports', response_model=AirportResponse, status_code=201)
def insert_airport(request: AirportRequest, db: Session = Depends(get_db)):
    new_airport = Airport(
        **request.model_dump()  # Convert Pydantic model to dict
    )
    
    db.add(new_airport)
    
    try:
        db.commit()
        db.refresh(new_airport)  
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="Failed to insert airport")

    return new_airport

@router.put('/airports/{id}', response_model = AirportResponse)
def update_airport(id: int, request: AirportRequest, db: Session = Depends(get_db)):
    airport = retrieve_airport_by_id(id, db)

    airport.name  = request.name
    airport.code = request.code
    airport.location = request.location
   
    
    db.add(airport)
    
    try:
        db.commit()
        db.refresh(airport)  
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="Failed to update airport")

    return airport

@router.delete('/airports/{id}', response_model=AirportResponse)
def delete_airport(id: int, db: Session = Depends(get_db)):
    airport = retrieve_airport_by_id(id, db)
    db.delete(airport)
    db.commit()

    return airport
    

def retrieve_airport_by_id(id: int, db: Session = Depends(get_db)) -> Airport:

   airport = db.query(Airport).filter_by(id=id).first()

   if airport is None:
        raise HTTPException(status_code=404, detail="Airport not found")
   
   return airport
       
@router.get("/airports/{origin_code}/reachable", response_model=ReachableAirportsResponse)
def get_airports_by_origin(origin_code: str, db: Session = Depends(get_db)):
    
    origin_airport = db.query(Airport).filter(Airport.code == origin_code).first()
    if not origin_airport:
        raise HTTPException(status_code=404, detail="Origin airport not found.")
    
    # Fetch routes where the origin matches the provided airport code
    routes = origin_airport.routes_origin
    
    if not routes:
        return ReachableAirportsResponse(origin=origin_airport, destinations=[])

    destination_airports = [
        route.destination
        for route in routes
    ]

    return ReachableAirportsResponse(origin=origin_airport, destinations=destination_airports)



























@router.get('/routes', response_model=List[RouteResponse])
def list_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()

@router.get('/routes/{id}', response_model=RouteResponse)
def get_route_by_id(id: int, db: Session = Depends(get_db)):
    return retrieve_route_by_id(id, db)

@router.post('/routes', response_model=RouteResponse, status_code=201)
def insert_route(request: RouteRequest, db: Session = Depends(get_db)):
    origin = db.query(Airport).filter(Airport.code==request.origin_code).first()
    destination = db.query(Airport).filter(Airport.code==request.destination_code).first()
    
    if not origin or not destination:
        raise HTTPException(status_code=400, detail="Invalid origin or destination airport code")

    new_route = Route(origin_id=origin.id,destination_id=destination.id)
    
    db.add(new_route)
    db.commit()
    db.refresh(new_route)  
    return RouteResponse(id=new_route.id, origin=origin, destination=destination)

@router.put('/routes/{id}', response_model = RouteResponse)
def update_route(id: int, request: RouteRequest, db: Session = Depends(get_db)):

    new_origin = db.query(Airport).filter(Airport.code==request.origin_code).first()
    new_destination = db.query(Airport).filter(Airport.code==request.destination_code).first()

    if not new_origin or not new_destination:
        raise HTTPException(status_code=400, detail="Invalid origin or destination airport code")

    updated_route = retrieve_route_by_id(id, db) #nesse caso acho que nem precisava disso
    updated_route.origin_id = new_origin.id
    updated_route.destination_id = new_destination.id

    db.add(updated_route)
    db.commit()
    db.refresh(updated_route)  
    
    return RouteResponse(id=id, origin=new_origin, destination=new_destination)

@router.delete('/routes/{id}', response_model=RouteResponse)
def delete_route(id: int, db: Session = Depends(get_db)):
    route = retrieve_route_by_id(id, db)
    deleted_route = RouteResponse(id=id, origin=route.origin, destination=route.destination)
    db.delete(route)
    db.commit()

    return deleted_route
    

def retrieve_route_by_id(id: int, db: Session = Depends(get_db)) -> Route:

   route = db.query(Route).filter(Route.id==id).first()

   if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
   
   return route
       