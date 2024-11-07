from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String(3), nullable=False)
    location = Column(String, nullable=False)

    routes_origin = relationship("Route", foreign_keys='Route.origin_id', back_populates="origin")
    routes_destination = relationship("Route", foreign_keys='Route.destination_id', back_populates="destination",  cascade="all, delete-orphan" )

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    origin_id = Column(Integer, ForeignKey('airports.id'), nullable=False)
    destination_id = Column(Integer, ForeignKey('airports.id'), nullable=False)

    origin = relationship("Airport", foreign_keys=[origin_id], back_populates='routes_origin')
    destination = relationship("Airport", foreign_keys=[destination_id], back_populates='routes_destination')

    flights = relationship("Flight", back_populates="route")