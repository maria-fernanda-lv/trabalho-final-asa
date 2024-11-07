from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Float
from sqlalchemy.orm import relationship

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('routes.id') , nullable=False)
    datetime = Column(DateTime, nullable=False)
    ticket_price = Column(Float, nullable=False)
    number_of_available_seats = Column(Integer, nullable=False)

    route = relationship("Route", back_populates="flights")

    purchased_tickets = relationship("Ticket", foreign_keys="Ticket.flight_id", back_populates="flight")

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    flight_id = Column(Integer, ForeignKey('flights.id'), nullable=False)
    number_of_seats = Column(Integer, nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates='user_tickets')
    flight = relationship("Flight", foreign_keys=[flight_id], back_populates="purchased_tickets")