from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from models import Machine, SystemCheck, User
from schemas import MachineCreate, MachineUpdate, SystemCheckCreate, UserCreate

# Machine CRUD operations
class MachineCRUD:
    def create(self, db: Session, machine: MachineCreate) -> Machine:
        db_machine = Machine(
            machine_id=machine.machine_id,
            hostname=machine.hostname,
            operating_system=machine.operating_system,
            os_version=machine.os_version,
            disk_encrypted=machine.disk_encrypted,
            os_up_to_date=machine.os_up_to_date,
            antivirus_active=machine.antivirus_active,
            sleep_settings_compliant=machine.sleep_settings_compliant
        )
        db.add(db_machine)
        db.commit()
        db.refresh(db_machine)
        return db_machine

    def get(self, db: Session, machine_id: str) -> Optional[Machine]:
        return db.query(Machine).filter(Machine.machine_id == machine_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Machine]:
        return db.query(Machine).offset(skip).limit(limit).all()

    def update(self, db: Session, machine_id: str, machine_update: MachineUpdate) -> Optional[Machine]:
        db_machine = self.get(db, machine_id)
        if not db_machine:
            return None
        
        update_data = machine_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_machine, field, value)
        
        db_machine.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_machine)
        return db_machine

    def delete(self, db: Session, machine_id: str) -> bool:
        db_machine = self.get(db, machine_id)
        if not db_machine:
            return False
        
        db.delete(db_machine)
        db.commit()
        return True

    def count(self, db: Session) -> int:
        return db.query(Machine).count()

    def count_healthy(self, db: Session) -> int:
        # Count machines with no issues and recent check-ins
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        return db.query(Machine).filter(
            and_(
                Machine.last_check_in > cutoff_time,
                or_(
                    Machine.issues.is_(None),
                    Machine.issues == []
                )
            )
        ).count()

    def count_warnings(self, db: Session) -> int:
        # Count machines with warnings but no critical issues
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        return db.query(Machine).filter(
            and_(
                Machine.last_check_in > cutoff_time,
                Machine.issues.isnot(None),
                Machine.issues != [],
                ~Machine.issues.any(lambda x: x.get('severity') == 'critical')
            )
        ).count()

    def count_critical(self, db: Session) -> int:
        # Count machines with critical issues
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        return db.query(Machine).filter(
            and_(
                Machine.last_check_in > cutoff_time,
                Machine.issues.isnot(None),
                Machine.issues != [],
                Machine.issues.any(lambda x: x.get('severity') == 'critical')
            )
        ).count()

    def get_by_os(self, db: Session, os_name: str) -> List[Machine]:
        return db.query(Machine).filter(
            Machine.operating_system.ilike(f"%{os_name}%")
        ).all()

    def get_offline_machines(self, db: Session, hours: int = 1) -> List[Machine]:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return db.query(Machine).filter(
            or_(
                Machine.last_check_in.is_(None),
                Machine.last_check_in < cutoff_time
            )
        ).all()

# System Check CRUD operations
class SystemCheckCRUD:
    def create(self, db: Session, check: SystemCheckCreate) -> SystemCheck:
        db_check = SystemCheck(
            machine_id=check.machine_id,
            check_type=check.check_type,
            status=check.status,
            details=check.details
        )
        db.add(db_check)
        db.commit()
        db.refresh(db_check)
        return db_check

    def get(self, db: Session, check_id: int) -> Optional[SystemCheck]:
        return db.query(SystemCheck).filter(SystemCheck.id == check_id).first()

    def get_by_machine(self, db: Session, machine_id: str, limit: int = 50) -> List[SystemCheck]:
        return db.query(SystemCheck).filter(
            SystemCheck.machine_id == machine_id
        ).order_by(SystemCheck.timestamp.desc()).limit(limit).all()

    def get_recent_checks(self, db: Session, hours: int = 24) -> List[SystemCheck]:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return db.query(SystemCheck).filter(
            SystemCheck.timestamp > cutoff_time
        ).order_by(SystemCheck.timestamp.desc()).all()

# User CRUD operations
class UserCRUD:
    def create(self, db: Session, user: UserCreate) -> User:
        from auth import get_password_hash
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            is_active=user.is_active,
            is_admin=user.is_admin
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def update(self, db: Session, user_id: int, user_update: dict) -> Optional[User]:
        db_user = self.get(db, user_id)
        if not db_user:
            return None
        
        for field, value in user_update.items():
            if hasattr(db_user, field):
                setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete(self, db: Session, user_id: int) -> bool:
        db_user = self.get(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True

# Create CRUD instances
machine_crud = MachineCRUD()
system_check_crud = SystemCheckCRUD()
user_crud = UserCRUD()
