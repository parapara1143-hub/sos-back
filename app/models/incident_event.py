
from datetime import datetime
from ..extensions import db

class IncidentEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, nullable=False)
    event = db.Column(db.String(40), nullable=False)  # created, assigned, in_progress, resolved, cancelled
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
