from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Machine schemas
class MachineBase(BaseModel):
    hostname: str = Field(..., description="Machine hostname")
    operating_system: str = Field(..., description="Operating system name")
    os_version: Optional[str] = Field(None, description="Operating system version")
    disk_encrypted: bool = Field(False, description="Whether disk encryption is enabled")
    os_up_to_date: bool = Field(False, description="Whether OS is up to date")
    antivirus_active: bool = Field(False, description="Whether antivirus is active")
    sleep_settings_compliant: bool = Field(False, description="Whether sleep settings are compliant")

class MachineCreate(MachineBase):
    machine_id: str = Field(..., description="Unique machine identifier")

class MachineUpdate(BaseModel):
    hostname: Optional[str] = None
    operating_system: Optional[str] = None
    os_version: Optional[str] = None
    disk_encrypted: Optional[bool] = None
    os_up_to_date: Optional[bool] = None
    antivirus_active: Optional[bool] = None
    sleep_settings_compliant: Optional[bool] = None
    cpu_usage: Optional[int] = Field(None, ge=0, le=100)
    memory_usage: Optional[int] = Field(None, ge=0, le=100)
    disk_usage: Optional[int] = Field(None, ge=0, le=100)
    network_status: Optional[str] = None
    issues: Optional[List[Dict[str, Any]]] = None

class Machine(MachineBase):
    machine_id: str
    cpu_usage: Optional[int] = None
    memory_usage: Optional[int] = None
    disk_usage: Optional[int] = None
    network_status: Optional[str] = None
    issues: Optional[List[Dict[str, Any]]] = []
    last_check_in: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# System Check schemas
class SystemCheckBase(BaseModel):
    machine_id: str = Field(..., description="Machine ID to associate with")
    check_type: str = Field(..., description="Type of system check")
    status: str = Field(..., description="Check status")
    details: Optional[str] = Field(None, description="Additional check details")

class SystemCheckCreate(SystemCheckBase):
    pass

class SystemCheck(SystemCheckBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    is_active: bool = Field(True, description="Whether user is active")
    is_admin: bool = Field(False, description="Whether user has admin privileges")

class UserCreate(UserBase):
    password: str = Field(..., description="Plain text password")

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Dashboard schemas
class DashboardStats(BaseModel):
    total_machines: int
    healthy_machines: int
    warning_machines: int
    critical_machines: int
    compliance_rate: float

class ComplianceOverview(BaseModel):
    disk_encryption: Dict[str, int]
    os_updates: Dict[str, int]
    antivirus: Dict[str, int]
    sleep_settings: Dict[str, int]

# Issue schema
class Issue(BaseModel):
    id: str
    severity: str = Field(..., description="Issue severity: info, warning, critical")
    message: str = Field(..., description="Issue description")
    details: Optional[str] = Field(None, description="Additional issue details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = Field(False, description="Whether issue is resolved")

# Health check schema
class HealthCheck(BaseModel):
    machine_id: str
    timestamp: datetime
    cpu_usage: int = Field(..., ge=0, le=100)
    memory_usage: int = Field(..., ge=0, le=100)
    disk_usage: int = Field(..., ge=0, le=100)
    network_status: str
    issues: List[Issue] = []
