from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Float, Integer, String, DateTime, Numeric, func
from sqlalchemy.orm import relationship
from src.Flights.models import Ticket

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    account_balance = Column(Float, nullable=False, default=0)

    user_tickets = relationship("Ticket", foreign_keys="Ticket.user_id", back_populates="user")

