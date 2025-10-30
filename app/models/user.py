from datetime import datetime
from enum import Enum
from ..extensions import db

class UserRole(str, Enum):
    owner="owner"; admin="admin"; supervisor="supervisor"; tecnico_seg="tecnico_seg"
    brigadista="brigadista"; socorrista="socorrista"; medico="medico"; patrimonial="patrimonial"; colaborador="colaborador"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.colaborador, nullable=False)
    company_id = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
