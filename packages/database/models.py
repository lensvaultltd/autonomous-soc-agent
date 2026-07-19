from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import enum

Base = declarative_base()

class SubscriptionTier(enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class Role(enum.Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    CUSTOMER = "customer"

# --- CORE TENANCY ---
class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(String, primary_key=True) # e.g. TEN-1234
    name = Column(String, nullable=False)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", back_populates="tenant")
    incidents = relationship("Incident", back_populates="tenant")

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(Role), default=Role.CUSTOMER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="users")

# --- SOC ENTITIES ---
# Notice: Every table MUST have a tenant_id for strict Row-Level Security isolation.
class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(String, primary_key=True) # e.g. INC-9921
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    title = Column(String, nullable=False)
    severity = Column(String, nullable=False) # Critical, High, Medium, Low
    status = Column(String, nullable=False) # Open, Investigating, Closed
    ai_summary = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="incidents")
