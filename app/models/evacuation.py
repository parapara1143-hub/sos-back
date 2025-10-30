
from datetime import datetime
from enum import Enum
from ..extensions import db

class EvacuationStatus(str, Enum):
    open="open"; closed="closed"

class EvacuationPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, nullable=False)

class MusterPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    lat = db.Column(db.Float); lon = db.Column(db.Float)

class EvacuationEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(EvacuationStatus), default=EvacuationStatus.open, nullable=False)
    started_by = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime)

class EvacuationCheckin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    method = db.Column(db.String(20))  # gps/triangulation/manual
    lat = db.Column(db.Float); lon = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
