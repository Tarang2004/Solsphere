from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import os

from database import engine, Base
from models import Machine, SystemCheck
from schemas import MachineCreate, MachineUpdate, SystemCheckCreate
from crud import machine_crud, system_check_crud
from auth import get_current_user, create_access_token, authenticate_user
from config import settings

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Solsphere System Utility API",
    description="API for monitoring system health and compliance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "solsphere-api"}

# Machine endpoints
@app.post("/api/machines", response_model=dict)
async def create_machine(machine: MachineCreate):
    """Create a new machine entry"""
    try:
        db_machine = await machine_crud.create(machine)
        return {"message": "Machine created successfully", "machine_id": db_machine.machine_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/machines")
async def get_machines(
    skip: int = 0,
    limit: int = 100,
    os_filter: str = None,
    status_filter: str = None
):
    """Get all machines with optional filtering"""
    try:
        machines = await machine_crud.get_multi(skip=skip, limit=limit)
        
        # Apply filters
        if os_filter:
            machines = [m for m in machines if m.operating_system and os_filter.lower() in m.operating_system.lower()]
        
        if status_filter:
            machines = [m for m in machines if get_machine_status(m) == status_filter]
        
        return machines
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/machines/{machine_id}")
async def get_machine(machine_id: str):
    """Get a specific machine by ID"""
    try:
        machine = await machine_crud.get(machine_id)
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")
        return machine
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/machines/{machine_id}")
async def update_machine(machine_id: str, machine_update: MachineUpdate):
    """Update a machine"""
    try:
        updated_machine = await machine_crud.update(machine_id, machine_update)
        if not updated_machine:
            raise HTTPException(status_code=404, detail="Machine not found")
        return updated_machine
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/machines/{machine_id}")
async def delete_machine(machine_id: str):
    """Delete a machine"""
    try:
        success = await machine_crud.delete(machine_id)
        if not success:
            raise HTTPException(status_code=404, detail="Machine not found")
        return {"message": "Machine deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# System check endpoints
@app.post("/api/system-checks")
async def create_system_check(check: SystemCheckCreate):
    """Create a new system check entry"""
    try:
        db_check = await system_check_crud.create(check)
        return {"message": "System check created successfully", "check_id": db_check.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/system-checks/{machine_id}")
async def get_system_checks(machine_id: str, limit: int = 50):
    """Get system checks for a specific machine"""
    try:
        checks = await system_check_crud.get_by_machine(machine_id, limit=limit)
        return checks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Dashboard endpoints
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        total_machines = await machine_crud.count()
        healthy_machines = await machine_crud.count_healthy()
        warning_machines = await machine_crud.count_warnings()
        critical_machines = await machine_crud.count_critical()
        
        return {
            "total_machines": total_machines,
            "healthy_machines": healthy_machines,
            "warning_machines": warning_machines,
            "critical_machines": critical_machines,
            "compliance_rate": round((healthy_machines / total_machines * 100) if total_machines > 0 else 0, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/compliance")
async def get_compliance_overview():
    """Get compliance overview for all systems"""
    try:
        machines = await machine_crud.get_multi()
        
        compliance_data = {
            "disk_encryption": {"compliant": 0, "total": len(machines)},
            "os_updates": {"compliant": 0, "total": len(machines)},
            "antivirus": {"compliant": 0, "total": len(machines)},
            "sleep_settings": {"compliant": 0, "total": len(machines)}
        }
        
        for machine in machines:
            if machine.disk_encrypted:
                compliance_data["disk_encryption"]["compliant"] += 1
            if machine.os_up_to_date:
                compliance_data["os_updates"]["compliant"] += 1
            if machine.antivirus_active:
                compliance_data["antivirus"]["compliant"] += 1
            if machine.sleep_settings_compliant:
                compliance_data["sleep_settings"]["compliant"] += 1
        
        return compliance_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Export endpoints
@app.get("/api/export/machines")
async def export_machines_csv():
    """Export all machines data as CSV"""
    try:
        machines = await machine_crud.get_multi()
        
        # Convert to CSV format
        csv_data = "Machine ID,Hostname,OS,Status,Last Check-in,Disk Encrypted,OS Updated,Antivirus Active,Sleep Compliant\n"
        
        for machine in machines:
            status = get_machine_status(machine)
            csv_data += f"{machine.machine_id},{machine.hostname},{machine.operating_system},{status},{machine.last_check_in},{machine.disk_encrypted},{machine.os_up_to_date},{machine.antivirus_active},{machine.sleep_settings_compliant}\n"
        
        return JSONResponse(
            content={"csv_data": csv_data},
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Utility functions
def get_machine_status(machine):
    """Determine machine status based on health checks"""
    if not machine.last_check_in:
        return "offline"
    
    # Check if machine is offline (no check-in for more than 1 hour)
    from datetime import datetime, timedelta
    if datetime.utcnow() - machine.last_check_in > timedelta(hours=1):
        return "offline"
    
    # Check for critical issues
    if machine.issues and any(issue.severity == "critical" for issue in machine.issues):
        return "critical"
    
    # Check for warnings
    if machine.issues and len(machine.issues) > 0:
        return "warning"
    
    return "healthy"

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
