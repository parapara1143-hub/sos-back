from datetime import datetime
from ..extensions import db

class InspectionChecklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class InspectionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(300), nullable=False)

class InspectionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    result = db.Column(db.JSON, nullable=False)  # {item_id: {"ok": bool, "obs": "..."}}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
