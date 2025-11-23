"""User Model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from enum import Enum

from app.database import Base


class UserRole(str, Enum):
    """User role enumeration"""
    BUYER = "buyer"
    BROKER = "broker"
    DEVELOPER = "developer"
    BANK = "bank"
    ADMIN = "admin"


class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.BUYER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
