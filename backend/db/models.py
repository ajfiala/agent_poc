from sqlalchemy import Column, BigInteger, String, Numeric, DateTime, text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import CITEXT, TEXT
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Room(Base):
    __tablename__ = 'rooms'

    room_id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_type = Column(String(50), nullable=False)
    rate = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Guest(Base):
    __tablename__ = 'guests'

    guest_id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(CITEXT, unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Reservation(Base):
    __tablename__ = 'reservations'
    
    reservation_id = Column(BigInteger, primary_key=True, autoincrement=True)
    guest_id = Column(BigInteger, ForeignKey('guests.guest_id'), nullable=False)
    room_id = Column(BigInteger, ForeignKey('rooms.room_id'), nullable=False)
    check_in = Column(DateTime(timezone=True), nullable=False)
    check_out = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Service(Base):
    __tablename__ = 'services'
    
    service_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ServiceOrders(Base):
    __tablename__ = 'service_orders'
    
    order_id = Column(BigInteger, primary_key=True, autoincrement=True)
    reservation_id = Column(BigInteger, ForeignKey('reservations.reservation_id'), nullable=False)
    service_id = Column(BigInteger, ForeignKey('services.service_id'), nullable=False)
    quantity = Column(BigInteger, nullable=False, server_default='1')
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Session(Base):
    __tablename__ = 'sessions'
    
    session_id = Column(BigInteger, primary_key=True, autoincrement=True)
    guest_id = Column(BigInteger, ForeignKey('guests.guest_id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class MessagePair(Base):
    __tablename__ = 'messages'
    
    message_id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(BigInteger, ForeignKey('sessions.session_id'), nullable=False)
    guest_id = Column(BigInteger, ForeignKey('guests.guest_id'), nullable=False)
    user_message = Column(TEXT, nullable=False)
    ai_message = Column(TEXT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())