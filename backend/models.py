from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, JSON
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class Machine(Base):
    __tablename__ = "machines"

    machine_id = Column(String, primary_key=True, index=True)
    hostname = Column(String, nullable=False)
    operating_system = Column(String, nullable=False)
    os_version = Column(String)
    disk_encrypted = Column(Boolean, default=False)
    os_up_to_date = Column(Boolean, default=False)
    antivirus_active = Column(Boolean, default=False)
    sleep_settings_compliant = Column(Boolean, default=False)
    last_check_in = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Additional fields for system health
    cpu_usage = Column(Integer)  # Percentage
    memory_usage = Column(Integer)  # Percentage
    disk_usage = Column(Integer)  # Percentage
    network_status = Column(String)  # "connected", "disconnected"
    
    # Issues as JSON field
    issues = Column(JSON, default=list)
    
    def __repr__(self):
        return f"<Machine(machine_id='{self.machine_id}', hostname='{self.hostname}')>"

class SystemCheck(Base):
    __tablename__ = "system_checks"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, nullable=False, index=True)
    check_type = Column(String, nullable=False)  # "health", "compliance", "security"
    status = Column(String, nullable=False)  # "pass", "fail", "warning"
    details = Column(Text)
    timestamp = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<SystemCheck(id={self.id}, machine_id='{self.machine_id}', type='{self.check_type}')>"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
