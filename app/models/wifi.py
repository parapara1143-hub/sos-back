from datetime import datetime
from ..extensions import db

class WifiAccessPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.String(120))
    bssid = db.Column(db.String(120), unique=True, nullable=False)
    lat = db.Column(db.Float); lon = db.Column(db.Float)
    company_id = db.Column(db.Integer)
    zone_id = db.Column(db.Integer)  # opcional: vincular a Zone

class LocationPing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    readings = db.Column(db.JSON, nullable=False)
    estimated_lat = db.Column(db.Float)
    estimated_lon = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
