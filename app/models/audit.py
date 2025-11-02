from datetime import datetime
from ..extensions import db

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(300), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
