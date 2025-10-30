from datetime import datetime
from enum import Enum
from ..extensions import db

class IncidentStatus(str, Enum):
    open="open"; in_progress="in_progress"; resolved="resolved"; cancelled="cancelled"

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    label = db.Column(db.String(120))

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(IncidentStatus), default=IncidentStatus.open, nullable=False)
    lat = db.Column(db.Float); lon = db.Column(db.Float)
    reporter_id = db.Column(db.Integer); assignee_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
