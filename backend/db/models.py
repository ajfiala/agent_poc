from sqlalchemy import Column, BigInteger, String, Numeric, DateTime, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Room(Base):
    __tablename__ = 'rooms'

    room_id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_number = Column(String(10), nullable=False)
    room_type = Column(String(50), nullable=False)
    rate = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
