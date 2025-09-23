import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from Task_1.apps.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True)
    name = Column(String(255))
    deleted_at = Column(TIMESTAMP)

    profiles = relationship("UserProfile", cascade="all, delete")
    activities = relationship("UserActivity", cascade="all, delete")
    uploads = relationship("Upload", cascade="all, delete")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    bio = Column(String(255))

class UserActivity(Base):
    __tablename__ = "user_activity"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    event = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Upload(Base):
    __tablename__ = "uploads"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    s3_key = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36))
    action = Column(String(255))
    detail = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
