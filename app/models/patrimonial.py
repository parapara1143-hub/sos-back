
from datetime import datetime
from ..extensions import db

class PatrolRoute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)

class PatrolCheckpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    lat = db.Column(db.Float); lon = db.Column(db.Float)

class PatrolCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    checkpoint_id = db.Column(db.Integer, nullable=False)
    ts = db.Column(db.DateTime, default=datetime.utcnow)

class AccessEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(120))  # pessoa/veículo
    badge = db.Column(db.String(60))
    event = db.Column(db.String(30))  # in/out/denied
    ts = db.Column(db.DateTime, default=datetime.utcnow)

class AssetIncident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(60))  # furto, invasão, vandalismo, porta violada...
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
